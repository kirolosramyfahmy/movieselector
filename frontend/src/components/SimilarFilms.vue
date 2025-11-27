<template>
  <div class="similar-films">
    <div class="similar-films__header">
      <h4 class="similar-films__title">Films similaires</h4>
    </div>
    
    <div class="similar-films__grid">
      <div
        v-for="film in films"
        :key="film.id"
        class="similar-film-card"
        @click="handleClick(film)"
      >
        <div class="similar-film-card__poster">
          <img
            v-if="film.poster_url"
            :src="film.poster_url"
            :alt="film.titre"
            loading="lazy"
          />
          <div v-else class="similar-film-card__poster-placeholder">
            🎬
          </div>
        </div>
        
        <div class="similar-film-card__info">
          <div class="similar-film-card__title">{{ film.titre }}</div>
          <div class="similar-film-card__year" v-if="film.annee">
            {{ film.annee }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  films: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['select'])

const handleClick = (film) => {
  emit('select', film)
}
</script>

<style scoped>
.similar-films {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-sm);
  animation: fadeInUp var(--transition-base);
  border: 1px solid var(--color-border);
}

.similar-films__header {
  margin-bottom: var(--spacing-md);
}

.similar-films__title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  margin: 0;
}

.similar-films__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.similar-film-card {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-base);
  border: 1px solid transparent;
}

.similar-film-card:hover {
  transform: translateY(-2px);
  border-color: var(--color-accent-primary);
  box-shadow: 4px 4px 0px var(--color-bg-tertiary);
}

.similar-film-card__poster {
  width: 50px;
  height: 75px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--color-bg-tertiary);
  flex-shrink: 0;
  border: 1px solid var(--color-border);
}

.similar-film-card__poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.similar-film-card__poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.similar-film-card__info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.similar-film-card__title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-tight);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: var(--spacing-xs);
}

.similar-film-card__year {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

@media (max-width: 480px) {
  .similar-films__grid {
    grid-template-columns: 1fr;
  }
}
</style>
