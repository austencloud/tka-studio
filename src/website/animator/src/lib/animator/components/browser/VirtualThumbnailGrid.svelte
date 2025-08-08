<script lang="ts">
	import type { DictionaryItem } from '../../types/core.js';
	import ThumbnailCard from './ThumbnailCard.svelte';
	import ScrollIndicator from './ScrollIndicator.svelte';
	import {
		VirtualGridManager,
		type VirtualGridItem
	} from '../../utils/performance/virtual-grid.js';

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
	let virtualState = $state({
		visibleItems: [] as VirtualGridItem[],
		topSpacer: 0,
		bottomSpacer: 0,
		totalItems: 0,
		renderRatio: 0
	});

	// Virtual grid manager
	const virtualGrid = new VirtualGridManager({
		itemHeight: 280, // Estimated height per thumbnail card
		overscan: 4, // Render 4 extra items outside viewport
		columns: 2, // Fixed 2-column layout
		gap: 16, // 1rem gap
		padding: 16 // 1rem padding
	});

	// Subscribe to virtual grid updates
	let unsubscribe: (() => void) | null = null;

	// Convert DictionaryItems to VirtualGridItems
	$effect(() => {
		const virtualItems: VirtualGridItem[] = items.map((item) => ({
			id: item.id,
			data: item
		}));

		virtualGrid.setItems(virtualItems);
		updateVirtualState();
	});

	// Set up virtual grid subscription
	$effect(() => {
		unsubscribe = virtualGrid.subscribe(() => {
			updateVirtualState();
		});

		return () => {
			unsubscribe?.();
			virtualGrid.destroy();
		};
	});

	// Handle resize events and viewport updates - DISABLED during sidebar resize for performance
	$effect(() => {
		if (!gridElement || typeof window === 'undefined') return;

		// Initial viewport setup
		const rect = gridElement.getBoundingClientRect();
		virtualGrid.updateViewport(rect.height, gridElement.scrollTop);

		// Listen for window resize events (but not during sidebar resize)
		const handleWindowResize = () => {
			// Only update if not currently resizing sidebar
			const sidebarResizing = document.body.style.cursor === 'col-resize';
			if (!sidebarResizing && gridElement) {
				const rect = gridElement.getBoundingClientRect();
				virtualGrid.updateViewport(rect.height, gridElement.scrollTop);
			}
		};

		window.addEventListener('resize', handleWindowResize);

		return () => {
			window.removeEventListener('resize', handleWindowResize);
		};
	});

	// Simplified resize handling - no complex state management during sidebar resize
	$effect(() => {
		if (typeof window === 'undefined') return;

		// Listen for the custom resize event dispatched after sidebar resize ends
		const handleCustomResize = () => {
			if (gridElement) {
				const rect = gridElement.getBoundingClientRect();
				virtualGrid.updateViewport(rect.height, gridElement.scrollTop);
				virtualGrid.endResize(); // Restore normal rendering
			}
		};

		window.addEventListener('resize', handleCustomResize);

		return () => {
			window.removeEventListener('resize', handleCustomResize);
		};
	});

	function updateVirtualState(): void {
		const state = virtualGrid.getState();
		const spacers = virtualGrid.getSpacerHeights();
		const stats = virtualGrid.getStats();

		virtualState = {
			visibleItems: state.visibleItems,
			topSpacer: spacers.top,
			bottomSpacer: spacers.bottom,
			totalItems: stats.totalItems,
			renderRatio: stats.renderRatio
		};
	}

	function handleScroll(event: Event): void {
		const target = event.target as HTMLDivElement;
		const { scrollTop, scrollHeight, clientHeight } = target;

		// Update virtual grid viewport
		virtualGrid.updateViewport(clientHeight, scrollTop);

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
		<!-- Top spacer for virtual scrolling -->
		{#if virtualState.topSpacer > 0}
			<div class="spacer" style:height="{virtualState.topSpacer}px"></div>
		{/if}

		<!-- Visible items -->
		{#each virtualState.visibleItems as virtualItem (virtualItem.id)}
			<ThumbnailCard item={virtualItem.data} onSelect={() => handleItemSelect(virtualItem.data)} />
		{/each}

		<!-- Bottom spacer for virtual scrolling -->
		{#if virtualState.bottomSpacer > 0}
			<div class="spacer" style:height="{virtualState.bottomSpacer}px"></div>
		{/if}
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

	.spacer {
		grid-column: 1 / -1; /* Span all columns */
		width: 100%;
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
