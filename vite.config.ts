import { sveltekit } from "@sveltejs/kit/vite";
import fs from "fs";
import type { IncomingMessage, ServerResponse } from "http";
import path from "path";
import type { ViteDevServer } from "vite";
import { defineConfig } from "vite";

// ============================================================================
// CUSTOM PLUGINS
// ============================================================================

/**
 * Serves PNG files from desktop directory
 * 2025: Added error handling and proper caching
 */
const dictionaryPlugin = () => ({
  name: "dictionary-files",
  configureServer(server: ViteDevServer) {
    server.middlewares.use(
      "/dictionary",
      (
        req: IncomingMessage,
        res: ServerResponse,
        next: (err?: unknown) => void
      ) => {
        if (req.url && req.url.endsWith(".png")) {
          try {
            const decodedUrl = decodeURIComponent(req.url);
            const relativePath = decodedUrl.substring(1);
            const filePath = path.resolve(
              "../desktop/data/dictionary",
              relativePath
            );

            if (fs.existsSync(filePath)) {
              res.setHeader("Content-Type", "image/png");
              res.setHeader("Cache-Control", "public, max-age=31536000"); // 2025: Better caching
              fs.createReadStream(filePath).pipe(res);
              return;
            }
          } catch (error) {
            console.error("Dictionary file error:", error);
          }
        }
        next();
      }
    );
  },
});

// ============================================================================
// VITE 6.0 CONFIGURATION (2025 - Optimized for SvelteKit 2)
// ============================================================================

export default defineConfig({
  plugins: [sveltekit(), dictionaryPlugin()],

  resolve: {
    alias: {
      // Aliases handled by SvelteKit
    },
  },

  // ============================================================================
  // BUILD (Production optimization)
  // ============================================================================
  build: {
    sourcemap: true,
    target: "esnext",
    minify: "esbuild", // 2025: Fast default minification
    cssMinify: "esbuild", // 2025: Works with Svelte 5

    rollupOptions: {
      output: {
        // Strategic chunking for your actual dependencies
        manualChunks: (id) => {
          if (id.includes("node_modules")) {
            if (id.includes("fabric")) return "vendor-fabric";
            if (id.includes("pdfjs-dist")) return "vendor-pdf";
            if (id.includes("firebase")) return "vendor-firebase";
            if (id.includes("dexie")) return "vendor-dexie";
            return "vendor";
          }
        },
        // 2025: Better cache busting
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]",
      },
    },

    chunkSizeWarningLimit: 1000, // Warn for 1MB+ chunks
  },

  // ============================================================================
  // SSR
  // ============================================================================
  ssr: {
    noExternal: ["svelte"],
    external: ["pdfjs-dist", "page-flip"],
  },

  // ============================================================================
  // CSS
  // ============================================================================
  css: {
    devSourcemap: true,
  },

  // ============================================================================
  // DEPENDENCY PRE-BUNDLING (Vite 6.0)
  // ============================================================================
  optimizeDeps: {
    include: [
      "page-flip",
      "inversify",
      "reflect-metadata",
      "zod",
      "embla-carousel-svelte",
      "dexie",
      "fabric",
      "file-saver",
    ],
    exclude: ["pdfjs-dist"],
  },

  // ============================================================================
  // DEV SERVER (Vite 6.0 enhancements)
  // ============================================================================
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,

    fs: {
      allow: [".", "../animator", "../desktop"],
      strict: true, // 2025: Security best practice
    },

    hmr: {
      overlay: true,
    },

    watch: {
      ignored: [
        "**/node_modules/**",
        "**/.git/**",
        "**/dist/**",
        "**/build/**",
        "**/.svelte-kit/**",
      ],
    },

    // 2025: Preload critical files on dev start
    warmup: {
      clientFiles: [
        "./src/lib/shared/**/*.ts",
        "./src/lib/modules/**/*.svelte",
      ],
    },
  },

  // ============================================================================
  // PREVIEW (Testing production builds)
  // ============================================================================
  preview: {
    port: 4173,
    strictPort: true,
    host: "0.0.0.0",
  },
});
