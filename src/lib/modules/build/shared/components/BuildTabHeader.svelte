<!--
  BuildTabHeader.svelte
  
  Header component for Build tab with segmented control for Construct/Generate toggle.
  Similar to option picker header but with a toggle in the middle.
  
  Responsibilities:
  - Display header with centered segmented control
  - Handle tab switching between Construct and Generate
  - Provide visual feedback for active tab
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  // Props
  const {
    activeTab,
    onTabChange,
  } = $props<{
    activeTab: "construct" | "generate";
    onTabChange: (tab: "construct" | "generate") => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Handle tab click
  function handleTabClick(tab: "construct" | "generate") {
    console.log("Ì¥Ñ BuildTabHeader.handleTabClick:", { tab, activeTab, onTabChange: typeof onTabChange });
    if (tab !== activeTab) {
      console.log("Ì≥¢ Tab changed, calling onTabChange");
      hapticService?.trigger("navigation");
      onTabChange(tab);
    } else {
      console.log("‚ö†Ô∏è Tab is already active, skipping");
    }
  }

  // Handle keyboard navigation
  function handleKeyDown(event: KeyboardEvent, tab: "construct" | "generate") {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleTabClick(tab);
    }
  }
</script>

<!-- Header with segmented control -->
<div class="build-tab-header">
  <div class="header-content">
    <!-- Segmented Control -->
    <div class="segmented-control" role="tablist" aria-label="Build tab selection">
      <!-- Construct Tab -->
      <button
        type="button"
        class="segment-button"
        class:active={activeTab === "construct"}
        onclick={() => handleTabClick("construct")}
        onkeydown={(e) => handleKeyDown(e, "construct")}
        role="tab"
        aria-selected={activeTab === "construct"}
        aria-controls="construct-panel"
        id="tab-construct"
      >
        Ì¥® Construct
      </button>

      <!-- Generate Tab -->
      <button
        type="button"
        class="segment-button"
        class:active={activeTab === "generate"}
        onclick={() => handleTabClick("generate")}
        onkeydown={(e) => handleKeyDown(e, "generate")}
        role="tab"
        aria-selected={activeTab === "generate"}
        aria-controls="generate-panel"
        id="tab-generate"
      >
        ‚ö° Generate
      </button>
    </div>
  </div>
</div>

<style>
  .build-tab-header {
    width: 100%;
    position: relative;
    padding: 12px 16px;
    min-height: auto;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .header-content {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  /* Segmented Control Styles */
  .segmented-control {
    display: inline-flex;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 4px;
    gap: 0;
  }

  .segment-button {
    flex: 1;
    padding: 8px 16px;
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 10px;
    white-space: nowrap;
    user-select: none;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }

  .segment-button:hover:not(.active) {
    color: rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.05);
  }

  .segment-button.active {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  }

  .segment-button:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .build-tab-header {
      padding: 10px 12px;
    }

    .segment-button {
      padding: 6px 12px;
      font-size: 12px;
      min-height: 28px;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .segment-button {
      transition: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .segmented-control {
      border: 2px solid rgba(255, 255, 255, 0.5);
    }

    .segment-button.active {
      border: 2px solid #667eea;
    }
  }
</style>
