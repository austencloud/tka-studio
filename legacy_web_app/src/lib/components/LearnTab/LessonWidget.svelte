<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { fade, fly, scale } from 'svelte/transition';
	import { elasticOut, cubicOut } from 'svelte/easing';
	import {
		learnStore,
		currentQuestion,
		currentAnswers,
		quizProgress
	} from '$lib/state/stores/learn/learnStore';
	import QuestionDisplay from './QuestionDisplay.svelte';
	import AnswerOptions from './AnswerOptions.svelte';
	import ProgressIndicator from './ProgressIndicator.svelte';
	import FeedbackIndicator from './FeedbackIndicator.svelte';
	import BackButton from './shared/BackButton.svelte';
	import QuizTimer from './QuizTimer.svelte';

	// Handle feedback display timing
	let showFeedback = false;
	let feedbackTimeout: ReturnType<typeof setTimeout>;

	// Track animation states
	let questionAnimating = true;
	let answerAnimating = true;
	let isTransitioning = false;

	// Streak tracking
	let currentStreak = 0;
	let showStreakAnimation = false;
	let streakTimeout: ReturnType<typeof setTimeout>;

	// Function to handle answer selection
	async function handleAnswerSelect(answer: any) {
		if (isTransitioning) return;

		learnStore.submitAnswer(answer);
		showFeedback = true;

		// Update streak
		if ($learnStore.isAnswerCorrect) {
			currentStreak++;
			if (currentStreak >= 3) {
				showStreakAnimation = true;
				if (streakTimeout) clearTimeout(streakTimeout);
				streakTimeout = setTimeout(() => {
					showStreakAnimation = false;
				}, 2000);
			}
		} else {
			currentStreak = 0;
		}

		// Clear any existing timeout
		if (feedbackTimeout) {
			clearTimeout(feedbackTimeout);
		}

		// Shorter feedback time based on whether answer is correct or not
		const feedbackTime = $learnStore.isAnswerCorrect ? 700 : 1000;

		feedbackTimeout = setTimeout(async () => {
			if ($learnStore.isAnswerCorrect) {
				// Start transition animation
				isTransitioning = true;
				showFeedback = false;

				// Wait for feedback to fade out - reduced delay
				await tick();
				await new Promise((resolve) => setTimeout(resolve, 150));

				// Move to next question
				learnStore.nextQuestionOrEnd();

				// If we've moved to the next question, generate it
				if ($learnStore.currentView === 'lesson') {
					questionAnimating = true;
					answerAnimating = true;
					learnStore.generateNextQuestion();

					// Reset transition state after a shorter delay
					setTimeout(() => {
						isTransitioning = false;
					}, 300);
				}
			} else {
				showFeedback = false;
			}
		}, feedbackTime);
	}

	function handleBack() {
		if (isTransitioning) return;
		learnStore.goBackToSelector();
	}

	// Handle question animation complete
	function onQuestionAnimationEnd() {
		questionAnimating = false;
	}

	// Handle answer animation complete
	function onAnswerAnimationEnd() {
		answerAnimating = false;
	}

	// Clean up on unmount
	onMount(() => {
		return () => {
			if (feedbackTimeout) {
				clearTimeout(feedbackTimeout);
			}
			if (streakTimeout) {
				clearTimeout(streakTimeout);
			}
		};
	});
</script>

