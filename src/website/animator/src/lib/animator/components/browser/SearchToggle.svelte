<script lang="ts">
	// Import Lucide icons
	import Search from 'lucide-svelte/icons/search';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import ChevronUp from 'lucide-svelte/icons/chevron-up';

	// Props
	let {
		isExpanded = false,
		onToggle
	}: {
		isExpanded?: boolean;
		onToggle?: () => void;
	} = $props();

	function handleToggle(): void {
		onToggle?.();
	}
</script>

<div class="search-toggle mobile-only">
	<button
		type="button"
		onclick={handleToggle}
		class="toggle-button"
		aria-label={isExpanded ? 'Collapse search' : 'Expand search'}
	>
		<Search size={16} />
		<span>Search & Filter</span>
		{#if isExpanded}
			<ChevronUp size={16} />
		{:else}
			<ChevronDown size={16} />
		{/if}
	</button>
</div>

<style>
	/* Mobile/Desktop Visibility Classes */
	.mobile-only {
		display: none;
	}

	/* Mobile search toggle */
	.search-toggle {
		margin-bottom: 0.5rem;
	}

	.search-toggle .toggle-button {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.2s ease;
		color: var(--color-text-primary);
		font-weight: 500;
		gap: 0.5rem;
	}

	.search-toggle .toggle-button:hover {
		background: var(--color-surface-hover);
		border-color: var(--color-primary);
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.mobile-only {
			display: block;
		}
	}
</style>
