<!-- src/lib/components/SettingsDialog/ImageExportTab/ImageExportTab.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import {
		getImageExportSettings,
		updateImageExportSettings,
		saveImageExportSettings,
		type ImageExportSettings
	} from '$lib/state/image-export-settings.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Import components
	import ImageExportControlPanel from './ImageExportControlPanel.svelte';
	import ImageExportPreviewPanel from './ImageExportPreviewPanel.svelte';

	// Local state to hold the current settings
	let settings = $state<ImageExportSettings>(getImageExportSettings());

	// Initialize when component mounts
	onMount(() => {
		// Load the current settings
		settings = getImageExportSettings();

		// Debug check - directly inspect localStorage
		if (browser) {
			try {
				const savedSettings = localStorage.getItem('image-export-settings');
				if (savedSettings) {
					const parsed = JSON.parse(savedSettings);
					console.log('ImageExportTab: Direct localStorage check on mount:', {
						rememberLastSaveDirectory: parsed.rememberLastSaveDirectory,
						type: typeof parsed.rememberLastSaveDirectory
					});
				}
			} catch (error) {
				console.error('ImageExportTab: Error checking localStorage:', error);
			}
		}
	});

	// Handle setting change
	function handleSettingChange(key: keyof ImageExportSettings, value: any): void {
		// Log the setting change
		console.log(`ImageExportTab: Setting change: ${key}`, {
			oldValue: settings[key],
			newValue: value,
			key
		});

		// Create a new settings object with the updated value
		// Use a clean copy to avoid issues with Svelte 5 runes proxy objects
		const newSettings = getImageExportSettings();

		// Update the specific property
		(newSettings as any)[key] = value;

		// Special handling for rememberLastSaveDirectory
		if (key === 'rememberLastSaveDirectory') {
			// Force strict boolean conversion
			newSettings.rememberLastSaveDirectory = value === true;

			// Provide haptic feedback
			if (browser && hapticFeedbackService.isAvailable()) {
				hapticFeedbackService.trigger('selection');
			}

			console.log(
				'ImageExportTab: Explicitly set rememberLastSaveDirectory to:',
				newSettings.rememberLastSaveDirectory,
				'type:',
				typeof newSettings.rememberLastSaveDirectory
			);
		}

		// Update local state
		settings = newSettings;

		// Update the global state and save to localStorage
		updateImageExportSettings(newSettings);

		// Force an immediate save to localStorage
		saveImageExportSettings();

		// Verify the change was applied
		console.log(`ImageExportTab: Setting after change: ${key}`, {
			currentValue: settings[key],
			expectedValue: value,
			match: settings[key] === value
		});

		// Add logging for rememberLastSaveDirectory
		if (key === 'rememberLastSaveDirectory') {
			// Directly check localStorage again to verify changes were saved
			if (browser) {
				try {
					// Add a slight delay to ensure saving has completed
					setTimeout(() => {
						const savedSettings = localStorage.getItem('image-export-settings');
						if (savedSettings) {
							const parsed = JSON.parse(savedSettings);
							console.log('ImageExportTab: LocalStorage after change:', {
								rememberLastSaveDirectory: parsed.rememberLastSaveDirectory,
								type: typeof parsed.rememberLastSaveDirectory,
								expected: value === true
							});
						}
					}, 50);
				} catch (error) {
					console.error('ImageExportTab: Error checking localStorage after change:', error);
				}
			}
		}
	}
</script>

<div class="image-export-tab">
	<h2>Image Export Settings</h2>

	<div class="split-panel">
		<!-- Control panel -->
		<div class="control-panel-container">
			<ImageExportControlPanel {settings} onSettingChange={handleSettingChange} />
		</div>

		<!-- Preview panel -->
		<div class="preview-panel-container">
			<h3>Export Preview</h3>
			<ImageExportPreviewPanel {settings} />
		</div>
	</div>
</div>

<style>
	.image-export-tab {
		padding: 1rem;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	h2 {
		margin-bottom: 1.5rem;
		color: var(--color-text-primary, white);
		font-size: 1.6rem;
		font-weight: 600;
	}

	h3 {
		margin: 0 0 1rem 0;
		font-size: 1.2rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		border-bottom: 1px solid rgba(108, 156, 233, 0.3);
		padding-bottom: 0.5rem;
	}

	.split-panel {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		flex: 1;
		min-height: 0;
	}

	.control-panel-container {
		display: flex;
		flex-direction: column;
		background: rgba(10, 10, 12, 0.2);
		border-radius: 8px;
		padding: 1rem;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		overflow-y: visible;
	}

	.preview-panel-container {
		display: flex;
		flex-direction: column;
		overflow: hidden;
		background: rgba(10, 10, 12, 0.2);
		border-radius: 8px;
		padding: 1rem;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		width: 100%;
		min-height: 100px;
	}

	/* Custom scrollbar styling */
	.control-panel-container::-webkit-scrollbar {
		width: 8px;
	}

	.control-panel-container::-webkit-scrollbar-track {
		background: rgba(20, 20, 25, 0.3);
		border-radius: 4px;
	}

	.control-panel-container::-webkit-scrollbar-thumb {
		background: rgba(108, 156, 233, 0.3);
		border-radius: 4px;
	}

	.control-panel-container::-webkit-scrollbar-thumb:hover {
		background: rgba(108, 156, 233, 0.5);
	}

	/* Responsive styles */
	@media (max-width: 1024px) {
		h2 {
			margin-bottom: 1rem;
			font-size: 1.4rem;
		}

		h3 {
			margin-bottom: 0.75rem;
			font-size: 1.1rem;
		}
	}

	@media (max-width: 768px) {
		.image-export-tab {
			padding: 0.75rem;
		}

		.split-panel {
			gap: 1rem;
		}
	}

	@media (max-width: 480px) {
		.preview-panel-container {
			padding: 0.75rem;
		}

		.image-export-tab {
			padding: 0.5rem;
		}

		.control-panel-container {
			padding: 0.75rem;
		}

		.split-panel {
			gap: 0.75rem;
		}

		h2 {
			font-size: 1.3rem;
			margin-bottom: 0.75rem;
		}

		h3 {
			font-size: 1rem;
			margin-bottom: 0.5rem;
		}
	}
</style>
