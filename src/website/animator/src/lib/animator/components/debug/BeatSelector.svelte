<script lang="ts">
	import type { BeatDebugInfo } from '../../types/debug.js';

	// Props
	let {
		debugHistory = [],
		selectedBeat = null,
		selectedProp = null,
		onBeatSelect = () => {},
		onPropSelect = () => {}
	}: {
		debugHistory?: BeatDebugInfo[];
		selectedBeat?: number | null;
		selectedProp?: 'blue' | 'red' | null;
		onBeatSelect?: (_beatNumber: number) => void;
		onPropSelect?: (_prop: 'blue' | 'red') => void;
	} = $props();

	function handleBeatChange(event: Event): void {
		const target = event.target as HTMLSelectElement;
		const value = target.value === 'null' ? null : parseInt(target.value);
		if (value !== null) {
			onBeatSelect(value);
		}
	}

	function handlePropClick(prop: 'blue' | 'red'): void {
		onPropSelect(prop);
	}
</script>

<div class="selection-section">
	<div class="beat-selector">
		<label for="beat-select">Select Beat:</label>
		<select id="beat-select" value={selectedBeat} onchange={handleBeatChange}>
			<option value={null}>Choose a beat...</option>
			{#each debugHistory as beat}
				<option value={beat.beatNumber}>Beat {beat.beatNumber}</option>
			{/each}
		</select>
	</div>

	{#if selectedBeat !== null}
		<fieldset class="prop-selector">
			<legend>Select Prop:</legend>
			<div class="prop-buttons">
				<button
					class="prop-button blue"
					class:active={selectedProp === 'blue'}
					onclick={() => handlePropClick('blue')}
				>
					🔵 Blue Prop
				</button>
				<button
					class="prop-button red"
					class:active={selectedProp === 'red'}
					onclick={() => handlePropClick('red')}
				>
					🔴 Red Prop
				</button>
			</div>
		</fieldset>
	{/if}
</div>

<style>
	.selection-section {
		display: flex;
		gap: 1rem;
		align-items: center;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border-radius: 8px;
		border: 1px solid var(--color-border);
	}

	.beat-selector,
	.prop-selector {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.beat-selector label,
	.prop-selector legend {
		font-weight: 600;
		color: var(--color-text);
		white-space: nowrap;
	}

	.beat-selector select {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		padding: 0.5rem;
		color: var(--color-text);
		min-width: 150px;
	}

	.prop-selector {
		border: none;
		padding: 0;
		margin: 0;
	}

	.prop-selector legend {
		padding: 0;
		margin-bottom: 0.5rem;
	}

	.prop-buttons {
		display: flex;
		gap: 0.5rem;
	}

	.prop-button {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 0.5rem 1rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
	}

	.prop-button:hover {
		background: var(--color-surface-hover);
	}

	.prop-button.active {
		background: var(--color-primary);
		color: white;
		border-color: var(--color-primary);
	}

	.prop-button.blue.active {
		background: #3b82f6;
		border-color: #3b82f6;
	}

	.prop-button.red.active {
		background: #ef4444;
		border-color: #ef4444;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.selection-section {
			flex-direction: column;
			align-items: stretch;
			gap: 1rem;
		}
	}
</style>
