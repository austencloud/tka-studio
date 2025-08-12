<!--
ModernPictograph.svelte - Modern Rune-Based Pictograph Component

This is the modern equivalent of the legacy Pictograph.svelte, but using pure Svelte 5 runes
instead of stores. It orchestrates the rendering of Grid, Props, Arrows, and Glyphs.
-->
<script lang="ts">
	import type { BeatData, PictographData } from '$lib/domain';
	import { createGridData, createPictographData, createPropData } from '$lib/domain';
	import Arrow from './Arrow.svelte';
	import Grid from './Grid.svelte';
	import Prop from './Prop.svelte';
	import { arrowPositioningService } from './services/arrowPositioningService';
	import TKAGlyph from './TKAGlyph.svelte';

	interface Props {
		/** Pictograph data to render */
		pictographData?: PictographData | null;
		/** Beat data (alternative to pictographData) */
		beatData?: BeatData | null;
		/** Click handler */
		onClick?: () => void;
		/** Debug mode */
		debug?: boolean;
		/** Animation duration for transitions */
		animationDuration?: number;
		/** Show loading indicator */
		showLoadingIndicator?: boolean;
		/** Beat number for display */
		beatNumber?: number | null;
		/** Is this a start position? */
		isStartPosition?: boolean;
		/** SVG dimensions */
		width?: number;
		height?: number;
	}

	let {
		pictographData = null,
		beatData = null,
		onClick,
		debug = false,
		beatNumber = null,
		isStartPosition = false,
		width = undefined,
		height = undefined,
	}: Props = $props();

	// Determine if we should use responsive sizing (no width/height specified)
	const isResponsive = $derived(() => width === undefined && height === undefined);

	// State using runes
	let isLoaded = $state(false);
	let isLoading = $state(false);
	let errorMessage = $state<string | null>(null);
	let loadedComponents = $state(new Set<string>());

	// Arrow positioning coordination state
	let arrowPositions = $state<Record<string, { x: number; y: number; rotation: number }>>({});
	let arrowMirroring = $state<Record<string, boolean>>({});
	let showArrows = $state(false);

	// Derived state - get effective pictograph data
	const effectivePictographData = $derived(() => {
		if (pictographData) return pictographData;
		if (beatData?.pictograph_data) return beatData.pictograph_data;
		return null;
	});

	// Derived state - check if we have required data
	const hasValidData = $derived(() => {
		return effectivePictographData() != null;
	});

	// Derived state - display letter
	const displayLetter = $derived(() => {
		const data = effectivePictographData();
		if (data?.letter) return data.letter;
		if (beatData && !beatData.is_blank) return beatData.beat_number.toString();
		return null;
	});

	// Derived state - arrows to render
	const arrowsToRender = $derived(() => {
		const data = effectivePictographData();
		if (!data?.arrows) return [];

		return Object.entries(data.arrows)
			.filter(([_, arrowData]) => arrowData != null)
			.map(([color, arrowData]) => ({ color: color as 'blue' | 'red', arrowData }));
	});

	// Derived state - props to render
	const propsToRender = $derived(() => {
		const data = effectivePictographData();
		if (!data?.props) return [];

		return Object.entries(data.props)
			.filter(([_, propData]) => propData != null)
			.map(([color, propData]) => ({ color: color as 'blue' | 'red', propData }));
	});

	// Component loading tracking
	let requiredComponents = $derived(() => {
		let components = ['grid'];

		const data = effectivePictographData();
		if (data?.arrows?.blue) components.push('blue-arrow');
		if (data?.arrows?.red) components.push('red-arrow');
		if (data?.props?.blue) components.push('blue-prop');
		if (data?.props?.red) components.push('red-prop');

		return components;
	});

	const allComponentsLoaded = $derived(() => {
		const required = requiredComponents();
		return required.every((component) => loadedComponents.has(component));
	});

	// Reactively update loading state
	$effect(() => {
		if (allComponentsLoaded()) {
			isLoading = false;
			isLoaded = true;
		}
	});

	// Initialize loading when data changes
	$effect(() => {
		if (hasValidData()) {
			isLoading = true;
			isLoaded = false;
			errorMessage = null;
			loadedComponents.clear();

			// Reset arrow positioning coordination
			arrowPositions = {};
			arrowMirroring = {};
			showArrows = false;
		}
	});

	// Arrow positioning coordination - calculate all positions upfront
	$effect(() => {
		const data = effectivePictographData();
		if (!data?.arrows) {
			showArrows = true; // No arrows to position
			return;
		}

		// Calculate positions for all arrows asynchronously
		(async () => {
			try {
				const arrowEntries = Object.entries(data.arrows).filter(
					([_, arrowData]) => arrowData != null
				);

				if (arrowEntries.length === 0) {
					showArrows = true;
					return;
				}

				const positionPromises = arrowEntries.map(async ([color, arrowData]) => {
					const motionData = data.motions?.[color];
					if (!motionData) return null;

					console.log(`🎨 Pictograph.svelte calculating position for ${color} arrow`);
					console.log(`Arrow data:`, {
						motion_type: arrowData.motion_type,
						turns: arrowData.turns,
						position_x: arrowData.position_x,
						position_y: arrowData.position_y,
					});
					console.log(`Motion data:`, {
						motion_type: motionData.motion_type,
						start_loc: motionData.start_loc,
						end_loc: motionData.end_loc,
						turns: motionData.turns,
					});

					// Create pictograph context for positioning
					const pictographContext = createPictographData({
						letter: data.letter || 'A',
						grid_data: createGridData(),
						arrows: { [color]: arrowData },
						props: {
							blue: createPropData({ color: 'blue' }),
							red: createPropData({ color: 'red' }),
						},
						motions: { [color]: motionData },
					});

					// Calculate position and mirroring
					console.log(
						`🔧 Calling arrowPositioningService.calculatePosition for ${color}...`
					);
					const position = await arrowPositioningService.calculatePosition(
						arrowData,
						motionData,
						pictographContext
					);
					console.log(`✅ Position calculated for ${color}:`, position);

					const shouldMirror = arrowPositioningService.shouldMirror(
						arrowData,
						motionData,
						pictographContext
					);
					console.log(`🪞 Mirroring for ${color}:`, shouldMirror);

					return { color, position, shouldMirror };
				});

				// Wait for all positions to be calculated
				const results = await Promise.all(positionPromises);
				console.log(`🎯 All position calculations complete:`, results);

				// Store calculated positions and mirroring
				const newPositions: Record<string, { x: number; y: number; rotation: number }> = {};
				const newMirroring: Record<string, boolean> = {};

				results.forEach((result) => {
					if (result) {
						newPositions[result.color] = result.position;
						newMirroring[result.color] = result.shouldMirror;
					}
				});

				arrowPositions = newPositions;
				arrowMirroring = newMirroring;

				console.log(`📍 Final arrow positions stored:`, arrowPositions);
				console.log(`🪞 Final arrow mirroring stored:`, arrowMirroring);

				// Small delay to ensure all Arrow components are ready, then show all arrows at once
				await new Promise((resolve) => setTimeout(resolve, 50));
				showArrows = true;
			} catch (error) {
				console.error('Failed to calculate arrow positions:', error);
				// Fallback: show arrows without coordination
				showArrows = true;
			}
		})();
	});

	// Component event handlers
	function handleComponentLoaded(componentName: string) {
		loadedComponents.add(componentName);
		if (debug) {
			console.log(`Component loaded: ${componentName}`, {
				loaded: loadedComponents.size,
				required: requiredComponents().length,
			});
		}
	}

	function handleComponentError(componentName: string, error: string) {
		errorMessage = `${componentName}: ${error}`;
		if (debug) {
			console.error(`Component error: ${componentName}`, error);
		}
		// Still mark as loaded to prevent blocking
		handleComponentLoaded(componentName);
	}

	function handleSvgClick() {
		onClick?.();
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onClick?.();
		}
	}

	// SVG viewBox calculation
	const viewBox = $derived(() => `0 0 950 950`);

	// Compute beat number from explicit prop or fallback to beatData
	const computedBeatNumber = $derived(() => {
		return beatNumber ?? beatData?.beat_number ?? null;
	});
