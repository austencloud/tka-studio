<!--
  ExportProgressIndicator.svelte

  Minimized progress indicator for background export.
  Shows in bottom-right corner while export is in progress.
-->
<script lang="ts">
  import type { GifExportProgress } from "$create/animate/services/contracts";

  let {
    show = false,
    progress = null,
    onExpand = () => {},
    onCancel = () => {},
  }: {
    show?: boolean;
    progress?: GifExportProgress | null;
    onExpand?: () => void;
    onCancel?: () => void;
  } = $props();

  const stageLabels: Record<string, string> = {
    capturing: "Capturing",
    encoding: "Encoding",
    transcoding: "Optimizing",
    complete: "Complete",
    error: "Error",
  };

  const progressPercent = $derived(
    progress ? Math.round(progress.progress * 100) : 0
  );

  const stageLabel = $derived(
    progress?.stage ? stageLabels[progress.stage] || "Processing" : "Processing"
  );
</script>

{#if show && progress && progress.stage !== "complete"}
  <div class="progress-indicator" class:error={progress.stage === "error"}>
    <button
      class="indicator-content"
      onclick={onExpand}
      aria-label="Expand export progress"
    >
      <div class="indicator-icon">
        {#if progress.stage === "capturing"}
          <i class="fas fa-camera"></i>
        {:else if progress.stage === "encoding" || progress.stage === "transcoding"}
          <i class="fas fa-cog fa-spin"></i>
        {/if}
      </div>
      <div class="indicator-text">
        <div class="indicator-label">{stageLabel}</div>
        <div class="indicator-progress">{progressPercent}%</div>
      </div>
      <div class="progress-ring">
        <svg width="40" height="40" viewBox="0 0 40 40">
          <circle
            class="progress-ring-bg"
            cx="20"
            cy="20"
            r="16"
            fill="none"
            stroke-width="3"
          />
          <circle
            class="progress-ring-fill"
            cx="20"
            cy="20"
            r="16"
            fill="none"
            stroke-width="3"
            stroke-dasharray="100.53"
            stroke-dashoffset={100.53 - (progressPercent / 100) * 100.53}
            transform="rotate(-90 20 20)"
          />
        </svg>
      </div>
    </button>
    <button
      class="cancel-button"
      onclick={onCancel}
      aria-label="Cancel export"
      title="Cancel export"
    >
      <i class="fas fa-times"></i>
    </button>
  </div>
{/if}

<style>
  .progress-indicator {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(
      135deg,
      rgba(30, 30, 40, 0.98),
      rgba(20, 20, 30, 0.98)
    );
    backdrop-filter: blur(20px);
    border-radius: 50px;
    padding: 8px 12px 8px 8px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.5),
      0 0 0 1px rgba(255, 255, 255, 0.1);
    animation: slide-in 0.3s cubic-bezier(0.32, 0.72, 0, 1);
  }

  @keyframes slide-in {
    from {
      transform: translateY(100px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  .indicator-content {
    display: flex;
    align-items: center;
    gap: 12px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    color: inherit;
    transition: transform 0.2s ease;
  }

  .indicator-content:hover {
    transform: scale(1.02);
  }

  .indicator-content:active {
    transform: scale(0.98);
  }

  .indicator-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: rgba(59, 130, 246, 0.9);
    flex-shrink: 0;
  }

  .indicator-text {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
    min-width: 80px;
  }

  .indicator-label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
  }

  .indicator-progress {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }

  .progress-ring {
    position: relative;
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }

  .progress-ring-bg {
    stroke: rgba(255, 255, 255, 0.1);
  }

  .progress-ring-fill {
    stroke: rgba(59, 130, 246, 0.9);
    stroke-linecap: round;
    transition: stroke-dashoffset 0.3s ease;
  }

  .cancel-button {
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
  }

  .cancel-button:hover {
    background: rgba(239, 68, 68, 0.2);
    color: rgba(239, 68, 68, 0.9);
    transform: scale(1.1);
  }

  .cancel-button:active {
    transform: scale(0.95);
  }

  /* Mobile adjustments */
  @media (max-width: 480px) {
    .progress-indicator {
      bottom: 16px;
      right: 16px;
    }

    .indicator-text {
      min-width: 70px;
    }

    .indicator-label {
      font-size: 12px;
    }

    .indicator-progress {
      font-size: 11px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .progress-indicator {
      animation: none;
    }

    .indicator-content,
    .cancel-button,
    .progress-ring-fill {
      transition: none;
    }

    .indicator-content:hover,
    .cancel-button:hover {
      transform: none;
    }
  }
</style>
