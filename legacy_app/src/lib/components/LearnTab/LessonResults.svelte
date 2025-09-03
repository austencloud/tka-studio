<script lang="ts">
	import { onMount } from 'svelte';
	import { fly, draw } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { learnStore, quizResults } from '$lib/state/stores/learn/learnStore';
	import BackButton from './shared/BackButton.svelte';
	import StartOverButton from './shared/StartOverButton.svelte';
	import { tweened } from 'svelte/motion';

	// Calculate percentage score
	$: percentage = Math.round(($quizResults.score / $quizResults.total) * 100);
	$: isPassing = percentage >= 70;

	type AchievementLevel = 'excellent' | 'great' | 'good' | 'fair' | 'needs-practice';

	// Determine achievement level
	$: achievementLevel = (
		percentage >= 90
			? 'excellent'
			: percentage >= 80
				? 'great'
				: percentage >= 70
					? 'good'
					: percentage >= 60
						? 'fair'
						: 'needs-practice'
	) as AchievementLevel;

	// Achievement messages
	const achievementMessages = {
		excellent: {
			title: 'Excellent!',
			message: "You've mastered this lesson with an outstanding score!",
			emoji: '🏆'
		},
		great: {
			title: 'Great Job!',
			message: "You've shown strong understanding of the material.",
			emoji: '🌟'
		},
		good: {
			title: 'Good Work!',
			message: "You've demonstrated solid knowledge of the concepts.",
			emoji: '👍'
		},
		fair: {
			title: 'Nice Try!',
			message: "You're making progress, but could use more practice.",
			emoji: '🔄'
		},
		'needs-practice': {
			title: 'Keep Practicing!',
			message: "Don't worry, learning takes time. Try again to improve.",
			emoji: '📚'
		}
	};

	// Animated percentage counter
	const animatedPercentage = tweened(0, {
		duration: 2000,
		easing: cubicOut
	});

	// Animated stats
	const animatedCorrect = tweened(0, {
		duration: 1500,
		easing: cubicOut
	});

	const animatedIncorrect = tweened(0, {
		duration: 1500,
		easing: cubicOut
	});

	// Start animations when component mounts
	onMount(() => {
		setTimeout(() => {
			animatedPercentage.set(percentage);
			animatedCorrect.set($quizResults.score);
			animatedIncorrect.set($quizResults.total - $quizResults.score);
		}, 300);
	});

	// Calculate circle progress
	$: circleRadius = 70;
	$: circleCircumference = 2 * Math.PI * circleRadius;
	$: strokeDashoffset = circleCircumference - ($animatedPercentage / 100) * circleCircumference;

	// Get color based on score
	$: scoreColor =
		percentage >= 90
			? '#4CAF50'
			: percentage >= 70
				? '#2196F3'
				: percentage >= 60
					? '#FF9800'
					: '#F44336';
</script>

