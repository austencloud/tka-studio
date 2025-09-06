<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { get } from 'svelte/store';
	import { getBackgroundContext } from './contexts/BackgroundContext';
	import { useBackgroundContext } from './contexts/BackgroundContext.svelte';
	import { BackgroundFactory } from './core/BackgroundFactory';
	import type { BackgroundType, PerformanceMetrics, QualityLevel, BackgroundSystem } from './types/types';
	import { browser } from '$app/environment';

	// Define props with Svelte 5 runes
	const props = $props<{
		backgroundType?: BackgroundType;
		appIsLoading?: boolean;
		onReady?: () => void;
		onPerformanceReport?: (metrics: PerformanceMetrics) => void;
	}>();

	// Create mutable state variables from props with defaults
	let backgroundType = $state(props.backgroundType || 'nightSky');
	let appIsLoading = $state(props.appIsLoading !== undefined ? props.appIsLoading : true);

	// Update state when props change
	$effect(() => {
		if (props.backgroundType !== undefined && props.backgroundType !== backgroundType) {
			backgroundType = props.backgroundType;
		}
		if (props.appIsLoading !== undefined && props.appIsLoading !== appIsLoading) {
			appIsLoading = props.appIsLoading;
		}
	});

	// Get the context only once - don't recreate it on each render
	let activeContext = browser ? useBackgroundContext() : null;
	// Track the current background system
	let currentBackgroundSystem: BackgroundSystem | null = null;

	// Flag to prevent changes during initialization
	let isInitialized = $state(false);

	// Use let for the canvas element
	let canvas: HTMLCanvasElement | undefined;

	onMount(() => {
		if (!browser) {
			return;
		}

		if (!canvas) {
			console.error('Canvas element not found!');
			return;
		}

		// Add event listener for background changes
		window.addEventListener('changeBackground', handleBackgroundChange as EventListener);

		if (activeContext) {
			// Set initial values from props to context once on mount
			if (backgroundType && backgroundType !== activeContext.backgroundType) {
				activeContext.setBackgroundType(backgroundType);
			}

			if (appIsLoading !== undefined && appIsLoading !== activeContext.isLoading) {
				activeContext.setLoading(appIsLoading);

				const quality: QualityLevel = appIsLoading ? 'medium' : 'high';
				if (quality !== activeContext.qualityLevel) {
					activeContext.setQuality(quality);
				}
			}

			// Get the background system if it exists
			if ('backgroundSystem' in activeContext) {
				currentBackgroundSystem = (activeContext as any).backgroundSystem;
			}

			// Use the active context for initialization and animation
			activeContext.initializeCanvas(canvas, () => {
				// Get updated background system after initialization
				if ('backgroundSystem' in activeContext) {
					currentBackgroundSystem = (activeContext as any).backgroundSystem;
				}

				// Call the onReady callback if provided
				if (props.onReady) {
					props.onReady();
				}
				isInitialized = true;
			});

			activeContext.startAnimation(
				(ctx, dimensions) => {
					// Always get latest background system for animation frame
					if ('backgroundSystem' in activeContext) {
						currentBackgroundSystem = (activeContext as any).backgroundSystem;
					}

					if (currentBackgroundSystem) {
						currentBackgroundSystem.update(dimensions);
						currentBackgroundSystem.draw(ctx, dimensions);
					} else {
						console.warn('No background system available for animation frame');
					}
				},
				(metrics) => {
					// Call the onPerformanceReport callback if provided
					if (props.onPerformanceReport) {
						props.onPerformanceReport(metrics);
					}
				}
			);
		} else if (browser) {
			// Fallback to direct instantiation for backward compatibility
			const manager = createBackgroundManagerFallback();

			manager.initializeCanvas(canvas, () => {
				// Call the onReady callback if provided
				if (props.onReady) {
					props.onReady();
				}
				isInitialized = true;
			});

			manager.startAnimation(
				(ctx, dimensions) => {
					// For the legacy manager, create a background system if needed
					if (!currentBackgroundSystem) {
						currentBackgroundSystem = BackgroundFactory.createBackgroundSystem({
							type: backgroundType,
							initialQuality: 'medium'
						});
						currentBackgroundSystem.initialize(dimensions, 'medium');
					}

					if (currentBackgroundSystem) {
						currentBackgroundSystem.update(dimensions);
						currentBackgroundSystem.draw(ctx, dimensions);
					}
				},
				(metrics) => {
					// Call the onPerformanceReport callback if provided
					if (props.onPerformanceReport) {
						props.onPerformanceReport(metrics);
					}
				}
			);
		}
	});

	// Listen for background change events - only in browser
	function handleBackgroundChange(event: CustomEvent) {
		if (!browser || !isInitialized) return;

		if (event.detail && typeof event.detail === 'string') {
			const newBackgroundType = event.detail as BackgroundType;

			// Only update if the background type has changed
			if (backgroundType !== newBackgroundType) {
				backgroundType = newBackgroundType;

				// Update context directly
				if (activeContext) {
					activeContext.setBackgroundType(newBackgroundType);
				}
			}
		}
	}

	onDestroy(() => {
		if (!browser) return;

		// Remove event listener
		window.removeEventListener('changeBackground', handleBackgroundChange as EventListener);

		// Use active context cleanup if available
		if (activeContext) {
			activeContext.stopAnimation();
		}

		// Clean up background system if needed
		if (currentBackgroundSystem) {
			currentBackgroundSystem.cleanup();
			currentBackgroundSystem = null;
		}
	});

	// Maintain the same public API - only in browser
	export function setQuality(quality: QualityLevel) {
		if (!browser || !isInitialized) return;

		if (activeContext) {
			activeContext.setQuality(quality);
		} else if (currentBackgroundSystem) {
			currentBackgroundSystem.setQuality(quality);
		}
	}

	// Import the old manager for backward compatibility
	// This is only used if the component is used outside of a BackgroundProvider
	import { createBackgroundManager } from './core/BackgroundManager';
	function createBackgroundManagerFallback() {
		console.warn(
			'BackgroundCanvas is being used without a BackgroundProvider. Consider updating your code to use the new context-based API.'
		);
		return createBackgroundManager();
	}
</script>

<div class="background-canvas-container">
	<canvas
		bind:this={canvas}
		class="background-canvas"
		style="
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			width: 100%;
			height: 100%;
			z-index: -1;
		"
	></canvas>
</div>

<style>
	.background-canvas-container {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
		overflow: hidden;
	}

	.background-canvas {
		display: block;
	}
</style>
