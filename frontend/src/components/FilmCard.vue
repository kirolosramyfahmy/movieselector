<template>
  <div 
    class="film-card" 
    :class="{ 'selected': isSelected, 'film-card--compact': compact }"
    @click="handleClick"
  >
    <div class="film-card__poster">
      <img 
        v-if="film.poster_url" 
        :src="film.poster_url" 
        :alt="film.titre"
        class="film-card__image"
        loading="lazy"
      />
      <div v-else class="film-card__poster-placeholder">
        <span>🎬</span>
      </div>
      
      <div v-if="showSelection" class="film-card__overlay">
        <div class="film-card__check">
          <svg v-if="isSelected" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
          </svg>
        </div>
      </div>
    </div>
    
    <div class="film-card__content">
      <h3 class="film-card__title">{{ film.titre }}</h3>
      <div class="film-card__meta">
        <span v-if="film.annee" class="film-card__year">{{ film.annee }}</span>
        <span v-if="film.vote_average" class="film-card__rating">
          ⭐ {{ film.vote_average.toFixed(1) }}
        </span>
      </div>
      <div v-if="film.genres && film.genres.length" class="film-card__genres">
        <span 
          v-for="genre in film.genres.slice(0, 2)" 
          :key="genre"
          class="film-card__genre"
        >
          {{ genre }}
        </span>
      </div>
      
      <p v-if="film.overview" class="film-card__overview">
        {{ film.overview }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  film: {
    type: Object,
    required: true,
  },
  isSelected: {
    type: Boolean,
    default: false,
  },
  showSelection: {
    type: Boolean,
    default: true,
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const handleClick = () => {
  emit('click', props.film)
}
</script>

<style scoped>
.film-card {
  position: relative;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--color-bg-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
}

.film-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), var(--shadow-glow);
  z-index: 10;
}

.film-card__poster {
  position: relative;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: #000000; /* Black background for letterboxing */
}

.film-card__image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Ensure full image is visible */
  object-position: center;
  transition: transform var(--transition-slow);
}

.film-card:hover .film-card__image {
  transform: scale(1.05);
}

.film-card__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9) 0%, transparent 60%);
  opacity: 0.6;
  transition: opacity var(--transition-normal);
}

.film-card:hover .film-card__overlay {
  opacity: 0.8;
}

.film-card__actions {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  display: flex;
  gap: var(--spacing-xs);
  opacity: 0;
  transform: translateY(-10px);
  transition: all var(--transition-normal);
}

.film-card:hover .film-card__actions {
  opacity: 1;
  transform: translateY(0);
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--color-text-primary);
  color: var(--color-bg-primary);
  transform: scale(1.1);
}

.action-btn.active {
  background: var(--color-accent-primary);
  color: var(--color-bg-primary);
}

.film-card__content {
  padding: var(--spacing-md);
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(to bottom, rgba(255,255,255,0.02), transparent);
}

.film-card__title {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xs);
  line-height: 1.3;
  color: var(--color-text-primary);
  font-weight: var(--font-weight-bold);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.film-card__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.film-card__rating {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-accent-primary);
  font-weight: var(--font-weight-medium);
}

.film-card__genres {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: auto;
}

.genre-tag {
  font-size: 0.7rem;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.film-card__overview {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  margin-top: var(--spacing-sm);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  opacity: 0.8;
}

/* Selected State */
.film-card--selected {
  border-color: var(--color-accent-primary);
  box-shadow: 0 0 20px rgba(185, 255, 102, 0.2);
}

.film-card__check {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  width: 24px;
  height: 24px;
  background: var(--color-accent-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-bg-primary);
  z-index: 2;
  box-shadow: 0 0 10px rgba(185, 255, 102, 0.5);
}

/* Compact Mode (Sidebar) */
.film-card--compact {
  flex-direction: row;
  height: 80px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.film-card--compact:hover {
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.05);
}

.film-card--compact .film-card__poster {
  width: 60px;
  aspect-ratio: auto;
  height: 100%;
}

.film-card--compact .film-card__content {
  padding: var(--spacing-sm) var(--spacing-md);
  justify-content: center;
  background: none;
}

.film-card--compact .film-card__title {
  font-size: var(--font-size-base);
  margin-bottom: 2px;
  -webkit-line-clamp: 1;
  line-height: 1.5;
  padding-top: 4px;
}

.film-card--compact .film-card__meta {
  margin-bottom: 0;
  font-size: var(--font-size-xs);
}

.film-card--compact .film-card__genres,
.film-card--compact .film-card__overlay,
.film-card--compact .film-card__actions,
.film-card--compact .film-card__overview {
  display: none;
}

.film-card--compact .film-card__remove {
  position: absolute;
  right: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity var(--transition-fast);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  cursor: pointer;
}

.film-card--compact:hover .film-card__remove {
  opacity: 1;
}

.film-card--compact .film-card__remove:hover {
  background: var(--color-error);
  color: white;
}
</style>
