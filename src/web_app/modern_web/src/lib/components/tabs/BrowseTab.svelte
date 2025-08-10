<script lang="ts">
	import FilterSelectionPanel from './browse/FilterSelectionPanel.svelte';
	import SequenceBrowserPanel from './browse/SequenceBrowserPanel.svelte';
	import SequenceViewerPanel from './browse/SequenceViewerPanel.svelte';

	// Tab state management
	let currentPanelIndex = 0; // 0 = filter selection, 1 = sequence browser
	let selectedFilter: { type: string; value: any } | null = null;
	let selectedSequence: any | null = null;
	let isLoading = false;

	// Switch to sequence browser when filter is selected
	function handleFilterSelected(event: CustomEvent) {
		selectedFilter = event.detail;
		currentPanelIndex = 1;
		// TODO: Trigger sequence loading based on filter
	}

	// Handle sequence selection from browser
	function handleSequenceSelected(event: CustomEvent) {
		selectedSequence = event.detail;
		// TODO: Load sequence details for viewer panel
	}

	// Navigate back to filter selection
	function handleBackToFilters() {
		currentPanelIndex = 0;
		selectedFilter = null;
	}

	// Navigate back to sequence browser
	function handleBackToBrowser() {
		selectedSequence = null;
	}

	// Handle sequence actions (edit, save, delete, fullscreen)
	function handleSequenceAction(event: CustomEvent) {
		const { action, sequence } = event.detail;
		console.log(`Action: ${action} on sequence:`, sequence);
		// TODO: Implement actions
	}
</script>

<div class="browse-tab">
	<!-- Main horizontal layout (2:1 ratio) -->
	<div class="main-layout">
		<!-- Left side - Stacked panels (2/3 width) -->
		<div class="left-panel-stack">
			{#if currentPanelIndex === 0}
				<!-- Filter Selection Panel -->
				<div class="panel-container" data-panel="filter-selection">
					<FilterSelectionPanel on:filterSelected={handleFilterSelected} />
				</div>
			{:else if currentPanelIndex === 1}
				<!-- Sequence Browser Panel -->
				<div class="panel-container" data-panel="sequence-browser">
					<SequenceBrowserPanel
						filter={selectedFilter}
						{isLoading}
						on:sequenceSelected={handleSequenceSelected}
						on:backToFilters={handleBackToFilters}
					/>
				</div>
			{/if}
		</div>

		<!-- Right side - Sequence Viewer Panel (1/3 width) -->
		<div class="right-panel">
			<SequenceViewerPanel
				sequence={selectedSequence}
				on:backToBrowser={handleBackToBrowser}
				on:sequenceAction={handleSequenceAction}
			/>
		</div>
	</div>
</div>

<style>
	.browse-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		overflow: hidden;
		background: transparent;
	}

	.main-layout {
		display: flex;
		flex: 1;
		gap: 0;
		overflow: hidden;
	}

	.left-panel-stack {
		flex: 2;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		min-width: 0;
	}

	.right-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		min-width: 0;
		border-left: var(--glass-border);
	}

	.panel-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	/* Smooth panel transitions */
	.panel-container {
		animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	/* Responsive design */
	@media (max-width: 1024px) {
		.main-layout {
			flex-direction: column;
		}

		.left-panel-stack {
			flex: 1;
		}

		.right-panel {
			flex: 1;
			border-left: none;
			border-top: var(--glass-border);
		}
	}

	@media (max-width: 768px) {
		.main-layout {
			gap: 0;
		}
	}
</style>
