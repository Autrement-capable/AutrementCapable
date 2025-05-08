<template>
  <div class="app">
      <header class="app-header">
        <h1>Picture Service Tester</h1>
        <div class="auth-status">
          <span v-if="isAuthenticated">
            <span class="status-badge authenticated">Authenticated</span>
            <button @click="logout" class="logout-btn">Logout</button>
          </span>
          <span v-else>
            <span class="status-badge not-authenticated">Not Authenticated</span>
            <button @click="showLoginModal = true" class="login-btn">Login</button>
            <button @click="showRegisterModal = true" class="register-btn">Register</button>
          </span>
        </div>
      </header>

      <!-- Main content area -->
      <main class="app-content">
        <div v-if="isAuthenticated">
          <PictureServiceTester />
        </div>
        <div v-else class="login-prompt">
          <h2>Authentication Required</h2>
          <p>Please login or register to test the Picture Service functionality.</p>
          <div class="auth-buttons">
            <button @click="showLoginModal = true" class="login-prompt-btn">Login</button>
            <button @click="showRegisterModal = true" class="register-prompt-btn">Register</button>
          </div>
        </div>
      </main>

      <!-- Login Modal -->
      <div v-if="showLoginModal" class="modal-overlay">
        <div class="login-modal">
          <button class="close-btn" @click="showLoginModal = false">×</button>
          <h2>Login</h2>
          <div class="login-form">
            <div class="form-group">
              <label for="username">Username/Email</label>
              <input type="text" id="username" v-model="credentials.username_or_email" placeholder="Username or Email">
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" v-model="credentials.password" placeholder="Password">
            </div>
            <div class="button-group">
              <button @click="login" :disabled="isLoggingIn" class="login-submit-btn">
                {{ isLoggingIn ? 'Logging in...' : 'Login' }}
              </button>
              <button @click="loginWithPasskey" :disabled="isLoggingIn" class="passkey-btn">
                Login with Passkey
              </button>
            </div>
            <div v-if="loginError" class="error-message">{{ loginError }}</div>
          </div>
        </div>
      </div>

      <!-- Register Modal -->
      <div v-if="showRegisterModal" class="modal-overlay">
        <div class="register-modal">
          <button class="close-btn" @click="showRegisterModal = false">×</button>
          <h2>Register</h2>
          <div class="tabs">
            <button 
              :class="['tab-button', { active: registerMethod === 'password' }]"
              @click="registerMethod = 'password'"
            >
              Traditional
            </button>
            <button 
              :class="['tab-button', { active: registerMethod === 'passkey' }]"
              @click="registerMethod = 'passkey'"
            >
              Passkey
            </button>
          </div>

          <!-- Traditional Registration Form -->
          <div v-if="registerMethod === 'password'" class="register-form">
            <div class="form-group">
              <label for="reg-username">Username</label>
              <input type="text" id="reg-username" v-model="registerData.username" placeholder="Username">
            </div>
            <div class="form-group">
              <label for="reg-email">Email</label>
              <input type="email" id="reg-email" v-model="registerData.email" placeholder="Email">
            </div>
            <div class="form-group">
              <label for="reg-password">Password</label>
              <input type="password" id="reg-password" v-model="registerData.password" placeholder="Password">
            </div>
            <div class="form-group">
              <label for="reg-firstname">First Name</label>
              <input type="text" id="reg-firstname" v-model="registerData.first_name" placeholder="First Name">
            </div>
            <div class="form-group">
              <label for="reg-lastname">Last Name</label>
              <input type="text" id="reg-lastname" v-model="registerData.last_name" placeholder="Last Name">
            </div>
            <div class="form-group">
              <label for="reg-phone">Phone (optional)</label>
              <input type="text" id="reg-phone" v-model="registerData.phone_number" placeholder="Phone Number">
            </div>
            <div class="form-group">
              <label for="reg-address">Address (optional)</label>
              <input type="text" id="reg-address" v-model="registerData.address" placeholder="Address">
            </div>
            <button @click="register" :disabled="isRegistering" class="register-submit-btn">
              {{ isRegistering ? 'Registering...' : 'Register' }}
            </button>
          </div>

          <!-- Passkey Registration Form -->
          <div v-else class="register-form">
            <div class="form-group">
              <label for="pk-firstname">First Name</label>
              <input type="text" id="pk-firstname" v-model="passkeyData.first_name" placeholder="First Name" required>
            </div>
            <div class="form-group">
              <label for="pk-lastname">Last Name</label>
              <input type="text" id="pk-lastname" v-model="passkeyData.last_name" placeholder="Last Name">
            </div>
            <div class="form-group">
              <label for="pk-age">Age</label>
              <input type="number" id="pk-age" v-model.number="passkeyData.age" placeholder="Age">
            </div>
            <div class="form-group">
              <label>Passions (up to 3)</label>
              <div class="passions-inputs">
                <input 
                  v-for="(passion, index) in passkeyData.passions" 
                  :key="index"
                  v-model="passkeyData.passions[index]"
                  placeholder="Enter a passion"
                  :disabled="index > 0 && !passkeyData.passions[index-1]"
                >
              </div>
            </div>
            <div class="form-group">
              <label for="pk-avatar">Avatar (optional)</label>
              <input type="file" id="pk-avatar" @change="handleAvatarChange" accept="image/*">
            </div>
            <button @click="registerWithPasskey" :disabled="isRegistering || !passkeyData.first_name" class="passkey-register-btn">
              {{ isRegistering ? 'Creating Passkey...' : 'Register with Passkey' }}
            </button>
          </div>

          <div v-if="registerError" class="error-message">{{ registerError }}</div>
          <div v-if="registerSuccess" class="success-message">{{ registerSuccess }}</div>
        </div>
      </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import AuthService from './services/AuthService';
