<!--
	Progress Tracker Component
	
	Displays quiz progress including question count, accuracy, and streaks.
	Adapts display based on quiz mode (fixed questions vs countdown).
-->

<script lang="ts">
	import type { LessonProgress, QuizMode } from '$lib/types/learn';
	import { QuizMode as QuizModeEnum } from '$lib/types/learn';

	// Props
	export let progress: LessonProgress;
	export let quizMode: QuizMode;
	export let showDetailed: boolean = true;
	export let compact: boolean = false;

	// Reactive statements
	$: accuracyPercentage =
		progress.questionsAnswered > 0
			? Math.round((progress.correctAnswers / progress.questionsAnswered) * 100)
			: 0;
	$: progressPercentage =
		quizMode === QuizModeEnum.FIXED_QUESTION && progress.totalQuestions > 0
			? Math.round((progress.questionsAnswered / progress.totalQuestions) * 100)
			: 0;
	$: formattedTime = formatTime(progress.timeElapsed);

	// Methods
	function formatTime(seconds: number): string {
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = seconds % 60;
		return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
	}

	function getAccuracyClass(percentage: number): string {
		if (percentage >= 80) return 'excellent';
		if (percentage >= 60) return 'good';
		if (percentage >= 40) return 'fair';
		return 'poor';
	}
</script>

