<!--
ConstructGenerateToggle.svelte

Modern segmented control toggle based on Let's Build UI pattern.
Uses radio buttons with smooth sliding background animation.

Design Principles:
- Semantic HTML: Uses radio buttons for proper form semantics
- Accessible: Full keyboard navigation and screen reader support
- Modern: Smooth CSS transitions with cubic-bezier easing (250ms)
- Responsive: Calculates position dynamically based on active state
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";

  type TabType = "construct" | "generate";

  const {
    activeTab = "construct",
    onTabChange,
  } = $props<{
    activeTab?: TabType;
    onTabChange?: (tab: TabType) => void;
  }>();

  let hapticService: IHapticFeedbackService | null = $state(null);
  let showTooltip = $state(false);
  let tooltipTimeout: number | null = null;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  function handleRadioChange(newTab: TabType) {
    hapticService?.trigger("selection");
    onTabChange?.(newTab);

    // Show tooltip on first interaction
    if (!showTooltip) {
      showTooltip = true;
      if (tooltipTimeout) clearTimeout(tooltipTimeout);
      tooltipTimeout = window.setTimeout(() => {
        showTooltip = false;
      }, 3000);
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === " " || event.key === "Enter") {
      event.preventDefault();
      handleRadioChange(activeTab === "construct" ? "generate" : "construct");
    }
  }
</script>

<div
  class="segmented-control"
  role="switch"
  aria-checked={activeTab === "generate"}
  aria-label="Toggle between Construct and Generate modes"
  onclick={() => handleRadioChange(activeTab === "construct" ? "generate" : "construct")}
  onkeydown={handleKeyDown}
  tabindex="0"
>
  <!-- Sliding background indicator -->
  <div class="slider" class:generate={activeTab === "generate"}></div>

  <!-- Construct segment -->
  <div class="segment-button" class:active={activeTab === "construct"}>
    <span class="emoji">🔨</span>
  </div>

  <!-- Generate segment -->
  <div class="segment-button" class:active={activeTab === "generate"}>
    <span class="emoji">⚡</span>
  </div>

  {#if showTooltip}
    <div class="tooltip">
      Click to switch between Construct and Generate
    </div>
  {/if}
</div>

<style>
  .segmented-control {
    display: flex;
    width: 100px;
    height: 48px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
    padding: 2px;
    gap: 0;
    cursor: pointer;
  }

  .segmented-control:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
  }

  /* Animated sliding background indicator */
  .slider {
    position: absolute;
    top: 2px;
    left: 2px;
    width: calc(50% - 4px);
    height: calc(100% - 4px);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(139, 92, 246, 0.2));
    border-radius: 20px;
    transition: left 250ms cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
    border: 1px solid rgba(102, 126, 234, 0.3);
    box-shadow: inset 0 0 12px rgba(102, 126, 234, 0.1);
    z-index: 0;
  }

  .slider.generate {
    left: calc(50% + 2px);
  }

  /* Individual segment button */
  .segment-button {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    height: 100%;
    border-radius: 20px;
    cursor: pointer;
    position: relative;
    z-index: 1;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .segment-button:focus-within {
    outline: 2px solid #818cf8;
    outline-offset: -2px;
  }

  /* Emoji styling */
  .emoji {
    font-size: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 0.45;
    transform: scale(0.9);
    filter: grayscale(80%);
  }

  /* Active state emoji styling */
  .segment-button.active .emoji {
    opacity: 1;
    transform: scale(1.15);
    filter: grayscale(0%) drop-shadow(0 0 6px rgba(102, 126, 234, 0.7));
    animation: activeEmojiBounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  @keyframes activeEmojiBounce {
    0% {
      transform: scale(0.85);
      opacity: 0.6;
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      transform: scale(1.15);
      opacity: 1;
    }
  }

  .tooltip {
    position: absolute;
    bottom: -40px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    white-space: nowrap;
    pointer-events: none;
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .construct-generate-toggle {
      width: 90px;
      height: 44px;
    }

    .emoji {
      font-size: 18px;
    }
  }

  @media (max-width: 480px) {
    .construct-generate-toggle {
      width: 80px;
      height: 40px;
    }

    .emoji {
      font-size: 16px;
    }
  }

  @media (max-width: 320px) {
    .construct-generate-toggle {
      width: 72px;
      height: 36px;
    }

    .emoji {
      font-size: 14px;
    }
  }
</style>
