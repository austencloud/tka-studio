<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ModuleDefinition, ModuleId } from "../domain/types";

  let {
    mainModules = [],
    devModules = [],
    currentModule,
    onModuleSelect,
    onHover,
    onMouseLeave,
  } = $props<{
    mainModules: ModuleDefinition[];
    devModules: ModuleDefinition[];
    currentModule: ModuleId;
    onModuleSelect: (moduleId: ModuleId) => void;
    onHover?: () => void;
    onMouseLeave?: () => void;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function selectModule(module: ModuleDefinition) {
    hapticService?.trigger("navigation");
    onModuleSelect(module.id);
  }
</script>

<!-- Desktop Module Dropdown -->
<div
  class="desktop-module-dropdown"
  role="menu"
  aria-label="Module selector"
  tabindex="-1"
  onmouseenter={onHover}
  onmouseleave={onMouseLeave}
>
  <!-- Main modules -->
  {#each mainModules as module}
    <button
      class="dropdown-module-item"
      class:current={module.id === currentModule}
      onclick={() => selectModule(module)}
      role="menuitem"
      tabindex="0"
    >
      <span class="module-icon" aria-hidden="true">{@html module.icon}</span>
      <div class="module-content">
        <span class="module-label">{module.label}</span>
        {#if module.description}
          <span class="module-description">{module.description}</span>
        {/if}
      </div>
      {#if module.id === currentModule}
        <span class="current-indicator" aria-hidden="true">✓</span>
      {/if}
    </button>
  {/each}

  <!-- Developer modules separator -->
  {#if devModules.length > 0}
    <div class="dropdown-separator">
      <span>Developer Tools</span>
    </div>
    {#each devModules as module}
      <button
        class="dropdown-module-item developer-module"
        class:current={module.id === currentModule}
        onclick={() => selectModule(module)}
        role="menuitem"
        tabindex="0"
      >
        <span class="module-icon" aria-hidden="true">{@html module.icon}</span>
        <div class="module-content">
          <span class="module-label">{module.label}</span>
          {#if module.description}
            <span class="module-description">{module.description}</span>
          {/if}
        </div>
        {#if module.id === currentModule}
          <span class="current-indicator" aria-hidden="true">✓</span>
        {/if}
      </button>
    {/each}
  {/if}
</div>

<style>
  /* Desktop Module Dropdown Styles */
  .desktop-module-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1000;
    min-width: 300px;
    margin-top: 8px;
    background: var(
      --dropdown-bg-current,
      linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.92) 0%,
        rgba(240, 242, 247, 0.92) 100%
      )
    );
    backdrop-filter: blur(20px);
    border: var(--dropdown-border-current, 1px solid rgba(99, 102, 241, 0.4));
    border-radius: 12px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    overflow: hidden;
    animation: dropdown-appear 0.2s ease-out;
  }

  @keyframes dropdown-appear {
    from {
      opacity: 0;
      transform: translateY(-8px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .dropdown-module-item {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    padding: 12px 16px;
    background: transparent;
    border: none;
    color: var(--dropdown-text-current, #1a1a1a);
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }

  .dropdown-module-item:last-child {
    border-bottom: none;
  }

  .dropdown-module-item:hover {
    background: var(--dropdown-hover-current, rgba(226, 232, 240, 0.8));
    transform: translateX(4px);
  }

  .dropdown-module-item.current {
    background: var(--dropdown-current-current, rgba(59, 130, 246, 0.2));
    border-left: 3px solid var(--accent, #3b82f6);
  }

  .dropdown-module-item.developer-module {
    border-left: 3px solid rgba(255, 165, 0, 0.3);
  }

  .dropdown-module-item.developer-module.current {
    border-left: 3px solid #ffa500;
  }

  .module-icon {
    font-size: 20px;
    width: 24px;
    text-align: center;
    flex-shrink: 0;
    transition:
      transform 0.2s ease,
      filter 0.2s ease;
  }

  .dropdown-module-item:hover .module-icon {
    transform: scale(1.1);
    filter: brightness(1.2);
  }

  .module-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .module-label {
    font-weight: 600;
    font-size: 14px;
    line-height: 1.2;
  }

  .module-description {
    font-size: 12px;
    color: var(--dropdown-description-current, #4a5568);
    font-weight: 400;
    line-height: 1.3;
  }

  .current-indicator {
    color: var(--accent, #3b82f6);
    font-weight: bold;
    flex-shrink: 0;
  }

  .dropdown-separator {
    padding: 8px 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    background: rgba(0, 0, 0, 0.02);
  }

  .dropdown-separator span {
    font-size: 12px;
    font-weight: 600;
    color: var(--muted-foreground);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Focus styles for accessibility */
  .dropdown-module-item:focus {
    outline: 2px solid var(--accent, #3b82f6);
    outline-offset: -2px;
    background: var(--dropdown-hover-current, rgba(226, 232, 240, 0.8));
  }
</style>
