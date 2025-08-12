<!-- LessonModeToggle.svelte - Quiz mode selection toggle -->
<script lang="ts">
	import { QuizMode } from '$lib/types/learn';

	// Props
	interface Props {
		selectedMode?: QuizMode;
		disabled?: boolean;
		onModeChanged?: (mode: QuizMode) => void;
	}

	let {
		selectedMode = $bindable(QuizMode.FIXED_QUESTION),
		disabled = false,
		onModeChanged,
	}: Props = $props();

	// Handle mode selection
	function selectMode(mode: QuizMode) {
		if (disabled) return;
		selectedMode = mode;
		onModeChanged?.(mode);
	}
</script>

<div class="mode-toggle-container">
	<div class="toggle-group">
		<button
			class="toggle-button"
			class:active={selectedMode === QuizMode.FIXED_QUESTION}
			class:disabled
			onclick={() => selectMode(QuizMode.FIXED_QUESTION)}
			{disabled}
		>
			Fixed Questions
		</button>
		<button
			class="toggle-button"
			class:active={selectedMode === QuizMode.COUNTDOWN}
			class:disabled
			onclick={() => selectMode(QuizMode.COUNTDOWN)}
			{disabled}
		>
			Countdown
		</button>
	</div>
</div>

<style>
	.mode-toggle-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin: var(--spacing-lg) 0;
	}

	.toggle-group {
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 6px;
		padding: 4px;
		display: flex;
		gap: 0;
		backdrop-filter: var(--glass-backdrop);
	}

	.toggle-button {
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.8);
		font-family: Georgia, serif;
		font-size: 12px;
		font-weight: 500;
		padding: 8px 16px;
		border-radius: 4px;
		cursor: pointer;
		transition: all var(--transition-normal);
		white-space: nowrap;
		min-width: 120px;
		text-align: center;
	}

	.toggle-button:hover:not(.disabled) {
		background: rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
	}

	.toggle-button.active {
		background: rgba(62, 99, 221, 0.8);
		color: white;
		font-weight: bold;
	}

	.toggle-button.active:hover:not(.disabled) {
		background: rgba(62, 99, 221, 0.9);
	}

	.toggle-button:active:not(.disabled) {
		transform: scale(0.98);
	}

	.toggle-button.disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.toggle-button {
			font-size: 11px;
			padding: 6px 12px;
			min-width: 100px;
		}
	}

	@media (max-width: 480px) {
		.toggle-button {
			font-size: 10px;
			padding: 5px 10px;
			min-width: 80px;
		}
	}
</style>
