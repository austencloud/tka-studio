<script lang="ts">
	// Assume LetterTypePicker is available
	import LetterTypePicker from './LetterTypePicker.svelte'; // Refactored version below

	// Example letter type options (replace with your actual data)
	const letterTypeOptionsData = [
		{ id: 'type1', label: 'Type 1', description: 'Basic motions, simple transitions.' },
		{ id: 'type2', label: 'Type 2', description: 'Intermediate flow, common patterns.' },
		{ id: 'type3', label: 'Type 3', description: 'Advanced patterns, complex movements.' },
		{ id: 'type4', label: 'Type 4', description: 'Expert sequences, intricate combinations.' },
        { id: 'alpha', label: 'Alpha Series', description: 'Focus on Alpha-based movements.' },
        { id: 'beta', label: 'Beta Series', description: 'Focus on Beta-based movements.' },
		{ id: 'gamma', label: 'Gamma Series', description: 'Focus on Gamma-based movements.' },
	];

	let selectedLetterTypes = $state<string[]>([]);

	// This function is primarily for the on:select event from LetterTypePicker
	// If binding selectedTypes directly, this specific handler might not be needed
	// unless additional logic is required on selection change.
	function handleLetterTypesChange(event: CustomEvent<string[]>) {
		// selectedLetterTypes is already updated by bind:selectedTypes
		// console.log('Selected letter types in FreeformSequencer:', selectedLetterTypes);
	}
</script>

<div class="freeform-sequencer-controls">
	<h4 class="sequencer-title">Freeform Options</h4>
	<div class="options-content">
		<LetterTypePicker
			options={letterTypeOptionsData}
			bind:selectedTypes={selectedLetterTypes}
			on:select={handleLetterTypesChange}
		/>
		<div class="info-panel">
			Selected Types: {selectedLetterTypes.length > 0 ? selectedLetterTypes.map(id => letterTypeOptionsData.find(opt => opt.id === id)?.label || id).join(', ') : 'All (Default)'}
		</div>
	</div>
</div>

<style>
	.freeform-sequencer-controls {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		height: 100%;
		min-height: 0; /* For flex child */
		background-color: var(--color-surface-700, rgba(30,40,60,0.4)); /* Slightly different bg for distinction */
		padding: var(--spacing-md, 1rem);
		border-radius: var(--border-radius-md, 0.5rem);
	}
	.sequencer-title {
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		margin: 0 0 0.5rem 0;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid var(--color-border, rgba(255,255,255,0.1));
	}
	.options-content {
		flex-grow: 1; /* Allows LetterTypePicker to use available space */
		overflow-y: auto; /* Makes this area scrollable if LetterTypePicker is too tall */
		min-height: 0; /* Important for scroll within flex item */
		padding-right: 4px; /* Space for scrollbar */

		/* Minimalist Scrollbar */
		scrollbar-width: thin;
		scrollbar-color: var(--color-accent, #3a7bd5) transparent;
	}
	.options-content::-webkit-scrollbar {
		width: 6px;
	}
	.options-content::-webkit-scrollbar-track {
		background: transparent;
	}
	.options-content::-webkit-scrollbar-thumb {
		background-color: var(--color-accent, #3a7bd5);
		border-radius: 3px;
	}
	.info-panel {
		margin-top: 1rem;
		padding: 0.75rem; /* Slightly more padding */
		background-color: var(--color-surface-800, rgba(20,30,50,0.6)); /* Darker info panel */
		border-radius: calc(var(--border-radius-md, 0.5rem) - 0.125rem);
		font-size: 0.8rem;
		color: var(--color-text-secondary, rgba(255,255,255,0.7));
		border: 1px solid var(--color-border, rgba(255,255,255,0.05));
	}
</style>
