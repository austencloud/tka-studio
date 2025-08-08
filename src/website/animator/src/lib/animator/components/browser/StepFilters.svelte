<script lang="ts">
	// Props
	let {
		selectedStepFilter = 'all',
		onStepFilterChange,
		disabled = false
	}: {
		selectedStepFilter?: string;
		onStepFilterChange?: (_filterId: string) => void;
		disabled?: boolean;
	} = $props();

	// Step count filter options
	const stepFilters = [
		{ id: 'all', label: 'All Steps', min: 0, max: Infinity },
		{ id: 'quick', label: 'Quick (1-3)', min: 1, max: 3 },
		{ id: 'short', label: 'Short (4-7)', min: 4, max: 7 },
		{ id: 'medium', label: 'Medium (8-15)', min: 8, max: 15 },
		{ id: 'long', label: 'Long (16+)', min: 16, max: Infinity }
	];

	function handleStepFilterChange(filterId: string): void {
		onStepFilterChange?.(filterId);
	}
</script>

<div class="step-filters">
	<div class="filter-chips">
		{#each stepFilters as filter (filter.id)}
			<button
				type="button"
				class="filter-chip"
				class:active={selectedStepFilter === filter.id}
				onclick={() => handleStepFilterChange(filter.id)}
				{disabled}
				aria-label={`Filter by ${filter.label}`}
			>
				{filter.label}
			</button>
		{/each}
	</div>
</div>

<style>
	.step-filters {
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--color-border);
	}

	.filter-chips {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		overflow-x: auto;
		padding-bottom: 0.25rem;
		scrollbar-width: none;
		-ms-overflow-style: none;
		-webkit-overflow-scrolling: touch;
	}

	.filter-chips::-webkit-scrollbar {
		display: none;
	}

	.filter-chip {
		padding: 0.5rem 1rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 20px;
		cursor: pointer;
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		transition: all 0.2s ease;
		white-space: nowrap;
		flex-shrink: 0;
		min-height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.filter-chip:hover {
		background: var(--color-surface-hover);
		border-color: var(--color-primary);
		color: var(--color-text-primary);
	}

	.filter-chip.active {
		background: var(--color-primary);
		border-color: var(--color-primary);
		color: white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.filter-chip:disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		/* Mobile filter chips - horizontal scroll */
		.filter-chips {
			flex-wrap: nowrap;
			overflow-x: auto;
			padding-right: 1rem;
			margin-right: -1rem;
			scroll-behavior: smooth;
			-webkit-overflow-scrolling: touch;
		}

		.filter-chip {
			font-size: 0.8rem;
			padding: 0.4rem 0.8rem;
			min-height: 40px;
		}
	}
</style>
