/**
 * Background Store Adapter
 *
 * This module provides an adapter between the modern background container
 * and the legacy store-based API. This allows for a gradual migration
 * to the new container-based approach.
 */

import { writable, derived, type Writable, type Readable } from 'svelte/store';
import { backgroundContainer, type BackgroundState } from './BackgroundContainer';
import type {
	BackgroundType,
	QualityLevel,
	PerformanceMetrics
} from '$lib/components/Backgrounds/types/types';

/**
 * Create a store adapter for the background container
 */
function createBackgroundStoreAdapter(): Writable<BackgroundState> & {
	setBackground: (background: BackgroundType) => void;
	setReady: (isReady: boolean) => void;
	setVisible: (isVisible: boolean) => void;
	setQuality: (quality: QualityLevel) => void;
	updatePerformanceMetrics: (metrics: PerformanceMetrics) => void;
	setError: (error: Error | null) => void;
	addAvailableBackground: (background: BackgroundType) => void;
	removeAvailableBackground: (background: BackgroundType) => void;
} {
	// Create a writable store that reflects the container's state
	const { subscribe, set } = writable<BackgroundState>(backgroundContainer.state);

	// Set up cleanup function
	let cleanup: () => void;

	// Check if the container has a subscribe method
	if (
		'subscribe' in backgroundContainer &&
		typeof (backgroundContainer as any).subscribe === 'function'
	) {
		// Use the subscribe method
		const unsubscribe = (backgroundContainer as any).subscribe((state: BackgroundState) => {
			set(state);
		});

		cleanup = () => {
			if (typeof unsubscribe === 'function') {
				unsubscribe();
			}
		};
	} else {
		// Fall back to polling with a short interval
		const intervalId = setInterval(() => {
			set(backgroundContainer.state);
		}, 16); // Poll at approximately 60fps for smoother updates

		cleanup = () => {
			clearInterval(intervalId);
		};
	}

	// Clean up when the window is unloaded
	if (typeof window !== 'undefined') {
		window.addEventListener('beforeunload', cleanup);
	}

	// Return a store with the same API as the original background store
	return {
		subscribe,
		set: (value: BackgroundState) => {
			// Update the container when the store is set
			backgroundContainer.setBackground(value.currentBackground);
			backgroundContainer.setReady(value.isReady);
			backgroundContainer.setVisible(value.isVisible);
			backgroundContainer.setQuality(value.quality);
			if (value.performanceMetrics) {
				backgroundContainer.updatePerformanceMetrics(value.performanceMetrics);
			}
			backgroundContainer.setError(value.error);
			set(value);
		},
		update: (updater: (value: BackgroundState) => BackgroundState) => {
			const newValue = updater(backgroundContainer.state);
			// Update the container with the new value
			backgroundContainer.setBackground(newValue.currentBackground);
			backgroundContainer.setReady(newValue.isReady);
			backgroundContainer.setVisible(newValue.isVisible);
			backgroundContainer.setQuality(newValue.quality);
			if (newValue.performanceMetrics) {
				backgroundContainer.updatePerformanceMetrics(newValue.performanceMetrics);
			}
			backgroundContainer.setError(newValue.error);
			set(newValue);
		},
		// Forward action methods to the container
		setBackground: backgroundContainer.setBackground,
		setReady: backgroundContainer.setReady,
		setVisible: backgroundContainer.setVisible,
		setQuality: backgroundContainer.setQuality,
		updatePerformanceMetrics: backgroundContainer.updatePerformanceMetrics,
		setError: backgroundContainer.setError,
		addAvailableBackground: backgroundContainer.addAvailableBackground,
		removeAvailableBackground: backgroundContainer.removeAvailableBackground
	};
}

// Create the adapter
export const backgroundStore = createBackgroundStoreAdapter();

// Create derived stores for backward compatibility
export const currentBackgroundStore: Readable<BackgroundType> = derived(
	backgroundStore,
	($store) => $store.currentBackground
);

export const isBackgroundReadyStore: Readable<boolean> = derived(
	backgroundStore,
	($store) => $store.isReady
);

export const isBackgroundVisibleStore: Readable<boolean> = derived(
	backgroundStore,
	($store) => $store.isVisible
);

export const backgroundQualityStore: Readable<QualityLevel> = derived(
	backgroundStore,
	($store) => $store.quality
);

export const availableBackgroundsStore: Readable<BackgroundType[]> = derived(
	backgroundStore,
	($store) => $store.availableBackgrounds
);

// Re-export the container for modern usage
export { backgroundContainer } from './BackgroundContainer';
export type { BackgroundState, BackgroundContainer } from './BackgroundContainer';
