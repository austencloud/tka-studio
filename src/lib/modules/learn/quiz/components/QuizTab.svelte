<!--
Quiz Tab - Interactive quiz system

Provides quiz functionality for learning TKA notation:
- Quiz selection and progress tracking
- Interactive quizzes with pictograph recognition
- Progress tracking and results
- Codex integration for reference
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from "svelte";
  import { ProgressTracker } from ".";
  import type { ICodexService } from "../../codex/services/contracts";
  import type { QuizProgress } from "../domain";
  import { QuizMode, QuizType } from "../domain";
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
  let hapticService: IHapticFeedbackService;

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

  async function handleQuizSelect(data: {
    lessonType: QuizType;
    quizMode: QuizMode;
  }) {
    // Trigger selection haptic for quiz selection
    hapticService?.trigger("selection");

    try {
      isLoading = true;
      // Convert the lesson type to a lesson ID
      const lessonId = `${data.lessonType}_${data.quizMode}`;
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
      console.log("✅ QuizTab: Quiz selected:", lessonId);
    } catch (err) {
      console.error("❌ QuizTab: Failed to start lesson:", err);
      error = err instanceof Error ? err.message : "Failed to start lesson";
    } finally {
      isLoading = false;
    }
  }

  async function handleAnswerSubmit(answer: any) {
    try {
      console.log("✅ QuizTab: Answer submitted:", answer);
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
      console.error("❌ QuizTab: Failed to submit answer:", err);
      error = err instanceof Error ? err.message : "Failed to submit answer";
    }
  }

  async function handleQuizComplete() {
    try {
      await quizSessionService.completeQuiz();
      currentView = "results";
      console.log("✅ QuizTab: Quiz completed");
    } catch (err) {
      console.error("❌ QuizTab: Failed to complete lesson:", err);
      error = err instanceof Error ? err.message : "Failed to complete lesson";
    }
  }

  function handleReturnToSelector() {
    // Trigger navigation haptic for returning to selector
    hapticService?.trigger("navigation");

    currentView = "selector";
    selectedQuizId = null;
    currentQuestionIndex = 0;
    score = 0;
    error = null;
    console.log("✅ QuizTab: Returned to selector");
  }

  async function handleRestartQuiz() {
    // Trigger navigation haptic for restart
    hapticService?.trigger("navigation");

    try {
      isLoading = true;
      await quizSessionService.restartQuiz();
      currentView = "workspace";
      currentQuestionIndex = 0;
      score = 0;
      error = null;
      console.log("✅ QuizTab: Quiz restarted");
    } catch (err) {
      console.error("❌ QuizTab: Failed to restart lesson:", err);
      error = err instanceof Error ? err.message : "Failed to restart lesson";
    } finally {
      isLoading = false;
    }
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(async () => {
    console.log("✅ QuizTab: Mounted");

    // Initialize haptic service
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    try {
      isLoading = true;

      // Initialize lesson repository
      await lessonRepo.initialize();

      // Load available lessons
      const lessons = lessonRepo.getAllQuizTypes();

      console.log(
        "✅ QuizTab: Initialization complete, loaded",
        lessons.length,
        "lessons"
      );
    } catch (err) {
      console.error("❌ QuizTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize quiz tab";
    } finally {
      isLoading = false;
    }
  });

  onDestroy(() => {
    console.log("✅ QuizTab: Cleanup");
    quizSessionService?.cleanup();
  });
</script>

li
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
          results={{
            sessionId: selectedQuizId || "",
            lessonType: QuizType.PICTOGRAPH_TO_LETTER,
            quizMode: QuizMode.FIXED_QUESTION,
            totalQuestions,
            correctAnswers: score,
            incorrectGuesses: totalQuestions - score,
            questionsAnswered: totalQuestions,
            accuracyPercentage:
              totalQuestions > 0 ? (score / totalQuestions) * 100 : 0,
            completionTimeSeconds: 0,
            completedAt: new Date(),
          }}
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
    background: transparent;
    color: var(--foreground, #ffffff);
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
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: transparent;
    display: flex;
    justify-content: center;
  }

  .content-area {
    flex: 1;
    overflow: auto;
    padding: 2rem;
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 0;
  }

  .controls-section {
    padding: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: transparent;
    display: flex;
    justify-content: center;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    z-index: 1000;
    color: var(--foreground, #ffffff);
  }

  .loading-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top: 2px solid var(--foreground, #ffffff);
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
