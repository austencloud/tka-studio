<script lang="ts">
  // Import app state management functions - BULLETPROOF RELATIVE IMPORTS
  import {
    getActiveTab,
    getSettings,
    getShowSettings,
    getShowSpotlight,
    getSpotlightSequence,
    getSpotlightThumbnailService,
    hideSpotlight,
    isTabActive,
    switchTab,
  } from "./application/state/app-state.svelte";
  // Import background types - BULLETPROOF RELATIVE IMPORTS
  import { onMount } from "svelte";
  import type { IAnimationService } from "./application/services/contracts";
  import type { IDeviceDetector } from "./device/services/contracts/IDeviceDetector";
  import type { IMobileFullscreenService } from "./mobile/services/contracts/IMobileFullscreenService";
  import { isContainerReady, resolve, TYPES } from "./inversify";
  // Import transition utilities - BULLETPROOF RELATIVE IMPORTS
  // Cross-module imports: Direct component imports (bulletproof default imports)
  import AboutTab from "../modules/about/components/AboutTab.svelte";
  import BuildTab from "../modules/build/shared/components/BuildTab.svelte";
  import SpotlightViewer from "../modules/explore/spotlight/components/SpotlightViewer.svelte";
  import LearnTab from "../modules/learn/LearnTab.svelte";
  import WordCardTab from "../modules/word-card/components/WordCardTab.svelte";
  import WriteTab from "../modules/write/components/WriteTab.svelte";
  // Shared components: Direct relative paths (bulletproof standard)
  import { ExploreTab } from "../modules";
  import FullscreenHint from "./mobile/components/FullscreenHint.svelte";
  import MobileFullscreenPrompt from "./mobile/components/MobileFullscreenPrompt.svelte";
  import EnhancedPWAInstallGuide from "./mobile/components/EnhancedPWAInstallGuide.svelte";
  import SubtleInstallBanner from "./mobile/components/SubtleInstallBanner.svelte";
  import UnifiedNavigationMenu from "./navigation/components/UnifiedNavigationMenu.svelte";
  import PrimaryNavigation from "./navigation/components/PrimaryNavigation.svelte";
  import {
    MODULE_DEFINITIONS,
    navigationState,
  } from "./navigation/state/navigation-state.svelte";
  import type { ModuleId } from "./navigation/domain/types";

  // Reactive state for template using proper derived
  let activeTab = $derived(getActiveTab());
  let isTabLoading = $derived(activeTab === null);
  let showSettings = $derived(getShowSettings());
  let settings = $derived(getSettings());
  let showSpotlight = $derived(getShowSpotlight());
  let spotlightSequence = $derived(getSpotlightSequence());
  let spotlightThumbnailService = $derived(getSpotlightThumbnailService());

  // Mobile PWA install prompt state
  let showMobileInstallPrompt = $state(false);
  let showPWAInstallGuide = $state(false);

  const INSTALL_REPROMPT_DELAY_MS = 45000;
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

    if (shouldShowInstallOverlay()) {
      showMobileInstallPrompt = true;
    } else {
      showMobileInstallPrompt = false;
    }

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

    if (typeof window !== "undefined" && fullscreenService) {
      const handleAppInstalled = () => {
        showMobileInstallPrompt = false;
        clearInstallRePromptTimer();
      };
      window.addEventListener("appinstalled", handleAppInstalled);
      cleanupFns.push(() =>
        window.removeEventListener("appinstalled", handleAppInstalled)
      );

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

    cleanupFns.push(() => clearInstallRePromptTimer());

    // Listen for custom event to open install guide
    const handleOpenInstallGuide = () => {
      showPWAInstallGuide = true;
    };
    window.addEventListener("pwa:open-install-guide", handleOpenInstallGuide);
    cleanupFns.push(() =>
      window.removeEventListener("pwa:open-install-guide", handleOpenInstallGuide)
    );

    return () => {
      cleanupFns.forEach((cleanup) => {
        try {
          cleanup();
        } catch (error) {
          console.warn(
            "Failed to clean up mobile PWA prompt listeners:",
            error
          );
        }
      });
    };
  });

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


  // Tab accessibility state - updated by BuildTab via callback
  let canAccessEditAndExportTabs = $state(false);

  // Callback for BuildTab to notify us of tab accessibility changes
  function handleTabAccessibilityChange(canAccess: boolean) {
    canAccessEditAndExportTabs = canAccess;
  }

  // Window dimensions for reactive layout tracking
  let windowInnerWidth = $state(0);
  let windowInnerHeight = $state(0);

  // Navigation layout state - updated by PrimaryNavigation
  let isPrimaryNavLandscape = $state(false);

  // Callback for PrimaryNavigation to notify us of layout changes
  function handlePrimaryNavLayoutChange(isLandscape: boolean) {
    isPrimaryNavLandscape = isLandscape;
  }

  // Resolve animation service - only when container is ready
  const animationService = $derived(() => {
    if (!isContainerReady()) {
      return null;
    }
    try {
      return resolve(TYPES.IAnimationService) as IAnimationService;
    } catch (error) {
      console.warn("Failed to resolve animation service:", error);
      return null;
    }
  });

  // Simple transition functions - animations are always enabled
  const tabOut = (node: Element) => {
    const service = animationService();
    if (!service) {
      return { duration: 250 }; // Fallback transition
    }
    return service.createFadeTransition({
      duration: 250,
    });
  };

  const tabIn = (node: Element) => {
    const service = animationService();
    if (!service) {
      return { duration: 300, delay: 250 }; // Fallback transition
    }
    return service.createFadeTransition({
      duration: 300,
      delay: 250, // Wait for out transition
    });
  };

  // App tab configuration - using correct TabId values that match content switching logic
  const allTabs = [
    { id: "construct", label: "Build", icon: "🔧", isMain: true },
    { id: "Explore", label: "Explore", icon: "🔍", isMain: true },
    { id: "learn", label: "Learn", icon: "🧠", isMain: true },
    // { id: "about", label: "About", icon: "ℹ️", isMain: true },
    { id: "word_card", label: "Word Card", icon: "🎴", isMain: false },
    { id: "write", label: "Write", icon: "✍️", isMain: false },
    { id: "animator", label: "Animator", icon: "🎯", isMain: false },
  ] as const;

  // Show all tabs (developer mode is always enabled)
  const appTabs = $derived(() => {
    // Show main tabs first, then developer tabs
    const mainTabs = allTabs.filter((tab) => tab.isMain);
    const devTabs = allTabs.filter((tab) => !tab.isMain);
    return [...mainTabs, ...devTabs];
  });

  // Developer mode is always enabled, no need for tab switching logic

  function handleTabSelect(tabId: string) {
    switchTab(
      tabId as
        | "construct"
        | "browse"
        | "word_card"
        | "write"
        | "learn"
        | "about"
        | "animator"
    );
  }

  function handleBackgroundChange(_background: string) {
    // Background change handled
  }

  // New module-based navigation state
  const currentModule = $derived(() => navigationState.currentModule);
  const currentSubMode = $derived(() => navigationState.currentSubMode);
  const currentModuleDefinition = $derived(() =>
    navigationState.getModuleDefinition(currentModule())
  );
  const currentModuleName = $derived(
    () => currentModuleDefinition()?.label || "Unknown"
  );

  // Make subModeTabs reactive to tab accessibility for build module
  const subModeTabs = $derived(() => {
    const baseTabs = currentModuleDefinition()?.subModes || [];
    const module = currentModule();

    // If we're in the build module, hide tabs that require a sequence
    if (module === "build") {
      // Filter out tabs that require a sequence when no sequence exists
      if (!canAccessEditAndExportTabs) {
        return baseTabs.filter((tab) => {
          // Only show construct and generate tabs when no sequence exists
          return tab.id === "construct" || tab.id === "generate";
        });
      }

      // When sequence exists, show all tabs
      return baseTabs;
    }

    return baseTabs;
  });

  // Module change handlers for new navigation
  function handleModuleChange(moduleId: any) {
    navigationState.setCurrentModule(moduleId);

    // Map module to tab for existing tab switching logic
    const moduleToTabMap: Record<string, string> = {
      build: "construct",
      explore: "explore",
      learn: "learn",
      write: "write",
      word_card: "word_card",
    };

    const tabId = moduleToTabMap[moduleId];
    if (tabId && activeTab !== tabId) {
      switchTab(tabId as any);
    }
  }

  function handleSubModeChange(subModeId: string) {
    navigationState.setCurrentSubMode(subModeId);
  }

  // Legacy mode change handlers for backward compatibility
  function handleBuildModeChange(mode: string) {
    navigationState.setBuildMode(mode);
    // If we're not on the construct tab, switch to it
    if (activeTab !== "construct") {
      switchTab("construct");
    }
  }

  function handleLearnModeChange(mode: string) {
    navigationState.setLearnMode(mode);
    // If we're not on the learn tab, switch to it
    if (activeTab !== "learn") {
      switchTab("learn");
    }
  }

