import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],

  // Simple Windows optimization to prevent EPERM errors
  server: {
    watch: {
      // Use polling on Windows to avoid file lock issues
      usePolling: true,
      interval: 300,
    },
  },
});
