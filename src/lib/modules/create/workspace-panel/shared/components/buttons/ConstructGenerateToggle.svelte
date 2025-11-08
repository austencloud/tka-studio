<!--
ConstructGenerateToggle.svelte

Single-icon toggle button that switches between Construct and Generate modes.
Shows the opposite mode's icon (the action you can take).
Uses Font Awesome icons: fa-hammer (construct) and fa-wand-magic-sparkles (generate).

Design Principles:
- Action-oriented: Shows what you'll switch TO, not what you're ON
- Accessible: Full keyboard navigation and screen reader support
- Adaptive: Shows text label when alone, icon-only when with other buttons
- Consistent: Same size as other action buttons (48px circle), neutral slate color
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  type TabType = "construct" | "generate";

  const {
    activeTab = "construct",
    onTabChange,
    showLabels = false,
  } = $props<{
    activeTab?: TabType;
    onTabChange?: (tab: TabType) => void;
    showLabels?: boolean;
  }>();

  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleClick() {
    hapticService?.trigger("selection");
    const newTab = activeTab === "construct" ? "generate" : "construct";
    onTabChange?.(newTab);
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === " " || event.key === "Enter") {
      event.preventDefault();
      handleClick();
    }
  }

  // Determine which icon and label to show (opposite of current mode)
  const targetMode = $derived(
    activeTab === "construct" ? "generate" : "construct"
  );
  const targetIcon = $derived(
    targetMode === "generate" ? "fa-wand-magic-sparkles" : "fa-hammer"
  );
  const targetLabel = $derived(
    targetMode === "generate" ? "Generate" : "Construct"
  );
  const ariaLabel = $derived(`Switch to ${targetLabel} mode`);
</script>

<button
  class="toggle-button"
  class:with-label={showLabels}
  role="switch"
  aria-checked={activeTab === "generate"}
  aria-label={ariaLabel}
  onclick={handleClick}
  onkeydown={handleKeyDown}
  title={ariaLabel}
>
  <i class="fa-solid {targetIcon}"></i>
  {#if showLabels}
    <span class="label">{targetLabel}</span>
  {/if}
</button>

<style>
  .toggle-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 48px;
    height: 48px;
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-radius: 50%;
    background: rgba(100, 116, 139, 0.8);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
    color: #ffffff;
  }

  /* Wider when showing label */
  .toggle-button.with-label {
    width: auto;
    padding: 0 16px;
    border-radius: 24px;
  }

  .toggle-button:hover {
    transform: scale(1.05);
    background: rgba(100, 116, 139, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .toggle-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .toggle-button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  /* Icon styling */
  .toggle-button i {
    font-size: 18px;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
  }

  /* Label text styling */
  .label {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    white-space: nowrap;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .toggle-button {
      width: 44px;
      height: 44px;
    }

    .toggle-button i {
      font-size: 16px;
    }

    .label {
      font-size: 13px;
    }
  }

  @media (max-width: 480px) {
    .toggle-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
    }

    .toggle-button i {
      font-size: 14px;
    }

    .label {
      font-size: 12px;
    }
  }

  @media (max-width: 320px) {
    .toggle-button {
      width: 44px; /* NEVER below 44px for accessibility */
      height: 44px;
    }

    .toggle-button i {
      font-size: 12px;
    }

    .label {
      font-size: 11px;
    }
  }

  /* Landscape mobile: Maintain 44px minimum */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .toggle-button {
      width: 44px; /* Maintain 44px minimum for accessibility */
      height: 44px;
    }

    .toggle-button i {
      font-size: 14px;
    }
  }
</style>
