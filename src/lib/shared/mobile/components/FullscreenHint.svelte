<!--
Smart Fullscreen Hint Component

Finds the actual fullscreen button and shows a non-intrusive animated hint
pointing to it for mobile users, encouraging them to try fullscreen mode.

Features:
- Remembers user dismissal (localStorage)
- Reactive positioning that tracks DOM changes
- Auto-hides after duration or when fullscreen is activated
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { IMobileFullscreenService } from "../services/contracts/IMobileFullscreenService";

  // Props
  let {
    showHint = $bindable(false),
    autoShow = true,
    duration = 5000, // How long to show the hint
  }: {
    showHint?: boolean;
    autoShow?: boolean;
    duration?: number;
  } = $props();

  // Service
  let fullscreenService: IMobileFullscreenService | null = null;

  // State
  let strategy = $state<
    "pwa" | "fullscreen-api" | "viewport-only" | "not-supported"
  >("not-supported");
  let isFullscreen = $state(false);
  let hasShownHint = $state(false);
  let buttonPosition = $state<{
    top: number;
    left: number;
    width: number;
    height: number;
  } | null>(null);
  let hintElement = $state<HTMLDivElement | null>(null);

  // Dismissal persistence
  const DISMISSAL_KEY = "tka-fullscreen-hint-dismissed";
  let hasBeenDismissed = $state(false);

  function findFullscreenButton(): HTMLElement | null {
    // Look for fullscreen button in ButtonPanel
    const fullscreenButton = document.querySelector(".fullscreen-button");
    if (fullscreenButton instanceof HTMLElement) {
      return fullscreenButton;
    }

    // Fallback: look for any button with fullscreen aria-label
    const buttons = document.querySelectorAll(
      'button[aria-label*="fullscreen"], button[aria-label*="Fullscreen"]'
    );
    for (const button of buttons) {
      if (button instanceof HTMLElement && button.offsetParent !== null) {
        return button;
      }
    }

    return null;
  }

  function updateButtonPosition() {
    const button = findFullscreenButton();
    if (button) {
      const rect = button.getBoundingClientRect();
      buttonPosition = {
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height,
      };
    } else {
      buttonPosition = null;
    }
  }

  function checkDismissalStatus() {
    if (typeof localStorage !== "undefined") {
      hasBeenDismissed = localStorage.getItem(DISMISSAL_KEY) === "true";
    }
  }

  function saveDismissalStatus() {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(DISMISSAL_KEY, "true");
    }
    hasBeenDismissed = true;
  }

  // Initialize service on mount
  onMount(() => {
    try {
      checkDismissalStatus();
      fullscreenService = resolve(TYPES.IMobileFullscreenService);
      if (!fullscreenService) return;

      strategy = fullscreenService.getRecommendedStrategy();
      isFullscreen = fullscreenService.isFullscreen();
    } catch (error) {
      console.error("Failed to initialize fullscreen hint:", error);
    }
  });

  // Effect: Subscribe to fullscreen changes
  $effect(() => {
    if (!fullscreenService) return;

    const unsubscribe = fullscreenService.onFullscreenChange((fs) => {
      isFullscreen = fs;
      if (fs) {
        // Hide hint when user goes fullscreen
        showHint = false;
        hasShownHint = true;
        saveDismissalStatus();
      }
    });

    return () => unsubscribe?.();
  });

  // Effect: Reactive button position tracking
  // Consolidates MutationObserver, ResizeObserver, and resize events
  $effect(() => {
    if (!showHint) {
      buttonPosition = null;
      return;
    }

    // Update position immediately
    updateButtonPosition();

    // Track DOM mutations
    const mutationObserver = new MutationObserver(() => {
      requestAnimationFrame(updateButtonPosition);
    });

    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class", "style"],
    });

    // Track window resize
    window.addEventListener("resize", updateButtonPosition);

    return () => {
      mutationObserver.disconnect();
      window.removeEventListener("resize", updateButtonPosition);
    };
  });

  // Effect: Auto-show hint with reactive timing
  $effect(() => {
    if (
      !autoShow ||
      strategy !== "fullscreen-api" ||
      !fullscreenService ||
      fullscreenService.isPWA() ||
      isFullscreen ||
      hasShownHint ||
      hasBeenDismissed
    ) {
      return;
    }

    // Wait for DOM to settle, then find button and show hint
    const showTimer = setTimeout(() => {
      updateButtonPosition();
      if (buttonPosition) {
        showHint = true;

        // Auto-hide after duration
        const hideTimer = setTimeout(() => {
          showHint = false;
          hasShownHint = true;
        }, duration);

        return () => clearTimeout(hideTimer);
      }
    }, 2000);

    return () => clearTimeout(showTimer);
  });

  function handleDismiss() {
    showHint = false;
    hasShownHint = true;
    saveDismissalStatus();
  }

  // Add a function to reset dismissal status (for debugging/settings)
  function resetDismissalStatus() {
    if (typeof localStorage !== "undefined") {
      localStorage.removeItem(DISMISSAL_KEY);
    }
    hasBeenDismissed = false;
  }

  // Export reset function for potential use by parent components
  export { resetDismissalStatus };
