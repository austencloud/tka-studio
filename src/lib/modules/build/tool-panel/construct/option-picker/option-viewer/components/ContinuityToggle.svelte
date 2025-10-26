<!--
ContinuityToggle.svelte - Combined header bar with section title and filter toggle

Compact header bar that displays:
- Left: Current section title (e.g., "Type 1", "Types 4-6")
- Right: Continuous/All toggle button
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Props
  let {
    isContinuousOnly = false,
    sectionTitle = "",
    onToggle = () => {}
  } = $props<{
    isContinuousOnly?: boolean;
    sectionTitle?: string;
    onToggle?: (isContinuousOnly: boolean) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  function handleClick() {
    hapticService?.trigger("selection");
    onToggle(!isContinuousOnly);
  }
</script>

<div class="header-bar">
  <!-- Section title (left) -->
  <div class="section-title">
    {@html sectionTitle}
  </div>

  <!-- Toggle button (right) -->
  <button
    class="toggle-button"
    class:continuous={isContinuousOnly}
    onclick={handleClick}
    title={isContinuousOnly ? "Showing continuous options only (click for all)" : "Showing all options (click for continuous only)"}
  >
    {isContinuousOnly ? "Continuous" : "All"}
  </button>
</div>

<style>
  .header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 6px 8px;
    margin-bottom: 6px;
    background: rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(8px);
    border-radius: 8px;
  }

  .section-title {
    flex: 0 1 auto;
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.85);
    padding-left: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .toggle-button {
    flex-shrink: 0;
    padding: 6px 14px;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-align: center;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }

  @media (hover: hover) {
    .toggle-button:hover {
      background: rgba(0, 0, 0, 0.6);
      color: rgba(255, 255, 255, 0.95);
      border-color: rgba(255, 255, 255, 0.25);
      transform: scale(1.05);
    }

    .toggle-button.continuous:hover {
      background: rgba(59, 130, 246, 0.35);
      border-color: rgba(59, 130, 246, 0.5);
      box-shadow: 0 2px 16px rgba(59, 130, 246, 0.35);
    }
  }

  .toggle-button.continuous {
    background: rgba(59, 130, 246, 0.25);
    color: white;
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.25);
  }

  .toggle-button:active {
    transform: scale(0.95);
  }

  /* Responsive adjustments */
  @media (max-width: 480px) {
    .header-bar {
      gap: 8px;
      padding: 5px 6px;
    }

    .section-title {
      font-size: 12px;
    }

    .toggle-button {
      padding: 5px 12px;
      font-size: 10px;
    }
  }
</style>
