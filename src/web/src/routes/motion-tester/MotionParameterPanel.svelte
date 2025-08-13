<script lang="ts">
	import type { MotionTesterState } from './motion-tester-state.svelte.ts';

	interface Props {
		state: MotionTesterState;
	}

	let { state }: Props = $props();

	// Location grid layout
	const locationGrid = [
		[null, 'n', null],
		['w', 'center', 'e'],
		[null, 's', null]
	];

	function handleLocationClick(location: string, isStart: boolean) {
		if (isStart) {
			state.setStartLocation(location);
		} else {
			state.setEndLocation(location);
		}
	}
</script>

<div class="motion-params-panel">
	<h2>🎯 Motion Parameters</h2>
	
	<!-- Start Location Grid -->
	<div class="input-group">
		<label for="start-location-grid">Start Location</label>
		<div id="start-location-grid" class="location-grid" role="group" aria-labelledby="start-location-grid">
			{#each locationGrid as row}
				<div class="location-row">
					{#each row as location}
						{#if location}
							<button 
								class="location-btn"
								class:active={state.motionParams.startLoc === location}
								onclick={() => handleLocationClick(location, true)}
							>
								{location === 'center' ? '⊙' : location.toUpperCase()}
							</button>
						{:else}
							<div class="location-spacer"></div>
						{/if}
					{/each}
				</div>
			{/each}
		</div>
	</div>

	<!-- End Location Grid -->
	<div class="input-group">
		<label for="end-location-grid">End Location</label>
		<div id="end-location-grid" class="location-grid" role="group" aria-labelledby="end-location-grid">
			{#each locationGrid as row}
				<div class="location-row">
					{#each row as location}
						{#if location}
							<button 
								class="location-btn"
								class:active={state.motionParams.endLoc === location}
								onclick={() => handleLocationClick(location, false)}
							>
								{location === 'center' ? '⊙' : location.toUpperCase()}
							</button>
						{:else}
							<div class="location-spacer"></div>
						{/if}
					{/each}
				</div>
			{/each}
		</div>
	</div>

	<!-- Motion Type -->
	<div class="input-group">
		<label for="motionType">Motion Type</label>
		<select 
			id="motionType"
			value={state.motionParams.motionType}
			onchange={(e) => state.updateMotionParam('motionType', e.currentTarget.value)}
		>
			<option value="pro">Pro</option>
			<option value="anti">Anti</option>
			<option value="static">Static</option>
			<option value="dash">Dash</option>
			<option value="fl">Float</option>
			<option value="none">None</option>
		</select>
	</div>

	<!-- Turns -->
	<div class="input-group">
		<label for="turns">Turns</label>
		<input 
			id="turns"
			type="number" 
			min="0" 
			max="10" 
			step="0.5"
			value={state.motionParams.turns}
			oninput={(e) => state.updateMotionParam('turns', parseFloat(e.currentTarget.value) || 0)}
		>
	</div>

	<!-- Rotation Direction -->
	<div class="input-group">
		<label for="propRotDir">Rotation Direction</label>
		<select 
			id="propRotDir"
			value={state.motionParams.propRotDir}
			onchange={(e) => state.updateMotionParam('propRotDir', e.currentTarget.value)}
		>
			<option value="cw">Clockwise (CW)</option>
			<option value="ccw">Counter-Clockwise (CCW)</option>
			<option value="no_rot">No Rotation</option>
		</select>
	</div>

	<!-- Start Orientation -->
	<div class="input-group">
		<label for="startOri">Start Orientation</label>
		<select 
			id="startOri"
			value={state.motionParams.startOri}
			onchange={(e) => state.updateMotionParam('startOri', e.currentTarget.value)}
		>
			<option value="in">In</option>
			<option value="out">Out</option>
			<option value="n">North</option>
			<option value="e">East</option>
			<option value="s">South</option>
			<option value="w">West</option>
			<option value="clock">Clock</option>
			<option value="counter">Counter</option>
		</select>
	</div>

	<!-- End Orientation -->
	<div class="input-group">
		<label for="endOri">End Orientation</label>
		<select 
			id="endOri"
			value={state.motionParams.endOri}
			onchange={(e) => state.updateMotionParam('endOri', e.currentTarget.value)}
		>
			<option value="in">In</option>
			<option value="out">Out</option>
			<option value="n">North</option>
			<option value="e">East</option>
			<option value="s">South</option>
			<option value="w">West</option>
			<option value="clock">Clock</option>
			<option value="counter">Counter</option>
		</select>
	</div>

	<!-- Motion Info Display -->
	<div class="motion-info">
		<h3>Current Motion</h3>
		<div class="motion-description">{state.motionDescription}</div>
	</div>

	<!-- Progress Control -->
	<div class="input-group">
		<label for="progressSlider">Animation Progress</label>
		<div class="slider-container">
			<input 
				id="progressSlider"
				type="range" 
				min="0" 
				max="100" 
				value={state.animationState.progress * 100}
				oninput={(e) => state.setProgress(parseFloat(e.currentTarget.value) / 100)}
			>
			<div class="slider-value">
				{(state.animationState.progress * 100).toFixed(1)}%
			</div>
		</div>
	</div>

	<!-- Animation Speed -->
	<div class="input-group">
		<label for="speedSlider">Animation Speed</label>
		<div class="slider-container">
			<input 
				id="speedSlider"
				type="range" 
				min="1" 
				max="100" 
				value={state.animationState.speed * 1000}
				oninput={(e) => state.setSpeed(parseFloat(e.currentTarget.value) / 1000)}
			>
			<div class="slider-value">
				{(state.animationState.speed * 1000).toFixed(0)}%
			</div>
		</div>
	</div>

	<!-- Orientation Visualizer -->
	<div class="orientation-visualizer">
		<div class="orientation-display">
			<h4>Start Orientation</h4>
			<div class="orientation-arrow">{state.getOrientationArrow(state.motionParams.startOri)}</div>
			<div class="orientation-text">{state.motionParams.startOri}</div>
		</div>
		<div class="orientation-display">
			<h4>End Orientation</h4>
			<div class="orientation-arrow">{state.getOrientationArrow(state.motionParams.endOri)}</div>
			<div class="orientation-text">{state.motionParams.endOri}</div>
		</div>
	</div>
</div>

<style>
	.motion-params-panel {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	h2 {
		margin: 0 0 20px 0;
		color: #e0e7ff;
		font-size: 1.25rem;
		border-bottom: 2px solid rgba(99, 102, 241, 0.3);
		padding-bottom: 10px;
	}

	.input-group {
		display: flex;
		flex-direction: column;
	}

	.input-group label {
		margin-bottom: 8px;
		font-weight: 500;
		color: #c7d2fe;
		font-size: 0.9rem;
	}

	.input-group select,
	.input-group input[type="number"],
	.input-group input[type="range"] {
		padding: 8px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		font-size: 14px;
	}

	.input-group select option {
		background: #312e81;
		color: white;
	}

	.location-grid {
		display: flex;
		flex-direction: column;
		gap: 6px;
		margin-top: 8px;
	}

	.location-row {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 6px;
	}

	.location-btn {
		padding: 8px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		cursor: pointer;
		transition: all 0.3s ease;
		font-weight: 500;
		font-size: 14px;
	}

	.location-btn:hover {
		background: rgba(99, 102, 241, 0.3);
		border-color: rgba(99, 102, 241, 0.5);
	}

	.location-btn.active {
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		border-color: rgba(255, 255, 255, 0.5);
	}

	.location-spacer {
		height: 40px;
	}

	.motion-info {
		background: rgba(99, 102, 241, 0.1);
		border: 1px solid rgba(99, 102, 241, 0.3);
		border-radius: 8px;
		padding: 15px;
	}

	.motion-info h3 {
		margin: 0 0 10px 0;
		color: #a5b4fc;
		font-size: 1rem;
	}

	.motion-description {
		color: #e0e7ff;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
	}

	.slider-container {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	.slider-value {
		text-align: center;
		font-size: 0.875rem;
		color: #c7d2fe;
		font-family: 'Courier New', monospace;
	}

	.orientation-visualizer {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 10px;
	}

	.orientation-display {
		padding: 12px;
		background: rgba(0, 0, 0, 0.2);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		text-align: center;
	}

	.orientation-display h4 {
		margin: 0 0 8px 0;
		color: #fbbf24;
		font-size: 0.9rem;
	}

	.orientation-arrow {
		font-size: 1.5rem;
		margin: 8px 0;
	}

	.orientation-text {
		font-size: 0.8rem;
		color: #c7d2fe;
		text-transform: capitalize;
	}
</style>
