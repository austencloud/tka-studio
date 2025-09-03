<script lang="ts">
	import { assetCache, type Rect } from '$lib/stores/glyphStore';
	import type { Letter } from '$lib/types/Letter';

	// Props
	let { letter = null, letterRect } = $props<{
		letter: Letter | null;
		letterRect: Rect;
	}>();

	// Reactive constant for positioning
	const PADDING = 5;

	// Derived values using Svelte 5 Runes
	const isDashVisible = $derived(letter?.toString().includes('-') ?? false);
	const dashDimensions = $derived($assetCache.dashSVG?.dimensions ?? { width: 0, height: 0 });
	const dashAvailable = $derived($assetCache.dashSVG !== null);

	// Position calculation with pure function pattern
	const dashPosition = $derived(calculateDashPosition(letterRect, dashDimensions, PADDING));

	// Pure function for calculating position
	function calculateDashPosition(
		rect: Rect,
		dimensions: { width: number; height: number },
		padding: number
	) {
		if (!rect || dimensions.width === 0) {
			return { x: 0, y: 0 };
		}

		const centerY = rect.top + rect.height / 2;
		return {
			x: rect.right + padding,
			y: centerY - dimensions.height / 2
		};
	}
</script>

<g class="tka-dash" opacity={isDashVisible ? 1 : 0}>
	{#if dashAvailable && isDashVisible}
		<image
			href={$assetCache.dashSVG?.svg}
			width={dashDimensions.width}
			height={dashDimensions.height}
			x={dashPosition.x}
			y={dashPosition.y}
		/>
	{/if}
</g>
