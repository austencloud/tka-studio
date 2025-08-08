<!--
Arrow Component for TKA Pictographs
Based on v1-legacy implementation using Svelte 5 runes
-->
<script lang="ts">
	// Props using runes
	const props = $props<{
		arrowData: {
			color: 'red' | 'blue';
			motionType: string;
			startLoc: string;
			endLoc: string;
			startOri: string;
			endOri: string;
			turns: number;
			coords: { x: number; y: number } | null;
		};
		onLoaded?: () => void;
		onError?: (message: string) => void;
	}>();

	// State using runes
	let isLoaded = $state(false);
	let hasError = $state(false);
	let svgData = $state<string | null>(null);

	// Derived values
	const transform = $derived(() => {
		if (!props.arrowData.coords) return '';

		// Basic positioning - more sophisticated rotation logic would go here
		const rotation = calculateRotation(props.arrowData);
		return `translate(${props.arrowData.coords.x}, ${props.arrowData.coords.y}) rotate(${rotation})`;
	});

	const arrowSvgPath = $derived(() => {
		// Simplified arrow SVG path selection based on motion type and color
		const { motionType, color } = props.arrowData;

		// For now, use a basic arrow - this would be expanded with proper SVG loading
		if (motionType === 'pro') {
			return `/images/arrows/${color}/pro_arrow.svg`;
		} else if (motionType === 'anti') {
			return `/images/arrows/${color}/anti_arrow.svg`;
		} else if (motionType === 'static') {
			return `/images/arrows/${color}/static_arrow.svg`;
		}

		return `/images/arrows/${color}/default_arrow.svg`;
	});

	function calculateRotation(arrowData: typeof props.arrowData): number {
		// Simplified rotation calculation
		// Real implementation would use proper TKA rotation logic
		const { startLoc, endLoc, turns } = arrowData;

		// Basic rotation based on direction
		const locationRotations: Record<string, number> = {
			'n': 0,
			'ne': 45,
			'e': 90,
			'se': 135,
			's': 180,
			'sw': 225,
			'w': 270,
			'nw': 315
		};

		const baseRotation = locationRotations[startLoc] || 0;
		const turnRotation = (turns || 0) * 90; // 90 degrees per turn

		return baseRotation + turnRotation;
	}

	function handleImageLoad() {
		isLoaded = true;
		hasError = false;
		props.onLoaded?.();
	}

	function handleImageError() {
		hasError = true;
		isLoaded = false;
		props.onError?.('Failed to load arrow image');
	}

	// Effect to load SVG data
	$effect(() => {
		if (arrowSvgPath) {
			// For now, we'll use a simple image element
			// In a full implementation, this would load and parse SVG data
			svgData = arrowSvgPath;
		}
	});
</script>

{#if props.arrowData.coords && svgData}
	<g
		{transform}
		data-testid="arrow-{props.arrowData.color}"
		data-motion-type={props.arrowData.motionType}
		data-loc={props.arrowData.startLoc}
	>
		<!-- For now, render a simple arrow shape -->
		<!-- In full implementation, this would render the actual SVG -->
		{#if props.arrowData.motionType === 'static'}
			<!-- Static motion: simple dot -->
			<circle
				cx="0"
				cy="0"
				r="8"
				fill={props.arrowData.color === 'red' ? '#ED1C24' : '#2E3192'}
				stroke="white"
				stroke-width="2"
			/>
		{:else}
			<!-- Dynamic motion: arrow shape -->
			<path
				d="M-20,0 L10,0 M5,-5 L10,0 L5,5"
				stroke={props.arrowData.color === 'red' ? '#ED1C24' : '#2E3192'}
				stroke-width="3"
				fill="none"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		{/if}
	</g>
{/if}
