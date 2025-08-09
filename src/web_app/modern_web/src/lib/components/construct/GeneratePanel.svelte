<!--
Generate Panel - Svelte Version for Construct Tab Right Panel
Modern Generate Panel with Tasteful Glassmorphism

A clean, compact design that fits in the construct tab's right panel
while maintaining the legacy layout structure with subtle glass effects.
-->
<script lang="ts">
	// Import all selector components from the tabs directory for now
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
	type CAPType = 'STRICT_ROTATED'; // Simplified for demo
	type LetterType = 'TYPE1' | 'TYPE2' | 'TYPE3' | 'TYPE4' | 'TYPE5' | 'TYPE6';

	interface GenerationConfig {
		mode: GenerationMode;
		length: number;
		level: number;
		turnIntensity: number;
		gridMode: GridMode;
		propContinuity: PropContinuity;
		letterTypes: Set<LetterType>;
		sliceSize: SliceSize;
		capType: CAPType;
	}

	interface GenerationState {
		config: GenerationConfig;
		isGenerating: boolean;
	}

	// State
	let currentConfig: GenerationConfig = $state({
		mode: 'FREEFORM',
		length: 16,
		level: 2,
		turnIntensity: 1.0,
		gridMode: 'DIAMOND',
		propContinuity: 'CONTINUOUS',
		letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3', 'TYPE4', 'TYPE5', 'TYPE6']),
		sliceSize: 'HALVED',
		capType: 'STRICT_ROTATED',
	});

	let isGenerating = $state(false);

	let currentState: GenerationState = $derived({
		config: currentConfig,
		isGenerating: isGenerating,
	});

	// Component references
	let lengthSelectorRef = $state<LengthSelector>();
	let levelSelectorRef = $state<LevelSelector>();
	let turnIntensitySelectorRef = $state<TurnIntensitySelector>();
	let gridModeSelectorRef = $state<GridModeSelector>();
	let generationModeToggleRef = $state<GenerationModeToggle>();
	let propContinuityToggleRef = $state<PropContinuityToggle>();
	let letterTypeSelectorRef = $state<LetterTypeSelector>();
	let sliceSizeSelectorRef = $state<SliceSizeSelector>();
	let capTypeSelectorRef = $state<CAPTypeSelector>();

	// Derived state
	let isFreeformMode = $derived(currentConfig.mode === 'FREEFORM');

	// Event handlers
	function updateConfig(updates: Partial<GenerationConfig>) {
		currentConfig = { ...currentConfig, ...updates };
		currentState = { ...currentState, config: currentConfig };

		console.log('🔍 [GENERATE_PANEL] Config updated:', updates);
		console.log('🔍 [GENERATE_PANEL] Current config:', currentConfig);
	}

	function onModeChanged(event: CustomEvent) {
		const mode = event.detail.mode as GenerationMode;
		updateConfig({ mode });
		updateComponentVisibility(mode);
	}

	function onLengthChanged(event: CustomEvent) {
		const length = event.detail.value as number;
		console.log('🔍 [GENERATE_PANEL] Length changed to:', length);
		updateConfig({ length });
	}

	function onLevelChanged(event: CustomEvent) {
		const level = event.detail.value as number;
		updateConfig({ level });
	}

	function onTurnIntensityChanged(event: CustomEvent) {
		const turnIntensity = event.detail.value as number;
		updateConfig({ turnIntensity });
	}

	function onGridModeChanged(event: CustomEvent) {
		const gridMode = event.detail.value as GridMode;
		updateConfig({ gridMode });
	}

	function onPropContinuityChanged(event: CustomEvent) {
		const propContinuity = event.detail.value as PropContinuity;
		updateConfig({ propContinuity });
	}

	function onLetterTypesChanged(event: CustomEvent) {
		const letterTypes = event.detail.value as Set<LetterType>;
		updateConfig({ letterTypes });
	}

	function onSliceSizeChanged(event: CustomEvent) {
		const sliceSize = event.detail.value as SliceSize;
		updateConfig({ sliceSize });
	}

	function onCAPTypeChanged(event: CustomEvent) {
		const capType = event.detail.value as CAPType;
		updateConfig({ capType });
	}

	function updateComponentVisibility(mode: GenerationMode) {
		const isFreeform = mode === 'FREEFORM';

		// Update visibility - these will be handled by reactive statements
		// In Svelte, we'll use conditional rendering in the template
	}

	function onGenerateClicked() {
		if (isGenerating) return;

		console.log('🎯 [GENERATE_PANEL] Generate clicked with config:', currentConfig);

		isGenerating = true;

		// Simulate generation process
		setTimeout(() => {
			isGenerating = false;
			console.log('✅ [GENERATE_PANEL] Generation completed');
		}, 2000);
	}

	function onAutoCompleteClicked() {
		if (isGenerating) return;

		console.log('🔄 [GENERATE_PANEL] Auto-complete clicked');
		// TODO: Implement auto-complete logic
	}

	// Set up event listeners
	$effect(() => {
		// Mode change events
		const handleModeChange = (e: Event) => onModeChanged(e as CustomEvent);
		document.addEventListener('modeChanged', handleModeChange);

		// Value change events
		const handleLengthChange = (e: Event) => onLengthChanged(e as CustomEvent);
		const handleLevelChange = (e: Event) => onLevelChanged(e as CustomEvent);
		const handleTurnIntensityChange = (e: Event) => onTurnIntensityChanged(e as CustomEvent);
		const handleGridModeChange = (e: Event) => onGridModeChanged(e as CustomEvent);
		const handlePropContinuityChange = (e: Event) => onPropContinuityChanged(e as CustomEvent);
		const handleLetterTypesChange = (e: Event) => onLetterTypesChanged(e as CustomEvent);
		const handleSliceSizeChange = (e: Event) => onSliceSizeChanged(e as CustomEvent);
		const handleCAPTypeChange = (e: Event) => onCAPTypeChanged(e as CustomEvent);

		document.addEventListener('valueChanged', handleLengthChange);
		document.addEventListener('valueChanged', handleLevelChange);
		document.addEventListener('valueChanged', handleTurnIntensityChange);
		document.addEventListener('valueChanged', handleGridModeChange);
		document.addEventListener('valueChanged', handlePropContinuityChange);
		document.addEventListener('valueChanged', handleLetterTypesChange);
		document.addEventListener('valueChanged', handleSliceSizeChange);
		document.addEventListener('valueChanged', handleCAPTypeChange);

		return () => {
			document.removeEventListener('modeChanged', handleModeChange);
			document.removeEventListener('valueChanged', handleLengthChange);
			document.removeEventListener('valueChanged', handleLevelChange);
			document.removeEventListener('valueChanged', handleTurnIntensityChange);
			document.removeEventListener('valueChanged', handleGridModeChange);
			document.removeEventListener('valueChanged', handlePropContinuityChange);
			document.removeEventListener('valueChanged', handleLetterTypesChange);
			document.removeEventListener('valueChanged', handleSliceSizeChange);
			document.removeEventListener('valueChanged', handleCAPTypeChange);
		};
	});
