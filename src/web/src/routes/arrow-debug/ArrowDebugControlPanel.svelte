<script lang="ts">

	import type { ArrowDebugState } from './state/arrow-debug-state.svelte';
	import QuickTestActions from './components/QuickTestActions.svelte';

	interface Props {
		state: ArrowDebugState;
	}

	let { state: debugState }: Props = $props();

	// Local reactive state for UI
	let loadingPictographs = $state(false);

	function handlePictographSelect(event: Event) {
		const target = event.target as HTMLSelectElement;
		const index = parseInt(target.value);
		if (index >= 0 && index < debugState.availablePictographs.length) {
			debugState.selectedPictograph = debugState.availablePictographs[index];
		}
	}

	function handleArrowColorChange(color: 'red' | 'blue') {
		debugState.selectedArrowColor = color;
	}

	function toggleStepByStepMode() {
		debugState.stepByStepMode = !debugState.stepByStepMode;
		if (!debugState.stepByStepMode) {
			debugState.currentStep = debugState.maxSteps; // Show all steps
		}
	}

	function nextStep() {
		if (debugState.currentStep < debugState.maxSteps) {
			debugState.currentStep++;
		}
	}

	function prevStep() {
		if (debugState.currentStep > 0) {
			debugState.currentStep--;
		}
	}

	function resetSteps() {
		debugState.currentStep = 0;
	}

	async function recalculatePositioning() {
		await debugState.calculateFullPositioning();
	}

	async function loadRealPictographs() {
		loadingPictographs = true;
		try {
			// In a real implementation, this would load actual pictograph data
			// For now, we'll add more diverse sample data
			await debugState.loadSamplePictographs();
		} catch (error) {
			console.error('Failed to load pictographs:', error);
		} finally {
			loadingPictographs = false;
		}
	}

	// Generate step names for UI
	const stepNames = [
		'Input Data',
		'Location Calculation', 
		'Initial Position',
		'Default Adjustment',
		'Special Adjustment',
		'Final Position'
	];
</script>

