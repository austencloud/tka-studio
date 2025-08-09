import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(),

		// Configure aliases for clean imports
		alias: {
			$domain: 'src/lib/domain',
			$services: 'src/lib/services',
			$stores: 'src/lib/stores',
			$components: 'src/lib/components',
			$utils: 'src/lib/utils',
			'@tka/schemas': '../../../schemas/generated-types.ts',
			'@tka/shared': '../shared',
		},
	},
};

export default config;
