<!-- ExportPanel.svelte - Export panel matching desktop app exactly -->
<script lang="ts">
	import { getCurrentSequence } from '$lib/state/sequenceState.svelte';
	import { createEventDispatcher } from 'svelte';
	import ExportActionsCard from './ExportActionsCard.svelte';
	import ExportPreviewCard from './ExportPreviewCard.svelte';
	import ExportSettingsCard from './ExportSettingsCard.svelte';

	const dispatch = createEventDispatcher();

	// Current sequence for export
	let currentSequence = $derived(getCurrentSequence());

	// Export settings state - matching desktop app defaults
	let exportSettings = $state({
		// Export options
		include_start_position: true,
		add_beat_numbers: true,
		add_reversal_symbols: true,
		add_user_info: true,
		add_word: true,
		use_last_save_directory: true,

		// Format settings
		export_format: 'PNG',
		export_quality: '300 DPI',

		// User settings
		user_name: 'Default User',
		custom_note: '',
	});

	// Handle setting changes
	function handleSettingChanged(event: CustomEvent) {
		const { setting, value } = event.detail;
		exportSettings = { ...exportSettings, [setting]: value };

		// Emit to parent for persistence
		dispatch('settingChanged', { setting, value });

		// Trigger preview update
		dispatch('previewUpdateRequested', exportSettings);
	}

	// Handle export current sequence
	function handleExportCurrent() {
		if (!currentSequence || !currentSequence.beats || currentSequence.beats.length === 0) {
			console.warn('No sequence to export');
			return;
		}

		const exportConfig = {
			sequence: currentSequence,
			settings: exportSettings,
		};

		dispatch('exportRequested', { type: 'current', config: exportConfig });
	}

	// Handle export all sequences
	function handleExportAll() {
		const exportConfig = {
			settings: exportSettings,
		};

		dispatch('exportRequested', { type: 'all', config: exportConfig });
	}
</script>

<div class="export-panel">
	<!-- Header -->
	<div class="export-header">
		<h2 class="export-title">Export</h2>
		<p class="export-description">Configure settings and export current sequence</p>
	</div>

	<!-- Main content: Settings and Preview side by side -->
	<div class="export-content">
		<!-- Left: Settings column -->
		<div class="settings-column">
			<!-- Actions should always be visible; place first and keep out of scroll -->
			<ExportActionsCard
				{currentSequence}
				on:exportCurrent={handleExportCurrent}
				on:exportAll={handleExportAll}
			/>

			<!-- Scroll only the settings, not the actions -->
			<div class="settings-scroll">
				<ExportSettingsCard {exportSettings} on:settingChanged={handleSettingChanged} />
			</div>
		</div>

		<!-- Right: Preview column -->
		<div class="preview-column">
			<ExportPreviewCard {currentSequence} {exportSettings} />
		</div>
	</div>
</div>

<style>
	.export-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: var(--spacing-sm);
		gap: var(--spacing-sm);
		overflow: hidden;
	}

	.export-header {
		flex-shrink: 0;
		text-align: left;
	}

	.export-title {
		margin: 0 0 2px 0;
		font-size: var(--font-size-lg);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
	}

	.export-description {
		margin: 0;
		font-size: var(--font-size-xs);
		color: rgba(255, 255, 255, 0.7);
	}

	.export-content {
		flex: 1;
		display: flex;
		gap: var(--spacing-sm);
		overflow: hidden;
		min-height: 0;
	}

	.settings-column {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		min-width: 0;
	}

	/* Only settings should scroll; keep actions visible */
	.settings-scroll {
		flex: 1;
		overflow-y: auto;
		min-height: 0;
	}

	.preview-column {
		flex: 2;
		display: flex;
		flex-direction: column;
		min-width: 0;
		overflow: hidden;
	}

	/* Responsive layout */
	@media (max-width: 1024px) {
		.export-content {
			flex-direction: column;
		}

		.settings-column,
		.preview-column {
			flex: none;
		}

		.settings-column {
			height: auto;
			max-height: 50vh;
		}

		.preview-column {
			flex: 1;
			min-height: 300px;
		}
	}

	@media (max-width: 768px) {
		.export-panel {
			padding: var(--spacing-sm);
		}

		.export-content {
			gap: var(--spacing-sm);
		}

		.settings-column {
			gap: var(--spacing-sm);
		}
	}
</style>
