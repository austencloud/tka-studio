<script lang="ts">
	import { browser } from '$app/environment';
	import { onDestroy, onMount } from 'svelte';
	import { getRunesBackgroundContext } from './contexts/BackgroundContext.svelte';
	import type { BackgroundType, Dimensions, QualityLevel } from './types/types';

	// Props using Svelte 5 runes
	const {
		dimensions: propDimensions,
		backgroundType: propBackgroundType,
		quality: propQuality,
		onready,
		onerror,
		onperformanceReport,
	} = $props<{
		dimensions?: Dimensions;
		backgroundType?: BackgroundType;
		quality?: QualityLevel;
		onready?: () => void;
		onerror?: (error: { message: string }) => void;
		onperformanceReport?: (report: { fps: number }) => void;
	}>();

	// Get background context
	let backgroundContext = browser ? getRunesBackgroundContext() : null;

	// Component state
	let currentBackgroundType = $state(propBackgroundType || 'snowfall');
	let currentQuality = $state(propQuality || 'medium');
	let currentDimensions = $state(propDimensions || { width: 0, height: 0 });

	// Update reactive state when props change
	$effect(() => {
		if (propBackgroundType !== undefined) {
			currentBackgroundType = propBackgroundType;
		}
		if (propQuality !== undefined) {
			currentQuality = propQuality;
		}
		if (propDimensions !== undefined) {
			currentDimensions = propDimensions;
		}
	});

	// Update context when state changes
	$effect(() => {
		if (!browser || !backgroundContext) return;

		if (backgroundContext.backgroundType !== currentBackgroundType) {
			backgroundContext.setBackgroundType(currentBackgroundType);
		}
	});

	$effect(() => {
		if (!browser || !backgroundContext) return;

		if (backgroundContext.qualityLevel !== currentQuality) {
			backgroundContext.setQuality(currentQuality);
		}
	});

	$effect(() => {
		if (!browser || !backgroundContext) return;

		if (currentDimensions.width > 0 && currentDimensions.height > 0) {
			// Update dimensions if they've changed significantly
			const currentDims = backgroundContext.dimensions;
			if (
				Math.abs(currentDims.width - currentDimensions.width) > 10 ||
				Math.abs(currentDims.height - currentDimensions.height) > 10
			) {
				// Trigger a resize-like update
				if (backgroundContext.backgroundSystem) {
					backgroundContext.backgroundSystem.handleResize?.(
						currentDims,
						currentDimensions
					);
				}
			}
		}
	});

	onMount(async () => {
		try {
			if (!browser || !backgroundContext) {
				if (browser) {
					console.error('Background context not available');
					onerror?.({ message: 'Background context not available' });
				}
				return;
			}

			// Set initial values
			if (currentBackgroundType !== backgroundContext.backgroundType) {
				backgroundContext.setBackgroundType(currentBackgroundType);
			}

			if (currentQuality !== backgroundContext.qualityLevel) {
				backgroundContext.setQuality(currentQuality);
			}

			// Start performance monitoring
			if (backgroundContext.performanceMetrics) {
				const interval = setInterval(() => {
					const metrics = backgroundContext.performanceMetrics;
					onperformanceReport?.({ fps: metrics.fps });
				}, 1000);

				// Clean up interval on destroy
				onDestroy(() => {
					clearInterval(interval);
				});
			}

			onready?.();
		} catch (error) {
			console.error('Failed to initialize background controller:', error);
			onerror?.({ message: 'Failed to initialize background controller' });
		}
	});

	onDestroy(() => {
		// Cleanup is handled by the background context
	});

	// Export functions for external control
	export function setBackgroundType(type: BackgroundType) {
		currentBackgroundType = type;
	}

	export function setQuality(quality: QualityLevel) {
		currentQuality = quality;
	}

	export function setVisibility(_visible: boolean) {
		// Visibility control can be implemented if needed
		// Currently not used but keeping for API compatibility
	}
</script>

<!-- This controller component doesn't render anything itself -->
<!-- It just manages the background state through the context -->
