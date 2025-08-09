/// <reference types="svelte" />
/// <reference types="vite/client" />
/// <reference types="@testing-library/jest-dom" />

// Global type declarations for the application

declare global {
	// Environment variables
	interface ImportMetaEnv {
		readonly VITE_APP_TITLE: string;
		readonly VITE_API_URL: string;
		readonly VITE_ENVIRONMENT: 'development' | 'staging' | 'production';
		readonly DEV: boolean;
		readonly PROD: boolean;
		readonly SSR: boolean;
	}

	interface ImportMeta {
		readonly env: ImportMetaEnv;
	}

	// Window extensions
	interface Window {
		// Add any global window properties here
		__SVELTE_KIT_DEV__?: boolean;
	}

	// Custom events
	interface CustomEventMap {
		'theme-change': CustomEvent<{ theme: 'light' | 'dark' }>;
		'settings-update': CustomEvent<{ settings: Record<string, unknown> }>;
	}

	// Extend the global EventTarget interface
	interface EventTarget {
		addEventListener<K extends keyof CustomEventMap>(
			type: K,
			listener: (this: EventTarget, ev: CustomEventMap[K]) => void,
			options?: boolean | AddEventListenerOptions
		): void;
		removeEventListener<K extends keyof CustomEventMap>(
			type: K,
			listener: (this: EventTarget, ev: CustomEventMap[K]) => void,
			options?: boolean | EventListenerOptions
		): void;
	}
}

// Module declarations for assets
declare module '*.svg' {
	const content: string;
	export default content;
}

declare module '*.png' {
	const content: string;
	export default content;
}

declare module '*.jpg' {
	const content: string;
	export default content;
}

declare module '*.jpeg' {
	const content: string;
	export default content;
}

declare module '*.gif' {
	const content: string;
	export default content;
}

declare module '*.webp' {
	const content: string;
	export default content;
}

declare module '*.ico' {
	const content: string;
	export default content;
}

// CSS modules
declare module '*.module.css' {
	const classes: { readonly [key: string]: string };
	export default classes;
}

declare module '*.module.scss' {
	const classes: { readonly [key: string]: string };
	export default classes;
}

// JSON modules
declare module '*.json' {
	const value: unknown;
	export default value;
}

// Svelte component types
declare module '*.svelte' {
	import type { ComponentType, SvelteComponent } from 'svelte';
	const component: ComponentType<SvelteComponent>;
	export default component;
}

export {};
