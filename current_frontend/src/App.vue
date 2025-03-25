<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import { ref, onMounted, watch } from 'vue'

const isDark = ref(false)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  localStorage.setItem('darkMode', isDark.value ? 'dark' : 'light')
  updateTheme()
}

const updateTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('darkMode')
  isDark.value = savedTheme === 'dark'
  updateTheme()
})
</script>

<template>
  <div class="flex min-h-screen bg-background-light text-text-light dark:bg-background-dark dark:text-text-dark transition-colors duration-200">
    <Sidebar :isDark="isDark" @toggle-dark-mode="toggleDarkMode" />
    <main class="flex-1">
      <router-view></router-view>
    </main>
  </div>
</template>