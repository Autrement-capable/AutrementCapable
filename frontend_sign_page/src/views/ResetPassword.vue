<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  loading.value = true
  error.value = ''
  
  try {
    // here i need to add our reset pass for our backend
    console.log('Reset password for:', email.value)
    success.value = true
  } catch (err) {
    error.value = 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="auth-container">
    <a href="/" class="logo">AutrementCapable</a>
    <h1>Reset Password</h1>
    
    <form v-if="!success" @submit="handleSubmit" class="auth-form" novalidate>
      <p class="description">Enter your email address and we'll send you a link to reset your password</p>
      
      <div class="form-group">
        <label for="email">Email address</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          autocomplete="email"
          aria-required="true"
          aria-describedby="email-error"
          :aria-invalid="error ? 'true' : 'false'"
          placeholder="Enter your email"
        >
      </div>

      <div v-if="error" role="alert" class="error">
        {{ error }}
      </div>

      <button 
        type="submit" 
        :disabled="loading"
        aria-busy="loading"
      >
        {{ loading ? 'Sending reset link...' : 'Send Reset Link' }}
      </button>

      <div class="auth-links">
        <router-link to="/signin">Back to Sign In</router-link>
      </div>
    </form>

    <div v-else role="alert" class="success">
      <h2>Check your email</h2>
      <p>If an account exists for {{ email }}, you will receive a password reset link shortly.</p>
      <div class="auth-links">
        <router-link to="/signin">Back to Sign In</router-link>
      </div>
    </div>
  </main>
</template>