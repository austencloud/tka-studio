<!--
SequenceTransformTools.svelte - Sequence Transformation Tools for Edit Tab

Handles sequence-level transformations like mirror, rotate, and swap colors.
Pure presentation component that delegates to sequence transform services.
Moved from workbench to edit tab as these are editing functions.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { Snippet } from "svelte";
  import { onMount } from "svelte";

  let {
    disabled = false,
    hasSequence = false,
    onMirror,
    onSwapColors,
    onRotate,
    renderExtra,
  } = $props<{
    disabled?: boolean;
    hasSequence?: boolean;
    onMirror?: () => void;
    onSwapColors?: () => void;
    onRotate?: () => void;
    renderExtra?: Snippet;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handle(fn?: () => void) {
    if (disabled || !hasSequence) return;
    hapticService?.trigger("selection");
    fn?.();
  }
</script>

<div class="sequence-transform-tools">
  <div class="tools-header">
    <h4>Sequence Transforms</h4>
    <span class="tools-description"
      >Apply transformations to the entire sequence</span
    >
  </div>

  <div class="tools-grid">
    <button
      type="button"
      class="transform-btn"
      title="Mirror Sequence"
      disabled={!hasSequence || disabled}
      onclick={() => handle(onMirror)}
    >
      <span class="btn-icon">🪞</span>
      <span class="btn-label">Mirror</span>
    </button>

    <button
      type="button"
      class="transform-btn"
      title="Swap Colors"
      disabled={!hasSequence || disabled}
      onclick={() => handle(onSwapColors)}
    >
      <span class="btn-icon">🎨</span>
      <span class="btn-label">Swap Colors</span>
    </button>

    <button
      type="button"
      class="transform-btn"
      title="Rotate Sequence"
      disabled={!hasSequence || disabled}
      onclick={() => handle(onRotate)}
    >
      <span class="btn-icon">🔄</span>
      <span class="btn-label">Rotate</span>
    </button>
  </div>

  {#if renderExtra}
    {@render renderExtra()}
  {/if}
</div>

<style>
  .sequence-transform-tools {
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius);
    padding: var(--spacing-md);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .tools-header {
    margin-bottom: var(--spacing-md);
  }

  .tools-header h4 {
    margin: 0 0 var(--spacing-xs) 0;
    color: var(--foreground);
    font-size: var(--font-size-md);
    font-weight: 600;
  }

  .tools-description {
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: var(--spacing-sm);
  }

  .transform-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    cursor: pointer;
    transition: all var(--transition-normal);
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
    min-height: 80px;

    /* Subtle inner shadow for depth */
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.1),
      0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .btn-icon {
    font-size: 24px;
    line-height: 1;
  }

  .btn-label {
    font-size: var(--font-size-sm);
    text-align: center;
    line-height: 1.2;
  }

  .transform-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.15),
      0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .transform-btn:active:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(0);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.2),
      0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .transform-btn:disabled {
    background: rgba(200, 200, 200, 0.05);
    border-color: rgba(200, 200, 200, 0.1);
    color: rgba(255, 255, 255, 0.3);
    cursor: not-allowed;
    transform: none;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }

  .transform-btn:disabled .btn-icon,
  .transform-btn:disabled .btn-label {
    opacity: 0.5;
  }

  /* Focus styles for accessibility */
  .transform-btn:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .tools-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: var(--spacing-xs);
    }

    .transform-btn {
      padding: var(--spacing-sm);
      min-height: 70px;
    }

    .btn-icon {
      font-size: 20px;
    }

    .btn-label {
      font-size: var(--font-size-xs);
    }
  }

  /* Ultra-narrow mobile optimization */
  @media (max-width: 480px) {
    .sequence-transform-tools {
      padding: var(--spacing-sm);
    }

    .tools-grid {
      gap: 4px;
    }

    .transform-btn {
      padding: var(--spacing-xs);
      min-height: 60px;
    }

    .btn-icon {
      font-size: 18px;
    }
  }

  /* Z Fold 6 cover screen optimization */
  @media (max-width: 320px) {
    .tools-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 2px;
    }

    .transform-btn {
      padding: 6px;
      min-height: 50px;
      border-radius: 6px;
    }

    .btn-icon {
      font-size: 16px;
    }

    .btn-label {
      font-size: 10px;
    }
  }
</style>
