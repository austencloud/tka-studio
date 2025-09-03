<!-- src/lib/components/objects/Glyphs/TKAGlyph/TKAGlyph.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { parseTurnsTupleString } from './utils/parseTurnsTuple';
	import { preloadCommonAssets, assetCache, type Rect } from '$lib/stores/glyphStore';
	import type { Letter } from '$lib/types/Letter';
	import type { DirRelation, PropRotDir, TKATurns } from '$lib/types/Types';
	import LetterRenderer from './components/LetterRenderer.svelte';
	import DashRenderer from './components/DashRenderer.svelte';
	import DotsRenderer from './components/DotsRenderer.svelte';
	import TurnsRenderer from './components/TurnsRenderer.svelte';

	// Props with TypeScript interface
	export let letter: Letter | null = null;
	export let turnsTuple: string = '';
	export let x: number = 0;
	export let y: number = 0;
	export let scale: number = 1;

	// Local state
	let letterRect: Rect | null = null;
	let letterLoaded = false;

	// Parse the turnsTuple
	$: parsedTurns = parseTurnsTuple(turnsTuple);

	// Destructure for easier access
	$: direction = parsedTurns?.direction || null;
	$: topTurn = parsedTurns?.top || (0 as TKATurns);
	$: bottomTurn = parsedTurns?.bottom || (0 as TKATurns);
	$: hasTurns =
		(topTurn !== 'fl' && Number(topTurn) > 0) || (bottomTurn !== 'fl' && Number(bottomTurn) > 0);
	$: shouldShowDots = hasTurns;

	// Ensure common assets are loaded
	onMount(() => {
		if (!$assetCache.dotSVG || !$assetCache.dashSVG) {
			preloadCommonAssets();
		}
	});

	// Helper functions
	function parseTurnsTuple(tuple: string) {
		if (!tuple) return { direction: null, top: 0 as TKATurns, bottom: 0 as TKATurns };

		const [dir, top, bottom] = parseTurnsTupleString(tuple);
		return { direction: dir, top, bottom };
	}

	// Handle letter loaded event
	function handleLetterLoaded(event: CustomEvent<Rect>) {
		letterRect = event.detail;
		letterLoaded = true;
	}
</script>

<g class="tka-glyph" transform={`translate(${x}, ${y}) scale(${scale})`}>
	<LetterRenderer {letter} on:letterLoaded={handleLetterLoaded} />

	{#if letterLoaded && letterRect}
		<DashRenderer {letter} {letterRect} />

		<DotsRenderer {direction} {letterRect} {letter} {shouldShowDots} />

		<TurnsRenderer topValue={topTurn} bottomValue={bottomTurn} {letterRect} />
	{/if}
</g>
