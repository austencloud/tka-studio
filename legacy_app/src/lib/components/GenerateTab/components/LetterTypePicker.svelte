<!-- src/lib/components/GenerateTab/Freeform/LetterTypePicker/LetterTypePicker.svelte -->
<script lang="ts">
	// Props
	export let options: {
		id: string;
		label: string;
		description: string;
	}[];
	export let selectedTypes: string[] = [];

	// Events
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher<{
		select: string[];
	}>();

	// Toggle selection of a letter type
	function toggleSelection(typeId: string) {
		if (selectedTypes.includes(typeId)) {
			selectedTypes = selectedTypes.filter((id) => id !== typeId);
		} else {
			selectedTypes = [...selectedTypes, typeId];
		}

		dispatch('select', selectedTypes);
	}
</script>

<div class="letter-type-picker">
	<h4>Letter Type Selection</h4>

	<div class="letter-types-grid">
		{#each options as option}
			<button
				class="letter-type-button"
				class:selected={selectedTypes.includes(option.id)}
				on:click={() => toggleSelection(option.id)}
			>
				<div class="letter-type-content">
					<span class="letter-type-label">{option.label}</span>
					<span class="letter-type-description">{option.description}</span>
				</div>
			</button>
		{/each}
	</div>

	<div class="selection-info">
		{#if selectedTypes.length === 0}
			<p class="info-text">No letter types selected. All types will be used.</p>
		{:else}
			<p class="info-text">Selected types: {selectedTypes.length}</p>
		{/if}
	</div>
</div>

<style>
	.letter-type-picker {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		width: 100%;
	}

	h4 {
		font-size: 1.1rem;
		margin: 0;
		color: var(--color-text-primary, white);
		font-weight: 500;
	}

	.letter-types-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: 0.75rem;
	}

	.letter-type-button {
		background: var(--color-surface-alt, rgba(40, 50, 70, 0.85));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 0.5rem;
		padding: 0.75rem;
		cursor: pointer;
		transition: all 0.2s ease;
		text-align: left;
		color: var(--color-text-primary, white);
	}

	.letter-type-button:hover {
		background: var(--color-surface-hover, rgba(50, 60, 80, 0.85));
		border-color: var(--color-border-hover, rgba(255, 255, 255, 0.2));
	}

	.letter-type-button.selected {
		background: var(--color-primary-container, rgba(100, 150, 255, 0.2));
		border-color: var(--color-primary, rgba(100, 150, 255, 0.8));
	}

	.letter-type-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.letter-type-label {
		font-weight: 500;
		font-size: 1rem;
	}

	.letter-type-description {
		font-size: 0.85rem;
		opacity: 0.8;
	}

	.selection-info {
		margin-top: 0.5rem;
	}

	.info-text {
		font-size: 0.9rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		margin: 0;
	}

	@media (max-width: 768px) {
		.letter-types-grid {
			grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		}
	}
</style>
