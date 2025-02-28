<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const success = ref(false)
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  error.value = ''

  try {
    await authStore.resetPassword(email.value)
    success.value = true
  } catch (err) {
    error.value = 'Failed to send reset email'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-200 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white/50 dark:bg-background-dark/50 p-8 rounded-lg shadow-md">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-primary-light dark:text-primary-dark">
          Reset your password
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Enter your email address and we'll send you a link to reset your password.
        </p>
      </div>

      <div v-if="error" class="bg-red-100 dark:bg-red-900 border border-red-400 text-red-700 dark:text-red-200 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <div v-if="success" class="bg-green-100 dark:bg-green-900 border border-green-400 text-green-700 dark:text-green-200 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">Password reset email sent! Check your inbox for further instructions.</span>
      </div>

      <form v-if="!success" class="mt-8 space-y-6" @submit="handleSubmit">
        <div>
          <label for="email-address" class="sr-only">Email address</label>
          <input
            id="email-address"
            name="email"
            type="email"
            autocomplete="email"
            required
            v-model="email"
            class="input-field"
            placeholder="Email address"
          />
        </div>

        <div class="flex items-center justify-between">
          <div class="text-sm">
            <router-link to="/signin" class="font-medium text-secondary-light dark:text-secondary-dark hover:text-purple-500">
              Back to sign in
            </router-link>
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="btn-primary w-full"
          >
            Send Reset Link
          </button>
        </div>
      </form>

      <div v-else class="text-center">
        <router-link to="/signin" class="font-medium text-primary-light dark:text-primary-dark hover:text-purple-500">
          Return to sign in
        </router-link>
      </div>
    </div>
  </div>
</template>