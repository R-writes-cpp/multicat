import { defineConfig } from 'vite';
import path from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/static/',
  build: {
    outDir: path.resolve(__dirname, './dist'),
    emptyOutDir: false,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        'css': path.resolve(__dirname, './src/main.css.js')
      },
      output: {
        entryFileNames: `js/[name]-bundle.js`,
      },
    },
  }
});
