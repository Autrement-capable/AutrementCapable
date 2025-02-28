<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { HomeIcon, ChatBubbleLeftRightIcon, UserIcon, CogIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const router = useRouter()

const navigation = computed(() => {
  const items = [
    { name: 'Dashboard', icon: HomeIcon, href: '/' },
    { name: 'Forum', icon: ChatBubbleLeftRightIcon, href: '/forum' },
  ]

  if (authStore.isAuthenticated) {
    items.push(
      { name: 'Profile', icon: UserIcon, href: '/profile' },
      { name: 'Settings', icon: CogIcon, href: '/settings' }
    )
  } else {
    items.push({ name: 'Sign In', icon: UserIcon, href: '/signin' })
  }

  return items
})

defineProps<{
  isDark: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle-dark-mode'): void
}>()

const handleLogout = () => {
  authStore.logout()
  router.push('/signin')
}
</script>

<template>
  <aside class="w-64 h-screen bg-white/50 dark:bg-background-dark/50 border-r border-text-light/10 dark:border-text-dark/10 backdrop-blur-sm">
    <div class="px-6 py-4 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-primary-light dark:text-primary-dark">Autrement Capable</h2>
      <button 
        @click="emit('toggle-dark-mode')"
        class="p-2 rounded-lg hover:bg-primary-light/10 dark:hover:bg-primary-dark/10 transition-colors"
        :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      >
        <SunIcon v-if="isDark" class="w-5 h-5 text-text-dark" />
        <MoonIcon v-else class="w-5 h-5 text-text-light" />
      </button>
    </div>
    <nav class="mt-6">
      <router-link
        v-for="item in navigation"
        :key="item.name"
        :to="item.href"
        :class="['sidebar-link']"
      >
        <component :is="item.icon" class="w-6 h-6" />
        {{ item.name }}
      </router-link>
      
      <button
        v-if="authStore.isAuthenticated"
        @click="handleLogout"
        class="sidebar-link w-full text-left"
      >
        <UserIcon class="w-6 h-6" />
        Logout
      </button>
    </nav>
  </aside>
</template>