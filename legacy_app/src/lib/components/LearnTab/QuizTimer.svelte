<script lang="ts">
	export let seconds: number = 60;

	// Format time as MM:SS
	$: formattedTime = formatTime(seconds);

	function formatTime(totalSeconds: number): string {
		const minutes = Math.floor(totalSeconds / 60);
		const seconds = totalSeconds % 60;
		return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
	}
</script>

<div class="quiz-timer" class:warning={seconds <= 10}>
	<div class="timer-icon">
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
			<circle cx="12" cy="12" r="10"></circle>
			<polyline points="12 6 12 12 16 14"></polyline>
		</svg>
	</div>
	<div class="timer-display">{formattedTime}</div>
</div>

<style>
	.quiz-timer {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.25rem 0.75rem;
		background-color: var(--color-surface-800, #1d1d1d);
		border-radius: 999px;
		transition: background-color 0.3s;
	}

	.quiz-timer.warning {
		background-color: var(--color-danger, #e53935);
		animation: pulse 1s infinite;
	}

	.timer-icon {
		display: flex;
		align-items: center;
	}

	.timer-display {
		font-family: monospace;
		font-size: 1.1rem;
		font-weight: 500;
	}

	@keyframes pulse {
		0% {
			opacity: 1;
		}
		50% {
			opacity: 0.7;
		}
		100% {
			opacity: 1;
		}
	}
</style>
