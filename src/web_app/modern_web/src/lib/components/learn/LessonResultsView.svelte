<!-- LessonResultsView.svelte - Lesson results placeholder -->
<script lang="ts">
	import type { LessonResults } from '$lib/types/learn';

	// Props
	interface Props {
		results?: LessonResults | null;
		onBackToSelector?: () => void;
		onRetryLesson?: () => void;
	}

	let { results = null, onBackToSelector, onRetryLesson }: Props = $props();

	// Handle navigation
	function handleBackClick() {
		onBackToSelector?.();
	}

	function handleRetryClick() {
		onRetryLesson?.();
	}

	// Get lesson display name
	function getLessonDisplayName(results: LessonResults | null): string {
		if (!results) return 'Unknown Lesson';

		switch (results.lessonType) {
			case 'pictograph_to_letter':
				return 'Lesson 1: Pictograph to Letter';
			case 'letter_to_pictograph':
				return 'Lesson 2: Letter to Pictograph';
			case 'valid_next_pictograph':
				return 'Lesson 3: Valid Next Pictograph';
			default:
				return 'Unknown Lesson';
		}
	}

	// Get quiz mode display name
	function getQuizModeDisplayName(results: LessonResults | null): string {
		if (!results) return 'Unknown Mode';

		switch (results.quizMode) {
			case 'fixed_question':
				return 'Fixed Questions';
			case 'countdown':
				return 'Countdown';
			default:
				return 'Unknown Mode';
		}
	}

	// Format time
	function formatTime(seconds: number): string {
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = Math.floor(seconds % 60);
		return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
	}

	// Get performance grade
	function getPerformanceGrade(accuracy: number): {
		grade: string;
		color: string;
		message: string;
	} {
		if (accuracy >= 90) return { grade: 'A', color: '#10b981', message: 'Excellent!' };
		if (accuracy >= 80) return { grade: 'B', color: '#3b82f6', message: 'Great job!' };
		if (accuracy >= 70) return { grade: 'C', color: '#f59e0b', message: 'Good work!' };
		if (accuracy >= 60) return { grade: 'D', color: '#ef4444', message: 'Keep practicing!' };
		return { grade: 'F', color: '#dc2626', message: 'Try again!' };
	}

	// Get performance feedback
	function getPerformanceFeedback(results: LessonResults): string {
		const accuracy = results.accuracyPercentage;
		const avgTime = results.averageTimePerQuestion || 0;

		if (accuracy >= 90) {
			if (avgTime < 3) {
				return "Outstanding! You're both accurate and fast.";
			} else {
				return 'Excellent accuracy! You really understand this lesson.';
			}
		} else if (accuracy >= 70) {
			return 'Good progress! Keep practicing to improve your speed and accuracy.';
		} else {
			return "Don't give up! Review the lesson materials and try again.";
		}
	}

	// Get achievement badges
	function getAchievements(results: LessonResults): string[] {
		const achievements: string[] = [];

		if (results.accuracyPercentage === 100) {
			achievements.push('🎯 Perfect Score');
		}
		if (results.accuracyPercentage >= 90) {
			achievements.push('⭐ High Achiever');
		}
		if (results.averageTimePerQuestion && results.averageTimePerQuestion < 3) {
			achievements.push('⚡ Speed Demon');
		}
		if (results.streakLongestCorrect && results.streakLongestCorrect >= 5) {
			achievements.push('🔥 Hot Streak');
		}
		if (results.completionTimeSeconds < 60) {
			achievements.push('🏃 Quick Learner');
		}

		return achievements;
	}
</script>

