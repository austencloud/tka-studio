import adapter from "@sveltejs/adapter-netlify";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations
  // for more information about preprocessors
  preprocess: vitePreprocess({
    script: true,
    style: true,
    sourceMap: true, // Enable source maps for Svelte files
    typescript: {
      tsconfigFile: "./tsconfig.json",
      compilerOptions: {
        module: "esnext",
        sourceMap: true, // Enable TypeScript source maps
        inlineSourceMap: false,
        inlineSources: false,
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
      $contracts: "./src/lib/services/contracts",
      "$contracts/*": "./src/lib/services/contracts/*",
      $implementations: "./src/lib/services/implementations",
      "$implementations/*": "./src/lib/services/implementations/*",
      $utils: "./src/lib/utils",
      "$utils/*": "./src/lib/utils/*",
      $state: "./src/lib/state",
      "$state/*": "./src/lib/state/*",
    },
  },
};

export default config;
