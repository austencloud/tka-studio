<script lang="ts">
	import { uiStore } from '../../stores/uiStore';

	// Zoom levels in pixels (min and max)
	const MIN_ZOOM = 40;
	const MAX_ZOOM = 200;
	const DEFAULT_ZOOM = 80;

	// Zoom in function
	function zoomIn() {
		uiStore.zoomIn();
	}

	// Zoom out function
	function zoomOut() {
		uiStore.zoomOut();
	}

	// Reset zoom function
	function resetZoom() {
		uiStore.updateCellSize(DEFAULT_ZOOM);
	}
</script>

<div class="zoom-control">
	<button
		class="zoom-button"
		on:click={zoomOut}
		disabled={$uiStore.gridSettings.cellSize <= MIN_ZOOM}
		aria-label="Zoom out"
	>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<circle cx="11" cy="11" r="8"></circle>
			<line x1="21" y1="21" x2="16.65" y2="16.65"></line>
			<line x1="8" y1="11" x2="14" y2="11"></line>
		</svg>
	</button>

	<span class="zoom-level"
		>{$uiStore.gridSettings.cellSize}px ({Math.round(
			($uiStore.gridSettings.cellSize / DEFAULT_ZOOM) * 100
		)}%)</span
	>

	<button
		class="zoom-button"
		on:click={zoomIn}
		disabled={$uiStore.gridSettings.cellSize >= MAX_ZOOM}
		aria-label="Zoom in"
	>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="16"
			height="16"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<circle cx="11" cy="11" r="8"></circle>
			<line x1="21" y1="21" x2="16.65" y2="16.65"></line>
			<line x1="11" y1="8" x2="11" y2="14"></line>
			<line x1="8" y1="11" x2="14" y2="11"></line>
		</svg>
	</button>

	<button class="reset-button" on:click={resetZoom} aria-label="Reset zoom"> Reset </button>
</div>

<style>
	.zoom-control {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		background-color: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
		position: absolute;
		bottom: 1rem;
		right: 1rem;
		z-index: 10;
	}

	.zoom-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 28px;
		height: 28px;
		background-color: #2a2a2a;
		border: none;
		border-radius: 4px;
		color: #e0e0e0;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.zoom-button:hover:not(:disabled) {
		background-color: #3a3a3a;
	}

	.zoom-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.zoom-level {
		font-size: 0.875rem;
		color: #e0e0e0;
		min-width: 90px;
		text-align: center;
	}

	.reset-button {
		background-color: #2a2a2a;
		border: none;
		border-radius: 4px;
		color: #e0e0e0;
		padding: 0.25rem 0.5rem;
		font-size: 0.75rem;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.reset-button:hover {
		background-color: #3a3a3a;
	}
</style>
