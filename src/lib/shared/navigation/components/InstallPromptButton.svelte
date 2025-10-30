<!--
  InstallPromptButton - PWA Installation UI Component

  Displays a button to install the app as a PWA or show installation guide.
  Handles both native install prompts and fallback to instruction guide.
-->
<script lang="ts">
  import type { IHapticFeedbackService, IMobileFullscreenService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    canUseNativeInstall = false,
    onInstall,
  } = $props<{
    canUseNativeInstall?: boolean;
    onInstall?: () => void;
  }>();

  let hapticService: IHapticFeedbackService;
  let fullscreenService: IMobileFullscreenService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    fullscreenService = resolve<IMobileFullscreenService>(
      TYPES.IMobileFullscreenService
    );
  });

  async function handleInstallClick() {
    hapticService?.trigger("selection");

    try {
      await fullscreenService?.handleInstallRequest();
      onInstall?.();
    } catch (error) {
      console.error("Failed to handle install request:", error);
    }
  }
</script>

<button class="install-button" onclick={handleInstallClick}>
  <span class="item-icon install-icon">
    <i class="fas fa-plus-circle"></i>
  </span>
  <div class="item-info">
    <span class="item-label">
      {canUseNativeInstall ? "Install App" : "Add to Home Screen"}
    </span>
    <span class="item-description">
      {canUseNativeInstall
        ? "Install for fullscreen experience"
        : "Learn how to install"}
    </span>
  </div>
</button>

<style>
  .install-button {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 12px;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.15) 0%,
      rgba(139, 92, 246, 0.15) 100%
    );
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    min-height: 56px;
    width: 100%;
  }

  .install-button:hover {
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.25) 0%,
      rgba(139, 92, 246, 0.25) 100%
    );
    border-color: rgba(99, 102, 241, 0.5);
    transform: translateX(4px);
  }

  .install-button:active {
    transform: translateX(4px) scale(0.98);
  }

  .item-icon {
    font-size: 24px;
    width: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .install-icon {
    color: rgba(139, 92, 246, 1);
  }

  .item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .item-label {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .item-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.3;
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .install-button {
      transition: none;
    }

    .install-button:hover,
    .install-button:active {
      transform: none;
    }
  }
</style>
