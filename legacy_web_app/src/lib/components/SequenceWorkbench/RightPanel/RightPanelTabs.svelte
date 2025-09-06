<!-- src/lib/components/SequenceWorkbench/RightPanel/RightPanelTabs.svelte -->
<script lang="ts">
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Props using Svelte 5 runes
	const props = $props<{
		activeTab: 'construct' | 'generate';
		onTabChange: (tab: 'construct' | 'generate') => void;
		isGenerateMode?: boolean;
	}>();

	// Tab definitions
	const tabs = [
		{ id: 'construct', label: 'Construct', icon: '⚒️' },
		{ id: 'generate', label: 'Generate', icon: '🤖' }
	];

	// Handle tab click
	function handleTabClick(tabId: 'construct' | 'generate') {
		// Only allow tab changes if not in generate mode from the main tab
		if (tabId !== props.activeTab && !props.isGenerateMode) {
			// Provide subtle navigation haptic feedback
			if (browser) {
				hapticFeedbackService.trigger('navigation');
			}

			props.onTabChange(tabId);
		}
	}
</script>

<div class="tabs-container">
	{#each tabs as tab}
		<button
			class="tab-button"
			class:active={props.activeTab === tab.id}
			class:disabled={props.isGenerateMode && tab.id !== 'generate'}
			onclick={() => handleTabClick(tab.id as 'construct' | 'generate')}
			aria-selected={props.activeTab === tab.id}
			aria-disabled={props.isGenerateMode && tab.id !== 'generate'}
			role="tab"
		>
			<span class="tab-icon">{tab.icon}</span>
			<span class="tab-label">{tab.label}</span>
		</button>
	{/each}
</div>

<style>
	.tabs-container {
		display: flex;
		background: var(--color-surface-900, rgba(15, 25, 40, 0.7));
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		padding: 0.5rem 0.5rem 0;
	}

	.tab-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1rem;
		background: transparent;
		border: none;
		border-radius: 0.5rem 0.5rem 0 0;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
		position: relative;
		flex: 1;
		justify-content: center;
	}

	.tab-button:hover {
		color: var(--color-text-primary, white);
		background: rgba(255, 255, 255, 0.05);
	}

	.tab-button.active {
		color: var(--color-text-primary, white);
		background: var(--color-surface-800, rgba(20, 30, 50, 0.5));
	}

	.tab-button.disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.tab-button.active::after {
		content: '';
		position: absolute;
		bottom: -1px;
		left: 0;
		right: 0;
		height: 1px;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.5));
	}

	.tab-icon {
		font-size: 1.2rem;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.tab-label {
			font-size: 0.9rem;
		}
	}

	@media (max-width: 480px) {
		.tab-button {
			padding: 0.5rem;
		}
	}
</style>
