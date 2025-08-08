<script lang="ts">
	import { backgroundContainer } from '$lib/state/stores/background/BackgroundContainer';
	import type { BackgroundType, QualityLevel } from './types/types';

	// Use the background container state directly
	const background = $state(backgroundContainer.state);

	// Event handlers
	function handleBackgroundChange(event: Event) {
		const select = event.target as HTMLSelectElement;
		backgroundContainer.setBackground(select.value as BackgroundType);
	}

	function handleQualityChange(event: Event) {
		const select = event.target as HTMLSelectElement;
		backgroundContainer.setQuality(select.value as QualityLevel);
	}

	function handleToggleVisibility() {
		backgroundContainer.setVisible(!background.isVisible);
	}

	// Function to get a user-friendly display name for each background
	function getDisplayName(type: BackgroundType): string {
		switch (type) {
			case 'snowfall':
				return 'Snowfall';
			case 'nightSky':
				return 'Night Sky';
			case 'deepOcean':
				return 'Deep Ocean';
			default:
				return type;
		}
	}
</script>

<div class="background-settings">
	<h3>Background Settings</h3>

	<div class="settings-group">
		<label for="background-select">Background:</label>
		<select
			id="background-select"
			value={background.currentBackground}
			onchange={handleBackgroundChange}
		>
			{#each background.availableBackgrounds as bg}
				<option value={bg}>{getDisplayName(bg)}</option>
			{/each}
		</select>
	</div>

	<div class="settings-group">
		<label for="quality-select">Quality:</label>
		<select id="quality-select" value={background.quality} onchange={handleQualityChange}>
			<option value="low">Low</option>
			<option value="medium">Medium</option>
			<option value="high">High</option>
		</select>
	</div>

	<div class="settings-group">
		<label for="visibility-toggle">Visibility:</label>
		<button
			id="visibility-toggle"
			class="toggle-button"
			class:active={background.isVisible}
			onclick={handleToggleVisibility}
		>
			{background.isVisible ? 'Visible' : 'Hidden'}
		</button>
	</div>

	{#if background.performanceMetrics}
		<div class="performance-metrics">
			<h4>Performance</h4>
			<div class="metric">
				<span>FPS:</span>
				<span class="value">{background.performanceMetrics.fps.toFixed(1)}</span>
			</div>
			{#if background.performanceMetrics.renderTime}
				<div class="metric">
					<span>Render Time:</span>
					<span class="value">{background.performanceMetrics.renderTime.toFixed(2)} ms</span>
				</div>
			{/if}
		</div>
	{/if}

	{#if background.error}
		<div class="error-message">
			<p>Error: {background.error.message}</p>
		</div>
	{/if}
</div>

<style>
	.background-settings {
		background-color: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 1rem;
		border-radius: 0.5rem;
		width: 100%;
		max-width: 300px;
	}

	h3 {
		margin-top: 0;
		margin-bottom: 1rem;
		font-size: 1.2rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
		padding-bottom: 0.5rem;
	}

	.settings-group {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	label {
		font-size: 0.9rem;
		margin-right: 0.5rem;
	}

	select {
		background-color: #333;
		color: white;
		border: 1px solid #555;
		padding: 0.25rem 0.5rem;
		border-radius: 0.25rem;
		font-size: 0.9rem;
	}

	.toggle-button {
		background-color: #333;
		color: white;
		border: 1px solid #555;
		padding: 0.25rem 0.75rem;
		border-radius: 0.25rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.9rem;
	}

	.toggle-button.active {
		background-color: #4caf50;
		border-color: #4caf50;
	}

	.performance-metrics {
		margin-top: 1rem;
		padding-top: 0.5rem;
		border-top: 1px solid rgba(255, 255, 255, 0.2);
	}

	h4 {
		margin-top: 0;
		margin-bottom: 0.5rem;
		font-size: 1rem;
	}

	.metric {
		display: flex;
		justify-content: space-between;
		font-size: 0.9rem;
		margin-bottom: 0.25rem;
	}

	.value {
		font-weight: bold;
	}

	.error-message {
		margin-top: 1rem;
		padding: 0.5rem;
		background-color: rgba(255, 0, 0, 0.3);
		border-radius: 0.25rem;
		border-left: 3px solid red;
		font-size: 0.9rem;
	}

	.error-message p {
		margin: 0;
	}
</style>
