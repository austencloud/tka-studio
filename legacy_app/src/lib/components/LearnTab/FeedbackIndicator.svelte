<script lang="ts">
	export let isCorrect: boolean | null = null;
</script>

<div
	class="feedback-indicator {isCorrect ? 'correct' : 'incorrect'}"
	role="alert"
	aria-live="assertive"
>
	<div class="feedback-content">
		{#if isCorrect}
			<div class="icon">✓</div>
			<div class="message">Correct!</div>
		{:else}
			<div class="icon">✗</div>
			<div class="message">Incorrect. Try Again!</div>
		{/if}
	</div>
</div>

<style>
	.feedback-indicator {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 2rem;
		display: flex;
		justify-content: center;
		pointer-events: none;
		z-index: 100;
	}

	.feedback-content {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		color: white;
		font-weight: 600;
		font-size: 1.2rem;
		box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
		animation: fadeInUp 0.3s ease-out;
	}

	.correct .feedback-content {
		background-color: var(--color-success, #43a047);
	}

	.incorrect .feedback-content {
		background-color: var(--color-danger, #e53935);
	}

	.icon {
		font-size: 1.25rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
