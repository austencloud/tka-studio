import adapter from "@sveltejs/adapter-netlify";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations
  // for more information about preprocessors
  preprocess: vitePreprocess({
    script: true,
    typescript: {
      tsconfigFile: "./tsconfig.json",
      compilerOptions: {
        module: "esnext",
      },
    },
  }),

  kit: {
    // adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
    // If your environment is not supported, or you settled on a specific environment, switch out the adapter.
    // See https://svelte.dev/docs/kit/adapters for more information about adapters.
    adapter: adapter(),

    // Prerender SEO pages for better search engine crawling
    prerender: {
      entries: ["*", "/about", "/features", "/getting-started", "/browse"],
    },

    // Move the path aliases from tsconfig.json to here
    alias: {
      $lib: "./src/lib",
      "$lib/*": "./src/lib/*",
      $components: "./src/lib/components",
      "$components/*": "./src/lib/components/*",
      $domain: "./src/lib/domain",
      "$domain/*": "./src/lib/domain/*",
      $services: "./src/lib/services",
      "$services/*": "./src/lib/services/*",
      $stores: "./src/lib/stores",
      "$stores/*": "./src/lib/stores/*",
      $utils: "./src/lib/utils",
      "$utils/*": "./src/lib/utils/*",
    },
  },
};

export default config;
