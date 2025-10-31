<!--
ConceptCard - Interactive card for a single TKA concept

Displays:
- Concept icon and name
- Status indicator (locked, available, in-progress, completed)
- Progress ring for in-progress/completed concepts
- Estimated time
- Visual feedback on hover/tap
-->
<script lang="ts">
  import type { LearnConcept, ConceptProgress, ConceptStatus } from "../domain";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";

  let { concept, progress, status, onClick } = $props<{
    concept: LearnConcept;
    progress?: ConceptProgress;
    status: ConceptStatus;
    onClick?: (concept: LearnConcept) => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  const isClickable = $derived(status !== "locked");
  const percentComplete = $derived(progress?.percentComplete || 0);

  // Status display config
  const statusConfig: Record<
    ConceptStatus,
    { icon: string; label: string; color: string }
  > = {
    locked: { icon: "🔒", label: "Locked", color: "#6B7280" },
    available: { icon: "⭕", label: "Ready", color: "#4A90E2" },
    "in-progress": { icon: "▶️", label: "In Progress", color: "#7B68EE" },
    completed: { icon: "✅", label: "Mastered", color: "#50C878" },
  };

  const currentStatus = $derived(statusConfig[status]);

  function handleClick() {
    if (!isClickable) return;

    hapticService?.trigger("selection");
    onClick?.(concept);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleClick();
    }
  }
</script>

<button
  class="concept-card"
  class:locked={status === "locked"}
  class:available={status === "available"}
  class:in-progress={status === "in-progress"}
  class:completed={status === "completed"}
  class:clickable={isClickable}
  onclick={handleClick}
  onkeydown={handleKeydown}
  disabled={!isClickable}
  aria-label={`${concept.name} - ${currentStatus.label}`}
  role="button"
  tabindex={isClickable ? 0 : -1}
>
  <!-- Progress ring (for in-progress/completed) -->
  {#if status === "in-progress" || status === "completed"}
    <div class="progress-ring">
      <svg width="56" height="56" viewBox="0 0 56 56">
        <circle
          class="progress-ring-background"
          cx="28"
          cy="28"
          r="24"
          fill="none"
          stroke="rgba(255, 255, 255, 0.1)"
          stroke-width="3"
        />
        <circle
          class="progress-ring-fill"
          cx="28"
          cy="28"
          r="24"
          fill="none"
          stroke={currentStatus.color}
          stroke-width="3"
          stroke-dasharray="150.8"
          stroke-dashoffset={150.8 * (1 - percentComplete / 100)}
          stroke-linecap="round"
          transform="rotate(-90 28 28)"
        />
      </svg>
    </div>
  {/if}

  <!-- Icon -->
  <div class="concept-icon">
    {concept.icon}
  </div>

  <!-- Content -->
  <div class="concept-content">
    <div class="concept-header">
      <h3 class="concept-name">{concept.shortName}</h3>
      <span
        class="status-badge"
        style="background-color: {currentStatus.color}"
      >
        <span class="status-icon">{currentStatus.icon}</span>
      </span>
    </div>

    <p class="concept-description">{concept.description}</p>

    <div class="concept-meta">
      <span class="meta-item">
        <span class="meta-icon">⏱️</span>
        <span class="meta-text">{concept.estimatedMinutes} min</span>
      </span>
      {#if progress && progress.accuracy > 0}
        <span class="meta-item">
          <span class="meta-icon">🎯</span>
          <span class="meta-text">{Math.round(progress.accuracy)}%</span>
        </span>
      {/if}
    </div>
  </div>

  <!-- Chevron for clickable cards -->
  {#if isClickable}
    <div class="chevron">›</div>
  {/if}
</button>

<style>
  .concept-card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    text-align: left;
    /* Minimum touch target: 44px */
    min-height: 44px;
  }

  .concept-card.locked {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .concept-card.clickable:hover:not(.locked) {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .concept-card.clickable:active:not(.locked) {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  }

  /* Status-specific colors */
  .concept-card.available {
    border-color: rgba(74, 144, 226, 0.3);
  }

  .concept-card.in-progress {
    border-color: rgba(123, 104, 238, 0.3);
  }

  .concept-card.completed {
    border-color: rgba(80, 200, 120, 0.3);
    background: rgba(80, 200, 120, 0.1);
  }

  /* Progress ring */
  .progress-ring {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    width: 56px;
    height: 56px;
    pointer-events: none;
  }

  .progress-ring-fill {
    transition: stroke-dashoffset 0.6s ease;
  }

  /* Icon */
  .concept-icon {
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
  }

  /* Content */
  .concept-content {
    flex: 1;
    min-width: 0; /* Allow text truncation */
  }

  .concept-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
  }

  .concept-name {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .status-badge {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    font-size: 0.75rem;
  }

  .status-icon {
    display: inline-block;
    transform: scale(0.8);
  }

  .concept-description {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0 0 0.5rem 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .concept-meta {
    display: flex;
    gap: 1rem;
  }

  .meta-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
  }

  .meta-icon {
    font-size: 0.875rem;
  }

  .meta-text {
    font-weight: 500;
  }

  /* Chevron */
  .chevron {
    flex-shrink: 0;
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.4);
    transition: transform 0.2s ease;
  }

  .concept-card.clickable:hover:not(.locked) .chevron {
    transform: translateX(4px);
    color: rgba(255, 255, 255, 0.8);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .concept-card {
      padding: 0.875rem;
    }

    .concept-icon {
      width: 40px;
      height: 40px;
      font-size: 1.5rem;
    }

    .concept-name {
      font-size: 1rem;
    }

    .concept-description {
      font-size: 0.8125rem;
    }

    .progress-ring {
      width: 48px;
      height: 48px;
    }

    .progress-ring svg {
      width: 48px;
      height: 48px;
    }
  }

  @media (max-width: 480px) {
    .concept-card {
      padding: 0.75rem;
      gap: 0.75rem;
    }

    .concept-icon {
      width: 36px;
      height: 36px;
      font-size: 1.25rem;
    }

    .concept-name {
      font-size: 0.9375rem;
    }

    .concept-description {
      font-size: 0.75rem;
      -webkit-line-clamp: 1;
    }

    .meta-item {
      font-size: 0.6875rem;
    }

    .chevron {
      font-size: 1.25rem;
    }
  }

  /* Accessibility */
  .concept-card:focus-visible {
    outline: 2px solid #4a90e2;
    outline-offset: 2px;
  }

  .concept-card[disabled] {
    cursor: not-allowed;
  }
</style>
