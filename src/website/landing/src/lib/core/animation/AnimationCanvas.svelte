<script lang="ts">
	import type { CanvasState } from './types';

	interface Props {
		canvasState: CanvasState;
		canvasSize: number;
		onCanvasReady?: (canvas: HTMLCanvasElement) => void;
	}

	let { canvasState, canvasSize, onCanvasReady }: Props = $props();
	let canvasElement: HTMLCanvasElement;

	// Notify parent when canvas is ready
	$effect(() => {
		if (canvasElement && onCanvasReady) {
			onCanvasReady(canvasElement);
		}
	});
</script>

<div class="canvas-container">
	<canvas
		bind:this={canvasElement}
		id="animationCanvas"
		width={canvasSize}
		height={canvasSize}
	></canvas>
	{#if !canvasState.imagesLoaded && canvasState.canvasReady}
		<div class="canvas-overlay">
			<div class="loading-spinner"></div>
			<p>Loading animation assets...</p>
		</div>
	{/if}
</div>

<style>
	.canvas-container {
		background: rgba(255, 255, 255, 0.95);
		border-radius: 1rem;
		padding: 1rem;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		position: relative;
	}

	.canvas-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.9);
		border-radius: 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: #1e3a8a;
		font-weight: 500;
	}

	.canvas-overlay .loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid rgba(30, 58, 138, 0.3);
		border-radius: 50%;
		border-top-color: #1e3a8a;
		animation: spin 1s ease-in-out infinite;
		margin-bottom: 0.75rem;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	#animationCanvas {
		display: block;
		border-radius: 0.5rem;
		max-width: 100%;
		height: auto;
	}

	@media (max-width: 480px) {
		#animationCanvas {
			width: 100%;
			max-width: 400px;
		}
	}
</style>
