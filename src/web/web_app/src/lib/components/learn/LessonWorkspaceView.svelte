<!-- LessonWorkspaceView.svelte - Enhanced lesson workspace with full functionality -->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import { LessonConfigService } from '$lib/services/learn/LessonConfigService';
	import { QuestionGeneratorService } from '$lib/services/learn/QuestionGeneratorService';
	import { QuizSessionService } from '$lib/services/learn/QuizSessionService';
	import type {
		LayoutMode,
		LessonProgress,
		LessonResults,
		LessonType,
		QuestionData,
		QuizMode,
	} from '$lib/types/learn';
	import { QuizMode as QuizModeEnum } from '$lib/types/learn';
	import { onDestroy, onMount } from 'svelte';

	import ProgressTracker from './ProgressTracker.svelte';
	import QuestionGenerator from './QuestionGenerator.svelte';
	import QuizTimer from './QuizTimer.svelte';
	import LessonControls from './LessonControls.svelte';

	// Props
	interface Props {
		lessonType?: LessonType | null;
		quizMode?: QuizMode | null;
		layoutMode?: LayoutMode;
		onBackToSelector?: () => void;
		onLessonComplete?: (results: LessonResults) => void;
	}

	let {
		lessonType = null,
		quizMode = null,
		onBackToSelector,
		onLessonComplete,
	}: Props = $props();

	// State
	let sessionId: string | null = null;
	let currentQuestion: QuestionData | null = $state(null);
	let progress: LessonProgress | null = $state(null);
	let isAnswered = $state(false);
	let showFeedback = $state(false);
	let selectedAnswerId: string | null = $state(null);
	let timeRemaining = $state(0);
	let isLoading = $state(false);
	let questionStartTime = 0;
	let isPaused = $state(false);
	let hasStarted = $state(false);

	// Component references
	let timerComponent = $state<QuizTimer>();

	// Derived state
	const isCountdownMode = $derived(quizMode === QuizModeEnum.COUNTDOWN);
	const isFixedQuestionMode = $derived(quizMode === QuizModeEnum.FIXED_QUESTION);

	// Lifecycle
	onMount(() => {
		if (lessonType && quizMode) {
			startLesson();
		}
	});

	onDestroy(() => {
		if (sessionId) {
			QuizSessionService.abandonSession(sessionId);
		}
	});

	// Methods
	function startLesson() {
		if (!lessonType || !quizMode) return;

		isLoading = true;

		// Create quiz session
		sessionId = QuizSessionService.createSession(lessonType, quizMode);

		// Set up timer for countdown mode
		if (isCountdownMode) {
			timeRemaining = LessonConfigService.getQuizTime(quizMode);
			if (timerComponent) {
				timerComponent.start();
			}
		}

		// Generate first question
		generateNewQuestion();
		updateProgress();
		hasStarted = true;

		isLoading = false;
	}

	function generateNewQuestion() {
		if (!lessonType) return;

		try {
			currentQuestion = QuestionGeneratorService.generateQuestion(lessonType);
			questionStartTime = Date.now();
			resetQuestionState();
		} catch (error) {
			console.error('Failed to generate question:', error);
		}
	}

	function resetQuestionState() {
		isAnswered = false;
		showFeedback = false;
		selectedAnswerId = null;
	}

	function handleAnswerSelected(data: {
		answerId: string;
		answerContent: PictographData;
		isCorrect: boolean;
	}) {
		if (isAnswered || !currentQuestion || !sessionId) return;

		const { answerId, isCorrect } = data;
		const timeToAnswer = Date.now() - questionStartTime;

		// Mark as answered
		isAnswered = true;
		selectedAnswerId = answerId;
		showFeedback = true;

		// Update session progress
		QuizSessionService.updateSessionProgress(sessionId, isCorrect, timeToAnswer / 1000);
		updateProgress();

		// Auto-advance after feedback delay
		setTimeout(() => {
			if (shouldContinueQuiz()) {
				handleNextQuestion();
			} else {
				completeLesson();
			}
		}, 2000);
	}

	function handleNextQuestion() {
		if (!sessionId) return;

		if (shouldContinueQuiz()) {
			generateNewQuestion();
		} else {
			completeLesson();
		}
	}

	function shouldContinueQuiz(): boolean {
		if (!sessionId) return false;

		const session = QuizSessionService.getSession(sessionId);
		if (!session || !session.isActive) return false;

		if (isFixedQuestionMode) {
			return session.questionsAnswered < session.totalQuestions;
		} else if (isCountdownMode) {
			return timeRemaining > 0;
		}

		return false;
	}

	function updateProgress() {
		if (!sessionId) return;
		progress = QuizSessionService.getLessonProgress(sessionId);
	}

	function handleTimerTick(event: CustomEvent) {
		timeRemaining = event.detail.timeRemaining;
	}

	function handleTimeUp() {
		completeLesson();
	}

	function completeLesson() {
		if (!sessionId) return;

		const results = QuizSessionService.completeSession(sessionId);
		if (results) {
			onLessonComplete?.(results);
		}
	}

	function handleBackClick() {
		if (sessionId) {
			QuizSessionService.abandonSession(sessionId);
		}
		onBackToSelector?.();
	}
	
	// Lesson control handlers
	function handlePauseClicked() {
		isPaused = true;
		if (timerComponent) {
			timerComponent.pause();
		}
	}
	
	function handleResumeClicked() {
		isPaused = false;
		if (timerComponent) {
			timerComponent.resume();
		}
	}
	
	function handleRestartClicked() {
		if (sessionId) {
			QuizSessionService.abandonSession(sessionId);
		}
		// Restart the lesson
		startLesson();
	}

	function formatLessonTitle(): string {
		if (!lessonType) return 'Unknown Lesson';
		return LessonConfigService.getFormattedLessonTitle(lessonType);
	}

	function getQuizModeDisplay(): string {
		if (!quizMode) return 'Unknown Mode';
		return LessonConfigService.getQuizModeName(quizMode);
	}
