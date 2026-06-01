// OWNER: MEMBER-1
import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

// Response interceptor: surface error messages consistently.
// TODO (MEMBER-1): when auth is implemented, add a request interceptor that
// attaches the JWT token from wherever it is stored, and a response interceptor
// that redirects to /login on 401.
client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ??
      error.response?.data?.message ??
      error.message ??
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  },
)

export default client
