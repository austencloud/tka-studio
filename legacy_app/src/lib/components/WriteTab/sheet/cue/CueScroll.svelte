<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { actStore } from '../../stores/actStore';
	import { uiStore } from '../../stores/uiStore';
	import CueBox from './CueBox.svelte';

	const dispatch = createEventDispatcher();

	// Grid dimensions
	const ROWS = 24;

	let scrollElement: HTMLDivElement;

	// Handle scroll events
	function handleScroll() {
		if (scrollElement) {
			dispatch('scroll', { scrollTop: scrollElement.scrollTop });
		}
	}

	// Handle cue updates
	function handleCueUpdate(event: CustomEvent) {
		const { row, cue, timestamp } = event.detail;
		actStore.updateCueAndTimestamp(row, cue, timestamp);
	}

	// Sync scroll position when the store updates
	$: if (scrollElement && $uiStore.scrollPosition.cueScroll !== undefined) {
		scrollElement.scrollTop = $uiStore.scrollPosition.cueScroll;
	}
</script>

<div class="cue-scroll" bind:this={scrollElement} on:scroll={handleScroll}>
	<div class="cue-container">
		{#each Array(ROWS) as _, rowIndex}
			<CueBox
				row={rowIndex}
				cue={$actStore.act.sequences[rowIndex]?.cue || ''}
				timestamp={$actStore.act.sequences[rowIndex]?.timestamp || ''}
				on:update={handleCueUpdate}
			/>
		{/each}
	</div>
</div>

<style>
	.cue-scroll {
		width: 200px;
		min-width: 150px; /* Minimum width */
		max-width: 250px; /* Maximum width */
		overflow-y: hidden; /* Hide vertical scrollbar */
		overflow-x: hidden;
		background-color: #252525;
		border-right: 1px solid #333;
	}

	.cue-container {
		display: grid;
		grid-auto-rows: minmax(
			var(--cell-size, 80px),
			auto
		); /* Match the grid row height and allow growth */
		width: 100%;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.cue-scroll {
			width: 150px;
		}
	}

	@media (max-width: 480px) {
		.cue-scroll {
			width: 120px;
		}
	}
</style>
