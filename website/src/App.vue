<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
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
}
</style>
