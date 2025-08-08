<script lang="ts">
	// Props
	let {
		isLoading = false,
		error = '',
		isEmpty = false,
		searchQuery = '',
		selectedCategory = 'All',
		onRetry
	}: {
		isLoading?: boolean;
		error?: string;
		isEmpty?: boolean;
		searchQuery?: string;
		selectedCategory?: string;
		onRetry?: () => void;
	} = $props();

	function handleRetry(): void {
		onRetry?.();
	}
</script>

{#if isLoading}
	<div class="loading-state">
		<div class="spinner" aria-hidden="true"></div>
		<p>Loading sequence library...</p>
	</div>
{:else if error}
	<div class="error-state">
		<div class="error-icon" aria-hidden="true">⚠️</div>
		<h3>Failed to Load Library</h3>
		<p>{error}</p>
		<button type="button" onclick={handleRetry} class="retry-button"> Try Again </button>
	</div>
{:else if isEmpty}
	<div class="empty-state">
		<div class="empty-icon" aria-hidden="true">🔍</div>
		<h3>No Sequences Found</h3>
		<p>
			{searchQuery || selectedCategory !== 'All'
				? 'Try adjusting your search or filter criteria.'
				: 'The sequence library appears to be empty.'}
		</p>
	</div>
{/if}

<style>
	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 3rem 1.5rem;
		text-align: center;
		min-height: 200px;
		flex: 1;
	}

	.spinner {
		width: 40px;
		height: 40px;
		border: 4px solid var(--color-border, #e0e0e0);
		border-top: 4px solid var(--color-primary, #2196f3);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.error-icon,
	.empty-icon {
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	.error-state h3,
	.empty-state h3 {
		margin: 0 0 0.5rem;
		font-size: 1.5rem;
		color: var(--color-text-primary, #333);
	}

	.error-state p,
	.empty-state p {
		margin: 0 0 1.5rem;
		color: var(--color-text-secondary, #666);
		max-width: 400px;
	}

	.retry-button {
		padding: 0.75rem 1.5rem;
		background: var(--color-primary, #2196f3);
		color: white;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.retry-button:hover {
		background: var(--color-primary-dark, #1976d2);
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.loading-state,
		.error-state,
		.empty-state {
			padding: 2rem 1rem;
			min-height: 150px;
		}
	}

	@media (max-width: 480px) {
		.loading-state,
		.error-state,
		.empty-state {
			padding: 1.5rem 1rem;
		}
	}
</style>
