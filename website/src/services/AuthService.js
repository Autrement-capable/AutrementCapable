import axios from 'axios';
import {
  startRegistration,
  startAuthentication
} from '@simplewebauthn/browser';

// Get the server URL from environment variables
const API_URL = process.env.VUE_APP_SERVER_URL || 'http://localhost:5000';

const AuthService = {
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
      });

      // Store tokens in localStorage
      localStorage.setItem('accessToken', completeResponse.data.access_token);
      localStorage.setItem('refreshToken', completeResponse.data.refresh_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Authenticate with passkey
  async authenticateWithPasskey() {
    try {
      // Step 1: Get authentication options from server and covert to SimpleWebAuthn format
      const { data } = await axios.post(`${API_URL}/auth/passkey/authentication/start`);

      const options = {
        challenge: data.options.challenge,
        timeout: data.options.timeout,
        rpId: data.options.rp_id,              // Convert rp_id to rpId
        allowCredentials: (data.options.allow_credentials || []).map(cred => ({
          id: cred.id,
          type: cred.type,
          transports: cred.transports
        })),
        userVerification: data.options.user_verification  // Convert user_verification to userVerification
      };

      // Step 2: Use SimpleWebAuthn to authenticate
      const authenticationResponse = await startAuthentication(options);

      // Step 3: Send the response to server to complete authentication
      const completeResponse = await axios.post(`${API_URL}/auth/passkey/authentication/complete`, {
        authentication_data: authenticationResponse,
        challenge: data.options.challenge
      });

      // Store tokens in localStorage
      localStorage.setItem('accessToken', completeResponse.data.access_token);
      localStorage.setItem('refreshToken', completeResponse.data.refresh_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Authentication error:', error);
      throw error;
    }
  },

  // Create a recovery code for the authenticated user
  async createRecoveryCode() {
    try {
      const { data } = await axios.get(`${API_URL}/auth/passkey/create-account-recovery`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      });
      return data;
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
      });

      // Store tokens in localStorage
      localStorage.setItem('accessToken', completeResponse.data.access_token);
      localStorage.setItem('refreshToken', completeResponse.data.refresh_token);

      return completeResponse.data;
    } catch (error) {
      console.error('Recovery registration error:', error);
      throw error;
    }
  },
};

export default AuthService;