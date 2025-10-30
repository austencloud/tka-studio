<!--
  ModuleList - Module switching UI component

  Displays a list of available modules (main and developer) and allows
  the user to switch between them with visual feedback for the current module.
-->
<script lang="ts">
  import type { ModuleDefinition, ModuleId } from "../domain/types";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    currentModule,
    modules = [],
    onModuleSelect,
  } = $props<{
    currentModule: ModuleId;
    modules: ModuleDefinition[];
    onModuleSelect?: (moduleId: ModuleId) => void;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Filter to main modules and dev modules
  const mainModules = $derived(
    modules.filter((m: ModuleDefinition) => m.isMain)
  );
  const devModules = $derived(
    modules.filter((m: ModuleDefinition) => !m.isMain)
  );

  function handleModuleClick(moduleId: ModuleId) {
    hapticService?.trigger("navigation");
    onModuleSelect?.(moduleId);
  }
</script>

<!-- Main Modules Section -->
<section class="module-section">
  <h3 class="section-title">Switch Module</h3>
  <div class="module-items">
    {#each mainModules as module}
      <button
        class="module-item"
        class:active={currentModule === module.id}
        onclick={() => handleModuleClick(module.id)}
      >
        <span class="item-icon">{@html module.icon}</span>
        <div class="item-info">
          <span class="item-label">{module.label}</span>
          {#if module.description}
            <span class="item-description">{module.description}</span>
          {/if}
        </div>
        {#if currentModule === module.id}
          <span class="active-indicator">
            <i class="fas fa-check"></i>
          </span>
        {/if}
      </button>
    {/each}
  </div>
</section>

<!-- Developer Modules Section -->
{#if devModules.length > 0}
  <section class="module-section">
    <h3 class="section-title">Developer Modules</h3>
    <div class="module-items">
      {#each devModules as module}
        <button
          class="module-item"
          class:active={currentModule === module.id}
          onclick={() => handleModuleClick(module.id)}
        >
          <span class="item-icon">{@html module.icon}</span>
          <div class="item-info">
            <span class="item-label">{module.label}</span>
            {#if module.description}
              <span class="item-description">{module.description}</span>
            {/if}
          </div>
          {#if currentModule === module.id}
            <span class="active-indicator">
              <i class="fas fa-check"></i>
            </span>
          {/if}
        </button>
      {/each}
    </div>
  </section>
{/if}

<style>
  .module-section {
    margin-bottom: 24px;
  }

  .module-section:last-child {
    margin-bottom: 0;
  }

  .section-title {
    margin: 0 0 12px 0;
    padding: 0 8px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: rgba(255, 255, 255, 0.5);
  }

  .module-items {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .module-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    min-height: 56px;
  }

  .module-item:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
  }

  .module-item:active {
    transform: translateX(4px) scale(0.98);
  }

  .module-item.active {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.4);
  }

  .item-icon {
    font-size: 24px;
    width: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .item-label {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .item-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.3;
  }

  .active-indicator {
    color: rgba(99, 102, 241, 1);
    font-size: 16px;
    flex-shrink: 0;
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .module-item {
      transition: none;
    }

    .module-item:hover,
    .module-item:active {
      transform: none;
    }
  }
</style>
