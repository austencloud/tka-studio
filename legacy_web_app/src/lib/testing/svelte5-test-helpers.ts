/**
 * Helper functions for testing Svelte 5 components
 */
import { vi } from 'vitest';
import type { ComponentProps } from 'svelte';

// Mock the onMount function to immediately call the callback
vi.mock('svelte', () => {
	return {
		onMount: (fn: () => any) => {
			fn(); // Execute the function immediately
			return () => {}; // Return a cleanup function
		}
	};
});

/**
 * Creates a mock component instance with the necessary properties for testing
 * @param props The component props
 * @returns A mock component instance
 */
export function createMockComponentInstance<T extends Record<string, any>>(props: T = {} as T) {
	const listeners: Record<string, Array<(event: CustomEvent<any>) => void>> = {};

	return {
		// Props
		...props,

		// Event handling
		$on: vi.fn((event: string, handler: (event: CustomEvent<any>) => void) => {
			if (!listeners[event]) {
				listeners[event] = [];
			}
			listeners[event].push(handler);
			return { destroy: vi.fn() };
		}),

		$dispatch: vi.fn((event: string, detail?: any) => {
			const handlers = listeners[event] || [];
			handlers.forEach((handler) => {
				handler(new CustomEvent(event, { detail }));
			});
			return true;
		}),

		// State management
		$set: vi.fn((newProps: Partial<T>) => {
			Object.assign(props, newProps);
		}),

		// Context
		$$: {
			ctx: Object.entries(props).map(([_, value]) => value)
		}
	};
}

/**
 * Mock render function for Svelte 5 components
 * @param Component The component to render
 * @param props The component props
 * @returns An object with the container and component instance
 */
export function mockRender<T extends Record<string, any>>(
	Component: any,
	props: Record<string, any> = {}
) {
	// Create a container element
	const container = document.createElement('div');

	// Create a mock component instance
	const component = createMockComponentInstance(props);

	// Call the component's onMount handler if it exists
	if (Component.prototype && typeof Component.prototype.onMount === 'function') {
		Component.prototype.onMount();
	}

	// Return both the container and the component instance
	return { container, component };
}
