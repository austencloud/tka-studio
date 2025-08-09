<!-- SettingsDialog.svelte - Simplified main settings dialog -->
<script lang="ts">
	import { hideSettingsDialog, getSettings, updateSettings } from '$stores/appState.svelte';
	import { createEventDispatcher } from 'svelte';

	import SettingsSidebar from './settings/SettingsSidebar.svelte';
	import GeneralTab from './settings/tabs/GeneralTab.svelte';
	import PropTypeTab from './settings/tabs/PropTypeTab.svelte';
	import VisibilityTab from './settings/tabs/VisibilityTab.svelte';
	import BackgroundTab from './settings/tabs/BackgroundTab.svelte';
	import CodexExporterTab from './settings/tabs/CodexExporterTab.svelte';

	const dispatch = createEventDispatcher();

	// Current settings state
	let settings = $state(getSettings());
	let activeTab = $state('General');

	// Simplified tab configuration
	const tabs = [
		{ id: 'General', label: 'General', icon: '⚙️' },
		{ id: 'PropType', label: 'Prop Type', icon: '🏷️' },
		{ id: 'Visibility', label: 'Visibility', icon: '👁️' },
		{ id: 'Background', label: 'Background', icon: '🌌' },
		{ id: 'CodexExporter', label: 'Codex Exporter', icon: '📤' },
	];

	// Handle tab switching
	function switchTab(tabId: string) {
		activeTab = tabId;
	}

	// Handle settings updates from tabs
	function handleSettingsUpdate(event: CustomEvent) {
		const { key, value } = event.detail;
		const newSettings = { ...settings, [key]: value };
		updateSettings(newSettings);
		settings = newSettings;
	}

	// Handle codex export request
	function handleCodexExport(event: CustomEvent) {
		const config = event.detail;
		console.log('🚀 Codex export requested with config:', config);
		// TODO: Implement actual export service call
		dispatch('codexExport', config);
	}

	// Handle apply/save
	function handleApply() {
		dispatch('applied', settings);
		console.log('✅ Settings applied:', settings);
		hideSettingsDialog();
	}

	// Handle close/cancel
	function handleClose() {
		hideSettingsDialog();
	}

	// Handle outside click to close
	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			handleClose();
		}
	}
</script>

<!-- Settings Dialog Overlay -->
<div class="settings-overlay" onclick={handleBackdropClick}>
	<div class="settings-dialog">
		<!-- Dialog Header -->
		<div class="dialog-header">
			<h2>Settings</h2>
			<button class="close-button" onclick={handleClose}>
				<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
					<path
						d="M18 6L6 18M6 6l12 12"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
					/>
				</svg>
			</button>
		</div>

		<!-- Dialog Content -->
		<div class="dialog-content">
			<!-- Sidebar Navigation -->
			<SettingsSidebar {tabs} {activeTab} onTabSelect={switchTab} />

			<!-- Content Area -->
			<main class="settings-content">
				{#if activeTab === 'General'}
					<GeneralTab {settings} on:update={handleSettingsUpdate} />
				{:else if activeTab === 'PropType'}
					<PropTypeTab {settings} on:update={handleSettingsUpdate} />
				{:else if activeTab === 'Visibility'}
					<VisibilityTab {settings} on:update={handleSettingsUpdate} />
				{:else if activeTab === 'Background'}
					<BackgroundTab {settings} on:update={handleSettingsUpdate} />
				{:else if activeTab === 'CodexExporter'}
					<CodexExporterTab
						{settings}
						on:update={handleSettingsUpdate}
						on:export={handleCodexExport}
					/>
				{/if}
			</main>
		</div>

		<!-- Dialog Footer -->
		<div class="dialog-footer">
			<button class="cancel-button" onclick={handleClose}>Cancel</button>
			<button class="apply-button" onclick={handleApply}>Apply Settings</button>
		</div>
	</div>
</div>

<style>
	.settings-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.7);
		backdrop-filter: blur(8px);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: var(--spacing-lg);
	}

	.settings-dialog {
		width: min(90vw, 800px);
		height: min(85vh, 600px);
		background: rgba(40, 44, 52, 0.95);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		backdrop-filter: blur(20px);
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	/* Dialog Header */
	.dialog-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-lg);
		border-bottom: 1px solid rgba(255, 255, 255, 0.15);
		background: rgba(255, 255, 255, 0.05);
	}

	.dialog-header h2 {
		margin: 0;
		font-size: var(--font-size-xl);
		font-weight: 600;
		color: #ffffff;
	}

	.close-button {
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.7);
		cursor: pointer;
		padding: var(--spacing-sm);
		border-radius: 6px;
		transition: all var(--transition-fast);
	}

	.close-button:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #ffffff;
	}

	/* Dialog Content Layout */
	.dialog-content {
		flex: 1;
		display: flex;
		overflow: hidden;
		min-height: 0;
	}

	/* Content Area */
	.settings-content {
		flex: 1;
		overflow-y: auto;
		padding: var(--spacing-lg);
		background: rgba(255, 255, 255, 0.02);
	}

	/* Dialog Footer */
	.dialog-footer {
		display: flex;
		justify-content: flex-end;
		gap: var(--spacing-md);
		padding: var(--spacing-lg);
		border-top: 1px solid rgba(255, 255, 255, 0.15);
		background: rgba(255, 255, 255, 0.05);
	}

	.cancel-button,
	.apply-button {
		padding: var(--spacing-sm) var(--spacing-lg);
		border-radius: 6px;
		font-size: var(--font-size-sm);
		font-weight: 500;
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.cancel-button {
		background: transparent;
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: rgba(255, 255, 255, 0.8);
	}

	.cancel-button:hover {
		background: rgba(255, 255, 255, 0.08);
		color: #ffffff;
	}

	.apply-button {
		background: #6366f1;
		border: 1px solid #6366f1;
		color: white;
	}

	.apply-button:hover {
		background: #5855eb;
		border-color: #5855eb;
	}

	/* Responsive */
	@media (max-width: 768px) {
		.settings-overlay {
			padding: var(--spacing-md);
		}

		.settings-dialog {
			width: 100%;
			height: 100%;
			max-height: none;
		}

		.dialog-content {
			flex-direction: column;
		}
	}
</style>
