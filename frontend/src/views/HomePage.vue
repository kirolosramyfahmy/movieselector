<template>
  <div class="home-page">
    <!-- Section 1: Introduction (Full Screen) -->
    <section id="intro" class="section section--intro">
      <div class="container">
        <div class="intro__content">
          <h2 class="intro__title">Découvrez vos prochains films préférés</h2>
          <p class="intro__description">
            Sélectionnez quelques films que vous adorez, et notre algorithme vous recommandera des pépites similaires.
          </p>
          <button class="btn btn-primary btn-get-started" @click="scrollToSelection">
            <span>Commencer</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- Section 2: Main Application Area -->
    <section id="app-interface" class="section section--app">
      <div class="container app-layout">
        
        <!-- Left Column: Search & Discovery -->
        <div id="selection" class="app-layout__main">
          <div class="selection__header">
            <h2 class="section__title">Explorez le catalogue</h2>
            <p class="section__subtitle">Cherchez et sélectionnez vos films favoris</p>
          </div>

          <!-- Search & Filters -->
          <div class="controls-wrapper">
            <div class="selection__search">
              <SearchBar @select="handleFilmSelect" placeholder="Rechercher un film..." />
            </div>
            
            <div class="selection__filters">
              <FilterPanel @filter="handleFilterChange" />
            </div>
          </div>
          
          <!-- Popular Films Grid -->
          <div class="popular-films">
            <div class="popular-films-header">
              <h2 class="section__title">Films Populaires</h2>
              
              <div class="sort-controls">
                <label for="sort-select">Trier par:</label>
                <select id="sort-select" :value="currentSort" @change="handleSortChange">
                  <option value="recent_popular">Récents & Populaires</option>
                  <option value="popularity">Popularité</option>
                </select>
              </div>
            </div>
            
            <div v-if="loading" class="loading-indicator">
              <div class="spinner"></div>
              <p>Chargement des films...</p>
            </div>
            
            <div v-else class="popular-films__grid" id="popular-films">
              <FilmCard
                v-for="film in popularFilms"
                :key="film.id"
                :film="film"
                :is-selected="isFilmSelected(film.id)"
                @click="handleFilmSelect(film)"
              />
            </div>
            
            <!-- Pagination Controls -->
            <div class="pagination-controls">
              <button 
                class="btn btn-secondary" 
                :disabled="currentPage === 1"
                @click="handlePageChange(currentPage - 1)"
              >
                &larr; Précédent
              </button>
              
              <span class="pagination-info">Page {{ currentPage }}</span>
              
              <button 
                class="btn btn-secondary" 
                :disabled="!hasMore"
                @click="handlePageChange(currentPage + 1)"
              >
                Suivant &rarr;
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column: Sticky Sidebar (Selection) -->
        <aside class="app-layout__sidebar">
          <div class="sidebar-content">
            <div class="selected-films__header">
              <h3 class="selected-films__title">
                Ma Sélection <span class="count">({{ filmStore.selectedFilms.length }})</span>
              </h3>
              <button 
                class="btn btn-primary btn-block"
                @click="getRecommendations"
                :disabled="!filmStore.canGetRecommendations || loading"
              >
                <span v-if="!loading">Lancer la recherche</span>
                <div v-else class="spinner"></div>
              </button>
            </div>

            <div v-if="filmStore.selectedFilms.length === 0" class="empty-state">
              <p>Sélectionnez au moins un film pour commencer</p>
            </div>
            
            <div v-else class="selected-films__list">
              <div v-for="film in filmStore.selectedFilms" :key="film.id" class="selected-film-item">
                <FilmCard
                  :film="film"
                  :is-selected="true"
                  :compact="true"
                  @click="filmStore.removeSelectedFilm(film.id)"
                />
              </div>
            </div>
          </div>
        </aside>

      </div>
    </section>

    <!-- Section 3: Recommendations (Overlay/Modal or Separate Section) -->
    <section 
      v-if="filmStore.recommendations.length > 0" 
      id="recommendations" 
      class="section section--recommendations"
    >
      <div class="container">
        <div class="recommendations-header">
          <h2 class="section__title">Résultats</h2>
          <button class="btn btn-secondary" @click="reset">Nouvelle recherche</button>
        </div>
        
        <div class="recommendations-content" v-if="topRecommendation">
          <!-- Hero Section for Top Recommendation -->
          <div class="recommendation-hero">
            <div class="recommendation-hero__backdrop">
              <img 
                v-if="topRecommendation.poster_url" 
                :src="topRecommendation.poster_url" 
                :alt="topRecommendation.titre"
              />
              <div class="recommendation-hero__overlay"></div>
            </div>
            
            <div class="recommendation-hero__content">
              <div class="recommendation-hero__poster">
                <img 
                  v-if="topRecommendation.poster_url" 
                  :src="topRecommendation.poster_url" 
                  :alt="topRecommendation.titre"
                />
              </div>
              
              <div class="recommendation-hero__info">
                <div class="recommendation-hero__badge">Meilleure Recommandation</div>
                <h3 class="recommendation-hero__title">{{ topRecommendation.titre }}</h3>
                
                <div class="recommendation-hero__meta">
                  <span v-if="topRecommendation.annee" class="meta-item">{{ topRecommendation.annee }}</span>
                  <span v-if="topRecommendation.vote_average" class="meta-item">⭐ {{ topRecommendation.vote_average.toFixed(1) }}</span>
                  <div class="meta-genres">
                    <span v-for="genre in topRecommendation.genres" :key="genre" class="genre-tag">{{ genre }}</span>
                  </div>
                </div>
                
                <p class="recommendation-hero__synopsis" v-if="topRecommendation.overview">
                  {{ topRecommendation.overview }}
                </p>
                
                <div class="recommendation-hero__actions">
                  <button
                    class="btn btn-primary"
                    :class="{ 'active': isLiked(topRecommendation.id) }"
                    @click="handleLike(topRecommendation)"
                  >
                    👍 J'aime ce film
                  </button>
                  
                  <button
                    class="btn btn-secondary"
                    :class="{ 'active': isDisliked(topRecommendation.id) }"
                    @click="handleDislike(topRecommendation)"
                  >
                    👎 Pas pour moi
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Secondary Grid for Other Recommendations -->
          <div class="recommendations-secondary">
            <h3 class="section__subtitle">D'autres films qui pourraient vous plaire</h3>
            <div class="recommendations__grid">
              <div
                v-for="film in otherRecommendations"
                :key="film.id"
                class="recommendation-card"
              >
                <FilmCard
                  :film="film"
                  :show-selection="false"
                />
                
                <div class="recommendation-card__actions">
                  <button
                    class="recommendation-btn recommendation-btn--like"
                    :class="{ 'active': isLiked(film.id) }"
                    @click="handleLike(film)"
                    title="J'aime"
                  >
                    👍
                  </button>
                  
                  <button
                    class="recommendation-btn recommendation-btn--dislike"
                    :class="{ 'active': isDisliked(film.id) }"
                    @click="handleDislike(film)"
                    title="Je n'aime pas"
                  >
                    👎
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFilmStore } from '@/stores/filmStore'
import FilmCard from '@/components/FilmCard.vue'
import SearchBar from '@/components/SearchBar.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import ShareButton from '@/components/ShareButton.vue'

