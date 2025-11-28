<template>
  <div id="app">
    <div class="lava-lamp-container">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
      <div class="blob blob-4"></div>
      <div class="blob blob-5"></div>
      <div class="blob blob-6"></div>
      <div class="blob blob-7"></div>
      <div class="blob blob-8"></div>
      <div class="blob blob-9"></div>
      <div class="blob blob-10"></div>
      <div class="blob blob-11"></div>
      <div class="blob blob-12"></div>
      <div class="blob blob-13"></div>
      <div class="blob blob-14"></div>
      <div class="blob blob-15"></div>
    </div>
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
