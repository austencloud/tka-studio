<!-- src/lib/components/GenerateTab/ui/TurnIntensity.svelte -->
<script lang="ts">
	import { settingsStore } from '../store/settings';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Export the value property for binding
	export let value: number = 3;

	// Constants
	const MIN_INTENSITY = 1;
	const MAX_INTENSITY = 5;

	// Labels for the intensity levels
	const intensityLabels = ['Minimal', 'Light', 'Moderate', 'Heavy', 'Extreme'];

	// Get current label
	$: currentLabel = intensityLabels[value - 1] || 'Moderate';

	// Update intensity
	function setIntensity(level: number) {
		if (level >= MIN_INTENSITY && level <= MAX_INTENSITY) {
			// Only trigger haptic feedback if the value is changing
			if (value !== level && browser) {
				// Use different feedback based on intensity level
				if (level > 3) {
					hapticFeedbackService.trigger('warning');
				} else {
					hapticFeedbackService.trigger('selection');
				}
			}

			value = level;
			settingsStore.setTurnIntensity(level);
		}
	}
</script>

<div class="turn-intensity">
	<div class="header">
		<label for="turn-intensity">Turn Intensity</label>
		<span class="current-level">{currentLabel}</span>
	</div>

	<div id="turn-intensity" class="intensity-buttons">
		{#each Array(MAX_INTENSITY) as _, i}
			{@const level = i + 1}
			<button
				class="intensity-button"
				class:active={value === level}
				on:click={() => setIntensity(level)}
				aria-label="Set turn intensity to {intensityLabels[i]}"
				aria-pressed={value === level}
			>
				<div class="button-content">
					<div class="level-indicator">
						{#each Array(level) as _}
							<div class="indicator-dot"></div>
						{/each}
					</div>
					<span class="level-number">{level}</span>
				</div>
			</button>
		{/each}
	</div>
</div>

<style>
	.turn-intensity {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.current-level {
		font-size: 0.875rem;
		color: var(--color-text-primary, white);
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
		padding: 0.125rem 0.5rem;
		border-radius: 1rem;
	}

	.intensity-buttons {
		display: flex;
		gap: 0.5rem;
		justify-content: space-between;
	}

	.intensity-button {
		flex: 1;
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 0.25rem;
		padding: 0.5rem;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.intensity-button:hover {
		background: var(--color-surface-hover, rgba(255, 255, 255, 0.1));
	}

	.intensity-button.active {
		background: var(--color-accent, #3a7bd5);
		border-color: var(--color-accent, #3a7bd5);
	}

	.button-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.25rem;
	}

	.level-indicator {
		display: flex;
		gap: 0.25rem;
	}

	.indicator-dot {
		width: 0.25rem;
		height: 0.25rem;
		border-radius: 50%;
		background-color: var(--color-text-primary, white);
	}

	.level-number {
		font-size: 0.75rem;
		color: var(--color-text-primary, white);
	}
</style>
