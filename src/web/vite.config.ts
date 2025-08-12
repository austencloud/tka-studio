import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  optimizeDeps: {
    include: [
      "clsx",
      "xstate",
      "@xstate/svelte",
      "lucide-svelte",
      "svelte/transition",
      "svelte/store",
      "svelte/motion",
      "html2canvas", // Add html2canvas to the optimized dependencies
      "lz-string", // Add lz-string to the optimized dependencies
    ],
    exclude: [],
    esbuildOptions: {
      logLevel: "error",
    },
    // Force Vite to always optimize dependencies
    force: true,
  },
  // Increase build performance and avoid timeout issues
  build: {
    // Increase chunk size limit to avoid splitting html2canvas
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        // Remove manual chunks for html2canvas as it's causing build issues
        manualChunks: (id) => {
          // Group xstate related modules
          if (id.includes("xstate")) {
            return "xstate-vendor";
          }
          // Group other vendor modules if needed
          if (id.includes("node_modules")) {
            return "vendor";
          }
        },
      },
    },
  },
  // Increase server timeout for dependency optimization
  server: {
    hmr: {
      timeout: 120000, // 120 seconds timeout for HMR
    },
    // Increase the timeout for dependency optimization
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  logLevel: "error",
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
    include: ["src/**/*.test.ts"],
    exclude: ["src/**/*.bench.ts"],
    benchmark: {
      include: ["src/**/*.bench.ts"],
      reporters: ["verbose"],
      outputFile: "./bench/results.json",
    },
  },
});
