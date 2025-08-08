<script lang="ts">
	// Import Lucide icons
	import RefreshCw from 'lucide-svelte/icons/refresh-cw';

	// Props
	let {
		selectedCategory = 'All',
		categories = [],
		onCategoryChange,
		onRefresh,
		disabled = false
	}: {
		selectedCategory: string;
		categories: string[];
		onCategoryChange?: (_category: string) => void;
		onRefresh?: () => void;
		disabled?: boolean;
	} = $props();

	// Local state
	let isRefreshing = $state(false);

	function handleCategorySelect(event: Event): void {
		const target = event.target as HTMLSelectElement;
		onCategoryChange?.(target.value);
	}

	function handleRefreshClick(): void {
		isRefreshing = true;
		onRefresh?.();

		// Reset refreshing state after animation
		setTimeout(() => {
			isRefreshing = false;
		}, 600);
	}
</script>

<div class="filter-container">
	<label for="category-filter" class="filter-label">Filter:</label>
	<select
		id="category-filter"
		value={selectedCategory}
		onchange={handleCategorySelect}
		{disabled}
		class="category-filter"
		aria-label="Filter by category"
	>
		{#each categories as category}
			<option value={category}>{category}</option>
		{/each}
	</select>

	<button
		type="button"
		onclick={handleRefreshClick}
		{disabled}
		class="refresh-button"
		class:refreshing={isRefreshing}
		aria-label="Refresh library"
		title="Refresh library"
	>
		<RefreshCw size={16} class={isRefreshing ? 'spinning' : ''} />
	</button>
</div>

<style>
	.filter-container {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.filter-label {
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		white-space: nowrap;
	}

	.category-filter {
		padding: 0.75rem;
		border: 1px solid var(--color-border);
		border-radius: 6px;
		font-size: 1rem;
		background: var(--color-surface);
		color: var(--color-text-primary);
		cursor: pointer;
		transition:
			border-color 0.2s ease,
			background-color 0.3s ease;
		flex: 1;
	}

	.category-filter:focus {
		outline: none;
		border-color: var(--color-primary);
		box-shadow: 0 0 0 3px var(--color-primary-alpha);
	}

	.category-filter:disabled {
		background: var(--color-surface-hover);
		color: var(--color-text-secondary);
		cursor: not-allowed;
	}

	.refresh-button {
		padding: 0.5rem;
		background: var(--color-background);
		border: 1px solid var(--color-border);
		border-radius: 50%;
		cursor: pointer;
		font-size: 1rem;
		line-height: 1;
		transition:
			background-color 0.2s ease,
			border-color 0.2s ease,
			box-shadow 0.2s ease;
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		margin-left: 0.5rem;
		color: var(--color-text-primary);
	}

	.refresh-button:hover:not(:disabled) {
		background: var(--color-surface-hover);
		border-color: var(--color-primary);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		color: var(--color-primary);
	}

	.refresh-button:active:not(:disabled) {
		transform: scale(0.95);
	}

	.refresh-button:disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	/* Spinning animation for refresh icon */
	:global(.spinning) {
		animation: spin 0.6s linear;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.filter-container {
			gap: 0.25rem;
		}

		.filter-label {
			font-size: 0.8rem;
		}

		.category-filter {
			font-size: 0.9rem;
		}

		.refresh-button {
			width: 36px;
			height: 36px;
		}
	}
</style>
