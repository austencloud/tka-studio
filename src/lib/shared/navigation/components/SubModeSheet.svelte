<!-- Slide-up Sheet for Sub-Mode Selection (Portrait Mobile) -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { IAnimationService } from "../../application/services/contracts";
  import { resolve, TYPES } from "../../inversify";
  import type { ModeOption, ModuleDefinition } from "../domain/types";

  let {
    show = false,
    module,
    currentSubMode,
    onSubModeSelect,
    onClose,
  } = $props<{
    show: boolean;
    module: ModuleDefinition | null;
    currentSubMode: string;
    onSubModeSelect?: (subModeId: string) => void;
    onClose?: () => void;
  }>();

  let animationService: IAnimationService | null = null;

  onMount(() => {
    animationService = resolve<IAnimationService>(TYPES.IAnimationService);
  });

  // Handle backdrop click
  function handleBackdropClick() {
    onClose?.();
  }

  // Handle sub-mode selection
  function handleSubModeClick(subMode: ModeOption) {
    onSubModeSelect?.(subMode.id);
    onClose?.();
  }

  // Slide transition
  const slideTransition = (node: Element) => {
    if (!animationService) {
      return {
        duration: 300,
        css: (t: number) => `transform: translateY(${(1 - t) * 100}%)`,
      };
    }
    return {
      duration: 300,
      css: (t: number) => {
        const easeOut = 1 - Math.pow(1 - t, 3);
        return `transform: translateY(${(1 - easeOut) * 100}%)`;
      },
    };
  };

  const fadeTransition = (node: Element) => {
    if (!animationService) {
      return {
        duration: 200,
        css: (t: number) => `opacity: ${t}`,
      };
    }
    return animationService.createFadeTransition({ duration: 200 });
  };
</script>

{#if show && module}
  <!-- Backdrop -->
  <div
    class="sheet-backdrop"
    onclick={handleBackdropClick}
    transition:fadeTransition
    role="presentation"
  ></div>

  <!-- Sheet -->
  <div
    class="sub-mode-sheet glass-surface"
    transition:slideTransition
    role="dialog"
    aria-label="Select mode"
  >
    <!-- Handle bar for visual affordance -->
    <div class="sheet-handle"></div>

    <!-- Module header -->
    <div class="sheet-header">
      <span class="module-icon">{@html module.icon}</span>
      <h2>{module.label}</h2>
    </div>

    <!-- Sub-mode buttons -->
    <div class="sub-mode-list">
      {#each module.subModes as subMode}
        <button
          class="sub-mode-button"
          class:active={currentSubMode === subMode.id}
          class:disabled={subMode.disabled}
          onclick={() => handleSubModeClick(subMode)}
          disabled={subMode.disabled}
        >
          <span class="sub-mode-icon">{@html subMode.icon}</span>
          <div class="sub-mode-info">
            <span class="sub-mode-label">{subMode.label}</span>
            {#if subMode.description}
              <span class="sub-mode-description">{subMode.description}</span>
            {/if}
          </div>
        </button>
      {/each}
    </div>
  </div>
{/if}

<style>
  .sheet-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 150;
    backdrop-filter: blur(4px);
  }

  .sub-mode-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 70vh;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--glass-backdrop-strong);
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    z-index: 151;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    /* Account for iOS safe area */
    padding-bottom: env(safe-area-inset-bottom);
  }

  .sheet-handle {
    width: 40px;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    margin: 12px auto 8px;
    flex-shrink: 0;
  }

  .sheet-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 24px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .module-icon {
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .sheet-header h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .sub-mode-list {
    padding: 12px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .sub-mode-button {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    min-height: 64px;
  }

  .sub-mode-button:active {
    transform: scale(0.98);
  }

  .sub-mode-button.active {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .sub-mode-button.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .sub-mode-button.disabled:active {
    transform: none;
  }

  .sub-mode-icon {
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .sub-mode-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }

  .sub-mode-label {
    font-size: 16px;
    font-weight: 600;
  }

  .sub-mode-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .sub-mode-sheet {
      background: rgba(0, 0, 0, 0.95);
      border-top: 2px solid white;
    }

    .sub-mode-button {
      background: rgba(255, 255, 255, 0.1);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .sub-mode-button.active {
      background: rgba(255, 255, 255, 0.3);
      border-color: white;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .sub-mode-button {
      transition: none;
    }

    .sub-mode-button:active {
      transform: none;
    }
  }
</style>
