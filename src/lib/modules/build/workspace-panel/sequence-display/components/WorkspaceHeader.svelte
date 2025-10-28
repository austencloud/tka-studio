<!--
  WorkspaceHeader.svelte
  
  Header component for the workspace panel containing:
  - Word label (center/left)
  - Sequence Actions button (top-right)
  
  This component provides a balanced top bar for the workspace,
  utilizing the space where the word label is displayed.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared/application/services/contracts";
  import { resolve, TYPES } from "$shared/inversify";
  import WordLabel from "./WordLabel.svelte";

  let {
    word = "",
    onSequenceActionsClick,
    isMultiSelectMode = false
  } = $props<{
    word?: string;
    onSequenceActionsClick?: () => void;
    isMultiSelectMode?: boolean;
  }>();

  // Resolve haptic feedback service
  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleSequenceActionsClick() {
    hapticService?.trigger("selection");
    onSequenceActionsClick?.();
  }
</script>

{#if !isMultiSelectMode}
  <div class="workspace-header">
    <!-- Word Label (center/left) -->
    <div class="word-label-wrapper">
      <WordLabel {word} />
    </div>

    <!-- Sequence Actions Button (top-right) -->
    <button
      class="sequence-actions-button glass-button"
      onclick={handleSequenceActionsClick}
      aria-label="Sequence actions"
      title="Sequence actions"
    >
      <i class="fas fa-tools"></i>
    </button>
  </div>
{/if}

<style>
  .workspace-header {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 48px;
    z-index: 10;
    pointer-events: none; /* Allow clicks to pass through to word label */
  }

  .word-label-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    pointer-events: auto;
  }

  .sequence-actions-button {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    pointer-events: auto;
    z-index: 20;
  }

  .sequence-actions-button:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .sequence-actions-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .sequence-actions-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  .sequence-actions-button i {
    font-size: 18px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .sequence-actions-button {
      width: 44px;
      height: 44px;
      font-size: 16px;
    }
  }

  @media (max-width: 480px) {
    .sequence-actions-button {
      width: 40px;
      height: 40px;
      font-size: 14px;
    }

    .sequence-actions-button i {
      font-size: 16px;
    }
  }

  @media (max-width: 320px) {
    .sequence-actions-button {
      width: 36px;
      height: 36px;
      font-size: 12px;
    }

    .sequence-actions-button i {
      font-size: 14px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Compact buttons for Z Fold 5 horizontal (882x344) */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .workspace-header {
      min-height: 36px;
    }

    .sequence-actions-button {
      width: 36px;
      height: 36px;
      font-size: 14px;
    }

    .sequence-actions-button i {
      font-size: 14px;
    }
  }
</style>

