<!-- src/lib/components/Backgrounds/simple/SimpleBackgroundCanvas.svelte -->
<!-- Lightweight Canvas 2D background component to replace Three.js implementation -->
<!-- Eliminates Svelte 5 reactive loop issues while maintaining visual appeal -->

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { EnhancedBackgroundSystem, type BackgroundType, type QualityLevel } from './EnhancedBackgroundSystem.svelte';

	// Props using Svelte 5 runes
	const props = $props<{
		backgroundType?: BackgroundType;
		quality?: QualityLevel;
		appIsLoading?: boolean;
	}>();

	// Local state
	let canvas: HTMLCanvasElement;
	let backgroundSystem: EnhancedBackgroundSystem | null = null;
	let resizeObserver: ResizeObserver | null = null;

	// Initialize background system - only in browser
	onMount(() => {
		if (!browser) return;

		console.log('✅ SimpleBackgroundCanvas: Initializing lightweight background system');

		if (!canvas) {
			console.error('SimpleBackgroundCanvas: Canvas element not found');
			return;
		}

		// Get initial dimensions
		const rect = canvas.getBoundingClientRect();
		const dimensions = {
			width: rect.width || window.innerWidth,
			height: rect.height || window.innerHeight
		};

		// Set canvas size
		canvas.width = dimensions.width;
		canvas.height = dimensions.height;

		// Initialize background system with non-reactive values
		const bgType = props.backgroundType || 'nightSky';
		const qualityLevel = props.quality || 'medium';

		backgroundSystem = new EnhancedBackgroundSystem(bgType, qualityLevel);
		backgroundSystem.initialize(canvas, dimensions);

		// Set up resize observer to handle dimension changes
		resizeObserver = new ResizeObserver((entries) => {
			for (const entry of entries) {
				const { width, height } = entry.contentRect;

				if (width > 0 && height > 0) {
					// Update canvas size
					canvas.width = width;
					canvas.height = height;

					// Update background system dimensions
					if (backgroundSystem) {
						backgroundSystem.updateDimensions({ width, height });
					}
				}
			}
		});

		// Observe the canvas element
		resizeObserver.observe(canvas);

		console.log('✅ SimpleBackgroundCanvas: Background system initialized successfully');
	});

	// Handle prop changes
	$effect(() => {
		if (backgroundSystem && props.backgroundType) {
			backgroundSystem.setBackgroundType(props.backgroundType);
		}
	});

	$effect(() => {
		if (backgroundSystem && props.quality) {
			backgroundSystem.setQuality(props.quality);
		}
	});

	// Cleanup
	onDestroy(() => {
		console.log('🧹 SimpleBackgroundCanvas: Cleaning up background system');

		if (backgroundSystem) {
			backgroundSystem.cleanup();
			backgroundSystem = null;
		}

		if (resizeObserver) {
			resizeObserver.disconnect();
			resizeObserver = null;
		}
	});
</script>

<canvas
	bind:this={canvas}
	class="simple-background-canvas"
	style="
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
		pointer-events: none;
	"
></canvas>

<style>
	.simple-background-canvas {
		/* Ensure canvas fills container and stays in background */
		display: block;
		background: transparent;
	}
</style>