const filmStore = useFilmStore()

const popularFilms = ref([])
const similarFilmsMap = ref({})
const loading = ref(false)
const currentFilters = ref({})
const currentPage = ref(1)
const currentSort = ref('recent_popular') // Default as requested
const hasMore = ref(true) // Simplified for now, ideally backend returns total count

const topRecommendation = computed(() => {
  return filmStore.recommendations.length > 0 ? filmStore.recommendations[0] : null
})

const otherRecommendations = computed(() => {
  return filmStore.recommendations.length > 1 ? filmStore.recommendations.slice(1) : []
})

const isFilmSelected = (filmId) => {
  return filmStore.selectedFilms.some(f => f.id === filmId)
}

const isLiked = (filmId) => {
  return filmStore.likedFilms.some(f => f.id === filmId)
}

const isDisliked = (filmId) => {
  return filmStore.dislikedFilms.some(f => f.id === filmId)
}

const handleFilmSelect = async (film) => {
  filmStore.toggleFilmSelection(film)
  
  // Fetch similar films if film was added
  if (isFilmSelected(film.id) && !similarFilmsMap.value[film.id]) {
    try {
      const similar = await filmStore.getSimilarFilms(film.id)
      similarFilmsMap.value[film.id] = similar
    } catch (error) {
      console.error('Error fetching similar films:', error)
    }
  }
}

