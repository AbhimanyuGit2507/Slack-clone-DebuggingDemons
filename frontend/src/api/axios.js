import axios from 'axios'

const api = axios.create({
  // Use VITE_API_URL if set, otherwise default to FastAPI backend for local dev
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
