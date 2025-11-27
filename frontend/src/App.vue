<template>
  <div id="app">
    <main class="app-main">
      <HomePage />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import HomePage from './views/HomePage.vue'
import { useFilmStore } from './stores/filmStore'

const filmStore = useFilmStore()

onMounted(() => {
  // Désactivé : on ne charge plus les sélections précédentes
  // filmStore.loadFromLocalStorage()
})
</script>

<style scoped>
.app-main {
  min-height: 100vh;
}
</style>
