<script lang="ts">
	import CodexComponent from '$lib/components/codex/CodexComponent.svelte';
	import LessonResultsView from '$lib/components/learn/LessonResultsView.svelte';
	import LessonSelectorView from '$lib/components/learn/LessonSelectorView.svelte';
	import LessonWorkspaceView from '$lib/components/learn/LessonWorkspaceView.svelte';
	import { LearnView, LessonType, QuizMode, type LessonResults } from '$lib/types/learn';
	import type { ServiceContainer } from '$services/di/ServiceContainer';
	import type {
		IApplicationInitializationService,
		IDeviceDetectionService,
		ISequenceService,
		ISettingsService,
	} from '$services/interfaces';
	import { getContext } from 'svelte';

	// Get DI container from context (like real app)
	const getContainer = getContext<() => ServiceContainer | null>('di-container');

	// Services - resolved lazily (like real app)
	let initService: IApplicationInitializationService | null = $state(null);
	let settingsService: ISettingsService | null = $state(null);
	let sequenceService: ISequenceService | null = $state(null);
	let deviceService: IDeviceDetectionService | null = $state(null);

	let codexWidth = $state(50); // percentage
	let isResizing = $state(false);
	let codexVisible = $state(true);

	// Learn tab state matching real implementation
	let currentView = $state(LearnView.LESSON_SELECTOR);
	let selectedMode = $state(QuizMode.FIXED_QUESTION);
	let currentLessonType = $state(null);
	let currentResults = $state(null);
	let isLoading = $state(false);
	let availableLessons = $state(Object.values(LessonType));
	let performanceData = $state({
		lagEvents: [],
		moveEvents: [],
		lagThreshold: 5,
	});

	let lagCount = $derived(performanceData.lagEvents.length);
	let avgTime = $derived(
		performanceData.moveEvents.length > 0
			? (
					performanceData.moveEvents.reduce((sum, e) => sum + e.duration, 0) /
					performanceData.moveEvents.length
				).toFixed(2)
			: 0
	);
	let worstLag = $derived(
		performanceData.lagEvents.length > 0
			? Math.max(...performanceData.lagEvents.map((e) => e.duration)).toFixed(2)
			: 0
	);

	// Resolve services when container is available (like real app)
	$effect(() => {
		const container = getContainer?.();
		if (container && !initService) {
			try {
				initService = container.resolve('IApplicationInitializationService');
				settingsService = container.resolve('ISettingsService');
				sequenceService = container.resolve('ISequenceService');
				deviceService = container.resolve('IDeviceDetectionService');
				console.log('✅ Test page: Services resolved successfully');
			} catch (error) {
				console.error('Test page: Failed to resolve services:', error);
			}
		}
	});

	// Navigation handlers matching real Learn tab
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

	// Handlers for CodexComponent
	function handlePictographSelected(pictograph) {
		console.log('Pictograph selected:', pictograph);
	}

	function handleCodexToggle() {
		codexVisible = !codexVisible;
	}

	// Handlers for LessonSelectorView are defined above with real implementation

	function handleResizeStart(event) {
		isResizing = true;
		event.preventDefault();

		const startX = event.clientX;
		const startWidth = codexWidth;
		const containerWidth = event.target.closest('.learn-content-wrapper')?.clientWidth || 1000;

		// Reset performance data
		performanceData.lagEvents = [];
		performanceData.moveEvents = [];

		function handleMouseMove(e) {
			if (!isResizing) return;

			const moveStartTime = performance.now();

			const deltaX = e.clientX - startX;
			const deltaPercent = (deltaX / containerWidth) * 100;
			const newWidth = Math.max(15, Math.min(60, startWidth + deltaPercent));

			codexWidth = newWidth;

			const moveEndTime = performance.now();
			const moveDuration = moveEndTime - moveStartTime;

			performanceData.moveEvents.push({
				duration: moveDuration,
				timestamp: moveEndTime,
			});

			if (moveDuration > performanceData.lagThreshold) {
				performanceData.lagEvents.push({
					duration: moveDuration,
					timestamp: moveEndTime,
				});
			}

			// Trigger reactivity for Svelte 5 runes
			performanceData.lagEvents = [...performanceData.lagEvents];
			performanceData.moveEvents = [...performanceData.moveEvents];
		}

		function handleMouseUp() {
			isResizing = false;

			console.log('Complex drag session complete:', {
				totalMoves: performanceData.moveEvents.length,
				lagEvents: performanceData.lagEvents.length,
				avgTime:
					performanceData.moveEvents.length > 0
						? (
								performanceData.moveEvents.reduce((sum, e) => sum + e.duration, 0) /
								performanceData.moveEvents.length
							).toFixed(2) + 'ms'
						: '0ms',
			});

			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		}

		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
	}
