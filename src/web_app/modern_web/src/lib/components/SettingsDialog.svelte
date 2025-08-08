/**
 * Settings Dialog - Pure Svelte 5 implementation
 * 
 * Application settings dialog with reactive state management.
 */

<script lang="ts">
	import type { ISettingsService, AppSettings } from '$services/interfaces';
	import { updateSettings, getSettings } from '$stores/appState.svelte';

	interface Props {
		settingsService: ISettingsService;
		onClose: () => void;
	}

	let { settingsService, onClose }: Props = $props();

	// Local state for form
	let localSettings = $state<AppSettings>({ ...getSettings() });
	let isSaving = $state(false);
	let saveError = $state<string | null>(null);

	// Reset local settings when dialog opens
	$effect(() => {
		localSettings = { ...getSettings() };
	});

	// Handle form submission
	async function handleSave() {
		isSaving = true;
		saveError = null;

		try {
			// Update each changed setting
			const changes = Object.entries(localSettings).filter(
				([key, value]) => getSettings()[key as keyof AppSettings] !== value
			);

			for (const [key, value] of changes) {
				await settingsService.updateSetting(key as keyof AppSettings, value);
			}

			// Update global state
			updateSettings(localSettings);
			
			console.log('Settings saved successfully');
			onClose();
		} catch (error) {
			saveError = error instanceof Error ? error.message : 'Failed to save settings';
			console.error('Failed to save settings:', error);
		} finally {
			isSaving = false;
		}
	}

	// Handle cancel
	function handleCancel() {
		localSettings = { ...getSettings() }; // Reset changes
		onClose();
	}

	// Handle backdrop click
	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			handleCancel();
		}
	}

	// Handle escape key
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			handleCancel();
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

<div
	class="settings-backdrop"
	onclick={handleBackdropClick}
	onkeydown={(e) => e.key === 'Escape' && handleCancel()}
	role="dialog"
	aria-modal="true"
	aria-labelledby="settings-title"
	tabindex="-1"
>
	<div class="settings-dialog glass-surface">
		<header class="dialog-header">
			<h2 id="settings-title">Settings</h2>
			<button class="close-button" onclick={handleCancel} aria-label="Close Settings">
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
					<path d="m18 6-12 12" stroke="currentColor" stroke-width="2"/>
					<path d="m6 6 12 12" stroke="currentColor" stroke-width="2"/>
				</svg>
			</button>
		</header>

		<div class="dialog-content">
			{#if saveError}
				<div class="error-message">
					{saveError}
				</div>
			{/if}

			<div class="settings-form">
				<!-- Theme Setting -->
				<div class="setting-group">
					<label class="setting-label">
						Theme
						<select bind:value={localSettings.theme} class="setting-input">
							<option value="dark">Dark</option>
							<option value="light">Light</option>
						</select>
					</label>
				</div>

				<!-- Grid Mode Setting -->
				<div class="setting-group">
					<label class="setting-label">
						Default Grid Mode
						<select bind:value={localSettings.gridMode} class="setting-input">
							<option value="diamond">Diamond</option>
							<option value="box">Box</option>
						</select>
					</label>
				</div>

				<!-- Beat Numbers Setting -->
				<div class="setting-group">
					<label class="setting-checkbox">
						<input 
							type="checkbox" 
							bind:checked={localSettings.showBeatNumbers}
						/>
						<span class="checkmark"></span>
						Show Beat Numbers
					</label>
				</div>

				<!-- Auto Save Setting -->
				<div class="setting-group">
					<label class="setting-checkbox">
						<input 
							type="checkbox" 
							bind:checked={localSettings.autoSave}
						/>
						<span class="checkmark"></span>
						Auto Save
					</label>
				</div>

				<!-- Export Quality Setting -->
				<div class="setting-group">
					<label class="setting-label">
						Export Quality
						<select bind:value={localSettings.exportQuality} class="setting-input">
							<option value="low">Low</option>
							<option value="medium">Medium</option>
							<option value="high">High</option>
						</select>
					</label>
				</div>
			</div>
		</div>

		<footer class="dialog-footer">
			<button class="btn btn-glass" onclick={handleCancel} disabled={isSaving}>
				Cancel
			</button>
			<button class="btn btn-primary" onclick={handleSave} disabled={isSaving}>
				{isSaving ? 'Saving...' : 'Save Changes'}
			</button>
		</footer>
	</div>
</div>

<style>
	.settings-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(10px);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: var(--spacing-lg);
	}

	.settings-dialog {
		width: 100%;
		max-width: 500px;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		color: var(--foreground);
	}

	.dialog-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-lg);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dialog-header h2 {
		font-size: var(--font-size-xl);
		font-weight: 600;
		color: var(--foreground);
	}

	.close-button {
		background: none;
		border: none;
		color: var(--muted-foreground);
		cursor: pointer;
		padding: var(--spacing-xs);
		border-radius: 6px;
		transition: all var(--transition-fast);
	}

	.close-button:hover {
		color: var(--foreground);
		background: rgba(255, 255, 255, 0.1);
	}

	.dialog-content {
		flex: 1;
		padding: var(--spacing-lg);
		overflow-y: auto;
	}

	.error-message {
		background: rgba(239, 68, 68, 0.1);
		border: 1px solid rgba(239, 68, 68, 0.3);
		color: #ef4444;
		padding: var(--spacing-md);
		border-radius: 8px;
		margin-bottom: var(--spacing-lg);
		font-size: var(--font-size-sm);
	}

	.settings-form {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-lg);
	}

	.setting-group {
		display: flex;
		flex-direction: column;
	}

	.setting-label {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		font-size: var(--font-size-sm);
		font-weight: 500;
		color: var(--foreground);
	}

	.setting-input {
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 6px;
		color: var(--foreground);
		font-size: var(--font-size-sm);
		transition: all var(--transition-fast);
	}

	.setting-input:focus {
		outline: none;
		border-color: var(--primary-color);
		box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
	}

	.setting-checkbox {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
		font-size: var(--font-size-sm);
		color: var(--foreground);
		cursor: pointer;
	}

	.setting-checkbox input[type="checkbox"] {
		appearance: none;
		width: 18px;
		height: 18px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-radius: 4px;
		background: transparent;
		cursor: pointer;
		position: relative;
		transition: all var(--transition-fast);
	}

	.setting-checkbox input[type="checkbox"]:checked {
		background: var(--primary-color);
		border-color: var(--primary-color);
	}

	.setting-checkbox input[type="checkbox"]:checked::after {
		content: '✓';
		position: absolute;
		top: -2px;
		left: 2px;
		color: white;
		font-size: 12px;
		font-weight: bold;
	}

	.dialog-footer {
		display: flex;
		justify-content: flex-end;
		gap: var(--spacing-md);
		padding: var(--spacing-lg);
		border-top: 1px solid rgba(255, 255, 255, 0.1);
	}

	/* Mobile responsive */
	@media (max-width: 768px) {
		.settings-backdrop {
			padding: var(--spacing-md);
		}

		.settings-dialog {
			max-height: 95vh;
		}
	}
</style>
