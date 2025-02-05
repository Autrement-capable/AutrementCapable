<template>
  <footer class="app-footer">
    <p>&copy; 2024 Autrement Capable. Tous droits réservés.‎ ‎ ‎ ‎ ‎ </p>
    <p><a href="/forum" class="forum-link">Visitez notre forum</a></p>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.app-footer {
  align-items: center;
  justify-content: center;
  display: flex;
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 1em 0;
  position: fixed;
  width: 100%;
  bottom: 0;
}

.forum-link {
  color: #fff;
  text-decoration: underline;
}

.forum-link:hover {
  text-decoration: none;
}
</style>
