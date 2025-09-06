<script lang="ts">
	// Tab interface for settings dialog
	import { fade } from 'svelte/transition';
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Define tab types
	export type SettingsTab = {
		id: string;
		label: string;
		icon: string;
	};

	// Props
	const { tabs, activeTab = '', onTabChange } = $props<{
		tabs: SettingsTab[];
		activeTab: string;
		onTabChange: (tabId: string) => void;
	}>();

	// Handle tab click
	function handleTabClick(tabId: string) {
		if (tabId !== activeTab) {
			// Provide haptic feedback for tab navigation
			if (browser) {
				hapticFeedbackService.trigger('navigation');
			}

			// Call the tab change handler
			onTabChange(tabId);
		}
	}
</script>

<div class="settings-tabs">
	<div class="tabs-container">
		{#each tabs as tab (tab.id)}
			<button
				class="tab-button"
				class:active={activeTab === tab.id}
				onclick={() => handleTabClick(tab.id)}
				aria-selected={activeTab === tab.id}
				role="tab"
				id={`tab-${tab.id}`}
				aria-controls={`panel-${tab.id}`}
			>
				<i class={`fa-solid ${tab.icon}`} aria-hidden="true"></i>
				<span class="tab-label">{tab.label}</span>
			</button>
		{/each}
	</div>
</div>

<style>
	.settings-tabs {
		width: 100%;
		border-bottom: 1px solid rgba(108, 156, 233, 0.2);
		background-color: rgba(20, 30, 50, 0.5);
	}

	.tabs-container {
		display: flex;
		overflow-x: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(108, 156, 233, 0.3) transparent;
		padding: 0 0.5rem;
	}

	.tabs-container::-webkit-scrollbar {
		height: 4px;
	}

	.tabs-container::-webkit-scrollbar-track {
		background: transparent;
	}

	.tabs-container::-webkit-scrollbar-thumb {
		background-color: rgba(108, 156, 233, 0.3);
		border-radius: 2px;
	}

	.tab-button {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.75rem 1.25rem;
		background: transparent;
		border: none;
		border-bottom: 2px solid transparent;
		color: rgba(255, 255, 255, 0.7);
		font-weight: 500;
		transition: all 0.2s ease;
		cursor: pointer;
		white-space: nowrap;
		gap: 0.5rem;
		min-width: 100px;
	}

	.tab-button:hover {
		color: white;
		background-color: rgba(108, 156, 233, 0.1);
	}

	.tab-button.active {
		color: #6c9ce9;
		border-bottom: 2px solid #6c9ce9;
		background-color: rgba(108, 156, 233, 0.15);
	}

	.tab-label {
		font-size: 0.9rem;
	}

	/* Mobile styles */
	@media (max-width: 480px) {
		.tab-button {
			padding: 0.75rem 1rem;
			min-width: 80px;
		}
	}
</style>
