// OWNER: MEMBER-1
import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

// Attach stored token on every request (AuthContext also sets the default
// header, but this interceptor covers requests made before context mounts).
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('upkeep_token')
  if (token) config.headers['Authorization'] = `Bearer ${token}`
  return config
})

// Normalise error messages and handle 401 globally.
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Let the AuthContext handle the actual logout; just clear storage here
      // so that the next request doesn't retry with a dead token.
      localStorage.removeItem('upkeep_token')
      delete client.defaults.headers.common['Authorization']
      // Only redirect if we're not already on the login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    const message =
      error.response?.data?.detail ??
      error.response?.data?.message ??
      error.message ??
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  },
)

export default client
