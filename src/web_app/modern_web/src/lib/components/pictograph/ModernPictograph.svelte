<!--
ModernPictograph.svelte - Modern Rune-Based Pictograph Component

This is the modern equivalent of the legacy Pictograph.svelte, but using pure Svelte 5 runes
instead of stores. It orchestrates the rendering of Grid, Props, Arrows, and Glyphs.
-->
<script lang="ts">
	import type { PictographData, BeatData } from '$lib/domain';
	import { createGridData } from '$lib/data/gridCoordinates';
	import Grid from './Grid.svelte';
	import Prop from './Prop.svelte';
	import Arrow from './Arrow.svelte';
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
		animationDuration = 200,
		showLoadingIndicator = true,
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

	// Derived state - get effective pictograph data
	const effectivePictographData = $derived(() => {
		if (pictographData) return pictographData;
		if (beatData?.pictograph_data) return beatData.pictograph_data;
		return null;
	});

	// Derived state - grid data
	const gridData = $derived(() => {
		const data = effectivePictographData();
		if (!data) return null;

		const gridMode = data.grid_data?.grid_mode || 'diamond';
		return createGridData(gridMode);
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

	// Loading state management
	const loadingProgress = $derived(() => {
		const required = requiredComponents();
		if (required.length === 0) return 100;
		return Math.round((loadedComponents.size / required.length) * 100);
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
		}
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

			<!-- Props (rendered before arrows for layering) -->
			{#each propsToRender() as { color, propData } (color)}
				<Prop
					{propData}
					motionData={effectivePictographData()?.motions?.[color]}
					gridMode={effectivePictographData()?.grid_data?.grid_mode || 'diamond'}
					allProps={propsToRender().map((p) => p.propData)}
					onLoaded={() => handleComponentLoaded(`${color}-prop`)}
					onError={(error) => handleComponentError(`${color}-prop`, error)}
				/>
			{/each}

			<!-- Arrows (rendered after props) -->
			{#each arrowsToRender() as { color, arrowData } (color)}
				<Arrow
					{arrowData}
					motionData={effectivePictographData()?.motions?.[color]}
					gridMode={effectivePictographData()?.grid_data?.grid_mode || 'diamond'}
					letter={displayLetter() || undefined}
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

		<!-- Loading overlay -->
		{#if isLoading && showLoadingIndicator}
			<g class="loading-overlay">
				<rect
					x="10"
					y="890"
					width="930"
					height="50"
					fill="rgba(59, 130, 246, 0.1)"
					stroke="#3b82f6"
					stroke-width="1"
					rx="4"
				/>
				<text x="475" y="910" text-anchor="middle" font-size="12" fill="#1d4ed8">
					Loading... {loadingProgress()}%
				</text>
				<rect
					x="20"
					y="920"
					width={Math.max(10, (loadingProgress() / 100) * 910)}
					height="4"
					fill="#3b82f6"
					rx="2"
				/>
			</g>
		{/if}

	</svg>
</div>

<style>
	.modern-pictograph {
		position: relative;
		display: inline-block;
		border-radius: 8px;
		overflow: hidden;
		transition: all 0.2s ease;
		background: white;
		border: 1px solid #e5e7eb;
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
