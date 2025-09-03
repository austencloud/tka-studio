<script lang="ts">
	import { settingsStore } from '$lib/state/stores/settings/settings.store';
	import { userContainer } from '$lib/state/stores/user/UserContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { uiStore } from '$lib/components/WriteTab/stores/uiStore';
	import {
		getImageExportSettings,
		updateImageExportSettings
	} from '$lib/state/image-export-settings.svelte';

	// Get current settings
	const settings = $derived(settingsStore.getSnapshot());
	const user = useContainer(userContainer);
	let username = $state(user.currentUser || 'User');

	// Get UI preferences
	let confirmDeletions = $state(true);
	let rememberLastSaveDirectory = $state(true);

	// Initialize state from stores
	$effect(() => {
		if (browser) {
			// Get confirmation dialog preference
			try {
				const uiState = $uiStore;
				confirmDeletions = uiState.preferences.confirmDeletions;
			} catch (error) {
				console.error('Failed to load confirmation dialog preference:', error);
			}

			// Get remember save location preference
			try {
				const exportSettings = getImageExportSettings();
				rememberLastSaveDirectory = exportSettings.rememberLastSaveDirectory;
			} catch (error) {
				console.error('Failed to load remember save location preference:', error);
			}
		}
	});

	// Toggle haptic feedback
	function toggleHapticFeedback() {
		if (browser && settings.hapticFeedback) hapticFeedbackService.trigger('selection');
		settingsStore.setHapticFeedback(!settings.hapticFeedback);
	}

	// Toggle confirmation dialogs
	function toggleConfirmDeletions() {
		if (browser) hapticFeedbackService.trigger('selection');

		// Toggle the state
		confirmDeletions = !confirmDeletions;

		// Update the store
		uiStore.toggleConfirmDeletions(confirmDeletions);
	}

	// Toggle remember save location
	function toggleRememberSaveLocation() {
		if (browser) hapticFeedbackService.trigger('selection');

		// Toggle the state
		rememberLastSaveDirectory = !rememberLastSaveDirectory;

		// Update image export settings
		const exportSettings = getImageExportSettings();
		exportSettings.rememberLastSaveDirectory = rememberLastSaveDirectory;
		updateImageExportSettings(exportSettings);

		// Log for debugging
		console.log('Remember save location toggled:', rememberLastSaveDirectory);
	}

	// Update username
	function updateUsername(event: Event) {
		const input = event.target as HTMLInputElement;
		const newUsername = input.value.trim();

		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		if (newUsername) {
			userContainer.setUsername(newUsername);
			username = newUsername;
		} else {
			userContainer.setUsername('User');
			username = 'User';
			input.value = 'User';
		}
	}
</script>

<div class="general-tab">
	<div class="settings-section">
		<h3>User Settings</h3>
		<div class="setting-item">
			<div class="setting-info">
				<span class="setting-label">Username</span>
				<span class="setting-description">Your name for exported sequences</span>
			</div>
			<div class="setting-control username-control">
				<input
					type="text"
					value={username}
					onchange={updateUsername}
					onblur={updateUsername}
					placeholder="Enter your name"
					aria-label="Username"
					class="username-input"
					maxlength="50"
				/>
			</div>
		</div>
	</div>

	<div class="settings-section">
		<h3>Preferences</h3>

		<div class="setting-item">
			<div class="setting-info">
				<span class="setting-label">Haptic Feedback</span>
				<span class="setting-description">Vibration feedback for touch interactions</span>
			</div>
			<div class="setting-control">
				<label class="switch">
					<input
						type="checkbox"
						checked={settings.hapticFeedback}
						onchange={toggleHapticFeedback}
						aria-label="Toggle haptic feedback"
						disabled={!hapticFeedbackService.isHapticFeedbackSupported()}
					/>
					<span class="slider round"></span>
				</label>
			</div>
		</div>

		<div class="setting-item">
			<div class="setting-info">
				<span class="setting-label">Confirmation Dialogs</span>
				<span class="setting-description"
					>Show confirmation when clearing sequences or deleting beats</span
				>
			</div>
			<div class="setting-control">
				<label class="switch">
					<input
						type="checkbox"
						checked={confirmDeletions}
						onchange={toggleConfirmDeletions}
						aria-label="Toggle confirmation dialogs"
					/>
					<span class="slider round"></span>
				</label>
			</div>
		</div>

		<div class="setting-item">
			<div class="setting-info">
				<span class="setting-label">Remember Save Location</span>
				<span class="setting-description">Remember last directory used for image exports</span>
			</div>
			<div class="setting-control">
				<label class="switch">
					<input
						type="checkbox"
						checked={rememberLastSaveDirectory}
						onchange={toggleRememberSaveLocation}
						aria-label="Toggle remember save location"
					/>
					<span class="slider round"></span>
				</label>
			</div>
		</div>
	</div>
</div>

<style>
	.general-tab {
		padding: 1rem;
		overflow-y: auto;
		max-height: 60vh;
		width: 100%;
		box-sizing: border-box;
	}

	.settings-section {
		margin-bottom: 1.5rem;
	}

	.settings-section h3 {
		margin: 0 0 1rem 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
		border-bottom: 1px solid rgba(108, 156, 233, 0.3);
		padding-bottom: 0.5rem;
	}

	.setting-item {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		padding: 0.75rem 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.setting-info {
		flex: 1;
		min-width: 0;
	}

	.setting-label {
		display: block;
		font-weight: 500;
		margin-bottom: 0.25rem;
		color: var(--color-text-primary, white);
	}

	.setting-description {
		display: block;
		font-size: 0.85rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		overflow-wrap: break-word;
	}

	.setting-control {
		margin-left: 0.5rem;
	}

	.switch {
		position: relative;
		display: inline-block;
		width: 50px;
		height: 24px;
		flex-shrink: 0;
	}

	.switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.slider {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: #ccc;
		transition: 0.3s;
	}

	.slider:before {
		position: absolute;
		content: '';
		height: 18px;
		width: 18px;
		left: 3px;
		bottom: 3px;
		background-color: white;
		transition: 0.3s;
	}

	input:checked + .slider {
		background-color: #4361ee;
	}

	input:focus + .slider {
		box-shadow: 0 0 1px #4361ee;
	}

	input:checked + .slider:before {
		transform: translateX(26px);
	}

	.slider.round {
		border-radius: 24px;
	}

	.slider.round:before {
		border-radius: 50%;
	}

	.username-control {
		flex: 1;
		max-width: 200px;
		min-width: 120px;
	}

	.username-input {
		width: 100%;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		background: linear-gradient(to bottom, #1f1f24, #2a2a30);
		border: 1px solid rgba(108, 156, 233, 0.3);
		color: var(--color-text-primary, white);
		font-size: 0.95rem;
		transition: all 0.2s ease;
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
		box-sizing: border-box;
	}

	.username-input:focus {
		border-color: #167bf4;
		box-shadow: 0 0 0 2px rgba(22, 123, 244, 0.3);
		outline: none;
	}
</style>
