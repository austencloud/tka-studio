// src/lib/composables/useResponsiveLayout.ts
import { readable, derived, type Readable } from 'svelte/store';
import { browser } from '$app/environment';

export interface Dimensions {
	width: number;
	height: number;
}

export type LayoutMode = 'horizontal' | 'vertical';

/**
 * A composable hook for responsive layouts
 * Returns reactive stores for dimensions, orientation and layout mode
 */
export function useResponsiveLayout() {
	// Create a readable store that tracks window dimensions
	const dimensions: Readable<Dimensions> = readable({ width: 0, height: 0 }, (set) => {
		if (!browser) return;

		// Initial value
		set({
			width: window.innerWidth,
			height: window.innerHeight
		});

		// Update on resize
		const handleResize = () => {
			set({
				width: window.innerWidth,
				height: window.innerHeight
			});
		};

		window.addEventListener('resize', handleResize);

		// Cleanup
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});

	// Derived values
	const isPortrait = derived(dimensions, ($d) => $d.height > $d.width);
	const layout = derived(isPortrait, ($p) => ($p ? 'horizontal' : ('vertical' as LayoutMode)));

	return {
		dimensions,
		isPortrait,
		layout
	};
}
