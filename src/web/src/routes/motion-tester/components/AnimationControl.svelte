<script lang="ts">
	interface Props {
		progress: number;
		isPlaying: boolean;
		onProgressChange: (progress: number) => void;
		onPlayPause: () => void;
		onReset: () => void;
	}

	let { 
		progress, 
		isPlaying, 
		onProgressChange, 
		onPlayPause, 
		onReset 
	}: Props = $props();

	let progressPercentage = $derived(Math.round(progress * 100));
</script>

<div class="animation-control">
	<div class="control-row">
		<div class="progress-control">
			<label for="progress-slider">Progress:</label>
			<div class="slider-container">
				<input 
					id="progress-slider"
					type="range" 
					min="0" 
					max="1" 
					step="0.01" 
					value={progress}
					oninput={(e) => onProgressChange(parseFloat(e.currentTarget.value))}
				>
				<span class="progress-value">{progressPercentage}%</span>
			</div>
		</div>
	</div>
</div>

<style>
	.animation-control {
		width: 100%;
	}

	.control-row {
		display: flex;
		align-items: center;
		gap: 15px;
		flex-wrap: wrap;
	}




	.progress-control {
		display: flex;
		align-items: center;
		gap: 10px;
		flex: 1;
		min-width: 200px;
	}

	.progress-control label {
		color: #c7d2fe;
		font-size: 0.8rem;
		min-width: 60px;
	}

	.slider-container {
		display: flex;
		align-items: center;
		gap: 10px;
		flex: 1;
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
		width: 16px;
		height: 16px;
		background: #6366f1;
		border-radius: 50%;
		cursor: pointer;
	}

	.slider-container input[type="range"]::-moz-range-thumb {
		width: 16px;
		height: 16px;
		background: #6366f1;
		border-radius: 50%;
		cursor: pointer;
		border: none;
	}

	.progress-value {
		color: #fbbf24;
		font-size: 0.8rem;
		font-weight: 600;
		min-width: 40px;
		text-align: right;
	}
</style>
