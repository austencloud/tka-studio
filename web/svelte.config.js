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

    // Clean domain-bounded aliases - relative imports within domains, barrels for cross-domain
    alias: {
      // ============================================================================
      // CORE ALIASES
      // ============================================================================
      $lib: "./src/lib",
      "$lib/*": "./src/lib/*",

      // ============================================================================
      // SHARED RESOURCES (Cross-domain access)
      // ============================================================================
      $shared: "./src/lib/shared",
      "$shared/*": "./src/lib/shared/*",

      // ============================================================================
      // MODULE ALIASES (For cross-domain barrel imports)
      // ============================================================================
      $build: "./src/lib/modules/build",
      "$build/*": "./src/lib/modules/build/*",

      $learn: "./src/lib/modules/learn",
      "$learn/*": "./src/lib/modules/learn/*",

      $browse: "./src/lib/modules/browse",
      "$browse/*": "./src/lib/modules/browse/*",

      $animator: "./src/lib/modules/animator",
      "$animator/*": "./src/lib/modules/animator/*",

      $wordcard: "./src/lib/modules/word-card",
      "$wordcard/*": "./src/lib/modules/word-card/*",

      $write: "./src/lib/modules/write",
      "$write/*": "./src/lib/modules/write/*",
    },
  },
};

export default config;