const handleFilterChange = async (filters) => {
  currentFilters.value = filters
  await loadPopularFilms(filters)
}

const loadPopularFilms = async (filters = {}) => {
  loading.value = true
  try {
    // Merge filters with pagination and sort
    const params = {
      ...filters,
      page: currentPage.value,
      sort_by: currentSort.value,
      limit: 20
    }
    const results = await filmStore.fetchPopularFilms(params)
    popularFilms.value = results
    
    // Simple check for "has more"
    hasMore.value = results.length === 20
  } catch (error) {
    console.error('Error loading popular films:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = async (newPage) => {
  if (newPage < 1) return
  currentPage.value = newPage
  await loadPopularFilms(currentFilters.value)
  // Scroll to top of grid
  document.getElementById('popular-films')?.scrollIntoView({ behavior: 'smooth' })
}

const handleSortChange = async (event) => {
  currentSort.value = event.target.value
  currentPage.value = 1 // Reset to page 1
  await loadPopularFilms(currentFilters.value)
}

const getRecommendations = async () => {
  loading.value = true
  try {
    await filmStore.fetchRecommendations()
    // Scroll to recommendations
    setTimeout(() => {
      document.getElementById('recommendations')?.scrollIntoView({ 
        behavior: 'smooth' 
      })
    }, 100)
  } catch (error) {
    console.error('Error getting recommendations:', error)
  } finally {
    loading.value = false
  }
}

const handleLike = async (film) => {
  filmStore.likeFilm(film)
  await refineRecommendations()
}

const handleDislike = async (film) => {
  filmStore.dislikeFilm(film)
  await refineRecommendations()
}

const refineRecommendations = async () => {
  loading.value = true
  try {
    await filmStore.fetchRecommendations()
  } catch (error) {
    console.error('Error refining recommendations:', error)
  } finally {
    loading.value = false
  }
}

const reset = () => {
  filmStore.reset()
  similarFilmsMap.value = {}
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToSelection = () => {
  document.getElementById('selection')?.scrollIntoView({ 
    behavior: 'smooth' 
  })
}

onMounted(async () => {
  await loadPopularFilms()
  
  // Load similar films for already selected films
  for (const film of filmStore.selectedFilms) {
    if (!similarFilmsMap.value[film.id]) {
      try {
        const similar = await filmStore.getSimilarFilms(film.id)
        similarFilmsMap.value[film.id] = similar
      } catch (error) {
        console.error('Error fetching similar films:', error)
      }
    }
  }
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* Section Styles */
.section {
  min-height: 100vh;
  padding: var(--spacing-3xl) 0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.section--intro {
  /* Transparent to show global background */
  background: transparent;
}

.section__title {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-xl);
  text-align: left;
  background: linear-gradient(to right, #fff, rgba(255, 255, 255, 0.5));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.section__subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
  font-family: var(--font-family-primary);
}

/* Intro Section */
.intro__content {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
}

/* Abstract decorative glow behind title */
.intro__content::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(185, 255, 102, 0.15) 0%, transparent 70%);
  z-index: -1;
  filter: blur(60px);
  pointer-events: none;
}

.intro__title {
  font-size: var(--font-size-6xl);
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-bold);
  line-height: 1;
  letter-spacing: -0.04em;
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.1);
}

.intro__description {
  font-size: var(--font-size-xl);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-3xl);
  line-height: var(--line-height-relaxed);
  font-family: var(--font-family-primary);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.btn-get-started {
  font-size: var(--font-size-xl);
  padding: var(--spacing-lg) var(--spacing-3xl);
  gap: var(--spacing-md);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-full);
  transition: all var(--transition-normal);
}

.btn-get-started:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
}

/* App Layout */
.app-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: var(--spacing-2xl);
  align-items: start;
  position: relative;
}

.app-layout__main {
  min-width: 0;
}

/* Floating Glass Sidebar */
.app-layout__sidebar {
  position: sticky;
  top: var(--spacing-xl);
  height: calc(100vh - var(--spacing-2xl));
  overflow-y: auto;
  padding: var(--spacing-xl);
  
  /* Glassmorphism */
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Controls */
.controls-wrapper {
  margin-bottom: var(--spacing-3xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.selection__search {
  z-index: 100;
}

/* Sidebar Elements */
.selected-films__header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.selected-films__title {
  font-size: var(--font-size-xl);
  margin: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-primary);
}

.count {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
  font-weight: normal;
}

.selected-films__list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl) 0;
  color: var(--color-text-tertiary);
  font-style: italic;
}

