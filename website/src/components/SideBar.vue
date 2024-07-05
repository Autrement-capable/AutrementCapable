<script setup>
</script>

<template>
  <div class="sidebar">
      <router-link class="title" to="/">Autrement Capable</router-link>
      <router-link to="/forum">Categories</router-link>
      <router-link to="/forum/posts/latest">Latest</router-link>
      <router-link to="/forum/posts/top">Top</router-link>
    </div>
</template>


<style scoped>
  .title {
    font-family: 'Glacial Indifference', sans-serif;
    font-weight: bold;
    font-size: 25px;
  }
  .sidebar {
    width: 170px;
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    background: #fefefe;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  }

  .sidebar a {
    display: block;
    margin: 10px 0;
    color: #333;
    text-decoration: none;
  }

  .sidebar a.router-link-active {
    font-weight: bold;
  }
</style>