import PictureServiceTester from './components/PictureServiceTester.vue';

export default {
  name: 'App',
  components: {
    PictureServiceTester
  },
  setup() {
    const isAuthenticated = ref(false);
    const showLoginModal = ref(false);
    const showRegisterModal = ref(false);
    const isLoggingIn = ref(false);
    const isRegistering = ref(false);
    const loginError = ref('');
    const registerError = ref('');
    const registerSuccess = ref('');
    const registerMethod = ref('password');

    // Login form data
    const credentials = ref({
      username_or_email: '',
      password: ''
    });

    // Traditional registration form data
    const registerData = ref({
      username: '',
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      address: ''
    });

    // Passkey registration form data
    const passkeyData = ref({
      first_name: '',
      last_name: '',
      age: null,
      passions: ['', '', ''],
      avatar: null
    });

    // Check authentication status on mount
    onMounted(() => {
      checkAuth();
      
      // Listen for auth events
      window.addEventListener('auth:login', checkAuth);
      window.addEventListener('auth:logout', checkAuth);
      window.addEventListener('auth:required', () => {
        showLoginModal.value = true;
      });
    });

    // Check if user is authenticated
    const checkAuth = () => {
      isAuthenticated.value = AuthService.isAuthenticated();
    };

    // Handle avatar file selection
    const handleAvatarChange = (event) => {
      passkeyData.value.avatar = event.target.files[0];
    };

    // Login with username/password
    const login = async () => {
      if (!credentials.value.username_or_email || !credentials.value.password) {
        loginError.value = 'Username and password are required';
        return;
      }

      try {
        isLoggingIn.value = true;
        loginError.value = '';
        
        await AuthService.login(credentials.value);
        
        isAuthenticated.value = true;
        showLoginModal.value = false;
        credentials.value = { username_or_email: '', password: '' };
      } catch (error) {
        loginError.value = error.response?.data?.detail || 'Login failed';
      } finally {
        isLoggingIn.value = false;
      }
    };

    // Login with passkey
    const loginWithPasskey = async () => {
      try {
        isLoggingIn.value = true;
        loginError.value = '';
        
        await AuthService.authenticateWithPasskey();
        
        isAuthenticated.value = true;
        showLoginModal.value = false;
      } catch (error) {
        loginError.value = 'Passkey authentication failed';
        console.error(error);
      } finally {
        isLoggingIn.value = false;
      }
    };

    // Register with username/password
    const register = async () => {
      // Validate form
      if (!registerData.value.username || !registerData.value.email || 
          !registerData.value.password || !registerData.value.first_name) {
        registerError.value = 'Username, email, password, and first name are required';
        return;
      }

      try {
        isRegistering.value = true;
        registerError.value = '';
        registerSuccess.value = '';
        
        await AuthService.register(registerData.value);
        
        registerSuccess.value = 'Registration successful! Please check your email to verify your account.';
        // Reset form
        registerData.value = {
          username: '',
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          phone_number: '',
          address: ''
        };
      } catch (error) {
        registerError.value = error.response?.data?.detail || 'Registration failed';
        console.error(error);
      } finally {
        isRegistering.value = false;
      }
    };

    // Register with passkey
    const registerWithPasskey = async () => {
      // Validate form
      if (!passkeyData.value.first_name) {
        registerError.value = 'First name is required';
        return;
      }

      try {
        isRegistering.value = true;
        registerError.value = '';
        registerSuccess.value = '';
        
        // Filter out empty passions
        const filteredPassions = passkeyData.value.passions.filter(passion => passion.trim() !== '');
        
        // Prepare data for passkey registration
        const userData = {
          first_name: passkeyData.value.first_name,
          last_name: passkeyData.value.last_name || undefined,
          age: passkeyData.value.age || undefined,
          passions: filteredPassions.length > 0 ? filteredPassions : undefined,
          avatar: passkeyData.value.avatar || undefined
        };
        
        // Register with passkey
        await AuthService.registerWithPasskey(userData);
        
        // Update authentication status
        isAuthenticated.value = true;
        showRegisterModal.value = false;
        
        // Reset form data
        passkeyData.value = {
          first_name: '',
          last_name: '',
          age: null,
          passions: ['', '', ''],
          avatar: null
        };
      } catch (error) {
        registerError.value = 'Passkey registration failed. Please try again.';
        console.error('Passkey registration error:', error);
      } finally {
        isRegistering.value = false;
      }
    };

    // Logout
    const logout = async () => {
      try {
        await AuthService.logout();
        isAuthenticated.value = false;
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    return {
      isAuthenticated,
      showLoginModal,
      showRegisterModal,
      isLoggingIn,
      isRegistering,
      loginError,
      registerError,
      registerSuccess,
      credentials,
      registerData,
      passkeyData,
      registerMethod,
      login,
      loginWithPasskey,
      register,
      registerWithPasskey,
      handleAvatarChange,
      logout
    };
  }
};
</script>

<style scoped>
.app {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eaeaea;
}

.auth-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 14px;
  margin-right: 10px;
}

.authenticated {
  background-color: #4caf50;
  color: white;
}

.not-authenticated {
  background-color: #f44336;
  color: white;
}

.login-btn, .logout-btn, .register-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  margin-left: 8px;
}