</script>

<div class="lesson-workspace">
	{#if isLoading}
		<div class="loading-screen">
			<div class="loading-spinner"></div>
			<p>Starting lesson...</p>
		</div>
	{:else}
		<!-- Header -->
		<div class="workspace-header">
			<button class="back-button" onclick={handleBackClick}> ← Back to Lessons </button>
			<div class="lesson-info">
				<h2 class="lesson-title">{formatLessonTitle()}</h2>
				<p class="quiz-mode">Mode: {getQuizModeDisplay()}</p>
			</div>
			{#if isCountdownMode && timeRemaining > 0}
			<div class="timer-container">
			<QuizTimer
			bind:this={timerComponent}
			{timeRemaining}
			totalTime={LessonConfigService.getQuizTime(
			quizMode || QuizModeEnum.FIXED_QUESTION
			)}
			isRunning={!isPaused}
			size="small"
			on:tick={handleTimerTick}
			on:timeUp={handleTimeUp}
			/>
			</div>
			{/if}
				
				<!-- Lesson Controls -->
				{#if hasStarted}
					<div class="controls-container">
						<LessonControls
							showPauseButton={isCountdownMode}
							showRestartButton={true}
							{isPaused}
							isDisabled={isLoading}
							onPauseClicked={handlePauseClicked}
							onResumeClicked={handleResumeClicked}
							onRestartClicked={handleRestartClicked}
						/>
					</div>
				{/if}
		</div>

		<!-- Progress Tracker -->
		{#if progress}
			<div class="progress-container">
				<ProgressTracker
					{progress}
					quizMode={quizMode || QuizModeEnum.FIXED_QUESTION}
					compact={true}
				/>
			</div>
		{/if}

		<!-- Main Content -->
		<div class="workspace-content">
			{#if currentQuestion && lessonType}
				<QuestionGenerator
					{lessonType}
					questionData={currentQuestion}
					{showFeedback}
					{selectedAnswerId}
					{isAnswered}
					onAnswerSelected={handleAnswerSelected}
					onNextQuestion={handleNextQuestion}
				/>
			{:else}
				<div class="no-question">
					<p>No question available</p>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.lesson-workspace {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		gap: var(--spacing-lg);
		padding: var(--spacing-lg);
	}

	.workspace-header {
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

	.quiz-mode {
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
		margin: 0;
	}

	.timer-container {
		display: flex;
		align-items: center;
	}
	
	.controls-container {
		display: flex;
		align-items: center;
		margin-left: auto;
	}

	.progress-container {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
	}

	.workspace-content {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 400px;
	}

	.no-question {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		color: #94a3b8;
		font-size: 1.125rem;
	}

	.loading-screen {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		gap: 1rem;
		color: #ffffff;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.1);
		border-left: 4px solid #667eea;
		border-radius: 50%;
		animation: spin 1s linear infinite;
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
		.lesson-workspace {
			padding: 1rem;
			gap: 1rem;
		}

		.workspace-header {
			flex-direction: column;
			align-items: flex-start;
			gap: 1rem;
		}

		.lesson-title {
			font-size: 1.25rem;
		}

		.workspace-content {
			min-height: 300px;
		}
	}

	@media (max-width: 480px) {
		.lesson-workspace {
			padding: 0.75rem;
		}

		.workspace-header {
			padding: 0.75rem 1rem;
		}

		.back-button {
			padding: 0.5rem 1rem;
			font-size: 0.75rem;
		}

		.lesson-title {
			font-size: 1.125rem;
		}

		.workspace-content {
			min-height: 250px;
		}
	}
</style>
