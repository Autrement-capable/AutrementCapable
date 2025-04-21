<template>
  <div class="wrapper">
    <form @submit.prevent="handleLogin">
      <h1>Login</h1>
      
      <div class="input-box">
        <input 
          type="text" 
          placeholder="Username" 
          v-model="credentials.username_or_email" 
          required 
          :disabled="isLoading" 
        />
        <i class="bx bxs-user"></i>
      </div>
      
      <div class="input-box">
        <input 
          type="password" 
          placeholder="Password" 
          v-model="credentials.password" 
          required 
          :disabled="isLoading" 
        />
        <i class="bx bxs-lock-alt"></i>
      </div>
      
      <div class="error-message" v-if="errorMessage">
        {{ errorMessage }}
      </div>
      
      <div class="remember-forgot">
        <label>
          <input type="checkbox" v-model="rememberMe" />Remember me
        </label>
        <a href="#" @click.prevent="goToPasswordReset">Forgot Password</a>
      </div>
      
      <button type="submit" class="btn" :disabled="isLoading">
        <span v-if="isLoading">Loading...</span>
        <span v-else>Login</span>
      </button>
      
      <button 
        v-if="supportsPasskeys" 
        type="button" 
        @click="loginWithPasskey" 
        class="btn passkey-btn" 
        :disabled="isLoading"
      >
        <span v-if="isPasskeyLoading">Loading...</span>
        <span v-else>Login with Passkey</span>
      </button>
      
      <div class="register-link">
        <p>Don't have an account? <a href="#" @click.prevent="goToRegister">Register Here</a></p>
      </div>
    </form>
  </div>
</template>

<script>
import AuthService from '@/services/AuthService';
import { browserSupportsWebAuthn } from '@simplewebauthn/browser';

export default {
  name: 'LoginPage',
  data() {
    return {
      credentials: {
        username_or_email: '',
        password: ''
      },
      rememberMe: false,
      isLoading: false,
      isPasskeyLoading: false,
      errorMessage: '',
      supportsPasskeys: false
    }
  },
  mounted() {
    // Check if browser supports WebAuthn/passkeys
    try {
      this.supportsPasskeys = browserSupportsWebAuthn();
    } catch (error) {
      console.error('Error checking WebAuthn support:', error);
      this.supportsPasskeys = false;
    }
    
    // Pre-fill username if remembered
    const rememberedUsername = localStorage.getItem('remembered_username');
    if (rememberedUsername) {
      this.credentials.username_or_email = rememberedUsername;
      this.rememberMe = true;
    }
  },
  methods: {
    async handleLogin() {
      if (this.isLoading) return;
      
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        // Call login method from AuthService
        await AuthService.login(this.credentials);
        
        // Save username if remember me is checked
        if (this.rememberMe) {
          localStorage.setItem('remembered_username', this.credentials.username_or_email);
        } else {
          localStorage.removeItem('remembered_username');
        }
        
        // Redirect to dashboard
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.detail || 'Invalid username or password';
      } finally {
        this.isLoading = false;
      }
    },
    
    async loginWithPasskey() {
      if (this.isPasskeyLoading) return;
      
      this.isPasskeyLoading = true;
      this.errorMessage = '';
      
      try {
        // Use passkey authentication
        await AuthService.authenticateWithPasskey();
        
        // Redirect to dashboard
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Passkey login error:', error);
        this.errorMessage = 'Passkey authentication failed. Please try again or use password.';
      } finally {
        this.isPasskeyLoading = false;
      }
    },
    
    goToPasswordReset() {
      this.$router.push('/password-reset');
    },
    
    goToRegister() {
      this.$router.push('/account-creation');
    }
  }
}
</script>

<style scoped>
.wrapper {
  background: url('../assets/img.jpg') no-repeat;
  background-size: cover;
  background-position: center;
  width: 420px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(40px);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 30px 40px;
}

.wrapper h1 {
  font-size: 36px;
  text-align: center;
}

.wrapper .input-box {
  width: 100%;
  height: 50px;
  margin: 30px 0;
  position: relative;
}

.input-box input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 40px;
  font-size: 16px;
  padding: 20px 45px 20px 20px;
}

.input-box i {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
}

.wrapper .remember-forgot {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin: 15px 0 15px;
}

.remember-forgot label input {
  accent-color: #fff;
  margin-right: 3px;
}

.remember-forgot a {
  text-decoration: none;
}

.remember-forgot a:hover {
  text-decoration: underline;
}

.wrapper .btn {
  width: 100%;
  height: 50px;
  background: #fff;
  border: none;
  outline: none;
  border-radius: 40px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 16px;
  color: #333;
  font-weight: 600;
  margin: 20px 0;
}

.wrapper .btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.passkey-btn {
  background: rgba(255, 255, 255, 0.8);
  margin-top: 0;
}

.wrapper .register-link {
  font-size: 14.5px;
  text-align: center;
  margin: 20px 0 15px;
}

.register-link p a {
  text-decoration: none;
  font-weight: 600;
}

.register-link p a:hover {
  text-decoration: underline;
}

.error-message {
  color: #ff5555;
  text-align: center;
  font-size: 14px;
  padding: 5px;
  background-color: rgba(255, 0, 0, 0.1);
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>