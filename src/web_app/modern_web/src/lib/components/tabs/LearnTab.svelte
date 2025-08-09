<!-- Learn Tab - Educational content with pixel-perfect desktop replica -->
<script lang="ts">
	import { LearnView, QuizMode, LessonType, type LessonResults } from '$lib/types/learn';
	import LessonSelectorView from '$lib/components/learn/LessonSelectorView.svelte';
	import LessonWorkspaceView from '$lib/components/learn/LessonWorkspaceView.svelte';
	import LessonResultsView from '$lib/components/learn/LessonResultsView.svelte';

	// State management using runes
	let currentView = $state<LearnView>(LearnView.LESSON_SELECTOR);
	let selectedMode = $state<QuizMode>(QuizMode.FIXED_QUESTION);
	let currentLessonType = $state<LessonType | null>(null);
	let currentResults = $state<LessonResults | null>(null);
	let isLoading = $state<boolean>(false);

	// Available lessons (all enabled for now)
	let availableLessons = $state<LessonType[]>(Object.values(LessonType));

	// Navigation handlers
	function handleLessonRequested(event: { lessonType: LessonType; quizMode: QuizMode }) {
		isLoading = true;

		// Small delay for smooth transition
		setTimeout(() => {
			currentLessonType = event.lessonType;
			selectedMode = event.quizMode;
			currentView = LearnView.LESSON_WORKSPACE;
			currentResults = null;
			isLoading = false;
		}, 300);
	}

	function handleModeChanged(mode: QuizMode) {
		selectedMode = mode;
	}

	function handleBackToSelector() {
		isLoading = true;

		// Small delay for smooth transition
		setTimeout(() => {
			currentView = LearnView.LESSON_SELECTOR;
			currentLessonType = null;
			currentResults = null;
			isLoading = false;
		}, 200);
	}

	function handleRetryLesson() {
		if (currentLessonType) {
			isLoading = true;

			// Small delay for smooth transition
			setTimeout(() => {
				currentView = LearnView.LESSON_WORKSPACE;
				currentResults = null;
				isLoading = false;
			}, 200);
		}
	}

	function handleLessonComplete(results: LessonResults) {
		isLoading = true;

		// Small delay for smooth transition
		setTimeout(() => {
			currentResults = results;
			currentView = LearnView.LESSON_RESULTS;
			isLoading = false;
		}, 500); // Longer delay to show completion feedback
	}
</script>

<div class="learn-tab">
	<!-- Loading Overlay -->
	{#if isLoading}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
			<p class="loading-text">
				{#if currentView === LearnView.LESSON_SELECTOR}
					Loading lessons...
				{:else if currentView === LearnView.LESSON_WORKSPACE}
					Starting lesson...
				{:else}
					Processing results...
				{/if}
			</p>
		</div>
	{/if}

	<!-- Main content area with stacked views -->
	<div class="learn-content" class:loading={isLoading}>
		{#if currentView === LearnView.LESSON_SELECTOR}
			<div class="view-container" class:active={!isLoading}>
				<LessonSelectorView
					bind:selectedMode
					{availableLessons}
					isLoading={false}
					onLessonRequested={handleLessonRequested}
					onModeChanged={handleModeChanged}
				/>
			</div>
		{:else if currentView === LearnView.LESSON_WORKSPACE}
			<div class="view-container" class:active={!isLoading}>
				<LessonWorkspaceView
					lessonType={currentLessonType}
					quizMode={selectedMode}
					onBackToSelector={handleBackToSelector}
					onLessonComplete={handleLessonComplete}
				/>
			</div>
		{:else if currentView === LearnView.LESSON_RESULTS}
			<div class="view-container" class:active={!isLoading}>
				<LessonResultsView
					results={currentResults}
					onBackToSelector={handleBackToSelector}
					onRetryLesson={handleRetryLesson}
				/>
			</div>
		{/if}
	</div>
</div>

<style>
	.learn-tab {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		position: relative;
		overflow: hidden;
		background: transparent;
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		z-index: 1000;
		backdrop-filter: blur(4px);
		animation: fadeIn 0.3s ease-out;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.1);
		border-left: 4px solid #667eea;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.loading-text {
		color: #ffffff;
		font-size: 1rem;
		font-weight: 500;
		margin: 0;
		text-align: center;
	}

	.learn-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		position: relative;
		transition: opacity 0.3s ease-out;
	}

	.learn-content.loading {
		opacity: 0.3;
		pointer-events: none;
	}

	.view-container {
		width: 100%;
		height: 100%;
		opacity: 0;
		transform: translateY(20px);
		transition: all 0.4s ease-out;
	}

	.view-container.active {
		opacity: 1;
		transform: translateY(0);
	}

	/* Animations */
	@keyframes fadeIn {
		0% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.learn-tab {
			position: relative;
		}

		.loading-text {
			font-size: 0.875rem;
		}

		.loading-spinner {
			width: 32px;
			height: 32px;
			border-width: 3px;
		}
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.loading-overlay,
		.learn-content,
		.view-container {
			transition: none;
			animation: none;
		}

		.loading-spinner {
			animation: none;
			border-left-color: transparent;
			border-top-color: #667eea;
		}
	}
</style>
