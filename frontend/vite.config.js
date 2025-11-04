import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// During local development we proxy API requests to the backend running on
// http://localhost:8000 so the app can call `/api/...` without CORS or
// needing VITE_API_URL. In production the frontend is built with
// VITE_API_URL (or served behind nginx which proxies /api/ to the backend).
export default defineConfig({
  plugins: [react()],
  server: {
    // Forward any request starting with /api to the backend.
    // This keeps the dev environment single-origin and avoids CORS.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path, // keep the /api prefix
      },
    },
  },
})
