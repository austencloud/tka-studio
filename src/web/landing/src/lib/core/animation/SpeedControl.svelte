<script lang="ts">
	interface Props {
		speed: number;
		onSpeedChange: (speed: number) => void;
	}

	let { speed, onSpeedChange }: Props = $props();

	function handleSpeedChange(event: Event) {
		const newSpeed = parseFloat((event.target as HTMLInputElement).value);
		onSpeedChange(newSpeed);
	}
</script>

<div class="control-group">
	<label for="speedSlider">Speed:</label>
	<input 
		type="range" 
		id="speedSlider" 
		min="0.1" 
		max="3" 
		step="0.1" 
		value={speed} 
		class="slider"
		oninput={handleSpeedChange}
	/>
	<span class="value-display">{speed.toFixed(1)}x</span>
</div>

<style>
	.control-group {
		display: flex;
		gap: 0.75rem;
		align-items: center;
	}

	.control-group label {
		font-size: 0.875rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.9);
		white-space: nowrap;
	}

	.slider {
		width: 120px;
		height: 6px;
		border-radius: 3px;
		background: rgba(255, 255, 255, 0.2);
		outline: none;
		cursor: pointer;
		appearance: none;
		-webkit-appearance: none;
	}

	.slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 18px;
		height: 18px;
		border-radius: 50%;
		background: rgba(59, 130, 246, 0.9);
		cursor: pointer;
		border: 2px solid white;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.slider::-moz-range-thumb {
		width: 18px;
		height: 18px;
		border-radius: 50%;
		background: rgba(59, 130, 246, 0.9);
		cursor: pointer;
		border: 2px solid white;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.value-display {
		font-weight: 600;
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.875rem;
		min-width: 3rem;
		text-align: center;
		color: rgba(255, 255, 255, 0.9);
	}
</style>
