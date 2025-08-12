<!-- ConstructTab.svelte - Refactored into smaller, manageable components -->
<script lang="ts">
	import ErrorBanner from '$components/construct/ErrorBanner.svelte';
	import LeftPanel from '$components/construct/LeftPanel.svelte';
	import LoadingOverlay from '$components/construct/LoadingOverlay.svelte';
	import RightPanel from '$components/construct/RightPanel.svelte';
	import { constructTabEventService } from '$services/implementations/ConstructTabEventService';
	import { constructTabState } from '$stores/constructTabState.svelte';
	import { onMount } from 'svelte';

	// Reactive state from store
	let errorMessage = $derived(constructTabState.errorMessage);
	let isTransitioning = $derived(constructTabState.isTransitioning);

	// Setup component coordination and reactive state updates on mount
	onMount(() => {
		console.log('🎭 ConstructTab mounted, setting up coordination');
		constructTabEventService.setupComponentCoordination();
	});

	// Handle reactive state updates for shouldShowStartPositionPicker
	$effect(() => {
		constructTabState.updateShouldShowStartPositionPicker();
	});
</script>

<div class="construct-tab" data-testid="construct-tab">
	<!-- Error display -->
	{#if errorMessage}
		<ErrorBanner message={errorMessage} />
	{/if}

	<!-- Main content area - Two panel layout like desktop app -->
	<div class="construct-content">
		<!-- Left Panel: Workbench (always visible) -->
		<LeftPanel />

		<!-- Right Panel: 4-Tab interface matching desktop -->
		<RightPanel />
	</div>

	<!-- Loading overlay -->
	{#if isTransitioning}
		<LoadingOverlay message="Processing..." />
	{/if}
</div>

<style>
	.construct-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		overflow: hidden;
		position: relative;
	}

	/* Main two-column layout: 50/50 split between left and right panels */
	.construct-content {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 1fr; /* 50/50 split between left panel and right panel */
		overflow: hidden;
		gap: var(--spacing-xs); /* Add small gap between content and button panel */

		padding: 8px;
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.construct-content {
			flex-direction: column;
		}
	}
</style>