<div class="progress-tracker" class:compact>
	{#if compact}
		<!-- Compact View -->
		<div class="compact-stats">
			{#if quizMode === QuizModeEnum.FIXED_QUESTION}
				<div class="stat-item">
					<span class="stat-value">{progress.currentQuestion}</span>
					<span class="stat-separator">/</span>
					<span class="stat-total">{progress.totalQuestions}</span>
				</div>
			{:else}
				<div class="stat-item">
					<span class="stat-value">{progress.questionsAnswered}</span>
					<span class="stat-label">answered</span>
				</div>
			{/if}

			<div class="stat-divider"></div>

			<div class="stat-item accuracy {getAccuracyClass(accuracyPercentage)}">
				<span class="stat-value">{accuracyPercentage}%</span>
				<span class="stat-label">accuracy</span>
			</div>
		</div>
	{:else}
		<!-- Detailed View -->
		<div class="detailed-stats">
			<!-- Progress Bar (for fixed question mode) -->
			{#if quizMode === QuizModeEnum.FIXED_QUESTION}
				<div class="progress-section">
					<div class="progress-header">
						<span class="progress-label">Question Progress</span>
						<span class="progress-count"
							>{progress.currentQuestion} / {progress.totalQuestions}</span
						>
					</div>
					<div class="progress-bar">
						<div class="progress-fill" style="width: {progressPercentage}%"></div>
					</div>
				</div>
			{/if}

			<!-- Stats Grid -->
			<div class="stats-grid">
				<div class="stat-card">
					<div class="stat-icon">📊</div>
					<div class="stat-content">
						<div class="stat-value">{progress.questionsAnswered}</div>
						<div class="stat-label">Questions Answered</div>
					</div>
				</div>

				<div class="stat-card accuracy-card {getAccuracyClass(accuracyPercentage)}">
					<div class="stat-icon">🎯</div>
					<div class="stat-content">
						<div class="stat-value">{accuracyPercentage}%</div>
						<div class="stat-label">Accuracy</div>
					</div>
				</div>

				<div class="stat-card">
					<div class="stat-icon">✅</div>
					<div class="stat-content">
						<div class="stat-value">{progress.correctAnswers}</div>
						<div class="stat-label">Correct</div>
					</div>
				</div>

				<div class="stat-card">
					<div class="stat-icon">❌</div>
					<div class="stat-content">
						<div class="stat-value">{progress.incorrectAnswers}</div>
						<div class="stat-label">Incorrect</div>
					</div>
				</div>

				{#if showDetailed}
					<div class="stat-card">
						<div class="stat-icon">⏱️</div>
						<div class="stat-content">
							<div class="stat-value">{formattedTime}</div>
							<div class="stat-label">Time Elapsed</div>
						</div>
					</div>

					<div class="stat-card">
						<div class="stat-icon">🔥</div>
						<div class="stat-content">
							<div class="stat-value">{progress.streakCurrent}</div>
							<div class="stat-label">Current Streak</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Streak Display -->
			{#if progress.streakLongest > 0}
				<div class="streak-section">
					<div class="streak-badge">
						<span class="streak-icon">🏆</span>
						<span class="streak-text">Best Streak: {progress.streakLongest}</span>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.progress-tracker {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		color: #ffffff;
	}

	/* Compact View */
	.compact {
		padding: 0.75rem 1rem;
	}

	.compact-stats {
		display: flex;
		align-items: center;
		gap: 1rem;
		font-size: 0.875rem;
	}

	.stat-item {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.stat-value {
		font-weight: bold;
		font-size: 1.125rem;
	}

	.stat-separator {
		color: #94a3b8;
		margin: 0 0.25rem;
	}

	.stat-total {
		color: #94a3b8;
		font-size: 1rem;
	}

	.stat-label {
		color: #94a3b8;
		font-size: 0.75rem;
	}

	.stat-divider {
		width: 1px;
		height: 20px;
		background: rgba(255, 255, 255, 0.2);
	}

	/* Detailed View */
	.detailed-stats {
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.progress-section {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.progress-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.875rem;
	}

	.progress-label {
		color: #ffffff;
		font-weight: 500;
	}

	.progress-count {
		color: #94a3b8;
		font-weight: 600;
	}

	.progress-bar {
		height: 8px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
		border-radius: 4px;
		transition: width 0.3s ease;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		gap: 1rem;
	}

	.stat-card {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		transition: all 0.2s ease;
	}

	.stat-card:hover {
		background: rgba(255, 255, 255, 0.1);
		transform: translateY(-2px);
	}

	.stat-icon {
		font-size: 1.5rem;
		opacity: 0.8;
	}

	.stat-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stat-card .stat-value {
		font-size: 1.25rem;
		font-weight: bold;
		color: #ffffff;
	}

	.stat-card .stat-label {
		font-size: 0.75rem;
		color: #94a3b8;
		font-weight: 500;
	}

	/* Accuracy Colors */
	.accuracy.excellent,
	.accuracy-card.excellent {
		color: #4ade80;
	}

	.accuracy.good,
	.accuracy-card.good {
		color: #22d3ee;
	}

	.accuracy.fair,
	.accuracy-card.fair {
		color: #f59e0b;
	}

	.accuracy.poor,
	.accuracy-card.poor {
		color: #f87171;
	}

	.accuracy-card.excellent {
		border-color: rgba(74, 222, 128, 0.3);
		background: rgba(74, 222, 128, 0.1);
	}

	.accuracy-card.good {
		border-color: rgba(34, 211, 238, 0.3);
		background: rgba(34, 211, 238, 0.1);
	}

	.accuracy-card.fair {
		border-color: rgba(245, 158, 11, 0.3);
		background: rgba(245, 158, 11, 0.1);
	}

	.accuracy-card.poor {
		border-color: rgba(248, 113, 113, 0.3);
		background: rgba(248, 113, 113, 0.1);
	}

	.streak-section {
		display: flex;
		justify-content: center;
	}

	.streak-badge {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
		color: #000000;
		border-radius: 20px;
		font-weight: 600;
		font-size: 0.875rem;
		box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
	}

	.streak-icon {
		font-size: 1rem;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.stats-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.detailed-stats {
			padding: 1rem;
			gap: 1rem;
		}

		.stat-card {
			padding: 0.75rem;
		}

		.stat-card .stat-value {
			font-size: 1.125rem;
		}
	}

	@media (max-width: 480px) {
		.stats-grid {
			grid-template-columns: 1fr;
		}

		.compact-stats {
			font-size: 0.75rem;
		}

		.compact .stat-value {
			font-size: 1rem;
		}
	}
</style>
