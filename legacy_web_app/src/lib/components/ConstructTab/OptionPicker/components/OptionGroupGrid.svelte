<script lang="ts">
	import { getContext } from 'svelte';
	import { type Readable } from 'svelte/store';
	import { fade, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import Option from './Option.svelte';
	import type { PictographData } from '$lib/types/PictographData';
	import {
		LAYOUT_CONTEXT_KEY,
		type LayoutContext,
		type LayoutContextValue
	} from '../layoutContext';
	import { uiState } from '../store';

	// --- Props ---
	export let options: PictographData[] = [];
	export let key: string = ''; // Key for parent transitions if needed

	// --- Context ---
	// Get the context as a Readable<LayoutContextValue>
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);

	// Properly extract the layout config values from the context store
	$: ({
		layoutConfig: { gridColumns: contextGridColumns, optionSize, gridGap, gridClass, aspectClass },
		isMobile: isMobileDevice,
		isTablet: isTabletDevice,
		isPortrait: isPortraitMode
	} = $layoutContext);

	// --- Get Sort Method from Store ---
	let currentSortMethod: string | null;
	uiState.subscribe((state) => {
		currentSortMethod = state.sortMethod;
	});

	// --- Layout Overrides for Single/Two Items ---
	// Determine if special single/two item styling should apply based on sorting context
	$: isTypeSortContext = currentSortMethod === 'type';
	$: applySingleItemClass = options.length === 1 && isTypeSortContext;
	$: applyTwoItemClass = options.length === 2 && isTypeSortContext;

	// Override grid columns if only one or two items are present in this specific grid
	$: actualGridColumns =
		options.length === 1
			? '1fr' // Force single column for single item
			: options.length === 2
				? 'repeat(2, 1fr)' // Force two columns for two items
				: contextGridColumns; // Use the layout context's column definition otherwise
</script>

<div
	class="options-grid {gridClass} {aspectClass}"
	class:single-item-grid={applySingleItemClass}
	class:two-item-grid={applyTwoItemClass}
	class:mobile-grid={isMobileDevice}
	class:tablet-grid={isTabletDevice}
	class:tablet-portrait-grid={isTabletDevice && isPortraitMode}
	style:grid-template-columns={actualGridColumns}
	style:--grid-gap={gridGap}
	style:--option-size={optionSize}
>
	{#each options as option, i ((option.letter ?? '') + (option.startPos ?? '') + (option.endPos ?? '') + i + key)}
		<div
			class="grid-item-wrapper"
			class:single-item={applySingleItemClass}
			class:two-item={applyTwoItemClass}

		>
			<Option pictographData={option} isPartOfTwoItems={applyTwoItemClass} />
		</div>
	{/each}
</div>

<style>
	/* --- Options Grid (Applied per group) --- */
	.options-grid {
		display: grid;
		width: auto;
		max-width: max-content; /* Fit the content */
		justify-items: center; /* Center items horizontally within their grid cell */
		justify-content: center; /* Center the grid content horizontally if grid is wider */
		align-content: center; /* Center grid content vertically */
		/* Add auto margins for horizontal centering within parent */
		margin-left: auto;
		margin-right: auto;
		/* Add some bottom margin for spacing between groups */
		/* margin-bottom: 1rem; */
		position: relative; /* For stacking context */
		transition: height 0.3s ease-out; /* Smooth height transitions */
		will-change: transform; /* Optimize for animations */
		transform: translateZ(0); /* Force GPU acceleration */
	}

	/* Add top margin only if it's NOT part of a multi-group item */
	:global(.options-panel > .options-grid) {
		margin-top: 0.5rem; /* Adjust as needed */
	}
	/* Remove extra top margin if it directly follows a header in single layout */
	:global(.options-panel > .section-header-container + .options-grid) {
		margin-top: 0;
	}

	/* --- Grid Item Wrapper --- */
	.grid-item-wrapper {
		width: var(--option-size, 100px); /* Use size from layout context */
		height: var(--option-size, 100px);
		aspect-ratio: 1 / 1; /* Maintain square aspect ratio */
		display: flex;
		justify-content: center;
		align-items: center;
		position: relative; /* For z-index */
		z-index: 1;
		margin: 0px; /* Add extra margin between items */
		transform-origin: center center; /* Ensure scaling happens from center */
		will-change: transform, opacity; /* Optimize for animations */
		backface-visibility: hidden; /* Prevent flickering during animations */
		transition: transform 0.2s ease-out; /* Smooth hover transition */
	}
	.grid-item-wrapper:hover {
		z-index: 10; /* Bring hovered item to front */
		transform: scale(1.03); /* Subtle scale on hover */
	}

	/* --- Responsive Grid Adjustments (Applied based on context) --- */
	.mobile-grid {
		padding: 0.2rem;
		grid-gap: var(--grid-gap, 6px); /* Potentially smaller gap on mobile */
	}

	.tablet-portrait-grid {
		grid-gap: 0.5rem;
		padding: 0.25rem;
	}

	/* Force minimum spacing between items with desktop square aspect */


	/* Smaller grid items on small screens */


	/* Even smaller for very small screens */
	@media (max-width: 380px) {
		.grid-item-wrapper {
			width: calc(var(--option-size, 100px) * 0.8);
			height: calc(var(--option-size, 100px) * 0.8);
		}

		.mobile-grid {
			grid-gap: 2px;
			padding: 0.1rem;
		}
	}
</style>
