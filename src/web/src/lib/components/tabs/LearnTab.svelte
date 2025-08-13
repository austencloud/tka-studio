<!-- Learn Tab - Educational content with pixel-perfect desktop replica -->
<script lang="ts">
	import CodexComponent from '$lib/components/codex/CodexComponent.svelte';
	import LessonResultsView from '$lib/components/learn/LessonResultsView.svelte';
	import LessonSelectorView from '$lib/components/learn/LessonSelectorView.svelte';
	import LessonWorkspaceView from '$lib/components/learn/LessonWorkspaceView.svelte';
	import type { PictographData } from '$lib/domain/PictographData';
	import { LearnView, LessonType, QuizMode, type LessonResults } from '$lib/types/learn';

	// State management using regular Svelte reactivity for better performance
	let currentView: LearnView = LearnView.LESSON_SELECTOR;
	let selectedMode: QuizMode = QuizMode.FIXED_QUESTION;
	let currentLessonType: LessonType | null = null;
	let currentResults: LessonResults | null = null;
	let isLoading: boolean = false;
	let codexVisible: boolean = true;
	let codexWidth: number = 50; // Default 50% width (1/2 of page)
	let isResizing: boolean = false;

	// Available lessons (all enabled for now)
	let availableLessons: LessonType[] = Object.values(LessonType);

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

	// Resize functionality optimized for Svelte 5 runes performance
	function handleResizeStart(event: MouseEvent) {
		isResizing = true;
		event.preventDefault();

		const startX = event.clientX;
		const startWidth = codexWidth;
		const containerWidth = window.innerWidth;

		function handleMouseMove(e: MouseEvent) {
			if (!isResizing) return;

			const deltaX = e.clientX - startX;
			const deltaPercent = (deltaX / containerWidth) * 100;
			const newWidth = Math.max(15, Math.min(60, startWidth + deltaPercent));
			codexWidth = newWidth;
		}

		function handleMouseUp() {
			isResizing = false;
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		}

		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
	}

	function handlePictographSelected(pictograph: PictographData) {
		// Handle pictograph selection from codex (for reference during learning)
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

		<!-- Codex Sidebar - Always present but can be collapsed -->
		<div
			class="codex-sidebar"
			class:collapsed={!codexVisible}
			style="width: {codexVisible ? codexWidth + '%' : '48px'}"
		>
			<CodexComponent
				isVisible={codexVisible}
				onPictographSelected={handlePictographSelected}
				onToggleVisibility={handleCodexToggle}
			/>
		</div>

		<!-- Resize handle - only show when expanded -->
		{#if codexVisible}
			<button
				class="resize-handle"
				class:resizing={isResizing}
				onmousedown={handleResizeStart}
				aria-label="Resize codex panel"
			></button>
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

	/* MAIN LAYOUT: Horizontal splitter (side-by-side) */
	.learn-content-wrapper {
		display: flex;
		flex-direction: row; /* DEFAULT: Horizontal layout */
		flex: 1;
		width: 100%;
		height: 100%;
		gap: 1rem;
		padding: 1rem;
		min-height: 0;
	}

	.codex-sidebar {
		/* Width is now controlled by inline style */
		min-width: 250px;
		max-width: 60%; /* Allow more flexibility */
		flex-shrink: 0;
		height: 100%;
		/* REMOVED CSS TRANSITION - THIS WAS CAUSING THE DRAG LAG! */
		border-right: 1px solid var(--desktop-border-tertiary);
	}

	.codex-sidebar.collapsed {
		min-width: 48px; /* Minimal collapsed width like VS Code */
		max-width: 48px;
	}

	.resize-handle {
		width: 4px;
		height: 100%;
		background: rgba(80, 80, 100, 0.4);
		cursor: col-resize;
		flex-shrink: 0;
		position: relative;
		transition: background-color 0.2s ease;
		border: none;
		padding: 0;
		margin: 0;
		outline: none;
	}

	.resize-handle:hover,
	.resize-handle.resizing {
		background: rgba(120, 150, 200, 0.8);
	}

	.resize-handle:focus {
		background: rgba(120, 150, 200, 0.6);
		outline: 2px solid rgba(120, 150, 200, 0.8);
		outline-offset: 1px;
	}

	.resize-handle::before {
		content: '';
		position: absolute;
		left: -2px;
		right: -2px;
		top: 0;
		bottom: 0;
		background: transparent;
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
			min-width: 200px;
		}
	}

	/* Small tablets - further reduce but stay horizontal */
	@media (max-width: 768px) and (min-width: 641px) {
		.codex-sidebar {
			min-width: 180px;
		}

		.learn-content-wrapper {
			gap: 0.75rem;
			padding: 0.75rem;
			padding-top: 3.5rem;
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
