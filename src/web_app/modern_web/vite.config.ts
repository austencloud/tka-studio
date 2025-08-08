import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
/// <reference types="vitest" />

export default defineConfig({
	plugins: [
		sveltekit()
	],
	
	// Optimize dependencies
	optimizeDeps: {
		include: ['@tka/schemas', '@tka/shared']
	},
	
	// Build configuration
	build: {
		rollupOptions: {
			output: {
				manualChunks: {
					'tka-core': ['@tka/schemas', '@tka/shared'],
					'pictograph': ['src/lib/components/pictograph'],
					'sequence': ['src/lib/components/sequence']
				}
			}
		}
	},
	
	// Development server configuration
	server: {
		port: 5174,
		host: 'localhost',
		open: true, // Auto-open browser
		fs: {
			allow: ['..'] // Allow access to parent directories for shared modules
		}
	},
	
	// Path resolution
	resolve: {
		alias: {
			'@tka/schemas': '../../../schemas/generated-types.ts',
			'@tka/shared': '../shared'
		}
	},
	
	// Test configuration
	test: {
		globals: true,
		environment: 'jsdom',
		setupFiles: ['src/lib/test/setup.ts']
	}
});
