<!--
  Unified Navigation Menu - Slide-Up Panel Approach

  Displays a single floating menu button that opens a modern slide-up panel
  focused on module switching and context:
  - Highlights the active module + mode
  - Lists all available modules
  - Provides quick access to Settings

  Uses 2025 UX trend: slide-up panel (bottom sheet) instead of center modal.
-->
<script lang="ts">
  import type { IHapticFeedbackService, IMobileFullscreenService, IGestureService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ModuleDefinition, ModuleId } from "../domain/types";
  import { slideTransition, fadeTransition } from "$shared/utils";
  import ModuleList from "./ModuleList.svelte";
  import InstallPromptButton from "./InstallPromptButton.svelte";
  import SettingsMenuItem from "./SettingsMenuItem.svelte";

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
  let gestureService: IGestureService;
  let showMenu = $state(false);
  let panelElement: HTMLDivElement | undefined = $state(undefined);
  let contentHeight = $state(0);

  // PWA install state
  let showInstallOption = $state(false);
  let canUseNativeInstall = $state(false);

  function closeMenu() {
    showMenu = false;
  }

  // Setup gesture handler for swipe-to-dismiss
  let gestureHandler = $state<ReturnType<IGestureService['createSwipeGestureHandler']>>();

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    fullscreenService = resolve<IMobileFullscreenService>(
      TYPES.IMobileFullscreenService
    );
    gestureService = resolve<IGestureService>(
      TYPES.IGestureService
    );

    // Initialize gesture handler
    gestureHandler = gestureService.createSwipeGestureHandler({
      direction: 'vertical',
      dismissOrientation: 'down',
      threshold: 100,
      onDismiss: () => closeMenu(),
      onDrag: (delta) => gestureService.applyDragTransform(panelElement ?? null, delta, 'vertical'),
      onSnapBack: () => gestureService.snapBackTransform(panelElement ?? null, 'vertical'),
    });

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
  });

  // Reactively measure content height when panel is shown
  $effect(() => {
    if (showMenu && panelElement) {
      // Wait for next frame to ensure content is rendered
      requestAnimationFrame(() => {
        const panel = panelElement;
        if (panel) {
          const scrollHeight = panel.scrollHeight;
          const viewportHeight = window.innerHeight;
          const maxHeight = viewportHeight * 0.9; // 90% of viewport
          const safeAreaBottom = parseInt(
            getComputedStyle(document.documentElement).getPropertyValue(
              "--safe-area-inset-bottom"
            ) || "0"
          );

          // Use the smaller of content height or 90vh
          contentHeight = Math.min(scrollHeight + safeAreaBottom, maxHeight);
        }
      });
    }
  });

  function toggleMenu() {
    hapticService?.trigger("navigation");
    showMenu = !showMenu;
  }

  function handleBackdropClick() {
    closeMenu();
  }

  function handleModuleSelect(moduleId: ModuleId) {
    onModuleChange?.(moduleId);
    closeMenu();
  }

  function handleSettingsClose() {
    closeMenu();
  }

  function handleInstallClose() {
    closeMenu();
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && showMenu) {
      closeMenu();
    }
  }

  $effect(() => {
    if (showMenu) {
      document.addEventListener("keydown", handleKeydown);
      return () => document.removeEventListener("keydown", handleKeydown);
    }
  });
</script>

<!-- Floating Menu Button -->
<button
  class="floating-menu-button glass-surface"
  onclick={toggleMenu}
  aria-label="Open navigation menu"
  aria-expanded={showMenu}
>
  <i class="fas fa-bars"></i>
</button>

<!-- Slide-Up Navigation Panel -->
{#if showMenu}
  <!-- Backdrop -->
  <div
    class="sheet-backdrop"
    onclick={handleBackdropClick}
    transition:fadeTransition
    role="presentation"
  ></div>

  <!-- Menu Panel -->
  <div
    bind:this={panelElement}
    class="menu-sheet glass-surface"
    style:height={contentHeight > 0 ? `${contentHeight}px` : "auto"}
    transition:slideTransition
    role="dialog"
    aria-label="Navigation menu"
    tabindex="-1"
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    ontouchstart={gestureHandler?.handleTouchStart}
    ontouchmove={gestureHandler?.handleTouchMove}
    ontouchend={gestureHandler?.handleTouchEnd}
  >
    <!-- Handle bar for swipe affordance -->
    <div class="sheet-handle"></div>

    <!-- Header -->
    <div class="sheet-header">
      <div class="header-content">
        <h2>Navigation</h2>
        <div class="current-location">
          <span class="module-name">{currentModuleName}</span>
        </div>
      </div>
      <button class="close-button" onclick={closeMenu} aria-label="Close menu">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div class="menu-scroll">
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

          <SettingsMenuItem onSettingsClick={handleSettingsClose} />
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  /* ============================================================================
     FLOATING MENU BUTTON
     ============================================================================ */
  .floating-menu-button {
    position: fixed;
    z-index: 200;
    left: 6px;
    top: 6px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: var(--glass-backdrop-strong);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: rgba(255, 255, 255, 0.9);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .floating-menu-button:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
  }

  .floating-menu-button:active {
    transform: scale(0.95);
  }



  /* ============================================================================
     SLIDE-UP PANEL (BOTTOM SHEET)
     ============================================================================ */
  .sheet-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    z-index: 250;
    transform: translateZ(0);
  }

  .menu-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 90vh;
    max-height: 90dvh;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: var(--glass-backdrop-strong, blur(20px));
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 251;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding-bottom: env(safe-area-inset-bottom);
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.4),
      0 -2px 8px rgba(0, 0, 0, 0.2);
    transform: translateZ(0);
    will-change: transform;
    touch-action: pan-y;
  }

  /* Handle bar */
  .sheet-handle {
    width: 48px;
    height: 5px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    margin: 12px auto 8px;
    flex-shrink: 0;
    cursor: grab;
    transition: background 0.2s ease;
  }

  .sheet-handle:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Header */
  .sheet-header {
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

  .sheet-header h2 {
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
    width: 36px;
    height: 36px;
    border-radius: 8px;
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

  /* Scrollable content */
  .menu-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
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
    .sheet-header {
      padding: 12px 20px;
    }

    .sheet-header h2 {
      font-size: 20px;
    }

    .menu-scroll {
      padding: 12px;
    }
  }

  /* ============================================================================
     ACCESSIBILITY
     ============================================================================ */
  @media (prefers-reduced-motion: reduce) {
    .floating-menu-button,
    .close-button,
    .sheet-handle {
      transition: none;
    }

    .floating-menu-button:hover,
    .floating-menu-button:active,
    .close-button:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .floating-menu-button {
      background: rgba(0, 0, 0, 0.95);
      border: 2px solid white;
    }

    .menu-sheet {
      background: rgba(0, 0, 0, 0.98);
      border-top: 2px solid white;
    }
  }
</style>
