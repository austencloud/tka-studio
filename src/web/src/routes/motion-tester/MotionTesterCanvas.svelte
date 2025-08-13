<script lang="ts">
	import type { MotionTesterState } from './state/motion-tester-state.svelte';
	import { AnimatorCanvas } from '$lib/animator';
	import AnimationControl from './components/AnimationControl.svelte';
	import GridOptionsControl from './components/GridOptionsControl.svelte';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	// Animation control handlers
	function handlePlayPause() {
		if (state.animationState.isPlaying) {
			state.stopAnimation();
		} else {
			state.startAnimation();
		}
	}
</script>

<div class="canvas-container">
	<h2>🎬 Motion Visualization</h2>
	
	{#if state.isEngineInitialized}
		<div class="animator-canvas-wrapper">
			<AnimatorCanvas
				blueProp={state.currentPropStates.blue || { x: 0, y: 0, centerPathAngle: 0, staffRotationAngle: 0 }}
				redProp={state.currentPropStates.red || { x: 0, y: 0, centerPathAngle: 0, staffRotationAngle: 0 }}
				width={400}
				height={400}
				gridVisible={true}
				gridType={state.gridType}
			/>
		</div>
	{:else}
		<div class="canvas-placeholder">
			<p>Initializing animation engine...</p>
		</div>
	{/if}
	
	<div class="animation-controls">
		<button 
			class="control-btn"
			class:active={state.animationState.isPlaying}
			onclick={state.startAnimation}
			disabled={state.animationState.isPlaying || !state.isEngineInitialized}
		>
			▶ Play
		</button>
		<button
			class="control-btn"
			onclick={state.stopAnimation}
			disabled={!state.animationState.isPlaying}
		>
			⏸ Stop
		</button>
		<button
			class="control-btn"
			onclick={state.resetAnimation}
			disabled={!state.isEngineInitialized}
		>
			⏹ Reset
		</button>
	</div>

	<!-- Progress Control -->
	<div class="progress-section">
		<AnimationControl
			progress={state.animationState.progress}
			isPlaying={state.animationState.isPlaying}
			onProgressChange={state.setProgress}
			onPlayPause={handlePlayPause}
			onReset={state.resetAnimation}
		/>
	</div>

	<!-- Grid Options -->
	<div class="grid-section">
		<h3>🔲 Grid Options</h3>
		<GridOptionsControl
			gridType={state.gridType}
			onGridTypeChange={state.setGridType}
		/>
	</div>



	<!-- Real-time state display -->
	<div class="current-state">
		<h3>Real-Time Prop States</h3>
		<div class="prop-states">
			<div class="prop-state">
				<h4>Blue Prop</h4>
				<div class="state-values">
					<div>Center: {((state.currentPropStates?.blue?.centerPathAngle || 0) * 180 / Math.PI).toFixed(1)}°</div>
					<div>Staff: {((state.currentPropStates?.blue?.staffRotationAngle || 0) * 180 / Math.PI).toFixed(1)}°</div>
				</div>
			</div>
			<div class="prop-state">
				<h4>Red Prop</h4>
				<div class="state-values">
					<div>Center: {((state.currentPropStates?.red?.centerPathAngle || 0) * 180 / Math.PI).toFixed(1)}°</div>
					<div>Staff: {((state.currentPropStates?.red?.staffRotationAngle || 0) * 180 / Math.PI).toFixed(1)}°</div>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.canvas-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
		height: 100%;
		padding: 10px;
	}

	h2 {
		margin: 0;
		color: #e0e7ff;
		font-size: 1.25rem;
		text-align: center;
	}

	.animator-canvas-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 20px;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.08) 0%, 
			rgba(255, 255, 255, 0.04) 100%);
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 16px;
		backdrop-filter: blur(15px);
		box-shadow: 
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.canvas-placeholder {
		width: 400px;
		height: 400px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.05);
		border: 2px dashed rgba(255, 255, 255, 0.3);
		border-radius: 12px;
		color: #c7d2fe;
	}

	.animation-controls {
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
		justify-content: center;
	}

	.control-btn {
		padding: 10px 16px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 8px;
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		color: white;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.3s ease;
		font-size: 14px;
	}

	.control-btn:hover:not(:disabled) {
		background: linear-gradient(135deg, #7c3aed, #a855f7);
		transform: translateY(-2px);
	}

	.control-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none;
	}

	.control-btn.active {
		background: linear-gradient(135deg, #10b981, #059669);
	}



	.current-state {
		background: rgba(34, 197, 94, 0.1);
		border: 1px solid rgba(34, 197, 94, 0.3);
		border-radius: 8px;
		padding: 15px;
		margin-top: 10px;
		min-width: 300px;
	}

	.current-state h3 {
		margin: 0 0 10px 0;
		color: #4ade80;
		font-size: 1rem;
		text-align: center;
	}

	.prop-states {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.prop-state h4 {
		margin: 0 0 8px 0;
		font-size: 0.9rem;
		text-align: center;
	}

	.prop-state h4:first-of-type {
		color: #60a5fa;
	}

	.prop-state:last-child h4 {
		color: #f87171;
	}

	.state-values {
		font-size: 0.75rem;
		color: #c7d2fe;
		font-family: 'Courier New', monospace;
		line-height: 1.4;
	}

	@media (max-width: 768px) {
		.animator-canvas-wrapper,
		.canvas-placeholder {
			width: 90vw;
			height: 90vw;
			max-width: 350px;
			max-height: 350px;
		}

		.animation-controls {
			gap: 8px;
		}

		.control-btn {
			padding: 8px 12px;
			font-size: 12px;
		}

		.prop-states {
			grid-template-columns: 1fr;
			gap: 10px;
		}

		.current-state {
			min-width: auto;
		}
	}
</style>
