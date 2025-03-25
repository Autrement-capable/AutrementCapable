<script setup lang="ts">
import { ref } from 'vue'

const user = ref({
  name: 'John Doe',
  email: 'john@example.com',
  avatar: 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y',
  joinDate: 'January 2024',
  role: 'Member'
})

const stats = ref([
  { label: 'Topics Created', value: '23' },
  { label: 'Replies', value: '149' },
  { label: 'Likes Received', value: '320' }
])

const recentActivity = ref([
  { type: 'reply', content: 'Replied to "Best Practices for Vue.js"', date: '2 hours ago' },
  { type: 'topic', content: 'Created "TypeScript Tips and Tricks"', date: '1 day ago' },
  { type: 'like', content: 'Liked "Getting Started with Tailwind"', date: '2 days ago' }
])
</script>

<template>
  <div class="p-6 max-w-4xl mx-auto">
    <!-- Profile Header -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow mb-6">
      <div class="p-6">
        <div class="flex items-center space-x-6">
          <img :src="user.avatar" alt="Profile" class="w-24 h-24 rounded-full" />
          <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ user.name }}</h1>
            <p class="text-gray-600 dark:text-gray-400">{{ user.email }}</p>
            <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
              <span>Joined {{ user.joinDate }}</span>
              <span>•</span>
              <span>{{ user.role }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div v-for="stat in stats" :key="stat.label" 
           class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ stat.label }}</h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Activity</h2>
        <div class="space-y-4">
          <div v-for="(activity, index) in recentActivity" :key="index"
               class="flex items-center justify-between py-3 border-b dark:border-gray-700 last:border-0">
            <div class="flex items-center space-x-3">
              <div class="text-gray-900 dark:text-white">{{ activity.content }}</div>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ activity.date }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings Section -->
    <div class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Profile Settings</h2>
        <form class="space-y-4">
          <div>
            <label for="display-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Display Name</label>
            <input type="text" id="display-name" name="display-name" 
                   class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                   :value="user.name" />
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
            <input type="email" id="email" name="email" 
                   class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                   :value="user.email" />
          </div>
          <div class="pt-4">
            <button type="submit" 
                    class="inline-flex justify-center py-2 px-4 btn-primary">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>