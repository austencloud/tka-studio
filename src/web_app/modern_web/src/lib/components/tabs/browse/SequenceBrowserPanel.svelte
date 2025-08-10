<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import LoadingSpinner from './LoadingSpinner.svelte';
	import type { SequenceData } from './SequenceThumbnail.svelte';
	import SequenceThumbnail from './SequenceThumbnail.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		filter = null,
		isLoading = false,
		onSequenceSelected = () => {},
		onBackToFilters = () => {},
	} = $props<{
		filter?: { type: string; value: unknown } | null;
		isLoading?: boolean;
		onSequenceSelected?: (sequence: SequenceData) => void;
		onBackToFilters?: () => void;
	}>();

	// ✅ PURE RUNES: State using runes
	let sequences: SequenceData[] = $state([]);
	let sortBy = $state('name'); // 'name', 'difficulty', 'length', 'recent'
	let viewMode: 'grid' | 'list' = $state('grid');

	// Sort options
	const sortOptions = [
		{ value: 'name', label: 'Name A-Z' },
		{ value: 'difficulty', label: 'Difficulty' },
		{ value: 'length', label: 'Length' },
		{ value: 'recent', label: 'Recently Added' },
	];

	// Generate mock sequences based on filter
	function generateMockSequences(
		filter: { type: string; value: unknown } | null
	): SequenceData[] {
		if (!filter) return [];

		const mockSequences: SequenceData[] = [];
		const count = Math.floor(Math.random() * 20) + 10; // 10-30 sequences

		for (let i = 0; i < count; i++) {
			mockSequences.push({
				id: `seq_${i}`,
				name: `Word${i + 1}`,
				difficulty: Math.floor(Math.random() * 4) + 1,
				createdDate: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000),
				description: `Sequence ${i + 1} description`,
				tags: ['flow', 'beginner', 'practice'].slice(0, Math.floor(Math.random() * 3) + 1),
				author: 'TKA User',
				duration: Math.floor(Math.random() * 60) + 30,
				beatCount: Math.floor(Math.random() * 6) + 2,
			});
		}

		return mockSequences;
	}

	// Sort sequences
	function sortSequences(sequences: SequenceData[], sortBy: string): SequenceData[] {
		return [...sequences].sort((a, b) => {
			switch (sortBy) {
				case 'name':
					return a.name.localeCompare(b.name);
				case 'difficulty':
					return a.difficulty - b.difficulty;
				case 'length':
					return (a.beatCount || 0) - (b.beatCount || 0);
				case 'recent':
					return b.createdDate.getTime() - a.createdDate.getTime();
				default:
					return 0;
			}
		});
	}

	// Handle sequence selection
	function handleSequenceSelect(sequence: SequenceData) {
		onSequenceSelected(sequence);
	}

	// Handle back to filters
	function handleBackToFilters() {
		onBackToFilters();
	}

	// Handle sort change
	function handleSortChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		sortBy = target.value;
	}

	// ✅ PURE RUNES: Reactive sorting using derived
	const sortedSequences = $derived(sortSequences(sequences, sortBy));

	// ✅ PURE RUNES: Load sequences when filter changes using effect
	$effect(() => {
		if (filter) {
			sequences = generateMockSequences(filter);
		}
	});
</script>

