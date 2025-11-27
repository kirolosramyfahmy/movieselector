<template>
  <div class="filter-panel" :class="{ 'expanded': isExpanded }">
    <button class="filter-panel__toggle" @click="isExpanded = !isExpanded">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
      </svg>
      <span>Filtres</span>
      <svg 
        class="filter-panel__toggle-icon" 
        :class="{ 'rotated': isExpanded }"
        width="20" 
        height="20" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>
    
    <div v-if="isExpanded" class="filter-panel__content">
      <!-- Genre Filter -->
      <div class="filter-panel__section">
        <label class="filter-panel__label">Genre</label>
        <select 
          v-model="selectedGenre" 
          class="filter-panel__select"
          @change="emitFilters"
        >
          <option value="">Tous les genres</option>
          <option v-for="genre in genres" :key="genre" :value="genre">
            {{ genre }}
          </option>
        </select>
      </div>
      
      <!-- Year Filter -->
      <div class="filter-panel__section">
        <label class="filter-panel__label">Année</label>
        <select 
          v-model="selectedYear" 
          class="filter-panel__select"
          @change="emitFilters"
        >
          <option value="">Toutes les années</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>
      
      <!-- Rating Filter -->
      <div class="filter-panel__section">
        <label class="filter-panel__label">
          Note minimum: {{ minRating }}
        </label>
        <input
          v-model.number="minRating"
          type="range"
          min="0"
          max="10"
          step="0.5"
          class="filter-panel__range"
          @input="emitFilters"
        />
        <div class="filter-panel__range-labels">
          <span>0</span>
          <span>10</span>
        </div>
      </div>
      
      <!-- Reset Button -->
      <button class="filter-panel__reset" @click="resetFilters">
        Réinitialiser les filtres
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFilmStore } from '@/stores/filmStore'

const emit = defineEmits(['filter'])

const filmStore = useFilmStore()

const isExpanded = ref(false)
const selectedGenre = ref('')
const selectedYear = ref('')
const minRating = ref(0)

const genres = computed(() => filmStore.metadata?.genres || [])

const years = computed(() => {
  const metadata = filmStore.metadata
  if (!metadata || !metadata.min_year || !metadata.max_year) return []
  
  const yearList = []
  for (let year = metadata.max_year; year >= metadata.min_year; year--) {
    yearList.push(year)
  }
  return yearList
})

const emitFilters = () => {
  const filters = {}
  
  if (selectedGenre.value) {
    filters.genre = selectedGenre.value
  }
  
  if (selectedYear.value) {
    filters.year = parseInt(selectedYear.value)
  }
  
  if (minRating.value > 0) {
    filters.min_rating = minRating.value
  }
  
  emit('filter', filters)
}

const resetFilters = () => {
  selectedGenre.value = ''
  selectedYear.value = ''
  minRating.value = 0
  emitFilters()
}

onMounted(async () => {
  if (!filmStore.metadata) {
    await filmStore.fetchMetadata()
  }
})
</script>

<style scoped>
.filter-panel {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border);
}

.filter-panel__toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-tertiary);
  border: none;
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
}

.filter-panel__toggle:hover {
  background: var(--color-bg-secondary);
  box-shadow: var(--shadow-glow);
}

.filter-panel__toggle-icon {
  margin-left: auto;
  transition: transform var(--transition-base);
}

.filter-panel__toggle-icon.rotated {
  transform: rotate(180deg);
}

.filter-panel__content {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  animation: fadeInDown var(--transition-base);
}

.filter-panel__section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-panel__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
}

.filter-panel__select {
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
  cursor: pointer;
  outline: none;
  transition: all var(--transition-fast);
  font-family: var(--font-family-primary);
}

.filter-panel__select:focus {
  border-color: var(--color-accent-primary);
}

.filter-panel__range {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-full);
  outline: none;
}

.filter-panel__range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: var(--color-accent-primary);
  border-radius: 0;
  cursor: pointer;
  box-shadow: none;
  transition: all var(--transition-fast);
  border: 2px solid var(--color-bg-primary);
}

.filter-panel__range::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: var(--shadow-glow-hover);
}

.filter-panel__range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: var(--color-accent-primary);
  border-radius: 0;
  cursor: pointer;
  border: 2px solid var(--color-bg-primary);
  box-shadow: none;
  transition: all var(--transition-fast);
}

.filter-panel__range::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: var(--shadow-glow-hover);
}

.filter-panel__range-labels {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

.filter-panel__reset {
  padding: var(--spacing-md);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-panel__reset:hover {
  background: var(--color-accent-primary);
  color: var(--color-bg-primary);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .filter-panel__content {
    padding: var(--spacing-md);
  }
}
</style>
