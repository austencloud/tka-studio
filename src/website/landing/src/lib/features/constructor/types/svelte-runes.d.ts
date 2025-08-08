/**
 * Type declarations for Svelte 5 runes
 */

// Instead of using declare global, we'll use module augmentation
// which is more reliable for TypeScript in Svelte components
declare module 'svelte' {
	export function $state<T>(initial: T): T;
	export function $state<T>(): T | undefined;

	export namespace $state {
		export function raw<T>(initial: T): T;
		export function raw<T>(): T | undefined;
		export function snapshot<T>(value: T): T;
	}

	export function $derived<T>(expression: T): T;

	export function $effect(callback: () => void | (() => void)): void;
	export function $effect<T>(callback: (value: T) => void | (() => void), deps: T): void;

	export function $props<T extends Record<string, any>>(): T;

	export function $bindable<T>(initial: T): T;
	export function $bindable<T>(): T | undefined;

	export function $inspect<T>(value: T, label?: string): T;

	export function $host(): HTMLElement | null;
}

// Also declare them globally for direct usage in .svelte files
declare global {
	const $state: typeof import('svelte').$state;
	const $derived: typeof import('svelte').$derived;
	const $effect: typeof import('svelte').$effect;
	const $props: typeof import('svelte').$props;
	const $bindable: typeof import('svelte').$bindable;
	const $inspect: typeof import('svelte').$inspect;
	const $host: typeof import('svelte').$host;
}

export {};