</script>

<div class="performance-info">
	Complex Drag Performance Monitor<br />
	Lag Events: <span>{lagCount}</span><br />
	Avg Time: <span>{avgTime}ms</span><br />
	Worst Lag: <span>{worstLag}ms</span><br />
	Codex Width: <span>{codexWidth.toFixed(1)}%</span>
</div>

<div class="learn-tab">
	<div class="learn-content-wrapper">
		<div class="codex-sidebar" style="width: {codexWidth}%;">
			<CodexComponent
				isVisible={codexVisible}
				onPictographSelected={handlePictographSelected}
				onToggleVisibility={handleCodexToggle}
			/>
		</div>

		<button
			class="resize-handle"
			class:resizing={isResizing}
			onmousedown={handleResizeStart}
			aria-label="Resize codex panel"
		></button>

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
</div>

<style>
	.learn-tab {
		display: flex;
		flex-direction: column;
		height: 100vh;
		background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
		color: white;
	}

	.learn-content-wrapper {
		display: flex;
		flex: 1;
		overflow: hidden;
	}

	.codex-sidebar {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		border-right: 1px solid rgba(255, 255, 255, 0.2);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		/* REMOVED CSS TRANSITION - THIS WAS CAUSING THE LAG! */
	}

	.codex-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
	}

	.codex-title h3 {
		margin: 0;
		font-size: 1.2rem;
	}

	.codex-subtitle {
		font-size: 0.8rem;
		opacity: 0.8;
	}

	.codex-toggle {
		background: none;
		border: none;
		color: white;
		font-size: 1.2rem;
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 4px;
	}

	.codex-controls {
		padding: 1rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
	}

	.orientation-control {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.orientation-control select {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 0.25rem;
		border-radius: 4px;
	}

	.transform-controls {
		display: flex;
		gap: 0.5rem;
	}

	.transform-controls button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 0.5rem;
		border-radius: 4px;
		cursor: pointer;
	}

	.pictograph-grid {
		flex: 1;
		overflow-y: auto;
		padding: 1rem;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
		gap: 0.5rem;
	}

	.pictograph-button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 4px;
		padding: 0.25rem;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.pictograph-button:hover {
		background: rgba(255, 255, 255, 0.2);
	}

	.pictograph-button img {
		width: 100%;
		height: auto;
		display: block;
	}

	.resize-handle {
		width: 4px;
		background: rgba(255, 255, 255, 0.3);
		cursor: col-resize;
		border: none;
		padding: 0;
		margin: 0;
		transition: background-color 0.2s;
	}

	.resize-handle:hover,
	.resize-handle.resizing {
		background: rgba(255, 255, 255, 0.6);
	}

	.lesson-content {
		flex: 1;
		padding: 2rem;
		overflow-y: auto;
	}

	.lesson-content h1 {
		margin: 0 0 2rem 0;
		font-size: 2rem;
	}

	.lesson-mode-buttons {
		display: flex;
		gap: 1rem;
		margin-bottom: 2rem;
	}

	.lesson-mode-buttons button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		cursor: pointer;
		font-size: 1rem;
	}

	.lesson-list {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.lesson-item {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.lesson-item button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 1rem;
		border-radius: 8px;
		cursor: pointer;
		font-size: 1.1rem;
		text-align: left;
	}

	.lesson-item p {
		margin: 0;
		opacity: 0.8;
		font-size: 0.9rem;
	}

	.performance-info {
		position: fixed;
		top: 10px;
		right: 10px;
		background: rgba(0, 0, 0, 0.8);
		color: white;
		padding: 10px;
		border-radius: 5px;
		font-family: monospace;
		font-size: 12px;
		z-index: 1000;
	}
</style>
