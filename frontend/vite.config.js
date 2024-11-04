import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    historyApiFallback: true, // Fallback to index.html for all routes
  },
  build: {
    outDir: 'dist', // Set the correct output directory for production
    commonjsOptions: {
      include: [/node_modules/], // Ensure compatibility with commonjs modules
    },
  },
});
