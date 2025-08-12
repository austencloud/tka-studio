<!-- SettingsDialog.svelte - Simplified main settings dialog -->
<script lang="ts">
	import type { BackgroundType, QualityLevel } from '$lib/components/backgrounds/types/types';
	import { getSettings, hideSettingsDialog, updateSettings } from '$lib/state/appState.svelte';

	import SettingsSidebar from './settings/SettingsSidebar.svelte';
	import BackgroundTab from './settings/tabs/BackgroundTab.svelte';
	import CodexExporterTab from './settings/tabs/CodexExporterTab.svelte';
	import GeneralTab from './settings/tabs/GeneralTab.svelte';
	import PropTypeTab from './settings/tabs/PropTypeTab.svelte';
	import VisibilityTab from './settings/tabs/VisibilityTab.svelte';

	// Current settings state
	let settings = $state(getSettings());
	let activeTab = $state('General');

	// Derived state for background settings - ensure compatibility
	const backgroundSettings = $derived(() => {
		const bgType = settings.backgroundType;
		// Map unsupported types to supported ones
		const supportedType: BackgroundType | undefined =
			bgType === 'auroraBorealis' || bgType === 'starfield'
				? 'aurora'
				: bgType === 'snowfall' ||
					  bgType === 'nightSky' ||
					  bgType === 'aurora' ||
					  bgType === 'bubbles'
					? bgType
					: bgType
						? 'aurora'
						: undefined; // default fallback or undefined if no bgType

		const result: {
			backgroundType?: BackgroundType;
			backgroundQuality?: QualityLevel;
			backgroundEnabled?: boolean;
		} = {};

		if (supportedType) result.backgroundType = supportedType;
		if (settings.backgroundQuality)
			result.backgroundQuality = settings.backgroundQuality as QualityLevel;
		if (settings.backgroundEnabled !== undefined)
			result.backgroundEnabled = settings.backgroundEnabled;

		return result;
	});

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

	// Adapter for modern prop-based updates
	function handlePropUpdate(event: { key: string; value: unknown }) {
		const newSettings = { ...settings, [event.key]: event.value };
		updateSettings(newSettings);
		settings = newSettings;
	}

	// Adapter for export handler
	function handlePropExport() {
		handleCodexExport(new CustomEvent('export'));
	}

	// Handle codex export request
	function handleCodexExport(event: CustomEvent) {
		const config = event.detail;
		console.log('🚀 Codex export requested with config:', config);
		// TODO: Implement actual export service call
	}

	// Handle apply/save
	function handleApply() {
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

	// Handle keyboard events for backdrop
	function handleBackdropKeyDown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			handleClose();
		}
	}
</script>

<!-- Settings Dialog Overlay -->
<div
	class="settings-overlay"
	onclick={handleBackdropClick}
	onkeydown={handleBackdropKeyDown}
	role="dialog"
	aria-modal="true"
	aria-labelledby="settings-title"
	tabindex="-1"
>
	<div class="settings-dialog">
		<!-- Dialog Header -->
		<div class="dialog-header">
			<h2 id="settings-title">Settings</h2>
			<button class="close-button" onclick={handleClose} aria-label="Close settings">
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
					<PropTypeTab {settings} onUpdate={handlePropUpdate} />
				{:else if activeTab === 'Visibility'}
					<VisibilityTab {settings} onUpdate={handlePropUpdate} />
				{:else if activeTab === 'Background'}
					<BackgroundTab
						settings={backgroundSettings()}
						on:update={handleSettingsUpdate}
					/>
				{:else if activeTab === 'CodexExporter'}
					<CodexExporterTab
						{settings}
						onUpdate={handlePropUpdate}
						onExport={handlePropExport}
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
		width: min(90vw, 1400px); /* Increased from 800px to 1400px for much larger dialog */
		height: min(90vh, 900px); /* Increased to 90vh and 900px for much taller dialog */
		background: rgba(40, 44, 52, 0.95);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		backdrop-filter: blur(20px);
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		container-type: inline-size;

		/* CSS Custom Properties for responsive sizing */
		--dialog-width: min(90vw, 1400px);
		--dialog-height: min(90vh, 900px);
		--sidebar-width: clamp(150px, 15vw, 250px);
		--content-width: calc(var(--dialog-width) - var(--sidebar-width));
		--content-padding: clamp(16px, 2vw, 32px);
		--responsive-columns: 1;
		--max-content-width: none;
	}

	/* Dialog Header */
	.dialog-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: clamp(16px, 2vw, 32px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.15);
		background: rgba(255, 255, 255, 0.05);
	}

	.dialog-header h2 {
		margin: 0;
		font-size: clamp(16px, 2vw, 24px);
		font-weight: 600;
		color: #ffffff;
	}

	.close-button {
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.7);
		cursor: pointer;
		padding: clamp(8px, 1vw, 12px);
		border-radius: 6px;
		transition: all var(--transition-fast);
		min-width: clamp(32px, 4vw, 44px);
		min-height: clamp(32px, 4vw, 44px);
		display: flex;
		align-items: center;
		justify-content: center;
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
		padding: var(--content-padding);
		background: rgba(255, 255, 255, 0.02);
		container-type: inline-size;
	}

	/* Container Queries for Responsive Layout */
	@container (min-width: 400px) {
		.settings-dialog {
			--responsive-columns: 1;
			--max-content-width: 100%;
		}
	}

	@container (min-width: 600px) {
		.settings-dialog {
			--responsive-columns: 1;
			--max-content-width: 90%;
		}
	}

	@container (min-width: 800px) {
		.settings-dialog {
			--responsive-columns: 2;
			--max-content-width: 85%;
		}
	}

	@container (min-width: 1000px) {
		.settings-dialog {
			--responsive-columns: 2;
			--max-content-width: 80%;
			--content-padding: clamp(24px, 3vw, 48px);
		}
	}

	@container (min-width: 1200px) {
		.settings-dialog {
			--responsive-columns: 3;
			--max-content-width: 75%;
			--content-padding: clamp(32px, 4vw, 64px);
		}
	}

	/* Dialog Footer */
	.dialog-footer {
		display: flex;
		justify-content: flex-end;
		gap: clamp(12px, 1.5vw, 24px);
		padding: clamp(16px, 2vw, 32px);
		border-top: 1px solid rgba(255, 255, 255, 0.15);
		background: rgba(255, 255, 255, 0.05);
		flex-wrap: wrap;
	}

	.cancel-button,
	.apply-button {
		padding: clamp(8px, 1vw, 12px) clamp(16px, 2vw, 32px);
		border-radius: 6px;
		font-size: clamp(12px, 1.2vw, 16px);
		font-weight: 500;
		cursor: pointer;
		transition: all var(--transition-fast);
		min-width: clamp(80px, 10vw, 120px);
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

	/* Responsive Design */
	@media (max-width: 1024px) {
		.settings-dialog {
			--sidebar-width: clamp(120px, 12vw, 180px);
		}
	}

	@media (max-width: 768px) {
		.settings-overlay {
			padding: clamp(8px, 2vw, 16px);
		}

		.settings-dialog {
			width: 100%;
			height: 100%;
			max-height: none;
			border-radius: 0;
			--sidebar-width: 100%;
			--content-padding: clamp(12px, 3vw, 24px);
		}

		.dialog-content {
			flex-direction: column;
		}
	}

	@media (max-width: 480px) {
		.settings-dialog {
			--content-padding: clamp(8px, 2vw, 16px);
		}
	}

	/* High DPI / Retina Display Support */
	@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
		.settings-dialog {
			border-width: 0.5px;
		}
	}
</style>
