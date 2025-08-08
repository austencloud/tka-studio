<script lang="ts">
	// Import Lucide icons
	import Search from 'lucide-svelte/icons/search';
	import X from 'lucide-svelte/icons/x';

	// Props
	let {
		searchQuery = '',
		onSearchChange,
		disabled = false
	}: {
		searchQuery: string;
		onSearchChange?: (_query: string) => void;
		disabled?: boolean;
	} = $props();

	// Local state for input handling
	let searchInput = $state(searchQuery);

	// Sync with external searchQuery changes
	$effect(() => {
		searchInput = searchQuery;
	});

	// Debounced search handling
	let searchTimeout: ReturnType<typeof setTimeout> | undefined;

	function handleSearchInput(event: Event): void {
		const target = event.target as HTMLInputElement;
		searchInput = target.value;

		// Clear existing timeout
		if (searchTimeout) {
			clearTimeout(searchTimeout);
		}

		// Debounce search to avoid excessive filtering
		searchTimeout = setTimeout(() => {
			onSearchChange?.(searchInput);
		}, 300);
	}

	function handleClearSearch(): void {
		searchInput = '';
		onSearchChange?.('');
	}
</script>

<div class="search-input-container">
	<div class="search-icon" aria-hidden="true">
		<Search size={16} />
	</div>
	<input
		type="text"
		placeholder="Search sequences by name, author, or word..."
		value={searchInput}
		oninput={handleSearchInput}
		{disabled}
		class="search-input"
		aria-label="Search sequences"
	/>
	{#if searchInput}
		<button
			type="button"
			onclick={handleClearSearch}
			{disabled}
			class="clear-button"
			aria-label="Clear search"
		>
			<X size={14} />
		</button>
	{/if}
</div>

<style>
	.search-input-container {
		position: relative;
		display: flex;
		align-items: center;
	}

	.search-icon {
		position: absolute;
		left: 12px;
		color: var(--color-text-secondary);
		font-size: 1rem;
		pointer-events: none;
		z-index: 1;
	}

	.search-input {
		width: 100%;
		padding: 0.75rem 1rem 0.75rem 2.5rem;
		border: 1px solid var(--color-border);
		border-radius: 6px;
		font-size: 1rem;
		background: var(--color-surface);
		color: var(--color-text-primary);
		transition:
			border-color 0.2s ease,
			box-shadow 0.2s ease,
			background-color 0.3s ease;
	}

	.search-input:focus {
		outline: none;
		border-color: var(--color-primary);
		box-shadow: 0 0 0 3px var(--color-primary-alpha);
	}

	.search-input:disabled {
		background: var(--color-surface-hover);
		color: var(--color-text-secondary);
		cursor: not-allowed;
	}

	.clear-button {
		position: absolute;
		right: 8px;
		background: none;
		border: none;
		color: var(--color-text-secondary);
		cursor: pointer;
		padding: 4px;
		border-radius: 4px;
		font-size: 1rem;
		line-height: 1;
		transition:
			background-color 0.2s ease,
			color 0.2s ease;
	}

	.clear-button:hover:not(:disabled) {
		background: var(--color-surface-hover);
		color: var(--color-text-primary);
	}

	.clear-button:disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.search-input {
			font-size: 16px; /* Prevent zoom on iOS */
		}
	}
</style>
