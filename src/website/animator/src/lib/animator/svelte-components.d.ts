/**
 * TypeScript declarations for Svelte components
 * Compatible with verbatimModuleSyntax
 */
declare module '*.svelte' {
	import type { ComponentType, SvelteComponent } from 'svelte';

	// Export the component constructor as the default export
	const component: ComponentType<SvelteComponent<any, any, any>>;
	export default component;
}
