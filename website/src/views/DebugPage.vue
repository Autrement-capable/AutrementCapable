<script setup>
import { ref } from 'vue'
import PopUp from '@/components/PopUp.vue'
import flamou from '@/assets/flamou/intresting.png'

const showPopup = ref(true)
</script>

<template>
  <h1>Debug Page</h1>
  <PopUp
    message="Wow, bien joué ! Est ce que tu veux changer de jeux ?"
    :image="flamou"
    redirect="/"
    buttonConfirm="Non"
    buttonCancel="Oui"
    :visible="showPopup"
    @close="showPopup = false"
  />
</template>

<style scoped></style>
