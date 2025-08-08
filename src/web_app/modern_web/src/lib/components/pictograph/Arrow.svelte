<!--
Arrow Component - Renders SVG arrows with proper positioning
-->
<script lang="ts">
	import type { ArrowData } from '$lib/domain';
	import { arrowPositioningService } from './services/arrowPositioningService';
	import { onMount } from 'svelte';

	interface Props {
		arrowData: ArrowData;
		gridMode?: string;
		letter?: string;
		onLoaded?: (componentType: string) => void;
		onError?: (componentType: string, error: string) => void;
	}

	let { arrowData, gridMode = 'diamond', letter, onLoaded, onError }: Props = $props();

	let arrowElement: SVGGElement;
	let loaded = $state(false);
	let error = $state<string | null>(null);

	// Calculate position using positioning service
	const position = $derived(() => {
		if (!arrowData) return { x: 475, y: 475 };

		return arrowPositioningService.calculatePosition({
			arrow_type: arrowData.color,
			motion_type: arrowData.motion_type,
			location: arrowData.location,
			grid_mode: gridMode,
			turns: arrowData.turns,
			letter: letter,
			start_orientation: arrowData.start_orientation,
			end_orientation: arrowData.end_orientation
		});
	});

	// Get arrow SVG path based on motion type and properties
	const arrowPath = $derived(() => {
		if (!arrowData) return '/images/arrows/static/still.svg';

		const { motion_type, rotation_direction } = arrowData;
		const baseDir = `/images/arrows/${motion_type}`;

		// For pro/anti arrows, consider rotation direction
		if (['pro', 'anti'].includes(motion_type)) {
			const isRadial = rotation_direction === 'clockwise';
			const subDir = isRadial ? 'from_radial' : 'from_nonradial';
			return `${baseDir}/${subDir}/${motion_type}.svg`;
		}

		// For other motion types
		return `${baseDir}/${motion_type}.svg`;
	});

	// Apply color transformation
	const coloredSVG = $derived(() => {
		const hexColor = arrowData?.color === 'blue' ? '#2E3192' : '#ED1C24';
		// This would be where we apply color transformations to the SVG
		// For now, we'll rely on CSS styling
		return arrowPath();
	});

	onMount(() => {
		// Simulate loading
		setTimeout(() => {
			loaded = true;
			onLoaded?.(`${arrowData?.color}-arrow`);
		}, 100);
	});
</script>

<!-- Arrow Group -->
<g 
	bind:this={arrowElement}
	class="arrow-group {arrowData?.color}-arrow"
	class:loaded
	data-arrow-color={arrowData?.color}
	data-motion-type={arrowData?.motion_type}
	data-location={arrowData?.location}
	transform="translate({position().x}, {position().y}) rotate({arrowData?.rotation_angle || 0})"
>
	{#if error}
		<!-- Error state -->
		<circle r="10" fill="red" opacity="0.5" />
		<text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
	{:else if !loaded}
		<!-- Loading state -->
		<circle r="8" fill="{arrowData?.color === 'blue' ? '#2E3192' : '#ED1C24'}" opacity="0.3" />
		<animate attributeName="opacity" values="0.3;0.8;0.3" dur="1s" repeatCount="indefinite" />
	{:else}
		<!-- Actual arrow SVG -->
		<image 
			href={coloredSVG()}
			width="40" 
			height="40" 
			x="-20" 
			y="-20"
			class="arrow-svg {arrowData?.color}-arrow-svg"
			on:error={() => {
				error = 'Failed to load arrow SVG';
				onError?.(`${arrowData?.color}-arrow`, error);
			}}
		/>

		<!-- Debug info (if needed) -->
		{#if import.meta.env.DEV}
			<circle r="2" fill="red" opacity="0.5" />
			<text x="0" y="-25" text-anchor="middle" font-size="6" fill="black">
				{arrowData?.location}
			</text>
		{/if}
	{/if}
</g>

<style>
	.arrow-group {
		transition: all 0.2s ease;
		transform-origin: center;
	}

	.arrow-group.loaded {
		opacity: 1;
	}

	.arrow-svg {
		pointer-events: none;
	}

	.blue-arrow-svg {
		filter: hue-rotate(240deg) saturate(1.2);
	}

	.red-arrow-svg {
		filter: hue-rotate(0deg) saturate(1.2);
	}

	/* Ensure proper layering */
	.arrow-group {
		z-index: 2;
	}
</style>
