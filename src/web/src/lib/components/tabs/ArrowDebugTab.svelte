<script lang="ts">
	/**
	 * Arrow Debug Tab - Rebuilt Component
	 * 
	 * Completely rewritten from scratch as requested.
	 * Broken down into smaller, focused components that work together.
	 */

	import { onMount } from 'svelte';
	import DebugHeader from './arrow-debug/DebugHeader.svelte';
	import DebugControls from './arrow-debug/DebugControls.svelte';
	import DebugCanvas from './arrow-debug/DebugCanvas.svelte';
	import DebugInfoPanel from './arrow-debug/DebugInfoPanel.svelte';
	import DebugErrorDisplay from './arrow-debug/DebugErrorDisplay.svelte';
	import DebugLoadingState from './arrow-debug/DebugLoadingState.svelte';
	import { createDebugState } from './arrow-debug/debug-state.svelte';

	// Application state
	let isAppReady = $state(false);
	let initError = $state<string | null>(null);

	// Create debug state
	const debugState = createDebugState();

	// Handle pictograph selection
	function handlePictographSelect(pictograph: any) {
		debugState.selectedPictograph = pictograph;
	}

	// Handle arrow color selection
	function handleArrowColorSelect(color: 'red' | 'blue') {
		debugState.selectedArrowColor = color;
	}

	// Handle step-by-step mode toggle
	function handleStepByStepToggle(enabled: boolean) {
		debugState.stepByStepMode = enabled;
	}

	// Handle step change
	function handleStepChange(step: number) {
		debugState.currentStep = step;
	}

	// Handle visualization toggles
	function handleVisualizationToggle(setting: string, enabled: boolean) {
		switch (setting) {
			case 'showCoordinateGrid':
				debugState.showCoordinateGrid = enabled;
				break;
			case 'showHandPoints':
				debugState.showHandPoints = enabled;
				break;
			case 'showLayer2Points':
				debugState.showLayer2Points = enabled;
				break;
			case 'showAdjustmentVectors':
				debugState.showAdjustmentVectors = enabled;
				break;
		}
	}

	// Handle auto-update toggle
	function handleAutoUpdateToggle(enabled: boolean) {
		debugState.autoUpdate = enabled;
	}

	// Handle manual positioning calculation
	function handleCalculatePositioning() {
		debugState.calculatePositioning();
	}

	// Handle section toggle
	function handleToggleSection(section: string) {
		debugState.toggleSection(section);
	}

	// Handle retry for errors
	function handleRetry() {
		initError = null;
		initializeApp();
	}

	// Initialize the application
	async function initializeApp() {
		try {
			// Initialize sample data (replacing DI container setup for now)
			debugState.initializeSampleData();
			
			// App is ready
			isAppReady = true;
		} catch (error) {
			console.error('Failed to initialize arrow debug:', error);
			initError = error instanceof Error ? error.message : 'Unknown initialization error';
		}
	}

	// Initialize on mount
	onMount(() => {
		initializeApp();
	});

	console.log('🎯 ArrowDebugTab (rebuilt) rendered!');
</script>

<div class="arrow-debug-tab">
	{#if initError}
		<DebugErrorDisplay error={initError} onRetry={handleRetry} />
	{:else if !isAppReady}
		<DebugLoadingState />
	{:else}
		<DebugHeader />

		<main class="debug-main">
			<!-- Left Panel: Controls -->
			<div class="panel control-panel">
				<DebugControls
					selectedPictograph={debugState.selectedPictograph}
					selectedArrowColor={debugState.selectedArrowColor}
					availablePictographs={debugState.availablePictographs}
					stepByStepMode={debugState.stepByStepMode}
					currentStep={debugState.currentStep}
					maxSteps={debugState.maxSteps}
					showCoordinateGrid={debugState.showCoordinateGrid}
					showHandPoints={debugState.showHandPoints}
					showLayer2Points={debugState.showLayer2Points}
					showAdjustmentVectors={debugState.showAdjustmentVectors}
					autoUpdate={debugState.autoUpdate}
					onPictographSelect={handlePictographSelect}
					onArrowColorSelect={handleArrowColorSelect}
					onStepByStepToggle={handleStepByStepToggle}
					onStepChange={handleStepChange}
					onVisualizationToggle={handleVisualizationToggle}
					onAutoUpdateToggle={handleAutoUpdateToggle}
					onCalculatePositioning={handleCalculatePositioning}
				/>
			</div>

			<!-- Center Panel: Visual Canvas -->
			<div class="panel canvas-panel">
				<DebugCanvas
					debugData={debugState.currentDebugData}
					showCoordinateGrid={debugState.showCoordinateGrid}
					showHandPoints={debugState.showHandPoints}
					showLayer2Points={debugState.showLayer2Points}
					showAdjustmentVectors={debugState.showAdjustmentVectors}
					currentStep={debugState.currentStep}
					stepByStepMode={debugState.stepByStepMode}
				/>
			</div>

			<!-- Right Panel: Debug Information -->
			<div class="panel debug-info-panel">
				<DebugInfoPanel
					debugData={debugState.currentDebugData}
					expandedSections={debugState.expandedSections}
					onToggleSection={handleToggleSection}
					isCalculating={debugState.isCalculating}
				/>
			</div>
		</main>
	{/if}
</div>

<style>
	.arrow-debug-tab {
		height: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
		background: transparent;
		color: white;
		padding: 20px;
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
		overflow: hidden;
	}

	.debug-main {
		display: grid;
		grid-template-columns: 320px 1fr 350px;
		gap: 15px;
		flex: 1;
		min-height: 0;
	}

	.panel {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		padding: 16px;
		overflow-y: auto;
	}

	.canvas-panel {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
	}

	/* Responsive design */
	@media (max-width: 1200px) {
		.debug-main {
			grid-template-columns: 280px 1fr 300px;
			gap: 12px;
		}
	}

	@media (max-width: 1000px) {
		.arrow-debug-tab {
			padding: 15px;
		}
		
		.debug-main {
			grid-template-columns: 1fr;
			grid-template-rows: auto auto 1fr;
			gap: 10px;
		}

		.panel {
			min-height: auto;
			padding: 12px;
		}
	}

	@media (max-width: 768px) {
		.arrow-debug-tab {
			padding: 10px;
		}

		.panel {
			padding: 10px;
		}
	}

	/* Scrollbar styling for webkit browsers */
	.panel::-webkit-scrollbar {
		width: 6px;
	}

	.panel::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}

	.panel::-webkit-scrollbar-thumb {
		background: rgba(251, 191, 36, 0.5);
		border-radius: 3px;
	}

	.panel::-webkit-scrollbar-thumb:hover {
		background: rgba(251, 191, 36, 0.7);
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.arrow-debug-tab {
			transition: none;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.panel {
			border: 2px solid white;
			background: rgba(0, 0, 0, 0.8);
		}
	}
</style>
