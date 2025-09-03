<!-- src/lib/components/SequenceWorkbench/BeatFrame/BeatFrameGrid.svelte -->
<script lang="ts">
	import StartPosBeat from './StartPosBeat.svelte';
	import AnimatedBeat from './AnimatedBeat.svelte';
	import ReversalGlyph from './ReversalGlyph.svelte';
	import EmptyStartPosLabel from './EmptyStartPosLabel.svelte';

	// Props
	const {
		beatRows,
		beatCols,
		cellSize,
		beats,
		selectedBeatIndex,
		sequenceIsEmpty,
		startPosBeatData,
		beatCount,
		onStartPosBeatClick,
		onBeatClick
	} = $props<{
		beatRows: number;
		beatCols: number;
		cellSize: number;
		beats: any[];
		selectedBeatIndex: number;
		sequenceIsEmpty: boolean;
		startPosBeatData: any;
		beatCount: number;
		onStartPosBeatClick: () => void;
		onBeatClick: (beatIndex: number) => void;
	}>();
</script>

<div
	class="beat-frame"
	style="--total-rows: {beatRows}; --total-cols: {beatCount === 0
		? 1
		: beatCols + 1}; --cell-size: {cellSize}px;"
	data-rows={beatRows}
>
	{#each Array(beatRows) as _, rowIndex}
		{#if rowIndex === 0}
			<div class="beat-container start-position" style="grid-row: 1; grid-column: 1;">
				{#if sequenceIsEmpty}
					<EmptyStartPosLabel onClick={onStartPosBeatClick} />
				{:else}
					<StartPosBeat beatData={startPosBeatData} onClick={onStartPosBeatClick} />
				{/if}
			</div>
		{/if}

		{#each Array(beatCols) as _, colIndex}
			{#if rowIndex * beatCols + colIndex < beats.length}
				{@const beatIndex = rowIndex * beatCols + colIndex}
				{@const beat = beats[beatIndex]}

				{#key beat.id}
					<div
						class="beat-container"
						class:selected={selectedBeatIndex === beatIndex}
						style="grid-row: {rowIndex + 1}; grid-column: {colIndex + (beatCount === 0 ? 1 : 2)};"
					>
						<AnimatedBeat
							{beat}
							onClick={() => onBeatClick(beatIndex)}
							isSelected={selectedBeatIndex === beatIndex}
						/>

						{#if beat.metadata?.blueReversal || beat.metadata?.redReversal}
							<div class="reversal-indicator">
								<ReversalGlyph
									blueReversal={beat.metadata?.blueReversal || false}
									redReversal={beat.metadata?.redReversal || false}
								/>
							</div>
						{/if}
					</div>
				{/key}
			{/if}
		{/each}
	{/each}
</div>

<style>
	.beat-frame {
		display: grid;
		/* Use fixed size columns to maintain 1:1 aspect ratio */
		grid-template-columns: repeat(var(--total-cols), var(--cell-size));
		grid-template-rows: repeat(var(--total-rows), var(--cell-size));
		gap: 0; /* No gap between cells */
		justify-content: center; /* Center the grid horizontally */
		align-content: center; /* Center by default for short sequences */
		width: 100%; /* Use full width instead of fit-content */
		max-width: calc(
			var(--total-cols) * (var(--cell-size) + 20px)
		); /* Prevent excessive stretching */
		height: fit-content; /* Default for non-scrolling */
		margin: 0 auto; /* Center horizontally with no vertical margin */
		transition: all 0.2s ease-out; /* Faster transition for more responsive feel */
		/* Reduce horizontal padding to use more space */
		padding: 0 calc(var(--safe-inset-right, 0px)) calc(20px + var(--safe-inset-bottom, 0px))
			calc(var(--safe-inset-left, 0px));
		transform-origin: center center;
		/* Ensure grid cells maintain their size */
		min-height: calc(var(--total-rows) * var(--cell-size));
	}

	/* When there are multiple rows, align content to the top in scrollable mode */
	:global(.scrollable-active) .beat-frame[data-rows='2'],
	:global(.scrollable-active) .beat-frame[data-rows='3'],
	:global(.scrollable-active) .beat-frame[data-rows='4'],
	:global(.scrollable-active) .beat-frame[data-rows='5'],
	:global(.scrollable-active) .beat-frame[data-rows='6'],
	:global(.scrollable-active) .beat-frame[data-rows='7'],
	:global(.scrollable-active) .beat-frame[data-rows='8'] {
		align-content: start; /* Align to top when scrolling with multiple rows */
		margin-top: 0; /* Remove top margin when aligned to top */
	}

	/* Use the data-scrollable attribute to control alignment */
	:global(.scrollable-active) .beat-frame[data-scrollable='true'] {
		align-content: start !important; /* Always align to top when scrollbars are enabled */
		margin-top: 0; /* Remove top margin when aligned to top */
		padding-top: 10px; /* Add some padding at the top for better spacing */
		padding-bottom: 30px; /* Add padding at the bottom to ensure content isn't cut off */
		/* Ensure grid cells maintain their size */
		min-height: calc(var(--total-rows) * var(--cell-size) + 40px); /* Add padding to total height */
		height: auto !important; /* Override any height constraints */
		/* Add a border to make scrollable area visible for debugging */
		border: 1px solid rgba(0, 255, 0, 0.3);
	}

	.beat-container {
		position: relative;
		width: var(--cell-size); /* Fixed width to maintain aspect ratio */
		height: var(--cell-size); /* Fixed height to maintain aspect ratio */
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: transparent;
		/* Add transition for smooth size changes */
		transition:
			width 0.2s ease,
			height 0.2s ease;
		/* Ensure content is properly centered */
		box-sizing: border-box;
		/* Prevent overflow */
		overflow: hidden;
		/* Enforce 1:1 aspect ratio */
		aspect-ratio: 1 / 1;
	}

	/* Specific styling for start position when it's the only beat */
	.beat-container.start-position:only-child {
		justify-self: center;
		align-self: center;
	}

	.reversal-indicator {
		position: absolute;
		bottom: 5px;
		right: 5px;
		z-index: 2;
	}
</style>