<div class="lesson-widget">
	<div class="lesson-background"></div>

	<header>
		<div class="header-left">
			<BackButton on:click={handleBack} />
		</div>

		<div class="header-center">
			<h1>{$learnStore.lessonConfig?.title || 'Lesson'}</h1>
			<div class="progress-container">
				<ProgressIndicator />

				{#if $learnStore.selectedMode === 'countdown'}
					<div class="timer-container">
						<QuizTimer seconds={$learnStore.remainingTime} />
					</div>
				{/if}
			</div>
		</div>

		<div class="header-right">
			{#if showStreakAnimation}
				<div class="streak-indicator" in:scale={{ duration: 400, easing: elasticOut }}>
					<span class="streak-count">{currentStreak}</span>
					<span class="streak-label">streak!</span>
					<div class="streak-fire">🔥</div>
				</div>
			{/if}
		</div>
	</header>

	<div class="content">
		<div class="question-section" class:animating={questionAnimating}>
			{#if $learnStore.lessonConfig}
				<div class="prompt" in:fly={{ y: -20, duration: 500, delay: 100, easing: cubicOut }}>
					{$learnStore.lessonConfig.prompt}
				</div>

				<div
					class="question-container"
					in:fly={{ y: 30, duration: 600, delay: 200, easing: cubicOut }}
					on:introend={onQuestionAnimationEnd}
				>
					<QuestionDisplay
						questionFormat={$learnStore.lessonConfig.questionFormat}
						questionData={$currentQuestion}
					/>
				</div>
			{/if}
		</div>

		<div class="answer-section" class:animating={answerAnimating}>
			{#if $learnStore.lessonConfig}
				<div
					class="answers-container"
					in:fly={{ y: 50, duration: 600, delay: 400, easing: cubicOut }}
					on:introend={onAnswerAnimationEnd}
				>
					<AnswerOptions
						answerFormat={$learnStore.lessonConfig.answerFormat}
						options={$currentAnswers}
						disabled={showFeedback || isTransitioning}
						on:select={(e) => handleAnswerSelect(e.detail)}
					/>
				</div>
			{/if}
		</div>
	</div>

	{#if showFeedback}
		<div transition:fade={{ duration: 300 }}>
			<FeedbackIndicator isCorrect={$learnStore.isAnswerCorrect} />
		</div>
	{/if}

	<div class="question-counter">
		<div class="counter-label">Question</div>
		<div class="counter-value">{$quizProgress.current}/{$quizProgress.total}</div>
	</div>
</div>

<style>
	.lesson-widget {
		display: flex;
		flex-direction: column;
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
		height: 100vh;
		position: relative;
		padding: 1.5rem;
	}

	.lesson-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image:
			radial-gradient(circle at 10% 20%, rgba(58, 123, 213, 0.03) 0%, transparent 50%),
			radial-gradient(circle at 90% 80%, rgba(58, 123, 213, 0.03) 0%, transparent 50%);
		z-index: -1;
		pointer-events: none;
	}

	header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
		position: relative;
		z-index: 2;
	}

	.header-center {
		text-align: center;
		flex: 1;
	}

	h1 {
		font-size: 1.75rem;
		margin-bottom: 0.75rem;
		font-weight: 700;
		background: linear-gradient(135deg, #fff, #a0a0a0);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
		text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}

	.progress-container {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 1rem;
	}

	.timer-container {
		margin-left: 1rem;
	}

	.header-left,
	.header-right {
		min-width: 100px;
		display: flex;
		align-items: center;
	}

	.header-right {
		justify-content: flex-end;
	}

	.content {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 2rem;
		position: relative;
		z-index: 1;
		min-height: 0; /* Important for flex container to properly size */
	}

	.question-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		position: relative;
		flex: 1;
		padding-top: 2rem;
	}

	.question-section.animating::after {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		width: 120%;
		height: 120%;
		transform: translate(-50%, -50%);
		background: radial-gradient(circle, rgba(58, 123, 213, 0.05) 0%, transparent 70%);
		z-index: -1;
		opacity: 0;
		animation: pulse 2s ease-out forwards;
	}

	@keyframes pulse {
		0% {
			opacity: 0;
			transform: translate(-50%, -50%) scale(0.8);
		}
		50% {
			opacity: 1;
			transform: translate(-50%, -50%) scale(1);
		}
		100% {
			opacity: 0;
			transform: translate(-50%, -50%) scale(1.2);
		}
	}

	.prompt {
		font-size: 1.3rem;
		color: var(--color-text-primary, white);
		margin-bottom: 0.5rem;
		font-weight: 500;
		text-align: center;
	}

	.question-container {
		background: rgba(30, 40, 60, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 16px;
		padding: 2rem;
		box-shadow:
			0 8px 32px rgba(0, 0, 0, 0.1),
			0 0 0 1px rgba(255, 255, 255, 0.05);
		width: 100%;
		max-width: 600px;
		display: flex;
		justify-content: center;
		align-items: center;
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease;
	}

	.question-container:hover {
		transform: translateY(-5px);
		box-shadow:
			0 12px 48px rgba(0, 0, 0, 0.15),
			0 0 0 1px rgba(255, 255, 255, 0.1);
	}

	.answer-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		position: relative;
		flex: 2;
		width: 100%;
	}

	.answers-container {
		width: 100%;
		max-width: 950px;
		margin: 0 auto;
	}

	.streak-indicator {
		background: linear-gradient(135deg, #ff9500, #ff5252);
		border-radius: 999px;
		padding: 0.5rem 1rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		box-shadow: 0 4px 12px rgba(255, 82, 82, 0.3);
		position: relative;
	}

	.streak-count {
		font-size: 1.25rem;
		font-weight: 700;
		color: white;
	}

	.streak-label {
		font-size: 0.9rem;
		color: rgba(255, 255, 255, 0.9);
	}

	.streak-fire {
		font-size: 1.25rem;
		animation: bounce 0.5s infinite alternate;
	}

	@keyframes bounce {
		from {
			transform: translateY(0);
		}
		to {
			transform: translateY(-3px);
		}
	}

	.question-counter {
		position: absolute;
		bottom: 1.5rem;
		right: 1.5rem;
		background: rgba(0, 0, 0, 0.2);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 999px;
		padding: 0.5rem 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.counter-label {
		font-size: 0.7rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.counter-value {
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text-primary, white);
	}

	@media (max-width: 768px) {
		.lesson-widget {
			padding: 1rem;
			height: calc(100vh - 2rem);
		}

		.content {
			gap: 1.5rem;
		}

		.prompt {
			font-size: 1.1rem;
		}

		.question-container {
			padding: 1.5rem;
		}

		.header-left,
		.header-right {
			min-width: 80px;
		}

		h1 {
			font-size: 1.5rem;
		}

		.question-counter {
			bottom: 1rem;
			right: 1rem;
		}
	}
</style>
