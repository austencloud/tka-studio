<!--
Responsive Generate Panel - Following Proper UX Principles
Uses device detection service for appropriate touch targets and layout
-->
<script lang="ts">
	import { resolve } from '$services/bootstrap';
	import type { IDeviceDetectionService } from '$services/interfaces';
	import { onMount } from 'svelte';
	
	// Import selector components
	import LengthSelector from '../tabs/generate/selectors/LengthSelector.svelte';
	import LevelSelector from '../tabs/generate/selectors/LevelSelector.svelte';
	import TurnIntensitySelector from '../tabs/generate/selectors/TurnIntensitySelector.svelte';
	import GridModeSelector from '../tabs/generate/selectors/GridModeSelector.svelte';
	import GenerationModeToggle from '../tabs/generate/selectors/GenerationModeToggle.svelte';
	import PropContinuityToggle from '../tabs/generate/selectors/PropContinuityToggle.svelte';
	import LetterTypeSelector from '../tabs/generate/selectors/LetterTypeSelector.svelte';
	import SliceSizeSelector from '../tabs/generate/selectors/SliceSizeSelector.svelte';
	import CAPTypeSelector from '../tabs/generate/selectors/CAPTypeSelector.svelte';

	// Types
	type GenerationMode = 'FREEFORM' | 'CIRCULAR';
	type GridMode = 'DIAMOND' | 'BOX';
	type PropContinuity = 'RANDOM' | 'CONTINUOUS';
	type SliceSize = 'HALVED' | 'QUARTERED';
	type CAPType = 'STRICT_ROTATED';
	type LetterType = 'TYPE1' | 'TYPE2' | 'TYPE3' | 'TYPE4' | 'TYPE5' | 'TYPE6';

	// Service and state
	let deviceService: IDeviceDetectionService | null = null;
	let deviceCapabilities = $state(null);
	let responsiveSettings = $state(null);

	// Generation state
	let currentConfig = $state({
		mode: 'FREEFORM' as GenerationMode,
		length: 16,
		level: 2,
		turnIntensity: 1.0,
		gridMode: 'DIAMOND' as GridMode,
		propContinuity: 'CONTINUOUS' as PropContinuity,
		letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3', 'TYPE4', 'TYPE5', 'TYPE6'] as LetterType[]),
		sliceSize: 'HALVED' as SliceSize,
		capType: 'STRICT_ROTATED' as CAPType,
	});

	let isGenerating = $state(false);
	let isFreeformMode = $derived(currentConfig.mode === 'FREEFORM');

	// Responsive layout properties
	let layoutMode = $derived(() => {
		if (!responsiveSettings) return 'comfortable';
		return responsiveSettings.layoutDensity;
	});

	let shouldAllowScrolling = $derived(() => {
		return responsiveSettings?.allowScrolling ?? true;
	});

	let minTouchTarget = $derived(() => {
		return responsiveSettings?.minTouchTarget ?? 44;
	});

	let elementSpacing = $derived(() => {
		return responsiveSettings?.elementSpacing ?? 16;
	});

	onMount(() => {
		try {
			deviceService = resolve('IDeviceDetectionService');
			deviceCapabilities = deviceService.getCapabilities();
			responsiveSettings = deviceService.getResponsiveSettings();

			console.log('🔍 Device capabilities:', deviceCapabilities);
			console.log('📱 Responsive settings:', responsiveSettings);

			// Listen for device changes (orientation, window resize)
			const cleanup = deviceService.onCapabilitiesChanged((caps) => {
				deviceCapabilities = caps;
				responsiveSettings = deviceService.getResponsiveSettings();
			});

			return cleanup;
		} catch (error) {
			console.warn('DeviceDetectionService not available, using defaults:', error);
			// Fallback defaults
			responsiveSettings = {
				minTouchTarget: 44,
				elementSpacing: 16,
				allowScrolling: true,
				layoutDensity: 'comfortable',
				fontScaling: 1.0
			};
		}
	});

	// Event handlers
	function updateConfig(updates: Partial<typeof currentConfig>) {
		currentConfig = { ...currentConfig, ...updates };
	}

	function onGenerateClicked() {
		if (isGenerating) return;
		isGenerating = true;
		
		console.log('🎯 Generate clicked with config:', currentConfig);
		
		setTimeout(() => {
			isGenerating = false;
		}, 2000);
	}

	function onAutoCompleteClicked() {
		if (isGenerating) return;
		console.log('🔄 Auto-complete clicked');
	}

	// Event handlers for selector changes
	function onLevelChanged(event: CustomEvent) {
		updateConfig({ level: event.detail.value });
	}

	function onLengthChanged(event: CustomEvent) {
		updateConfig({ length: event.detail.value });
	}

	function onTurnIntensityChanged(event: CustomEvent) {
		updateConfig({ turnIntensity: event.detail.value });
	}

	function onGridModeChanged(value: GridMode) {
		updateConfig({ gridMode: value });
	}

	function onGenerationModeChanged(mode: GenerationMode) {
		updateConfig({ mode });
	}

	function onPropContinuityChanged(value: PropContinuity) {
		updateConfig({ propContinuity: value });
	}

	function onLetterTypesChanged(event: CustomEvent) {
		updateConfig({ letterTypes: event.detail.value });
	}

	function onSliceSizeChanged(value: SliceSize) {
		updateConfig({ sliceSize: value });
	}

	function onCAPTypeChanged(event: CustomEvent) {
		updateConfig({ capType: event.detail.value });
	}
