<script lang="ts">
	import type { MotionTesterState } from './state/motion-tester-state.svelte.ts';
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
	import { createPictographData, createGridData } from '$lib/domain';
	import { GridMode } from '$lib/domain/enums';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	// Simple placeholder pictograph data for now
	let pictographData = $derived(createPictographData({
		id: 'motion-tester-pictograph',
		grid_data: createGridData({
			grid_mode: state.gridType === 'diamond' ? GridMode.DIAMOND : GridMode.BOX
		}),
		arrows: {},
		props: {},
		motions: {},
		letter: 'A',
		beat: 1,
		is_blank: false,
		is_mirrored: false,
		metadata: {}
	}));
</script>

<div class="pictograph-visualization-panel">
	<h2>🎬 Motion Visualization</h2>
	
	<!-- Animation Controls -->
	<div class="animation-controls">
		<div class="playback-controls">
			<button 
				class="control-btn play-btn" 
				onclick={state.animationState.isPlaying ? state.stopAnimation : state.startAnimation}
				disabled={!state.isEngineInitialized}
			>
				{state.animationState.isPlaying ? '⏸️' : '▶️'}
			</button>
			<button 
				class="control-btn reset-btn" 
				onclick={state.resetAnimation}
				disabled={!state.isEngineInitialized}
			>
				⏹️
			</button>
		</div>

		<div class="progress-control">
			<label for="progress-slider">Progress:</label>
			<div class="slider-container">
				<input
					id="progress-slider"
					type="range"
					min="0"
					max="1"
					step="0.01"
					value={state.animationState.progress}
					oninput={(e) => state.setProgress(parseFloat(e.currentTarget.value))}
					disabled={!state.isEngineInitialized}
				/>
				<span class="progress-value">{Math.round(state.animationState.progress * 100)}%</span>
			</div>
		</div>
	</div>

	<!-- Grid Options -->
	<div class="grid-options">
		<h3>🔲 Grid Options</h3>
		<div class="grid-toggle">
			<button 
				class="grid-btn {state.gridType === 'diamond' ? 'active' : ''}"
				onclick={() => state.setGridType('diamond')}
			>
				◆ Diamond
			</button>
			<button 
				class="grid-btn {state.gridType === 'box' ? 'active' : ''}"
				onclick={() => state.setGridType('box')}
			>
				⬜ Box
			</button>
		</div>
	</div>

	<!-- Pictograph Display -->
	<div class="pictograph-container">
		<Pictograph
			{pictographData}
			width={400}
			height={400}
			debug={false}
		/>
	</div>

	<!-- Real-Time Prop States -->
	<div class="prop-states">
		<h3>Real-Time Prop States</h3>
		<div class="prop-states-grid">
			<div class="prop-state blue-state">
				<h4>🔵 Blue Prop</h4>
				<div class="state-values">
					<div class="state-item">
						<span>Center:</span>
						<span>{((state.currentPropStates.blue?.centerPathAngle ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
					</div>
					<div class="state-item">
						<span>Staff:</span>
						<span>{((state.currentPropStates.blue?.staffRotationAngle ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
					</div>
				</div>
			</div>
			<div class="prop-state red-state">
				<h4>🔴 Red Prop</h4>
				<div class="state-values">
					<div class="state-item">
						<span>Center:</span>
						<span>{((state.currentPropStates.red?.centerPathAngle ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
					</div>
					<div class="state-item">
						<span>Staff:</span>
						<span>{((state.currentPropStates.red?.staffRotationAngle ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Motion Summary -->
	<div class="motion-summary">
		<h3>📝 Motion Summary</h3>
		<div class="summary-grid">
			<div class="summary-item">
				<span class="prop-label">🔵 Blue:</span>
				<span class="motion-desc">{state.blueMotionParams.startLoc.toUpperCase()}→{state.blueMotionParams.endLoc.toUpperCase()} {state.blueMotionParams.motionType.toUpperCase()} {state.blueMotionParams.turns}T</span>
			</div>
			<div class="summary-item">
				<span class="prop-label">🔴 Red:</span>
				<span class="motion-desc">{state.redMotionParams.startLoc.toUpperCase()}→{state.redMotionParams.endLoc.toUpperCase()} {state.redMotionParams.motionType.toUpperCase()} {state.redMotionParams.turns}T</span>
			</div>
		</div>
	</div>
</div>

<style>
	.pictograph-visualization-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 20px;
		overflow-y: auto;
	}

	h2 {
		margin: 0 0 15px 0;
		color: #e0e7ff;
		font-size: 1.3rem;
		font-weight: 700;
		text-align: center;
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	h3 {
		margin: 0 0 10px 0;
		color: #c7d2fe;
		font-size: 1rem;
		font-weight: 600;
	}

	/* Animation Controls */
	.animation-controls {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 15px;
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	.playback-controls {
		display: flex;
		gap: 10px;
		justify-content: center;
	}

	.control-btn {
		background: rgba(99, 102, 241, 0.3);
		border: 1px solid rgba(99, 102, 241, 0.5);
		border-radius: 8px;
		color: white;
		padding: 10px 15px;
		cursor: pointer;
		font-size: 16px;
		transition: all 0.2s ease;
		min-width: 50px;
	}

	.control-btn:hover:not(:disabled) {
		background: rgba(99, 102, 241, 0.5);
		transform: translateY(-2px);
	}

	.control-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.progress-control {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.progress-control label {
		color: #c7d2fe;
		font-size: 14px;
		font-weight: 600;
	}

	.slider-container {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.slider-container input[type="range"] {
		flex: 1;
		height: 6px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 3px;
		outline: none;
		-webkit-appearance: none;
		appearance: none;
	}

	.slider-container input[type="range"]::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 18px;
		height: 18px;
		background: #6366f1;
		border-radius: 50%;
		cursor: pointer;
		border: 2px solid white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.progress-value {
		color: #fbbf24;
		font-size: 14px;
		font-weight: 600;
		min-width: 40px;
		text-align: right;
	}

	/* Grid Options */
	.grid-options {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 15px;
	}

	.grid-toggle {
		display: flex;
		gap: 10px;
	}

	.grid-btn {
		flex: 1;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		color: #e0e7ff;
		padding: 10px 15px;
		cursor: pointer;
		font-size: 13px;
		font-weight: 600;
		transition: all 0.2s ease;
	}

	.grid-btn:hover {
		background: rgba(99, 102, 241, 0.2);
		border-color: rgba(99, 102, 241, 0.4);
	}

	.grid-btn.active {
		background: rgba(99, 102, 241, 0.4);
		border-color: rgba(99, 102, 241, 0.6);
		box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
	}

	/* Pictograph Container */
	.pictograph-container {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 20px;
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 400px;
	}

	/* Prop States */
	.prop-states {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 15px;
	}

	.prop-states-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.prop-state {
		background: rgba(0, 0, 0, 0.2);
		border-radius: 8px;
		padding: 12px;
	}

	.prop-state h4 {
		margin: 0 0 8px 0;
		color: #e0e7ff;
		font-size: 14px;
		font-weight: 600;
	}

	.state-values {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.state-item {
		display: flex;
		justify-content: space-between;
		font-size: 12px;
		color: #c7d2fe;
	}

	/* Motion Summary */
	.motion-summary {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1));
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 15px;
	}

	.summary-grid {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.summary-item {
		display: flex;
		align-items: center;
		gap: 10px;
		font-size: 13px;
	}

	.prop-label {
		font-weight: 600;
		color: #e0e7ff;
		min-width: 80px;
	}

	.motion-desc {
		color: #c7d2fe;
		font-family: 'Courier New', monospace;
		background: rgba(99, 102, 241, 0.2);
		padding: 4px 8px;
		border-radius: 4px;
		border: 1px solid rgba(99, 102, 241, 0.3);
	}
</style>
