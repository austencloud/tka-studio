<script lang="ts">
	import { onMount } from 'svelte';
	import { uiStore } from '../stores/uiStore';

	// Props
	export let onResize: (width: number) => void;

	// State
	let isDragging = false;
	let startX = 0;
	let startWidth = 0;
	let handle: HTMLDivElement;

	// Set up drag handlers
	function handleMouseDown(event: MouseEvent) {
		isDragging = true;
		startX = event.clientX;
		startWidth = $uiStore.browserPanelWidth;

		// Prevent text selection during drag
		document.body.style.userSelect = 'none';

		// Add event listeners for drag and release
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);

		// Prevent default behavior
		event.preventDefault();
	}

	// Handle keyboard accessibility
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
			const delta = event.key === 'ArrowLeft' ? 10 : -10;
			const newWidth = $uiStore.browserPanelWidth - delta;
			onResize(newWidth);
			event.preventDefault();
		}
	}

	function handleMouseMove(event: MouseEvent) {
		if (!isDragging) return;

		// Calculate new width based on drag distance
		const deltaX = event.clientX - startX;
		const newWidth = startWidth - deltaX; // Subtract because we're dragging from right to left

		// Update width through callback
		onResize(newWidth);
	}

	function handleMouseUp() {
		isDragging = false;

		// Restore text selection
		document.body.style.userSelect = '';

		// Remove event listeners
		document.removeEventListener('mousemove', handleMouseMove);
		document.removeEventListener('mouseup', handleMouseUp);
	}

	// Clean up event listeners on component destruction
	onMount(() => {
		return () => {
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		};
	});
</script>

<div
	class="resize-handle"
	bind:this={handle}
	on:mousedown={handleMouseDown}
	on:keydown={handleKeyDown}
	class:dragging={isDragging}
	title="Drag to resize"
	role="button"
	tabindex="0"
	aria-label="Resize browser panel"
>
	<div class="handle-line"></div>
</div>

<style>
	.resize-handle {
		position: relative;
		width: 20px; /* Wider area for easier targeting */
		height: 100%;
		cursor: ew-resize;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 10;
		background-color: rgba(0, 0, 0, 0.3); /* More visible background */
	}

	.handle-line {
		width: 6px; /* Thicker line for better visibility */
		height: 100%;
		background-color: rgba(52, 152, 219, 0.4); /* More visible blue color */
		border-radius: 3px;
		transition:
			background-color 0.2s,
			width 0.2s;
		position: relative;
	}

	/* Add grip dots to make it look like a draggable handle */
	.handle-line::before {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 2px;
		height: 40px; /* Taller grip area */
		background-image: radial-gradient(circle, rgba(255, 255, 255, 0.7) 1px, transparent 2px);
		background-size: 2px 6px;
		background-repeat: repeat-y;
	}

	.resize-handle:hover .handle-line,
	.dragging .handle-line {
		width: 8px; /* Expand on hover for visual feedback */
		background-color: rgba(52, 152, 219, 0.6); /* Bright blue for better visibility */
	}
</style>
