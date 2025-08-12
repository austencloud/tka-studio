<!-- SequenceCardTab.svelte - Clone of desktop modern sequence card tab -->
<script lang="ts">
	import { getIsLoading, getSequences } from '$lib/state/sequenceState.svelte';
	import type { SequenceData } from '$services/interfaces';
	import { onMount } from 'svelte';
	import SequenceCardContent from './sequence_card/SequenceCardContent.svelte';
	import SequenceCardHeader from './sequence_card/SequenceCardHeader.svelte';
	import SequenceCardNavigation from './sequence_card/SequenceCardNavigation.svelte';

	// State matching desktop app functionality
	let selectedLength = $state(16); // Default to 16 like desktop
	let columnCount = $state(2); // Default to 2 columns
	let isExporting = $state(false);
	let isRegenerating = $state(false);
	let progressValue = $state(0);
	let progressMessage = $state('Select a sequence length to view cards');
	let filteredSequences = $state<SequenceData[]>([]);

	// Reactive sequences from store
	let allSequences = $derived(getSequences());
	let isLoading = $derived(getIsLoading());

	// Filter sequences based on selected length
	$effect(() => {
		if (selectedLength === 0) {
			// "All" selected
			filteredSequences = allSequences;
		} else {
			filteredSequences = allSequences.filter((seq) => seq.beats?.length === selectedLength);
		}
	});

	// Update progress message based on filtered sequences
	$effect(() => {
		if (isLoading) {
			progressMessage = 'Loading sequences...';
		} else if (isExporting) {
			progressMessage = `Exporting... ${progressValue}%`;
		} else if (isRegenerating) {
			progressMessage = `Regenerating images... ${progressValue}%`;
		} else if (filteredSequences.length === 0) {
			progressMessage =
				selectedLength === 0
					? 'No sequences available'
					: `No sequences found with ${selectedLength} beats`;
		} else {
			progressMessage = `Displaying ${filteredSequences.length} sequence${filteredSequences.length === 1 ? '' : 's'}`;
		}
	});

	// Handle length selection from navigation
	function handleLengthSelected(event: CustomEvent<number>) {
		selectedLength = event.detail;
		console.log('Length selected:', selectedLength);
	}

	// Handle column count change from navigation
	function handleColumnCountChanged(event: CustomEvent<number>) {
		columnCount = event.detail;
		console.log('Column count changed:', columnCount);
	}

	// Handle export all request from header
	async function handleExportAll() {
		try {
			isExporting = true;
			progressValue = 0;

			// Simulate export progress
			for (let i = 0; i <= 100; i += 10) {
				progressValue = i;
				await new Promise((resolve) => setTimeout(resolve, 200));
			}

			// TODO: Implement actual export functionality
			console.log('Exporting all sequence cards...');
			alert(
				'Export completed! (This is a demo - actual export functionality will be implemented)'
			);
		} catch (error) {
			console.error('Export failed:', error);
			alert('Export failed. Please try again.');
		} finally {
			isExporting = false;
			progressValue = 0;
		}
	}

	// Handle refresh request from header
	function handleRefresh() {
		console.log('Refreshing sequence cards...');
		// TODO: Implement refresh functionality
		// This might involve reloading sequences or regenerating cache
	}

	// Handle regenerate images request from header
	async function handleRegenerateImages() {
		try {
			isRegenerating = true;
			progressValue = 0;

			// Simulate regeneration progress
			for (let i = 0; i <= 100; i += 5) {
				progressValue = i;
				await new Promise((resolve) => setTimeout(resolve, 100));
			}

			// TODO: Implement actual image regeneration
			console.log('Regenerating all images...');
			alert('Image regeneration completed! (This is a demo)');
		} catch (error) {
			console.error('Image regeneration failed:', error);
			alert('Image regeneration failed. Please try again.');
		} finally {
			isRegenerating = false;
			progressValue = 0;
		}
	}

	onMount(() => {
		console.log('🎴 SequenceCardTab mounted');
	});
</script>

<div class="sequence-card-tab" data-testid="sequence-card-tab">
	<!-- Header Component -->
	<div class="header-section">
		<SequenceCardHeader
			{isExporting}
			{isRegenerating}
			{progressValue}
			{progressMessage}
			showProgress={isLoading || isExporting || isRegenerating}
			on:exportAll={handleExportAll}
			on:refresh={handleRefresh}
			on:regenerateImages={handleRegenerateImages}
		/>
	</div>

	<!-- Main Content Area -->
	<div class="main-content">
		<!-- Navigation Sidebar -->
		<div class="navigation-section">
			<SequenceCardNavigation
				{selectedLength}
				{columnCount}
				on:lengthSelected={handleLengthSelected}
				on:columnCountChanged={handleColumnCountChanged}
			/>
		</div>

		<!-- Content Display Area -->
		<div class="content-section">
			<SequenceCardContent
				sequences={filteredSequences}
				{columnCount}
				{isLoading}
				{selectedLength}
			/>
		</div>
	</div>
</div>

<style>
	.sequence-card-tab {
	display: flex;
	flex-direction: column;
	height: 100%;
	width: 100%;
	background: transparent;
	overflow: hidden;
}

	.header-section {
	flex-shrink: 0;
	padding: var(--spacing-lg);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	box-shadow: var(--shadow-glass);
}

	.main-content {
		flex: 1;
		display: flex;
		gap: var(--spacing-lg);
		padding: var(--spacing-lg);
		overflow: hidden;
	}

	.navigation-section {
		flex-shrink: 0;
		width: 280px;
		display: flex;
		flex-direction: column;
	}

	.content-section {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
	}

	/* Responsive Design */
	@media (max-width: 1024px) {
		.main-content {
			flex-direction: column;
		}

		.navigation-section {
			width: auto;
			order: 2;
		}

		.content-section {
			order: 1;
			flex: 0 0 60%;
		}
	}

	@media (max-width: 768px) {
		.header-section {
			padding: var(--spacing-md);
		}

		.main-content {
			padding: var(--spacing-md);
			gap: var(--spacing-md);
		}

		.navigation-section {
			order: 1;
		}

		.content-section {
			order: 2;
			flex: 1;
		}
	}
</style>
