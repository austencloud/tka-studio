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

    // Move the path aliases from tsconfig.json to here
    alias: {
      $lib: "./src/lib",
      "$lib/*": "./src/lib/*",
    },
  },
};

export default config;
