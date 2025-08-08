<script lang="ts">
	import { InputValidator } from '../../utils/validation/input-validator.js';

	// Props
	let {
		isPlaying = false,
		speed = 1.0,
		currentBeat = 0,
		totalBeats = 0,
		onPlayPause,
		onReset,
		onSpeedChange
	}: {
		isPlaying?: boolean;
		speed?: number;
		currentBeat?: number;
		totalBeats?: number;
		onPlayPause?: () => void;
		onReset?: () => void;
		onSpeedChange?: (_value: number) => void;
	} = $props();

	// Handle speed change
	function handleSpeedChange(event: Event): void {
		const value = parseFloat((event.target as HTMLInputElement).value);
		const validation = InputValidator.validateSpeed(value);

		if (validation.isValid) {
			onSpeedChange?.(value);
		} else {
			console.warn('Invalid speed:', validation.errors.join(', '));
		}

		// Log warnings if any
		if (validation.warnings.length > 0) {
			console.info('Speed warnings:', validation.warnings.join(', '));
		}
	}

	// Computed values
	// Progress bar should only show progress during actual animation (beat 1+)
	// Beat 0 (start position) should show 0% progress
	const progressPercent = $derived(
		totalBeats <= 0 || currentBeat <= 0
			? 0
			: (() => {
					// Progress from beat 1 to totalBeats (animation steps only)
					const animationProgress = Math.max(0, currentBeat - 1);
					const maxAnimationProgress = totalBeats - 1;
					return maxAnimationProgress > 0
						? Math.round((animationProgress / maxAnimationProgress) * 100)
						: 0;
				})()
	);

	// Step calculation aligned with new timing system:
	// Beat 0 = "Start", Beat 1-N = "Step 1" to "Step N"
	const currentStep = $derived(
		currentBeat === 0
			? 'Start'
			: currentBeat >= totalBeats
				? `Step ${totalBeats}`
				: `Step ${Math.floor(currentBeat)}`
	);

	const totalSteps = $derived(Math.floor(totalBeats));

	const elapsedSeconds = $derived(currentBeat / speed);
	const elapsedMinutes = $derived(Math.floor(elapsedSeconds / 60));
	const elapsedRemainingSeconds = $derived(Math.floor(elapsedSeconds % 60));
	const elapsedTimeFormatted = $derived(
		`${elapsedMinutes}:${elapsedRemainingSeconds.toString().padStart(2, '0')}`
	);
</script>

<div class="sequence-control-panel">
	<!-- Primary Controls Row -->
	<div class="primary-controls">
		<!-- Play Controls -->
		<div class="play-controls">
			<button type="button" class="btn-reset" onclick={onReset} title="Reset animation">
				<span class="icon">⏮</span>
			</button>
			<button
				type="button"
				class="btn-play"
				onclick={onPlayPause}
				title={isPlaying ? 'Pause animation' : 'Play animation'}
			>
				<span class="icon">{isPlaying ? '⏸' : '▶'}</span>
			</button>
		</div>

		<!-- Progress Info -->
		<div class="progress-info">
			<div class="progress-header">
				<span class="progress-label">Progress</span>
				<span class="progress-value">{progressPercent}%</span>
			</div>
			<div class="progress-details">
				<span>{currentStep} of {totalSteps} steps</span>
				<span>{elapsedTimeFormatted}</span>
			</div>
		</div>

		<!-- Speed Control -->
		<div class="speed-control">
			<div class="speed-header">
				<span class="speed-label">Speed</span>
				<span class="speed-value">{speed.toFixed(1)}×</span>
			</div>
			<input
				type="range"
				class="speed-slider"
				min="0.1"
				max="3.0"
				step="0.1"
				value={speed}
				oninput={handleSpeedChange}
				title="Adjust playback speed"
			/>
		</div>
	</div>

	<!-- Progress Bar (Full Width) -->
	<div class="progress-bar-container">
		<div class="progress-bar">
			<div class="progress-fill" style:width="{progressPercent}%"></div>
		</div>
	</div>
</div>

