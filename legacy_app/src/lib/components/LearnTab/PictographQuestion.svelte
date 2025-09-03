<script lang="ts">
	// No longer need writable with Svelte 5 approach
	import Pictograph from '$lib/components/Pictograph/Pictograph.svelte';
	import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
	import type { PictographData } from '$lib/types/PictographData';
	import { PictographService } from '$lib/components/Pictograph/PictographService';

	export let pictograph: PictographData | null = null;

	// Track a unique ID for the pictograph that changes with each new pictograph
	let pictographId = crypto.randomUUID();

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
			const service = new PictographService(processingData);
			return processingData;
		} catch (err) {
			console.error('Error processing pictograph data:', err);
			return processingData;
		}
	}

	// Process pictograph data when it changes
	$: processedPictographData = pictograph ? processData(pictograph) : defaultPictographData;

	// Update the ID when pictograph changes
	$: if (pictograph) {
		pictographId = crypto.randomUUID(); // Generate new ID when pictograph changes
	} else {
		pictographId = crypto.randomUUID(); // Generate new ID for default data too
	}
</script>

<div class="pictograph-question">
	{#if pictograph}
		{#key pictographId}
			<div class="pictograph-container">
				<Pictograph pictographData={processedPictographData} showLoadingIndicator={false} />
			</div>
		{/key}
	{:else}
		<div class="placeholder">No pictograph data</div>
	{/if}
</div>

<style>
	.pictograph-question {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		padding: 1rem;
	}

	.pictograph-container {
		width: 300px;
		height: 300px;
		max-width: 90vw;
		max-height: 90vw;
	}

	.placeholder {
		border: 2px dashed #555;
		border-radius: 8px;
		padding: 2rem;
		color: #777;
		background-color: rgba(0, 0, 0, 0.1);
	}
</style>
