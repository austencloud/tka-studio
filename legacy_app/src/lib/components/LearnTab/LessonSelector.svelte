<script lang="ts">
	import { onMount } from 'svelte';
	import { fly, scale } from 'svelte/transition';
	import { elasticOut, cubicOut } from 'svelte/easing';
	import { learnStore, type LessonMode } from '$lib/state/stores/learn/learnStore';
	import { lessonConfigs } from '$lib/state/stores/learn/lesson_configs';
	import { progressStore, badgeStatus } from '$lib/state/stores/learn/progressStore';
	import LessonModeToggle from './LessonModeToggle.svelte';

	// Track hover state for cards
	let hoveredCard: string | null = null;

	// Calculate progress percentage
	function getProgressPercentage(lessonId: string): number {
		const lessonProgress = $progressStore.lessonProgress[lessonId];
		return lessonProgress ? Math.round((lessonProgress.completed / lessonProgress.total) * 100) : 0;
	}

	// Get badge status from the derived store
	function getBadgeStatus(lessonId: string): 'none' | 'bronze' | 'silver' | 'gold' {
		return $badgeStatus[lessonId] || 'none';
	}

	// Handle lesson selection
	function selectLesson(lessonId: string) {
		learnStore.selectLesson(lessonId);
		learnStore.startLesson();
	}

	// Handle mode change
	function handleModeChange(mode: LessonMode) {
		learnStore.setMode(mode);
	}

	// Component initialization
	onMount(() => {
		// Any initialization can go here
	});
</script>

