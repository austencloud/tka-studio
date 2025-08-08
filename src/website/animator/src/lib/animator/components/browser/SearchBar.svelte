<script lang="ts">
	// Import new sub-components
	import SearchToggle from './SearchToggle.svelte';
	import SearchInput from './SearchInput.svelte';
	import CategoryFilter from './CategoryFilter.svelte';
	import StepFilters from './StepFilters.svelte';
	import Upload from 'lucide-svelte/icons/upload';

	// Props
	let {
		searchQuery = '',
		selectedCategory = 'All',
		categories = [],
		onSearchChange,
		onCategoryChange,
		onRefresh,
		onJSONImport,
		disabled = false
	}: {
		searchQuery: string;
		selectedCategory: string;
		categories: string[];
		onSearchChange?: (_query: string) => void;
		onCategoryChange?: (_category: string) => void;
		onRefresh?: () => void;
		onJSONImport?: () => void;
		disabled?: boolean;
	} = $props();

	// Local state
	let isExpanded = $state(false);
	let selectedStepFilter = $state('all');

	function toggleExpanded(): void {
		isExpanded = !isExpanded;
	}

	function handleStepFilterChange(filterId: string): void {
		selectedStepFilter = filterId;
		// For now, we'll just store the filter state
		// In a real implementation, this would trigger filtering
	}

	function handleJSONImport(): void {
		onJSONImport?.();
	}
</script>

<div class="search-bar">
	<!-- Mobile: Collapsible search toggle -->
	<SearchToggle {isExpanded} onToggle={toggleExpanded} />

	<!-- Search controls - always visible on desktop, collapsible on mobile -->
	<div class="search-controls" class:expanded={isExpanded}>
		<SearchInput {searchQuery} {onSearchChange} {disabled} />

		<CategoryFilter {selectedCategory} {categories} {onCategoryChange} {onRefresh} {disabled} />

		<StepFilters {selectedStepFilter} onStepFilterChange={handleStepFilterChange} {disabled} />

		<!-- JSON Import Button -->
		<button
			type="button"
			class="json-import-button"
			onclick={handleJSONImport}
			{disabled}
			title="Import sequence from JSON data"
			aria-label="Import JSON sequence"
		>
			<Upload size={16} />
			Import JSON
		</button>
	</div>
</div>

<style>
	.search-bar {
		margin-bottom: 1rem;
		padding: 1rem;
		background: var(--color-background);
		border-radius: 6px;
		border: 1px solid var(--color-border);
		flex-shrink: 0;
		transition: all 0.3s ease;
	}

	.search-controls {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		transition: all 0.3s ease;
		overflow: hidden;
	}

	.json-import-button {
		background: var(--color-primary);
		border: 1px solid var(--color-primary);
		color: white;
		padding: 0.75rem 1rem;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		font-size: 0.875rem;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		justify-content: center;
		min-width: fit-content;
	}

	.json-import-button:hover:not(:disabled) {
		background: var(--color-primary-hover);
		border-color: var(--color-primary-hover);
		transform: translateY(-1px);
		box-shadow: 0 4px 8px rgba(var(--color-primary-rgb), 0.3);
	}

	.json-import-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
		box-shadow: none;
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.search-controls {
			flex-direction: row;
			align-items: center;
			gap: 0.75rem;
		}
	}

	@media (max-width: 768px) {
		/* Collapsible search on mobile */
		.search-controls {
			max-height: 0;
			opacity: 0;
			margin-bottom: 0;
			padding: 0;
			flex-direction: column;
			gap: 0.5rem;
			transition: all 0.3s ease;
		}

		.search-controls.expanded {
			max-height: 200px;
			opacity: 1;
			margin-bottom: 0.75rem;
			padding: 0.75rem;
			background: var(--color-surface);
			border: 1px solid var(--color-border);
			border-radius: 8px;
		}

		.search-bar {
			padding: 0.5rem;
			margin-bottom: 0.5rem;
		}
	}
</style>
