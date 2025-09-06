<!--
Learn Tab - Interactive learning and quiz system

Provides educational content and quizzes for learning TKA notation:
- Quiz selection and progress tracking
- Interactive quizzes with pictograph recognition
- Progress tracking and results
- Codex integration for reference
-->
<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { ProgressTracker } from ".";
  import { resolve, TYPES } from "../../../../shared/inversify";
  import type { ICodexService } from "../../codex/services/contracts";
  import type { QuizProgress } from "../domain";
  import { QuizMode } from "../domain";
  import type {
    IQuizRepoManager,
    IQuizSessionService,
  } from "../services/contracts";
  import QuizControls from "./QuizControls.svelte";
  import QuizResultsView from "./QuizResultsView.svelte";
  import QuizSelectorView from "./QuizSelectorView.svelte";
  import QuizWorkspaceView from "./QuizWorkspaceView.svelte";

  // Import learn components

  // ============================================================================
  // SERVICE RESOLUTION
  // ============================================================================

  const codexService = resolve(TYPES.ICodexService) as ICodexService;
  const lessonRepo = resolve(TYPES.IQuizRepoManager) as IQuizRepoManager;
  const quizSessionService = resolve(
    TYPES.IQuizSessionService
  ) as IQuizSessionService;

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  let currentView = $state<"selector" | "workspace" | "results">("selector");
  let selectedQuizId = $state<string | null>(null);
  let currentQuestionIndex = $state(0);
  let totalQuestions = $state(10);
  let score = $state(0);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  // Progress tracking state
  let progress = $state<QuizProgress>({
    currentQuestion: 1,
    totalQuestions: 10,
    correctAnswers: 0,
    incorrectAnswers: 0,
    questionsAnswered: 0,
    timeElapsed: 0,
    streakCurrent: 0,
    streakLongest: 0,
  });

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  async function handleQuizSelect(lessonId: string) {
    try {
      isLoading = true;
      selectedQuizId = lessonId;
      await quizSessionService.startQuiz(lessonId);
      const sessionData = quizSessionService.getCurrentSession();
      totalQuestions = sessionData?.totalQuestions || 10;
      currentQuestionIndex = 0;
      score = 0;

      // Reset progress
      progress.currentQuestion = 1;
      progress.totalQuestions = totalQuestions;
      progress.correctAnswers = 0;
      progress.incorrectAnswers = 0;
      progress.questionsAnswered = 0;
      progress.timeElapsed = 0;
      progress.streakCurrent = 0;
      progress.streakLongest = 0;

      currentView = "workspace";
      console.log("✅ LearnTab: Quiz selected:", lessonId);
    } catch (err) {
      console.error("❌ LearnTab: Failed to start lesson:", err);
      error = err instanceof Error ? err.message : "Failed to start lesson";
    } finally {
      isLoading = false;
    }
  }

  async function handleAnswerSubmit(answer: any) {
    try {
      console.log("✅ LearnTab: Answer submitted:", answer);
      const isCorrect = await quizSessionService.submitAnswer(answer);
      if (isCorrect) score++;

      // Update progress
      progress.questionsAnswered++;
      progress.correctAnswers = score;
      progress.incorrectAnswers = progress.questionsAnswered - score;
      progress.currentQuestion = currentQuestionIndex + 1;

      if (currentQuestionIndex < totalQuestions - 1) {
        currentQuestionIndex++;
      } else {
        currentView = "results";
      }
    } catch (err) {
      console.error("❌ LearnTab: Failed to submit answer:", err);
      error = err instanceof Error ? err.message : "Failed to submit answer";
    }
  }

  async function handleQuizComplete() {
    try {
      await quizSessionService.completeQuiz();
      currentView = "results";
      console.log("✅ LearnTab: Quiz completed");
    } catch (err) {
      console.error("❌ LearnTab: Failed to complete lesson:", err);
      error = err instanceof Error ? err.message : "Failed to complete lesson";
    }
  }

  function handleReturnToSelector() {
    currentView = "selector";
    selectedQuizId = null;
    currentQuestionIndex = 0;
    score = 0;
    error = null;
    console.log("✅ LearnTab: Returned to selector");
  }

  async function handleRestartQuiz() {
    try {
      isLoading = true;
      await quizSessionService.restartQuiz();
      currentView = "workspace";
      currentQuestionIndex = 0;
      score = 0;
      error = null;
      console.log("✅ LearnTab: Quiz restarted");
    } catch (err) {
      console.error("❌ LearnTab: Failed to restart lesson:", err);
      error = err instanceof Error ? err.message : "Failed to restart lesson";
    } finally {
      isLoading = false;
    }
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(async () => {
    console.log("✅ LearnTab: Mounted");

    try {
      isLoading = true;

      // Initialize lesson repository
      await lessonRepo.initialize();

      // Load available lessons
      const lessons = lessonRepo.getAllQuizTypes();

      console.log(
        "✅ LearnTab: Initialization complete, loaded",
        lessons.length,
        "lessons"
      );
    } catch (err) {
      console.error("❌ LearnTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize learn tab";
    } finally {
      isLoading = false;
    }
  });

  onDestroy(() => {
    console.log("✅ LearnTab: Cleanup");
    quizSessionService?.cleanup();
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="learn-tab" data-testid="learn-tab">
  <!-- Error display -->
  {#if error}
    <div class="error-banner">
      <span>{error}</span>
      <button onclick={() => (error = null)}>×</button>
    </div>
  {/if}

  <div class="learn-layout">
    <!-- Progress Tracker -->
    <div class="progress-section">
      <ProgressTracker
        {progress}
        quizMode={QuizMode.FIXED_QUESTION}
        compact={true}
      />
    </div>

    <!-- Main Content Area -->
    <div class="content-area">
      {#if currentView === "selector"}
        <QuizSelectorView onQuizSelect={handleQuizSelect} />
      {:else if currentView === "workspace"}
        <QuizWorkspaceView
          lessonId={selectedQuizId}
          questionIndex={currentQuestionIndex}
          onAnswerSubmit={handleAnswerSubmit}
          onQuizComplete={handleQuizComplete}
        />
      {:else if currentView === "results"}
        <QuizResultsView
          {score}
          {totalQuestions}
          onReturnToSelector={handleReturnToSelector}
          onRestartQuiz={handleRestartQuiz}
        />
      {/if}
    </div>

    <!-- Controls -->
    <div class="controls-section">
      <QuizControls {currentView} onReturnToSelector={handleReturnToSelector} />
    </div>
  </div>

  <!-- Loading overlay -->
  {#if isLoading}
    <div class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>Loading lesson...</span>
    </div>
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .learn-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .learn-layout {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .error-banner {
    background: var(--color-error, #ff4444);
    color: white;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .error-banner button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
  }

  .progress-section {
    padding: 1rem;
    border-bottom: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
  }

  .content-area {
    flex: 1;
    overflow: auto;
    padding: 1rem;
    background: var(--color-surface-secondary, #f8f9fa);
  }

  .controls-section {
    padding: 1rem;
    border-top: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    z-index: 1000;
  }

  .loading-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid var(--color-border, #ddd);
    border-top: 2px solid var(--color-primary, #007acc);
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
    .progress-section,
    .content-area,
    .controls-section {
      padding: 0.75rem;
    }
  }

  @media (max-width: 480px) {
    .progress-section,
    .content-area,
    .controls-section {
      padding: 0.5rem;
    }
  }
</style>
