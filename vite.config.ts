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

/**
 * 🚀 2025 OPTIMIZATION: Aggressive caching for static SVG assets
 * Adds cache headers to SVG files for browser-level performance optimization
 */
const svgCachePlugin = () => ({
  name: "svg-cache-headers",
  configureServer(server: ViteDevServer) {
    server.middlewares.use(
      (
        req: IncomingMessage,
        res: ServerResponse,
        next: (err?: unknown) => void
      ) => {
        // Apply aggressive caching to all SVG files in /images/ directory
        if (req.url && req.url.startsWith("/images/") && req.url.endsWith(".svg")) {
          // Intercept the response to add cache headers
          const originalWriteHead = res.writeHead;
          res.writeHead = function (...args: any[]) {
            // Set aggressive caching for static SVG assets (1 year)
            res.setHeader("Cache-Control", "public, max-age=31536000, immutable");
            res.setHeader("Vary", "Accept-Encoding");
            return originalWriteHead.apply(res, args);
          };
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
  plugins: [
    sveltekit({
      // Explicitly enable HMR and hot module replacement
      hot: {
        preserveLocalState: true,
        injectCss: true,
      },
    }),
    dictionaryPlugin(),
    svgCachePlugin(), // 🚀 2025: Aggressive SVG caching
  ],

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
      "vaul-svelte",
      "bits-ui",
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
      clientPort: 5173, // Explicit client port
      timeout: 30000, // 30s timeout instead of default 5s
    },

    watch: {
      ignored: [
        "**/node_modules/**",
        "**/.git/**",
        "**/dist/**",
        // 🚨 CRITICAL: Use ./build/** NOT **/build/**
        // The pattern **/build/** will match ANY directory named "build" at any depth.
        // This could cause HMR to ignore source code directories.
        // Only ignore the root-level build output directory.
        "./build/**",
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
