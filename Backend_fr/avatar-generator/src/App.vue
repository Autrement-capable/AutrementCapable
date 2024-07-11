<template>
  <div id="app">
    <AvatarGenerator />
  </div>
</template>

<script>
import AvatarGenerator from './components/AvatarGenerator.vue';

export default {
  name: 'App',
  components: {
    AvatarGenerator,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
