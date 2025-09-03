<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { draggable } from '../utils/dragDropUtils';

	export let src: string;
	export let alt: string;
	export let word: string;

	const dispatch = createEventDispatcher();
	let imageElement: HTMLImageElement;
	let isDragging = false;

	// Mock sequence data for drag and drop
	// In a real implementation, this would be loaded from metadata
	const mockSequenceData = {
		word,
		beats: Array(8)
			.fill(null)
			.map((_, i) => ({
				beat_number: i + 1,
				pictograph_data: {
					letter: 'A',
					startPos: 'center',
					endPos: 'center',
					redPropData: {
						/* prop data */
					},
					bluePropData: {
						/* prop data */
					}
				},
				step_label: `Step ${i + 1}`
			}))
	};

	// Handle drag start and end events
	function handleDragStart() {
		isDragging = true;
		dispatch('dragstart', { sequenceData: mockSequenceData });
	}

	function handleDragEnd() {
		isDragging = false;
		dispatch('dragend');
	}

	// Custom drag handler that uses our utility but also sets the drag image
	function handleDragStartEvent(event: DragEvent) {
		if (!event.dataTransfer || !imageElement) return;
		event.dataTransfer.setDragImage(imageElement, 0, 0);
	}
</script>

<div
	class="thumbnail-image-container"
	class:dragging={isDragging}
	role="button"
	tabindex="0"
	use:draggable={{
		data: mockSequenceData,
		effectAllowed: 'copy',
		onDragStart: handleDragStart,
		onDragEnd: handleDragEnd
	}}
>
	<!-- Fallback image if src is not available -->
	{#if !src || src.includes('undefined')}
		<div class="fallback-image">
			<span>{word.charAt(0)}</span>
		</div>
	{:else}
		<img
			bind:this={imageElement}
			{src}
			{alt}
			class="thumbnail-image"
			loading="lazy"
			on:error={() => {
				// If image fails to load, we could set a fallback
				src = '';
			}}
		/>
	{/if}

	<!-- Drag indicator overlay -->
	<div class="drag-indicator">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		>
			<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
			<polyline points="14 2 14 8 20 8"></polyline>
			<line x1="12" y1="18" x2="12" y2="12"></line>
			<line x1="9" y1="15" x2="15" y2="15"></line>
		</svg>
		<span>Drag to Act Sheet</span>
	</div>
</div>

<style>
	.thumbnail-image-container {
		position: relative;
		width: 100%;
		height: 100%;
		cursor: grab;
		overflow: hidden;
	}

	.thumbnail-image-container.dragging {
		cursor: grabbing;
		opacity: 0.7;
	}

	.thumbnail-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.3s;
	}

	.thumbnail-image-container:hover .thumbnail-image {
		transform: scale(1.05);
	}

	.fallback-image {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		background-color: #444;
		color: #ddd;
		font-size: 3rem;
		font-weight: bold;
	}

	.drag-indicator {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: rgba(0, 0, 0, 0.7);
		color: white;
		opacity: 0;
		transition: opacity 0.2s;
		pointer-events: none;
	}

	.thumbnail-image-container:hover .drag-indicator {
		opacity: 1;
	}

	.drag-indicator svg {
		margin-bottom: 0.5rem;
	}
</style>