<div class="lesson-results">
	<div class="results-container">
		<div class="results-header" in:fly={{ y: -20, duration: 600, easing: cubicOut }}>
			<h1>Quiz Results</h1>
			<p class="subtitle">
				{achievementMessages[achievementLevel].title}
				{achievementMessages[achievementLevel].emoji}
			</p>
		</div>

		<div class="score-display" in:fly={{ y: 30, duration: 800, delay: 200, easing: cubicOut }}>
			<div class="circle-progress">
				<svg width="180" height="180" viewBox="0 0 180 180">
					<!-- Background circle -->
					<circle
						cx="90"
						cy="90"
						r={circleRadius}
						fill="none"
						stroke="rgba(255, 255, 255, 0.1)"
						stroke-width="10"
					/>

					<!-- Progress circle -->
					<circle
						cx="90"
						cy="90"
						r={circleRadius}
						fill="none"
						stroke={scoreColor}
						stroke-width="10"
						stroke-linecap="round"
						stroke-dasharray={circleCircumference}
						stroke-dashoffset={strokeDashoffset}
						transform="rotate(-90 90 90)"
						in:draw={{ duration: 2000, easing: cubicOut }}
					/>

					<!-- Percentage text -->
					<text
						x="90"
						y="90"
						text-anchor="middle"
						dominant-baseline="middle"
						font-size="36"
						font-weight="bold"
						fill="white"
					>
						{Math.round($animatedPercentage)}%
					</text>

					<!-- Fraction text -->
					<text
						x="90"
						y="115"
						text-anchor="middle"
						dominant-baseline="middle"
						font-size="16"
						fill="rgba(255, 255, 255, 0.8)"
					>
						{$quizResults.score}/{$quizResults.total}
					</text>
				</svg>
			</div>
		</div>

		<div class="feedback-message" in:fly={{ y: 20, duration: 600, delay: 400, easing: cubicOut }}>
			<p>{achievementMessages[achievementLevel].message}</p>
		</div>

		<div class="stats-container" in:fly={{ y: 20, duration: 600, delay: 600, easing: cubicOut }}>
			<div class="stat-card">
				<div class="stat-icon correct">✓</div>
				<div class="stat-value">{Math.round($animatedCorrect)}</div>
				<div class="stat-label">Correct</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon incorrect">✗</div>
				<div class="stat-value">{Math.round($animatedIncorrect)}</div>
				<div class="stat-label">Incorrect</div>
			</div>
		</div>

		<div class="next-steps" in:fly={{ y: 20, duration: 600, delay: 800, easing: cubicOut }}>
			<h2>Next Steps</h2>
			<div class="recommendation">
				{#if isPassing}
					<p>
						Ready to continue your learning journey? Try another lesson or challenge yourself again!
					</p>
				{:else}
					<p>Practice makes perfect! Review the material and try again to improve your score.</p>
				{/if}
			</div>
		</div>

		<div class="actions" in:fly={{ y: 20, duration: 600, delay: 1000, easing: cubicOut }}>
			<BackButton on:click={() => learnStore.goBackToSelector()}>Back to Lessons</BackButton>
			<StartOverButton on:click={() => learnStore.startOver()}>Try Again</StartOverButton>
		</div>
	</div>

	<div class="confetti-container">
		{#if isPassing}
			{#each Array(20) as _}
				<div
					class="confetti"
					style="
						--delay: {Math.random() * 5}s;
						--left: {Math.random() * 100}%;
						--color: hsl({Math.random() * 360}, 80%, 60%);
						--size: {Math.random() * 0.7 + 0.3}rem;
						--rotation: {Math.random() * 360}deg;
						--speed: {Math.random() * 3 + 2}s;
					"
				></div>
			{/each}
		{/if}
	</div>
</div>

<style>
	.lesson-results {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 2rem 1rem;
		min-height: 100%;
		position: relative;
		overflow: hidden;
	}

	.results-container {
		background-color: rgba(30, 40, 60, 0.5);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 16px;
		padding: 2.5rem;
		width: 100%;
		max-width: 600px;
		box-shadow:
			0 8px 32px rgba(0, 0, 0, 0.2),
			0 0 0 1px rgba(255, 255, 255, 0.05);
		text-align: center;
		position: relative;
		z-index: 2;
	}

	.results-header {
		margin-bottom: 2rem;
	}

	h1 {
		margin-bottom: 0.5rem;
		font-size: 2rem;
		font-weight: 700;
		background: linear-gradient(135deg, #fff, #a0a0a0);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
		text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}

	.subtitle {
		font-size: 1.25rem;
		color: var(--color-text-primary, white);
		margin-bottom: 0.5rem;
	}

	.score-display {
		margin: 1rem 0 2rem;
		display: flex;
		justify-content: center;
	}

	.circle-progress {
		position: relative;
	}

	.feedback-message {
		margin-bottom: 2rem;
		font-size: 1.1rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.8));
		line-height: 1.5;
	}

	.stats-container {
		display: flex;
		justify-content: center;
		gap: 2rem;
		margin: 2rem 0;
	}

	.stat-card {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		padding: 1.5rem;
		min-width: 120px;
		display: flex;
		flex-direction: column;
		align-items: center;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		transition: transform 0.3s ease;
	}

	.stat-card:hover {
		transform: translateY(-5px);
	}

	.stat-icon {
		font-size: 1.5rem;
		font-weight: bold;
		width: 2.5rem;
		height: 2.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		margin-bottom: 0.75rem;
	}

	.stat-icon.correct {
		background-color: rgba(76, 175, 80, 0.2);
		color: #4caf50;
	}

	.stat-icon.incorrect {
		background-color: rgba(244, 67, 54, 0.2);
		color: #f44336;
	}

	.stat-value {
		font-size: 2rem;
		font-weight: 700;
		line-height: 1;
		margin-bottom: 0.5rem;
	}

	.stat-label {
		font-size: 0.9rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.next-steps {
		background: rgba(255, 255, 255, 0.03);
		border-radius: 12px;
		padding: 1.5rem;
		margin-bottom: 2rem;
	}

	.next-steps h2 {
		font-size: 1.25rem;
		margin-bottom: 1rem;
		color: var(--color-text-primary, white);
	}

	.recommendation {
		font-size: 1rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.8));
		line-height: 1.5;
	}

	.actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		margin-top: 1.5rem;
	}

	.confetti-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 1;
	}

	.confetti {
		position: absolute;
		top: -10%;
		left: var(--left);
		width: var(--size);
		height: var(--size);
		background-color: var(--color);
		transform: rotate(var(--rotation));
		opacity: 0.8;
		animation: fall var(--speed) var(--delay) linear infinite;
	}

	@keyframes fall {
		0% {
			top: -10%;
			transform: rotate(var(--rotation));
			opacity: 1;
		}
		75% {
			opacity: 0.7;
		}
		100% {
			top: 110%;
			transform: rotate(calc(var(--rotation) + 360deg));
			opacity: 0;
		}
	}

	@media (max-width: 600px) {
		.results-container {
			padding: 1.5rem;
		}

		h1 {
			font-size: 1.75rem;
		}

		.subtitle {
			font-size: 1.1rem;
		}

		.stats-container {
			flex-direction: column;
			gap: 1rem;
			align-items: center;
		}

		.stat-card {
			width: 100%;
			max-width: 200px;
		}
	}
</style>
