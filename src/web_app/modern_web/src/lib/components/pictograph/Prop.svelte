<!--
Prop Component - Renders SVG props with proper positioning
-->
<script lang="ts">
	import type { PropData } from '$lib/domain';
	import { onMount } from 'svelte';

	interface Props {
		propData: PropData;
		gridMode?: string;
		onLoaded?: (componentType: string) => void;
		onError?: (componentType: string, error: string) => void;
	}

	let { propData, gridMode = 'diamond', onLoaded, onError }: Props = $props();

	let propElement: SVGGElement;
	let loaded = $state(false);
	let error = $state<string | null>(null);

	// Calculate position based on location and grid mode
	const position = $derived(() => {
		if (!propData) return { x: 475, y: 475 };

		// Props use hand coordinates (where staffs are positioned)
		const { location } = propData;

		// Base coordinates for diamond grid hand points
		const diamondHandPoints: Record<string, { x: number; y: number }> = {
			'n': { x: 475, y: 175 },
			'ne': { x: 650, y: 250 },
			'e': { x: 725, y: 475 },
			'se': { x: 650, y: 700 },
			's': { x: 475, y: 775 },
			'sw': { x: 300, y: 700 },
			'w': { x: 225, y: 475 },
			'nw': { x: 300, y: 250 }
		};

		const boxHandPoints: Record<string, { x: number; y: number }> = {
			'n': { x: 475, y: 200 },
			'ne': { x: 625, y: 275 },
			'e': { x: 700, y: 475 },
			'se': { x: 625, y: 675 },
			's': { x: 475, y: 750 },
			'sw': { x: 325, y: 675 },
			'w': { x: 250, y: 475 },
			'nw': { x: 325, y: 275 }
		};

		const points = gridMode === 'box' ? boxHandPoints : diamondHandPoints;
		return points[location] || { x: 475, y: 475 };
	});

	// Get prop SVG path
	const propPath = $derived(() => {
		if (!propData) return '/images/props/staff.svg';
		return `/images/props/${propData.prop_type}.svg`;
	});

	onMount(() => {
		// Simulate loading
		setTimeout(() => {
			loaded = true;
			onLoaded?.(`${propData?.color}-prop`);
		}, 100);
	});
</script>

<!-- Prop Group -->
<g 
	bind:this={propElement}
	class="prop-group {propData?.color}-prop"
	class:loaded
	data-prop-color={propData?.color}
	data-prop-type={propData?.prop_type}
	data-location={propData?.location}
	transform="translate({position().x}, {position().y}) rotate({propData?.rotation_angle || 0})"
>
	{#if error}
		<!-- Error state -->
		<rect x="-15" y="-15" width="30" height="30" fill="red" opacity="0.5" rx="3" />
		<text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
	{:else if !loaded}
		<!-- Loading state -->
		<rect x="-12" y="-12" width="24" height="24" fill="{propData?.color === 'blue' ? '#2E3192' : '#ED1C24'}" opacity="0.3" rx="2" />
		<animate attributeName="opacity" values="0.3;0.8;0.3" dur="1s" repeatCount="indefinite" />
	{:else}
		<!-- Actual prop SVG -->
		<image 
			href={propPath()}
			width="50" 
			height="50" 
			x="-25" 
			y="-25"
			class="prop-svg {propData?.color}-prop-svg"
			on:error={() => {
				error = 'Failed to load prop SVG';
				onError?.(`${propData?.color}-prop`, error);
			}}
		/>

		<!-- Debug info (if needed) -->
		{#if import.meta.env.DEV}
			<circle r="2" fill="green" opacity="0.5" />
			<text x="0" y="-30" text-anchor="middle" font-size="6" fill="black">
				{propData?.location}
			</text>
		{/if}
	{/if}
</g>

<style>
	.prop-group {
		transition: all 0.2s ease;
		transform-origin: center;
	}

	.prop-group.loaded {
		opacity: 1;
	}

	.prop-svg {
		pointer-events: none;
	}

	.blue-prop-svg {
		filter: hue-rotate(240deg) saturate(1.2);
	}

	.red-prop-svg {
		filter: hue-rotate(0deg) saturate(1.2);
	}

	/* Ensure proper layering */
	.prop-group {
		z-index: 1;
	}
</style>
