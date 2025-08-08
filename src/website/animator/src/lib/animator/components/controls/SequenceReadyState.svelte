<script lang="ts">
	// Props
	let {
		sequenceWord = '',
		sequenceAuthor = '',
		totalSteps = 0,
		onPlay
	}: {
		sequenceWord?: string;
		sequenceAuthor?: string;
		totalSteps?: number;
		onPlay?: () => void;
	} = $props();
</script>

<div class="sequence-ready-state">
	<div class="sequence-info">
		<h2 class="sequence-title">{sequenceWord}</h2>
		{#if sequenceAuthor}
			<p class="sequence-author">by {sequenceAuthor}</p>
		{/if}
		<p class="sequence-details">{totalSteps} steps ready to animate</p>
	</div>

	<button type="button" class="play-button" onclick={onPlay} title="Start animation">
		<div class="play-icon">
			<svg viewBox="0 0 24 24" fill="currentColor">
				<path d="M8 5v14l11-7z" />
			</svg>
		</div>
		<span class="play-text">Play Animation</span>
	</button>

	<div class="ready-indicator">
		<div class="pulse-ring"></div>
		<div class="ready-dot"></div>
	</div>
</div>

<style>
	.sequence-ready-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2rem;
		padding: 2rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 16px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		max-width: 400px;
		margin: 0 auto;
		text-align: center;
		position: relative;
		overflow: hidden;
	}

	.sequence-ready-state::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, var(--color-primary), var(--color-success));
		border-radius: 16px 16px 0 0;
	}

	.sequence-info {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.sequence-title {
		font-size: 1.75rem;
		font-weight: 700;
		color: var(--color-text-primary);
		margin: 0;
		letter-spacing: 0.5px;
	}

	.sequence-author {
		font-size: 1rem;
		color: var(--color-text-secondary);
		margin: 0;
		font-style: italic;
	}

	.sequence-details {
		font-size: 0.9rem;
		color: var(--color-text-secondary);
		margin: 0;
		font-weight: 500;
	}

	.play-button {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem 2rem;
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 50px;
		font-size: 1.1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s ease;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		position: relative;
		overflow: hidden;
	}

	.play-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
		filter: brightness(1.1);
	}

	.play-button:active {
		transform: translateY(0);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.play-button::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
		transition: left 0.5s ease;
	}

	.play-button:hover::before {
		left: 100%;
	}

	.play-icon {
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.play-icon svg {
		width: 100%;
		height: 100%;
		filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
	}

	.play-text {
		position: relative;
		z-index: 1;
	}

	.ready-indicator {
		position: relative;
		width: 20px;
		height: 20px;
	}

	.ready-dot {
		width: 12px;
		height: 12px;
		background: var(--color-success);
		border-radius: 50%;
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.pulse-ring {
		width: 20px;
		height: 20px;
		border: 2px solid var(--color-success);
		border-radius: 50%;
		position: absolute;
		top: 0;
		left: 0;
		opacity: 0.6;
		animation: pulse 2s infinite ease-out;
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
			opacity: 0.6;
		}
		100% {
			transform: scale(1.8);
			opacity: 0;
		}
	}

	/* Mobile responsive */
	@media (max-width: 768px) {
		.sequence-ready-state {
			padding: 1.5rem;
			gap: 1.5rem;
			margin: 0 1rem;
		}

		.sequence-title {
			font-size: 1.5rem;
		}

		.play-button {
			padding: 0.875rem 1.75rem;
			font-size: 1rem;
		}
	}

	@media (max-width: 480px) {
		.sequence-ready-state {
			padding: 1.25rem;
			gap: 1.25rem;
		}

		.sequence-title {
			font-size: 1.25rem;
		}

		.play-button {
			padding: 0.75rem 1.5rem;
			font-size: 0.95rem;
			gap: 0.75rem;
		}

		.play-icon {
			width: 20px;
			height: 20px;
		}
	}
</style>
