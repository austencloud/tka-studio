<!-- src/lib/components/Backgrounds/simple/SimpleBackgroundAdapter.svelte -->
<!-- Drop-in replacement for BackgroundCanvas.svelte that uses lightweight alternatives -->
<!-- Maintains the same API while eliminating Three.js and reactive loop issues -->

<script lang="ts">
	import { onMount } from 'svelte';
	import SimpleBackgroundCanvas from './SimpleBackgroundCanvas.svelte';
	import CSSBackgroundCanvas from './CSSBackgroundCanvas.svelte';
	import type { BackgroundType, QualityLevel } from './SimpleBackgroundSystem.svelte.ts';

	// Props - same interface as original BackgroundCanvas
	const props = $props<{
		backgroundType?: 'snowfall' | 'nightSky' | 'deepOcean' | 'static';
		quality?: 'high' | 'medium' | 'low';
		appIsLoading?: boolean;
		useCSSOnly?: boolean; // New prop to force CSS-only mode
	}>();

	// Determine which background system to use
	let useCanvasBackground = $state(true);
	let useCSSBackground = $state(false);

	onMount(() => {
		console.log('🎨 SimpleBackgroundAdapter: Initializing lightweight background system');

		// Check for performance preferences
		const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		const isLowEndDevice = navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2;

		// Decide which background system to use
		if (props.useCSSOnly || prefersReducedMotion || isLowEndDevice || props.quality === 'low') {
			console.log('🎨 Using CSS-only background for optimal performance');
			useCanvasBackground = false;
			useCSSBackground = true;
		} else {
			console.log('🎨 Using Canvas 2D background for enhanced visuals');
			useCanvasBackground = true;
			useCSSBackground = false;
		}
	});

	// Map background types to ensure compatibility - fix Svelte 5 reactivity
	let mappedBackgroundType: BackgroundType = $state('deepOcean');
	let mappedQuality: QualityLevel = $state('medium');

	// Update mapped values when props change
	$effect(() => {
		const bgType = props.backgroundType;
		switch (bgType) {
			case 'snowfall':
				mappedBackgroundType = 'snowfall';
				break;
			case 'nightSky':
				mappedBackgroundType = 'nightSky';
				break;
			case 'deepOcean':
				mappedBackgroundType = 'deepOcean';
				break;
			case 'static':
			default:
				mappedBackgroundType = 'static';
				break;
		}
	});

	$effect(() => {
		const quality = props.quality;
		switch (quality) {
			case 'high':
				mappedQuality = 'high';
				break;
			case 'medium':
				mappedQuality = 'medium';
				break;
			case 'low':
			default:
				mappedQuality = 'low';
				break;
		}
	});
</script>

<!-- Render the appropriate background system -->
{#if useCanvasBackground}
	<SimpleBackgroundCanvas
		backgroundType={mappedBackgroundType}
		quality={mappedQuality}
		appIsLoading={props.appIsLoading}
	/>
{:else if useCSSBackground}
	<CSSBackgroundCanvas
		backgroundType={mappedBackgroundType}
		quality={mappedQuality}
		appIsLoading={props.appIsLoading}
	/>
{/if}

<!-- Fallback static background if both systems fail -->
<div class="fallback-background" style="display: {!useCanvasBackground && !useCSSBackground ? 'block' : 'none'}">
</div>

<style>
	.fallback-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
		background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
		pointer-events: none;
	}
</style>
