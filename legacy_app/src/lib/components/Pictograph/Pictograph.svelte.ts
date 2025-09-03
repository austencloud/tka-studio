/**
 * Pictograph Component with Svelte 5 Runes Integration
 *
 * This file provides the Svelte 5 runes integration for the Pictograph component.
 * It's used by the Pictograph.svelte component to access the modern container.
 */

import { pictographContainer } from '$lib/state/stores/pictograph/pictographContainer';
import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
import type { PictographData } from '$lib/types/PictographData';

/**
 * Hook to use the pictograph container with Svelte 5 runes
 */
export function usePictographContainer() {
	return useContainer(pictographContainer);
}

/**
 * Hook to use a local pictograph data with the container
 */
export function useLocalPictographData(data: PictographData) {
	// Set the data in the container
	$effect(() => {
		pictographContainer.setData(data);
	});

	// Return the container state
	return useContainer(pictographContainer);
}
