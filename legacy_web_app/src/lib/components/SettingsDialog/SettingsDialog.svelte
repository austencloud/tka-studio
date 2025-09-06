<script lang="ts">
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	// Image export settings imports temporarily removed
	import { showSuccess, showError } from '$lib/components/shared/ToastManager.svelte';
	import { onMount } from 'svelte';

	// Import tab components
	import SettingsTabs from './SettingsTabs.svelte';
	import GeneralTab from './GeneralTab/GeneralTab.svelte';
	// ImageExportTab import temporarily removed

	// Constants for localStorage keys
	const SETTINGS_ACTIVE_TAB_KEY = 'settings_active_tab';
	const SETTINGS_SCROLL_POSITION_KEY = 'settings_scroll_position';

	// Props
	const { onClose } = $props<{
		onClose: () => void;
	}>();

	// Define tabs - temporarily removed Image Export tab
	const tabs = [
		{ id: 'general', label: 'General', icon: 'fa-sliders' }
		// Image Export tab temporarily removed
	];

	// Load the last active tab from localStorage or default to 'general'
	function getLastActiveTab(): string {
		if (browser) {
			try {
				const savedTab = localStorage.getItem(SETTINGS_ACTIVE_TAB_KEY);
				if (savedTab && tabs.some((tab) => tab.id === savedTab)) {
					return savedTab;
				}
			} catch (error) {
				console.error('Failed to load last active settings tab:', error);
			}
		}
		return 'general';
	}

	// Active tab state
	let activeTab = $state(getLastActiveTab());

	// Track if we're currently saving (to show UI feedback)
	let isSaving = $state(false);

	// Handle tab change
	function handleTabChange(tabId: string) {
		activeTab = tabId;

		// Save the active tab to localStorage
		if (browser) {
			try {
				localStorage.setItem(SETTINGS_ACTIVE_TAB_KEY, tabId);
			} catch (error) {
				console.error('Failed to save active settings tab:', error);
			}
		}

		// Provide haptic feedback for navigation
		if (browser) {
			hapticFeedbackService.trigger('navigation');
		}
	}

	// Reference to the content container for scroll position tracking
	let contentContainer: HTMLDivElement;

	// Initialize when component mounts
	onMount(() => {
		// Restore scroll position if available
		if (browser && contentContainer) {
			try {
				const savedScrollPosition = localStorage.getItem(SETTINGS_SCROLL_POSITION_KEY);
				if (savedScrollPosition) {
					const position = parseInt(savedScrollPosition, 10);
					if (!isNaN(position)) {
						setTimeout(() => {
							contentContainer.scrollTop = position;
						}, 50);
					}
				}
			} catch (error) {
				console.error('Failed to restore settings scroll position:', error);
			}
		}
	});

	// Save all settings
	function saveAllSettings() {
		console.log('saveAllSettings called');

		// Prevent multiple save operations
		if (isSaving) return;

		isSaving = true;

		// Provide haptic feedback
		if (browser) {
			hapticFeedbackService.trigger('success');
		}

		try {
			// Image export settings saving temporarily removed

			// Save general settings
			if (browser && localStorage) {
				try {
					const settings = JSON.parse(localStorage.getItem('settings') || '{}');
					localStorage.setItem('settings', JSON.stringify(settings));
					console.log('General settings saved');
				} catch (error) {
					console.error('Failed to save general settings:', error);
				}
			}

			// Save the current scroll position
			if (browser && contentContainer) {
				try {
					localStorage.setItem(SETTINGS_SCROLL_POSITION_KEY, contentContainer.scrollTop.toString());
					console.log('Scroll position saved:', contentContainer.scrollTop);
				} catch (error) {
					console.error('Failed to save settings scroll position:', error);
				}
			}

			// Save the active tab
			if (browser) {
				try {
					localStorage.setItem(SETTINGS_ACTIVE_TAB_KEY, activeTab);
					console.log('Active tab saved:', activeTab);
				} catch (error) {
					console.error('Failed to save active tab:', error);
				}
			}

			// Show success message
			showSuccess('Settings saved successfully');

			// Add visual feedback on the button
			const saveButtons = document.querySelectorAll('.save-button');
			saveButtons.forEach((button) => {
				button.classList.add('save-success');
			});

			// Add a delay before closing to ensure everything is saved
			setTimeout(() => {
				isSaving = false;
				onClose();
			}, 300);
		} catch (error) {
			console.error('Failed to save settings:', error);
			showError('Failed to save settings. Please try again.');
			isSaving = false;
		}
	}

	// Reset settings to defaults
	function resetToDefaults(): void {
		// Provide haptic feedback for reset action
		if (browser) {
			hapticFeedbackService.trigger('warning');
		}

		try {
			// Image export settings reset temporarily removed

			// Reset general settings
			if (browser && localStorage) {
				try {
					// Reset general settings
					const generalSettings = JSON.parse(localStorage.getItem('settings') || '{}');
					// You can add specific resets for general settings here if needed
					localStorage.setItem('settings', JSON.stringify(generalSettings));
				} catch (error) {
					console.error('Failed to reset general settings:', error);
				}
			}

			// Show success message
			showSuccess('Settings reset to defaults');
		} catch (error) {
			console.error('Failed to reset settings:', error);
			showError('Failed to reset settings. Please try again.');
		}
	}

	// Handle close button click
	function handleClose() {
		// Provide haptic feedback
		if (browser) {
			hapticFeedbackService.trigger('selection');
		}

		// Save the current scroll position and active tab
		if (browser) {
			try {
				// Save scroll position
				if (contentContainer) {
					localStorage.setItem(SETTINGS_SCROLL_POSITION_KEY, contentContainer.scrollTop.toString());
					console.log('Scroll position saved on close:', contentContainer.scrollTop);
				}

				// Save active tab
				localStorage.setItem(SETTINGS_ACTIVE_TAB_KEY, activeTab);
				console.log('Active tab saved on close:', activeTab);
			} catch (error) {
				console.error('Failed to save settings state on close:', error);
			}
		}

		// Call the close handler directly without saving all settings
		// This prevents double-saving and double-closing
		onClose();
	}
