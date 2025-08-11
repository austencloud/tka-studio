<script lang="ts">
	import type { FilterType, FilterValue } from '$lib/domain/browse';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		filter = null,
		onBackToFilters = () => {},
	} = $props<{
		filter?: { type: FilterType; value: FilterValue } | null;
		onBackToFilters?: () => void;
	}>();

	// Get filter display text
	function getFilterDisplayText(): string {
		if (!filter) return '';

		const { type, value } = filter;
		switch (type) {
			case 'starting_letter':
				return typeof value === 'string' && value.includes('-')
					? `Letters ${value}`
					: `Letter ${value}`;
			case 'contains_letters':
				return `Contains "${value}"`;
			case 'length':
				return value === 'all' ? 'All Lengths' : `${value} beats`;
			case 'difficulty':
				return value === 'all' ? 'All Levels' : `${value} level`;
			case 'author':
				return value === 'all' ? 'All Authors' : `By ${value}`;
			case 'all_sequences':
				return 'All Sequences';
			case 'favorites':
				return 'Favorites';
			case 'recent':
				return 'Recently Added';
			default:
				return String(value || 'Unknown');
		}
	}

	function handleBackToFilters() {
		onBackToFilters();
	}
</script>

<div class="browser-header">
	<div class="header-left">
		<button class="back-button" onclick={handleBackToFilters} type="button">
			<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
				<path
					d="M12.5 15L7.5 10L12.5 5"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
			Back to Filters
		</button>

		{#if filter}
			<div class="filter-info">
				<span class="filter-type">{filter.type.replace('_', ' ')}</span>
				<span class="filter-value">{getFilterDisplayText()}</span>
			</div>
		{/if}
	</div>
</div>

<style>
	.browser-header {
		flex-shrink: 0;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-lg);
		background: rgba(255, 255, 255, 0.05);
		border-bottom: var(--glass-border);
		backdrop-filter: var(--glass-backdrop);
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
	}

	.back-button {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 255, 255, 0.1);
		border: var(--glass-border);
		border-radius: 8px;
		color: var(--foreground);
		font-family: inherit;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.back-button:hover {
		background: rgba(255, 255, 255, 0.15);
		border-color: var(--primary-color);
		color: var(--primary-color);
	}

	.filter-info {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(99, 102, 241, 0.1);
		border: 1px solid rgba(99, 102, 241, 0.3);
		border-radius: 20px;
		font-size: var(--font-size-sm);
	}

	.filter-type {
		color: var(--primary-color);
		font-weight: 500;
		text-transform: capitalize;
	}

	.filter-value {
		color: var(--foreground);
		font-weight: 600;
	}
</style>
