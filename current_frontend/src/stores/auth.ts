import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)

  function login(email: string, password: string) {
    return new Promise((resolve, reject) => {
      if (email && password) {
        isAuthenticated.value = true
        user.value = { email }
        resolve(true)
      } else {
        reject(new Error('Invalid credentials'))
      }
    })
  }

  function logout() {
    isAuthenticated.value = false
    user.value = null
  }

  function signup(email: string, password: string) {
    // Mock implementation
    return new Promise((resolve) => {
      isAuthenticated.value = true
      user.value = { email }
      resolve(true)
    })
  }

  function resetPassword(email: string) {
    // Mock implementation
    return new Promise((resolve) => {
      resolve(true)
    })
  }

  return {
    isAuthenticated,
    user,
    login,
    logout,
    signup,
    resetPassword
  }
})