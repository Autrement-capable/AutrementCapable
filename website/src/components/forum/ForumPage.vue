<script setup>
  import SideBar from '../SideBar.vue'
  import ForumCategories from './ForumCategories.vue';
</script>

<template>
  <div id="app">
    <SideBar class="sidebar" />
    <div class="appContent">
      <ForumCategories />
    </div>
  </div>
</template>

<style>
.appContent {
  margin-left: 200px;
  padding-left: 10px;
}
</style>
