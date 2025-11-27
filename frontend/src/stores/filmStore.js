import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useFilmStore = defineStore('film', () => {
  // State
  const selectedFilms = ref([])
  const likedFilms = ref([])
  const dislikedFilms = ref([])
  const recommendations = ref([])
  const popularFilms = ref([])
  const metadata = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const hasSelectedFilms = computed(() => selectedFilms.value.length > 0)
  const canGetRecommendations = computed(() => selectedFilms.value.length >= 1)

  // Actions
  async function fetchPopularFilms(filters = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await api.getPopularFilms(filters)
      popularFilms.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function searchFilms(query) {
    if (!query || query.length < 2) return []
    
    loading.value = true
    error.value = null
    try {
      const data = await api.searchFilms(query)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getSimilarFilms(filmId) {
    loading.value = true
    error.value = null
    try {
      const data = await api.getSimilarFilms(filmId)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRecommendations() {
    if (!canGetRecommendations.value) {
      throw new Error('At least one film must be selected')
    }

    loading.value = true
    error.value = null
    try {
      const data = await api.getRecommendations({
        selected_film_ids: selectedFilms.value.map(f => f.id),
        liked_film_ids: likedFilms.value.map(f => f.id),
        disliked_film_ids: dislikedFilms.value.map(f => f.id),
        limit: 5,
      })
      recommendations.value = data.recommendations
      return data.recommendations
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMetadata() {
    loading.value = true
    error.value = null
    try {
      const data = await api.getMetadata()
      metadata.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  function addSelectedFilm(film) {
    if (!selectedFilms.value.find(f => f.id === film.id)) {
      selectedFilms.value.push(film)
      saveToLocalStorage()
    }
  }

  function removeSelectedFilm(filmId) {
    selectedFilms.value = selectedFilms.value.filter(f => f.id !== filmId)
    saveToLocalStorage()
  }

  function toggleFilmSelection(film) {
    const index = selectedFilms.value.findIndex(f => f.id === film.id)
    if (index !== -1) {
      removeSelectedFilm(film.id)
    } else {
      addSelectedFilm(film)
    }
  }

  function likeFilm(film) {
    // Remove from disliked if present
    dislikedFilms.value = dislikedFilms.value.filter(f => f.id !== film.id)
    
    // Add to liked if not already there
    if (!likedFilms.value.find(f => f.id === film.id)) {
      likedFilms.value.push(film)
      saveToLocalStorage()
    }
  }

  function dislikeFilm(film) {
    // Remove from liked if present
    likedFilms.value = likedFilms.value.filter(f => f.id !== film.id)
    
    // Add to disliked if not already there
    if (!dislikedFilms.value.find(f => f.id === film.id)) {
      dislikedFilms.value.push(film)
      saveToLocalStorage()
    }
  }

  function resetFeedback() {
    likedFilms.value = []
    dislikedFilms.value = []
    saveToLocalStorage()
  }

  function reset() {
    selectedFilms.value = []
    likedFilms.value = []
    dislikedFilms.value = []
    recommendations.value = []
    localStorage.removeItem('movie-recommender-state')
  }

  function saveToLocalStorage() {
    // Désactivé : on ne sauvegarde plus dans localStorage
    // const state = {
    //   selectedFilms: selectedFilms.value,
    //   likedFilms: likedFilms.value,
    //   dislikedFilms: dislikedFilms.value,
    // }
    // localStorage.setItem('movie-recommender-state', JSON.stringify(state))
  }

  function loadFromLocalStorage() {
    const saved = localStorage.getItem('movie-recommender-state')
    if (saved) {
      try {
        const state = JSON.parse(saved)
        selectedFilms.value = state.selectedFilms || []
        likedFilms.value = state.likedFilms || []
        dislikedFilms.value = state.dislikedFilms || []
      } catch (err) {
        console.error('Error loading from localStorage:', err)
      }
    }
  }

  return {
    // State
    selectedFilms,
    likedFilms,
    dislikedFilms,
    recommendations,
    popularFilms,
    metadata,
    loading,
    error,
    
    // Computed
    hasSelectedFilms,
    canGetRecommendations,
    
    // Actions
    fetchPopularFilms,
    searchFilms,
    getSimilarFilms,
    fetchRecommendations,
    fetchMetadata,
    addSelectedFilm,
    removeSelectedFilm,
    toggleFilmSelection,
    likeFilm,
    dislikeFilm,
    resetFeedback,
    reset,
    loadFromLocalStorage,
  }
})
