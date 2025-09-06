<script lang="ts">
	import { getContext, createEventDispatcher } from 'svelte'; // Import createEventDispatcher
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../layoutContext';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// --- Props ---
	export let categoryKeys: string[] = [];
	export let selectedTab: string | null = null;
	// REMOVED: export let onTabSelect: (tab: string) => void; // No longer needed as prop

	// --- Context ---
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);

	// --- Events ---
	const dispatch = createEventDispatcher<{ tabSelect: string }>(); // Dispatcher for tab selection

	// --- Event Handler ---
	function handleTabClick(categoryKey: string) {
		// Provide haptic feedback for tab navigation
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('navigation');
		}

		// Dispatch the event instead of calling a prop function
		dispatch('tabSelect', categoryKey);
	}

	// Helper to format the display name for tabs
	function formatTabName(key: string): string {
		return key.charAt(0).toUpperCase() + key.slice(1);
	}
</script>

<div>
	<div class="tabs" role="tablist" aria-label="Option Categories">
		{#if categoryKeys.length > 0}
			{#each categoryKeys as categoryKey (categoryKey)}
				<button
					class="tab"
					class:active={selectedTab === categoryKey}
					on:click={() => handleTabClick(categoryKey)}
					role="tab"
					aria-selected={selectedTab === categoryKey}
					aria-controls={`options-panel-${categoryKey}`}
					id="tab-{categoryKey}"
				>
					{formatTabName(categoryKey)}
				</button>
			{/each}
		{:else}
			<span class="no-categories-message">No sub-categories</span>
		{/if}
	</div>
</div>

<style>
	/* Styles remain the same */
	.tabs {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
		gap: 4px 8px;
		padding: 0;
		margin: 0;
		max-width: 100%;
	}
	.tab {
		background: none;
		border: none;
		padding: clamp(0.4rem, 1vw, 0.6rem) clamp(0.8rem, 1.5vw, 1.2rem);
		cursor: pointer;
		font-weight: 500;
		font-size: clamp(0.8rem, 2vw, 0.95rem);
		color: #4b5563;
		border-bottom: 3px solid transparent;
		transition:
			border-color 0.2s ease-in-out,
			color 0.2s ease-in-out,
			background-color 0.15s ease;
		white-space: nowrap;
		flex-shrink: 0;
		border-radius: 4px 4px 0 0;
		margin-bottom: 2px;
	}
	.tab.active {
		border-color: #3b82f6;
		color: #1e40af;
		font-weight: 600;
	}
	.tab:hover:not(.active) {
		color: #1f2937;
		background-color: #f3f4f6;
		border-color: #d1d5db;
	}
	.tab:focus-visible {
		outline: 2px solid #60a5fa;
		outline-offset: 1px;
		background-color: rgba(59, 130, 246, 0.1);
	}
	.no-categories-message {
		color: #6b7280;
		font-style: italic;
		padding: clamp(0.4rem, 1vw, 0.6rem) clamp(0.8rem, 1.5vw, 1.2rem);
		white-space: nowrap;
	}
</style>