</script>

{#if showHint && strategy === "fullscreen-api" && buttonPosition}
  <div
    bind:this={hintElement}
    class="fullscreen-hint"
    style="
      top: {buttonPosition.top - 60}px;
      left: {buttonPosition.left + buttonPosition.width / 2 - 75}px;
    "
  >
    <div class="hint-content">
      <div class="hint-text">Tap for fullscreen</div>
      <button
        class="hint-dismiss"
        onclick={handleDismiss}
        aria-label="Dismiss hint"
      >
        ×
      </button>
    </div>

    <!-- Arrow pointing down to the button -->
    <div class="hint-arrow">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M12 5v14M19 12l-7 7-7-7" />
      </svg>
    </div>
  </div>
{/if}

<style>
  .fullscreen-hint {
    position: fixed;
    z-index: 999;
    pointer-events: none;
    animation: hintBounce 2s ease-in-out infinite;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 150px;
  }

  .hint-content {
    /* Enhanced background for better visibility against all backgrounds */
    background: linear-gradient(
      135deg,
      var(--primary-color) 0%,
      var(--primary-dark) 100%
    );
    /* Fallback for better contrast */
    background-color: var(--primary-color, #6366f1);
    color: white;
    padding: 8px 12px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
    /* Enhanced shadow and backdrop for better visibility */
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.4),
      0 2px 4px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 14px;
    font-weight: 500;
    pointer-events: auto;
    position: relative;
    white-space: nowrap;
  }

  .hint-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-color, #6366f1);
    animation: arrowPulse 1.5s ease-in-out infinite;
    margin-top: 4px;
    /* Enhanced visibility with shadow */
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  }

  .hint-text {
    white-space: nowrap;
  }

  .hint-dismiss {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    padding: 0;
    margin-left: 4px;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .hint-dismiss:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Subtle bounce animation */
  @keyframes hintBounce {
    0%,
    20%,
    50%,
    80%,
    100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-4px);
    }
    60% {
      transform: translateY(-2px);
    }
  }

  /* Arrow pulse animation */
  @keyframes arrowPulse {
    0%,
    100% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.1);
      opacity: 0.8;
    }
  }

  /* Mobile optimizations */
  @media (max-width: 480px) {
    .fullscreen-hint {
      top: 16px;
      right: 16px;
    }

    .hint-content {
      padding: 6px 10px;
      font-size: 13px;
    }

    .hint-arrow svg {
      width: 20px;
      height: 20px;
    }
  }

  /* Position hint near fullscreen button area */
  @media (orientation: landscape) and (max-height: 500px) {
    .fullscreen-hint {
      top: 16px;
      right: 60px; /* Adjust based on where fullscreen button typically appears */
    }
  }
</style>
