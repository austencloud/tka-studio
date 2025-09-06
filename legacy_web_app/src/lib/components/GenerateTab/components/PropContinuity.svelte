<!-- src/lib/components/GenerateTab/ui/PropContinuity.svelte -->
<script lang="ts">
	import { settingsStore } from '../store/settings';

	// Export the value property for binding
	export let value: 'continuous' | 'random' = 'continuous';

	// Options
	const continuityOptions = [
		{ id: 'continuous', label: 'Continuous' },
		{ id: 'random', label: 'Random' }
	];

	// Toggle between options
	function toggleContinuity() {
		const newValue = value === 'continuous' ? 'random' : 'continuous';
		value = newValue;
		settingsStore.setPropContinuity(newValue);
	}

	// Get current option
	$: currentOption = continuityOptions.find((opt) => opt.id === value) || continuityOptions[0];
</script>

<div class="prop-continuity">
	<label for="prop-continuity-toggle">Prop Continuity</label>

	<div class="toggle-control">
		<button
			id="prop-continuity-toggle"
			type="button"
			class="toggle-track"
			on:click={toggleContinuity}
			aria-label="Toggle Prop Continuity"
		>
			<div class="toggle-labels">
				{#each continuityOptions as option}
					<span class="toggle-label" class:selected={option.id === value}>
						{option.label}
					</span>
				{/each}
			</div>
			<div class="toggle-thumb" class:right={value === 'random'}></div>
		</button>
	</div>

	<div class="description">
		{#if value === 'continuous'}
			<p>Props will maintain rotation direction when possible.</p>
		{:else}
			<p>Props may randomly change rotation direction.</p>
		{/if}
	</div>
</div>

<style>
	.prop-continuity {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.toggle-control {
		display: flex;
		align-items: center;
	}

	.toggle-track {
		position: relative;
		width: 10rem;
		height: 2rem;
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 1rem;
		cursor: pointer;
		transition: background-color 0.2s ease;
		overflow: hidden;
	}

	.toggle-labels {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: space-between;
		z-index: 1;
	}

	.toggle-label {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		font-size: 0.75rem;
		font-weight: 500;
		transition: color 0.2s ease;
	}

	.toggle-label.selected {
		color: var(--color-text-primary, white);
	}

	.toggle-thumb {
		position: absolute;
		top: 0.125rem;
		left: 0.125rem;
		width: calc(50% - 0.25rem);
		height: calc(100% - 0.25rem);
		background: var(--color-accent, #3a7bd5);
		border-radius: 0.875rem;
		transition: transform 0.2s ease;
		z-index: 0;
	}

	.toggle-thumb.right {
		transform: translateX(calc(100% + 0.25rem));
	}

	.description {
		font-size: 0.75rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.6));
		opacity: 0.8;
	}

	.description p {
		margin: 0;
	}
</style>
