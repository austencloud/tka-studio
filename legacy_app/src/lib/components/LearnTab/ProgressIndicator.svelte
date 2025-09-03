<script lang="ts">
	import { learnStore, quizProgress } from '$lib/state/stores/learn/learnStore';
	import QuizTimer from './QuizTimer.svelte';
</script>

<div class="progress-indicator">
	{#if $learnStore.selectedMode === 'fixed_question'}
		<div class="question-progress">
			Question {$quizProgress.current} of {$quizProgress.total}
		</div>
	{:else if $learnStore.selectedMode === 'countdown'}
		<div class="timer-progress">
			<QuizTimer seconds={$quizProgress.remainingTime} />
		</div>
	{/if}
</div>

<style>
	.progress-indicator {
		font-size: 1rem;
		color: var(--color-text-muted, #aaa);
	}

	.question-progress {
		padding: 0.25rem 0.75rem;
		background-color: var(--color-surface-800, #1d1d1d);
		border-radius: 999px;
	}

	.timer-progress {
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
