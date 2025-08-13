<!--
Enhanced Browse Tab with Unified Panel Management

Integrates panel management service with runes for:
- Unified collapse/expand logic for both panels
- Splitter-based resizing
- Persistent panel state
- Reactive UI updates
-->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import { NavigationMode } from '$lib/domain/browse';
	import { resolve } from '$lib/services/bootstrap';
	import type {
		IBrowseService,
		IDeleteService,
		IFavoritesService,
		IFilterPersistenceService,
		INavigationService,
		IPanelManagementService,
		ISectionService,
		ISequenceIndexService,
		IThumbnailService,
	} from '$lib/services/interfaces';
	import { createBrowseState } from '$lib/state/browse-state.svelte';
	import { createPanelState, BROWSE_TAB_PANEL_CONFIGS } from '$lib/state/panel-state.svelte';
	import { onMount, onDestroy } from 'svelte';

	// Enhanced components
	import BrowseLayoutEnhanced from './browse/BrowseLayout.svelte';
	import NavigationSidebar from './browse/NavigationSidebar.svelte';
	import AnimationPanel from './browse/AnimationPanel.svelte';

	// Existing components
	import DeleteConfirmationDialog from './browse/DeleteConfirmationDialog.svelte';
	import ErrorBanner from './browse/ErrorBanner.svelte';
	import FilterSelectionPanel from './browse/FilterSelectionPanel.svelte';
	import FullscreenSequenceViewer from './browse/FullscreenSequenceViewer.svelte';
	import LoadingOverlay from './browse/LoadingOverlay.svelte';
	import PanelContainer from './browse/PanelContainer.svelte';
	import SequenceBrowserPanel from './browse/sequence-browser/SequenceBrowserPanel.svelte';

	// Event handlers
	import { createBrowseEventHandlers } from './browse/browse-event-handlers';
	import { createNavigationEventHandlers } from './browse/navigation-event-handlers';

	// ✅ RESOLVE SERVICES: Get services from DI container
	const browseService = resolve('IBrowseService') as IBrowseService;
	const thumbnailService = resolve('IThumbnailService') as IThumbnailService;
	const sequenceIndexService = resolve('ISequenceIndexService') as ISequenceIndexService;
	const favoritesService = resolve('IFavoritesService') as IFavoritesService;
	const navigationService = resolve('INavigationService') as INavigationService;
	const filterPersistenceService = resolve('IFilterPersistenceService') as IFilterPersistenceService;
	const sectionService = resolve('ISectionService') as ISectionService;
	const deleteService = resolve('IDeleteService') as IDeleteService;
	const panelManagementService = resolve('IPanelManagementService') as IPanelManagementService;

	// ✅ REGISTER PANELS: Configure panel management
	onMount(() => {
		panelManagementService.registerPanel(BROWSE_TAB_PANEL_CONFIGS.navigation);
		panelManagementService.registerPanel(BROWSE_TAB_PANEL_CONFIGS.animation);
	});

	// ✅ CREATE STATE MANAGERS: Runes-based reactive state
	const browseState = createBrowseState(
		browseService,
		thumbnailService,
		sequenceIndexService,
		favoritesService,
		navigationService,
		filterPersistenceService,
		sectionService,
		deleteService
	);

	const panelState = createPanelState(panelManagementService);

	// ✅ PURE RUNES: Local UI state
	let currentPanelIndex = $state(0); // 0 = filter selection, 1 = sequence browser
	let showFullscreenViewer = $state(false); // Fullscreen sequence viewer state
	let fullscreenSequence = $state<BrowseSequenceMetadata | undefined>(undefined); // Current sequence for fullscreen
	let animationSequence = $state<BrowseSequenceMetadata | null>(null); // Current sequence for animation

	// ✅ DERIVED RUNES: Computed UI state from browse state
	let selectedFilter = $derived(browseState.currentFilter);
	let isLoading = $derived(browseState.isLoading);
	let hasError = $derived(browseState.hasError);
	let sequences = $derived(browseState.displayedSequences);
	let navigationMode = $derived(browseState.navigationMode);
	let navigationSections = $derived(browseState.navigationSections);
	let deleteConfirmation = $derived(browseState.deleteConfirmation);
	let showDeleteDialog = $derived(browseState.showDeleteDialog);

	// ✅ EFFECT: Sync navigation mode with panel index
	$effect(() => {
		if (navigationMode === NavigationMode.FILTER_SELECTION) {
			currentPanelIndex = 0;
		} else if (navigationMode === NavigationMode.SEQUENCE_BROWSER) {
			currentPanelIndex = 1;
		}
	});

	// Load initial data when component mounts
	onMount(async () => {
		try {
			await browseState.loadAllSequences();
		} catch (error) {
			console.error('❌ Failed to load browse data:', error);
		}
	});

	// Cleanup on destroy
	onDestroy(() => {
		panelState.cleanup();
	});

	// ✅ EVENT HANDLERS: Create event handlers using extracted functions
	const browseEventHandlers = createBrowseEventHandlers(browseState, (index) => {
		currentPanelIndex = index;
	});

	const navigationEventHandlers = createNavigationEventHandlers(
		browseState,
		(index) => {
			currentPanelIndex = index;
		},
		() => {
			panelState.toggleNavigationCollapse();
		}
	);

	// Destructure handlers for easier use
	const {
		handleFilterSelected,
		handleBackToFilters,
		handleSequenceAction: originalHandleSequenceAction,
		handleConfirmDelete,
		handleCancelDelete,
		handleClearError,
	} = browseEventHandlers;

	const {
		handleNavigationSectionToggle,
		handleNavigationItemClick,
		handleToggleNavigationCollapse,
	} = navigationEventHandlers;

	// ✅ FULLSCREEN HANDLERS
	function handleCloseFullscreen() {
		showFullscreenViewer = false;
		fullscreenSequence = undefined;
	}

	// ✅ SEQUENCE ACTION HANDLER: Enhanced with animation panel integration
	function handleSequenceAction(action: string, sequence: BrowseSequenceMetadata) {
		if (action === 'animate') {
			// Show animation panel and set sequence
			animationSequence = sequence;
			panelState.setAnimationVisible(true);
			// Expand panel if it's collapsed
			if (panelState.isAnimationCollapsed) {
				panelState.toggleAnimationCollapse();
			}
		} else if (action === 'edit') {
			// Close fullscreen and handle edit
			handleCloseFullscreen();
			originalHandleSequenceAction(action, sequence);
		} else if (action === 'save') {
			// Handle save action
			originalHandleSequenceAction(action, sequence);
		} else if (action === 'delete') {
			// Close fullscreen and handle delete
			handleCloseFullscreen();
			originalHandleSequenceAction(action, sequence);
		} else if (action === 'fullscreen') {
			// Handle fullscreen action
			fullscreenSequence = sequence;
			showFullscreenViewer = true;
		} else {
			// Pass through other actions to original handler
			originalHandleSequenceAction(action, sequence);
		}
	}

	// ✅ ANIMATION PANEL HANDLERS
	function handleCloseAnimationPanel() {
		panelState.setAnimationVisible(false);
		animationSequence = null;
	}

	// ✅ RESIZE HANDLERS: For panel width changes
	function handleNavigationResize(width: number) {
		// Additional logic if needed when navigation panel is resized
	}

	function handleAnimationResize(width: number) {
		// Additional logic if needed when animation panel is resized
	}
