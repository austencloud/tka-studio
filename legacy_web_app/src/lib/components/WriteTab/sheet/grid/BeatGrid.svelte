<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { actStore } from '../../stores/actStore';
	import { uiStore } from '../../stores/uiStore';
	import { selectionStore } from '../../stores/selectionStore';
	import { dropTarget } from '../../utils/dragDropUtils';
	import BeatCell from './BeatCell.svelte';
	import StepLabel from './StepLabel.svelte';

	const dispatch = createEventDispatcher();

	// Grid dimensions
	const COLUMNS = 8;
	const ROWS = 24;

	let gridElement: HTMLDivElement;
	let gridWidth = 0;
	let gridHeight = 0;
	let resizeObserver: ResizeObserver;

	// Calculate responsive cell size based on container dimensions
	$: responsiveCellSize =
		gridWidth > 0
			? Math.floor((gridWidth - (COLUMNS + 1)) / COLUMNS) // Always use full width
			: 80; // Default fallback

	// Dispatch resize event when cell size changes
	$: if (responsiveCellSize && dispatch) {
		dispatch('resize', {
			cellSize: responsiveCellSize
		});
	}

	// Set up resize observer to track container size changes
	onMount(() => {
		if (gridElement && typeof ResizeObserver !== 'undefined') {
			resizeObserver = new ResizeObserver((entries) => {
				const entry = entries[0];
				if (entry) {
					gridWidth = entry.contentRect.width;
					gridHeight = entry.contentRect.height;

					// Dispatch a resize event to synchronize with CueScroll
					dispatch('resize', {
						width: gridWidth,
						height: gridHeight,
						cellSize: responsiveCellSize
					});
				}
			});

			resizeObserver.observe(gridElement);

			return () => {
				if (resizeObserver) {
					resizeObserver.disconnect();
				}
			};
		}
	});

	// Handle scroll events
	function handleScroll() {
		if (gridElement) {
			dispatch('scroll', { scrollTop: gridElement.scrollTop });
		}
	}

	// Handle drop events
	function handleDrop(event: DragEvent, data: any) {
		// Get the drop target
		const target = event.target as HTMLElement;
		const beatCell = target.closest('.beat-cell');

		if (!beatCell) return;

		// Get the row and column from the data attributes
		const row = parseInt(beatCell.getAttribute('data-row') || '0', 10);
		const col = parseInt(beatCell.getAttribute('data-col') || '0', 10);

		// Use the data from the drop event
		if (data) {
			actStore.populateFromDrop(data, row, col);
		}
	}

	// Handle cell selection
	function handleCellClick(event: CustomEvent) {
		const { row, col } = event.detail;
		selectionStore.selectBeat(row, col);
	}

	// Sync scroll position when the store updates
	$: if (gridElement && $uiStore.scrollPosition.beatGrid !== undefined) {
		gridElement.scrollTop = $uiStore.scrollPosition.beatGrid;
	}
</script>

<div
	class="beat-grid"
	bind:this={gridElement}
	on:scroll={handleScroll}
	use:dropTarget={{
		acceptedTypes: ['application/sequence-data'],
		dropEffect: 'copy',
		onDrop: handleDrop
	}}
>
	<div class="grid-container" style="--columns: {COLUMNS};">
		{#each Array(ROWS) as _, rowIndex}
			{#each Array(COLUMNS) as _, colIndex}
				<div class="beat-cell-wrapper" style="--row: {rowIndex}; --col: {colIndex};">
					<BeatCell
						row={rowIndex}
						col={colIndex}
						beat={$actStore.act.sequences[rowIndex]?.beats[colIndex]}
						on:click={handleCellClick}
					/>

					{#if colIndex === 0}
						<StepLabel
							row={rowIndex}
							col={colIndex}
							label={$actStore.act.sequences[rowIndex]?.beats[colIndex]?.step_label || ''}
						/>
					{/if}
				</div>
			{/each}
		{/each}
	</div>
</div>

<style>
	.beat-grid {
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
		background-color: #1a1a1a;
	}

	.grid-container {
		display: grid;
		grid-template-columns: repeat(var(--columns), 1fr); /* Use 1fr instead of fixed size */
		grid-auto-rows: minmax(var(--cell-size), auto); /* Allow rows to grow if needed */
		gap: 1px;
		padding: 1px;
		width: 100%; /* Always take full width */
		background-color: #333;
	}

	.beat-cell-wrapper {
		position: relative;
		grid-row: calc(var(--row) + 1);
		grid-column: calc(var(--col) + 1);
		background-color: #1a1a1a;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.grid-container {
			--cell-size: 60px;
		}
	}

	@media (max-width: 480px) {
		.grid-container {
			--cell-size: 50px;
		}
	}
</style>