<div class="lesson-results">
	<!-- Header -->
	<div class="results-header glass-surface">
		<button class="back-button btn-glass" onclick={handleBackClick}> ← Back to Lessons </button>
		<div class="lesson-info">
			<h2 class="lesson-title">Lesson Complete!</h2>
			<p class="lesson-subtitle">{getLessonDisplayName(results)}</p>
		</div>
	</div>

	<!-- Results Content -->
	<div class="results-content">
		{#if results}
			<!-- Actual Results -->
			<div class="results-card glass-surface">
				<div class="performance-summary">
					<div
						class="grade-circle"
						style="border-color: {getPerformanceGrade(results.accuracyPercentage)
							.color}"
					>
						<span
							class="grade-letter"
							style="color: {getPerformanceGrade(results.accuracyPercentage).color}"
						>
							{getPerformanceGrade(results.accuracyPercentage).grade}
						</span>
					</div>
					<div class="accuracy-text">
						<span class="accuracy-percentage"
							>{results.accuracyPercentage.toFixed(1)}%</span
						>
						<span class="accuracy-label">Accuracy</span>
						<span class="performance-message"
							>{getPerformanceGrade(results.accuracyPercentage).message}</span
						>
					</div>
				</div>

				<!-- Performance Feedback -->
				<div class="feedback-section">
					<p class="feedback-text">{getPerformanceFeedback(results)}</p>
				</div>

				<!-- Achievements -->
				{#if getAchievements(results).length > 0}
					<div class="achievements-section">
						<h4>Achievements</h4>
						<div class="achievements-grid">
							{#each getAchievements(results) as achievement}
								<div class="achievement-badge">
									{achievement}
								</div>
							{/each}
						</div>
					</div>
				{/if}

				<div class="stats-grid">
					<div class="stat-item">
						<span class="stat-value">{results.correctAnswers}</span>
						<span class="stat-label">Correct</span>
					</div>
					<div class="stat-item">
						<span class="stat-value">{results.incorrectGuesses}</span>
						<span class="stat-label">Incorrect</span>
					</div>
					<div class="stat-item">
						<span class="stat-value">{results.totalQuestions}</span>
						<span class="stat-label">Total</span>
					</div>
					<div class="stat-item">
						<span class="stat-value">{formatTime(results.completionTimeSeconds)}</span>
						<span class="stat-label">Time</span>
					</div>
				</div>

				<div class="lesson-details">
					<p><strong>Mode:</strong> {getQuizModeDisplayName(results)}</p>
					<p><strong>Completed:</strong> {results.completedAt.toLocaleDateString()}</p>
				</div>
			</div>
		{:else}
			<!-- Placeholder Results -->
			<div class="placeholder-results glass-surface">
				<div class="placeholder-icon">🏆</div>
				<h3>Lesson Results</h3>
				<p>Lesson completion results will be displayed here.</p>
				<div class="coming-soon">
					<p>🚧 Coming Soon:</p>
					<ul>
						<li>Accuracy Percentage</li>
						<li>Time Tracking</li>
						<li>Performance Grades</li>
						<li>Progress Statistics</li>
						<li>Achievement Badges</li>
					</ul>
				</div>
			</div>
		{/if}

		<!-- Action Buttons -->
		<div class="action-buttons">
			<button class="retry-button btn-primary" onclick={handleRetryClick}>
				🔄 Retry Lesson
			</button>
			<button class="new-lesson-button btn-glass" onclick={handleBackClick}>
				📚 Choose New Lesson
			</button>
		</div>
	</div>
</div>

<style>
	.lesson-results {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		gap: var(--spacing-lg);
		padding: var(--spacing-lg);
	}

	.results-header {
		display: flex;
		align-items: center;
		gap: var(--spacing-lg);
		padding: var(--spacing-md) var(--spacing-lg);
		border-radius: 12px;
	}

	.back-button {
		padding: var(--spacing-sm) var(--spacing-md);
		border-radius: 8px;
		font-size: var(--font-size-sm);
		font-weight: 500;
		transition: all var(--transition-normal);
		white-space: nowrap;
	}

	.back-button:hover {
		transform: translateX(-2px);
	}

	.lesson-info {
		flex: 1;
	}

	.lesson-title {
		color: var(--foreground);
		font-family: Georgia, serif;
		font-size: var(--font-size-xl);
		font-weight: bold;
		margin: 0 0 var(--spacing-xs) 0;
	}

	.lesson-subtitle {
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
		margin: 0;
	}

	.results-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--spacing-xl);
	}

	.results-card,
	.placeholder-results {
		padding: var(--spacing-2xl);
		border-radius: 16px;
		max-width: 600px;
		width: 100%;
		text-align: center;
	}

	.performance-summary {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--spacing-lg);
		margin-bottom: var(--spacing-xl);
	}

	.grade-circle {
		width: 80px;
		height: 80px;
		border: 4px solid;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.grade-letter {
		font-size: 2rem;
		font-weight: bold;
		font-family: Georgia, serif;
	}

	.accuracy-text {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.accuracy-percentage {
		font-size: 2.5rem;
		font-weight: bold;
		color: var(--foreground);
	}

	.accuracy-label {
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
	}

	.performance-message {
		color: var(--foreground);
		font-size: var(--font-size-sm);
		font-weight: 600;
		margin-top: var(--spacing-xs);
	}

	.feedback-section {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		padding: var(--spacing-md);
		margin-bottom: var(--spacing-lg);
	}

	.feedback-text {
		color: var(--foreground);
		font-size: var(--font-size-base);
		margin: 0;
		text-align: center;
		font-style: italic;
	}

	.achievements-section {
		margin-bottom: var(--spacing-lg);
	}

	.achievements-section h4 {
		color: var(--foreground);
		font-size: var(--font-size-lg);
		margin: 0 0 var(--spacing-md) 0;
		text-align: center;
	}

	.achievements-grid {
		display: flex;
		flex-wrap: wrap;
		gap: var(--spacing-sm);
		justify-content: center;
	}

	.achievement-badge {
		background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
		color: #000000;
		padding: var(--spacing-xs) var(--spacing-sm);
		border-radius: 20px;
		font-size: var(--font-size-sm);
		font-weight: 600;
		box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
		animation: badgeAppear 0.5s ease-out;
	}

	@keyframes badgeAppear {
		0% {
			opacity: 0;
			transform: scale(0.8) translateY(10px);
		}
		100% {
			opacity: 1;
			transform: scale(1) translateY(0);
		}
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: var(--spacing-lg);
		margin-bottom: var(--spacing-xl);
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--spacing-xs);
	}

	.stat-value {
		font-size: var(--font-size-xl);
		font-weight: bold;
		color: var(--foreground);
	}

	.stat-label {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
	}

	.lesson-details {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		padding: var(--spacing-md);
		text-align: left;
	}

	.lesson-details p {
		color: var(--foreground);
		margin: var(--spacing-xs) 0;
		font-size: var(--font-size-sm);
	}

	.placeholder-icon {
		font-size: 4rem;
		margin-bottom: var(--spacing-lg);
	}

	.placeholder-results h3 {
		color: var(--foreground);
		font-size: var(--font-size-2xl);
		margin-bottom: var(--spacing-md);
	}

	.placeholder-results > p {
		color: var(--muted-foreground);
		font-size: var(--font-size-lg);
		margin-bottom: var(--spacing-xl);
	}

	.coming-soon {
		text-align: left;
		background: rgba(255, 255, 255, 0.03);
		border-radius: 8px;
		padding: var(--spacing-md);
	}

	.coming-soon p {
		color: var(--muted-foreground);
		font-weight: 500;
		margin-bottom: var(--spacing-sm);
	}

	.coming-soon ul {
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
		margin: 0;
		padding-left: var(--spacing-lg);
	}

	.coming-soon li {
		margin-bottom: var(--spacing-xs);
	}

	.action-buttons {
		display: flex;
		gap: var(--spacing-md);
		justify-content: center;
		flex-wrap: wrap;
	}

	.retry-button,
	.new-lesson-button {
		padding: var(--spacing-md) var(--spacing-lg);
		border-radius: 12px;
		font-weight: 500;
		transition: all var(--transition-normal);
		min-width: 160px;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.lesson-results {
			padding: var(--spacing-md);
			gap: var(--spacing-md);
		}

		.results-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--spacing-md);
		}

		.stats-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.performance-summary {
			flex-direction: column;
			gap: var(--spacing-md);
		}

		.grade-circle {
			width: 60px;
			height: 60px;
		}

		.grade-letter {
			font-size: 1.5rem;
		}

		.accuracy-percentage {
			font-size: 2rem;
		}
	}

	@media (max-width: 480px) {
		.lesson-results {
			padding: var(--spacing-sm);
		}

		.results-card,
		.placeholder-results {
			padding: var(--spacing-lg);
		}

		.action-buttons {
			flex-direction: column;
		}

		.retry-button,
		.new-lesson-button {
			min-width: auto;
		}
	}
</style>
