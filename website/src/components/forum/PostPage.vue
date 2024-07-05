<script setup>
  import { ref, defineProps } from 'vue'
  import { postsList } from '../../data/data.js'

  const props = defineProps(['category', 'id'])
  const postId = parseInt(props.id)
  const post = ref(postsList.find(post => post.id === postId))
</script>

<template>
  <div>
    <h1>{{ post.title }}</h1>
    <p> {{ post.content }}</p>
    <p> Posted at: {{ post.createdAt }}</p>
    <p> Likes: {{ post.likes }}</p>
  </div>
  <ul>
    <li v-for="reply in post.replies" :key="reply.id">
      <p>{{ reply.content }}</p>
      <p>Posted at:{{ reply.createdAt }}</p>
    </li>
  </ul>
</template>

<style scoped>
  ul {
    list-style: none;
  }
</style>
