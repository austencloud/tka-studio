<!--
  ModuleSwitcher - Module Navigation Drawer

  A standardized drawer component for switching between app modules.
  Uses the shared Drawer component (vaul-svelte based) for consistent UX.
-->
<script lang="ts">
  import type {
    IHapticFeedbackService,
    IMobileFullscreenService,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { Drawer } from "$shared";
  import { onMount } from "svelte";
  import type { ModuleDefinition, ModuleId } from "../domain/types";
  import ModuleList from "./ModuleList.svelte";
  import InstallPromptButton from "./InstallPromptButton.svelte";

  let {
    // Current state
    currentModule,
    currentModuleName,

    // Available options
    modules = [],

    // Callbacks
    onModuleChange,
  } = $props<{
    currentModule: ModuleId;
    currentModuleName: string;
    modules: ModuleDefinition[];
    onModuleChange?: (moduleId: ModuleId) => void;
  }>();

  let hapticService: IHapticFeedbackService;
  let fullscreenService: IMobileFullscreenService;
  let isOpen = $state(false);

  // PWA install state
  let showInstallOption = $state(false);
  let canUseNativeInstall = $state(false);

  function closeDrawer() {
    hapticService?.trigger("selection");
    isOpen = false;
  }

  function openDrawer() {
    hapticService?.trigger("selection");
    isOpen = true;
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    fullscreenService = resolve<IMobileFullscreenService>(
      TYPES.IMobileFullscreenService
    );

    // Check if PWA install should be shown
    try {
      const isPWA = fullscreenService?.isPWA?.() ?? false;

      // Only show install option if not already installed as PWA
      if (!isPWA) {
        showInstallOption = true;
        canUseNativeInstall = fullscreenService?.canInstallPWA?.() ?? false;

        // Listen for install prompt availability
        const unsubscribe = fullscreenService?.onInstallPromptAvailable?.(
          (available: boolean) => {
            canUseNativeInstall = available;
          }
        );

        // Listen for app installation
        const handleAppInstalled = () => {
          showInstallOption = false;
        };
        window.addEventListener("appinstalled", handleAppInstalled);

        return () => {
          unsubscribe?.();
          window.removeEventListener("appinstalled", handleAppInstalled);
        };
      }
    } catch (error) {
      console.warn("Failed to check PWA install status:", error);
    }

    return undefined;
  });

  function handleModuleSelect(moduleId: ModuleId) {
    onModuleChange?.(moduleId);
    closeDrawer();
  }

  function handleInstallClose() {
    closeDrawer();
  }

  // Listen for custom event from primary navigation
  onMount(() => {
    const handleToggleEvent = () => {
      if (isOpen) {
        closeDrawer();
      } else {
        openDrawer();
      }
    };
    window.addEventListener("module-switcher-toggle", handleToggleEvent);

    return () => {
      window.removeEventListener("module-switcher-toggle", handleToggleEvent);
    };
  });
</script>

<!-- Drawer Component -->
<Drawer
  bind:isOpen
  ariaLabel="Module navigation menu"
  class="module-switcher-drawer"
  backdropClass="module-switcher-backdrop"
  showHandle={true}
  closeOnBackdrop={true}
>
  <div class="module-switcher-container">
    <!-- Header -->
    <div class="module-switcher-header">
      <div class="header-content">
        <h2>Navigation</h2>
        <div class="current-location">
          <span class="module-name">{currentModuleName}</span>
        </div>
      </div>
      <button class="close-button" onclick={closeDrawer} aria-label="Close menu">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- Content -->
    <div class="module-switcher-content">
      <!-- Module Selection -->
      <ModuleList
        {currentModule}
        {modules}
        onModuleSelect={handleModuleSelect}
      />

      <!-- App Actions Section -->
      <section class="menu-section">
        <div class="menu-items">
          {#if showInstallOption}
            <InstallPromptButton
              {canUseNativeInstall}
              onInstall={handleInstallClose}
            />
          {/if}
        </div>
      </section>
    </div>
  </div>
</Drawer>

<style>
  /* ============================================================================
     DRAWER STYLING
     ============================================================================ */
  :global(.module-switcher-drawer) {
    --sheet-max-height: calc(100vh - 1px) !important;
    max-height: calc(100vh - 1px) !important;
    height: calc(100vh - 1px) !important;
    --sheet-width: 100%;
    --sheet-bg: rgba(26, 26, 46, 0.95);
    --sheet-filter: blur(24px);
    --sheet-border: 1px solid rgba(255, 255, 255, 0.15);
    --sheet-radius-large: 24px;
    box-sizing: border-box !important;
  }

  :global(.module-switcher-backdrop) {
    --sheet-backdrop-bg: rgba(0, 0, 0, 0.6);
    --sheet-backdrop-filter: blur(8px);
  }

  /* Sheet content - ensure proper z-index */
  :global(.drawer-content.module-switcher-drawer) {
    z-index: 1100 !important;
  }

  /* CRITICAL: Disable overflow on drawer-inner to allow swipe-to-dismiss */
  :global(.drawer-content.module-switcher-drawer .drawer-inner) {
    overflow-y: visible !important;
  }

  /* ============================================================================
     CONTAINER
     ============================================================================ */
  .module-switcher-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    max-height: 100%;
    /* NO overflow: hidden - let child elements handle scrolling for drag gestures */
  }

  /* ============================================================================
     HEADER
     ============================================================================ */
  .module-switcher-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 16px 24px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
    gap: 16px;
  }

  .header-content {
    flex: 1;
    min-width: 0;
  }

  .module-switcher-header h2 {
    margin: 0 0 8px 0;
    font-size: 22px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: -0.02em;
  }

  .current-location {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    flex-wrap: wrap;
  }

  .module-name {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
  }

  /* Close button */
  .close-button {
    width: 44px; /* iOS/Android minimum touch target */
    height: 44px;
    border-radius: 50%; /* Consistent circular style */
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.95);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  /* ============================================================================
     CONTENT
     ============================================================================ */
  .module-switcher-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 16px;
    min-height: 0;

    /* Smooth scrolling */
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;

    /* Scrollbar styling */
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
  }

  .module-switcher-content::-webkit-scrollbar {
    width: 8px;
  }

  .module-switcher-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .module-switcher-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .module-switcher-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Menu sections */
  .menu-section {
    margin-bottom: 24px;
  }

  .menu-section:last-child {
    margin-bottom: 0;
  }

  .menu-items {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  /* ============================================================================
     RESPONSIVE ADJUSTMENTS
     ============================================================================ */
  @media (max-width: 500px) {
    .module-switcher-header {
      padding: 12px 20px;
    }

    .module-switcher-header h2 {
      font-size: 20px;
    }

    .module-switcher-content {
      padding: 12px;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .close-button {
      transition: none;
    }

    .close-button:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    :global(.module-switcher-drawer) {
      --sheet-bg: rgba(0, 0, 0, 0.98);
      --sheet-border: 2px solid white;
    }

    .close-button {
      background: rgba(255, 255, 255, 0.95);
      border: 2px solid white;
      color: black;
    }
  }
</style>
