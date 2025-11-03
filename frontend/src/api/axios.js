import axios from 'axios'

const api = axios.create({
  // Prefer explicit VITE_API_URL when set at build time. Otherwise use an
  // empty baseURL so code that calls endpoints like `/api/users` will result
  // in a single `/api/...` request (nginx will proxy /api/ to the backend).
  // Using an empty string avoids producing `/api/api/...` when requests
  // already include the `/api` prefix in the app code.
  baseURL: import.meta.env.VITE_API_URL || '',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
