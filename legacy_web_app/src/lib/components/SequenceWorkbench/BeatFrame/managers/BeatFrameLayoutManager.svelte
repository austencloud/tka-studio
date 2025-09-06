<!-- src/lib/components/SequenceWorkbench/BeatFrame/managers/BeatFrameLayoutManager.svelte -->
<script lang="ts" module>
	// Export the interface for the component
	export interface BeatFrameLayoutManager {
		getLayoutInfo: () => {
			beatRows: number;
			beatCols: number;
			cellSize: number;
			contentOverflows: boolean;
			naturalGridHeight: number;
		};
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { useResizeObserver } from '$lib/composables/useResizeObserver';
	import { autoAdjustLayout, calculateCellSize } from '../beatFrameHelpers';
	import { layoutStore } from '$lib/stores/layout/layoutStore';
	import { createEventDispatcher } from 'svelte';
	import type { BeatFrameLayoutOptions } from '$lib/types/BeatFrameLayoutOptions';

	// Create event dispatcher for natural height changes
	const dispatch = createEventDispatcher<{
		naturalheightchange: { height: number };
		layoutchanged: { rows: number; cols: number; beatCount: number };
	}>();

	// Use Svelte 5 runes for reactive state
	const { size: sizeStore, resizeObserver } = useResizeObserver({
		width: browser ? window.innerWidth : 800,
		height: browser ? window.innerHeight : 600
	});

	// Convert the size store to a reactive value
	const size = $derived({
		width: $sizeStore?.width || 0,
		height: $sizeStore?.height || 0
	});

	// Props
	const {
		beatCount,
		containerRef,
		isScrollable = $bindable(false),
		layoutOverride = $bindable(null),
		fullScreenMode = $bindable(false)
	} = $props<{
		beatCount: number;
		containerRef: HTMLElement | null;
		isScrollable?: boolean;
		layoutOverride?: BeatFrameLayoutOptions | null;
		fullScreenMode?: boolean;
	}>();

	// Local state
	let beatRows = $state(1);
	let beatCols = $state(1);
	let prevRows = $state(1);
	let prevCols = $state(1);
	let cellSize = $state(100);
	let naturalGridHeight = $state(0);
	let contentOverflows = $state(false);

	// Track the full sequence widget dimensions
	let sequenceWidgetWidth = $state(0);
	let sequenceWidgetHeight = $state(0);

	// Listen for sequence widget dimensions
	let sequenceWidgetDimensionsListener: (event: CustomEvent) => void;

	// Calculate layout based on beat count
	$effect(() => {
		// Always ensure at least one row for the start position beat
		[beatRows, beatCols] = autoAdjustLayout(Math.max(1, beatCount));

		// Check if the layout has changed
		if (beatRows !== prevRows || beatCols !== prevCols) {
			// Update the layout store
			layoutStore.updateLayout(beatRows, beatCols, beatCount);

			// Update previous values
			prevRows = beatRows;
			prevCols = prevCols;

			// Dispatch a custom event for layout changes
			dispatch('layoutchanged', {
				rows: beatRows,
				cols: beatCols,
				beatCount
			});

			// Also dispatch a global event for components that aren't direct parents
			const event = new CustomEvent('layout-changed', {
				bubbles: true,
				detail: {
					rows: beatRows,
					cols: beatCols,
					beatCount,
					previousLayout: { rows: prevRows, cols: prevCols }
				}
			});
			document.dispatchEvent(event);

			// Check for overflow after layout changes
			// Delay to ensure DOM is updated
			setTimeout(checkForOverflow, 100);
		}
	});

	// Calculate natural grid height
	$effect(() => {
		if (!containerRef) return;

		const gridElement = containerRef.querySelector('.beat-frame');
		if (gridElement) {
			naturalGridHeight = gridElement.scrollHeight; // Use scrollHeight for the most accurate content height
		} else {
			// Fallback calculation if element not ready
			naturalGridHeight = beatRows * cellSize + 20; // Add padding-bottom (20px) of the .beat-frame
		}

		// Dispatch natural height change event
		if (naturalGridHeight > 0) {
			dispatch('naturalheightchange', { height: naturalGridHeight });
		}

		// Check for overflow after natural height is calculated
		// This needs to be delayed to ensure DOM is updated
		setTimeout(checkForOverflow, 50);
	});

	// Calculate cell size based on the full sequence widget dimensions
	$effect(() => {
		// Only calculate if we have valid dimensions
		if (sequenceWidgetWidth > 0 && sequenceWidgetHeight > 0) {
			// Use the full sequence widget height instead of the beat frame's height
			cellSize = calculateCellSize(
				beatCount,
				sequenceWidgetWidth,
				sequenceWidgetHeight,
				beatRows,
				beatCols + 1, // Add 1 for start position column
				0 // No gap
			);
		} else {
			// Fallback to using the beat frame's dimensions if sequence widget dimensions aren't available
			cellSize = calculateCellSize(
				beatCount,
				size.width,
				size.height,
				beatRows,
				beatCols + 1, // Add 1 for start position column
				0 // No gap
			);
		}

		// Check for overflow after cell size is calculated
		// This needs to be delayed to ensure DOM is updated
		setTimeout(checkForOverflow, 100);
	});

	// Add an effect to check for overflow when beat count changes
	$effect(() => {
		// Just reference beatCount to make the effect depend on it
		if (beatCount >= 0) {
			// Delay the check to ensure DOM is updated
			setTimeout(checkForOverflow, 150);
		}
	});

	// Add an effect to check for overflow when layout changes
	$effect(() => {
		// Just reference these values to make the effect depend on them
		if (beatRows > 0 && beatCols > 0) {
			// Delay the check to ensure DOM is updated
			setTimeout(checkForOverflow, 150);
		}
	});

	// Add an effect to check for overflow when size changes
	$effect(() => {
		// Just reference size to make the effect depend on it
		if (size.width > 0 && size.height > 0) {
			// Delay the check to ensure DOM is updated
			setTimeout(checkForOverflow, 150);
		}
	});

	// Function to check if content overflows container and update state
	function checkForOverflow() {
		if (!containerRef) return;

		const container = containerRef;
		const beatFrame = container.querySelector('.beat-frame');

		if (!beatFrame) return;

		// Find the sequence widget container (parent of our container)
		// This is the actual constrained height container we need to check against
		const sequenceWidget = container.closest('.sequence-widget') || container.parentElement;

		// Get the available height from the sequence widget or parent element
		// This is the actual constrained height we need to work within
		const availableHeight =
			sequenceWidgetHeight > 0
				? sequenceWidgetHeight
				: sequenceWidget
					? sequenceWidget.clientHeight
					: container.clientHeight;

		// Get the content dimensions
		const contentHeight = beatFrame.scrollHeight; // Use scrollHeight for more accurate measurement
		const contentWidth = beatFrame.scrollWidth; // Use scrollWidth for more accurate measurement
		const containerWidth = container.clientWidth;

		// Add a small buffer to prevent flickering at the boundary
		const buffer = 10; // 10px buffer

		// Calculate overflow - check both height and width
		// Compare content height to the available height from sequence widget
		const heightOverflow = contentHeight > availableHeight - buffer;
		const widthOverflow = contentWidth > containerWidth + buffer;

		// Get the minimum cell size based on fullscreen mode
		const isLikelyFullscreen = containerWidth > 800 && availableHeight > 600;
		const minCellSize = isLikelyFullscreen ? 100 : 80; // Match values from beatFrameHelpers.ts

		// Check if the current cell size is at or near the minimum threshold
		// If so, we should enable scrolling to prevent further shrinking
		const cellSizeNearMinimum = cellSize <= minCellSize * 1.1; // Add 10% buffer

		// Calculate the total height needed for the grid
		const totalGridHeight = beatRows * cellSize;

		// Check if the grid would be too tall for the available height
		const gridTooTall = totalGridHeight > availableHeight - 40; // 40px buffer for padding

		// Enhanced overflow detection:
		// 1. If content physically overflows the container, enable scrollbars
		// 2. If cell size is at/near minimum and we have multiple rows, enable scrollbars
		// 3. If the grid would be too tall for the container, enable scrollbars
		const newOverflowState = heightOverflow || widthOverflow || gridTooTall;

		// Always log overflow information for debugging
		console.debug('BeatFrame overflow analysis:', {
			availableHeight,
			contentHeight,
			containerWidth,
			contentWidth,
			heightOverflow,
			widthOverflow,
			cellSize,
			minCellSize,
			cellSizeNearMinimum,
			beatRows,
			totalGridHeight,
			gridTooTall,
			newOverflowState,
			sequenceWidgetWidth,
			sequenceWidgetHeight
		});

		// Always log the current overflow state for debugging
		console.log('Current overflow state:', {
			contentOverflows,
			newOverflowState,
			heightOverflow,
			widthOverflow,
			cellSizeNearMinimum,
			gridTooTall,
			beatRows,
			cellSize
		});

		// Only update if the state has changed to avoid unnecessary re-renders
		if (contentOverflows !== newOverflowState) {
			console.log('Overflow state changed:', {
				from: contentOverflows,
				to: newOverflowState,
				reason: heightOverflow
					? 'height overflow'
					: widthOverflow
						? 'width overflow'
						: cellSizeNearMinimum
							? 'cell size near minimum'
							: gridTooTall
								? 'grid too tall'
								: 'unknown'
			});

			contentOverflows = newOverflowState;

			// Force a layout recalculation after changing overflow state
			setTimeout(() => {
				if (beatFrame) {
					// Update data-rows attribute to ensure CSS selectors work correctly
					beatFrame.setAttribute('data-rows', String(beatRows));

					// Add a data attribute to indicate if we're in scrollable mode
					// This will be used for CSS selectors to adjust alignment
					beatFrame.setAttribute('data-scrollable', String(newOverflowState));

					// Log the DOM state after update
					console.log('DOM state after update:', {
						dataRows: beatFrame.getAttribute('data-rows'),
						dataScrollable: beatFrame.getAttribute('data-scrollable'),
						parentHasScrollableClass: beatFrame.closest('.scrollable-active') !== null,
						containerScrollHeight: container.scrollHeight,
						containerClientHeight: container.clientHeight
					});
				}
			}, 0);
		}
	}

	// Initialize event listeners
	onMount(() => {
		// Create a listener for the sequence-widget-dimensions event
		sequenceWidgetDimensionsListener = (event: CustomEvent) => {
			if (event.detail && event.detail.width && event.detail.height) {
				sequenceWidgetWidth = event.detail.width;
				sequenceWidgetHeight = event.detail.height;
			}
		};

		// Add the event listener
		document.addEventListener(
			'sequence-widget-dimensions',
			sequenceWidgetDimensionsListener as EventListener
		);

		// Add window resize listener to check for overflow on window resize
		const handleResize = () => {
			setTimeout(checkForOverflow, 100);
		};
		window.addEventListener('resize', handleResize);

		// Check for overflow after component is mounted
		// Delay to ensure DOM is fully rendered
		setTimeout(checkForOverflow, 200);

		return () => {
			// Remove the event listeners when the component is destroyed
			document.removeEventListener(
				'sequence-widget-dimensions',
				sequenceWidgetDimensionsListener as EventListener
			);
			window.removeEventListener('resize', handleResize);
		};
	});

	// Export methods for parent components
	export function getLayoutInfo() {
		return {
			beatRows,
			beatCols,
			cellSize,
			contentOverflows,
			naturalGridHeight
		};
	}
</script>

<!-- This is an invisible component that just manages layout -->
<div style="display: none;" aria-hidden="true">
	<!-- Status for debugging -->
	{#if beatRows > 0 && beatCols > 0}
		<!-- Layout manager initialized -->
	{/if}
</div>
