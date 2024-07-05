<script setup>
  import { useRouter } from 'vue-router'
  import { categoriesList } from '../../data/data.js'
  import CategoriesCard from '../CategoriesCard.vue'

  const router = useRouter()

  const categoryClicked = (categoryClicked) => {
    router.push({ name: 'postsList', params: { category: categoryClicked } })
  }
</script>

<template>
  <ul class="cardContainer">
    <li v-for="category in categoriesList" :key="category.nameCode" class="categoriesCard" @click="categoryClicked(category.nameCode)">
      <CategoriesCard :category="category" />
    </li>
  </ul>
</template>

<style scoped>
  .cardContainer {
    list-style: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-bottom: 70px;
  }

  .categoriesCard {
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    width: 70%;
    height: 10%;
    background: #ffffff;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  }

</style>