<div class="control-panel">
	<h2>🎮 Debug Controls</h2>

	<!-- Pictograph Selection -->
	<section class="control-section">
		<h3>📊 Pictograph Data</h3>
		
		<div class="control-group">
			<label for="pictograph-select">Select Pictograph:</label>
			<select
				id="pictograph-select"
				onchange={handlePictographSelect}
				disabled={debugState.isCalculating}
			>
				{#each debugState.availablePictographs as pictograph, index}
					<option value={index} selected={debugState.selectedPictograph === pictograph}>
						Letter {pictograph.letter} ({pictograph.grid_mode})
					</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<span class="control-label">Arrow Color:</span>
			<div class="arrow-color-buttons" role="group" aria-label="Arrow color selection">
				<button
					class="color-btn blue {debugState.selectedArrowColor === 'blue' ? 'active' : ''}"
					onclick={() => handleArrowColorChange('blue')}
					disabled={debugState.isCalculating}
				>
					🔵 Blue
				</button>
				<button
					class="color-btn red {debugState.selectedArrowColor === 'red' ? 'active' : ''}"
					onclick={() => handleArrowColorChange('red')}
					disabled={debugState.isCalculating}
				>
					🔴 Red
				</button>
			</div>
		</div>

		<button
			class="load-btn"
			onclick={loadRealPictographs}
			disabled={loadingPictographs || debugState.isCalculating}
		>
			{loadingPictographs ? '⏳ Loading...' : '📁 Load Real Data'}
		</button>
	</section>

	<!-- Step Control -->
	<section class="control-section">
		<h3>🔍 Step-by-Step Analysis</h3>
		
		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.stepByStepMode}
					onchange={toggleStepByStepMode}
				/>
				Enable Step-by-Step Mode
			</label>
		</div>

		{#if debugState.stepByStepMode}
			<div class="step-controls">
				<div class="step-info">
					<span class="step-counter">
						Step {debugState.currentStep + 1} of {debugState.maxSteps + 1}
					</span>
					<span class="step-name">
						{stepNames[debugState.currentStep] || 'Complete'}
					</span>
				</div>

				<div class="step-buttons">
					<button
						onclick={resetSteps}
						disabled={debugState.currentStep === 0 || debugState.isCalculating}
						title="Reset to beginning"
					>
						⏮️
					</button>
					<button
						onclick={prevStep}
						disabled={debugState.currentStep === 0 || debugState.isCalculating}
						title="Previous step"
					>
						⏪
					</button>
					<button
						onclick={nextStep}
						disabled={debugState.currentStep >= debugState.maxSteps || debugState.isCalculating}
						title="Next step"
					>
						⏩
					</button>
				</div>
			</div>

			<div class="step-progress">
				<div class="progress-bar">
					<div
						class="progress-fill"
						style="width: {((debugState.currentStep + 1) / (debugState.maxSteps + 1)) * 100}%"
					></div>
				</div>
			</div>
		{/if}
	</section>

	<!-- Visualization Options -->
	<section class="control-section">
		<h3>👁️ Visualization</h3>
		
		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.showCoordinateGrid}
					onchange={(e) => debugState.showCoordinateGrid = (e.target as HTMLInputElement).checked}
				/>
				Show Coordinate Grid
			</label>
		</div>

		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.showHandPoints}
					onchange={(e) => debugState.showHandPoints = (e.target as HTMLInputElement).checked}
				/>
				Show Hand Points
			</label>
		</div>

		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.showLayer2Points}
					onchange={(e) => debugState.showLayer2Points = (e.target as HTMLInputElement).checked}
				/>
				Show Layer2 Points
			</label>
		</div>

		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.showAdjustmentVectors}
					onchange={(e) => debugState.showAdjustmentVectors = (e.target as HTMLInputElement).checked}
				/>
				Show Adjustment Vectors
			</label>
		</div>
	</section>

	<!-- Calculation Control -->
	<section class="control-section">
		<h3>⚙️ Calculation</h3>
		
		<div class="control-group">
			<label class="checkbox-label">
				<input
					type="checkbox"
					checked={debugState.autoUpdate}
					onchange={(e) => debugState.autoUpdate = (e.target as HTMLInputElement).checked}
				/>
				Auto-update on changes
			</label>
		</div>

		<button 
			class="calculate-btn"
			onclick={recalculatePositioning}
			disabled={debugState.isCalculating || !debugState.selectedPictograph}
		>
			{debugState.isCalculating ? '⏳ Calculating...' : '🔄 Recalculate'}
		</button>
	</section>

	<!-- Quick Test Actions -->
	<QuickTestActions state={debugState} />

	<!-- Current Input Summary -->
	{#if debugState.selectedPictograph && debugState.currentMotionData}
		<section class="control-section">
			<h3>📋 Current Input</h3>
			<div class="input-summary">
				<div class="summary-item">
					<span class="label">Letter:</span>
					<span class="value">{debugState.selectedPictograph.letter}</span>
				</div>
				<div class="summary-item">
					<span class="label">Grid Mode:</span>
					<span class="value">{debugState.selectedPictograph.grid_mode}</span>
				</div>
				<div class="summary-item">
					<span class="label">Motion Type:</span>
					<span class="value">{debugState.currentMotionData.motion_type}</span>
				</div>
				<div class="summary-item">
					<span class="label">Start→End:</span>
					<span class="value">{debugState.currentMotionData.start_ori}→{debugState.currentMotionData.end_ori}</span>
				</div>
				<div class="summary-item">
					<span class="label">Turns:</span>
					<span class="value">{debugState.currentMotionData.turns}</span>
				</div>
				<div class="summary-item">
					<span class="label">Rotation:</span>
					<span class="value">{debugState.currentMotionData.prop_rot_dir}</span>
				</div>
			</div>
		</section>
	{/if}
</div>

<style>
	.control-panel {
		display: flex;
		flex-direction: column;
		gap: 20px;
		height: 100%;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #fbbf24;
		font-size: 1.3rem;
		border-bottom: 2px solid rgba(251, 191, 36, 0.3);
		padding-bottom: 10px;
		text-align: center;
	}

	h3 {
		margin: 0 0 15px 0;
		color: #fde047;
		font-size: 1rem;
		font-weight: 600;
		border-bottom: 1px solid rgba(253, 224, 71, 0.2);
		padding-bottom: 8px;
	}

	.control-section {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 15px;
	}

	.control-group {
		margin-bottom: 12px;
	}

	label {
		display: block;
		color: #c7d2fe;
		font-size: 0.9rem;
		margin-bottom: 5px;
		font-weight: 500;
	}

	select {
		width: 100%;
		padding: 8px 12px;
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		color: white;
		font-size: 0.9rem;
	}

	select:focus {
		outline: none;
		border-color: #fbbf24;
		box-shadow: 0 0 0 2px rgba(251, 191, 36, 0.2);
	}

	.arrow-color-buttons {
		display: flex;
		gap: 8px;
	}

	.color-btn {
		flex: 1;
		padding: 8px 12px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(0, 0, 0, 0.4);
		color: white;
		font-size: 0.9rem;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.color-btn:hover {
		background: rgba(255, 255, 255, 0.1);
	}

	.color-btn.active {
		border-color: #fbbf24;
		background: rgba(251, 191, 36, 0.2);
	}

	.color-btn.blue.active {
		border-color: #60a5fa;
		background: rgba(96, 165, 250, 0.2);
	}

	.color-btn.red.active {
		border-color: #f87171;
		background: rgba(248, 113, 113, 0.2);
	}

	.load-btn, .calculate-btn {
		width: 100%;
		padding: 10px 16px;
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		border: none;
		border-radius: 8px;
		color: white;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.9rem;
	}

	.load-btn:hover, .calculate-btn:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
	}

	.load-btn:disabled, .calculate-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
		box-shadow: none;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 8px;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.checkbox-label input[type="checkbox"] {
		width: auto;
		margin: 0;
	}

	.step-controls {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.step-info {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.step-counter {
		font-size: 0.8rem;
		color: #a3a3a3;
	}

	.step-name {
		font-size: 0.9rem;
		color: #fbbf24;
		font-weight: 600;
	}

	.step-buttons {
		display: flex;
		gap: 6px;
		justify-content: center;
	}

	.step-buttons button {
		padding: 6px 12px;
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		color: white;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.step-buttons button:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.1);
		border-color: #fbbf24;
	}

	.step-buttons button:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.step-progress {
		margin-top: 10px;
	}

	.progress-bar {
		width: 100%;
		height: 6px;
		background: rgba(0, 0, 0, 0.4);
		border-radius: 3px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #fbbf24, #f59e0b);
		transition: width 0.3s ease;
	}

	.input-summary {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.summary-item {
		display: flex;
		justify-content: space-between;
		font-size: 0.8rem;
	}

	.summary-item .label {
		color: #a3a3a3;
		margin-bottom: 0;
	}

	.summary-item .value {
		color: #fbbf24;
		font-weight: 600;
		font-family: 'Courier New', monospace;
	}
</style>
