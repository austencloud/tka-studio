<!--
Learn Tab - Interactive learning and quiz system

Provides educational content and quizzes for learning TKA notation:
- Lesson selection and progress tracking
- Interactive quizzes with pictograph recognition
- Progress tracking and results
- Codex integration for reference
-->
<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  // TEMPORARY: All service resolution commented out until container is restored
  // import type {
  //   ICodexService,
  //   IQuizRepoManager,
  //   IQuizSessionService,
  // } from "$services";

  // Import learn components

  // ============================================================================
  // SERVICE RESOLUTION - TEMPORARY DISABLED
  // ============================================================================

  // TEMPORARY: All service resolution commented out until container is restored
  // const codexService = resolve(TYPES.ICodexService) as ICodexService;
  // const lessonRepository = resolve(TYPES.IQuizRepoManager) as IQuizRepoManager;
  // const quizSessionService = resolve(TYPES.IQuizSessionService) as IQuizSessionService;

  // ============================================================================
  // COMPONENT STATE - TEMPORARY PLACEHOLDERS
  // ============================================================================

  let currentView = $state<"selector" | "workspace" | "results">("selector");
  let selectedLessonId = $state<string | null>(null);
  let currentQuestionIndex = $state(0);
  let totalQuestions = $state(10);
  let score = $state(0);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  // ============================================================================
  // EVENT HANDLERS - TEMPORARY DISABLED
  // ============================================================================

  function handleLessonSelect(lessonId: string) {
    selectedLessonId = lessonId;
    currentView = "workspace";
    console.log("✅ LearnTab: Lesson selected (services disabled):", lessonId);
    // quizSessionService.startLesson(lessonId);
  }

  function handleAnswerSubmit(answer: any) {
    console.log("✅ LearnTab: Answer submitted (services disabled):", answer);
    // const isCorrect = quizSessionService.submitAnswer(answer);
    // if (isCorrect) score++;

    if (currentQuestionIndex < totalQuestions - 1) {
      currentQuestionIndex++;
    } else {
      currentView = "results";
    }
  }

  function handleLessonComplete() {
    currentView = "results";
    console.log("✅ LearnTab: Lesson completed (services disabled)");
    // quizSessionService.completeLesson();
  }

  function handleReturnToSelector() {
    currentView = "selector";
    selectedLessonId = null;
    currentQuestionIndex = 0;
    score = 0;
    console.log("✅ LearnTab: Returned to selector (services disabled)");
  }

  function handleRestartLesson() {
    currentView = "workspace";
    currentQuestionIndex = 0;
    score = 0;
    console.log("✅ LearnTab: Lesson restarted (services disabled)");
    // quizSessionService.restartLesson();
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
    console.log("✅ LearnTab: Mounted (services temporarily disabled)");

    // TEMPORARY: All initialization commented out
    try {
      // Initialize codex service
      // await codexService.initialize();

      // Load available lessons
      // const lessons = await lessonRepository.getAllLessons();

      console.log("✅ LearnTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ LearnTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize learn tab";
    }
  });

  onDestroy(() => {
    console.log("✅ LearnTab: Cleanup (services disabled)");
    // quizSessionService?.cleanup();
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
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>🎓 Learn Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Interactive lessons and quizzes</li>
          <li>✅ Pictograph recognition training</li>
          <li>✅ Progress tracking and scoring</li>
          <li>✅ Codex integration for reference</li>
          <li>✅ Multiple lesson types and difficulties</li>
          <li>✅ Results analysis and improvement suggestions</li>
        </ul>
      </div>

      <!-- Placeholder interface -->
      <div class="placeholder-interface">
        <h3>Learning Interface (placeholder):</h3>
        <div class="view-selector">
          <button
            onclick={() => (currentView = "selector")}
            class:active={currentView === "selector"}
          >
            Lesson Selector
          </button>
          <button
            onclick={() => (currentView = "workspace")}
            class:active={currentView === "workspace"}
          >
            Quiz Workspace
          </button>
          <button
            onclick={() => (currentView = "results")}
            class:active={currentView === "results"}
          >
            Results
          </button>
        </div>

        <div class="current-view">
          <strong>Current View:</strong>
          {currentView}
        </div>

        {#if currentView === "workspace"}
          <div class="quiz-info">
            <span>Question: {currentQuestionIndex + 1} / {totalQuestions}</span>
            <span>Score: {score}</span>
          </div>
        {/if}
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
    <!-- Progress Tracker -->
    <!-- <div class="progress-section">
      <ProgressTracker
        currentQuestion={currentQuestionIndex}
        totalQuestions={totalQuestions}
        score={score}
      />
    </div> -->

    <!-- Main Content Area -->
    <!-- <div class="content-area">
      {#if currentView === 'selector'}
        <LessonSelectorView
          onLessonSelect={handleLessonSelect}
        />
      {:else if currentView === 'workspace'}
        <LessonWorkspaceView
          lessonId={selectedLessonId}
          questionIndex={currentQuestionIndex}
          onAnswerSubmit={handleAnswerSubmit}
          onLessonComplete={handleLessonComplete}
        />
      {:else if currentView === 'results'}
        <LessonResultsView
          score={score}
          totalQuestions={totalQuestions}
          onReturnToSelector={handleReturnToSelector}
          onRestartLesson={handleRestartLesson}
        />
      {/if}
    </div> -->

    <!-- Controls -->
    <!-- <div class="controls-section">
      <LessonControls
        currentView={currentView}
        onReturnToSelector={handleReturnToSelector}
      />
    </div> -->
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
    justify-content: center;
    align-items: center;
    /* Original layout: */
    /* flex-direction: column;
    overflow: hidden; */
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

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  .placeholder-interface {
    margin-top: 1.5rem;
    padding: 1rem;
    background: var(--color-surface, #fff);
    border-radius: 4px;
    border: 1px solid var(--color-border, #ddd);
  }

  .placeholder-interface h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .view-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    justify-content: center;
  }

  .view-selector button {
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-border, #ddd);
    background: var(--color-surface, #fff);
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .view-selector button.active {
    background: var(--color-primary, #007acc);
    color: white;
    border-color: var(--color-primary, #007acc);
  }

  .view-selector button:hover:not(.active) {
    background: var(--color-surface-hover, #f0f0f0);
  }

  .current-view {
    color: var(--color-text-secondary, #666);
    margin-bottom: 1rem;
  }

  .quiz-info {
    display: flex;
    gap: 1rem;
    justify-content: center;
    color: var(--color-text-secondary, #666);
    font-size: 0.9rem;
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
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }

    .view-selector {
      flex-direction: column;
      align-items: center;
    }

    .quiz-info {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
</style>
