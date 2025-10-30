<!--
  FloatingFullscreenButton.svelte

  Floating fullscreen toggle button positioned at bottom-right of viewport.
  Features auto-hide behavior and subtle styling for minimal visual intrusion.
  Only shown when not running as PWA (since PWAs are already fullscreen).
-->
<script lang="ts">
  import type {
    IHapticFeedbackService,
    IMobileFullscreenService,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  // State
  let isFullscreen = $state(false);
  let isFullscreenSupported = $state(false);
  let isPWA = $state(false);
  let isVisible = $state(true);
  let hideTimeout: ReturnType<typeof setTimeout> | null = null;

  // Services
  let hapticService: IHapticFeedbackService | null = null;
  let fullscreenService: IMobileFullscreenService | null = null;

  onMount(() => {
    const cleanupFns: Array<() => void> = [];

    try {
      hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    } catch (error) {
      console.warn("Failed to resolve haptic feedback service:", error);
    }

    try {
      fullscreenService = resolve<IMobileFullscreenService>(
        TYPES.IMobileFullscreenService
      );
    } catch (error) {
      console.warn("Failed to resolve mobile fullscreen service:", error);
      fullscreenService = null;
    }

    if (fullscreenService) {
      isFullscreenSupported = fullscreenService.isFullscreenSupported();
      isFullscreen = fullscreenService.isFullscreen();
      isPWA = fullscreenService.isPWA();

      const unsubscribeFullscreen = fullscreenService.onFullscreenChange(
        (fullscreen) => {
          isFullscreen = fullscreen;
        }
      );
      cleanupFns.push(() => unsubscribeFullscreen?.());

      const updatePWAStatus = () => {
        isPWA = fullscreenService?.isPWA() ?? false;
      };

      const unsubscribeInstall = fullscreenService.onInstallPromptAvailable(
        () => updatePWAStatus()
      );
      cleanupFns.push(() => unsubscribeInstall?.());

      if (typeof window !== "undefined" && "matchMedia" in window) {
        const queries = [
          "(display-mode: standalone)",
          "(display-mode: fullscreen)",
          "(display-mode: minimal-ui)",
        ];

        queries.forEach((query) => {
          const mediaQuery = window.matchMedia(query);
          const handler = () => updatePWAStatus();

          if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener("change", handler);
            cleanupFns.push(() =>
              mediaQuery.removeEventListener("change", handler)
            );
          } else if (mediaQuery.addListener) {
            mediaQuery.addListener(handler);
            cleanupFns.push(() => mediaQuery.removeListener(handler));
          }
        });

        const handleAppInstalled = () => updatePWAStatus();
        window.addEventListener("appinstalled", handleAppInstalled);
        cleanupFns.push(() =>
          window.removeEventListener("appinstalled", handleAppInstalled)
        );
      }
    } else {
      // Fallback to direct DOM checks if service is unavailable
      const supportsFullscreen = !!(
        document.fullscreenEnabled ||
        (document as any).webkitFullscreenEnabled ||
        (document as any).mozFullScreenEnabled ||
        (document as any).msFullscreenEnabled
      );
      isFullscreenSupported = supportsFullscreen;
      isPWA = false;

      const handleFullscreenChange = () => {
        isFullscreen = !!(
          document.fullscreenElement ||
          (document as any).webkitFullscreenElement ||
          (document as any).mozFullScreenElement ||
          (document as any).msFullscreenElement
        );
      };

      document.addEventListener("fullscreenchange", handleFullscreenChange);
      document.addEventListener(
        "webkitfullscreenchange",
        handleFullscreenChange
      );
      document.addEventListener("mozfullscreenchange", handleFullscreenChange);
      document.addEventListener("MSFullscreenChange", handleFullscreenChange);

      cleanupFns.push(() =>
        document.removeEventListener("fullscreenchange", handleFullscreenChange)
      );
      cleanupFns.push(() =>
        document.removeEventListener(
          "webkitfullscreenchange",
          handleFullscreenChange
        )
      );
      cleanupFns.push(() =>
        document.removeEventListener(
          "mozfullscreenchange",
          handleFullscreenChange
        )
      );
      cleanupFns.push(() =>
        document.removeEventListener(
          "MSFullscreenChange",
          handleFullscreenChange
        )
      );
    }

    // Auto-hide behavior: hide after 3 seconds of no interaction
    const resetHideTimer = () => {
      isVisible = true;
      if (hideTimeout) {
        clearTimeout(hideTimeout);
      }
      hideTimeout = setTimeout(() => {
        isVisible = false;
      }, 3000);
    };

    // Show button on mouse movement or touch
    const handleInteraction = () => {
      resetHideTimer();
    };

    // Set initial timer
    resetHideTimer();

    // Listen for user interactions
    window.addEventListener("mousemove", handleInteraction);
    window.addEventListener("touchstart", handleInteraction);
    window.addEventListener("scroll", handleInteraction);

    cleanupFns.push(() => {
      window.removeEventListener("mousemove", handleInteraction);
      window.removeEventListener("touchstart", handleInteraction);
      window.removeEventListener("scroll", handleInteraction);
      if (hideTimeout) {
        clearTimeout(hideTimeout);
      }
    });

    return () => {
      cleanupFns.forEach((cleanup) => {
        try {
          cleanup();
        } catch (error) {
          console.warn("Failed to clean up floating fullscreen listeners:", error);
        }
      });
    };
  });

  async function handleClick() {
    try {
      if (isFullscreen) {
        hapticService?.trigger("navigation");

        if (fullscreenService) {
          await fullscreenService.exitFullscreen();
        } else if (document.exitFullscreen) {
          await document.exitFullscreen();
        } else if ((document as any).webkitExitFullscreen) {
          await (document as any).webkitExitFullscreen();
        } else if ((document as any).mozCancelFullScreen) {
          await (document as any).mozCancelFullScreen();
        } else if ((document as any).msExitFullscreen) {
          await (document as any).msExitFullscreen();
        }
      } else {
        hapticService?.trigger("selection");

        if (fullscreenService) {
          await fullscreenService.requestFullscreen();
        } else {
          const element = document.documentElement;
          if (element.requestFullscreen) {
            await element.requestFullscreen();
          } else if ((element as any).webkitRequestFullscreen) {
            await (element as any).webkitRequestFullscreen();
          } else if ((element as any).mozRequestFullScreen) {
            await (element as any).mozRequestFullScreen();
          } else if ((element as any).msRequestFullscreen) {
            await (element as any).msRequestFullscreen();
          }
        }
      }
    } catch (error) {
      console.warn("Fullscreen toggle failed:", error);
    }
  }

  function handleMouseEnter() {
    isVisible = true;
    if (hideTimeout) {
      clearTimeout(hideTimeout);
      hideTimeout = null;
    }
  }

  function handleMouseLeave() {
    if (hideTimeout) {
      clearTimeout(hideTimeout);
    }
    hideTimeout = setTimeout(() => {
      isVisible = false;
    }, 3000);
  }
