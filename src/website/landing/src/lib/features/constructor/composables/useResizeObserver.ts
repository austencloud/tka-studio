// src/lib/composables/useResizeObserver.ts
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export interface ElementSize {
	width: number;
	height: number;
	x: number;
	y: number;
}

/**
 * A hook that observes an element's size changes
 * @param defaultSize Optional default dimensions to use before measuring
 * @returns An object with a store and an action
 */
export function useResizeObserver(defaultSize: Partial<ElementSize> = {}) {
	const initialSize: ElementSize = {
		width: defaultSize.width || 0,
		height: defaultSize.height || 0,
		x: defaultSize.x || 0,
		y: defaultSize.y || 0
	};

	// Create a store for the element's dimensions
	const size: Writable<ElementSize> = writable(initialSize);

	// Create a Svelte action for the resize observer
	function resizeObserver(node: HTMLElement) {
		// Initialize with current dimensions if available
		const rect = node.getBoundingClientRect();
		if (rect.width > 0 && rect.height > 0) {
			size.set({
				width: rect.width,
				height: rect.height,
				x: rect.x,
				y: rect.y
			});
		}

		// Create observer
		const observer = new ResizeObserver((entries) => {
			for (const entry of entries) {
				if (entry.contentRect) {
					size.set({
						width: entry.contentRect.width,
						height: entry.contentRect.height,
						x: entry.contentRect.x,
						y: entry.contentRect.y
					});
				}
			}
		});

		// Start observing
		observer.observe(node);

		// Cleanup on component unmount
		return {
			destroy() {
				observer.disconnect();
			}
		};
	}

	return {
		size,
		resizeObserver
	};
}
