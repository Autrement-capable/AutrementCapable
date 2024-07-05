<template>
  <div id="app">
    <Login />
  </div>
</template>

<script>
import Login from './components/Login.vue'

export default {
  name: 'App',
  components: {
    Login
  }
}
</script>

<style>
/* You can include global styles here */
body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
}
</style>
