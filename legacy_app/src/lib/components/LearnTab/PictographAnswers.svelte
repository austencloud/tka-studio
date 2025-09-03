<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
	import type { PictographData } from '$lib/types/PictographData';
	import { PictographService } from '$lib/components/Pictograph/PictographService';

	export let pictographs: PictographData[] = [];
	export let disabled: boolean = false;

	const dispatch = createEventDispatcher();

	// Create an array of unique IDs for each pictograph
	let pictographIds: string[] = [];

	// Generate a new set of IDs whenever pictographs array changes
	$: if (Array.isArray(pictographs)) {
		pictographIds = pictographs.map(() => crypto.randomUUID());
	}

	// Process the pictograph data to ensure it has all required properties
	function processData(data: PictographData): PictographData {
		if (!data) return defaultPictographData;

		// Make a deep copy to avoid modifying the original data
		const processingData = JSON.parse(JSON.stringify(data));

		// Add a unique ID to ensure components remount
		processingData.id = crypto.randomUUID();

		// Ensure grid is set if gridMode is present
		if (processingData.gridMode && !processingData.grid) {
			processingData.grid = processingData.gridMode;
		}

		// Initialize service to generate missing components if needed
		try {
			// Create a service instance to initialize the motion objects
			new PictographService(processingData);
			return processingData;
		} catch (err) {
			console.error('Error processing pictograph data:', err);
			return processingData;
		}
	}

	// Process pictographs for direct use
	$: processedPictographs = Array.isArray(pictographs)
		? pictographs.map((p) => (p ? processData(p) : defaultPictographData))
		: [];

	// We'll use the processed pictographs directly instead of creating stores
	// This ensures proper initialization of motion objects in the Pictograph component

	function handleSelect(pictograph: PictographData) {
		if (!disabled) {
			dispatch('select', pictograph);
		}
	}
</script>

<div class="pictograph-answers">
	{#if Array.isArray(processedPictographs) && processedPictographs.length > 0}
		{#each processedPictographs as processedPictograph, i}
			{#key pictographIds[i]}
				<button
					class="pictograph-button"
					on:click={() => handleSelect(pictographs[i])}
					{disabled}
					aria-label="Pictograph answer option"
				>
					<div class="pictograph-container">
						<Pictograph pictographData={processedPictograph} showLoadingIndicator={false} />
					</div>
				</button>
			{/key}
		{/each}
	{:else}
		<div class="no-options">No options available</div>
	{/if}
</div>

<style>
	.pictograph-answers {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
		margin: 1rem auto 0;
		width: 100%;
		max-width: 960px;
		justify-content: center;
		justify-items: center;
		box-sizing: border-box;
		padding-left: 16px;
		padding-right: 16px;
		position: relative;
		left: 50%;
		transform: translateX(-50%);
	}

	.pictograph-container {
		width: 100%;
		aspect-ratio: 1/1;
		min-width: 120px;
		max-width: min(220px, 22vw);
	}

	.pictograph-button {
		padding: 0.5rem;
		border-radius: 8px;
		border: 2px solid transparent;
		background-color: var(--color-surface-700, #2d2d2d);
		cursor: pointer;
		transition:
			transform 0.15s,
			border-color 0.15s,
			box-shadow 0.2s ease;
		width: 100%;
		height: 100%;
	}

	.pictograph-button:hover:not(:disabled) {
		border-color: var(--color-primary, #3e63dd);
		transform: translateY(-3px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.pictograph-button:active:not(:disabled) {
		transform: translateY(0);
	}

	.pictograph-button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	.no-options {
		padding: 2rem;
		background-color: rgba(0, 0, 0, 0.1);
		border-radius: 8px;
		color: var(--text-color-secondary, #aaa);
		grid-column: span 4;
	}

	/* Tablet layout - 2×2 grid */
	@media (max-width: 900px) {
		.pictograph-answers {
			grid-template-columns: repeat(2, 1fr);
			gap: 1.5rem;
			max-width: 600px;
		}

		.pictograph-container {
			max-width: 45vw;
		}

		.no-options {
			grid-column: span 2;
		}
	}

	/* Mobile phone in portrait mode */
	@media (max-width: 480px) {
		.pictograph-answers {
			grid-template-columns: repeat(2, 1fr);
			gap: 0.75rem;
			max-width: 400px;
		}

		.pictograph-container {
			min-width: 100px;
		}
	}
</style>
