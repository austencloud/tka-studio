<!--
  WorkspaceHeader.svelte

  Header component for the workspace panel containing:
  - Word label (center/left)
  - Settings button (top-right)

  This component provides a balanced top bar for the workspace,
  utilizing the space where the word label is displayed.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared/application/services/contracts";
  import type { SequenceData } from "$shared/foundation/domain/models/SequenceData";
  import { showSettingsDialog } from "$shared/application/state/app-state.svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import WordLabel from "./WordLabel.svelte";

  let {
    word = "",
    isMultiSelectMode = false,
    sequence = null
  } = $props<{
    word?: string;
    isMultiSelectMode?: boolean;
    sequence?: SequenceData | null;
  }>();

  // Resolve services
  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleSettingsClick() {
    hapticService?.trigger("selection");
    showSettingsDialog();
  }
</script>

{#if !isMultiSelectMode}
  <div class="workspace-header">
    <div class="header-content">
      <!-- Word Label (center/left) -->
      <div class="word-label-wrapper">
        <WordLabel {word} {sequence} />
      </div>
    </div>


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

  .header-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: auto;
  }

  .word-label-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .settings-button {
    position: absolute;
    top: 6px;
    right: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Desktop: 40px, Mobile: 44px minimum for touch targets */
    width: 40px;
    height: 40px;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--glass-backdrop-strong);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    pointer-events: auto;
    z-index: 20;
  }

  .settings-button:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
  }

  .settings-button:active {
    transform: scale(0.95);
  }

  .settings-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  .settings-button i {
    font-size: 20px;
  }

  /* Mobile responsive - 44px minimum for accessibility */
  @media (max-width: 768px) {
    .settings-button {
      width: 44px;
      height: 44px;
    }

    .settings-button i {
      font-size: 20px;
    }
  }

  @media (max-width: 480px) {
    .settings-button {
      width: 44px; /* Maintain 44px minimum */
      height: 44px;
    }

    .settings-button i {
      font-size: 18px;
    }
  }

  @media (max-width: 320px) {
    .settings-button {
      width: 44px; /* NEVER below 44px */
      height: 44px;
    }

    .settings-button i {
      font-size: 18px;
    }
  }

  /* 🎯 LANDSCAPE MOBILE: Maintain 44px minimum for accessibility */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .workspace-header {
      min-height: 36px;
    }

    .settings-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
    }

    .settings-button i {
      font-size: 20px;
    }
  }
</style>
