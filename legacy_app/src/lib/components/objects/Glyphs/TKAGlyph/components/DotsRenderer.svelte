<!-- src/lib/components/objects/Glyphs/TKAGlyph/components/DotsRenderer.svelte -->
<script lang="ts">
	import { assetCache, type Rect } from '$lib/stores/glyphStore';
	import { LetterType } from '$lib/types/LetterType';
	import type { Letter } from '$lib/types/Letter';
	import type { DirRelation, PropRotDir } from '$lib/types/Types';

	// Props interface
	interface DotsRendererProps {
		direction: DirRelation | PropRotDir | null;
		letterRect: Rect;
		letter: Letter | null;
		shouldShowDots: boolean;
	}

	// Props
	export let direction: DotsRendererProps['direction'] = null;
	export let letterRect: DotsRendererProps['letterRect'];
	export let letter: DotsRendererProps['letter'] = null;
	export let shouldShowDots: DotsRendererProps['shouldShowDots'] = true;

	// Config
	const DOT_PADDING = 20;

	// Calculate positions using functional approach
	$: dotPositions = calculateDotPositions(letterRect, $assetCache.dotSVG?.dimensions);
	$: canShowDots = letter && LetterType.getLetterType(letter) !== LetterType.Type1;
	$: dotsAvailable = $assetCache.dotSVG !== null;
	$: dotsVisible = canShowDots && dotsAvailable && direction !== null && shouldShowDots;

	// Pure functions for calculations
	function calculateDotPositions(rect: Rect, dimensions?: { width: number; height: number }) {
		const dotDimensions = dimensions || { width: 20, height: 20 };

		if (!rect || rect.width === 0) {
			return { same: { x: 0, y: 0 }, opposite: { x: 0, y: 0 } };
		}

		const centerX = rect.left + rect.width / 2;

		return {
			same: {
				x: centerX,
				y: rect.top - DOT_PADDING - dotDimensions.height / 2
			},
			opposite: {
				x: centerX,
				y: rect.bottom + DOT_PADDING + dotDimensions.height / 2
			}
		};
	}
</script>

<g class="dot-renderer">
	{#if dotsVisible}
		<!-- Same Dot -->
		<g
			class="tka-dot"
			transform={`translate(${dotPositions.same.x}, ${dotPositions.same.y})`}
			opacity={direction === 's' ? 1 : 0}
		>
			<image
				href={$assetCache.dotSVG?.svg}
				width={$assetCache.dotSVG?.dimensions.width || 0}
				height={$assetCache.dotSVG?.dimensions.height || 0}
				x={-($assetCache.dotSVG?.dimensions.width || 0) / 2}
				y={-($assetCache.dotSVG?.dimensions.height || 0) / 2}
			/>
		</g>

		<!-- Opposite Dot -->
		<g
			class="tka-dot"
			transform={`translate(${dotPositions.opposite.x}, ${dotPositions.opposite.y})`}
			opacity={direction === 'o' ? 1 : 0}
		>
			<image
				href={$assetCache.dotSVG?.svg}
				width={$assetCache.dotSVG?.dimensions.width || 0}
				height={$assetCache.dotSVG?.dimensions.height || 0}
				x={-($assetCache.dotSVG?.dimensions.width || 0) / 2}
				y={-($assetCache.dotSVG?.dimensions.height || 0) / 2}
			/>
		</g>
	{/if}
</g>

<style>
	.tka-dot image {
		transform-box: fill-box;
		transform-origin: center;
	}
</style>