</script>

<div class="generate-panel">
	<!-- Minimal header -->
	<div class="header">
		<h3>Customize Your Sequence</h3>
	</div>

	<!-- Controls section - clean and spacious -->
	<div class="controls-section">
		<LevelSelector bind:this={levelSelectorRef} initialValue={currentConfig.level} />

		<LengthSelector bind:this={lengthSelectorRef} initialValue={currentConfig.length} />

		<TurnIntensitySelector
			bind:this={turnIntensitySelectorRef}
			initialValue={currentConfig.turnIntensity}
		/>

		<GridModeSelector bind:this={gridModeSelectorRef} initialMode={currentConfig.gridMode} />

		<GenerationModeToggle
			bind:this={generationModeToggleRef}
			initialMode={currentConfig.mode}
		/>

		<PropContinuityToggle
			bind:this={propContinuityToggleRef}
			initialValue={currentConfig.propContinuity}
		/>

		<!-- Mode-specific controls with fixed height container -->
		<div class="mode-specific-controls">
			{#if isFreeformMode}
				<LetterTypeSelector
					bind:this={letterTypeSelectorRef}
					initialValue={currentConfig.letterTypes}
				/>
			{:else}
				<SliceSizeSelector
					bind:this={sliceSizeSelectorRef}
					initialValue={currentConfig.sliceSize}
				/>

				<CAPTypeSelector
					bind:this={capTypeSelectorRef}
					initialValue={currentConfig.capType}
				/>
			{/if}
		</div>
	</div>

	<!-- Action buttons - prominent and clear -->
	<div class="action-buttons">
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
		flex: 1; /* Take full available height from flex parent */
		min-height: 0; /* Allow flex shrinking */
		padding: 16px;
		/* Transparent background to show beautiful background without blur */
		background: rgba(255, 255, 255, 0.05);
		/* backdrop-filter: blur(20px); - REMOVED to show background */
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
		font-family: 'Segoe UI', sans-serif;
		border-radius: 8px;
		gap: 12px;
		overflow-y: auto;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.header {
		text-align: center;
		padding: 0 0 8px 0;
		margin: 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.header h3 {
		color: rgba(255, 255, 255, 0.95);
		font-size: 18px;
		font-weight: 600;
		letter-spacing: 0.5px;
		margin: 0;
		background: transparent;
		border: none;
	}

	.controls-section {
		display: flex;
		flex-direction: column;
		gap: 12px; /* Restore gap for proper spacing */
		flex: 1; /* Take all available space between header and buttons */
		overflow-y: visible; /* Allow natural height */
		padding-bottom: 8px; /* Add some bottom spacing */
		justify-content: space-evenly; /* Distribute space evenly between controls */
	}

	/* Make each control item expand equally without breaking internal layouts */
	.controls-section > :global(*) {
		flex: 1; /* Each control gets equal space */
		display: flex;
		align-items: center; /* Center content vertically within each flex item */
		min-height: 60px; /* Minimum height for each control */
		padding: 12px 0; /* Add vertical padding for spacing */
		border-bottom: 1px solid rgba(255, 255, 255, 0.05); /* Subtle separator */
	}

	/* Remove border from last item */
	.controls-section > :global(*:last-child) {
		border-bottom: none;
	}

	/* Fixed height container for mode-specific controls */
	.mode-specific-controls {
		flex: 2; /* Give this section more space since it can have multiple components */
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: stretch;
		min-height: 120px; /* Fixed minimum height to prevent layout shifts */
		max-height: 140px; /* Fixed maximum height to maintain consistency */
		overflow: hidden; /* Hide overflow if content is too tall */
		gap: 8px; /* Space between multiple components in circular mode */
		padding: 12px 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	/* Ensure child components fit within the fixed height */
	.mode-specific-controls > :global(*) {
		flex-shrink: 1; /* Allow shrinking if needed */
		overflow: hidden; /* Prevent overflow */
	}

	.action-buttons {
		display: flex;
		flex-direction: column;
		gap: 12px;
		flex-shrink: 0; /* Don't shrink */
		padding-top: 16px; /* Add some spacing above buttons */
		border-top: 1px solid rgba(255, 255, 255, 0.1); /* Subtle separator */
	}

	.action-button {
		border-radius: 6px;
		font-size: 14px;
		font-weight: 500;
		padding: 10px 16px;
		width: 100%;
		cursor: pointer;
		transition: all 0.2s ease;
		border: none;
		outline: none;
	}

	.action-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.action-button.secondary {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: rgba(255, 255, 255, 0.9);
		font-weight: 500;
	}

	.action-button.secondary:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.15);
		border-color: rgba(255, 255, 255, 0.3);
		color: white;
	}

	.action-button.secondary:active:not(:disabled) {
		background: rgba(255, 255, 255, 0.2);
	}

	.action-button.primary {
		background: rgba(70, 130, 255, 0.8);
		border: 1px solid rgba(70, 130, 255, 0.9);
		color: white;
		font-weight: 600;
	}

	.action-button.primary:hover:not(:disabled) {
		background: rgba(80, 140, 255, 0.9);
		border-color: rgba(80, 140, 255, 1);
	}

	.action-button.primary:active:not(:disabled) {
		background: rgba(60, 120, 245, 0.9);
	}
</style>
