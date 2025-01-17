<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  loading.value = true
  error.value = ''
  
  try {
    // here i need to add our sign in for our backend
    console.log('Sign in:', { email: email.value, password: password.value })
  } catch (err) {
    error.value = 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="auth-container">
    <a href="/" class="logo">AutrementCapable</a>
    <h1>Welcome Back</h1>
    <p class="description">Sign in to access your job search journey</p>
    
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
          autocomplete="current-password"
          aria-required="true"
          aria-describedby="password-error"
          :aria-invalid="error ? 'true' : 'false'"
          placeholder="Enter your password"
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
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>

      <div class="auth-links">
        <router-link to="/reset-password">Forgot your password?</router-link>
        <router-link to="/signup">New to AutrementCapable? Create an account</router-link>
      </div>
    </form>
  </main>
</template>