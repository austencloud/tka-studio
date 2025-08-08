<script lang="ts">
	import { slide } from 'svelte/transition';

	// Props
	let {
		currentBeat = 0,
		totalBeats = 0,
		showAdvanced = false
	}: {
		currentBeat?: number;
		totalBeats?: number;
		showAdvanced?: boolean;
	} = $props();

	// State for advanced toggle
	let showAdvancedInfo = $state(showAdvanced);

	// Advanced technical details aligned with new timing system
	const tValue = $derived(currentBeat === 0 ? 0 : currentBeat - Math.floor(currentBeat));

	const currentStepIndex = $derived(
		currentBeat === 0
			? 'Start Position'
			: currentBeat >= totalBeats
				? `Step ${totalBeats} (End)`
				: `Step ${Math.floor(currentBeat)}`
	);
</script>

<div class="advanced-section">
	<button
		type="button"
		class="advanced-toggle"
		onclick={() => (showAdvancedInfo = !showAdvancedInfo)}
		aria-expanded={showAdvancedInfo}
		title="Show technical details"
	>
		<span>Technical Details</span>
		<span class="toggle-icon" class:rotated={showAdvancedInfo}>▼</span>
	</button>

	{#if showAdvancedInfo}
		<div class="advanced-content" transition:slide>
			<div class="info-item">
				<span class="label">Current Beat:</span>
				<span class="value">{currentBeat.toFixed(2)}</span>
			</div>
			<div class="info-item">
				<span class="label">Step Index:</span>
				<span class="value">{currentStepIndex}</span>
			</div>
			<div class="info-item">
				<span class="label">T-Value:</span>
				<span class="value">{tValue.toFixed(3)}</span>
			</div>
			<div class="info-item">
				<span class="label">Total Beats:</span>
				<span class="value">{totalBeats}</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.advanced-section {
		border-top: 1px solid var(--color-border);
		padding-top: 1rem;
	}

	.advanced-toggle {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		background: var(--color-background);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		cursor: pointer;
		font-weight: 600;
		color: var(--color-text-secondary);
		transition: all 0.2s ease;
	}

	.advanced-toggle:hover {
		background: var(--color-surface-hover);
		color: var(--color-text-primary);
		border-color: var(--color-primary);
	}

	.toggle-icon {
		transition: transform 0.2s ease;
		font-size: 0.8rem;
	}

	.toggle-icon.rotated {
		transform: rotate(180deg);
	}

	.advanced-content {
		margin-top: 1rem;
		padding: 1rem;
		background: var(--color-background);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.info-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem 0;
		border-bottom: 1px solid var(--color-border);
	}

	.info-item:last-child {
		border-bottom: none;
	}

	.label {
		font-weight: 500;
		color: var(--color-text-secondary);
		font-size: 0.9rem;
	}

	.value {
		font-family:
			'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
		font-weight: 600;
		color: var(--color-text-primary);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-size: 0.85rem;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.advanced-toggle {
			padding: 0.75rem;
			font-size: 0.9rem;
		}

		.info-item {
			font-size: 0.85rem;
			flex-direction: column;
			align-items: flex-start;
			gap: 0.5rem;
		}

		.value {
			align-self: flex-end;
		}
	}

	@media (max-width: 480px) {
		.advanced-content {
			gap: 0.75rem;
		}
	}
</style>
