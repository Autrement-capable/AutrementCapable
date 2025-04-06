import axios from 'axios';
import {
  startRegistration,
  startAuthentication
} from '@simplewebauthn/browser';

// Get the server URL from environment variables
const API_URL = process.env.VUE_APP_SERVER_URL || 'http://localhost:5000';

// Create axios instance for authenticated requests
const authAxios = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Important: This ensures cookies are sent with requests
});

// Authentication state
let isRefreshing = false;
let failedQueue = [];
let authMode = 'passkey'; // Default authentication mode: 'passkey' or 'password'

// Helper function to process queue of failed requests after token refresh
const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

const AuthService = {
  // Set the preferred authentication method
  setAuthMode(mode) {
    if (mode === 'passkey' || mode === 'password') {
      authMode = mode;
    } else {
      console.warn('Invalid auth mode. Using default:', authMode);
    }
  },

  // Get current auth mode
  getAuthMode() {
    return authMode;
  },

  // Store access token
  setAccessToken(token) {
    if (token) {
      localStorage.setItem('accessToken', token);
      authAxios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  },

  // Get the current access token
  getAccessToken() {
    return localStorage.getItem('accessToken');
  },

  // Clear tokens on logout
  clearTokens() {
    localStorage.removeItem('accessToken');
    delete authAxios.defaults.headers.common['Authorization'];
  },

  // Register with username/password
  async register(userData) {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, userData);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Login with username/password
  async login(credentials) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, credentials, {
        withCredentials: true, // Important: This ensures the refresh token cookie is saved
      });
      
      // Store access token
      this.setAccessToken(response.data.access_token);
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Logout (both revoke tokens on server and clear local storage)
  async logout() {
    try {
      // Call logout endpoint which will clear the refresh token cookie
      await authAxios.post(`${API_URL}/auth/logout`);
      
      // Clear local storage
      this.clearTokens();
      
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      // Even if server-side logout fails, clear local storage
      this.clearTokens();
      throw error;
    }
  },

  // Refresh access token using HTTP-only refresh token cookie
  async refreshAccessToken() {
    try {
      const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
        withCredentials: true, // Important: Send cookies with the request
      });
      
      // Update the access token
      this.setAccessToken(response.data.access_token);
      
      return response.data.access_token;
    } catch (error) {
      console.error('Token refresh error:', error);
      this.clearTokens();
      throw error;
    }
  },

  // Handle authentication failure
  async handleAuthFailure() {
    this.clearTokens();
    
    // Attempt re-authentication based on preferred mode
    if (authMode === 'passkey') {
      return this.authenticateWithPasskey()
        .catch(() => {
          // If passkey auth fails, emit an event or notify the app
          // This is where you'd typically redirect to login page
          const event = new CustomEvent('auth:required', { 
            detail: { message: 'Authentication required' } 
          });
          window.dispatchEvent(event);
          throw new Error('Authentication required');
        });
    } else {
      // Emit auth required event for password login
      const event = new CustomEvent('auth:required', { 
        detail: { message: 'Authentication required' } 
      });
      window.dispatchEvent(event);
      throw new Error('Authentication required');
    }
  },

  // API request with automatic token refresh
  async fetchWithAuth(config) {
    // Ensure Authorization header is set if we have a token
    const token = this.getAccessToken();
    if (token) {
      config.headers = { 
        ...config.headers,
        Authorization: `Bearer ${token}`
      };
    }

    try {
      return await authAxios(config);
    } catch (error) {
      // If error is not 401 or refreshing is in progress, throw the error
      if (error.response?.status !== 401 || isRefreshing) {
        throw error;
      }

      // If refreshing is not in progress, start refreshing
      if (!isRefreshing) {
        isRefreshing = true;

        try {
          // Try to refresh the token
          const newToken = await this.refreshAccessToken();

          // Update config with new token
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${newToken}`
          };

          // Retry the original request with new token
          isRefreshing = false;
          processQueue(null, newToken);
          return await authAxios(config);
        } catch (refreshError) {
          // If refresh fails, try re-authentication
          isRefreshing = false;
          processQueue(refreshError, null);
          return this.handleAuthFailure();
        }
      } else {
        // If refreshing is in progress, queue this request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(newToken => {
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${newToken}`
          };
          return authAxios(config);
        }).catch(err => {
          throw err;
        });
      }
    }
  },

  // Simpler version for most API calls
  async request(method, url, data = null, options = {}) {
    return this.fetchWithAuth({
      method,
      url,
      data,
      ...options
    });
  },

  // Start passkey registration for new user
  async registerWithPasskey(userData) {
    try {
      // Step 1: Send user data to server and get registration options
      const { data } = await axios.post(`${API_URL}/auth/passkey/registration/start`, userData);

      // Step 2: Use SimpleWebAuthn to create the passkey
      const registrationResponse = await startRegistration(data.options);

      // Step 3: Send the response to server to complete registration
      const completeResponse = await axios.post(`${API_URL}/auth/passkey/registration/complete`, {
        user_id: data.user_id,
        registration_data: registrationResponse,
        challenge: data.options.challenge
      }, {
        withCredentials: true, // Important: This ensures cookies are saved
      });

      // Store access token (refresh token is in HTTP-only cookie)
      this.setAccessToken(completeResponse.data.access_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Authenticate with passkey
  async authenticateWithPasskey() {
    try {
      // Step 1: Get authentication options from server
      const { data } = await axios.post(`${API_URL}/auth/passkey/authentication/start`);

      // Step 2: Format options for SimpleWebAuthn
      const options = {
        challenge: data.options.challenge,
        timeout: data.options.timeout,
        rpId: data.options.rpId || window.location.hostname,
        allowCredentials: (data.options.allowCredentials || []).map(cred => ({
          id: cred.id,
          type: cred.type,
          transports: cred.transports
        })),
        userVerification: data.options.userVerification
      };

      // Step 3: Use SimpleWebAuthn to authenticate
      const authenticationResponse = await startAuthentication(options);

      // Step 4: Send the response to server to complete authentication
      const completeResponse = await axios.post(`${API_URL}/auth/passkey/authentication/complete`, {
        authentication_data: authenticationResponse,
        challenge: data.options.challenge
      }, {
        withCredentials: true, // Important: This ensures cookies are saved
      });

      // Store access token (refresh token is in HTTP-only cookie)
      this.setAccessToken(completeResponse.data.access_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Authentication error:', error);
      throw error;
    }
  },

  // Create a recovery code for the authenticated user
  async createRecoveryCode() {
    try {
      const response = await this.request('get', '/auth/recovery/create-account-recovery');
      return response.data;
    } catch (error) {
      console.error('Recovery code generation error:', error);
      throw error;
    }
  },

  // Use recovery code to register a passkey for an existing account
  async registerWithRecoveryCode(code) {
    try {
      // Step 1: Get registration options using recovery code
      const { data } = await axios.post(`${API_URL}/auth/passkey/rec-acc-passkey`, { code });

      // Step 2: Use SimpleWebAuthn to create the passkey
      const registrationResponse = await startRegistration(data.options);

      // Step 3: Send the response to server to complete registration
      const completeResponse = await axios.post(`${API_URL}/auth/passkey/registration/complete`, {
        user_id: data.user_id,
        registration_data: registrationResponse,
        challenge: data.options.challenge
      }, {
        withCredentials: true, // Important: This ensures cookies are saved
      });

      // Store access token (refresh token is in HTTP-only cookie)
      this.setAccessToken(completeResponse.data.access_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Recovery registration error:', error);
      throw error;
    }
  },

  // Verify email address. Untested requires changes in env file backend
  async verifyEmail(code) {
    try {
      const response = await axios.post(`${API_URL}/auth/verify-code?code=${code}`, {}, {
        withCredentials: true // Important: This ensures cookies are saved
      });

      if (response.data.access_token) {
        this.setAccessToken(response.data.access_token);
      }

      return response.data;
    } catch (error) {
      console.error('Email verification error:', error);
      throw error;
    }
  },

  // Request password reset. Untested
  async requestPasswordReset(email) {
    try {
      const response = await axios.post(`${API_URL}/recovery/request-password-reset`, { email });
      return response.data;
    } catch (error) {
      console.error('Password reset request error:', error);
      throw error;
    }
  },

  // Reset password with token. Untested
  async resetPassword(password, token) {
    try {
      const response = await axios.post(`${API_URL}/recovery/reset-password`, {
        password,
        token
      }, {
        withCredentials: true // Important: This ensures cookies are saved
      });

      if (response.data.access_token) {
        this.setAccessToken(response.data.access_token);
      }

      return response.data;
    } catch (error) {
      console.error('Password reset error:', error);
      throw error;
    }
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getAccessToken();
  },
};

// Set auth header for initial load if token exists
const token = AuthService.getAccessToken();
if (token) {
  authAxios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default AuthService;

// Usage example:
/*
// Import the AuthService
import AuthService from './AuthService';

// Example 1: User Registration with Password
async function registerUser() {
  try {
    const userData = {
      username: 'newuser',
      email: 'user@example.com',
      password: 'securePassword123',
      first_name: 'John',
      last_name: 'Doe',
      phone_number: '+15551234567',
      address: '123 Main St'
    };
    
    const result = await AuthService.register(userData);
    console.log('Registration successful! Check your email to verify your account.');
    return result;
  } catch (error) {
    console.error('Registration failed:', error.response?.data?.detail || error.message);
  }
}

// Example 2: User Registration with Passkey
async function registerWithPasskey() {
  try {
    const userData = {
      first_name: 'John',
      last_name: 'Doe',
      age: 28
    };
    
    const result = await AuthService.registerWithPasskey(userData);
    console.log('Passkey registration successful!', result);
    
    // You're now logged in with the access token automatically set
    // The refresh token is automatically stored in an HTTP-only cookie
    return result;
  } catch (error) {
    console.error('Passkey registration failed:', error);
  }
}

// Example 3: Login with Password
async function loginWithPassword() {
  try {
    const credentials = {
      username_or_email: 'user@example.com',
      password: 'securePassword123'
    };
    
    const result = await AuthService.login(credentials);
    console.log('Login successful!', result);
    
    // You're now logged in with the access token automatically set
    // The refresh token is automatically stored in an HTTP-only cookie
    return result;
  } catch (error) {
    console.error('Login failed:', error.response?.data?.detail || error.message);
  }
}

// Example 4: Login with Passkey
async function loginWithPasskey() {
  try {
    const result = await AuthService.authenticateWithPasskey();
    console.log('Passkey authentication successful!', result);
    
    // You're now logged in with the access token automatically set
    // The refresh token is automatically stored in an HTTP-only cookie
    return result;
  } catch (error) {
    console.error('Passkey authentication failed:', error);
  }
}

// Example 5: Make an Authenticated API Request
async function fetchUserProfile() {
  try {
    // Option 1: Using the request helper method
    const response = await AuthService.request('get', '/api/user/profile');
    console.log('User profile:', response.data);
    
    // Option 2: Using fetchWithAuth for more control
    const detailedResponse = await AuthService.fetchWithAuth({
      method: 'get',
      url: '/api/user/profile',
      params: {
        include_details: true
      }
    });
    console.log('Detailed profile:', detailedResponse.data);
    
    return response.data;
  } catch (error) {
    // If there was an authentication error, you may have been redirected to login
    console.error('Failed to fetch profile:', error.message);
  }
}

// Example 6: Update User Skills
async function updateUserSkills() {
  try {
    const skillsData = {
      skills: {
        empathie: 10,
        initiative: 8,
        communication: 12,
        travail_equipe: 15
      }
    };
    
    const response = await AuthService.request('put', '/skills', skillsData);
    console.log('Skills updated successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to update skills:', error.message);
  }
}

// Example 7: Update User Abilities
async function updateAbilities() {
  try {
    const abilitiesData = {
      abilities: {
        WantToLearn: ["Gestion du stress", "Pensée critique"],
        Unknown: ["Intelligence émotionnelle"],
        Weak: ["Programmation", "Design graphique"],
        Strong: ["Communication écrite", "Recherche"]
      }
    };
    
    const response = await AuthService.request('put', '/abilities', abilitiesData);
    console.log('Abilities updated successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to update abilities:', error.message);
  }
}

// Example 8: Create Account Recovery Code
async function createRecoveryCode() {
  try {
    const result = await AuthService.createRecoveryCode();
    console.log('Recovery code generated:', result.recover_code);
    console.log('Save this code in a safe place. You will need it to recover your account.');
    return result;
  } catch (error) {
    console.error('Failed to generate recovery code:', error.message);
  }
}

// Example 9: Verify Email Address
async function verifyEmailAddress() {
  try {
    // This code would typically come from the URL query parameter
    const verificationCode = 'abc123xyz'; 
    
    const result = await AuthService.verifyEmail(verificationCode);
    console.log('Email verification successful!', result);
    
    // If auto_login was enabled, you're now logged in
    return result;
  } catch (error) {
    console.error('Email verification failed:', error.message);
  }
}

// Example 10: Logout
async function logoutUser() {
  try {
    await AuthService.logout();
    console.log('Logout successful!');
    
    // You're now logged out
    // - Access token has been removed from localStorage
    // - Refresh token cookie has been cleared
    // - Tokens have been revoked on the server
  } catch (error) {
    console.error('Logout failed:', error.message);
  }
}
*/