</script>

<div 
	class="generate-panel" 
	data-layout={layoutMode} 
	data-allow-scroll={shouldAllowScrolling}
	style="--min-touch-target: {minTouchTarget}px; --element-spacing: {elementSpacing}px;"
>
	<!-- Header -->
	<div class="header">
		<h3>Customize Your Sequence</h3>
		<!-- Debug info removed for production -->
	</div>

	<!-- Settings Container - responsive layout -->
	<div class="settings-container">
		<!-- Core sequence settings always visible -->
		<section class="settings-section">
			<h4 class="section-title">Sequence Settings</h4>
			<div class="settings-grid">
				<div class="setting-item">
					<LevelSelector 
						initialValue={currentConfig.level}
						on:valueChanged={onLevelChanged}
					/>
				</div>
				<div class="setting-item">
					<LengthSelector 
						initialValue={currentConfig.length}
						on:valueChanged={onLengthChanged}
					/>
				</div>
				<div class="setting-item">
					<TurnIntensitySelector
						initialValue={currentConfig.turnIntensity}
						on:valueChanged={onTurnIntensityChanged}
					/>
				</div>
			</div>
		</section>

		<!-- Mode and grid settings -->
		<section class="settings-section">
			<h4 class="section-title">Mode & Layout</h4>
			<div class="settings-grid">
				<div class="setting-item">
					<GridModeSelector
						initialMode={currentConfig.gridMode}
						onvalueChanged={onGridModeChanged}
					/>
				</div>
				<div class="setting-item">
					<GenerationModeToggle
						initialMode={currentConfig.mode}
						onmodeChanged={onGenerationModeChanged}
					/>
				</div>
				<div class="setting-item">
					<PropContinuityToggle
						initialValue={currentConfig.propContinuity}
						onvalueChanged={onPropContinuityChanged}
					/>
				</div>
			</div>
		</section>

		<!-- Mode-specific settings with consistent structure -->
		<section class="settings-section mode-specific-section">
			{#if isFreeformMode}
				<h4 class="section-title">Filter Options</h4>
				<div class="settings-grid">
					<div class="setting-item full-width">
						<LetterTypeSelector
							initialValue={currentConfig.letterTypes}
							on:valueChanged={onLetterTypesChanged}
						/>
					</div>
				</div>
			{:else}
				<h4 class="section-title">Circular Mode Options</h4>
				<div class="settings-grid">
					<div class="setting-item">
						<SliceSizeSelector
							initialValue={currentConfig.sliceSize}
							onvalueChanged={onSliceSizeChanged}
						/>
					</div>
					<div class="setting-item">
						<CAPTypeSelector
							initialValue={currentConfig.capType}
							on:valueChanged={onCAPTypeChanged}
						/>
					</div>
				</div>
			{/if}
		</section>
	</div>

	<!-- Action buttons with proper touch targets -->
	<div class="action-section">
		<button
			class="action-button secondary"
			onclick={onAutoCompleteClicked}
			disabled={isGenerating}
			type="button"
		>
			Auto-Complete
		</button>

		<button
			class="action-button primary"
			onclick={onGenerateClicked}
			disabled={isGenerating}
			type="button"
		>
			{isGenerating ? 'Generating...' : 'Generate New'}
		</button>
	</div>
</div>

<style>
	.generate-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: 16px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		color: rgba(255, 255, 255, 0.9);
		font-family: 'Segoe UI', sans-serif;
		gap: var(--element-spacing);
		overflow: hidden;
	}

	.header {
		flex-shrink: 0;
		text-align: center;
		padding-bottom: 12px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.header h3 {
		margin: 0;
		font-size: 18px;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
	}

	.settings-container {
		flex: 1;
		overflow-y: auto;
		display: grid;
		grid-template-rows: auto auto auto;
		gap: calc(var(--element-spacing) * 1.25);
		margin-bottom: var(--element-spacing);
		min-height: 0; /* Allow proper overflow handling */
		align-content: start; /* Align to top instead of distributing */
	}

	.settings-section {
		display: flex;
		flex-direction: column;
		gap: 12px;
		/* Remove flex: 1 to prevent height expansion issues */
		min-height: auto; /* Let content determine height */
	}

	.section-title {
		margin: 0;
		font-size: 14px;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.8);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		padding-bottom: 6px;
	}

	.settings-grid {
		display: grid;
		gap: var(--element-spacing);
		grid-template-columns: 1fr;
		/* Remove flex: 1 and space-evenly to prevent layout instability */
		align-content: start; /* Align items to start instead of distributing */
	}

	.setting-item {
		border-radius: 6px;
		padding: var(--element-spacing);
		transition: background-color 0.2s ease;
		min-height: var(--min-touch-target);
		display: flex;
		align-items: center;
		justify-content: center;
		/* Remove flex: 1 to prevent expansion issues */
	}

	.setting-item:hover {
		background: rgba(255, 255, 255, 0.08);
	}

	.setting-item.full-width {
		grid-column: 1 / -1;
	}

	/* Ensure smooth transitions when content changes */
	.settings-section {
		transition: height 0.2s ease-out;
	}

	/* Prevent layout shift during mode switching */
	.settings-grid {
		transition: grid-template-rows 0.2s ease-out;
	}

	/* Ensure consistent height for mode-specific section */
	.mode-specific-section {
		min-height: 120px; /* Reserve space to prevent layout shift */
	}

	.action-section {
		flex-shrink: 0;
		display: flex;
		gap: var(--element-spacing);
		padding-top: var(--element-spacing);
		border-top: 1px solid rgba(255, 255, 255, 0.1);
	}

	.action-button {
		flex: 1;
		min-height: var(--min-touch-target);
		padding: 12px 20px;
		border: none;
		border-radius: 6px;
		font-size: 14px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.action-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.action-button.secondary {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: rgba(255, 255, 255, 0.9);
	}

	.action-button.secondary:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.15);
		border-color: rgba(255, 255, 255, 0.3);
	}

	.action-button.primary {
		background: rgba(70, 130, 255, 0.8);
		border: 1px solid rgba(70, 130, 255, 0.9);
		color: white;
	}

	.action-button.primary:hover:not(:disabled) {
		background: rgba(80, 140, 255, 0.9);
		border-color: rgba(80, 140, 255, 1);
	}

	/* Responsive layouts based on device capabilities */
	
	/* Comfortable layout for touch-primary devices */
	.generate-panel[data-layout="comfortable"] .settings-grid {
		grid-template-columns: 1fr;
		gap: calc(var(--element-spacing) * 1.25);
	}

	.generate-panel[data-layout="comfortable"] .setting-item {
		padding: calc(var(--element-spacing) * 1.25);
		min-height: calc(var(--min-touch-target) * 1.2);
	}

	.generate-panel[data-layout="comfortable"] .action-button {
		min-height: calc(var(--min-touch-target) * 1.1);
		font-size: 16px;
	}

	/* Spacious layout for hybrid devices (desktop + touch) */
	.generate-panel[data-layout="spacious"] {
		padding: calc(var(--element-spacing) * 1.5);
		gap: calc(var(--element-spacing) * 1.5);
	}

	.generate-panel[data-layout="spacious"] .settings-grid {
		grid-template-columns: 1fr; /* Keep single column to prevent wrapping issues */
		gap: calc(var(--element-spacing) * 1.5);
	}

	.generate-panel[data-layout="spacious"] .setting-item {
		padding: calc(var(--element-spacing) * 1.5);
		min-height: calc(var(--min-touch-target) * 1.4);
	}

	.generate-panel[data-layout="spacious"] .action-button {
		min-height: calc(var(--min-touch-target) * 1.3);
		font-size: 16px;
	}

	/* Compact layout for precise pointer devices (desktop mouse) */
	.generate-panel[data-layout="compact"] {
		padding: 12px;
		gap: calc(var(--element-spacing) * 0.75);
	}

	.generate-panel[data-layout="compact"] .settings-grid {
		grid-template-columns: 1fr; /* Keep single column to prevent wrapping issues */
		gap: calc(var(--element-spacing) * 0.75);
	}

	.generate-panel[data-layout="compact"] .setting-item {
		padding: calc(var(--element-spacing) * 0.75);
		min-height: calc(var(--min-touch-target) * 0.8);
	}

	.generate-panel[data-layout="compact"] .header h3 {
		font-size: 16px;
	}

	.generate-panel[data-layout="compact"] .action-button {
		min-height: var(--min-touch-target);
		font-size: 13px;
		padding: 8px 16px;
	}

	/* Ensure no scrolling is forced when not appropriate */
	.generate-panel[data-allow-scroll="false"] {
		overflow: hidden;
	}

	.generate-panel[data-allow-scroll="false"] .settings-container {
		overflow: hidden;
		flex: 1;
		min-height: 0;
		/* Ensure grid doesn't expand beyond container */
		max-height: 100%;
	}

	/* Mobile-specific adjustments */
	@media (max-width: 768px) {
		.generate-panel {
			padding: var(--element-spacing);
		}

		.settings-grid {
			grid-template-columns: 1fr !important;
		}

		.action-section {
			flex-direction: column;
		}

		.action-button {
			min-height: calc(var(--min-touch-target) * 1.1) !important;
			font-size: 16px !important;
		}
	}

	/* Large desktop optimization - only enable multi-column for sections with multiple items */
	@media (min-width: 1440px) {
		/* Only apply multi-column to sections that have multiple setting items */
		.generate-panel[data-layout="compact"] .settings-section:not(:has(.full-width)) .settings-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.generate-panel[data-layout="spacious"] .settings-section:not(:has(.full-width)) .settings-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	/* High DPI display adjustments */
	@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
		.action-button {
			border-width: 0.5px;
		}
		
		.setting-item {
			border-width: 0.5px;
		}
	}

	/* Child component styling to work with responsive settings */
	.setting-item :global(.level-selector),
	.setting-item :global(.length-selector),
	.setting-item :global(.turn-intensity-selector),
	.setting-item :global(.grid-mode-selector) {
		width: 100%;
	}

	.setting-item :global(.level-button) {
		min-height: calc(var(--min-touch-target) * 0.8);
		min-width: calc(var(--min-touch-target) * 0.8);
	}

	.setting-item :global(.value-display) {
		min-height: calc(var(--min-touch-target) * 0.6);
		min-width: calc(var(--min-touch-target) * 0.8);
	}
</style>