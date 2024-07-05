<script setup>
  import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div id="app">
      <Sidebar class="sidebar" />
    <div class="appContent">
      <router-view />
    </div>
  </div>
</template>

<style>

.appContent {
  margin-left: 200px;
  padding-left: 10px;
}
</style>
