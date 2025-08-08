<script lang="ts">
	// Props
	let {
		onPlay
	}: {
		onPlay?: () => void;
	} = $props();

	function handlePlayClick(event: Event): void {
		event.stopPropagation(); // Prevent card click
		onPlay?.();
	}
</script>

<div class="card-overlay">
	<button type="button" class="play-button" onclick={handlePlayClick} aria-label="Play sequence">
		▶️
	</button>
</div>

<style>
	.card-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.4);
		display: flex;
		align-items: center;
		justify-content: center;
		opacity: 0;
		transition: opacity 0.2s ease;
		pointer-events: none; /* Allow clicks to pass through when hidden */
	}

	.play-button {
		background: rgba(255, 255, 255, 0.9);
		border: none;
		border-radius: 50%;
		width: 60px;
		height: 60px;
		font-size: 1.5rem;
		cursor: pointer;
		transition: transform 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.play-button:hover {
		transform: scale(1.1);
		background: white;
	}

	/* Enable pointer events when overlay is visible */
	:global(.thumbnail-card:hover) .card-overlay {
		pointer-events: auto;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.play-button {
			width: 60px;
			height: 60px;
			font-size: 1.5rem;
		}
	}
</style>
