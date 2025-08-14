import { defineConfig } from "vitest/config";
import { sveltekit } from "@sveltejs/kit/vite";

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/lib/test/setup.ts"],
    include: ["src/**/*.{test,spec}.{js,ts}"],
    exclude: ["legacy_app/**/*", "node_modules/**/*"],
    alias: {
      $lib: new URL("./src/lib", import.meta.url).pathname,
      $app: new URL("./src/app", import.meta.url).pathname,
    },
    pool: "forks",
    poolOptions: {
      forks: {
        singleFork: true,
      },
    },
  },
  resolve: {
    conditions: ["browser"],
  },
});
