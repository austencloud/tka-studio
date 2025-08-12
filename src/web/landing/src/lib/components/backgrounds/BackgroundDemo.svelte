<script lang="ts">
	import { browser } from '$app/environment';
	import BackgroundCanvas from '$lib/components/backgrounds/BackgroundCanvas.svelte';
	import BackgroundController from '$lib/components/backgrounds/BackgroundController.svelte';
	import BackgroundProvider from '$lib/components/backgrounds/BackgroundProvider.svelte';
	import type { BackgroundType, QualityLevel } from '$lib/components/backgrounds/types/types';

	// Props
	const {
		backgroundType: propBackgroundType,
		quality: propQuality,
		showControls,
		width: propWidth,
		height: propHeight,
	} = $props<{
		backgroundType?: BackgroundType;
		quality?: QualityLevel;
		showControls?: boolean;
		width?: number;
		height?: number;
	}>();

	// Component state
	let currentBackground = $state<BackgroundType>(propBackgroundType || 'snowfall');
	let currentQuality = $state<QualityLevel>(propQuality || 'medium');
	let isVisible = $state(true);
	let controller: BackgroundController;

	// Available options
	const backgroundTypes: BackgroundType[] = ['snowfall', 'nightSky'];
	const qualityLevels: QualityLevel[] = ['low', 'medium', 'high'];

	// Performance metrics
	let fps = $state(0);
	let showMetrics = $state(false);

	// Get dimensions from props or default to viewport
	let dimensions = $state({
		width: propWidth || (browser ? window.innerWidth : 1920),
		height: propHeight || (browser ? window.innerHeight : 1080),
	});

	// Update dimensions on window resize
	if (browser) {
		const handleResize = () => {
			if (!propWidth || !propHeight) {
				dimensions = {
					width: window.innerWidth,
					height: window.innerHeight,
				};
			}
		};

		window.addEventListener('resize', handleResize);

		// Cleanup
		if (typeof window !== 'undefined') {
			$effect(() => {
				return () => {
					window.removeEventListener('resize', handleResize);
				};
			});
		}
	}

	// Handle control changes
	function handleBackgroundChange(event: Event) {
		const target = event.target;
		if (target instanceof HTMLSelectElement) {
			currentBackground = target.value as BackgroundType;
			controller?.setBackgroundType(currentBackground);
		}
	}

	function handleQualityChange(event: Event) {
		const target = event.target;
		if (target instanceof HTMLSelectElement) {
			currentQuality = target.value as QualityLevel;
			controller?.setQuality(currentQuality);
		}
	}

	function toggleVisibility() {
		isVisible = !isVisible;
		controller?.setVisibility(isVisible);
	}

	function handlePerformanceReport(report: { fps: number }) {
		fps = report.fps;
	}

	function handleReady() {
		console.log('Background system ready');
	}

	function handleError(error: { message: string }) {
		console.error('Background system error:', error.message);
	}
</script>

<div class="background-demo" style="width: {dimensions.width}px; height: {dimensions.height}px;">
	<BackgroundProvider>
		<div class="canvas-container">
			<BackgroundCanvas />
		</div>

		<BackgroundController
			bind:this={controller}
			backgroundType={currentBackground}
			quality={currentQuality}
			{dimensions}
			{isVisible}
			onready={handleReady}
			onerror={handleError}
			onperformanceReport={handlePerformanceReport}
		/>

		{#if showControls}
			<div class="controls">
				<div class="control-group">
					<label for="background-select">Background:</label>
					<select
						id="background-select"
						value={currentBackground}
						onchange={handleBackgroundChange}
					>
						{#each backgroundTypes as type}
							<option value={type}>{type}</option>
						{/each}
					</select>
				</div>

				<div class="control-group">
					<label for="quality-select">Quality:</label>
					<select
						id="quality-select"
						value={currentQuality}
						onchange={handleQualityChange}
					>
						{#each qualityLevels as level}
							<option value={level}>{level}</option>
						{/each}
					</select>
				</div>

				<button onclick={toggleVisibility}>
					{isVisible ? 'Hide' : 'Show'} Background
				</button>

				<button onclick={() => (showMetrics = !showMetrics)}>
					{showMetrics ? 'Hide' : 'Show'} Metrics
				</button>
			</div>
		{/if}

		{#if showMetrics && fps > 0}
			<div class="metrics">
				<div class="metric">
					<span class="label">FPS:</span>
					<span class="value">{fps.toFixed(1)}</span>
				</div>
			</div>
		{/if}
	</BackgroundProvider>
</div>

<style>
	.background-demo {
		position: relative;
		overflow: hidden;
		background: #000;
	}

	.canvas-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 0;
	}

	.controls {
		position: absolute;
		top: 20px;
		left: 20px;
		z-index: 10;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 15px;
		border-radius: 8px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		display: flex;
		flex-direction: column;
		gap: 10px;
		min-width: 200px;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.control-group label {
		font-size: 14px;
		font-weight: 500;
		min-width: 80px;
	}

	.control-group select,
	.controls button {
		padding: 6px 10px;
		border: 1px solid #444;
		border-radius: 4px;
		background: #222;
		color: white;
		font-size: 14px;
		cursor: pointer;
	}

	.control-group select:hover,
	.controls button:hover {
		background: #333;
	}

	.metrics {
		position: absolute;
		top: 20px;
		right: 20px;
		z-index: 10;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 15px;
		border-radius: 8px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		font-size: 14px;
	}

	.metric {
		display: flex;
		justify-content: space-between;
		gap: 15px;
	}

	.metric .label {
		font-weight: 500;
	}

	.metric .value {
		font-family: 'Courier New', monospace;
		color: #0f0;
	}
</style>
