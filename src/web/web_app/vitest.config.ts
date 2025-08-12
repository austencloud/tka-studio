/// <reference types="vitest" />
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	// Ensure the browser build of Svelte is used in tests (jsdom),
	// otherwise Vitest may resolve to the server entry leading to
	// `lifecycle_function_unavailable` errors.
	resolve: {
		conditions: ['browser'],
	},
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		environment: 'jsdom',
		setupFiles: ['./vitest-setup.ts'],
		globals: true,
		// Inline Svelte to avoid SSR resolution quirks during Vitest transforms
		deps: {
			inline: ['svelte'],
		},
		alias: {
			$lib: './src/lib',
			$app: './node_modules/@sveltejs/kit/src/runtime/app',
			'@tka/schemas': './src/lib/domain',
		},
	},
});
