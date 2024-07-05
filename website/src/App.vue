<template>
  <div id="app" class="app-container">
    <router-view></router-view>
    <AppFooter />
  </div>
</template>

<script>
import AppFooter from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    AppFooter
  }
}
</script>

<style>
@font-face {
  font-family: 'Glacial Indifference';
  src: url('@/assets/fonts/GlacialIndifference-Regular.otf') format('opentype');
  font-weight: normal;
}

@font-face {
  font-family: 'Glacial Indifference';
  src: url('@/assets/fonts/GlacialIndifference-Bold.otf') format('opentype');
  font-weight: bold;
}

body {
  font-family: 'Glacial Indifference', sans-serif;
  padding-top: 0%;
  margin-top: 0%;
}
.app-container {
  padding-bottom: 60px;
}
</style>
