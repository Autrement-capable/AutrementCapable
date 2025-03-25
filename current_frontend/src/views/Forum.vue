<script setup lang="ts">
import { ref } from 'vue'

const topics = ref([
  {
    id: 1,
    title: 'Getting Started with Vue.js',
    author: 'John Doe',
    replies: 23,
    views: 156,
    lastActivity: '2h ago'
  },
  {
    id: 2,
    title: 'Best Practices for Tailwind CSS',
    author: 'Jane Smith',
    replies: 15,
    views: 98,
    lastActivity: '4h ago'
  },
  {
    id: 3,
    title: 'TypeScript Tips and Tricks',
    author: 'Mike Johnson',
    replies: 34,
    views: 245,
    lastActivity: '1d ago'
  }
])
</script>

<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Forum</h1>
      <button class="px-4 py-2 btn-primary">
        New Topic
      </button>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <div class="min-w-full">
        <div class="bg-gray-50 dark:bg-gray-700 border-b dark:border-gray-600">
          <div class="grid grid-cols-12 px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
            <div class="col-span-6">Topic</div>
            <div class="col-span-2">Author</div>
            <div class="col-span-1">Replies</div>
            <div class="col-span-1">Views</div>
            <div class="col-span-2">Last Activity</div>
          </div>
        </div>

        <div class="divide-y divide-gray-200 dark:divide-gray-700">
          <div v-for="topic in topics" :key="topic.id" 
               class="grid grid-cols-12 px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
            <div class="col-span-6">
              <div class="text-sm font-medium text-primary-light dark:text-primary-dark">{{ topic.title }}</div>
            </div>
            <div class="col-span-2">
              <div class="text-sm text-gray-900 dark:text-gray-300">{{ topic.author }}</div>
            </div>
            <div class="col-span-1">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ topic.replies }}</div>
            </div>
            <div class="col-span-1">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ topic.views }}</div>
            </div>
            <div class="col-span-2">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ topic.lastActivity }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>