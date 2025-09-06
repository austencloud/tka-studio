<!-- src/lib/components/objects/Glyphs/TKAGlyph/components/TurnsRenderer.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { assetCache, fetchSVGDimensions, type Rect } from '$lib/stores/glyphStore';
	import type { TKATurns } from '$lib/types/Types';

	// Props
	export let topValue: TKATurns = 0;
	export let bottomValue: TKATurns = 0;
	export let letterRect: Rect;

	// Constants
	const PADDING_X = 15;
	const PADDING_Y = 5;

	// Calculated positioning
	$: turnsPositions = calculateTurnsPositions(letterRect, PADDING_X, PADDING_Y);

	// Pure functions for calculations
	function calculateTurnsPositions(rect: Rect, paddingX: number, paddingY: number) {
		if (!rect || rect.width === 0) {
			return { top: { x: 0, y: 0 }, bottom: { x: 0, y: 0 } };
		}

		const baseX = rect.right + paddingX;

		return {
			top: {
				x: baseX,
				y: rect.top - paddingY
			},
			bottom: {
				x: baseX,
				y: rect.bottom + paddingY
			}
		};
	}

	// Get path for number SVGs
	function getNumberPath(value: TKATurns): string {
		if (value === 'fl') return '/images/numbers/float.svg';
		if (typeof value === 'number' && value > 0) {
			return `/images/numbers/${value}.svg`;
		}
		return '';
	}

	// Async load for number dimensions
	async function ensureNumberLoaded(value: TKATurns) {
		if (!value) return;

		const path = getNumberPath(value);
		if (!path) return;

		// Check cache
		const cacheKey = typeof value === 'number' ? value.toString() : value;
		if ($assetCache.numberSVGs.has(cacheKey)) return;

		try {
			const dimensions = await fetchSVGDimensions(path);

			// Update cache
			assetCache.update((cache) => {
				cache.numberSVGs.set(cacheKey, {
					svg: path,
					dimensions
				});
				return cache;
			});
		} catch (error) {
			console.error(`Failed to load number SVG for ${value}:`, error);
		}
	}

	// Ensure numbers are loaded
	$: {
		if (topValue !== 0) ensureNumberLoaded(topValue);
		if (bottomValue !== 0) ensureNumberLoaded(bottomValue);
	}

	// Helpers for rendering
	function getNumberSVGDetails(value: TKATurns) {
		if (!value) return null;

		const cacheKey = typeof value === 'number' ? value.toString() : value;
		const cached = $assetCache.numberSVGs.get(cacheKey);

		if (!cached) return null;

		return {
			path: cached.svg,
			width: cached.dimensions.width,
			height: cached.dimensions.height
		};
	}
</script>

<g class="turns-number-group">
	{#if topValue !== 0}
		{@const topDetails = getNumberSVGDetails(topValue)}
		{#if topDetails}
			<g transform={`translate(${turnsPositions.top.x}, ${turnsPositions.top.y})`}>
				<image href={topDetails.path} width={topDetails.width} height={topDetails.height} />
			</g>
		{/if}
	{/if}

	{#if bottomValue !== 0}
		{@const bottomDetails = getNumberSVGDetails(bottomValue)}
		{#if bottomDetails}
			<g transform={`translate(${turnsPositions.bottom.x}, ${turnsPositions.bottom.y})`}>
				<image
					href={bottomDetails.path}
					width={bottomDetails.width}
					height={bottomDetails.height}
				/>
			</g>
		{/if}
	{/if}
</g>
