<!--
  SubtleInstallBanner.svelte

  Tier 1: Subtle, non-blocking banner that slides in from top
  after user meets engagement thresholds.

  Features:
  - Minimalist design
  - Easy to dismiss
  - Shows only after meaningful engagement
  - Respects dismissal timing (7/30/90 days)
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";
  import type { IMobileFullscreenService } from "../services/contracts/IMobileFullscreenService";
  import type { IPWAEngagementService } from "../services/contracts/IPWAEngagementService";
  import type { IPWAInstallDismissalService } from "../services/contracts/IPWAInstallDismissalService";

  // Services
  let fullscreenService: IMobileFullscreenService | null = null;
  let engagementService: IPWAEngagementService | null = null;
  let dismissalService: IPWAInstallDismissalService | null = null;

  // State
  let show = $state(false);
  let canInstallPWA = $state(false);
  let isPWA = $state(false);
  let isInstalling = $state(false);

  onMount(() => {
    try {
      fullscreenService = resolve<IMobileFullscreenService>(
        TYPES.IMobileFullscreenService
      );
      engagementService = resolve<IPWAEngagementService>(
        TYPES.IPWAEngagementService
      );
      dismissalService = resolve<IPWAInstallDismissalService>(
        TYPES.IPWAInstallDismissalService
      );
    } catch (error) {
      console.warn("Failed to resolve PWA services:", error);
      return;
    }

    if (!fullscreenService || !engagementService || !dismissalService) {
      return;
    }

    // Check initial state
    isPWA = fullscreenService.isPWA();
    canInstallPWA = fullscreenService.canInstallPWA();

    // Don't show if already installed as PWA
    if (isPWA) {
      return;
    }

    // Check if we should show based on engagement and dismissal timing
    const hasEngagement = engagementService.shouldShowInstallPrompt();
    const canShowPrompt = dismissalService.canShowPrompt();

    if (hasEngagement && canShowPrompt) {
      // Delay banner appearance to avoid interrupting
      setTimeout(() => {
        show = true;
      }, 1500);
    }

    // Listen for install prompt availability
    const unsubscribe = fullscreenService.onInstallPromptAvailable(
      (available) => {
        canInstallPWA = available;
      }
    );

    // Listen for app installation
    const handleAppInstalled = () => {
      show = false;
      isPWA = true;
      dismissalService?.recordInstallation();
    };

    window.addEventListener("appinstalled", handleAppInstalled);

    return () => {
      unsubscribe?.();
      window.removeEventListener("appinstalled", handleAppInstalled);
    };
  });

  async function handleInstall() {
    if (!fullscreenService || !canInstallPWA || isInstalling) {
      return;
    }

    isInstalling = true;

    try {
      const accepted = await fullscreenService.promptInstallPWA();
      if (accepted) {
        show = false;
        dismissalService?.recordInstallation();
      }
    } catch (error) {
      console.error("Failed to install PWA:", error);
    } finally {
      isInstalling = false;
    }
  }

  function handleDismiss() {
    show = false;
    dismissalService?.recordDismissal();
  }

  function handleOpenGuide() {
    // Dispatch event to open full install guide
    window.dispatchEvent(new CustomEvent("pwa:open-install-guide"));
    show = false;
  }
</script>

{#if show && !isPWA}
  <div class="subtle-banner" transition:slide={{ duration: 300 }}>
    <div class="banner-content">
      <span class="banner-icon">
        <i class="fas fa-mobile-alt"></i>
      </span>
      <span class="banner-text"
        >Add TKA to your home screen for quick access</span
      >

      <div class="banner-actions">
        {#if canInstallPWA}
          <button
            class="install-btn"
            onclick={handleInstall}
            disabled={isInstalling}
          >
            <i class="fas fa-download"></i>
            <span>{isInstalling ? "Installing..." : "Install"}</span>
          </button>
        {:else}
          <button class="learn-btn" onclick={handleOpenGuide}>
            <i class="fas fa-info-circle"></i>
            <span>Learn How</span>
          </button>
        {/if}
        <button
          class="dismiss-btn"
          onclick={handleDismiss}
          aria-label="Dismiss"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .subtle-banner {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;

    /* Glass morphism styling matching app design */
    background: rgba(26, 26, 46, 0.92);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow:
      0 4px 24px rgba(0, 0, 0, 0.3),
      0 0 0 1px rgba(255, 255, 255, 0.05) inset;

    padding: 14px 20px;
    animation: slideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .banner-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1200px;
    margin: 0 auto;
    gap: 16px;
  }

  .banner-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.25) 0%,
      rgba(139, 92, 246, 0.25) 100%
    );
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: rgba(139, 92, 246, 1);
    font-size: 18px;
    flex-shrink: 0;
  }

  .banner-text {
    flex: 1;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.4;
    color: rgba(255, 255, 255, 0.95);
  }

  .banner-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }

  .install-btn,
  .learn-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.9) 0%,
      rgba(139, 92, 246, 0.9) 100%
    );
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  }

  .install-btn:hover,
  .learn-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 1) 0%,
      rgba(139, 92, 246, 1) 100%
    );
  }

  .install-btn:active,
  .learn-btn:active {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(99, 102, 241, 0.3);
  }

  .install-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .dismiss-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .dismiss-btn:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.95);
  }

  .dismiss-btn:active {
    transform: scale(0.95);
  }

  @keyframes slideDown {
    from {
      transform: translateY(-100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  /* Mobile optimizations */
  @media (max-width: 480px) {
    .subtle-banner {
      padding: 12px 16px;
    }

    .banner-icon {
      width: 32px;
      height: 32px;
      font-size: 16px;
    }

    .banner-text {
      font-size: 13px;
    }

    .install-btn,
    .learn-btn {
      padding: 7px 14px;
      font-size: 12px;
      gap: 5px;
    }

    .dismiss-btn {
      width: 30px;
      height: 30px;
      font-size: 13px;
    }
  }

  /* Very small screens */
  @media (max-width: 360px) {
    .subtle-banner {
      padding: 10px 12px;
    }

    .banner-content {
      gap: 12px;
    }

    .banner-icon {
      width: 28px;
      height: 28px;
      font-size: 14px;
    }

    .banner-actions {
      gap: 8px;
    }

    .install-btn,
    .learn-btn {
      padding: 6px 12px;
      font-size: 11px;
    }

    .install-btn span,
    .learn-btn span {
      display: none; /* Hide text on very small screens, show icon only */
    }

    .dismiss-btn {
      width: 28px;
      height: 28px;
    }
  }
</style>
