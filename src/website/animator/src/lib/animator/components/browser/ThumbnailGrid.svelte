<script lang="ts">
	import type { DictionaryItem } from '../../types/core.js';
	import ThumbnailCard from './ThumbnailCard.svelte';
	import ScrollIndicator from './ScrollIndicator.svelte';

	// Props
	let {
		items = [],
		onItemSelect,
		onScroll
	}: {
		items?: DictionaryItem[];
		onItemSelect?: (_item: DictionaryItem) => void;
		onScroll?: (_event: Event) => void;
	} = $props();

	// State
	let gridElement: HTMLDivElement | null = $state(null);
	let scrollProgress = $state(0);
	let showScrollIndicator = $state(false);

	function handleScroll(event: Event): void {
		const target = event.target as HTMLDivElement;
		const { scrollTop, scrollHeight, clientHeight } = target;

		// Calculate scroll progress (0 to 1)
		const maxScroll = scrollHeight - clientHeight;
		scrollProgress = maxScroll > 0 ? scrollTop / maxScroll : 0;

		// Show indicator if there's content to scroll
		showScrollIndicator = maxScroll > 10;

		// Call parent handler
		onScroll?.(event);
	}

	function handleItemSelect(item: DictionaryItem): void {
		onItemSelect?.(item);
	}
</script>

<div class="grid-container">
	<ScrollIndicator {scrollProgress} showIndicator={showScrollIndicator} />

	<div
		class="thumbnail-grid"
		role="grid"
		aria-label="Sequence thumbnails"
		bind:this={gridElement}
		onscroll={handleScroll}
	>
		{#each items as item (item.id)}
			<ThumbnailCard {item} onSelect={() => handleItemSelect(item)} />
		{/each}
	</div>
</div>

<style>
	.grid-container {
		position: relative;
		flex: 1;
		min-height: 0;
	}

	.thumbnail-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		grid-auto-rows: min-content;
		gap: 1rem;
		padding: 1rem;
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
		min-height: 0;
		scrollbar-width: thin;
		scrollbar-color: var(--color-border, #e0e0e0) transparent;
		align-items: start;
		grid-auto-flow: row;
		height: 100%;
		justify-content: center;
	}

	.thumbnail-grid::-webkit-scrollbar {
		width: 8px;
	}

	.thumbnail-grid::-webkit-scrollbar-track {
		background: transparent;
	}

	.thumbnail-grid::-webkit-scrollbar-thumb {
		background: var(--color-border, #e0e0e0);
		border-radius: 4px;
	}

	.thumbnail-grid::-webkit-scrollbar-thumb:hover {
		background: var(--color-text-secondary, #666);
	}

	/* Responsive Design */
	@media (max-width: 1200px) {
		.thumbnail-grid {
			grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
			gap: 0.75rem;
			padding: 0.75rem;
		}
	}

	@media (max-width: 768px) {
		.thumbnail-grid {
			grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
			gap: 0.75rem;
			padding: 0.75rem;
		}
	}

	@media (max-width: 480px) {
		.thumbnail-grid {
			grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
			gap: 0.5rem;
			padding: 0.5rem;
		}
	}
</style>
