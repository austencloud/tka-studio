<!-- CodexExporterTab.svelte - Export all pictographs with turn configurations -->
<script lang="ts">
	import type { AppSettings } from '$services/interfaces';
	import SelectInput from '../SelectInput.svelte';
	import SettingCard from '../SettingCard.svelte';
	import TextInput from '../TextInput.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';

	interface Props {
		settings: AppSettings & { codexExporter?: Record<string, unknown> };
		onUpdate?: (event: { key: string; value: unknown }) => void;
		onExport?: () => void;
	}

	let { settings, onUpdate, onExport }: Props = $props();

	// Local state for form values - matching desktop app defaults
	let redTurns = $state((settings.codexExporter?.redTurns as number) ?? 16);
	let blueTurns = $state((settings.codexExporter?.blueTurns as number) ?? 16);
	let gridMode = $state((settings.codexExporter?.gridMode as string) ?? 'diamond');
	let generateAll = $state((settings.codexExporter?.generateAll as boolean) ?? true);
	let quality = $state((settings.codexExporter?.quality as number) ?? 300);
	let includeMetadata = $state((settings.codexExporter?.includeMetadata as boolean) ?? true);

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
		onUpdate?.({ key: 'codexExporter', value: codexExporterSettings });
	}

	function handleExportClick() {
		// Emit export event (services will be handled later)
		onExport?.();

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
		width: 100%;
		max-width: var(--max-content-width, 100%);
		margin: 0 auto;
		container-type: inline-size;
	}

	.section-group {
		margin-bottom: clamp(16px, 2vw, 32px);
	}

	.section-title {
		margin: 0 0 clamp(12px, 1.5vw, 24px) 0;
		font-size: clamp(14px, 1.4vw, 18px);
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		padding-bottom: clamp(8px, 1vw, 16px);
	}

	.turn-inputs {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: clamp(12px, 1.5vw, 24px);
	}

	/* Container queries for codex exporter layout */
	@container (min-width: 400px) {
		.tab-content {
			display: grid;
			grid-template-columns: 1fr;
			gap: clamp(20px, 2.5vw, 40px);
		}
	}

	@container (min-width: 600px) {
		.tab-content {
			grid-template-columns: 1fr 1fr;
			gap: clamp(24px, 3vw, 48px);
			align-items: start;
		}
	}

	@container (max-width: 500px) {
		.turn-inputs {
			grid-template-columns: 1fr;
		}
	}

	.export-section {
		margin-top: clamp(24px, 3vw, 48px);
		display: flex;
		justify-content: center;
	}

	.export-button {
		background: linear-gradient(135deg, #6366f1 0%, #5855eb 100%);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		color: white;
		font-size: clamp(12px, 1.2vw, 16px);
		font-weight: 600;
		padding: clamp(12px, 1.5vw, 20px) clamp(20px, 2.5vw, 40px);
		cursor: pointer;
		transition: all var(--transition-fast);
		min-width: clamp(150px, 20vw, 250px);
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

	/* Remove old responsive styles - replaced with container queries */
</style>