.login-btn:hover, .logout-btn:hover, .register-btn:hover {
  background-color: #0b7dda;
}

.register-btn {
  background-color: #4caf50;
}

.register-btn:hover {
  background-color: #45a049;
}

.logout-btn {
  background-color: #f44336;
}

.logout-btn:hover {
  background-color: #d32f2f;
}

.app-content {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-prompt {
  text-align: center;
  padding: 50px 20px;
}

.login-prompt h2 {
  margin-bottom: 15px;
  color: #333;
}

.login-prompt p {
  margin-bottom: 25px;
  color: #666;
}

.auth-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.login-prompt-btn, .register-prompt-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-prompt-btn:hover, .register-prompt-btn:hover {
  background-color: #0b7dda;
}

.register-prompt-btn {
  background-color: #4caf50;
}

.register-prompt-btn:hover {
  background-color: #45a049;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.login-modal, .register-modal {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.register-modal {
  max-width: 500px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  border: none;
  background: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab-button {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-button:hover {
  background-color: #f5f5f5;
}

.tab-button.active {
  border-bottom-color: #2196f3;
  color: #2196f3;
  font-weight: bold;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.passions-inputs {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.login-submit-btn, .passkey-btn, .register-submit-btn, .passkey-register-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-submit-btn, .register-submit-btn {
  background-color: #4caf50;
  color: white;
}

.login-submit-btn:hover, .register-submit-btn:hover {
  background-color: #45a049;
}

.passkey-btn, .passkey-register-btn {
  background-color: #673ab7;
  color: white;
}

.passkey-btn:hover, .passkey-register-btn:hover {
  background-color: #5e35b1;
}

.login-submit-btn:disabled, .passkey-btn:disabled, 
.register-submit-btn:disabled, .passkey-register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 15px;
  color: #f44336;
  font-size: 14px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.success-message {
  margin-top: 15px;
  color: #4caf50;
  font-size: 14px;
  padding: 10px;
  background-color: #e8f5e9;
  border-radius: 4px;
}
</style>