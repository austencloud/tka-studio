import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],

  // Performance optimizations
  build: {
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Optimize chunk size
    rollupOptions: {
      output: {
        // Manual chunk splitting for better caching
        manualChunks: {
          // Vendor chunks
          vendor: ["svelte"],
        },
      },
    },
    // Enable minification
    minify: "esbuild",
    // Source maps for production debugging
    sourcemap: false,
    // Target modern browsers for smaller bundles
    target: "es2020",
  },

  // Development server optimizations
  server: {
    // Enable HMR
    hmr: true,
    // Faster file watching
    watch: {
      usePolling: false,
    },
  },

  // Dependency optimization
  optimizeDeps: {
    include: ["svelte"],
  },

  // CSS preprocessing
  css: {
    // Enable CSS modules if needed
    modules: false,
    // PostCSS configuration can be added here
    postcss: {},
  },
});
