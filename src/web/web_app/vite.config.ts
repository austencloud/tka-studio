import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
/// <reference types="vitest" />

export default defineConfig({
	plugins: [sveltekit()],

	// Optimize dependencies
	optimizeDeps: {
		include: [],
	},

	// Build configuration
	build: {
		sourcemap: true, // Enable source maps for production builds
	},

	// Development server configuration
	server: {
		port: 5174,
		host: 'localhost',
		open: true, // Auto-open browser
	},

	// Path resolution
	resolve: {
		alias: {},
	},

	// Test configuration
	test: {
		globals: true,
		environment: 'jsdom',
		setupFiles: ['src/lib/test/setup.ts'],
	},
});