<div class="sequence-browser-panel">
	<!-- Header with controls -->
	<div class="browser-header">
		<div class="header-left">
			<button class="back-button" onclick={handleBackToFilters} type="button">
				<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
					<path
						d="M12.5 15L7.5 10L12.5 5"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
				Back to Filters
			</button>

			{#if filter}
				<div class="filter-info">
					<span class="filter-type">{filter.type.replace('_', ' ')}</span>
					<span class="filter-value">{filter.value}</span>
				</div>
			{/if}
		</div>

		<div class="header-right">
			<div class="view-controls">
				<label class="sort-control">
					Sort by:
					<select bind:value={sortBy} onchange={handleSortChange}>
						{#each sortOptions as option}
							<option value={option.value}>{option.label}</option>
						{/each}
					</select>
				</label>

				<div class="view-mode-toggle">
					<button
						class="view-button"
						class:active={viewMode === 'grid'}
						onclick={() => (viewMode = 'grid')}
						title="Grid View"
						aria-label="Switch to grid view"
						type="button"
					>
						<svg width="16" height="16" viewBox="0 0 16 16">
							<rect x="1" y="1" width="6" height="6" fill="currentColor" />
							<rect x="9" y="1" width="6" height="6" fill="currentColor" />
							<rect x="1" y="9" width="6" height="6" fill="currentColor" />
							<rect x="9" y="9" width="6" height="6" fill="currentColor" />
						</svg>
					</button>
					<button
						class="view-button"
						class:active={viewMode === 'list'}
						onclick={() => (viewMode = 'list')}
						title="List View"
						aria-label="Switch to list view"
						type="button"
					>
						<svg width="16" height="16" viewBox="0 0 16 16">
							<rect x="1" y="2" width="14" height="2" fill="currentColor" />
							<rect x="1" y="7" width="14" height="2" fill="currentColor" />
							<rect x="1" y="12" width="14" height="2" fill="currentColor" />
						</svg>
					</button>
				</div>
			</div>
		</div>
	</div>

	<!-- Content area -->
	<div class="browser-content">
		{#if isLoading}
			<div class="loading-container" transition:fade>
				<LoadingSpinner />
				<p>Loading sequences...</p>
			</div>
		{:else if sortedSequences.length > 0}
			<div
				class="sequences-grid"
				class:list-view={viewMode === 'list'}
				transition:slide={{ duration: 300 }}
			>
				{#each sortedSequences as sequence}
					<SequenceThumbnail {sequence} {viewMode} onSelect={handleSequenceSelect} />
				{/each}
			</div>
		{:else}
			<div class="empty-state">
				<div class="empty-content">
					<div class="empty-icon">📭</div>
					<h3>No sequences found</h3>
					<p>Try adjusting your filter criteria or browse all sequences.</p>
					<button class="browse-all-button" onclick={handleBackToFilters} type="button">
						Browse All Sequences
					</button>
				</div>
			</div>
		{/if}
	</div>

	<!-- Results summary -->
	{#if !isLoading && sortedSequences.length > 0}
		<div class="results-footer" transition:slide>
			<span class="results-count">
				{sortedSequences.length} sequence{sortedSequences.length !== 1 ? 's' : ''} found
			</span>
		</div>
	{/if}
</div>

<style>
	.sequence-browser-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	/* Header */
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

	.header-left {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
	}

	.back-button {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 255, 255, 0.1);
		border: var(--glass-border);
		border-radius: 8px;
		color: var(--foreground);
		font-family: inherit;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.back-button:hover {
		background: rgba(255, 255, 255, 0.15);
		border-color: var(--primary-color);
		color: var(--primary-color);
	}

	.filter-info {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(99, 102, 241, 0.1);
		border: 1px solid rgba(99, 102, 241, 0.3);
		border-radius: 20px;
		font-size: var(--font-size-sm);
	}

	.filter-type {
		color: var(--primary-color);
		font-weight: 500;
		text-transform: capitalize;
	}

	.filter-value {
		color: var(--foreground);
		font-weight: 600;
	}

	.header-right {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
	}

	.view-controls {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
	}

	.sort-control {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
	}

	.sort-control select {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: rgba(255, 255, 255, 0.1);
		border: var(--glass-border);
		border-radius: 6px;
		color: var(--foreground);
		font-family: inherit;
		font-size: var(--font-size-sm);
	}

	.view-mode-toggle {
		display: flex;
		background: rgba(255, 255, 255, 0.05);
		border: var(--glass-border);
		border-radius: 6px;
		overflow: hidden;
	}

	.view-button {
		padding: var(--spacing-xs);
		background: transparent;
		border: none;
		color: var(--muted-foreground);
		cursor: pointer;
		transition: all var(--transition-fast);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.view-button:hover {
		background: rgba(255, 255, 255, 0.1);
		color: var(--foreground);
	}

	.view-button.active {
		background: var(--primary-color);
		color: white;
	}

	/* Content */
	.browser-content {
		flex: 1;
		overflow-y: auto;
		padding: var(--spacing-lg);
	}

	.sequences-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: var(--spacing-lg);
	}

	.sequences-grid.list-view {
		grid-template-columns: 1fr;
		gap: var(--spacing-md);
	}

	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		gap: var(--spacing-md);
		color: var(--muted-foreground);
	}

	.empty-state {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
	}

	.empty-content {
		text-align: center;
		max-width: 400px;
	}

	.empty-icon {
		font-size: 4rem;
		margin-bottom: var(--spacing-lg);
	}

	.empty-content h3 {
		font-size: var(--font-size-xl);
		color: var(--foreground);
		margin-bottom: var(--spacing-md);
	}

	.empty-content p {
		color: var(--muted-foreground);
		margin-bottom: var(--spacing-lg);
		line-height: 1.5;
	}

	.browse-all-button {
		padding: var(--spacing-md) var(--spacing-lg);
		background: var(--gradient-primary);
		border: none;
		border-radius: 8px;
		color: white;
		font-family: inherit;
		font-weight: 500;
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.browse-all-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
	}

	/* Footer */
	.results-footer {
		flex-shrink: 0;
		padding: var(--spacing-md) var(--spacing-lg);
		background: rgba(255, 255, 255, 0.03);
		border-top: var(--glass-border);
		text-align: center;
	}

	.results-count {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
	}

	/* Responsive Design */
	@media (max-width: 1024px) {
		.sequences-grid {
			grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
		}
	}

	@media (max-width: 768px) {
		.browser-header {
			flex-direction: column;
			gap: var(--spacing-md);
			align-items: stretch;
		}

		.header-left,
		.header-right {
			justify-content: center;
		}

		.sequences-grid {
			grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
			gap: var(--spacing-md);
		}

		.browser-content {
			padding: var(--spacing-md);
		}
	}

	@media (max-width: 480px) {
		.sequences-grid {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
