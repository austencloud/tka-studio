<!--
Prop Component - Renders SVG props with proper positioning
-->
<script lang="ts">
	import type { PropData, MotionData } from '$lib/domain';
	import { onMount } from 'svelte';

	interface Props {
		propData: PropData;
		motionData?: MotionData;
		gridMode?: string;
		onLoaded?: (componentType: string) => void;
		onError?: (componentType: string, error: string) => void;
	}

	let { propData, motionData, gridMode = 'diamond', onLoaded, onError }: Props = $props();

	let propElement: SVGGElement;
	let loaded = $state(false);
	let error = $state<string | null>(null);
	let svgData = $state<{
		imageSrc: string;
		viewBox: { width: number; height: number };
		center: { x: number; y: number };
	} | null>(null);

	// Calculate position based on motion's end location and grid mode
	const position = $derived(() => {
		if (!propData) return { x: 475, y: 475 };

		// Props use motion's END location, not propData.location
		// This is the critical research finding - props ALWAYS use motion end_loc
		const location = motionData?.end_loc || propData.location;

		// Base coordinates for diamond grid hand points
		const diamondHandPoints: Record<string, { x: number; y: number }> = {
			n: { x: 475, y: 175 },
			ne: { x: 650, y: 250 },
			e: { x: 725, y: 475 },
			se: { x: 650, y: 700 },
			s: { x: 475, y: 775 },
			sw: { x: 300, y: 700 },
			w: { x: 225, y: 475 },
			nw: { x: 300, y: 250 },
		};

		const boxHandPoints: Record<string, { x: number; y: number }> = {
			n: { x: 475, y: 200 },
			ne: { x: 625, y: 275 },
			e: { x: 700, y: 475 },
			se: { x: 625, y: 675 },
			s: { x: 475, y: 750 },
			sw: { x: 325, y: 675 },
			w: { x: 250, y: 475 },
			nw: { x: 325, y: 275 },
		};

		const points = gridMode === 'box' ? boxHandPoints : diamondHandPoints;
		return points[location || 'n'] || { x: 475, y: 475 };
	});

	// Parse SVG to get proper dimensions and center point
	const parsePropSvg = (
		svgText: string
	): { viewBox: { width: number; height: number }; center: { x: number; y: number } } => {
		const doc = new DOMParser().parseFromString(svgText, 'image/svg+xml');
		const svg = doc.documentElement;

		// Get viewBox dimensions
		const viewBoxValues = svg.getAttribute('viewBox')?.split(/\s+/) || ['0', '0', '252.8', '77.8'];
		const viewBox = {
			width: parseFloat(viewBoxValues[2]) || 252.8,
			height: parseFloat(viewBoxValues[3]) || 77.8,
		};

		// Get center point from SVG
		let center = { x: viewBox.width / 2, y: viewBox.height / 2 };

		try {
			const centerElement = doc.getElementById('centerPoint');
			if (centerElement) {
				center = {
					x: parseFloat(centerElement.getAttribute('cx') || '0') || center.x,
					y: parseFloat(centerElement.getAttribute('cy') || '0') || center.y,
				};
			}
		} catch (e) {
			console.warn('SVG center calculation failed, using default center');
		}

		return { viewBox, center };
	};

	// Apply color transformation to SVG content
	const applyColorToSvg = (svgText: string, color: 'blue' | 'red'): string => {
		// Define color values
		const colors = {
			blue: '#2E3192',
			red: '#ED1C24',
		};

		console.log(`🎨 Applying ${color} color to prop SVG`);

		// Replace the entire style block with our colors
		let coloredSvg = svgText.replace(
			/<style type="text\/css">[\s\S]*?<\/style>/g,
			`<style type="text/css">
	.st0{fill:${colors[color]};stroke:#FFFFFF;stroke-width:2.75;stroke-miterlimit:10;}
	.st1{fill:#FF0000;}
</style>`
		);

		console.log(`✅ ${color} color applied to prop SVG`);
		return coloredSvg;
	};

	// Load SVG data
	const loadSvg = async () => {
		try {
			if (!propData) throw new Error('No prop data available');

			const response = await fetch(`/images/props/${propData.prop_type}.svg`);
			if (!response.ok) throw new Error('Failed to fetch SVG');

			const originalSvgText = await response.text();
			const { viewBox, center } = parsePropSvg(originalSvgText);

			// Apply color transformation to the SVG
			const coloredSvgText = applyColorToSvg(originalSvgText, propData.color as 'blue' | 'red');

			svgData = {
				imageSrc: `data:image/svg+xml;base64,${btoa(coloredSvgText)}`,
				viewBox,
				center,
			};

			loaded = true;
			onLoaded?.(`${propData?.color}-prop`);
		} catch (e) {
			error = `Failed to load prop SVG: ${e}`;
			onError?.(`${propData?.color}-prop`, error);
			// Still mark as loaded to prevent blocking
			loaded = true;
		}
	};

	onMount(() => {
		loadSvg();
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
>
	{#if error}
		<!-- Error state -->
		<rect x="-15" y="-15" width="30" height="30" fill="red" opacity="0.5" rx="3" />
		<text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
	{:else if !loaded || !svgData}
		<!-- Loading state -->
		<rect
			x="-12"
			y="-12"
			width="24"
			height="24"
			fill={propData?.color === 'blue' ? '#2E3192' : '#ED1C24'}
			opacity="0.3"
			rx="2"
		/>
		<animate attributeName="opacity" values="0.3;0.8;0.3" dur="1s" repeatCount="indefinite" />
	{:else}
		<!-- Actual prop SVG with proper sizing and centering -->
		<image
			href={svgData.imageSrc}
			transform="
				translate({position().x}, {position().y})
				rotate({0})
				translate({-svgData.center.x}, {-svgData.center.y})
			"
			width={svgData.viewBox.width}
			height={svgData.viewBox.height}
			preserveAspectRatio="xMidYMid meet"
			class="prop-svg"
			onerror={() => {
				error = 'Failed to load prop SVG';
				onError?.(`${propData?.color}-prop`, error);
			}}
		/>

		<!-- Debug info (if needed) -->
		{#if import.meta.env.DEV}
			<circle r="2" fill="green" opacity="0.5" cx={position().x} cy={position().y} />
			<text x={position().x} y={position().y - 30} text-anchor="middle" font-size="6" fill="black">
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

	/* Ensure proper layering */
	.prop-group {
		z-index: 1;
	}
</style>
