import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations
  // for more information about preprocessors
  preprocess: vitePreprocess(),

  kit: {
    // adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
    // If your environment is not supported, or you settled on a specific environment, switch out the adapter.
    // See https://svelte.dev/docs/kit/adapters for more information about adapters.
    adapter: adapter(),
    alias: {
      "$lib/core": "src/lib/core",
      "$lib/shared": "src/lib/core/shared",
      "$lib/features": "src/lib/features",
      "$lib/constructor": "src/lib/features/constructor",
      "$lib/components": "src/lib/core",
      "@tka/domain": "src/lib/domain/index.ts",
    },
  },
};

export default config;
