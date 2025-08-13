<script lang="ts">
	/**
	 * Debug Controls Component
	 * Handles pictograph selection, arrow color selection, and debug settings
	 */

	import type { PictographData } from '$lib/domain';

	interface Props {
		selectedPictograph: PictographData | null;
		selectedArrowColor: 'red' | 'blue';
		availablePictographs: PictographData[];
		stepByStepMode: boolean;
		currentStep: number;
		maxSteps: number;
		showCoordinateGrid: boolean;
		showHandPoints: boolean;
		showLayer2Points: boolean;
		showAdjustmentVectors: boolean;
		autoUpdate: boolean;
		onPictographSelect: (pictograph: PictographData) => void;
		onArrowColorSelect: (color: 'red' | 'blue') => void;
		onStepByStepToggle: (enabled: boolean) => void;
		onStepChange: (step: number) => void;
		onVisualizationToggle: (setting: string, enabled: boolean) => void;
		onAutoUpdateToggle: (enabled: boolean) => void;
		onCalculatePositioning: () => void;
	}

	let {
		selectedPictograph,
		selectedArrowColor,
		availablePictographs,
		stepByStepMode,
		currentStep,
		maxSteps,
		showCoordinateGrid,
		showHandPoints,
		showLayer2Points,
		showAdjustmentVectors,
		autoUpdate,
		onPictographSelect,
		onArrowColorSelect,
		onStepByStepToggle,
		onStepChange,
		onVisualizationToggle,
		onAutoUpdateToggle,
		onCalculatePositioning
	}: Props = $props();

	function handlePictographChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const pictograph = availablePictographs.find(p => p.id === target.value);
		if (pictograph) {
			onPictographSelect(pictograph);
		}
	}

	function handleArrowColorChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		onArrowColorSelect(target.value as 'red' | 'blue');
	}
</script>

<div class="debug-controls">
	<div class="section">
		<h3>📋 Pictograph Selection</h3>
		<div class="control-group">
			<label for="pictograph-select">Pictograph:</label>
			<select 
				id="pictograph-select"
				value={selectedPictograph?.id || ''}
				onchange={handlePictographChange}
			>
				<option value="">Select a pictograph</option>
				{#each availablePictographs as pictograph}
					<option value={pictograph.id}>
						{pictograph.letter || pictograph.id.slice(0, 8)}
					</option>
				{/each}
			</select>
		</div>
		
		<div class="control-group">
			<label for="arrow-color-select">Arrow Color:</label>
			<select 
				id="arrow-color-select"
				value={selectedArrowColor}
				onchange={handleArrowColorChange}
			>
				<option value="blue">Blue Arrow</option>
				<option value="red">Red Arrow</option>
			</select>
		</div>
	</div>

	<div class="section">
		<h3>⚙️ Debug Settings</h3>
		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={stepByStepMode}
					onchange={(e) => onStepByStepToggle(e.currentTarget.checked)}
				/>
				Step-by-step mode
			</label>
		</div>

		{#if stepByStepMode}
			<div class="control-group">
				<label for="step-slider">Current Step: {currentStep}</label>
				<input 
					id="step-slider"
					type="range" 
					min="0" 
					max={maxSteps}
					value={currentStep}
					onchange={(e) => onStepChange(parseInt(e.currentTarget.value))}
				/>
			</div>
		{/if}

		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={autoUpdate}
					onchange={(e) => onAutoUpdateToggle(e.currentTarget.checked)}
				/>
				Auto-update positioning
			</label>
		</div>
	</div>

	<div class="section">
		<h3>👁️ Visualization</h3>
		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={showCoordinateGrid}
					onchange={(e) => onVisualizationToggle('showCoordinateGrid', e.currentTarget.checked)}
				/>
				Coordinate grid
			</label>
		</div>
		
		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={showHandPoints}
					onchange={(e) => onVisualizationToggle('showHandPoints', e.currentTarget.checked)}
				/>
				Hand points
			</label>
		</div>
		
		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={showLayer2Points}
					onchange={(e) => onVisualizationToggle('showLayer2Points', e.currentTarget.checked)}
				/>
				Layer 2 points
			</label>
		</div>
		
		<div class="control-group">
			<label>
				<input 
					type="checkbox" 
					checked={showAdjustmentVectors}
					onchange={(e) => onVisualizationToggle('showAdjustmentVectors', e.currentTarget.checked)}
				/>
				Adjustment vectors
			</label>
		</div>
	</div>

	<div class="section">
		<h3>🔄 Actions</h3>
		<button class="calculate-btn" onclick={onCalculatePositioning}>
			Calculate Positioning
		</button>
	</div>
</div>

<style>
	.debug-controls {
		display: flex;
		flex-direction: column;
		gap: 20px;
		height: 100%;
		overflow-y: auto;
	}

	.section {
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		padding: 16px;
		background: rgba(255, 255, 255, 0.05);
	}

	.section h3 {
		margin: 0 0 12px 0;
		color: #fbbf24;
		font-size: 1rem;
		font-weight: 600;
	}

	.control-group {
		margin-bottom: 12px;
	}

	.control-group:last-child {
		margin-bottom: 0;
	}

	label {
		display: block;
		color: #c7d2fe;
		font-size: 0.9rem;
		margin-bottom: 4px;
		cursor: pointer;
	}

	label input[type="checkbox"] {
		margin-right: 8px;
	}

	select, input[type="range"] {
		width: 100%;
		padding: 8px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		background: rgba(0, 0, 0, 0.3);
		color: white;
		font-size: 0.9rem;
	}

	select:focus, input:focus {
		outline: none;
		border-color: #fbbf24;
		box-shadow: 0 0 0 2px rgba(251, 191, 36, 0.2);
	}

	input[type="range"] {
		background: transparent;
		-webkit-appearance: none;
		appearance: none;
		height: 6px;
		border-radius: 3px;
		background: rgba(255, 255, 255, 0.2);
		outline: none;
	}

	input[type="range"]::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 18px;
		height: 18px;
		border-radius: 50%;
		background: #fbbf24;
		cursor: pointer;
	}

	input[type="range"]::-moz-range-thumb {
		width: 18px;
		height: 18px;
		border-radius: 50%;
		background: #fbbf24;
		cursor: pointer;
		border: none;
	}

	.calculate-btn {
		width: 100%;
		padding: 12px;
		background: linear-gradient(135deg, #fbbf24, #f59e0b);
		border: none;
		border-radius: 6px;
		color: black;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.calculate-btn:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
	}

	.calculate-btn:active {
		transform: translateY(0);
	}
</style>
