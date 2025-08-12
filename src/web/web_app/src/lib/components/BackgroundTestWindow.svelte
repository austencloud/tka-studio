<!-- BackgroundTestWindow.svelte - Simple test window to preview all backgrounds -->
<script lang="ts">
	import BackgroundCanvas from './backgrounds/BackgroundCanvas.svelte';
	import BackgroundProvider from './backgrounds/BackgroundProvider.svelte';
	import type { BackgroundType, QualityLevel } from './backgrounds/types/types';

	// State for testing
	let currentBackground = $state<BackgroundType>('aurora');
	let currentQuality = $state<QualityLevel>('medium');
	let isVisible = $state(true);

	// Background options
	const backgroundOptions: { value: BackgroundType; label: string; description: string }[] = [
		{
			value: 'snowfall',
			label: 'Snowfall',
			description: 'Gentle falling snowflakes with shooting stars',
		},
		{
			value: 'nightSky',
			label: 'Night Sky',
			description: 'Starry night with celestial bodies and shooting stars',
		},
		{
			value: 'aurora',
			label: 'Aurora',
			description: 'Colorful aurora with animated blobs and sparkles',
		},

		{
			value: 'bubbles',
			label: 'Bubbles',
			description: 'Underwater scene with floating bubbles and light rays',
		},
	];

	// Quality options
	const qualityOptions: { value: QualityLevel; label: string }[] = [
		{ value: 'minimal', label: 'Minimal' },
		{ value: 'low', label: 'Low' },
		{ value: 'medium', label: 'Medium' },
		{ value: 'high', label: 'High' },
	];

	// Get current background info
	let currentBackgroundInfo = $derived(
		backgroundOptions.find((bg) => bg.value === currentBackground) || backgroundOptions[0]
	);

	// Force re-render when background type or quality changes
	let backgroundKey = $derived(`${currentBackground}-${currentQuality}-${isVisible}`);

	// Log changes for debugging
	$effect(() => {
		console.log(
			`🌌 Test window: Background changed to ${currentBackground} with quality ${currentQuality}, visible: ${isVisible}`
		);
	});
</script>

<div class="test-window">
	<BackgroundProvider>
		<!-- Background Canvas -->
		{#if isVisible}
			{#key backgroundKey}
				<BackgroundCanvas
					backgroundType={currentBackground}
					quality={currentQuality}
					onReady={() =>
						console.log(
							`🌌 Background ${currentBackground} ready with quality ${currentQuality}!`
						)}
				/>
			{/key}
		{/if}

		<!-- Control Panel -->
		<div class="control-panel">
			<div class="panel-header">
				<h2>🌌 Background Test Window</h2>
				<p>Test all the beautiful backgrounds and see them in action!</p>
			</div>

			<div class="controls">
				<!-- Background Type Selector -->
				<div class="control-group">
					<label for="background-select">Background Type:</label>
					<select
						id="background-select"
						bind:value={currentBackground}
						class="select-input"
					>
						{#each backgroundOptions as option}
							<option value={option.value}>{option.label}</option>
						{/each}
					</select>
					<p class="description">
						{currentBackgroundInfo?.description || 'No description available'}
					</p>
				</div>

				<!-- Quality Selector -->
				<div class="control-group">
					<label for="quality-select">Quality Level:</label>
					<select id="quality-select" bind:value={currentQuality} class="select-input">
						{#each qualityOptions as option}
							<option value={option.value}>{option.label}</option>
						{/each}
					</select>
					<p class="description">Higher quality shows more particles and effects</p>
				</div>

				<!-- Visibility Toggle -->
				<div class="control-group">
					<label class="checkbox-label">
						<input type="checkbox" bind:checked={isVisible} class="checkbox-input" />
						Show Background
					</label>
				</div>

				<!-- Current Status -->
				<div class="status-display">
					<h3>Current Settings:</h3>
					<div class="status-item">
						<strong>Background:</strong>
						{currentBackgroundInfo?.label || 'Unknown'}
					</div>
					<div class="status-item">
						<strong>Quality:</strong>
						{qualityOptions.find((q) => q.value === currentQuality)?.label}
					</div>
					<div class="status-item">
						<strong>Visible:</strong>
						{isVisible ? 'Yes' : 'No'}
					</div>
				</div>
			</div>
		</div>
	</BackgroundProvider>
</div>

<style>
	.test-window {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		overflow: hidden;
		background: #000;
		z-index: 1000;
	}

	.control-panel {
		position: absolute;
		top: 20px;
		right: 20px;
		width: 350px;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		padding: 20px;
		color: white;
		font-family: 'Segoe UI', sans-serif;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
		z-index: 10;
	}

	.panel-header {
		text-align: center;
		margin-bottom: 20px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
		padding-bottom: 15px;
	}

	.panel-header h2 {
		margin: 0 0 8px 0;
		font-size: 1.4rem;
		font-weight: 600;
	}

	.panel-header p {
		margin: 0;
		font-size: 0.9rem;
		opacity: 0.8;
	}

	.controls {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.control-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.control-group label {
		font-weight: 500;
		font-size: 0.9rem;
		color: rgba(255, 255, 255, 0.9);
	}

	.select-input {
		padding: 8px 12px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		font-size: 0.9rem;
		outline: none;
		transition: all 0.2s ease;
	}

	.select-input:focus {
		border-color: rgba(70, 130, 255, 0.8);
		background: rgba(255, 255, 255, 0.15);
	}

	.select-input option {
		background: #2a2a2a;
		color: white;
	}

	.description {
		font-size: 0.8rem;
		opacity: 0.7;
		margin: 0;
		font-style: italic;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 8px;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.checkbox-input {
		width: 16px;
		height: 16px;
		accent-color: rgba(70, 130, 255, 0.8);
	}

	.status-display {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 15px;
	}

	.status-display h3 {
		margin: 0 0 10px 0;
		font-size: 1rem;
		font-weight: 500;
	}

	.status-item {
		margin: 5px 0;
		font-size: 0.85rem;
	}

	.status-item strong {
		color: rgba(70, 130, 255, 0.9);
	}
</style>