</script>

<!-- Main SVG Container -->
<div
	class="modern-pictograph"
	class:loading={isLoading}
	class:loaded={isLoaded}
	class:has-error={errorMessage}
	class:clickable={onClick}
	class:debug-mode={debug}
	class:responsive={isResponsive()}
	style:width={isResponsive() ? '100%' : `${width}px`}
	style:height={isResponsive() ? '100%' : `${height}px`}
>
	<svg
		width={isResponsive() ? '100%' : width || 144}
		height={isResponsive() ? '100%' : height || 144}
		viewBox={viewBox()}
		xmlns="http://www.w3.org/2000/svg"
		onclick={handleSvgClick}
		onkeydown={handleKeyDown}
		role={onClick ? 'button' : 'img'}
		{...onClick ? { tabindex: 0 } : {}}
		aria-label={isStartPosition
			? 'Start Position'
			: `Beat ${computedBeatNumber() || ''} Pictograph`}
	>
		<!-- Background -->
		<rect width="950" height="950" fill="white" />

		{#if hasValidData()}
			<!-- Grid (always rendered first) -->
			<Grid
				gridMode={effectivePictographData()?.grid_data?.grid_mode || 'diamond'}
				onLoaded={() => handleComponentLoaded('grid')}
				onError={(error) => handleComponentError('grid', error)}
				{debug}
			/>

			<!-- Props (rendered first so arrows appear on top) -->
			{#each propsToRender() as { color, propData } (color)}
				{@const motionData = effectivePictographData()?.motions?.[color]}
				<Prop
					{propData}
					{...motionData && { motionData }}
					gridMode={effectivePictographData()?.grid_data?.grid_mode || 'diamond'}
					allProps={Object.values(effectivePictographData()?.props || {})}
					onLoaded={() => handleComponentLoaded(`${color}-prop`)}
					onError={(error) => handleComponentError(`${color}-prop`, error)}
				/>
			{/each}

			<!-- Arrows (rendered after props) -->
			{#each arrowsToRender() as { color, arrowData } (color)}
				{@const motionData = effectivePictographData()?.motions?.[color]}
				<Arrow
					{arrowData}
					{...motionData && { motionData }}
					preCalculatedPosition={arrowPositions[color]}
					preCalculatedMirroring={arrowMirroring[color]}
					showArrow={showArrows}
					onLoaded={() => handleComponentLoaded(`${color}-arrow`)}
					onError={(error) => handleComponentError(`${color}-arrow`, error)}
				/>
			{/each}
			<!-- Letter/Glyph overlay -->
			{#if displayLetter()}
				<TKAGlyph letter={displayLetter()} turnsTuple="(s, 0, 0)" />
			{/if}

			<!-- Beat label -->
			{#if computedBeatNumber() && !isStartPosition}
				<text
					x="475"
					y="50"
					text-anchor="middle"
					font-family="Arial, sans-serif"
					font-size="24"
					font-weight="bold"
					fill="#4b5563"
				>
					{computedBeatNumber()}
				</text>
			{/if}

			<!-- Start position label -->
			{#if isStartPosition}
				<text
					x="475"
					y="50"
					text-anchor="middle"
					font-family="Arial, sans-serif"
					font-size="20"
					font-weight="bold"
					fill="#059669"
				>
					START
				</text>
			{/if}
		{:else}
			<!-- Empty state -->
			<g class="empty-state">
				<circle
					cx="475"
					cy="475"
					r="100"
					fill="#f3f4f6"
					stroke="#e5e7eb"
					stroke-width="2"
				/>
				<text
					x="475"
					y="475"
					text-anchor="middle"
					font-family="Arial, sans-serif"
					font-size="16"
					fill="#6b7280"
				>
					{computedBeatNumber() || 'Empty'}
				</text>
			</g>
		{/if}
	</svg>
</div>

<style>
	.modern-pictograph {
		position: relative;
		border-radius: 8px;
		transition: all 0.2s ease;
		background: white;
		border: 1px solid #e5e7eb;
		/* add a border radius */
	}

	.modern-pictograph.responsive {
		width: 100% !important;
		height: 100% !important;
		display: block;
	}

	.modern-pictograph.clickable {
		cursor: pointer;
	}

	.modern-pictograph.clickable:hover {
		border-color: #3b82f6;
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
		transform: translateY(-1px);
	}

	.modern-pictograph.loading {
		opacity: 0.8;
	}

	.modern-pictograph.has-error {
		border-color: #ef4444;
	}

	.modern-pictograph.debug-mode {
		border-color: #8b5cf6;
		border-width: 2px;
	}

	svg {
		display: block;
		box-sizing: border-box;
	}

	/* Only use 100% size when responsive */
	.responsive svg {
		width: 100%;
		height: 100%;
	}

	.modern-pictograph:focus-within {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
	}

	/* Animation classes for component loading */
	:global(.component-loading) {
		opacity: 0.5;
		animation: pulse 1s infinite;
	}

	@keyframes pulse {
		0% {
			opacity: 0.5;
		}
		50% {
			opacity: 0.8;
		}
		100% {
			opacity: 0.5;
		}
	}
</style>
