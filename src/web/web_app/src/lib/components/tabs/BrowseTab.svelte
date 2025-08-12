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
		ISectionService,
		ISequenceIndexService,
		IThumbnailService,
	} from '$lib/services/interfaces';
	import { createBrowseState } from '$lib/state/browse-state.svelte';
	import { onMount } from 'svelte';
	// Extracted components
	import AnimationPanel from './browse/AnimationPanel.svelte';
	import BrowseLayout from './browse/BrowseLayout.svelte';
	import DeleteConfirmationDialog from './browse/DeleteConfirmationDialog.svelte';
	import ErrorBanner from './browse/ErrorBanner.svelte';
	import FilterSelectionPanel from './browse/FilterSelectionPanel.svelte';
	import FullscreenSequenceViewer from './browse/FullscreenSequenceViewer.svelte';
	import LoadingOverlay from './browse/LoadingOverlay.svelte';
	import NavigationSidebar from './browse/NavigationSidebar.svelte';
	import PanelContainer from './browse/PanelContainer.svelte';
	import SequenceBrowserPanel from './browse/sequence-browser/SequenceBrowserPanel.svelte';
	// Extracted event handlers
	import { createBrowseEventHandlers } from './browse/browse-event-handlers';
	import { createNavigationEventHandlers } from './browse/navigation-event-handlers';

	// ✅ RESOLVE SERVICES: Get services from DI container
	const browseService = resolve('IBrowseService') as IBrowseService;
	const thumbnailService = resolve('IThumbnailService') as IThumbnailService;
	const sequenceIndexService = resolve('ISequenceIndexService') as ISequenceIndexService;
	// Advanced browse services
	const favoritesService = resolve('IFavoritesService') as IFavoritesService;
	const navigationService = resolve('INavigationService') as INavigationService;
	const filterPersistenceService = resolve(
		'IFilterPersistenceService'
	) as IFilterPersistenceService;
	const sectionService = resolve('ISectionService') as ISectionService;
	const deleteService = resolve('IDeleteService') as IDeleteService;

	// ✅ CREATE BROWSE STATE: Runes-based reactive state
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

	// ✅ PURE RUNES: Local UI state
	let currentPanelIndex = $state(0); // 0 = filter selection, 1 = sequence browser
	let isNavigationCollapsed = $state(false); // Navigation sidebar collapse state
	let showFullscreenViewer = $state(false); // Fullscreen sequence viewer state
	let fullscreenSequence = $state<BrowseSequenceMetadata | undefined>(undefined); // Current sequence for fullscreen

	// Phase 3: Animation panel state
	let showAnimationPanel = $state(false); // Animation panel visibility
	let animationSequence = $state<BrowseSequenceMetadata | null>(null); // Current sequence for animation

	// ✅ DERIVED RUNES: Computed UI state from browse state
	let selectedFilter = $derived(browseState.currentFilter);
	let isLoading = $derived(browseState.isLoading);
	let hasError = $derived(browseState.hasError);
	let sequences = $derived(browseState.displayedSequences);
	let navigationMode = $derived(browseState.navigationMode);

	// Advanced derived values
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
			console.log('🚀 Loading browse data...');
			await browseState.loadAllSequences();
			console.log('✅ Browse data loaded successfully');
		} catch (error) {
			console.error('❌ Failed to load browse data:', error);
		}
	});

	// ✅ EXTRACTED EVENT HANDLERS: Create event handlers using extracted functions
	const browseEventHandlers = createBrowseEventHandlers(browseState, (index) => {
		currentPanelIndex = index;
	});

	const navigationEventHandlers = createNavigationEventHandlers(
		browseState,
		(index) => {
			currentPanelIndex = index;
		},
		() => {
			isNavigationCollapsed = !isNavigationCollapsed;
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

	// ✅ CUSTOM HANDLERS: Override default behavior for fullscreen functionality
	function handleSequenceSelected(sequence: BrowseSequenceMetadata) {
		console.log('📄 Opening sequence in fullscreen:', sequence.word);
		fullscreenSequence = sequence;
		showFullscreenViewer = true;
	}

	function handleCloseFullscreen() {
		console.log('❌ Closing fullscreen viewer');
		showFullscreenViewer = false;
		fullscreenSequence = undefined;
	}

	function handleSequenceAction(action: string, sequence: BrowseSequenceMetadata) {
		console.log(`🎬 Sequence action: ${action} on sequence:`, sequence.id);

		if (action === 'animate') {
			// Phase 3: Handle animate action
			console.log('🎬 Opening animation panel for sequence:', sequence.id);
			animationSequence = sequence;
			showAnimationPanel = true;
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
		} else {
			// Pass through other actions to original handler
			originalHandleSequenceAction(action, sequence);
		}
	}

	// Phase 3: Animation panel handlers
	function handleCloseAnimationPanel() {
		console.log('🎬 Closing animation panel');
		showAnimationPanel = false;
		animationSequence = null;
	}
</script>

<div class="browse-tab">
	<!-- Error banner -->
	<ErrorBanner
		show={hasError}
		message={browseState.loadingState.error || ''}
		onDismiss={handleClearError}
	/>

	<!-- Main layout using extracted component -->
	<BrowseLayout {isNavigationCollapsed}>
		{#snippet navigationSidebar()}
			<NavigationSidebar
				sections={navigationSections}
				onSectionToggle={handleNavigationSectionToggle}
				onItemClick={handleNavigationItemClick}
				isCollapsed={isNavigationCollapsed}
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
						onSequenceSelected={handleSequenceSelected}
						onBackToFilters={handleBackToFilters}
					/>
				</PanelContainer>
			{/if}
		{/snippet}
	</BrowseLayout>

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
</style>
