<!--
Prop Component for TKA Pictographs
Based on v1-legacy implementation using Svelte 5 runes
-->
<script lang="ts">
	// Props using runes
	const props = $props<{
		propData: {
			color: 'red' | 'blue';
			propType: string;
			loc: string;
			ori: string;
			coords: { x: number; y: number } | null;
		};
		onLoaded?: () => void;
		onError?: (message: string) => void;
	}>();

	// State using runes
	let isLoaded = $state(false);
	let hasError = $state(false);

	// Derived values
	const transform = $derived.by(() => {
		if (!props.propData.coords) return '';

		const rotation = calculateRotation(props.propData);
		return `translate(${props.propData.coords.x}, ${props.propData.coords.y}) rotate(${rotation})`;
	});

	function calculateRotation(propData: typeof props.propData): number {
		// Simplified rotation calculation based on orientation
		const { ori } = propData;

		// Basic orientation rotations
		const orientationRotations: Record<string, number> = {
			'in': 0,
			'out': 180,
			'clock': 90,
			'counter': 270
		};

		return orientationRotations[ori] || 0;
	}

	function handleLoad() {
		isLoaded = true;
		hasError = false;
		props.onLoaded?.();
	}

	// Effect to simulate loading
	$effect(() => {
		// Simulate async loading
		setTimeout(() => {
			handleLoad();
		}, 10);
	});
</script>

{#if props.propData.coords}
	<g
		{transform}
		data-testid="prop-{props.propData.color}"
		data-prop-type={props.propData.propType}
		data-loc={props.propData.loc}
		data-ori={props.propData.ori}
	>
		<!-- Staff representation using SVG -->
		{#if props.propData.propType === 'staff'}
			<!-- Try to load actual staff SVG first -->
			<image
				href="/images/props/staff.svg"
				x="-25"
				y="-25"
				width="50"
				height="50"
				onload={handleLoad}
				onerror={() => {
					// Fallback to simplified representation
					hasError = true;
				}}
				style="filter: hue-rotate({props.propData.color === 'red' ? '0deg' : '240deg'});"
			/>

			<!-- Fallback simplified staff if SVG fails -->
			{#if hasError}
				<!-- Staff body (horizontal bar) -->
				<rect
					x="-25"
					y="-3"
					width="50"
					height="6"
					fill={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
					rx="3"
				/>

				<!-- Staff end caps -->
				<circle
					cx="-25"
					cy="0"
					r="4"
					fill={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
				/>
				<circle
					cx="25"
					cy="0"
					r="4"
					fill={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
				/>

				<!-- Orientation indicator -->
				{#if props.propData.ori === 'in'}
					<!-- In orientation: filled center -->
					<circle
						cx="0"
						cy="0"
						r="8"
						fill={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
						stroke="white"
						stroke-width="2"
					/>
				{:else}
					<!-- Out orientation: hollow center -->
					<circle
						cx="0"
						cy="0"
						r="8"
						fill="white"
						stroke={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
						stroke-width="3"
					/>
				{/if}
			{/if}
		{:else}
			<!-- Default prop representation -->
			<circle
				cx="0"
				cy="0"
				r="12"
				fill={props.propData.color === 'red' ? '#ED1C24' : '#2E3192'}
				stroke="white"
				stroke-width="2"
			/>
		{/if}
	</g>
{/if}
