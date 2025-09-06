<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import type { ImageExportSettings } from '$lib/state/image-export-settings.svelte';

	// Props
	const { settings } = $props<{
		settings: ImageExportSettings;
	}>();

	// Local state
	let canvas = $state<HTMLCanvasElement | null>(null);

	// Update the sample pictograph when settings change
	$effect(() => {
		if (browser && canvas) {
			drawExamplePictograph();
		}
	});

	// Draw the example pictograph on mount
	onMount(() => {
		if (browser && canvas) {
			drawExamplePictograph();
		}
	});

	// Draw the example pictograph
	function drawExamplePictograph() {
		if (!canvas) return;

		const ctx = canvas.getContext('2d');
		if (!ctx) return;

		// Clear canvas
		ctx.clearRect(0, 0, canvas.width, canvas.height);

		// Get settings
		const { addDifficultyLevel, addWord, addUserInfo, addBeatNumbers, addReversalSymbols } =
			settings;

		// Draw pictograph background
		ctx.fillStyle = 'white';
		ctx.fillRect(0, 0, canvas.width, canvas.height);

		// Draw grid (simplified diamond)
		ctx.strokeStyle = '#cccccc';
		ctx.lineWidth = 1;

		// Diamond grid
		ctx.beginPath();
		ctx.moveTo(canvas.width / 2, 20);
		ctx.lineTo(canvas.width - 20, canvas.height / 2);
		ctx.lineTo(canvas.width / 2, canvas.height - 20);
		ctx.lineTo(20, canvas.height / 2);
		ctx.closePath();
		ctx.stroke();

		// Inner diamond
		ctx.beginPath();
		ctx.moveTo(canvas.width / 2, 40);
		ctx.lineTo(canvas.width - 40, canvas.height / 2);
		ctx.lineTo(canvas.width / 2, canvas.height - 40);
		ctx.lineTo(40, canvas.height / 2);
		ctx.closePath();
		ctx.stroke();

		// Cross
		ctx.beginPath();
		ctx.moveTo(canvas.width / 2, 20);
		ctx.lineTo(canvas.width / 2, canvas.height - 20);
		ctx.moveTo(20, canvas.height / 2);
		ctx.lineTo(canvas.width - 20, canvas.height / 2);
		ctx.stroke();

		// Draw difficulty level indicator
		if (addDifficultyLevel) {
			const radius = 15;
			ctx.fillStyle = '#167bf4';
			ctx.beginPath();
			ctx.arc(30, 30, radius, 0, Math.PI * 2);
			ctx.fill();

			ctx.fillStyle = 'white';
			ctx.font = 'bold 16px Arial';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText('2', 30, 30);
		}

		// Draw word/title
		if (addWord) {
			ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
			ctx.fillRect(0, 10, canvas.width, 20);

			ctx.fillStyle = 'black';
			ctx.font = '12px Arial';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText('Example', canvas.width / 2, 20);
		}

		// Draw user info
		if (addUserInfo) {
			ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
			ctx.fillRect(0, canvas.height - 30, canvas.width, 20);

			ctx.fillStyle = 'black';
			ctx.font = '10px Arial';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText('User • Sample', canvas.width / 2, canvas.height - 20);
		}

		// Draw beat number
		if (addBeatNumbers) {
			ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
			ctx.beginPath();
			ctx.arc(canvas.width - 20, 20, 12, 0, Math.PI * 2);
			ctx.fill();

			ctx.fillStyle = 'white';
			ctx.font = 'bold 12px Arial';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText('1', canvas.width - 20, 20);
		}

		// Draw reversal symbols
		if (addReversalSymbols) {
			// Blue reversal
			ctx.fillStyle = 'blue';
			ctx.beginPath();
			ctx.arc(canvas.width / 2 - 10, canvas.height - 40, 8, 0, Math.PI * 2);
			ctx.fill();

			// Red reversal
			ctx.fillStyle = 'red';
			ctx.beginPath();
			ctx.arc(canvas.width / 2 + 10, canvas.height - 40, 8, 0, Math.PI * 2);
			ctx.fill();
		}

		// Draw props (simplified)
		// Blue prop
		ctx.strokeStyle = 'blue';
		ctx.lineWidth = 3;
		ctx.beginPath();
		ctx.moveTo(canvas.width / 2 - 30, canvas.height / 2);
		ctx.lineTo(canvas.width / 2 - 10, canvas.height / 2 - 30);
		ctx.stroke();

		// Red prop
		ctx.strokeStyle = 'red';
		ctx.lineWidth = 3;
		ctx.beginPath();
		ctx.moveTo(canvas.width / 2 + 30, canvas.height / 2);
		ctx.lineTo(canvas.width / 2 + 10, canvas.height / 2 + 30);
		ctx.stroke();

		// Letter in center
		ctx.fillStyle = 'black';
		ctx.font = 'bold 24px Arial';
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.fillText('A', canvas.width / 2, canvas.height / 2);
	}
</script>

<div class="example-pictograph">
	<canvas bind:this={canvas} width="180" height="180" class="pictograph-canvas"></canvas>
</div>

<style>
	.example-pictograph {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #fff;
		border-radius: 6px;
		overflow: hidden;
	}

	.pictograph-canvas {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}
</style>
