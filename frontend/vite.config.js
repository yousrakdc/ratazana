import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    historyApiFallback: true,  // Fallback to index.html for all routes
  },
  build: {
    outDir: 'build',  // Set the correct output directory for production
    rollupOptions: {
      external: ['react-router-dom'],  // Mark react-router-dom as external
    },
  },
});
