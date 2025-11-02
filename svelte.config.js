import adapter from "@sveltejs/adapter-netlify";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // ============================================================================
  // PREPROCESSING (Vite handles TypeScript, styles, etc.)
  // ============================================================================
  // 2025: Enable script preprocessing for TypeScript features that emit code
  // (enums, decorators, class visibility modifiers, etc.)
  preprocess: vitePreprocess({ script: true }),

  kit: {
    // ============================================================================
    // ADAPTER (Netlify deployment - 2025 best practice: explicit adapter)
    // ============================================================================
    adapter: adapter({
      // 2025: Use Node-based functions (edge: false is default, more compatible)
      edge: false,
      // 2025: Single function bundle is simpler and often faster for cold starts
      split: false,
    }),

    // ============================================================================
    // PATH ALIASES (Clean domain-bounded architecture)
    // ============================================================================
    alias: {
      // Core aliases
      $lib: "./src/lib",
      "$lib/*": "./src/lib/*",

      // Shared resources (cross-domain access)
      $shared: "./src/lib/shared",
      "$shared/*": "./src/lib/shared/*",

      // Module aliases (for cross-domain barrel imports)
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

    // ============================================================================
    // 2025: SECURITY & PERFORMANCE
    // ============================================================================
    csrf: {
      checkOrigin: true, // 2025: CSRF protection enabled
    },

    // 2025: Preload critical modules for better performance
    prerender: {
      // Configure if you want static prerendering
      crawl: true,
    },
  },

  // ============================================================================
  // SVELTE 5 COMPILER OPTIONS
  // ============================================================================
  compilerOptions: {
    // Svelte 5 runes mode is enabled by default
    // 2025: Runes provide better reactivity and performance
  },
};

export default config;
