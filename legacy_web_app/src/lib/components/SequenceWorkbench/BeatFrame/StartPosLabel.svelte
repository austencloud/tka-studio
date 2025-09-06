<script lang="ts">
	import { onMount } from 'svelte';

	let container: HTMLElement;
	let parentSize = 0;

	// Function to calculate font size based on parent container size
	function calculateFontSize(): string {
		// Base the font size on the parent container width
		// Using a percentage ensures it scales proportionally
		return `${Math.max(parentSize * 0.15, 12)}px`;
	}

	// Function to update the parent size
	function updateParentSize() {
		if (!container) return;

		// Get the parent beat container
		const beatContainer = container.closest('.beat-container');
		if (!beatContainer) return;

		// Get the computed size of the beat container
		const computedStyle = window.getComputedStyle(beatContainer);
		const width = parseFloat(computedStyle.width);

		// Update the parent size
		parentSize = width;
	}

	onMount(() => {
		// Initial size calculation
		updateParentSize();

		// Set up a resize observer to update when the container size changes
		const resizeObserver = new ResizeObserver(() => {
			updateParentSize();
		});

		// Find the parent beat container to observe
		const beatContainer = container.closest('.beat-container');
		if (beatContainer) {
			resizeObserver.observe(beatContainer);
		}

		// Clean up the observer when the component is destroyed
		return () => {
			resizeObserver.disconnect();
		};
	});
</script>

<div class="start-pos-label" bind:this={container} style="font-size: {calculateFontSize()}">
	Start
</div>

<style>
	.start-pos-label {
		font-weight: bold;
		text-align: left;
		background-color: transparent;
		color: #000;
		padding: 0;
		border-radius: 4px;
		position: absolute;
		top: 3px;
		/* Changed from right to left */
		left: 10px;
		text-align: left;
		/* Add a subtle text shadow to make it readable on any background */
		text-shadow:
			0px 0px 2px #fff,
			0px 0px 3px #fff,
			0px 0px 4px #fff;
		/* Prevent text selection */
		user-select: none;
		/* Ensure it's above the pictograph but doesn't interfere with interactions */
		pointer-events: none;
		z-index: 5;
		/* Force alignment to top-left */
		margin: 0;
		width: auto;
		height: auto;
		display: block;
	}
</style>
