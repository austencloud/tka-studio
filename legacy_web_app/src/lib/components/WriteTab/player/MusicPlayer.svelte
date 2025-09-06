<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';

	// Player state
	const currentTime = writable(0);
	const duration = writable(0);
	const isPlaying = writable(false);
	const volume = writable(0.7);

	let audioElement: HTMLAudioElement;
	let progressInterval: ReturnType<typeof setInterval> | null = null;

	// Mock audio source - in a real implementation, this would be configurable
	let audioSrc = '';

	onMount(() => {
		// Create audio element
		audioElement = new Audio();

		// Set up event listeners
		audioElement.addEventListener('loadedmetadata', () => {
			duration.set(audioElement.duration);
		});

		audioElement.addEventListener('ended', () => {
			isPlaying.set(false);
			currentTime.set(0);
			if (progressInterval) {
				clearInterval(progressInterval);
				progressInterval = null;
			}
		});

		// Set initial volume
		audioElement.volume = $volume;
	});

	onDestroy(() => {
		// Clean up
		if (audioElement) {
			audioElement.pause();
			audioElement.src = '';
		}

		if (progressInterval) {
			clearInterval(progressInterval);
		}
	});

	// Play/pause toggle
	function togglePlay() {
		if (!audioElement) return;

		if ($isPlaying) {
			audioElement.pause();
			isPlaying.set(false);

			if (progressInterval) {
				clearInterval(progressInterval);
				progressInterval = null;
			}
		} else {
			// If no audio is loaded, show file picker
			if (!audioElement.src) {
				openFilePicker();
				return;
			}

			audioElement.play();
			isPlaying.set(true);

			// Update progress
			progressInterval = setInterval(() => {
				currentTime.set(audioElement.currentTime);
			}, 100);
		}
	}

	// Stop playback
	function stop() {
		if (!audioElement) return;

		audioElement.pause();
		audioElement.currentTime = 0;
		isPlaying.set(false);
		currentTime.set(0);

		if (progressInterval) {
			clearInterval(progressInterval);
			progressInterval = null;
		}
	}

	// Update current time when slider is moved
	function handleProgressChange(event: Event) {
		const target = event.target as HTMLInputElement;
		const newTime = parseFloat(target.value);

		if (audioElement) {
			audioElement.currentTime = newTime;
			currentTime.set(newTime);
		}
	}

	// Update volume when slider is moved
	function handleVolumeChange(event: Event) {
		const target = event.target as HTMLInputElement;
		const newVolume = parseFloat(target.value);

		volume.set(newVolume);

		if (audioElement) {
			audioElement.volume = newVolume;
		}
	}

	// Open file picker to select audio file
	function openFilePicker() {
		const input = document.createElement('input');
		input.type = 'file';
		input.accept = 'audio/*';

		input.onchange = (event) => {
			const target = event.target as HTMLInputElement;
			const file = target.files?.[0];

			if (file) {
				const url = URL.createObjectURL(file);
				loadAudio(url, file.name);
			}
		};

		input.click();
	}

	// Load audio from URL
	function loadAudio(url: string, name: string = 'Audio') {
		if (!audioElement) return;

		// Clean up previous audio
		if (audioElement.src) {
			audioElement.pause();
			URL.revokeObjectURL(audioElement.src);
		}

		audioElement.src = url;
		audioSrc = name;

		// Reset state
		currentTime.set(0);
		isPlaying.set(false);

		if (progressInterval) {
			clearInterval(progressInterval);
			progressInterval = null;
		}

		// Load metadata
		audioElement.load();
	}

	// Format time in MM:SS format
	function formatTime(seconds: number): string {
		const mins = Math.floor(seconds / 60);
		const secs = Math.floor(seconds % 60);
		return `${mins}:${secs.toString().padStart(2, '0')}`;
	}
</script>

<div class="music-player">
	<div class="player-controls">
		<button class="control-button" on:click={togglePlay} aria-label={$isPlaying ? 'Pause' : 'Play'}>
			{#if $isPlaying}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<rect x="6" y="4" width="4" height="16"></rect>
					<rect x="14" y="4" width="4" height="16"></rect>
				</svg>
			{:else}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<polygon points="5 3 19 12 5 21 5 3"></polygon>
				</svg>
			{/if}
		</button>

		<button class="control-button" on:click={stop} aria-label="Stop">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<rect x="6" y="6" width="12" height="12"></rect>
			</svg>
		</button>

		<div class="time-display">
			{formatTime($currentTime)} / {formatTime($duration)}
		</div>
	</div>

	<div class="progress-container">
		<input
			type="range"
			min="0"
			max={$duration || 100}
			value={$currentTime}
			on:input={handleProgressChange}
			class="progress-slider"
			aria-label="Playback progress"
		/>
	</div>

	<div class="audio-info">
		<button
			class="audio-name"
			on:click={openFilePicker}
			type="button"
			aria-label="Select audio file"
		>
			{audioSrc || 'Click to select audio file'}
		</button>

		<div class="volume-control">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="16"
				height="16"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
				<path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
				<path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
			</svg>

			<input
				type="range"
				min="0"
				max="1"
				step="0.01"
				value={$volume}
				on:input={handleVolumeChange}
				class="volume-slider"
				aria-label="Volume"
			/>
		</div>
	</div>
</div>

<style>
	.music-player {
		background-color: #252525;
		border-top: 1px solid #333;
		padding: 0.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.player-controls {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.control-button {
		background: none;
		border: none;
		color: #e0e0e0;
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 4px;
		transition: background-color 0.2s;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.control-button:hover {
		background-color: rgba(255, 255, 255, 0.1);
	}

	.time-display {
		margin-left: 0.5rem;
		font-family: monospace;
		font-size: 0.875rem;
		color: #999;
	}

	.progress-container {
		width: 100%;
	}

	.progress-slider {
		width: 100%;
		height: 4px;
		-webkit-appearance: none;
		appearance: none;
		background: #444;
		outline: none;
		border-radius: 2px;
		cursor: pointer;
	}

	.progress-slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 12px;
		height: 12px;
		background: #3498db;
		border-radius: 50%;
		cursor: pointer;
	}

	.progress-slider::-moz-range-thumb {
		width: 12px;
		height: 12px;
		background: #3498db;
		border-radius: 50%;
		cursor: pointer;
		border: none;
	}

	.audio-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.875rem;
	}

	.audio-name {
		color: #999;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition: background-color 0.2s;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		max-width: 60%;
		background: none;
		border: none;
		text-align: left;
		font-family: inherit;
		font-size: inherit;
	}

	.audio-name:hover {
		background-color: rgba(255, 255, 255, 0.1);
		color: #e0e0e0;
	}

	.volume-control {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: #999;
	}

	.volume-slider {
		width: 80px;
		height: 4px;
		-webkit-appearance: none;
		appearance: none;
		background: #444;
		outline: none;
		border-radius: 2px;
		cursor: pointer;
	}

	.volume-slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 10px;
		height: 10px;
		background: #3498db;
		border-radius: 50%;
		cursor: pointer;
	}

	.volume-slider::-moz-range-thumb {
		width: 10px;
		height: 10px;
		background: #3498db;
		border-radius: 50%;
		cursor: pointer;
		border: none;
	}

	/* Responsive adjustments */
	@media (max-width: 640px) {
		.time-display {
			display: none;
		}

		.audio-name {
			max-width: 50%;
		}
	}
</style>
