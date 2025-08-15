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
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
	import DebugInfoPanel from './arrow-debug/DebugInfoPanel.svelte';
	import HorizontalDebugSteps from './arrow-debug/HorizontalDebugSteps.svelte';
	import SimplePictographSelector from './arrow-debug/SimplePictographSelector.svelte';
	import DebugErrorDisplay from './arrow-debug/DebugErrorDisplay.svelte';
	import DebugLoadingState from './arrow-debug/DebugLoadingState.svelte';
	import { createDebugState } from './arrow-debug/debug-state.svelte';
	import type { PictographData } from '$lib/domain';

	// Application state
	let isAppReady = $state(false);
	let initError = $state<string | null>(null);

	// Create debug state
	const debugState = createDebugState();

	// Codex state
	let codexVisible = $state(false);

	// Handle pictograph selection from dropdown (legacy)
	function handlePictographSelect(pictograph: any) {
		debugState.selectedPictograph = pictograph;
	}

	// Handle pictograph selection from codex
	function handleCodexPictographSelected(pictograph: PictographData) {
		debugState.selectedPictograph = pictograph;
		// Optionally close codex after selection
		// codexVisible = false;
	}

	// Handle codex toggle
	function handleCodexToggle() {
		codexVisible = !codexVisible;
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

	// Handle grid mode change
	function handleGridModeChange(mode: 'diamond' | 'box') {
		debugState.gridMode = mode;
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
			console.log('🚀 Initializing Arrow Debug Tab with real data...');

			// Initialize real pictograph data from CSV
			await debugState.initializeRealData();

			// App is ready
			isAppReady = true;
			console.log('✅ Arrow Debug Tab initialized successfully');
		} catch (error) {
			console.error('❌ Failed to initialize arrow debug:', error);
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
			<!-- Left Panel: Simplified Pictograph Selector -->
			<div class="panel codex-main-panel">
				<SimplePictographSelector
					onPictographSelected={handleCodexPictographSelected}
					selectedPictograph={debugState.selectedPictograph}
				/>
			</div>

			<!-- Right Panel: Visualization and Controls -->
			<div class="panel visualization-panel">
				{#if debugState.selectedPictograph}
					<div class="pictograph-container">
						<h3>🎯 Pictograph Visualization</h3>
						<Pictograph
							pictographData={debugState.selectedPictograph}
							width={400}
							height={400}
							debug={true}
						/>

						<!-- Visualization Controls -->
						<div class="visualization-controls">
							<div class="control-group">
								<h4>🔲 Grid Mode</h4>
								<div class="grid-toggle">
									<button
										class="grid-btn {debugState.gridMode === 'diamond' ? 'active' : ''}"
										onclick={() => handleGridModeChange('diamond')}
									>
										◆ Diamond
									</button>
									<button
										class="grid-btn {debugState.gridMode === 'box' ? 'active' : ''}"
										onclick={() => handleGridModeChange('box')}
									>
										⬜ Box
									</button>
								</div>
							</div>

							<div class="control-group">
								<h4>⚙️ Debug Settings</h4>
								<label class="checkbox-label">
									<input
										type="checkbox"
										bind:checked={debugState.stepByStepMode}
										onchange={() => handleStepByStepToggle(debugState.stepByStepMode)}
									/>
									Step-by-step mode
								</label>
								<label class="checkbox-label">
									<input
										type="checkbox"
										bind:checked={debugState.autoUpdate}
										onchange={() => handleAutoUpdateToggle(debugState.autoUpdate)}
									/>
									Auto-update
								</label>
							</div>

							<div class="control-group">
								<button
									class="calculate-btn"
									onclick={handleCalculatePositioning}
									disabled={debugState.isCalculating}
								>
									{debugState.isCalculating ? '⏳ Calculating...' : '🔄 Calculate Positioning'}
								</button>
							</div>
						</div>

						<!-- Arrow Position Data for Both Colors -->
						{#if debugState.currentDebugData.finalPosition}
							<div class="arrow-positions">
								<h4>📍 Arrow Positions</h4>
								<div class="position-cards">
									{#if debugState.selectedPictograph?.arrows?.red}
										<div class="position-card red">
											<h5>🔴 Red Arrow</h5>
											<p>X: {debugState.currentDebugData.finalPosition.x.toFixed(2)}</p>
											<p>Y: {debugState.currentDebugData.finalPosition.y.toFixed(2)}</p>
											<p>Rotation: {debugState.currentDebugData.finalRotation.toFixed(2)}°</p>
										</div>
									{/if}
									{#if debugState.selectedPictograph?.arrows?.blue}
										<div class="position-card blue">
											<h5>🔵 Blue Arrow</h5>
											<p>X: {debugState.currentDebugData.finalPosition.x.toFixed(2)}</p>
											<p>Y: {debugState.currentDebugData.finalPosition.y.toFixed(2)}</p>
											<p>Rotation: {debugState.currentDebugData.finalRotation.toFixed(2)}°</p>
										</div>
									{/if}
								</div>
							</div>
						{/if}

						{#if debugState.currentDebugData.errors.length > 0}
							<div class="debug-overlay">
								<h4>⚠️ Positioning Errors:</h4>
								<ul>
									{#each debugState.currentDebugData.errors as error}
										<li>{error.step}: {error.error}</li>
									{/each}
								</ul>
							</div>
						{/if}
					</div>
				{:else}
					<div class="no-pictograph">
						<p>Select a pictograph from the codex to view visualization</p>
					</div>
				{/if}
			</div>
		</main>

		<!-- Bottom Panel: Debug Steps (Horizontal) -->
		{#if debugState.selectedPictograph}
			<div class="debug-steps-panel">
				<HorizontalDebugSteps
					debugData={debugState.stepByStepMode ? debugState.currentStepData : debugState.currentDebugData}
					currentStep={debugState.currentStep}
					maxSteps={debugState.maxSteps}
					stepByStepMode={debugState.stepByStepMode}
					onStepChange={handleStepChange}
				/>
			</div>
		{/if}
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
		grid-template-columns: 1fr 1fr;
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

	.codex-main-panel {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.visualization-panel {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-start;
		background: rgba(255, 255, 255, 0.05);
	}

	.debug-steps-panel {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		padding: 16px;
		margin: 16px;
		min-height: 300px;
		max-height: 400px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	/* Pictograph container styles */
	.pictograph-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
		width: 100%;
		max-width: 500px;
	}

	.pictograph-container h3 {
		color: #fbbf24;
		margin: 0;
		font-size: 1.1rem;
		text-align: center;
	}

	.debug-overlay {
		background: rgba(0, 0, 0, 0.7);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 12px;
		margin-top: 8px;
		width: 100%;
		max-width: 400px;
	}

	.debug-overlay h4 {
		color: #fbbf24;
		margin: 0 0 8px 0;
		font-size: 0.9rem;
	}

	.debug-overlay ul {
		margin: 0;
		padding-left: 16px;
		color: #f87171;
	}

	.debug-overlay li {
		font-size: 0.85rem;
		margin: 4px 0;
	}

	.no-pictograph {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 200px;
		color: rgba(255, 255, 255, 0.5);
		font-style: italic;
	}

	/* Visualization controls */
	.visualization-controls {
		display: flex;
		flex-direction: column;
		gap: 16px;
		width: 100%;
		max-width: 400px;
		margin-top: 16px;
	}

	.control-group {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 12px;
	}

	.control-group h4 {
		color: #fbbf24;
		margin: 0 0 8px 0;
		font-size: 0.9rem;
	}

	.grid-toggle {
		display: flex;
		gap: 8px;
	}

	.grid-btn {
		flex: 1;
		padding: 8px 12px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		background: rgba(0, 0, 0, 0.3);
		color: rgba(255, 255, 255, 0.7);
		font-size: 0.9rem;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.grid-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		color: white;
	}

	.grid-btn.active {
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		color: black;
		border-color: #fbbf24;
		font-weight: 600;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 8px;
		color: rgba(255, 255, 255, 0.8);
		font-size: 0.9rem;
		margin: 4px 0;
		cursor: pointer;
	}

	.calculate-btn {
		width: 100%;
		padding: 12px;
		background: linear-gradient(135deg, #10b981, #059669);
		border: none;
		border-radius: 6px;
		color: white;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.calculate-btn:hover:not(:disabled) {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
	}

	.calculate-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
	}

	/* Arrow position cards */
	.arrow-positions {
		width: 100%;
		max-width: 400px;
		margin-top: 16px;
	}

	.arrow-positions h4 {
		color: #fbbf24;
		margin: 0 0 12px 0;
		font-size: 1rem;
		text-align: center;
	}

	.position-cards {
		display: flex;
		gap: 12px;
	}

	.position-card {
		flex: 1;
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 12px;
	}

	.position-card.red {
		border-color: #ef4444;
	}

	.position-card.blue {
		border-color: #3b82f6;
	}

	.position-card h5 {
		margin: 0 0 8px 0;
		font-size: 0.9rem;
		text-align: center;
	}

	.position-card p {
		color: #c7d2fe;
		margin: 4px 0;
		font-size: 0.85rem;
		font-family: 'Courier New', monospace;
		text-align: center;
	}

	/* Responsive design */
	@media (max-width: 1200px) {
		.debug-main {
			grid-template-columns: 1fr 1fr;
			gap: 12px;
		}
	}

	@media (max-width: 1000px) {
		.arrow-debug-tab {
			padding: 15px;
		}
		
		.debug-main {
			grid-template-columns: 1fr;
			grid-template-rows: auto auto;
			gap: 10px;
		}

		.panel {
			min-height: auto;
			padding: 12px;
		}

		.position-cards {
			flex-direction: column;
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