</script>

<!-- Bind to window dimensions for reactive layout adjustments -->
<svelte:window bind:innerWidth={windowInnerWidth} bind:innerHeight={windowInnerHeight} />

<div class="main-interface" class:nav-landscape={isPrimaryNavLandscape}>
  <!-- Unified Navigation Menu - Single Floating Button -->
  <UnifiedNavigationMenu
    currentModule={currentModule()}
    currentModuleName={currentModuleName()}
    modules={MODULE_DEFINITIONS}
    onModuleChange={handleModuleChange}
  />

  <!-- Main Content Area -->
  <main
    class="content-area"
    class:about-active={isTabActive("about")}
    class:has-primary-nav={currentModule() === 'build' || currentModule() === 'learn' || currentModule() === 'explore'}
    class:nav-landscape={isPrimaryNavLandscape}
  >
    {#if isTabLoading}
      <!-- Loading state while tab is being restored -->
      <div class="tab-loading">
        <div class="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    {:else}
      <!-- App Content with reliable transitions -->
      {#key activeTab}
        <div
          class="tab-content"
          class:about-tab={isTabActive("about")}
          in:tabIn
          out:tabOut
        >
          {#if isTabActive("construct")}
            <BuildTab onTabAccessibilityChange={handleTabAccessibilityChange} />
          {:else if isTabActive("explore")}
            <ExploreTab />
          {:else if isTabActive("learn")}
            <LearnTab />
          {:else if isTabActive("word_card")}
            <WordCardTab />
          {:else if isTabActive("write")}
            <WriteTab />
          {:else if isTabActive("about")}
            <AboutTab />
          {/if}
        </div>
      {/key}
    {/if}
  </main>

  <!-- Primary Navigation (Build, Learn & Explore Modules) - Responsive Bottom/Side -->
  {#if currentModule() === 'build' || currentModule() === 'learn' || currentModule() === 'explore'}
    <PrimaryNavigation
      subModeTabs={subModeTabs()}
      currentSubMode={currentSubMode()}
      onSubModeChange={(subModeId) => {
        if (currentModule() === 'learn') {
          navigationState.setLearnMode(subModeId);
        } else if (currentModule() === 'build') {
          // Use the NEW navigation system (currentSubMode) not the legacy setBuildMode
          navigationState.setCurrentSubMode(subModeId);
        } else if (currentModule() === 'explore') {
          // Explore uses the new navigation system
          navigationState.setCurrentSubMode(subModeId);
        }
      }}
      onModuleSwitcherTap={() => {
        // Open unified menu for module switching
        const event = new CustomEvent('unified-menu-toggle');
        window.dispatchEvent(event);
      }}
      onLayoutChange={handlePrimaryNavLayoutChange}
    />
  {/if}

  <!-- Settings Dialog - REMOVED - now rendered in MainApplication.svelte to avoid duplicates -->

  <MobileFullscreenPrompt
    bind:showPrompt={showMobileInstallPrompt}
    autoShow={false}
    position="center"
    nagMode={true}
    on:dismiss={handleMobileInstallDismiss}
  />

  <!-- Subtle Fullscreen Hint -->
  <FullscreenHint />

  <!-- Tier 1: Subtle Install Banner (non-blocking) -->
  <SubtleInstallBanner />

  <!-- Enhanced PWA Install Guide (modal with device-specific instructions) -->
  <EnhancedPWAInstallGuide bind:showGuide={showPWAInstallGuide} />

  <!-- Spotlight Viewer - rendered at root level for proper z-index -->
  {#if showSpotlight && spotlightSequence && spotlightThumbnailService}
    <SpotlightViewer
      show={showSpotlight}
      sequence={spotlightSequence}
      thumbnailService={spotlightThumbnailService}
      onClose={hideSpotlight}
    />
  {/if}

</div>

<style>
  .main-interface {
    display: flex;
    flex-direction: column;
    /* Multi-layer fallback for reliable viewport height */
    height: 100vh; /* Fallback 1: Static viewport height */
    height: var(
      --viewport-height,
      100vh
    ); /* Fallback 2: JS-calculated height */
    height: 100dvh; /* Preferred: Dynamic viewport height (when it works) */
    width: 100%;
    overflow: hidden;
    position: relative;
    background: transparent;
  }

  /* Debug: Show landscape state on main interface */
  /* .main-interface.nav-landscape {
    outline: 5px solid orange !important;
    outline-offset: -5px;
  } */

  /* Allow main interface to overflow when About tab is active */
  .main-interface:has(.content-area.about-active) {
    overflow: visible !important;
    height: auto !important;
    min-height: 100vh !important;
    min-height: var(--viewport-height, 100vh) !important;
    min-height: 100dvh !important;
  }

  .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    min-height: 0;
  }

  /* Reserve space for primary navigation when present */
  .content-area.has-primary-nav {
    /* Default: Bottom padding for portrait mode (navigation at bottom) */
    padding-bottom: max(64px, env(safe-area-inset-bottom));
    padding-left: 0;
  }

  /* Landscape mode: Reserve space on the left instead of bottom */
  .content-area.has-primary-nav.nav-landscape {
    padding-bottom: 0 !important;
    padding-left: 72px !important;
    padding-left: max(72px, env(safe-area-inset-left)) !important;
  }

  .tab-content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 100%;
    height: 100%;
  }

  /* Adjust tab-content for portrait mode - navigation at bottom */
  .content-area.has-primary-nav .tab-content {
    bottom: max(64px, env(safe-area-inset-bottom));
    height: calc(100% - max(64px, env(safe-area-inset-bottom)));
  }

  /* Adjust tab-content for landscape navigation - navigation on left */
  .content-area.has-primary-nav.nav-landscape .tab-content {
    left: 72px;
    bottom: 0;
    width: calc(100% - 72px);
    height: 100%;
  }

  /* Allow scrolling for About tab */
  .content-area.about-active {
    overflow: visible !important;
  }

  .tab-content.about-tab {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    position: static !important;
    height: auto !important;
    min-height: 100% !important;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
  }

  /* Responsive design - removed empty ruleset */

  /* Disable animations when user prefers reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .main-interface,
    .tab-content {
      transition: none !important;
      animation: none !important;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .main-interface {
      border: 2px solid #667eea;
    }
  }

  /* Print styles */
  @media print {
    .main-interface {
      height: auto;
      overflow: visible;
    }

    .content-area {
      overflow: visible;
      height: auto;
    }

    .tab-content {
      position: relative;
      overflow: visible;
      height: auto;
    }
  }

  /* Loading state styles */
  .tab-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 200px;
    color: var(--text-color, #333);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border-color, #e0e0e0);
    border-top: 3px solid var(--primary-color, #007bff);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .tab-loading p {
    margin: 0;
    font-size: 14px;
    opacity: 0.7;
  }
</style>
