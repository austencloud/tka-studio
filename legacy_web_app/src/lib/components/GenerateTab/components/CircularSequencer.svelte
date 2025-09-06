<script lang="ts">
	// Import components and types
	import CAPPicker from './CAPPicker.svelte';
	import type { CAPType } from '$lib/state/machines/sequenceMachine/types';

	// Use Svelte 5 props rune
	const props = $props<{
		selectedCapType?: CAPType;
		onCapTypeChange?: (capType: CAPType) => void;
	}>();

	// Default values with derived values
	let selectedCapType = $state<CAPType>(props.selectedCapType ?? 'mirrored');

	// Sync with props
	$effect(() => {
		if (props.selectedCapType) {
			selectedCapType = props.selectedCapType;
		}
	});

	// Example CAP types (replace with your actual data)
	const capTypesData = [
		{ id: 'mirrored', label: 'Mirrored', description: 'Second half mirrors the first.' },
		{ id: 'rotated', label: 'Rotated', description: 'Second half rotates the first.' },
		{
			id: 'mirrored_complementary',
			label: 'Mirrored Complementary',
			description: 'Mirrored with complementary motion.'
		},
		// Add all your CAP types here
		{
			id: 'rotated_complementary',
			label: 'Rotated Complementary',
			description: 'Rotated with complementary motion.'
		},
		{
			id: 'mirrored_swapped',
			label: 'Mirrored Swapped',
			description: 'Mirrored with swapped prop colors.'
		},
		{
			id: 'rotated_swapped',
			label: 'Rotated Swapped',
			description: 'Rotated with swapped prop colors.'
		},
		{ id: 'strict_mirrored', label: 'Strict Mirrored', description: 'Strictly mirrored sequence.' },
		{ id: 'strict_rotated', label: 'Strict Rotated', description: 'Strictly rotated sequence.' }
	];

	function handleCapTypeSelect(capId: string) {
		// Validate that the selected type is a valid CAPType
		const isValidCapType = capTypesData.some((capType) => capType.id === capId);

		if (isValidCapType) {
			const newCapType = capId as CAPType;
			selectedCapType = newCapType;

			// Call the callback if provided
			if (props.onCapTypeChange) {
				props.onCapTypeChange(newCapType);
			}
		}
	}
</script>

<div class="circular-sequencer-controls">
	<h4 class="sequencer-title">Circular Options</h4>
	<div class="options-content">
		<CAPPicker
			capTypes={capTypesData}
			selectedCapId={selectedCapType}
			onSelect={handleCapTypeSelect}
		/>
	</div>
</div>

<style>
	.circular-sequencer-controls {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		height: 100%; /* Allow it to fill space in parent */
		min-height: 0; /* For flex child, ensures it doesn't overflow its container unnecessarily */
		background-color: var(
			--color-surface-700,
			rgba(30, 40, 60, 0.4)
		); /* Slightly different bg for distinction */
		padding: var(--spacing-md, 1rem);
		border-radius: var(--border-radius-md, 0.5rem);
	}
	.sequencer-title {
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		margin: 0 0 0.5rem 0;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
	}
	.options-content {
		flex-grow: 1; /* Allows CAPPicker to use available space */
		overflow-y: auto; /* Makes this area scrollable if CAPPicker is too tall */
		min-height: 0; /* Important for scroll within flex item */
		padding-right: 4px; /* Space for scrollbar, adjust if needed */

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
</style>
