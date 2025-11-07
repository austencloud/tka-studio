<script lang="ts">
  /**
   * PWAInstallationManager
   * Domain: PWA Installation & Mobile Experience
   *
   * Responsibilities:
   * - Manage PWA installation prompts and timing
   * - Handle device detection and capability changes
   * - Orchestrate install prompt re-display logic
   * - Respond to app installation events
   */
  import { onMount } from "svelte";
  import type { IDeviceDetector } from "../device/services/contracts/IDeviceDetector";
  import type { IMobileFullscreenService } from "../mobile/services/contracts/IMobileFullscreenService";
  import { resolve, TYPES } from "../inversify";
  import MobileFullscreenPrompt from "../mobile/components/MobileFullscreenPrompt.svelte";
  import FullscreenHint from "../mobile/components/FullscreenHint.svelte";
  import SubtleInstallBanner from "../mobile/components/SubtleInstallBanner.svelte";
  import EnhancedPWAInstallGuide from "../mobile/components/EnhancedPWAInstallGuide.svelte";

  const INSTALL_REPROMPT_DELAY_MS = 45000;

  let showMobileInstallPrompt = $state(false);
  let showPWAInstallGuide = $state(false);
  let deviceDetector: IDeviceDetector | null = null;
  let fullscreenService: IMobileFullscreenService | null = null;
  let installRePromptTimer: ReturnType<typeof setTimeout> | null = null;

  const isOnMobile = () =>
    !!deviceDetector &&
    (deviceDetector.isMobile() || deviceDetector.isLandscapeMobile());

  const shouldShowInstallOverlay = () =>
    !!fullscreenService && isOnMobile() && !fullscreenService.isPWA();

  function clearInstallRePromptTimer() {
    if (installRePromptTimer !== null) {
      clearTimeout(installRePromptTimer);
      installRePromptTimer = null;
    }
  }

  function scheduleInstallRePrompt() {
    clearInstallRePromptTimer();

    if (typeof window === "undefined" || !shouldShowInstallOverlay()) {
      return;
    }

    installRePromptTimer = setTimeout(() => {
      if (shouldShowInstallOverlay()) {
        showMobileInstallPrompt = true;
      }
    }, INSTALL_REPROMPT_DELAY_MS);
  }

  onMount(() => {
    if (typeof window === "undefined") {
      return;
    }

    const cleanupFns: Array<() => void> = [];

    // Resolve services
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
    } catch (error) {
      console.warn("Failed to resolve device detector:", error);
      deviceDetector = null;
    }

    try {
      fullscreenService = resolve<IMobileFullscreenService>(
        TYPES.IMobileFullscreenService
      );
    } catch (error) {
      console.warn("Failed to resolve mobile fullscreen service:", error);
      fullscreenService = null;
    }

    // Initialize prompt state
    if (shouldShowInstallOverlay()) {
      showMobileInstallPrompt = true;
    } else {
      showMobileInstallPrompt = false;
    }

    // Listen for device capability changes
    if (deviceDetector) {
      const unsubscribeCapabilities = deviceDetector.onCapabilitiesChanged(
        () => {
          if (shouldShowInstallOverlay()) {
            showMobileInstallPrompt = true;
          } else {
            showMobileInstallPrompt = false;
            clearInstallRePromptTimer();
          }
        }
      );
      cleanupFns.push(() => unsubscribeCapabilities?.());
    }

    // Listen for install prompt availability
    if (fullscreenService) {
      const unsubscribeInstall = fullscreenService.onInstallPromptAvailable(
        () => {
          if (shouldShowInstallOverlay()) {
            showMobileInstallPrompt = true;
          }
        }
      );
      cleanupFns.push(() => unsubscribeInstall?.());
    }

    // Listen for app installation event
    if (typeof window !== "undefined" && fullscreenService) {
      const handleAppInstalled = () => {
        showMobileInstallPrompt = false;
        clearInstallRePromptTimer();
      };
      window.addEventListener("appinstalled", handleAppInstalled);
      cleanupFns.push(() =>
        window.removeEventListener("appinstalled", handleAppInstalled)
      );

      // Listen for display mode changes
      const updatePromptFromDisplayMode = () => {
        if (shouldShowInstallOverlay()) {
          showMobileInstallPrompt = true;
        } else {
          showMobileInstallPrompt = false;
          clearInstallRePromptTimer();
        }
      };

      const queries = [
        "(display-mode: standalone)",
        "(display-mode: fullscreen)",
        "(display-mode: minimal-ui)",
      ];

      queries.forEach((query) => {
        const mediaQuery = window.matchMedia(query);
        const handler = () => updatePromptFromDisplayMode();

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
    }

    // Listen for custom event to open install guide
    const handleOpenInstallGuide = () => {
      showPWAInstallGuide = true;
    };
    window.addEventListener("pwa:open-install-guide", handleOpenInstallGuide);
    cleanupFns.push(() =>
      window.removeEventListener(
        "pwa:open-install-guide",
        handleOpenInstallGuide
      )
    );

    cleanupFns.push(() => clearInstallRePromptTimer());

    return () => {
      cleanupFns.forEach((cleanup) => {
        try {
          cleanup();
        } catch (error) {
          console.warn("Failed to clean up PWA installation manager:", error);
        }
      });
    };
  });

  // Auto re-prompt effect
  $effect(() => {
    if (typeof window === "undefined") {
      return;
    }

    if (!fullscreenService) {
      return;
    }

    if (showMobileInstallPrompt) {
      clearInstallRePromptTimer();
      return;
    }

    if (shouldShowInstallOverlay()) {
      scheduleInstallRePrompt();
    } else {
      clearInstallRePromptTimer();
    }
  });

  function handleMobileInstallDismiss() {
    if (fullscreenService?.getRecommendedStrategy() === "not-supported") {
      clearInstallRePromptTimer();
      return;
    }
    scheduleInstallRePrompt();
  }
</script>

<!-- Mobile Fullscreen Prompt (modal) -->
<MobileFullscreenPrompt
  bind:showPrompt={showMobileInstallPrompt}
  autoShow={false}
  position="center"
  nagMode={true}
  onDismiss={handleMobileInstallDismiss}
/>

<!-- Subtle Fullscreen Hint (non-blocking) -->
<FullscreenHint />

<!-- Subtle Install Banner (non-blocking) -->
<SubtleInstallBanner />

<!-- Enhanced PWA Install Guide (modal with device-specific instructions) -->
<EnhancedPWAInstallGuide bind:showGuide={showPWAInstallGuide} />
