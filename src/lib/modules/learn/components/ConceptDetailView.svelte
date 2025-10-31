<!--
ConceptDetailView - Full view when a concept is selected

Shows three tabs:
- Learn: PDF pages, explanations, key concepts
- Practice: Quiz questions specific to this concept
- Stats: Progress, accuracy, streaks
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import type {
    LearnConcept,
    ConceptDetailView,
    ConceptProgress,
  } from "../domain";
  import { conceptProgressService } from "../services/ConceptProgressService";

  let { concept, onClose } = $props<{
    concept: LearnConcept;
    onClose?: () => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  let activeTab = $state<ConceptDetailView>("learn");
  let progress = $state<ConceptProgress>(
    conceptProgressService.getConceptProgress(concept.id)
  );

  // Start the concept when detail view opens
  onMount(() => {
    if (progress.status === "available") {
      conceptProgressService.startConcept(concept.id);
    }

    // Subscribe to progress updates
    const unsubscribe = conceptProgressService.subscribe(() => {
      progress = conceptProgressService.getConceptProgress(concept.id);
    });

    return unsubscribe;
  });

  function handleTabChange(tab: ConceptDetailView) {
    hapticService?.trigger("selection");
    activeTab = tab;
  }

  function handleClose() {
    hapticService?.trigger("selection");
    onClose?.();
  }
</script>

<div class="concept-detail">
  <!-- Header -->
  <header class="detail-header">
    <button
      class="back-button"
      onclick={handleClose}
      aria-label="Back to concept list"
    >
      <span class="back-icon">‹</span>
      <span class="back-text">Back</span>
    </button>

    <div class="header-content">
      <div class="concept-icon-large">{concept.icon}</div>
      <div class="header-info">
        <h1 class="concept-title">{concept.name}</h1>
        <p class="concept-description">{concept.description}</p>
      </div>
    </div>

    <div class="header-stats">
      {#if progress.percentComplete > 0}
        <div class="stat-pill">
          <span class="stat-label">Progress</span>
          <span class="stat-value">{Math.round(progress.percentComplete)}%</span
          >
        </div>
      {/if}
      {#if progress.accuracy > 0}
        <div class="stat-pill">
          <span class="stat-label">Accuracy</span>
          <span class="stat-value">{Math.round(progress.accuracy)}%</span>
        </div>
      {/if}
    </div>
  </header>

  <!-- Tab bar -->
  <nav class="tab-bar" role="tablist">
    <button
      class="tab"
      class:active={activeTab === "learn"}
      onclick={() => handleTabChange("learn")}
      role="tab"
      aria-selected={activeTab === "learn"}
      aria-controls="learn-panel"
    >
      <span class="tab-icon">📖</span>
      <span class="tab-label">Learn</span>
    </button>

    <button
      class="tab"
      class:active={activeTab === "practice"}
      onclick={() => handleTabChange("practice")}
      role="tab"
      aria-selected={activeTab === "practice"}
      aria-controls="practice-panel"
    >
      <span class="tab-icon">🎯</span>
      <span class="tab-label">Practice</span>
    </button>

    <button
      class="tab"
      class:active={activeTab === "stats"}
      onclick={() => handleTabChange("stats")}
      role="tab"
      aria-selected={activeTab === "stats"}
      aria-controls="stats-panel"
    >
      <span class="tab-icon">📊</span>
      <span class="tab-label">Stats</span>
    </button>
  </nav>

  <!-- Tab content -->
  <div class="tab-content">
    {#if activeTab === "learn"}
      <div class="tab-panel" role="tabpanel" id="learn-panel">
        <div class="learn-content">
          <h2 class="section-title">Key Concepts</h2>
          <ul class="concept-list">
            {#each concept.concepts as keyPoint}
              <li class="concept-item">{keyPoint}</li>
            {/each}
          </ul>

          <div class="pdf-reference">
            <h3 class="subsection-title">Reference Material</h3>
            <p class="pdf-info">
              See pages <strong>{concept.pdfPages.join(", ")}</strong> in
              <em>The Kinetic Alphabet Level 1</em>
            </p>
            <p class="hint-text">
              💡 Tip: Open the Codex panel for quick pictograph reference while
              learning!
            </p>
          </div>

          <div class="practice-prompt">
            <p>
              Ready to practice? Switch to the <strong>Practice</strong> tab to test
              your knowledge!
            </p>
          </div>
        </div>
      </div>
    {:else if activeTab === "practice"}
      <div class="tab-panel" role="tabpanel" id="practice-panel">
        <div class="practice-content">
          <div class="coming-soon">
            <span class="coming-soon-icon">🚧</span>
            <h2 class="coming-soon-title">Practice Mode Coming Soon!</h2>
            <p class="coming-soon-text">
              We're building concept-specific quizzes for targeted practice. For
              now, use the general quiz mode to practice TKA letters.
            </p>
          </div>
        </div>
      </div>
    {:else if activeTab === "stats"}
      <div class="tab-panel" role="tabpanel" id="stats-panel">
        <div class="stats-content">
          <h2 class="section-title">Your Progress</h2>

          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-card-icon">✅</span>
              <span class="stat-card-value">{progress.correctAnswers}</span>
              <span class="stat-card-label">Correct</span>
            </div>

            <div class="stat-card">
              <span class="stat-card-icon">❌</span>
              <span class="stat-card-value">{progress.incorrectAnswers}</span>
              <span class="stat-card-label">Incorrect</span>
            </div>

            <div class="stat-card">
              <span class="stat-card-icon">🎯</span>
              <span class="stat-card-value"
                >{Math.round(progress.accuracy)}%</span
              >
              <span class="stat-card-label">Accuracy</span>
            </div>

            <div class="stat-card">
              <span class="stat-card-icon">🔥</span>
              <span class="stat-card-value">{progress.currentStreak}</span>
              <span class="stat-card-label">Streak</span>
            </div>

            <div class="stat-card">
              <span class="stat-card-icon">⭐</span>
              <span class="stat-card-value">{progress.bestStreak}</span>
              <span class="stat-card-label">Best Streak</span>
            </div>

            <div class="stat-card">
              <span class="stat-card-icon">⏱️</span>
              <span class="stat-card-value"
                >{Math.round(progress.timeSpentSeconds / 60)}</span
              >
              <span class="stat-card-label">Minutes</span>
            </div>
          </div>

          {#if progress.status === "completed"}
            <div class="completion-badge">
              <span class="badge-icon">🏆</span>
              <span class="badge-text">Concept Mastered!</span>
              {#if progress.completedAt}
                <span class="badge-date">
                  Completed on {new Date(
                    progress.completedAt
                  ).toLocaleDateString()}
                </span>
              {/if}
            </div>
          {:else}
            <div class="progress-info">
              <p>
                Keep practicing to master this concept! You're {Math.round(
                  progress.percentComplete
                )}% of the way there.
              </p>
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .concept-detail {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: transparent;
  }

  /* Header */
  .detail-header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  }

  .back-button {
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    /* Minimum touch target */
    min-height: 44px;
  }

  .back-button:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .back-icon {
    font-size: 1.5rem;
    font-weight: bold;
  }

  .header-content {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .concept-icon-large {
    font-size: 4rem;
    flex-shrink: 0;
  }

  .header-info {
    flex: 1;
  }

  .concept-title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(135deg, #ffffff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .concept-description {
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }

  .header-stats {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .stat-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 999px;
  }

  .stat-label {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
  }

  .stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: white;
  }

  /* Tab bar */
  .tab-bar {
    display: flex;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .tab {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    padding: 1rem;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.2s ease;
    /* Minimum touch target */
    min-height: 44px;
  }

  .tab:hover {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
  }

  .tab.active {
    color: white;
    border-bottom-color: #4a90e2;
    background: rgba(74, 144, 226, 0.1);
  }

  .tab-icon {
    font-size: 1.5rem;
  }

  .tab-label {
    font-size: 0.875rem;
    font-weight: 600;
  }

  /* Tab content */
  .tab-content {
    flex: 1;
    overflow-y: auto;
  }

  .tab-panel {
    padding: 2rem;
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Learn content */
  .learn-content {
    max-width: 600px;
    margin: 0 auto;
  }

  .section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin: 0 0 1rem 0;
  }

  .concept-list {
    list-style: none;
    padding: 0;
    margin: 0 0 2rem 0;
  }

  .concept-item {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid #4a90e2;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.9);
  }

  .pdf-reference {
    padding: 1.5rem;
    background: rgba(74, 144, 226, 0.1);
    border: 2px solid rgba(74, 144, 226, 0.3);
    border-radius: 12px;
    margin-bottom: 1.5rem;
  }

  .subsection-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: white;
    margin: 0 0 0.75rem 0;
  }

  .pdf-info {
    color: rgba(255, 255, 255, 0.9);
    margin: 0 0 0.75rem 0;
  }

  .hint-text {
    font-size: 0.9375rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  .practice-prompt {
    padding: 1.5rem;
    background: rgba(123, 104, 238, 0.1);
    border: 2px solid rgba(123, 104, 238, 0.3);
    border-radius: 12px;
    text-align: center;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Practice/Coming soon */
  .practice-content,
  .coming-soon {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    text-align: center;
    padding: 2rem;
  }

  .coming-soon-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  .coming-soon-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin: 0 0 1rem 0;
  }

  .coming-soon-text {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.7);
    max-width: 400px;
    margin: 0;
    line-height: 1.6;
  }

  /* Stats content */
  .stats-content {
    max-width: 600px;
    margin: 0 auto;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
  }

  .stat-card-icon {
    font-size: 2rem;
  }

  .stat-card-value {
    font-size: 2rem;
    font-weight: 800;
    color: white;
  }

  .stat-card-label {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .completion-badge {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 2rem;
    background: rgba(80, 200, 120, 0.1);
    border: 2px solid rgba(80, 200, 120, 0.3);
    border-radius: 12px;
  }

  .badge-icon {
    font-size: 3rem;
  }

  .badge-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
  }

  .badge-date {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
  }

  .progress-info {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    text-align: center;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .detail-header {
      padding: 1rem;
    }

    .concept-icon-large {
      font-size: 3rem;
    }

    .concept-title {
      font-size: 1.5rem;
    }

    .concept-description {
      font-size: 1rem;
    }

    .tab-panel {
      padding: 1.5rem;
    }

    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 480px) {
    .detail-header {
      padding: 0.75rem;
    }

    .header-content {
      flex-direction: column;
      align-items: flex-start;
    }

    .concept-icon-large {
      font-size: 2.5rem;
    }

    .concept-title {
      font-size: 1.25rem;
    }

    .concept-description {
      font-size: 0.9375rem;
    }

    .tab {
      padding: 0.75rem 0.5rem;
    }

    .tab-icon {
      font-size: 1.25rem;
    }

    .tab-label {
      font-size: 0.75rem;
    }

    .tab-panel {
      padding: 1rem;
    }
  }
</style>
