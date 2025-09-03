<!-- src/lib/components/SequenceWorkbench/BeatFrame/SelectionOverlay.svelte -->
<script lang="ts">
	export let isSelected: boolean = false;

	// Force reactivity by using a derived value
	$: selectionClass = isSelected ? 'selected' : '';
</script>

<div class="overlay {selectionClass}"></div>

<style>
	.overlay {
		position: absolute;
		inset: 1px; /* Extend beyond the beat container */
		border: 4px solid transparent;
		border-radius: 8px;
		pointer-events: none; /* Important - this lets events pass through */
		transition: all 0.3s ease-in-out;
		z-index: 3;
	}

	.selected {
		border-color: #ffcc00; /* Brighter gold */
		box-shadow:
			0 0 0 2px rgba(255, 204, 0, 0.5),
			0 0 10px 2px rgba(255, 204, 0, 0.3);
		background-color: rgba(255, 255, 200, 0.1); /* Very subtle highlight */
	}
</style>
