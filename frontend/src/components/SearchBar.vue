<template>
  <div class="search-bar">
    <div class="search-bar__input-wrapper">
      <svg class="search-bar__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      
      <input
        v-model="searchQuery"
        type="text"
        class="search-bar__input"
        :placeholder="placeholder"
        @input="handleInput"
        @focus="showResults = true"
        @blur="handleBlur"
      />
      
      <button
        v-if="searchQuery"
        class="search-bar__clear"
        @click="clearSearch"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    
    <div v-if="showResults && results.length > 0" class="search-bar__results">
      <div
        v-for="film in results"
        :key="film.id"
        class="search-bar__result"
        @mousedown.prevent="selectFilm(film)"
      >
        <img
          v-if="film.poster_url"
          :src="film.poster_url"
          :alt="film.titre"
          class="search-bar__result-poster"
        />
        <div class="search-bar__result-poster-placeholder" v-else>
          🎬
        </div>
        
        <div class="search-bar__result-info">
          <div class="search-bar__result-title">{{ film.titre }}</div>
          <div class="search-bar__result-meta">
            <span v-if="film.annee">{{ film.annee }}</span>
            <span v-if="film.genres && film.genres.length">
              {{ film.genres.slice(0, 2).join(', ') }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="search-bar__loading">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useFilmStore } from '@/stores/filmStore'

const props = defineProps({
  placeholder: {
    type: String,
    default: 'Rechercher un film...',
  },
})

const emit = defineEmits(['select'])

const filmStore = useFilmStore()

const searchQuery = ref('')
const results = ref([])
const showResults = ref(false)
const loading = ref(false)
let searchTimeout = null

const handleInput = () => {
  clearTimeout(searchTimeout)
  
  if (searchQuery.value.length < 2) {
    results.value = []
    return
  }
  
  showResults.value = true // Fix: Ensure results are shown when typing
  loading.value = true
  
  searchTimeout = setTimeout(async () => {
    try {
      showResults.value = true // Fix: Ensure results are shown when search executes
      results.value = await filmStore.searchFilms(searchQuery.value)
    } catch (error) {
      console.error('Search error:', error)
      results.value = []
    } finally {
      loading.value = false
    }
  }, 300) // Debounce 300ms
}

const selectFilm = (film) => {
  emit('select', film)
  searchQuery.value = ''
  results.value = []
  showResults.value = false
}

const clearSearch = () => {
  searchQuery.value = ''
  results.value = []
}

const handleBlur = () => {
  setTimeout(() => {
    showResults.value = false
  }, 200)
}
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 600px;
  /* Chrome optimization */
  transform: translateZ(0);
  will-change: contents;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

.search-bar__input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-bar__icon {
  position: absolute;
  left: var(--spacing-md);
  color: var(--color-text-tertiary);
  pointer-events: none;
  z-index: 2;
}

.search-bar__input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-3xl);
  font-size: var(--font-size-lg);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-full);
  color: var(--color-text-primary);
  outline: none;
  transition: all var(--transition-fast);
  /* Chrome optimization */
  transform: translateZ(0);
  -webkit-font-smoothing: antialiased;
  font-family: var(--font-family-primary);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.search-bar__input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-accent-primary);
  box-shadow: 0 0 0 2px rgba(185, 255, 102, 0.2), 0 8px 30px rgba(0, 0, 0, 0.3);
}

.search-bar__clear {
  position: absolute;
  right: var(--spacing-md);
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  cursor: pointer;
  padding: var(--spacing-xs);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all var(--transition-fast);
  z-index: 2;
}

.search-bar__clear:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.search-bar__results {
  position: absolute;
  top: calc(100% + var(--spacing-sm));
  left: 0;
  right: 0;
  background: rgba(20, 20, 20, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  max-height: 400px;
  overflow-y: auto;
  z-index: 999999;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  padding: var(--spacing-xs);
}

.search-bar__result {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  cursor: pointer;
  transition: background var(--transition-fast);
  border-radius: var(--radius-sm);
  margin-bottom: 2px;
}

.search-bar__result:hover {
  background: rgba(255, 255, 255, 0.1);
}

.search-bar__result-poster {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.search-bar__result-poster-placeholder {
  width: 40px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.search-bar__result-info {
  flex: 1;
  min-width: 0;
}

.search-bar__result-title {
  font-weight: var(--font-weight-medium);
  margin-bottom: 2px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
  color: var(--color-text-primary);
}

.search-bar__result-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  display: flex;
  gap: var(--spacing-md);
}

.search-bar__loading {
  position: absolute;
  right: var(--spacing-3xl);
  top: 50%;
  transform: translateY(-50%);
}
</style>
