<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { Section } from "../domain/types";

  let {
    modes = [],
    currentMode,
    onModeChange,
    onClose,
    isOpen = false,
  } = $props<{
    modes: Section[];
    currentMode: string;
    onModeChange: (mode: string) => void;
    onClose: () => void;
    isOpen: boolean;
  }>();

  let dropdownElement = $state<HTMLDivElement>();
  let hapticService: IHapticFeedbackService;

  // Handle click outside to close dropdown
  function handleClickOutside(event: MouseEvent) {
    if (dropdownElement && !dropdownElement.contains(event.target as Node)) {
      onClose();
    }
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      onClose();
    }
  }

  // Set up event listeners
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    if (isOpen) {
      document.addEventListener("click", handleClickOutside);
      document.addEventListener("keydown", handleKeydown);

      return () => {
        document.removeEventListener("click", handleClickOutside);
        document.removeEventListener("keydown", handleKeydown);
      };
    }
  });

  // Handle mode selection
  function selectMode(mode: Section) {
    hapticService?.trigger("selection");
    onModeChange(mode.id);
    onClose();
  }
</script>

{#if isOpen}
  <div
    bind:this={dropdownElement}
    class="dropdown-menu"
    role="menu"
    aria-label="Build modes"
  >
    {#each modes as mode}
      <button
        class="dropdown-item"
        class:current={mode.id === currentMode}
        onclick={() => selectMode(mode)}
        role="menuitem"
        tabindex="0"
      >
        <span class="mode-icon" aria-hidden="true">{mode.icon}</span>
        <div class="mode-content">
          <span class="mode-label">{mode.label}</span>
          {#if mode.description}
            <span class="mode-description">{mode.description}</span>
          {/if}
        </div>
        {#if mode.id === currentMode}
          <span class="current-indicator" aria-hidden="true">✓</span>
        {/if}
      </button>
    {/each}
  </div>
{/if}

<style>
  .dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1000;
    min-width: 280px;
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

  .dropdown-item {
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

  .dropdown-item:last-child {
    border-bottom: none;
  }

  .dropdown-item:hover {
    background: var(--dropdown-hover-current, rgba(226, 232, 240, 0.8));
    transform: translateX(4px);
  }

  .dropdown-item.current {
    background: var(--dropdown-current-current, rgba(59, 130, 246, 0.2));
    border-left: 3px solid var(--accent, #3b82f6);
  }

  .mode-icon {
    font-size: 20px;
    width: 24px;
    text-align: center;
    flex-shrink: 0;
  }

  .mode-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .mode-label {
    font-weight: 600;
    font-size: 14px;
    line-height: 1.2;
  }

  .mode-description {
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

  /* Focus styles for accessibility */
  .dropdown-item:focus {
    outline: 2px solid var(--accent, #3b82f6);
    outline-offset: -2px;
    background: var(--dropdown-hover-current, rgba(226, 232, 240, 0.8));
  }
</style>
