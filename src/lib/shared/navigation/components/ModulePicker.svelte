<!-- Slide-up Sheet for Module Selection (Portrait Mobile) -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { IAnimationService } from "../../application/services/contracts";
  import { resolve, TYPES } from "../../inversify";
  import type { ModuleDefinition, ModuleId } from "../domain/types";

  let {
    show = false,
    modules = [],
    currentModule,
    onModuleSelect,
    onClose,
  } = $props<{
    show: boolean;
    modules: ModuleDefinition[];
    currentModule: ModuleId;
    onModuleSelect?: (moduleId: ModuleId) => void;
    onClose?: () => void;
  }>();

  let animationService: IAnimationService | null = null;

  onMount(() => {
    animationService = resolve<IAnimationService>(TYPES.IAnimationService);
  });

  // Filter to main modules only
  const mainModules = $derived(
    modules.filter((m: ModuleDefinition) => m.isMain)
  );

  // Handle backdrop click
  function handleBackdropClick() {
    onClose?.();
  }

  // Handle module selection
  function handleModuleClick(module: ModuleDefinition) {
    onModuleSelect?.(module.id);
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

{#if show}
  <!-- Backdrop -->
  <div
    class="sheet-backdrop"
    onclick={handleBackdropClick}
    transition:fadeTransition
    role="presentation"
  ></div>

  <!-- Sheet -->
  <div
    class="module-picker-sheet glass-surface"
    transition:slideTransition
    role="dialog"
    aria-label="Select module"
  >
    <!-- Handle bar for visual affordance -->
    <div class="sheet-handle"></div>

    <!-- Header -->
    <div class="sheet-header">
      <h2>Switch Module</h2>
    </div>

    <!-- Module buttons -->
    <div class="module-list">
      {#each mainModules as module}
        <button
          class="module-button"
          class:active={currentModule === module.id}
          onclick={() => handleModuleClick(module)}
        >
          <span class="module-icon">{@html module.icon}</span>
          <div class="module-info">
            <span class="module-label">{module.label}</span>
            {#if module.description}
              <span class="module-description">{module.description}</span>
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

  .module-picker-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 50vh;
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
    justify-content: center;
    padding: 16px 24px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .sheet-header h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .module-list {
    padding: 12px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .module-button {
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

  .module-button:active {
    transform: scale(0.98);
  }

  .module-button.active {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }

  .module-icon {
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .module-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }

  .module-label {
    font-size: 18px;
    font-weight: 600;
  }

  .module-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .module-picker-sheet {
      background: rgba(0, 0, 0, 0.95);
      border-top: 2px solid white;
    }

    .module-button {
      background: rgba(255, 255, 255, 0.1);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .module-button.active {
      background: rgba(255, 255, 255, 0.3);
      border-color: white;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .module-button {
      transition: none;
    }

    .module-button:active {
      transform: none;
    }
  }
</style>
