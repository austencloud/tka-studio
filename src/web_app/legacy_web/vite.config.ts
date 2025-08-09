import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [
    sveltekit(),
    {
      name: "client-log-forwarder",
      apply: "serve",
      configureServer(server) {
        server.middlewares.use("/__client-log", (req, res) => {
          if (req.method !== "POST") {
            res.statusCode = 405;
            res.end("Method Not Allowed");
            return;
          }

          let body = "";
          req.on("data", (chunk) => (body += chunk));
          req.on("end", () => {
            try {
              const payload = JSON.parse(body || "{}");
              const level = payload.level || "log";
              const args = Array.isArray(payload.args) ? payload.args : [payload.args];

              const prefix = "[client]";
              switch (level) {
                case "error":
                  console.error(prefix, ...args);
                  break;
                case "warn":
                  console.warn(prefix, ...args);
                  break;
                case "info":
                  console.info(prefix, ...args);
                  break;
                case "debug":
                  console.debug(prefix, ...args);
                  break;
                default:
                  console.log(prefix, ...args);
              }
            } catch (e) {
              console.error("[client-log] Failed to parse payload:", e);
            }
            res.statusCode = 200;
            res.end("ok");
          });
        });
      },
    },
  ],
  optimizeDeps: {
    include: [
      "clsx",
      "xstate",
      "@xstate/svelte",
      "lucide-svelte",
      "svelte/transition",
      "svelte/store",
      "svelte/motion",
      "html2canvas", // Add html2canvas to the optimized dependencies
      "lz-string", // Add lz-string to the optimized dependencies
    ],
    exclude: [],
    esbuildOptions: {
      logLevel: "error",
    },
    // Force Vite to always optimize dependencies
    force: true,
  },
  // Increase build performance and avoid timeout issues
  build: {
    // Increase chunk size limit to avoid splitting html2canvas
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        // Remove manual chunks for html2canvas as it's causing build issues
        manualChunks: (id) => {
          // Group xstate related modules
          if (id.includes("xstate")) {
            return "xstate-vendor";
          }
          // Group other vendor modules if needed
          if (id.includes("node_modules")) {
            return "vendor";
          }
        },
      },
    },
  },
  // Server configuration with dedicated port and improved static serving
  server: {
    port: 5175,
    host: "localhost",
    hmr: {
      timeout: 120000, // 120 seconds timeout for HMR
    },
    // Increase the timeout for dependency optimization
    watch: {
      usePolling: true,
      interval: 1000,
    },
    // Ensure proper static file serving
    middlewareMode: false,
    fs: {
      strict: false,
      allow: ['..']
    }
  },
  logLevel: "error",
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
    include: ["src/**/*.test.ts"],
    exclude: ["src/**/*.bench.ts"],
    benchmark: {
      include: ["src/**/*.bench.ts"],
      reporters: ["verbose"],
      outputFile: "./bench/results.json",
    },
  },
});
