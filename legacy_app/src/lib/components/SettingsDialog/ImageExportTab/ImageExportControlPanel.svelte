<!-- src/lib/components/SettingsDialog/ImageExportTab/ImageExportControlPanel.svelte -->
<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { saveImageExportSettings } from '$lib/state/image-export-settings.svelte';
	import type { ImageExportSettings } from '$lib/state/image-export-settings.svelte';
	import { userContainer } from '$lib/state/stores/user/UserContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import { isMobileDevice as checkMobileDevice } from '$lib/utils/fileSystemUtils';
	import ImageExportToggleButton from './ImageExportToggleButton.svelte';

	// Props
	const { settings, onSettingChange } = $props<{
		settings: ImageExportSettings;
		onSettingChange: (key: keyof ImageExportSettings, value: any) => void;
	}>();

	// Local state
	let isMobileDevice = $state(false);

	// Use the user container with Svelte 5 runes
	const user = useContainer(userContainer);

	// Button settings configuration
	const buttonSettings = [
		// Start position is now always included
		{
			label: 'User Info',
			key: 'addUserInfo',
			tooltip: 'Include user info (name, note, date) in the exported image'
		},
		{ label: 'Word', key: 'addWord', tooltip: 'Add the sequence word as a title' },
		{
			label: 'Difficulty Level',
			key: 'addDifficultyLevel',
			tooltip: 'Add difficulty indicator in the top-left corner'
		},
		{
			label: 'Beat Numbers',
			key: 'addBeatNumbers',
			tooltip: 'Show beat numbers on each pictograph'
		},
		{
			label: 'Reversal Symbols',
			key: 'addReversalSymbols',
			tooltip: 'Show prop reversal indicators'
		}
	] as const;

	// Initialize on mount
	onMount(() => {
		if (browser) {
			try {
				// Detect if we're on a mobile device
				isMobileDevice = checkMobileDevice();

				console.log('Device detection:', { isMobileDevice });

				// Get current user from container
				const currentUser = user.currentUser;

				// Set the current user as the userName if available
				if (currentUser && currentUser.trim() !== '') {
					onSettingChange('userName', currentUser);
				}
			} catch (error) {
				console.error('Failed to initialize:', error);
			}
		}
	});

	// Handle toggle button click
	function handleToggle(key: keyof ImageExportSettings) {
		const newValue = !settings[key];

		// Provide haptic feedback
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		console.log(`Toggle ${key}:`, {
			currentValue: settings[key],
			newValue: newValue,
			type: typeof newValue
		});

		// For rememberLastSaveDirectory, ensure strict boolean conversion
		if (key === 'rememberLastSaveDirectory') {
			onSettingChange(key, newValue === true);
		} else {
			onSettingChange(key, newValue);
		}

		// Force save after toggle
		setTimeout(() => {
			saveImageExportSettings();
		}, 50);
	}

	// Handle custom note change
	function handleNoteChange(event: Event) {
		const input = event.target as HTMLInputElement;
		onSettingChange('customNote', input.value);
	}

	// Removed handleRememberDirectoryChange function as it's now in GeneralTab
</script>

<div class="control-panel">
	<div class="panel-section note-section">
		<div class="form-group">
			<label for="custom-note" class="compact-label">Note for exports:</label>
			<textarea
				id="custom-note"
				value={settings.customNote}
				onchange={handleNoteChange}
				placeholder="Enter note to include in exports"
				aria-label="Custom note for exports"
				class="text-area"
				rows="1"
			></textarea>
			<div class="note-info">
				<span class="note-hint">This text will appear in exported images</span>
			</div>
		</div>
	</div>

	<div class="panel-section options-section">
		<h3>Options</h3>

		<div class="options-grid">
			{#each buttonSettings as button}
				<ImageExportToggleButton
					label={button.label}
					settingKey={button.key}
					isActive={settings[button.key]}
					onToggle={handleToggle}
					tooltip={button.tooltip}
				/>
			{/each}
		</div>
	</div>
</div>

<style>
	.control-panel {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		width: 100%;
	}

	.panel-section {
		border-radius: 8px;
		background: rgba(20, 20, 25, 0.3);
		padding: 1rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		margin-bottom: 0.5rem;
	}

	.note-section {
		display: flex;
		flex-direction: column;
	}

	.form-group {
		flex: 1;
		width: 100%;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
		color: var(--color-text-primary, white);
		font-weight: 600;
		font-size: 0.9rem;
	}

	.compact-label {
		margin-bottom: 0.3rem;
		font-size: 0.85rem;
	}

	.text-area {
		width: 100%;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		background: linear-gradient(to bottom, #1f1f24, #2a2a30);
		border: 1px solid rgba(108, 156, 233, 0.3);
		color: var(--color-text-primary, white);
		font-size: 0.95rem;
		transition: all 0.2s ease;
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
		resize: none;
		min-height: 2.5rem;
		font-family: inherit;
		max-width: 100%; /* Ensure it doesn't extend beyond container */
		box-sizing: border-box; /* Include padding and border in width calculation */
	}

	.text-area:focus {
		border-color: #167bf4;
		box-shadow: 0 0 0 2px rgba(22, 123, 244, 0.3);
		outline: none;
		min-height: 4rem; /* Expand when focused */
	}

	.note-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 0.5rem;
		font-size: 0.8rem;
	}

	.note-hint {
		color: rgba(255, 255, 255, 0.5);
		font-style: italic;
	}

	/* Removed toggle switch styles as they're now only in GeneralTab */

	.options-section h3 {
		margin: 0 0 1rem 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		border-bottom: 1px solid rgba(108, 156, 233, 0.3);
		padding-bottom: 0.5rem;
	}

	.options-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		gap: 0.75rem;
		align-content: start;
		margin-top: 1rem;
	}

	/* Responsive styles */
	@media (max-width: 768px) {
		.panel-section {
			padding: 1rem;
		}

		.options-grid {
			width: 100%;
			grid-template-columns: repeat(2, 1fr);
		}

		.note-info {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.5rem;
		}
	}

	@media (max-width: 480px) {
		.panel-section {
			padding: 0.75rem;
		}

		.options-grid {
			grid-template-columns: 1fr;
		}

		.text-area {
			font-size: 0.9rem;
			min-height: 2.2rem;
		}

		.note-hint {
			font-size: 0.75rem;
		}

		.compact-label {
			font-size: 0.8rem;
		}
	}
</style>