<style>
	.sequence-control-panel {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 1.25rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		transition: all 0.3s ease;
		max-width: 800px; /* Prevent excessive width on desktop */
		margin: 0 auto; /* Center on desktop */
	}

	/* Primary Controls Row - Desktop: Horizontal, Mobile: Vertical */
	.primary-controls {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 1.5rem;
		align-items: center;
	}

	/* Play Controls */
	.play-controls {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.play-controls button {
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 50%;
		width: 44px;
		height: 44px;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.play-controls button:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
		filter: brightness(1.1);
	}

	.btn-reset {
		background: var(--color-text-secondary) !important;
		color: var(--color-background) !important;
	}

	.btn-reset:hover {
		filter: brightness(0.9) !important;
	}

	.icon {
		font-size: 1.25rem;
		color: inherit;
	}

	/* Progress Info */
	.progress-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		text-align: center;
		min-width: 0; /* Allow shrinking */
	}

	.progress-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
	}

	.progress-label {
		font-weight: 600;
		color: var(--color-text-primary);
		font-size: 0.9rem;
	}

	.progress-value {
		font-weight: 700;
		color: var(--color-primary);
		font-size: 1.1rem;
	}

	.progress-details {
		display: flex;
		justify-content: space-between;
		font-size: 0.8rem;
		color: var(--color-text-secondary);
		font-weight: 500;
		gap: 1rem;
	}

	/* Speed Control */
	.speed-control {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		min-width: 120px;
	}

	.speed-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.speed-label {
		font-weight: 600;
		color: var(--color-text-primary);
		font-size: 0.9rem;
	}

	.speed-value {
		font-weight: 700;
		color: var(--color-primary);
		font-size: 1rem;
	}

	.speed-slider {
		width: 100%;
		cursor: pointer;
		accent-color: var(--color-primary);
		height: 6px;
		border-radius: 3px;
		background: var(--color-border);
		outline: none;
		transition: all 0.2s ease;
	}

	.speed-slider:hover {
		background: var(--color-text-secondary);
	}

	.speed-slider::-webkit-slider-thumb {
		appearance: none;
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: var(--color-primary);
		cursor: pointer;
		border: 2px solid var(--color-background);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: all 0.2s ease;
	}

	.speed-slider::-webkit-slider-thumb:hover {
		transform: scale(1.1);
		box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
	}

	.speed-slider::-moz-range-thumb {
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: var(--color-primary);
		cursor: pointer;
		border: 2px solid var(--color-background);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: all 0.2s ease;
	}

	/* Progress Bar Container */
	.progress-bar-container {
		width: 100%;
	}

	.progress-bar {
		height: 8px;
		background: var(--color-border);
		border-radius: 4px;
		overflow: hidden;
		position: relative;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, var(--color-primary), var(--color-success));
		border-radius: 4px;
		transition: width 0.3s ease;
		position: relative;
	}

	.progress-fill::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
		animation: shimmer 2s infinite;
	}

	@keyframes shimmer {
		0% {
			transform: translateX(-100%);
		}
		100% {
			transform: translateX(100%);
		}
	}

	/* Tablet Layout */
	@media (max-width: 1024px) {
		.sequence-control-panel {
			max-width: none;
			margin: 0;
		}
	}

	/* Mobile Layout */
	@media (max-width: 768px) {
		.sequence-control-panel {
			padding: 1rem;
			gap: 1rem;
		}

		.primary-controls {
			grid-template-columns: 1fr;
			grid-template-rows: auto auto auto;
			gap: 1rem;
			text-align: center;
		}

		.play-controls {
			justify-content: center;
		}

		.play-controls button {
			width: 48px;
			height: 48px;
		}

		.progress-info {
			text-align: center;
		}

		.speed-control {
			min-width: unset;
		}

		.speed-slider::-webkit-slider-thumb {
			width: 20px;
			height: 20px;
		}

		.speed-slider::-moz-range-thumb {
			width: 20px;
			height: 20px;
		}
	}

	/* Small Mobile Layout */
	@media (max-width: 480px) {
		.sequence-control-panel {
			padding: 0.75rem;
			gap: 0.75rem;
		}

		.primary-controls {
			gap: 0.75rem;
		}

		.play-controls button {
			width: 52px;
			height: 52px;
		}

		.icon {
			font-size: 1.4rem;
		}

		.speed-slider::-webkit-slider-thumb {
			width: 22px;
			height: 22px;
		}

		.speed-slider::-moz-range-thumb {
			width: 22px;
			height: 22px;
		}
	}
</style>
