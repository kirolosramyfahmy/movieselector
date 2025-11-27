<template>
  <div class="share-button">
    <button class="btn btn-secondary" @click="toggleMenu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="18" cy="5" r="3"></circle>
        <circle cx="6" cy="12" r="3"></circle>
        <circle cx="18" cy="19" r="3"></circle>
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
      </svg>
      Partager
    </button>
    
    <div v-if="showMenu" class="share-menu">
      <button class="share-menu__item" @click="shareToTwitter">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path>
        </svg>
        Twitter
      </button>
      
      <button class="share-menu__item" @click="shareToMastodon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M23.193 7.879c0-5.206-3.411-6.732-3.411-6.732C18.062.357 15.108.025 12.041 0h-.076c-3.068.025-6.02.357-7.74 1.147 0 0-3.411 1.526-3.411 6.732 0 1.192-.023 2.618.015 4.129.124 5.092.934 10.109 5.641 11.355 2.17.574 4.034.695 5.535.612 2.722-.15 4.25-.972 4.25-.972l-.09-1.975s-1.945.613-4.129.539c-2.165-.074-4.449-.233-4.799-2.891a5.499 5.499 0 0 1-.048-.745s2.125.52 4.817.643c1.646.075 3.19-.097 4.758-.283 3.007-.359 5.625-2.212 5.954-3.905.517-2.665.475-6.507.475-6.507zm-4.024 6.709h-2.497V8.469c0-1.29-.543-1.944-1.628-1.944-1.2 0-1.802.776-1.802 2.312v3.349h-2.483v-3.35c0-1.536-.602-2.312-1.802-2.312-1.085 0-1.628.655-1.628 1.944v6.119H4.832V8.284c0-1.289.328-2.313.987-3.07.68-.758 1.569-1.147 2.674-1.147 1.278 0 2.246.491 2.886 1.474L12 6.585l.622-1.044c.64-.983 1.608-1.474 2.886-1.474 1.104 0 1.994.389 2.674 1.147.658.757.986 1.781.986 3.07v6.304z"/>
        </svg>
        Mastodon
      </button>
      
      <button class="share-menu__item" @click="copyLink">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
          <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
        </svg>
        {{ copied ? 'Copié !' : 'Copier le lien' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  films: {
    type: Array,
    default: () => [],
  },
})

const showMenu = ref(false)
const copied = ref(false)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const shareToTwitter = () => {
  const filmTitles = props.films.slice(0, 3).map(f => f.titre).join(', ')
  const text = `Découvrez mes recommandations de films : ${filmTitles}...`
  const url = window.location.href
  const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`
  window.open(twitterUrl, '_blank')
  showMenu.value = false
}

const shareToMastodon = () => {
  const filmTitles = props.films.slice(0, 3).map(f => f.titre).join(', ')
  const text = `Découvrez mes recommandations de films : ${filmTitles}...`
  const url = window.location.href
  const mastodonText = `${text} ${url}`
  
  // Open Mastodon share (user will need to enter their instance)
  const mastodonUrl = `https://mastodon.social/share?text=${encodeURIComponent(mastodonText)}`
  window.open(mastodonUrl, '_blank')
  showMenu.value = false
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => {
      copied.value = false
      showMenu.value = false
    }, 2000)
  } catch (error) {
    console.error('Failed to copy link:', error)
  }
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.share-button')) {
    showMenu.value = false
  }
})
</script>

<style scoped>
.share-button {
  position: relative;
}

.share-menu {
  position: absolute;
  bottom: calc(100% + var(--spacing-sm));
  right: 0;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-accent-primary);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  min-width: 200px;
  box-shadow: 4px 4px 0px var(--color-bg-tertiary);
  z-index: var(--z-dropdown);
  animation: fadeInUp var(--transition-base);
}

.share-menu__item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  font-family: var(--font-family-primary);
}

.share-menu__item:hover {
  background: var(--color-accent-primary);
  color: var(--color-bg-primary);
  transform: translateX(-4px);
}

@media (max-width: 768px) {
  .share-menu {
    right: auto;
    left: 0;
  }
}
</style>
