<!--
🎨 PICTOGRAPH SVG COMPONENT

Renders the actual SVG content for pictographs using proper TKA components.
Based on the v1-legacy implementation patterns with Grid, Arrow, Prop, and TKAGlyph components.
-->
<script lang="ts">
	import type { PictographData } from '@tka/domain';
	import Grid from './Grid.svelte';
	import Arrow from './Arrow.svelte';
	import Prop from './Prop.svelte';
	import TKAGlyph from './TKAGlyph.svelte';

	// Props using runes
	const props = $props<{
		pictographData: PictographData | null;
		debug?: boolean;
		onError?: (component: string, message: string) => void;
		onComponentLoaded?: (component: string) => void;
		onGridLoaded?: (data: any) => void;
	}>();

	// State using runes
	let gridLoaded = $state(false);
	let gridData = $state<any>(null);

	// Helper function for accessibility
	function getPictographAriaLabel(data: PictographData | null): string {
		if (!data) return 'Empty pictograph';
		return `Pictograph showing letter ${data.letter || 'unknown'}`;
	}

	// Handle grid loaded event
	function handleGridLoaded(data: any) {
		gridData = data;
		gridLoaded = true;
		props.onGridLoaded?.(data);
	}

	// Handle component errors
	function handleComponentError(componentName: string, message: string) {
		console.error(`${componentName} error:`, message);
		props.onError?.(componentName, message);
	}

	// Get coordinates for a location from grid data
	function getLocationCoordinates(location: string, gridData: any): { x: number, y: number } | null {
		if (!gridData || !location) return null;

		// Try to find the location in hand points first
		const handPoint = gridData.allHandPointsNormal?.[`${location}_diamond_hand_point`];
		if (handPoint?.coordinates) {
			return handPoint.coordinates;
		}

		// Fallback to center
		return gridData.centerPoint?.coordinates || { x: 475, y: 475 };
	}

	// Process pictograph data for components
	const redArrowData = $derived.by(() => {
		if (!props.pictographData?.redMotionData || !gridData) return null;

		return {
			color: 'red' as const,
			motionType: props.pictographData.redMotionData.motionType,
			startLoc: props.pictographData.redMotionData.startLoc,
			endLoc: props.pictographData.redMotionData.endLoc,
			startOri: props.pictographData.redMotionData.startOri,
			endOri: props.pictographData.redMotionData.endOri,
			turns: props.pictographData.redMotionData.turns || 0,
			coords: getLocationCoordinates(props.pictographData.redMotionData.startLoc, gridData)
		};
	});

	const blueArrowData = $derived.by(() => {
		if (!props.pictographData?.blueMotionData || !gridData) return null;

		return {
			color: 'blue' as const,
			motionType: props.pictographData.blueMotionData.motionType,
			startLoc: props.pictographData.blueMotionData.startLoc,
			endLoc: props.pictographData.blueMotionData.endLoc,
			startOri: props.pictographData.blueMotionData.startOri,
			endOri: props.pictographData.blueMotionData.endOri,
			turns: props.pictographData.blueMotionData.turns || 0,
			coords: getLocationCoordinates(props.pictographData.blueMotionData.startLoc, gridData)
		};
	});

	const redPropData = $derived.by(() => {
		if (!props.pictographData?.redMotionData || !gridData) return null;

		return {
			color: 'red' as const,
			propType: 'staff',
			loc: props.pictographData.redMotionData.startLoc,
			ori: props.pictographData.redMotionData.startOri,
			coords: getLocationCoordinates(props.pictographData.redMotionData.startLoc, gridData)
		};
	});

	const bluePropData = $derived.by(() => {
		if (!props.pictographData?.blueMotionData || !gridData) return null;

		return {
			color: 'blue' as const,
			propType: 'staff',
			loc: props.pictographData.blueMotionData.startLoc,
			ori: props.pictographData.blueMotionData.startOri,
			coords: getLocationCoordinates(props.pictographData.blueMotionData.startLoc, gridData)
		};
	});
</script>

<svg
	class="pictograph"
	class:debug={props.debug}
	viewBox="0 0 950 950"
	xmlns="http://www.w3.org/2000/svg"
	role="img"
	aria-label={getPictographAriaLabel(props.pictographData)}
>
	<!-- Grid Component -->
	<Grid
		gridMode={props.pictographData?.gridMode || 'diamond'}
		onPointsReady={handleGridLoaded}
		onError={(message) => handleComponentError('grid', message)}
		debug={props.debug}
	/>

	<!-- Only render other components after grid is loaded -->
	{#if gridLoaded && props.pictographData}
		<!-- Props -->
		{#if redPropData && redPropData.coords}
			<Prop
				propData={redPropData}
				onLoaded={() => props.onComponentLoaded?.('redProp')}
				onError={(message) => handleComponentError('redProp', message)}
			/>
		{/if}

		{#if bluePropData && bluePropData.coords}
			<Prop
				propData={bluePropData}
				onLoaded={() => props.onComponentLoaded?.('blueProp')}
				onError={(message) => handleComponentError('blueProp', message)}
			/>
		{/if}

		<!-- Arrows -->
		{#if redArrowData && redArrowData.coords}
			<Arrow
				arrowData={redArrowData}
				onLoaded={() => props.onComponentLoaded?.('redArrow')}
				onError={(message) => handleComponentError('redArrow', message)}
			/>
		{/if}

		{#if blueArrowData && blueArrowData.coords}
			<Arrow
				arrowData={blueArrowData}
				onLoaded={() => props.onComponentLoaded?.('blueArrow')}
				onError={(message) => handleComponentError('blueArrow', message)}
			/>
		{/if}

		<!-- TKA Glyph - positioned in bottom-left area like legacy -->
		{#if props.pictographData.letter}
			<TKAGlyph
				letter={props.pictographData.letter}
				turnsTuple="(s, 0, 0)"
				x={50}
				y={800}
				scale={1.5}
			/>
		{/if}
	{/if}
</svg>

<style>
	.pictograph {
		width: 100%;
		height: 100%;
		max-width: 100%;
		max-height: 100%;
		display: block;
		background-color: white;
		transition: transform 0.1s ease-in-out;
		transform: scale(1);
		z-index: 1;
		position: relative;
		border: 1px solid #ccc;
		aspect-ratio: 1;
		margin: auto;
		overflow: visible;
		transform-origin: center center;
		box-sizing: border-box;
		border-radius: 8px;
	}

	.pictograph.debug {
		border-color: #ff6b6b;
		border-width: 2px;
	}
</style>