<div class="lesson-selector">
	<div class="header-section">
		<h1>Learning Journey</h1>
		<p class="subtitle">Master pictographs through interactive lessons</p>

		<div class="mode-toggle-container">
			<div class="mode-label">Quiz Mode:</div>
			<LessonModeToggle
				selected={$learnStore.selectedMode}
				on:change={(e) => handleModeChange(e.detail)}
			/>
		</div>
	</div>

	<div class="learning-paths">
		<h2 class="section-title">
			<span class="icon">🧠</span>
			<span>Learning Paths</span>
		</h2>

		<div class="lessons-grid">
			{#each lessonConfigs as lesson, i}
				<button
					class="lesson-card"
					class:hovered={hoveredCard === lesson.id}
					on:click={() => selectLesson(lesson.id)}
					on:mouseenter={() => (hoveredCard = lesson.id)}
					on:mouseleave={() => (hoveredCard = null)}
					in:fly={{ y: 30, delay: 100 + i * 100, duration: 600, easing: cubicOut }}
				>
					<div class="card-content">
						<div class="card-header">
							<div class="lesson-icon">
								{#if lesson.id === 'letter_to_pictograph'}
									<span>A→◯</span>
								{:else if lesson.id === 'pictograph_to_letter'}
									<span>◯→A</span>
								{:else if lesson.id === 'turns'}
									<span>↻↺</span>
								{:else if lesson.id === 'positions'}
									<span>⬆⬇</span>
								{/if}
							</div>

							<div class="badge-container">
								{#if getBadgeStatus(lesson.id) !== 'none'}
									<div class="badge {getBadgeStatus(lesson.id)}">
										{#if getBadgeStatus(lesson.id) === 'gold'}
											🥇
										{:else if getBadgeStatus(lesson.id) === 'silver'}
											🥈
										{:else}
											🥉
										{/if}
									</div>
								{/if}
							</div>
						</div>

						<h3>{lesson.title}</h3>
						<p>{lesson.description}</p>

						<div class="lesson-format">
							<span class="format-label">Q: {lesson.questionFormat}</span>
							<span class="format-label">A: {lesson.answerFormat}</span>
						</div>

						<div class="progress-container">
							<div class="progress-bar">
								<div class="progress-fill" style="width: {getProgressPercentage(lesson.id)}%"></div>
							</div>
							<div class="progress-text">
								{getProgressPercentage(lesson.id)}% Complete
							</div>
						</div>
					</div>

					<div class="card-overlay"></div>

					{#if hoveredCard === lesson.id}
						<div class="start-button" in:scale={{ duration: 200, easing: elasticOut }}>
							Start Lesson
						</div>
					{/if}
				</button>
			{/each}
		</div>
	</div>

	<div class="achievements-section">
		<h2 class="section-title">
			<span class="icon">🏆</span>
			<span>Your Progress</span>
		</h2>

		<div class="stats-container" in:fly={{ y: 20, duration: 500, delay: 500 }}>
			<div class="stat-card">
				<div class="stat-value">{$progressStore.totalLessonsStarted}</div>
				<div class="stat-label">Lessons Started</div>
			</div>

			<div class="stat-card">
				<div class="stat-value">{$progressStore.totalQuestionsAnswered}</div>
				<div class="stat-label">Questions Answered</div>
			</div>

			<div class="stat-card">
				<div class="stat-value">{$progressStore.averageScore}<span class="percent">%</span></div>
				<div class="stat-label">Average Score</div>
			</div>
		</div>
	</div>
</div>

<style>
	.lesson-selector {
		max-width: 1000px;
		margin: 0 auto;
		width: 100%;
		padding: 2rem 1.5rem;
	}

	.header-section {
		text-align: center;
		margin-bottom: 3rem;
	}

	h1 {
		font-size: 2.5rem;
		font-weight: 800;
		margin-bottom: 0.5rem;
		background: linear-gradient(135deg, #fff, #a0a0a0);
		background-clip: text;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		letter-spacing: -0.02em;
	}

	.subtitle {
		font-size: 1.1rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		margin-bottom: 2rem;
	}

	.mode-toggle-container {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin: 0 auto;
		background: rgba(255, 255, 255, 0.05);
		padding: 0.75rem 1.5rem;
		border-radius: 999px;
		width: fit-content;
	}

	.mode-label {
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.section-title {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		font-size: 1.5rem;
		font-weight: 700;
		margin-bottom: 1.5rem;
		color: var(--color-text-primary, white);
	}

	.icon {
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.25rem;
	}

	.learning-paths {
		margin-bottom: 3rem;
	}

	.lessons-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.5rem;
		width: 100%;
		max-width: 100%;
		overflow-x: hidden;
	}

	.lesson-card {
		position: relative;
		background-color: rgba(30, 40, 60, 0.5);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 12px;
		padding: 0;
		text-align: left;
		border: 1px solid rgba(255, 255, 255, 0.05);
		cursor: pointer;
		transition: all 0.2s ease-out;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		overflow: hidden;
		height: 100%;
		width: 100%;
		box-shadow:
			0 4px 12px rgba(0, 0, 0, 0.1),
			0 1px 3px rgba(0, 0, 0, 0.05);
	}

	.card-content {
		position: relative;
		z-index: 2;
		padding: 1.5rem;
		width: 100%;
		transition: transform 0.2s ease-out;
	}

	.lesson-card:hover {
		transform: translateY(-3px); /* Reduced from -5px to -3px for subtler effect */
		box-shadow:
			0 8px 16px rgba(0, 0, 0, 0.15),
			0 1px 3px rgba(0, 0, 0, 0.1);
		border-color: rgba(58, 123, 213, 0.3);
	}

	.lesson-card:hover .card-content {
		transform: translateY(-1.5rem); /* Reduced from -2.5rem to -1.5rem for subtler effect */
	}

	.card-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(to bottom, transparent 50%, rgba(58, 123, 213, 0.1) 100%);
		z-index: 1;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.lesson-card:hover .card-overlay {
		opacity: 1;
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 1rem;
	}

	.lesson-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 3rem;
		height: 3rem;
		background: rgba(58, 123, 213, 0.15);
		border-radius: 12px;
		font-size: 1.25rem;
		font-weight: 700;
		color: var(--color-accent, #3a7bd5);
		margin-bottom: 0.5rem;
	}

	.badge-container {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.badge {
		font-size: 1.25rem;
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
	}

	h3 {
		font-size: 1.25rem;
		margin-bottom: 0.5rem;
		color: var(--color-text-primary, white);
		font-weight: 600;
	}

	p {
		font-size: 0.9rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		line-height: 1.5;
		margin-bottom: 1rem;
	}

	.lesson-format {
		display: flex;
		flex-wrap: wrap; /* Allow wrapping to prevent overflow */
		gap: 0.5rem;
		margin-bottom: 1.25rem;
		max-width: 100%; /* Ensure it doesn't exceed container width */
	}

	.format-label {
		background-color: rgba(0, 0, 0, 0.2);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-size: 0.75rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		text-transform: capitalize;
		white-space: nowrap; /* Prevent label text from wrapping */
	}

	.progress-container {
		margin-top: auto;
	}

	.progress-bar {
		height: 6px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
		overflow: hidden;
		margin-bottom: 0.5rem;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(to right, var(--color-accent, #3a7bd5), #5a9bd5);
		border-radius: 3px;
		transition: width 1s cubic-bezier(0.2, 0.8, 0.2, 1);
	}

	.progress-text {
		font-size: 0.8rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		text-align: right;
	}

	.start-button {
		position: absolute;
		bottom: 1.5rem;
		left: 0;
		width: 100%;
		text-align: center;
		font-weight: 600;
		font-size: 0.9rem;
		color: var(--color-accent, #3a7bd5);
		z-index: 3;
	}

	.achievements-section {
		margin-top: 3rem;
	}

	.stats-container {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.5rem;
	}

	.stat-card {
		background: rgba(255, 255, 255, 0.03);
		border-radius: 12px;
		padding: 1.5rem;
		text-align: center;
		border: 1px solid rgba(255, 255, 255, 0.05);
		transition: all 0.3s ease;
	}

	.stat-card:hover {
		background: rgba(255, 255, 255, 0.05);
		transform: translateY(-3px);
	}

	.stat-value {
		font-size: 2.5rem;
		font-weight: 700;
		color: var(--color-text-primary, white);
		margin-bottom: 0.5rem;
		line-height: 1;
	}

	.percent {
		font-size: 1.5rem;
		opacity: 0.7;
	}

	.stat-label {
		font-size: 0.9rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	@media (max-width: 768px) {
		.lesson-selector {
			padding: 1.5rem 1rem;
		}

		h1 {
			font-size: 2rem;
		}

		.subtitle {
			font-size: 1rem;
		}

		.lessons-grid {
			grid-template-columns: 1fr;
		}

		.stats-container {
			grid-template-columns: 1fr;
		}
	}
</style>