</script>

{#if isFullscreenSupported && !isPWA}
  {#if isVisible}
    <button
      class="floating-fullscreen-button"
      class:hidden={!isVisible}
      onclick={handleClick}
      onmouseenter={handleMouseEnter}
      onmouseleave={handleMouseLeave}
      aria-label={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
      title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
      transition:fade={{ duration: 200 }}
    >
      {#if isFullscreen}
        <!-- Exit fullscreen icon -->
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      {:else}
        <!-- Enter fullscreen icon -->
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      {/if}
    </button>
  {/if}
{/if}

<style>
  .floating-fullscreen-button {
    /* Fixed positioning at bottom-right */
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999; /* High z-index to ensure it's always on top */

    /* Button styling */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    color: #ffffff;

    /* Subtle glass morphism styling */
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);

    /* Smooth transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .floating-fullscreen-button:hover {
    transform: scale(1.1);
    background: rgba(0, 0, 0, 0.7);
    border-color: rgba(255, 255, 255, 0.25);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  }

  .floating-fullscreen-button:active {
    transform: scale(0.95);
    transition: all 0.1s ease;
  }

  .floating-fullscreen-button:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  .floating-fullscreen-button.hidden {
    opacity: 0;
    pointer-events: none;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .floating-fullscreen-button {
      width: 44px;
      height: 44px;
      bottom: 16px;
      right: 16px;
    }
  }

  @media (max-width: 480px) {
    .floating-fullscreen-button {
      width: 44px; /* iOS/Android minimum touch target */
      height: 44px;
      bottom: 12px;
      right: 12px;
    }
  }

  @media (max-width: 320px) {
    .floating-fullscreen-button {
      width: 44px; /* NEVER below 44px for accessibility */
      height: 44px;
      bottom: 10px;
      right: 10px;
    }
  }

  /* Landscape mobile: maintain 44px minimum */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .floating-fullscreen-button {
      width: 44px; /* Maintain 44px minimum even in landscape */
      height: 44px;
      bottom: 12px;
      right: 12px;
    }
  }

  /* Extreme constraints: still maintain 44px */
  @media (max-width: 500px) and (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .floating-fullscreen-button {
      width: 44px; /* Accessibility trumps space constraints */
      height: 44px;
      bottom: 8px;
      right: 8px;
    }
  }
</style>
