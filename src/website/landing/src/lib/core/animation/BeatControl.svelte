<script lang="ts">
	interface Props {
		currentBeat: number;
		totalBeats: number;
		onBeatChange: (beat: number) => void;
	}

	let { currentBeat, totalBeats, onBeatChange }: Props = $props();

	function handleBeatChange(event: Event) {
		const newBeat = parseFloat((event.target as HTMLInputElement).value);
		onBeatChange(newBeat);
	}
</script>

<div class="control-group">
	<label for="beatSlider">Time:</label>
	<input
		type="range"
		id="beatSlider"
		min="0"
		max={totalBeats}
		step="0.01"
		value={currentBeat}
		class="slider"
		oninput={handleBeatChange}
	/>
	<span class="value-display">{currentBeat.toFixed(2)}</span>
	/ <span class="value-display">{totalBeats}</span>
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
