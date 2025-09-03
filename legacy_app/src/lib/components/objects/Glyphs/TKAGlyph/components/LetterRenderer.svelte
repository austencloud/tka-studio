<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { getLetterPath, assetCache, fetchSVGDimensions, type Rect } from '$lib/stores/glyphStore';
	import type { Letter } from '$lib/types/Letter';

	// Props
	let { letter = null } = $props<{
		letter: Letter | null;
	}>();

	// Event dispatcher
	const dispatch = createEventDispatcher<{
		letterLoaded: Rect;
	}>();

	// Local state using Svelte 5 Runes
	let svgPath = $state('');
	let dimensions = $state({ width: 0, height: 0 });
	let imageElement = $state<SVGImageElement | null>(null);
	let isLoaded = $state(false);
	let isFetchFailed = $state(false);
	let hasDispatchedLetterLoaded = $state(false);

	// Load SVG with proper caching strategy
	// This function is async, so it's called within an $effect
	async function loadLetterSVG(currentLetter: Letter) {
		if (!currentLetter) return;

		const path = getLetterPath(currentLetter);
		svgPath = path; // Update state

		// Check cache first
		const cacheKey = currentLetter.toString();
		let cachedSVG = $assetCache.letterSVGs.get(cacheKey);

		if (cachedSVG) {
			dimensions = cachedSVG.dimensions; // Update state
			isLoaded = true; // Update state
			return;
		}

		try {
			// Fetch dimensions if not in cache
			const fetchedDimensions = await fetchSVGDimensions(path);
			dimensions = fetchedDimensions; // Update state

			// Update cache
			assetCache.update((cache: any) => {
				cache.letterSVGs.set(cacheKey, {
					svg: path, // svgPath is already set
					dimensions: fetchedDimensions
				});
				return cache;
			});

			isLoaded = true; // Update state
		} catch (error) {
			console.error(`Failed to load letter SVG for ${currentLetter}:`, error);
			isFetchFailed = true; // Update state
		}
	}

	// Effect to react to letter changes
	$effect(() => {
		if (letter) {
			isLoaded = false; // Reset loading state
			isFetchFailed = false; // Reset error state
			hasDispatchedLetterLoaded = false; // Reset dispatch state
			loadLetterSVG(letter);
		} else {
			// Reset if letter becomes null
			svgPath = '';
			dimensions = { width: 0, height: 0 };
			isLoaded = false;
			isFetchFailed = false;
		}
	});

	// Handle image loaded with proper layout calculation
	function handleImageLoad() {
		// Prevent multiple dispatches for the same image load
		if (hasDispatchedLetterLoaded || !imageElement) return;

		try {
			const bbox = imageElement.getBBox();
			const rect: Rect = {
				left: bbox.x,
				top: bbox.y,
				width: bbox.width,
				height: bbox.height,
				right: bbox.x + bbox.width,
				bottom: bbox.y + bbox.height
			};

			// Set flag to prevent multiple dispatches
			hasDispatchedLetterLoaded = true; // Update state

			// Dispatch the event
			dispatch('letterLoaded', rect);
		} catch (error) {
			console.error('Error calculating letter bounding box:', error);
		}
	}
</script>

<g class="tka-letter">
	{#if svgPath && isLoaded && dimensions.width > 0}
		<image
			bind:this={imageElement}
			href={svgPath}
			width={dimensions.width}
			height={dimensions.height}
			preserveAspectRatio="xMinYMin meet"
			onload={handleImageLoad}
		/>
	{:else if isFetchFailed}
		<rect width="50" height="50" fill="rgba(255,0,0,0.2)" stroke="red" stroke-width="1" />
		<text x="10" y="30" fill="red" font-size="12">Error</text>
	{:else}
		<rect width="50" height="50" fill="rgba(200,200,200,0.3)" />
	{/if}
</g>
