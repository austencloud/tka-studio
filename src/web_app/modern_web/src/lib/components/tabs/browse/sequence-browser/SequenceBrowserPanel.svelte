<script lang="ts">
	import type { BrowseSequenceMetadata, FilterType, FilterValue } from '$lib/domain/browse';
	import { SortMethod } from '$lib/domain/browse';
	import { resolve } from '$lib/services/bootstrap';
	import SequenceBrowserControls from './SequenceBrowserControls.svelte';
	import SequenceBrowserFooter from './SequenceBrowserFooter.svelte';
	import SequenceBrowserHeader from './SequenceBrowserHeader.svelte';
	import SequenceBrowserStates from './SequenceBrowserStates.svelte';
	import SequenceGrid from './SequenceGrid.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		filter = null,
		sequences = [],
		isLoading = false,
		onSequenceSelected = () => {},
		onBackToFilters = () => {},
	} = $props<{
		filter?: { type: FilterType; value: FilterValue } | null;
		sequences?: BrowseSequenceMetadata[];
		isLoading?: boolean;
		onSequenceSelected?: (sequence: BrowseSequenceMetadata) => void;
		onBackToFilters?: () => void;
	}>();

	// ✅ RESOLVE SERVICES: Get services from DI container
	const thumbnailService = resolve('IThumbnailService');

	// ✅ PURE RUNES: State using runes
	let sortBy = $state<SortMethod>(SortMethod.ALPHABETICAL);
	let viewMode: 'grid' | 'list' = $state('grid');
	let error = $state<string | null>(null);

	// ✅ DERIVED RUNES: Reactive sorting
	const sortedSequences = $derived(() => {
		console.log(
			'🔄 Recomputing sortedSequences derived. sequences.length:',
			sequences.length,
			'sortBy:',
			sortBy
		);

		if (sequences.length === 0) {
			return [];
		}

		const sorted = [...sequences].sort((a, b) => {
			switch (sortBy) {
				case SortMethod.ALPHABETICAL:
					return a.word.localeCompare(b.word);
				case SortMethod.DIFFICULTY_LEVEL:
					// Fix: Use difficultyLevel instead of difficulty
					const getDifficultyOrder = (level?: string) => {
						switch (level) {
							case 'beginner':
								return 1;
							case 'intermediate':
								return 2;
							case 'advanced':
								return 3;
							default:
								return 0;
						}
					};
					return (
						getDifficultyOrder(a.difficultyLevel) -
						getDifficultyOrder(b.difficultyLevel)
					);
				case SortMethod.SEQUENCE_LENGTH:
					// Fix: Use sequenceLength instead of length
					return (a.sequenceLength || 0) - (b.sequenceLength || 0);
				case SortMethod.DATE_ADDED:
					return (b.dateAdded?.getTime() || 0) - (a.dateAdded?.getTime() || 0);
				case SortMethod.AUTHOR:
					return (a.author || '').localeCompare(b.author || '');
				default:
					return 0;
			}
		});

		console.log('✅ Sorted sequences:', sorted.length);
		return sorted;
	});

	// ✅ DERIVED RUNES: UI state
	const isEmpty = $derived(() => !isLoading && !error && sortedSequences().length === 0);
	const hasSequences = $derived(() => !isLoading && !error && sortedSequences().length > 0);
	const showFooter = $derived(() => !isLoading && !error && sortedSequences().length > 0);

	// ✅ RUNES METHODS: Event handlers
	function handleSortChange(newSortBy: SortMethod) {
		console.log('🔄 Sort changed to:', newSortBy);
		sortBy = newSortBy;
	}

	function handleViewModeChange(newViewMode: 'grid' | 'list') {
		console.log('👁️ View mode changed to:', newViewMode);
		viewMode = newViewMode;
	}

	function handleSequenceSelect(sequence: BrowseSequenceMetadata) {
		console.log('📄 Sequence selected:', sequence.word);
		onSequenceSelected(sequence);
	}

	function handleBackToFilters() {
		console.log('🔙 Back to filters');
		onBackToFilters();
	}

	function handleRetry() {
		console.log('🔄 Retry loading');
		error = null;
		// Error handling will be managed by parent component
	}
</script>

<div class="sequence-browser-panel">
	<!-- Header with back button and filter info -->
	<div class="browser-header">
		<SequenceBrowserHeader {filter} onBackToFilters={handleBackToFilters} />
		<SequenceBrowserControls
			{sortBy}
			{viewMode}
			onSortChange={handleSortChange}
			onViewModeChange={handleViewModeChange}
		/>
	</div>

	<!-- Content area -->
	<div class="browser-content">
		<SequenceBrowserStates
			{isLoading}
			{error}
			isEmpty={isEmpty()}
			sequencesLength={sequences.length}
			sortedSequencesLength={sortedSequences().length}
			onRetry={handleRetry}
			onBackToFilters={handleBackToFilters}
		/>

		{#if hasSequences()}
			<SequenceGrid
				sequences={sortedSequences()}
				{viewMode}
				{thumbnailService}
				onSequenceSelected={handleSequenceSelect}
			/>
		{/if}
	</div>

	<!-- Results summary -->
	<SequenceBrowserFooter sequenceCount={sortedSequences().length} isVisible={showFooter()} />
</div>

<style>
	.sequence-browser-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.browser-header {
		flex-shrink: 0;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-lg);
		background: rgba(255, 255, 255, 0.05);
		border-bottom: var(--glass-border);
		backdrop-filter: var(--glass-backdrop);
	}

	.browser-content {
		flex: 1;
		overflow-y: auto;
		padding: var(--spacing-lg);
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.browser-header {
			flex-direction: column;
			gap: var(--spacing-md);
			align-items: stretch;
		}
	}
</style>
