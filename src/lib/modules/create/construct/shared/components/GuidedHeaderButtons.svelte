<!-- Guided variant: back button, title, optional next hand button -->
<script lang="ts">
  import type { GridMode, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import GridModeToggle from "./GridModeToggle.svelte";

  const {
    title = "",
    showNextHandButton = false,
    nextHandButtonText = "Build Red Hand",
    currentGridMode,
    onBackClick,
    onNextHand,
    onGridModeChange,
  }: {
    title?: string;
    showNextHandButton?: boolean;
    nextHandButtonText?: string;
    currentGridMode?: GridMode;
    onBackClick?: (() => void) | undefined;
    onNextHand?: (() => void) | undefined;
    onGridModeChange?: ((gridMode: GridMode) => void) | undefined;
  } = $props();

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  function handleBackClick() {
    hapticService?.trigger("selection");
    onBackClick?.();
  }

  function handleNextHandClick() {
    hapticService?.trigger("selection");
    onNextHand?.();
  }
</script>

<div class="guided-header-buttons">
  <div class="header-left">
    <button class="back-button" onclick={handleBackClick} aria-label="Reset">
      <i class="fas fa-arrow-left"></i>
    </button>
  </div>

  <div class="header-center">
    <h1 class="header-title">{title}</h1>
  </div>

  <div class="header-right">
    {#if showNextHandButton}
      <button class="next-hand-button" onclick={handleNextHandClick}>
        {nextHandButtonText}
        <i class="fas fa-arrow-right"></i>
      </button>
    {:else if onGridModeChange && currentGridMode}
      <GridModeToggle {currentGridMode} {onGridModeChange} />
    {/if}
  </div>
</div>

<style>
  .guided-header-buttons {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1rem;
  }

  .header-left,
  .header-right {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    min-height: 44px;
  }

  .header-right {
    justify-content: flex-end;
  }

  .header-center {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-width: 0;
    overflow: visible;
    min-height: 44px;
  }

  .header-title {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    white-space: nowrap;
    overflow: visible;
  }

  .back-button {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
  }

  @media (hover: hover) {
    .back-button:hover {
      background: rgba(255, 255, 255, 0.12);
      transform: translateX(-2px);
    }
  }

  .back-button:active {
    transform: scale(0.95);
  }

  .next-hand-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    white-space: nowrap;
  }

  @media (hover: hover) {
    .next-hand-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
  }

  .next-hand-button:active {
    transform: translateY(0);
  }

  @media (max-width: 600px) {
    .guided-header-buttons {
      gap: 0.5rem;
    }

    .next-hand-button {
      padding: 0.625rem 1rem;
      font-size: 0.875rem;
    }
  }
</style>