</script>

<div class="browse-tab">
	<!-- Error banner -->
	<ErrorBanner
		show={hasError}
		message={browseState.loadingState.error || ''}
		onDismiss={handleClearError}
	/>

	<!-- Enhanced layout with unified panel management -->
	<BrowseLayoutEnhanced 
		{panelState}
		onNavigationResize={handleNavigationResize}
		onAnimationResize={handleAnimationResize}
	>
		{#snippet navigationSidebar()}
			<NavigationSidebar
				sections={navigationSections}
				onSectionToggle={handleNavigationSectionToggle}
				onItemClick={handleNavigationItemClick}
				isCollapsed={panelState.isNavigationCollapsed}
				onToggleCollapse={handleToggleNavigationCollapse}
			/>
		{/snippet}

		{#snippet centerPanel()}
			{#if currentPanelIndex === 0}
				<!-- Filter Selection Panel -->
				<PanelContainer panelName="filter-selection">
					<FilterSelectionPanel onFilterSelected={handleFilterSelected} />
				</PanelContainer>
			{:else if currentPanelIndex === 1}
				<!-- Sequence Browser Panel -->
				<PanelContainer panelName="sequence-browser">
					<SequenceBrowserPanel
						filter={selectedFilter}
						{sequences}
						{isLoading}
						onBackToFilters={handleBackToFilters}
						onAction={handleSequenceAction}
					/>
				</PanelContainer>
			{/if}
		{/snippet}

		{#snippet rightPanel()}
			<!-- Enhanced Animation Panel with unified panel management -->
			<AnimationPanel
				sequence={animationSequence}
				{panelState}
				onClose={handleCloseAnimationPanel}
			/>
		{/snippet}
	</BrowseLayoutEnhanced>

	<!-- Loading overlay for initial load -->
	<LoadingOverlay
		show={isLoading && sequences.length === 0}
		message="Loading sequence library..."
		detail={browseState.loadingState.currentOperation}
	/>

	<!-- Delete Confirmation Dialog -->
	<DeleteConfirmationDialog
		confirmationData={deleteConfirmation}
		show={showDeleteDialog}
		onConfirm={handleConfirmDelete}
		onCancel={handleCancelDelete}
	/>

	<!-- Fullscreen Sequence Viewer -->
	<FullscreenSequenceViewer
		show={showFullscreenViewer}
		{...fullscreenSequence ? { sequence: fullscreenSequence } : {}}
		{thumbnailService}
		onClose={handleCloseFullscreen}
		onAction={handleSequenceAction}
	/>
</div>

<style>
	.browse-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		overflow: hidden;
		background: transparent;
		position: relative;
	}

	/* Global panel animation support */
	:global(.browse-tab .panel-transition) {
		transition: all var(--transition-normal);
	}

	/* Ensure proper stacking for overlays */
	.browse-tab :global(.loading-overlay),
	.browse-tab :global(.error-banner),
	.browse-tab :global(.delete-dialog),
	.browse-tab :global(.fullscreen-viewer) {
		z-index: 1000;
	}

	/* Panel state debugging (remove in production) */
	.browse-tab::after {
		content: '';
		position: fixed;
		top: 10px;
		right: 10px;
		width: 10px;
		height: 10px;
		background: var(--color-success);
		border-radius: 50%;
		z-index: 9999;
		opacity: 0;
		transition: opacity 0.3s;
	}
</style>
