import { sveltekit } from "@sveltejs/kit/vite";
import fs from "fs";
import type { IncomingMessage, ServerResponse } from "http";
import path from "path";
import type { ViteDevServer, HmrContext } from "vite";
import { defineConfig } from "vite";

const isDev = process.env.NODE_ENV !== "production";

// Custom plugin to force full reload for ALL Svelte files
// This completely disables HMR for Svelte to prevent white screen issues
const forceReloadPlugin = () => ({
  name: "force-reload-svelte",
  handleHotUpdate({ file, server }: HmrContext) {
    // Force full reload for ANY Svelte file or runes state file
    // This is aggressive but prevents the white screen bug
    if (
      file.endsWith(".svelte") ||
      file.endsWith(".svelte.ts") ||
      file.includes("app-state") ||
      file.includes("navigation-state") ||
      file.includes("ui-state")
    ) {
      console.log(`[🔄 Full Reload] ${file.split("\\").pop()}`);
      server.ws.send({
        type: "full-reload",
        path: "*",
      });
      return [];
    }
  },
});

// Custom plugin to serve PNG files from desktop directory
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
          // Decode URL-encoded characters
          const decodedUrl = decodeURIComponent(req.url);
          // Remove leading slash and construct file path
          const relativePath = decodedUrl.substring(1); // Remove leading /
          const filePath = path.resolve(
            "../desktop/data/dictionary",
            relativePath
          );

          // Check if file exists
          if (fs.existsSync(filePath)) {
            // Serve the file
            res.setHeader("Content-Type", "image/png");
            fs.createReadStream(filePath).pipe(res);
            return;
          }
        }
        next();
      }
    );
  },
});

export default defineConfig({
  plugins: [forceReloadPlugin(), sveltekit(), dictionaryPlugin()],

  resolve: {
    alias: {
      // Main project aliases are handled by SvelteKit
    },
  },

  build: {
    sourcemap: true, // Enable source maps to debug the SA variable issue
    minify: false, // Temporarily disable minification to debug the SA variable issue
    rollupOptions: {
      output: {
        // Prevent circular dependency issues
        manualChunks: undefined,
      },
    },
  },

  ssr: {
    noExternal: ["svelte"],
    external: ["pdfjs-dist", "page-flip"],
  },

  esbuild: {
    sourcemap: true,
    keepNames: true,
    target: "es2020", // Use a more conservative target
  },

  // Enable caching for faster subsequent builds
  cacheDir: "node_modules/.vite",

  css: {
    devSourcemap: isDev,
  },

  optimizeDeps: {
    include: [
      "@sveltejs/kit",
      "page-flip",
      "inversify",
      "reflect-metadata",
      "zod",
      "embla-carousel-svelte",
      "dexie",
      "fabric",
      "file-saver",
    ],
    // FIXED: Removed @sveltejs/kit/src/runtime/client/entry.js from exclude
    // Excluding it caused white screen on refresh due to path with spaces
    exclude: ["pdfjs-dist"],
    // Only force re-optimization when dependencies change, not on every start
    force: false,
  },

  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    open: false,
    fs: {
      allow: [".", "../animator", "../desktop"],
      strict: false,
    },
    hmr: {
      port: 5173,
      host: "localhost", // Use localhost instead of 0.0.0.0 for HMR
      clientPort: 5173,
      overlay: true,
      protocol: "ws", // Force WebSocket protocol
      // Add timeout to prevent stale connections
      timeout: 30000,
    },
    cors: true,
    watch: {
      // Use native file watching for better performance
      // Only enable polling if you're on a network file system
      usePolling: false,
      // Ignore node_modules and other large directories
      ignored: ["**/node_modules/**", "**/.git/**", "**/dist/**"],
    },
    // Force page reload on certain events instead of HMR
    middlewareMode: false,
  },

  define: {
    __VITE_IS_MODERN__: true,
  },
});
