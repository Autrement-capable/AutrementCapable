<script setup lang="ts">
import { onMounted } from "vue";
import { createPixiApp } from "@/assets/main";

onMounted(() => {
  createPixiApp("pixi-container");
});
</script>

<template>
    <div id="pixi-container">
    </div>
</template>

<style scoped>
#pixi-container {
  width: 100%;
  height: 100%;
}
</style>