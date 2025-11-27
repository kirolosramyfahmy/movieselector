import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default {
  // Films endpoints
  async getPopularFilms(params = {}) {
    const response = await apiClient.get('/films/popular', { params })
    return response.data
  },

  async searchFilms(query, limit = 10) {
    const response = await apiClient.get('/films/search', {
      params: { q: query, limit },
    })
    return response.data
  },

  async getFilmDetails(filmId) {
    const response = await apiClient.get(`/films/${filmId}`)
    return response.data
  },

  async getSimilarFilms(filmId, limit = 2) {
    const response = await apiClient.get(`/films/${filmId}/similar`, {
      params: { limit },
    })
    return response.data
  },

  async getRecommendations(data) {
    const response = await apiClient.post('/films/recommendations', data)
    return response.data
  },

  async getMetadata() {
    const response = await apiClient.get('/films/metadata/info')
    return response.data
  },
}
