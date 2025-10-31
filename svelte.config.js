import adapter from "@sveltejs/adapter-netlify";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://svelte.dev/docs/kit/integrations
  // for more information about preprocessors
  preprocess: vitePreprocess({
    script: true,
    style: true,
    sourceMap: process.env.NODE_ENV !== "production", // Only enable source maps in development
    typescript: {
      tsconfigFile: "./tsconfig.json",
      compilerOptions: {
        module: "esnext",
        sourceMap: process.env.NODE_ENV !== "production", // Only enable TypeScript source maps in development
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

      $Explore: "./src/lib/modules/Explore",
      "$Explore/*": "./src/lib/modules/explore/*",

      $animator: "./src/lib/modules/build/animate",
      "$animator/*": "./src/lib/modules/build/animate/*",

      $wordcard: "./src/lib/modules/word-card",
      "$wordcard/*": "./src/lib/modules/word-card/*",

      $write: "./src/lib/modules/write",
      "$write/*": "./src/lib/modules/write/*",

      $render: "./src/lib/shared/render",
      "$render/*": "./src/lib/shared/render/*",
    },
  },

  // ============================================================================
  // SVELTE 5 HMR CONFIGURATION - Enable hot module replacement
  // ============================================================================
  compilerOptions: {
    hmr: true,
  },
};

export default config;
