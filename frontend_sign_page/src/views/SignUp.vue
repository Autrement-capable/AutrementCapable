<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  loading.value = true
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    loading.value = false
    return
  }
  
  try {
    // here i need to add our sign up for our backend
    console.log('Sign up:', { email: email.value, password: password.value })
  } catch (err) {
    error.value = 'Failed to create account'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="auth-container">
    <a href="/" class="logo">AutrementCapable</a>
    <h1>Join AutrementCapable</h1>
    <p class="description">Create an account to start your inclusive job search</p>
    
    <form @submit="handleSubmit" class="auth-form" novalidate>
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

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          autocomplete="new-password"
          aria-required="true"
          aria-describedby="password-error"
          :aria-invalid="error ? 'true' : 'false'"
          placeholder="Create a password"
        >
      </div>

      <div class="form-group">
        <label for="confirm-password">Confirm Password</label>
        <input
          id="confirm-password"
          v-model="confirmPassword"
          type="password"
          required
          autocomplete="new-password"
          aria-required="true"
          aria-describedby="confirm-password-error"
          :aria-invalid="error ? 'true' : 'false'"
          placeholder="Confirm your password"
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
        {{ loading ? 'Creating your account...' : 'Create Account' }}
      </button>

      <div class="auth-links">
        <router-link to="/signin">Already have an account? Sign in</router-link>
      </div>
    </form>
  </main>
</template>