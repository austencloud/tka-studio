<!--
ProgressHeader - Overall learning progress display

Shows:
- Overall completion percentage
- Motivational message
- Visual progress bar
- Quick stats
-->
<script lang="ts">
  import type { LearningProgress } from "../domain";

  let { progress, compact = false } = $props<{
    progress: LearningProgress;
    compact?: boolean;
  }>();

  // Calculate derived stats
  const completedCount = $derived(progress.completedConcepts.size);
  const totalConcepts = 28;
  const progressPercent = $derived(Math.round(progress.overallProgress));

  // Motivational messages based on progress
  const getMessage = (percent: number): string => {
    if (percent === 0) return "Begin your journey!";
    if (percent < 10) return "Taking your first steps...";
    if (percent < 25) return "Building foundations!";
    if (percent < 50) return "Making great progress!";
    if (percent < 75) return "Over halfway there!";
    if (percent < 90) return "Almost a master!";
    if (percent < 100) return "So close to mastery!";
    return "TKA Master! 🎉";
  };

  const message = $derived(getMessage(progressPercent));
</script>

<div class="progress-header" class:compact>
  <!-- Progress bar -->
  <div class="progress-bar-container">
    <div
      class="progress-bar-fill"
      style="width: {progressPercent}%"
      role="progressbar"
      aria-valuenow={progressPercent}
      aria-valuemin="0"
      aria-valuemax="100"
    >
      <div class="progress-shimmer"></div>
    </div>
  </div>

  <!-- Stats and message -->
  <div class="progress-info">
    <div class="progress-text">
      <span class="progress-percentage">{progressPercent}%</span>
      <span class="progress-message">{message}</span>
    </div>

    {#if !compact}
      <div class="progress-stats">
        <div class="stat">
          <span class="stat-value">{completedCount}/{totalConcepts}</span>
          <span class="stat-label">Concepts</span>
        </div>
        {#if progress.totalCorrect > 0}
          <div class="stat">
            <span class="stat-value">{progress.totalCorrect}</span>
            <span class="stat-label">Correct</span>
          </div>
        {/if}
        {#if progress.badges.length > 0}
          <div class="stat">
            <span class="stat-value">{progress.badges.length}</span>
            <span class="stat-label">Badges</span>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .progress-header {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    backdrop-filter: blur(10px);
  }

  .progress-header.compact {
    padding: 1rem;
  }

  /* Progress bar */
  .progress-bar-container {
    position: relative;
    width: 100%;
    height: 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 1rem;
  }

  .progress-bar-fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background: linear-gradient(90deg, #4a90e2, #7b68ee, #50c878);
    border-radius: 999px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
  }

  /* Animated shimmer effect */
  .progress-shimmer {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
    animation: shimmer 2s infinite;
  }

  @keyframes shimmer {
    0% {
      left: -100%;
    }
    100% {
      left: 100%;
    }
  }

  /* Info section */
  .progress-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .progress-text {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .progress-percentage {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .progress-message {
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
  }

  .progress-stats {
    display: flex;
    gap: 2rem;
  }

  .stat {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
  }

  .stat-label {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .progress-header {
      padding: 1rem;
    }

    .progress-text {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .progress-percentage {
      font-size: 1.75rem;
    }

    .progress-message {
      font-size: 1rem;
    }

    .progress-stats {
      gap: 1.5rem;
    }

    .stat-value {
      font-size: 1.125rem;
    }

    .stat-label {
      font-size: 0.75rem;
    }
  }

  @media (max-width: 480px) {
    .progress-header {
      padding: 0.75rem;
    }

    .progress-bar-container {
      height: 8px;
      margin-bottom: 0.75rem;
    }

    .progress-percentage {
      font-size: 1.5rem;
    }

    .progress-message {
      font-size: 0.9375rem;
    }

    .progress-stats {
      gap: 1rem;
    }

    .stat-value {
      font-size: 1rem;
    }

    .stat-label {
      font-size: 0.6875rem;
    }
  }
</style>
