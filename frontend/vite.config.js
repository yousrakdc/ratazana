import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    historyApiFallback: true,  // Fallback to index.html for all routes
  },
  build: {
    outDir: 'dist',  // Ensure correct build directory for static files
  }
})