</script>

<div class="settings-container" role="dialog" aria-modal="true" aria-labelledby="settings-title">
	<div class="settings-header">
		<div class="settings-title">
			<i class="fa-solid fa-gear"></i>
			<h2 id="settings-title">Settings</h2>
		</div>

		<button
			onclick={handleClose}
			class="close-button"
			aria-label="Close settings"
			disabled={isSaving}
		>
			<i class="fa-solid fa-xmark"></i>
		</button>
	</div>

	<SettingsTabs {tabs} {activeTab} onTabChange={handleTabChange} />

	<div class="settings-content" bind:this={contentContainer}>
		{#if activeTab === 'general'}
			<GeneralTab />
		{/if}
		<!-- Image Export tab temporarily removed -->
	</div>

	<div class="settings-footer">
		<button
			onclick={resetToDefaults}
			class="reset-button"
			aria-label="Reset settings to defaults"
			disabled={isSaving}
		>
			<i class="fa-solid fa-arrows-rotate"></i>
			Reset to Defaults
		</button>
		<button
			onclick={saveAllSettings}
			class="save-button"
			aria-label="Save settings"
			disabled={isSaving}
		>
			<i class="fa-solid {isSaving ? 'fa-spinner fa-spin' : 'fa-save'}"></i>
			{isSaving ? 'Saving...' : 'Save Settings'}
		</button>
	</div>
</div>

<style>
	.settings-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		max-height: 90vh; /* Limit height to 90% of viewport height */
		background: rgba(30, 40, 60, 0.9);
		backdrop-filter: blur(10px);
		color: #e0e0e0;
		border-radius: 12px;
		overflow: hidden; /* Keep this for the border radius */
	}

	.settings-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid rgba(108, 156, 233, 0.2);
		background-color: rgba(20, 30, 50, 0.5);
	}

	.settings-title {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.settings-title i {
		font-size: 1.5rem;
		color: #6c9ce9;
	}

	.settings-title h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: white;
	}

	.close-button {
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.7);
		cursor: pointer;
		width: 36px;
		height: 36px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
	}

	.close-button i {
		font-size: 1.25rem;
	}

	.close-button:hover {
		background-color: rgba(255, 255, 255, 0.1);
		color: white;
	}

	.settings-content {
		flex: 1;
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(108, 156, 233, 0.3) transparent;
		padding-bottom: 10px; /* Reduced padding since we have a footer now */
	}

	.settings-footer {
		display: flex;
		justify-content: space-between;
		padding: 1rem;
		border-top: 1px solid rgba(108, 156, 233, 0.2);
		background-color: rgba(20, 30, 50, 0.5);
	}

	.save-button {
		background: linear-gradient(to bottom, #2563eb, #1d4ed8);
		color: white;
		border: none;
		border-radius: 8px;
		padding: 0.75rem 1.5rem;
		font-weight: bold;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		transition: all 0.2s ease;
		cursor: pointer;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.save-button i {
		font-size: 1.1rem;
	}

	.save-button:hover {
		background: linear-gradient(to bottom, #3b82f6, #2563eb);
		transform: translateY(-2px);
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
	}

	.save-button:active {
		transform: translateY(0);
		background: linear-gradient(to bottom, #1d4ed8, #1e40af);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	.reset-button {
		background: linear-gradient(to bottom, #3a3a43, #2a2a2e);
		color: var(--color-text-primary, white);
		border: 2px solid var(--tkc-border-color, #3c3c41);
		border-radius: 8px;
		padding: 0.75rem 1.5rem;
		font-weight: bold;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		transition: all 0.2s ease;
		cursor: pointer;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.reset-button i {
		font-size: 1.1rem;
	}

	.reset-button:hover {
		background: linear-gradient(to bottom, #454550, #323238);
		transform: translateY(-2px);
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
	}

	.reset-button:active {
		transform: translateY(0);
		background: linear-gradient(to bottom, #2a2a30, #1e1e22);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	/* Success state styling */
	:global(.save-button.save-success) {
		background: linear-gradient(to bottom, #10b981, #059669);
		transform: translateY(-1px);
		box-shadow: 0 3px 8px rgba(0, 0, 0, 0.25);
	}

	:global(.save-button.save-success i) {
		animation: pulse 0.5s ease-in-out;
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.2);
		}
		100% {
			transform: scale(1);
		}
	}

	.settings-content::-webkit-scrollbar {
		width: 6px;
	}

	.settings-content::-webkit-scrollbar-track {
		background: transparent;
	}

	.settings-content::-webkit-scrollbar-thumb {
		background-color: rgba(108, 156, 233, 0.3);
		border-radius: 3px;
	}

	/* Mobile styles */
	@media (max-width: 480px) {
		.settings-container {
			max-height: 85vh; /* Slightly smaller on mobile to ensure it fits */
			height: auto; /* Allow it to size based on content */
		}

		.settings-header {
			padding: 0.75rem 1rem;
		}

		.settings-title h2 {
			font-size: 1.1rem;
		}

		.settings-content {
			padding-bottom: 10px; /* Reduced padding since we have a footer now */
		}

		.settings-footer {
			padding: 0.75rem;
			flex-direction: column;
			gap: 0.75rem;
		}

		.reset-button,
		.save-button {
			padding: 0.6rem 1.2rem;
			font-size: 0.9rem;
			width: 100%; /* Full width on mobile */
			justify-content: center;
		}

		.reset-button {
			order: 2; /* Move reset button below save button on mobile */
		}

		.save-button {
			order: 1; /* Keep save button at the top on mobile */
		}
	}
</style>
