<!--
  ModuleMobileModal.svelte

  Mobile module selector presented as a bottom sheet.
  Relies on the shared BottomSheet component for consistent accessibility.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { BottomSheet, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ModuleDefinition, ModuleId } from "../domain/types";
  import { ViewportCalculator } from "../services/implementations";

  let {
    mainModules = [],
    devModules = [],
    currentModule,
    onModuleSelect,
    onClose,
    isOpen = false,
  } = $props<{
    mainModules: ModuleDefinition[];
    devModules: ModuleDefinition[];
    currentModule: ModuleId;
    onModuleSelect: (moduleId: ModuleId) => void;
    onClose: () => void;
    isOpen: boolean;
  }>();

  let hapticService: IHapticFeedbackService | null = null;
  const viewportCalculator = new ViewportCalculator();
  let teardownViewport: (() => void) | null = null;

  onMount(() => {
    try {
      hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    } catch (error) {
      console.warn("ModuleMobileModal: failed to resolve IHapticFeedbackService", error);
    }
  });

  function handleClose() {
    onClose();
  }

  function handleSheetClose() {
    hapticService?.trigger("navigation");
    handleClose();
  }

  function selectModule(module: ModuleDefinition) {
    hapticService?.trigger("selection");
    onModuleSelect(module.id);
    handleClose();
  }

  $effect(() => {
    if (!isOpen) {
      if (teardownViewport) {
        teardownViewport();
        teardownViewport = null;
      }
      return;
    }

    if (typeof window === "undefined") {
      return;
    }

    viewportCalculator.updateCSSProperties();

    if (!teardownViewport) {
      teardownViewport = viewportCalculator.setupListeners(() => {
        viewportCalculator.updateCSSProperties();
      });
    }

    return () => {
      if (teardownViewport) {
        teardownViewport();
        teardownViewport = null;
      }
    };
  });
</script>

<BottomSheet
  {isOpen}
  labelledBy="module-selector-title"
  on:close={handleSheetClose}
  class="module-sheet"
  backdropClass="module-sheet-backdrop"
>
  <header class="sheet-header">
    <div class="sheet-header__title">
      <h2 id="module-selector-title">Choose Module</h2>
      <p>Select a primary experience. Developer tools live below.</p>
    </div>
    <button class="close-button" onclick={handleSheetClose} aria-label="Close module selector">
      <span aria-hidden="true">&times;</span>
    </button>
  </header>

  <section class="module-list">
    {#each mainModules as module (module.id)}
      <button
        class="module-card"
        class:current={module.id === currentModule}
        onclick={() => selectModule(module)}
      >
        <span class="module-icon">{@html module.icon}</span>
        <div class="module-info">
          <span class="module-label">{module.label}</span>
          {#if module.description}
            <span class="module-description">{module.description}</span>
          {/if}
        </div>
        {#if module.id === currentModule}
          <span class="current-indicator" aria-hidden="true">●</span>
        {/if}
      </button>
    {/each}
  </section>

  {#if devModules.length > 0}
    <div class="list-separator" role="presentation">
      <span>Developer Modules</span>
    </div>

    <section class="module-list developer">
      {#each devModules as module (module.id)}
        <button
          class="module-card developer"
          class:current={module.id === currentModule}
          onclick={() => selectModule(module)}
        >
          <span class="module-icon">{@html module.icon}</span>
          <div class="module-info">
            <span class="module-label">{module.label}</span>
            {#if module.description}
              <span class="module-description">{module.description}</span>
            {/if}
          </div>
          {#if module.id === currentModule}
            <span class="current-indicator developer" aria-hidden="true">●</span>
          {/if}
        </button>
      {/each}
    </section>
  {/if}

  <footer class="sheet-footer">
    <button class="cancel-button" onclick={handleSheetClose}>Cancel</button>
  </footer>
</BottomSheet>

<style>
  :global(.module-sheet-backdrop) {
    z-index: 1100;
  }

  :global(.module-sheet) {
    background: rgba(19, 19, 24, 0.92);
  }

  .sheet-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    padding: 20px 12px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .sheet-header__title h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .sheet-header__title p {
    margin: 4px 0 0;
    color: rgba(255, 255, 255, 0.55);
    font-size: 13px;
  }

  .close-button {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.85);
    border: none;
    border-radius: 999px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.16);
  }

  .module-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 16px 8px 0;
  }

  .module-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    color: rgba(255, 255, 255, 0.95);
    text-align: left;
    cursor: pointer;
    transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
  }

  .module-card:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .module-card.current {
    border-color: var(--accent, #4f46e5);
    background: rgba(79, 70, 229, 0.15);
  }

  .module-card.developer {
    border-color: rgba(255, 165, 0, 0.25);
  }

  .module-card.developer.current {
    border-color: rgba(255, 165, 0, 0.55);
    background: rgba(255, 165, 0, 0.12);
  }

  .module-icon {
    font-size: 30px;
    width: 44px;
    height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .module-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }

  .module-label {
    font-size: 16px;
    font-weight: 600;
  }

  .module-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  .list-separator {
    padding: 12px 0 0;
    text-align: center;
    color: rgba(255, 255, 255, 0.5);
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .sheet-footer {
    margin-top: 16px;
    padding: 12px 8px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .cancel-button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: rgba(255, 255, 255, 0.9);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease, border-color 0.2s ease;
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.24);
  }

  @media (max-width: 480px) {
    .module-card {
      padding: 14px;
    }

    .sheet-header {
      padding: 18px 10px 12px;
    }

    .sheet-footer {
      padding: 10px 6px 0;
    }
  }
</style>
