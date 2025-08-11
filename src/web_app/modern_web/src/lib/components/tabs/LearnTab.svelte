<!-- Learn Tab - Educational content with pixel-perfect desktop replica -->
<script lang="ts">
	import CodexComponent from '$lib/components/codex/CodexComponent.svelte';
	import LessonResultsView from '$lib/components/learn/LessonResultsView.svelte';
	import LessonSelectorView from '$lib/components/learn/LessonSelectorView.svelte';
	import LessonWorkspaceView from '$lib/components/learn/LessonWorkspaceView.svelte';
	import type { PictographData } from '$lib/domain/PictographData';
	import { LearnView, LessonType, QuizMode, type LessonResults } from '$lib/types/learn';

	// State management using runes
	let currentView = $state<LearnView>(LearnView.LESSON_SELECTOR);
	let selectedMode = $state<QuizMode>(QuizMode.FIXED_QUESTION);
	let currentLessonType = $state<LessonType | null>(null);
	let currentResults = $state<LessonResults | null>(null);
	let isLoading = $state<boolean>(false);
	let codexVisible = $state<boolean>(true);

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

	// Codex handlers
	function handleCodexToggle() {
		codexVisible = !codexVisible;
	}

	function handlePictographSelected(pictograph: PictographData) {
		// Handle pictograph selection from codex (for reference during learning)
		console.log('Pictograph selected from codex:', pictograph);
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
	<!-- Codex Toggle Button -->
	<button class="codex-toggle" onclick={handleCodexToggle}>
		{codexVisible ? 'Hide' : 'Show'} Codex
	</button>

	<!-- Main Content with Splitter Layout -->
	<div class="learn-content-wrapper" class:codex-visible={codexVisible}>
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

		<!-- Codex Sidebar -->
		{#if codexVisible}
			<div class="codex-sidebar">
				<CodexComponent
					isVisible={codexVisible}
					onPictographSelected={handlePictographSelected}
					onToggleVisibility={handleCodexToggle}
				/>
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

	.codex-toggle {
		position: absolute;
		top: 1rem;
		left: 1rem;
		z-index: 1001;
		padding: 0.5rem 1rem;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		color: #ffffff;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
		backdrop-filter: blur(10px);
	}

	.codex-toggle:hover {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.3);
	}

	/* MAIN LAYOUT: Horizontal splitter (side-by-side) */
	.learn-content-wrapper {
		display: flex;
		flex-direction: row; /* DEFAULT: Horizontal layout */
		flex: 1;
		width: 100%;
		height: 100%;
		gap: 1rem;
		padding: 1rem;
		padding-top: 4rem; /* Space for toggle button */
		min-height: 0;
	}

	.codex-sidebar {
		width: 300px;
		min-width: 250px;
		max-width: 400px;
		flex-shrink: 0;
		height: 100%;
		transition: all 0.3s ease;
	}

	.learn-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		position: relative;
		transition: opacity 0.3s ease-out;
		min-width: 0; /* Allow shrinking */
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

	/* When codex is hidden, content takes full width */
	.learn-content-wrapper:not(.codex-visible) {
		padding-top: 1rem;
	}

	.learn-content-wrapper:not(.codex-visible) .learn-content {
		width: 100%;
		max-width: none;
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

	/* Responsive Design - MAINTAIN HORIZONTAL LAYOUT */
	
	/* Tablets and larger screens - keep horizontal */
	@media (min-width: 769px) {
		.learn-content-wrapper {
			flex-direction: row !important; /* Force horizontal */
		}
	}

	/* Medium tablets - reduce codex width but stay horizontal */
	@media (max-width: 1024px) and (min-width: 769px) {
		.codex-sidebar {
			width: 250px;
			min-width: 200px;
		}
	}

	/* Small tablets - further reduce but stay horizontal */
	@media (max-width: 768px) and (min-width: 641px) {
		.codex-sidebar {
			width: 220px;
			min-width: 180px;
		}
		
		.learn-content-wrapper {
			gap: 0.75rem;
			padding: 0.75rem;
			padding-top: 3.5rem;
		}
		
		.codex-toggle {
			top: 0.75rem;
			left: 0.75rem;
			font-size: 0.8rem;
			padding: 0.4rem 0.8rem;
		}
	}

	/* ONLY on very small mobile screens (phones) - stack vertically */
	@media (max-width: 640px) {
		.learn-content-wrapper {
			flex-direction: column; /* Only stack on phones */
			padding: 0.5rem;
			padding-top: 3.5rem;
			gap: 0.5rem;
		}

		.codex-sidebar {
			width: 100%;
			min-width: unset;
			max-width: none;
			height: 200px;
			flex-shrink: 0;
		}

		.codex-toggle {
			top: 0.5rem;
			left: 0.5rem;
			font-size: 0.75rem;
			padding: 0.375rem 0.75rem;
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
