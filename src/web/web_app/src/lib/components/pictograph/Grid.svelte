<!--
Grid.svelte - Modern Rune-Based Grid Component

Renders the diamond or box grid background using real SVG assets.
Uses pure runes instead of stores for reactivity.
-->
<script lang="ts">
	import { createGridData } from '$lib/data/gridCoordinates';

	interface Props {
		/** Grid mode - diamond or box */
		gridMode?: 'diamond' | 'box';
		/** Called when grid is successfully loaded */
		onLoaded?: () => void;
		/** Called when grid loading fails */
		onError?: (error: string) => void;
		/** Debug mode */
		debug?: boolean;
	}

	let { gridMode = 'diamond', onLoaded, onError, debug = false }: Props = $props();

	// State using runes
	let isLoaded = $state(false);
	let hasError = $state(false);
	let errorMessage = $state<string | null>(null);
	// Image element for potential future use
	// @ts-expect-error: Used in bind:this but not referenced in code
	let _imageElement = $state<SVGImageElement | null>(null);

	// Derived state - grid image path
	const gridImagePath = $derived(() => {
		return `/images/grid/${gridMode}_grid.svg`;
	});

	// Derived state - grid data for positioning (in case parent components need it)
	const gridData = $derived(() => {
		return createGridData(gridMode);
	});

	// Initialize loading state when grid mode changes
	$effect(() => {
		isLoaded = false;
		hasError = false;
		errorMessage = null;

		if (debug) {
			console.log(`Grid: Loading ${gridMode} grid from ${gridImagePath()}`);
		}
	});

	// Event handlers
	function handleImageLoad() {
		isLoaded = true;
		hasError = false;
		errorMessage = null;

		if (debug) {
			console.log(`Grid: Successfully loaded ${gridMode} grid`);
		}

		onLoaded?.();
	}

	function handleImageError() {
		hasError = true;
		errorMessage = `Failed to load ${gridMode} grid image`;

		if (debug) {
			console.error(`Grid: ${errorMessage}`);
		}

		onError?.(errorMessage);

		// Still call onLoaded to prevent blocking the parent component
		onLoaded?.();
	}

	// Fallback grid rendering using coordinates
	const fallbackGridPath = $derived(() => {
		const data = gridData();

		if (gridMode === 'diamond') {
			// Create diamond shape from hand points
			const points = [
				data.allHandPointsNormal.n_diamond_hand_point?.coordinates,
				data.allHandPointsNormal.e_diamond_hand_point?.coordinates,
				data.allHandPointsNormal.s_diamond_hand_point?.coordinates,
				data.allHandPointsNormal.w_diamond_hand_point?.coordinates,
			].filter(Boolean);

			if (points.length === 4) {
				return `M ${points[0]!.x},${points[0]!.y} L ${points[1]!.x},${points[1]!.y} L ${points[2]!.x},${points[2]!.y} L ${points[3]!.x},${points[3]!.y} Z`;
			}
		} else {
			// Create box shape from hand points
			const points = [
				data.allHandPointsNormal.nw_box_hand_point?.coordinates,
				data.allHandPointsNormal.ne_box_hand_point?.coordinates,
				data.allHandPointsNormal.se_box_hand_point?.coordinates,
				data.allHandPointsNormal.sw_box_hand_point?.coordinates,
			].filter(Boolean);

			if (points.length === 4) {
				return `M ${points[0]!.x},${points[0]!.y} L ${points[1]!.x},${points[1]!.y} L ${points[2]!.x},${points[2]!.y} L ${points[3]!.x},${points[3]!.y} Z`;
			}
		}

		// Ultimate fallback - simple centered shape
		const center = { x: 475, y: 475 };
		const size = 143;

		if (gridMode === 'diamond') {
			return `M ${center.x},${center.y - size} L ${center.x + size},${center.y} L ${center.x},${center.y + size} L ${center.x - size},${center.y} Z`;
		} else {
			return `M ${center.x - size},${center.y - size} L ${center.x + size},${center.y - size} L ${center.x + size},${center.y + size} L ${center.x - size},${center.y + size} Z`;
		}
	});
</script>

<!-- Grid Group -->
<g class="grid" class:grid-loaded={isLoaded} class:grid-error={hasError} data-grid-mode={gridMode}>
	{#if !hasError}
		<!-- Primary grid image -->
		<image
			bind:this={_imageElement}
			href={gridImagePath()}
			x="0"
			y="0"
			width="950"
			height="950"
			preserveAspectRatio="none"
			onload={handleImageLoad}
			onerror={handleImageError}
		/>
	{:else}
		<!-- Fallback grid rendering -->
		<g class="fallback-grid">
			<path
				d={fallbackGridPath()}
				fill="none"
				stroke="#e5e7eb"
				stroke-width="2"
				stroke-dasharray="5,5"
			/>

			<!-- Center point -->
			<circle cx="475" cy="475" r="3" fill="#9ca3af" />

			{#if debug}
				<!-- Debug points -->
				{#each Object.entries(gridData().allHandPointsNormal) as [key, point]}
					{#if point.coordinates}
						<circle
							cx={point.coordinates.x}
							cy={point.coordinates.y}
							r="2"
							fill="#ef4444"
						/>
						<text
							x={point.coordinates.x + 5}
							y={point.coordinates.y - 5}
							font-size="8"
							fill="#ef4444"
							font-family="monospace"
						>
							{key.replace('_hand_point', '').replace(`_${gridMode}`, '')}
						</text>
					{/if}
				{/each}
			{/if}
		</g>
	{/if}

	{#if debug}
		<!-- Debug overlay showing grid state -->
		<g class="debug-overlay">
			<rect x="10" y="10" width="200" height="60" fill="rgba(0, 0, 0, 0.8)" rx="4" />
			<text x="20" y="30" font-size="12" fill="white" font-family="monospace">
				Grid: {gridMode}
			</text>
			<text x="20" y="45" font-size="10" fill="white" font-family="monospace">
				Loaded: {isLoaded ? 'YES' : 'NO'}
			</text>
			<text x="20" y="60" font-size="10" fill="white" font-family="monospace">
				Error: {hasError ? 'YES' : 'NO'}
			</text>
		</g>
	{/if}
</g>

<style>
	.grid {
		/* Grid is rendered first, so it's in the background */
		z-index: 1;
	}

	.grid-loaded {
		opacity: 1;
		transition: opacity 0.3s ease;
	}

	.grid-error .fallback-grid {
		opacity: 0.7;
	}

	.fallback-grid path {
		animation: dash 2s linear infinite;
	}

	@keyframes dash {
		to {
			stroke-dashoffset: -10;
		}
	}

	.debug-overlay {
		pointer-events: none;
	}
</style>
