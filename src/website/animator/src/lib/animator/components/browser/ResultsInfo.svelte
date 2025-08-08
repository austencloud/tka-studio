<script lang="ts">
	// Props
	let {
		itemCount = 0,
		searchQuery = '',
		selectedCategory = 'All'
	}: {
		itemCount?: number;
		searchQuery?: string;
		selectedCategory?: string;
	} = $props();

	// Computed values
	const isFiltered = $derived(searchQuery || selectedCategory !== 'All');
	const resultText = $derived(isFiltered ? 'found' : 'available');
	const pluralSuffix = $derived(itemCount !== 1 ? 's' : '');
</script>

<div class="results-info">
	<span class="results-count">
		{itemCount} sequence{pluralSuffix}
		{resultText}
	</span>
</div>

<style>
	.results-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
		padding: 0 0.5rem;
	}

	.results-count {
		color: var(--color-text-secondary, #666);
		font-size: 0.9rem;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.results-info {
			margin-bottom: 1rem;
			padding: 0 0.5rem;
		}

		.results-count {
			font-size: 0.85rem;
		}
	}
</style>
