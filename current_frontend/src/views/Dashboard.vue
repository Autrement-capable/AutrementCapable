<script setup lang="ts">
import { ref } from 'vue'

const stats = [
  { name: 'Total Users', value: '1,234' },
  { name: 'Active Topics', value: '56' },
  { name: 'Total Posts', value: '2,345' },
  { name: 'Online Users', value: '42' }
]

const recentActivity = [
  { user: 'John Doe', action: 'created a new topic', time: '5m ago' },
  { user: 'Jane Smith', action: 'replied to "Getting Started"', time: '15m ago' },
  { user: 'Mike Johnson', action: 'liked a post', time: '1h ago' }
]
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in stats" :key="stat.name" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ stat.name }}</h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">{{ stat.value }}</p>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Activity</h2>
        <div class="space-y-4">
          <div v-for="(activity, index) in recentActivity" :key="index" 
               class="flex items-center justify-between py-3 border-b dark:border-gray-700 last:border-0">
            <div>
              <span class="font-medium text-gray-900 dark:text-white">{{ activity.user }}</span>
              <span class="text-gray-500 dark:text-gray-400"> {{ activity.action }}</span>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>