<script lang="ts">
	import type { DictionaryItem, SequenceData } from '../../types/core.js';
	import { HybridDictionaryService } from '../../core/services/hybrid-dictionary.js';
	import SearchBar from './SearchBar.svelte';
	import BrowserStates from './BrowserStates.svelte';
	import ResultsInfo from './ResultsInfo.svelte';
	import VirtualThumbnailGrid from './VirtualThumbnailGrid.svelte';
	import JSONImportModal from './JSONImportModal.svelte';

	// Props
	let {
		onSequenceSelected
	}: {
		onSequenceSelected?: (_data: SequenceData, _item: DictionaryItem) => void;
	} = $props();

	// State
	let items = $state<DictionaryItem[]>([]);
	let filteredItems = $state<DictionaryItem[]>([]);
	let categories = $state<string[]>([]);
	let isLoading = $state(true);
	let error = $state('');
	let searchQuery = $state('');
	let selectedCategory = $state('All');
	let isJSONModalOpen = $state(false);

	// Services
	const dictionaryService = HybridDictionaryService.getInstance();

	// Load dictionary on mount
	$effect(() => {
		loadDictionary();
	});

	// Filter items when search or category changes
	$effect(() => {
		filterItems();
	});

	async function loadDictionary(): Promise<void> {
		try {
			isLoading = true;
			error = '';

			const index = await dictionaryService.getIndex();
			items = sortByStepCount(index.items);
			categories = ['All', ...index.categories];
			filteredItems = items;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load dictionary';
			console.error('Failed to load dictionary:', err);
		} finally {
			isLoading = false;
		}
	}

	async function filterItems(): Promise<void> {
		try {
			const results = await dictionaryService.searchItems(
				searchQuery,
				selectedCategory === 'All' ? undefined : selectedCategory
			);
			// Sort by step count (shortest to longest) as default
			filteredItems = sortByStepCount(results);
		} catch (err) {
			console.error('Failed to filter items:', err);
			filteredItems = sortByStepCount(items);
		}
	}

	function sortByStepCount(itemsToSort: DictionaryItem[]): DictionaryItem[] {
		return [...itemsToSort].sort((a, b) => {
			const stepsA = a.sequenceData.length - 2; // Subtract metadata and start position
			const stepsB = b.sequenceData.length - 2;

			// Primary sort: by step count (ascending)
			if (stepsA !== stepsB) {
				return stepsA - stepsB;
			}

			// Secondary sort: by name (alphabetical)
			return a.name.localeCompare(b.name);
		});
	}

	function handleSearchChange(query: string): void {
		searchQuery = query;
	}

	function handleCategoryChange(category: string): void {
		selectedCategory = category;
	}

	function handleItemSelect(item: DictionaryItem): void {
		onSequenceSelected?.(item.sequenceData, item);
	}

	function handleRefresh(): void {
		loadDictionary();
	}

	function handleJSONImport(): void {
		isJSONModalOpen = true;
	}

	function handleJSONModalClose(): void {
		isJSONModalOpen = false;
	}

	function handleJSONImported(): void {
		isJSONModalOpen = false;
		loadDictionary(); // Refresh after import
	}
</script>

<div class="thumbnail-browser">
	<div class="browser-header">
		<SearchBar
			{searchQuery}
			{categories}
			{selectedCategory}
			onSearchChange={handleSearchChange}
			onCategoryChange={handleCategoryChange}
		/>
	</div>

	<div class="browser-content">
		<BrowserStates {isLoading} {error} onRefresh={handleRefresh} onImport={handleJSONImport}>
			<div class="results-section">
				<ResultsInfo
					totalItems={items.length}
					filteredItems={filteredItems.length}
					{searchQuery}
					{selectedCategory}
				/>

				<VirtualThumbnailGrid items={filteredItems} onItemSelect={handleItemSelect} />
			</div>
		</BrowserStates>
	</div>
</div>

{#if isJSONModalOpen}
	<JSONImportModal onClose={handleJSONModalClose} onImported={handleJSONImported} />
{/if}

<style>
	.thumbnail-browser {
		display: flex;
		flex-direction: column;
		height: 100%;
		min-height: 0;
	}

	.browser-header {
		flex-shrink: 0;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-background);
	}

	.browser-content {
		flex: 1;
		min-height: 0;
		display: flex;
		flex-direction: column;
	}

	.results-section {
		flex: 1;
		min-height: 0;
		display: flex;
		flex-direction: column;
	}
</style>
