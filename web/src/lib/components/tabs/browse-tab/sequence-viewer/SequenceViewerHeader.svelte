<!-- SequenceViewerHeader.svelte - Header with title, back button, and difficulty -->
<script lang="ts">
  import type { SequenceData } from "$domain";

  interface Props {
    sequence?: SequenceData & {
      difficulty?: number;
      word?: string;
    };
    onBackToBrowser?: () => void;
  }

  let { sequence, onBackToBrowser }: Props = $props();

  // Handle navigation back to browser
  function handleBackToBrowser() {
    onBackToBrowser?.();
  }

  function getDifficultyColor(difficulty: number) {
    const colors: Record<number, string> = {
      1: "#10b981", // green
      2: "#f59e0b", // yellow
      3: "#ef4444", // red
      4: "#8b5cf6", // purple
    };
    return colors[difficulty] || "#6366f1";
  }

  function getDifficultyLabel(difficulty: number) {
    const labels: Record<number, string> = {
      1: "Beginner",
      2: "Intermediate",
      3: "Advanced",
      4: "Expert",
    };
    return labels[difficulty] || "Unknown";
  }
</script>

<div class="viewer-header">
  <button class="back-button" onclick={handleBackToBrowser} type="button">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
      <path
        d="M12.5 15L7.5 10L12.5 5"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
    Back
  </button>

  <div class="sequence-header-info">
    <h2 class="sequence-title">{sequence?.word || "Untitled Sequence"}</h2>
    <div
      class="difficulty-badge"
      style="--difficulty-color: {getDifficultyColor(
        sequence?.difficulty || 1
      )}"
    >
      {getDifficultyLabel(sequence?.difficulty || 1)}
    </div>
  </div>
</div>

<style>
  .viewer-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding-bottom: var(--spacing-md);
    border-bottom: var(--glass-border);
  }

  .back-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm);
    background: rgba(255, 255, 255, 0.1);
    border: var(--glass-border);
    border-radius: 8px;
    color: var(--foreground);
    font-family: inherit;
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
    flex-shrink: 0;
  }

  .back-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--primary-color);
    color: var(--primary-color);
  }

  .sequence-header-info {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    flex: 1;
    min-width: 0;
  }

  .sequence-title {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--foreground);
    margin: 0;
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .difficulty-badge {
    --difficulty-color: var(--primary-color);

    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--difficulty-color);
    color: white;
    border-radius: 12px;
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .sequence-header-info {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-sm);
    }

    .sequence-title {
      font-size: var(--font-size-lg);
    }
  }
</style>
