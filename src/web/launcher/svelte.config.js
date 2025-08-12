import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    alias: {
      $lib: "./src/lib",
      $components: "./src/lib/components",
      $stores: "./src/lib/stores",
      $types: "./src/lib/types",
      $services: "./src/lib/services",
    },
  },
};

export default config;
