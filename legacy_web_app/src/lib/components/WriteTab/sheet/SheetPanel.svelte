<script lang="ts">
	import { onMount } from 'svelte';
	import ActHeader from './header/ActHeader.svelte';
	import BeatGrid from './grid/BeatGrid.svelte';
	import CueScroll from './cue/CueScroll.svelte';
	import { uiStore } from '../stores/uiStore';

	// Reactive variable to store the current cell size
	let currentCellSize = $uiStore.gridSettings.cellSize;

	// Handle synchronized scrolling between beat grid and cue scroll
	function handleBeatGridScroll(event: CustomEvent) {
		uiStore.updateBeatGridScroll(event.detail.scrollTop);
		uiStore.updateCueScrollPosition(event.detail.scrollTop);
	}

	function handleCueScrollScroll(event: CustomEvent) {
		uiStore.updateCueScrollPosition(event.detail.scrollTop);
		uiStore.updateBeatGridScroll(event.detail.scrollTop);
	}

	// Handle grid resize events
	function handleGridResize(event: CustomEvent) {
		currentCellSize = event.detail.cellSize;
	}
</script>

<div class="sheet-panel">
	<ActHeader />

	<div class="sheet-content" style="--current-cell-size: {currentCellSize}px;">
		<CueScroll on:scroll={handleCueScrollScroll} />
		<BeatGrid on:scroll={handleBeatGridScroll} on:resize={handleGridResize} />
	</div>
</div>

<style>
	.sheet-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		background-color: #1a1a1a;
		color: #e0e0e0;
	}

	.sheet-content {
		display: grid;
		grid-template-columns: auto 1fr; /* First column for cues, second for grid */
		flex: 1;
		overflow: hidden;
		--cell-size: var(--current-cell-size, 80px); /* Share cell size with children */
	}
</style>
