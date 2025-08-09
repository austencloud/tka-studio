<!-- CodexExporterTab.svelte - Export all pictographs with turn configurations -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import SettingCard from '../SettingCard.svelte';
	import TextInput from '../TextInput.svelte';
	import SelectInput from '../SelectInput.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';

	interface Props {
		settings: any;
	}

	let { settings }: Props = $props();
	const dispatch = createEventDispatcher();

	// Local state for form values - matching desktop app defaults
	let redTurns = $state(settings.codexExporter?.redTurns ?? 16);
	let blueTurns = $state(settings.codexExporter?.blueTurns ?? 16);
	let gridMode = $state(settings.codexExporter?.gridMode ?? 'diamond');
	let generateAll = $state(settings.codexExporter?.generateAll ?? true);
	let quality = $state(settings.codexExporter?.quality ?? 300);
	let includeMetadata = $state(settings.codexExporter?.includeMetadata ?? true);

	// Options - matching desktop app
	const gridModeOptions = [
		{ value: 'diamond', label: 'Diamond' },
		{ value: 'box', label: 'Box' },
	];

	// Update handlers
	function handleRedTurnsChange(event: CustomEvent) {
		redTurns = parseInt(event.detail);
		saveSettings();
	}

	function handleBlueTurnsChange(event: CustomEvent) {
		blueTurns = parseInt(event.detail);
		saveSettings();
	}

	function handleGridModeChange(event: CustomEvent) {
		gridMode = event.detail;
		saveSettings();
	}

	function handleGenerateAllChange(event: CustomEvent) {
		generateAll = event.detail;
		saveSettings();
	}

	function handleQualityChange(event: CustomEvent) {
		quality = parseInt(event.detail);
		saveSettings();
	}

	function handleIncludeMetadataChange(event: CustomEvent) {
		includeMetadata = event.detail;
		saveSettings();
	}

	function saveSettings() {
		const codexExporterSettings = {
			redTurns,
			blueTurns,
			gridMode,
			generateAll,
			quality,
			includeMetadata,
		};
		dispatch('update', { key: 'codexExporter', value: codexExporterSettings });
	}

	function handleExportClick() {
		const config = {
			red_turns: redTurns,
			blue_turns: blueTurns,
			grid_mode: gridMode,
			generate_all: generateAll,
			quality: quality,
			include_metadata: includeMetadata,
		};

		// Emit export event (services will be handled later)
		dispatch('export', config);

		// Show success message
		alert('Pictograph export has been initiated. This may take several minutes to complete.');
	}
</script>

<div class="tab-content">
	<SettingCard
		title="Codex Exporter"
		description="Export all pictographs with customizable turn configurations"
	>
		<!-- Turn Configuration Section -->
		<div class="section-group">
			<h4 class="section-title">Turn Configuration</h4>
			<div class="turn-inputs">
				<TextInput
					label="Red Turns"
					value={redTurns.toString()}
					type="number"
					min={1}
					max={64}
					helpText="Number of red turns for pictographs"
					on:change={handleRedTurnsChange}
				/>
				<TextInput
					label="Blue Turns"
					value={blueTurns.toString()}
					type="number"
					min={1}
					max={64}
					helpText="Number of blue turns for pictographs"
					on:change={handleBlueTurnsChange}
				/>
			</div>
		</div>

		<!-- Grid Mode Section -->
		<div class="section-group">
			<h4 class="section-title">Grid Mode</h4>
			<SelectInput
				label="Grid Layout"
				value={gridMode}
				options={gridModeOptions}
				helpText="Pictograph grid layout style"
				on:change={handleGridModeChange}
			/>
		</div>

		<!-- Export Options Section -->
		<div class="section-group">
			<h4 class="section-title">Export Options</h4>
			<ToggleSetting
				label="Generate All Variations"
				checked={generateAll}
				helpText="Generate all possible pictograph variations"
				on:change={handleGenerateAllChange}
			/>

			<TextInput
				label="Image Quality (DPI)"
				value={quality.toString()}
				type="number"
				min={72}
				max={600}
				helpText="Image resolution for exported pictographs"
				on:change={handleQualityChange}
			/>

			<ToggleSetting
				label="Include Export Metadata"
				checked={includeMetadata}
				helpText="Include metadata information in exported files"
				on:change={handleIncludeMetadataChange}
			/>
		</div>

		<!-- Export Button -->
		<div class="export-section">
			<button class="export-button" onclick={handleExportClick}>
				Export All Pictographs
			</button>
		</div>
	</SettingCard>
</div>

<style>
	.tab-content {
		max-width: 500px;
	}

	.section-group {
		margin-bottom: var(--spacing-lg);
	}

	.section-title {
		margin: 0 0 var(--spacing-md) 0;
		font-size: var(--font-size-md);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		padding-bottom: var(--spacing-sm);
	}

	.turn-inputs {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--spacing-md);
	}

	.export-section {
		margin-top: var(--spacing-xl);
		display: flex;
		justify-content: center;
	}

	.export-button {
		background: linear-gradient(135deg, #6366f1 0%, #5855eb 100%);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		color: white;
		font-size: var(--font-size-sm);
		font-weight: 600;
		padding: var(--spacing-md) var(--spacing-xl);
		cursor: pointer;
		transition: all var(--transition-fast);
		min-width: 200px;
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
	}

	.export-button:hover {
		background: linear-gradient(135deg, #5855eb 0%, #4f46e5 100%);
		transform: translateY(-1px);
		box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
	}

	.export-button:active {
		transform: translateY(0);
		box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
	}

	/* Responsive */
	@media (max-width: 768px) {
		.turn-inputs {
			grid-template-columns: 1fr;
		}
	}
</style>