.btn-block {
  width: 100%;
}

/* Grids */
.popular-films__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-lg);
}

.recommendations__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--spacing-xl);
}

/* Pagination & Sort */
.popular-films-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-family: var(--font-family-heading);
  text-transform: uppercase;
  font-size: var(--font-size-sm);
  letter-spacing: 0.05em;
}

.sort-controls select {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: var(--spacing-xs) var(--spacing-md);
  font-family: var(--font-family-primary);
  cursor: pointer;
  outline: none;
  border-radius: var(--radius-full);
  backdrop-filter: blur(5px);
}

.sort-controls select:focus {
  border-color: var(--color-accent-primary);
  background: rgba(255, 255, 255, 0.1);
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-xl);
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-info {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

/* Recommendations Hero */
.recommendation-hero {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border: var(--glass-border);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-3xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.recommendation-hero__backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.4;
}

.recommendation-hero__backdrop img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(40px) saturate(120%);
}

.recommendation-hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(5, 5, 5, 0.9) 0%, rgba(5, 5, 5, 0.4) 100%);
}

.recommendation-hero__content {
  position: relative;
  z-index: 1;
  display: flex;
  gap: var(--spacing-3xl);
  padding: var(--spacing-3xl);
}

.recommendation-hero__poster {
  flex-shrink: 0;
  width: 320px;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transform: rotate(-2deg);
  transition: transform var(--transition-slow);
}

.recommendation-hero:hover .recommendation-hero__poster {
  transform: rotate(0deg) scale(1.02);
}

.recommendation-hero__poster img {
  width: 100%;
  height: auto;
  display: block;
}

.recommendation-hero__info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.recommendation-hero__badge {
  display: inline-block;
  background: var(--color-accent-primary);
  color: #000;
  padding: var(--spacing-xs) var(--spacing-md);
  font-weight: bold;
  text-transform: uppercase;
  font-size: var(--font-size-xs);
  margin-bottom: var(--spacing-lg);
  align-self: flex-start;
  border-radius: var(--radius-full);
  letter-spacing: 0.05em;
  box-shadow: 0 0 15px rgba(185, 255, 102, 0.4);
}

.recommendation-hero__title {
  font-size: var(--font-size-5xl);
  margin-bottom: var(--spacing-lg);
  line-height: 1;
  color: var(--color-text-primary);
  text-shadow: 0 4px 10px rgba(0,0,0,0.5);
}

.recommendation-hero__meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

.meta-genres {
  display: flex;
  gap: var(--spacing-sm);
}

.genre-tag {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4px 12px;
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  border-radius: var(--radius-full);
  backdrop-filter: blur(5px);
}

.recommendation-hero__synopsis {
  font-size: var(--font-size-lg);
  line-height: 1.6;
  margin-bottom: var(--spacing-2xl);
  max-width: 800px;
  font-family: var(--font-family-primary);
  color: rgba(255, 255, 255, 0.9);
}

.recommendation-hero__actions {
  display: flex;
  gap: var(--spacing-md);
}

/* Responsive */
@media (max-width: 1024px) {
  .app-layout {
    grid-template-columns: 1fr;
  }
  
  .app-layout__sidebar {
    position: fixed;
    bottom: var(--spacing-md);
    top: auto;
    left: var(--spacing-md);
    right: var(--spacing-md);
    height: auto;
    max-height: 40vh;
    width: auto;
    z-index: 1000;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 -10px 40px rgba(0,0,0,0.5);
    border-radius: var(--radius-lg);
    background: rgba(10, 10, 10, 0.9);
    backdrop-filter: blur(20px);
  }

  .recommendation-hero__content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: var(--spacing-xl);
  }
  
  .recommendation-hero__poster {
    width: 200px;
    transform: none;
    margin-bottom: var(--spacing-lg);
  }
  
  .recommendation-hero:hover .recommendation-hero__poster {
    transform: none;
  }
  
  .recommendation-hero__actions {
    justify-content: center;
  }
  
  .recommendation-hero__badge {
    align-self: center;
  }
}
</style>
