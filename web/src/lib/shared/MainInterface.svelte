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
  import { BackgroundType } from "$shared";
  import type { IAnimationService } from "./application/services/contracts";
  import { resolve, TYPES } from "./inversify";
// Import transition utilities - BULLETPROOF RELATIVE IMPORTS
  // Cross-module imports: Direct component imports (bulletproof default imports)
  import AboutTab from "../modules/about/components/AboutTab.svelte";
  import AnimatorTab from "../modules/animator/components/AnimatorTab.svelte";
  import BuildTab from "../modules/build/shared/components/BuildTab.svelte";
  import SpotlightViewer from "../modules/gallery/spotlight/components/SpotlightViewer.svelte";
  import LearnTab from "../modules/learn/LearnTab.svelte";
  import WordCardTab from "../modules/word-card/components/WordCardTab.svelte";
  import WriteTab from "../modules/write/components/WriteTab.svelte";
// Shared components: Direct relative paths (bulletproof standard)
  import { GalleryTab } from "../modules";
  import BackgroundCanvas from "./background/shared/components/BackgroundCanvas.svelte";
  import NavigationBar from "./navigation/components/NavigationBar.svelte";
  import { navigationState } from "./navigation/state/navigation-state.svelte";
  import SettingsDialog from "./settings/components/SettingsDialog.svelte";

  // Reactive state for template using proper derived
  let activeTab = $derived(getActiveTab());
  let isTabLoading = $derived(activeTab === null);
  let showSettings = $derived(getShowSettings());
  let settings = $derived(getSettings());
  let showSpotlight = $derived(getShowSpotlight());
  let spotlightSequence = $derived(getSpotlightSequence());
  let spotlightThumbnailService = $derived(getSpotlightThumbnailService());

  // Resolve animation service
  const animationService = resolve(
    TYPES.IAnimationService
  ) as IAnimationService;

  // Simple transition functions that respect animation settings
  const tabOut = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return animationService.createFadeTransition({
      duration: animationsEnabled ? 250 : 0,
    });
  };

  const tabIn = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return animationService.createFadeTransition({
      duration: animationsEnabled ? 300 : 0,
      delay: animationsEnabled ? 250 : 0, // Wait for out transition
    });
  };

  // App tab configuration - using correct TabId values that match content switching logic
  const allTabs = [
    { id: "construct", label: "Build", icon: "🔧", isMain: true },
    { id: "gallery", label: "Gallery", icon: "🔍", isMain: true },
    { id: "learn", label: "Learn", icon: "🧠", isMain: true },
    // { id: "about", label: "About", icon: "ℹ️", isMain: true },
    { id: "sequence_card", label: "Word Card", icon: "🎴", isMain: false },
    { id: "write", label: "Write", icon: "✍️", isMain: false },
    { id: "animator", label: "Animator", icon: "🎯", isMain: false },
  ] as const;

  // Filter tabs based on developer mode
  const appTabs = $derived(() => {
    if (settings.developerMode) {
      // In developer mode, show main tabs first, then developer tabs
      const mainTabs = allTabs.filter((tab) => tab.isMain);
      const devTabs = allTabs.filter((tab) => !tab.isMain);
      return [...mainTabs, ...devTabs];
    } else {
      // In consumer mode, only show main tabs
      return allTabs.filter((tab) => tab.isMain);
    }
  });

  // Handle developer mode changes - if user is on a dev tab and switches to consumer mode,
  // redirect them to a main tab (but not during initial app load/restoration)
  let hasInitialRestoreCompleted = false;

  $effect(() => {
    // Skip the first run to allow tab restoration to complete
    if (!hasInitialRestoreCompleted) {
      hasInitialRestoreCompleted = true;
      return;
    }

    if (!settings.developerMode) {
      const currentTabIsMain = allTabs.find(
        (tab) => tab.id === activeTab
      )?.isMain;
      if (currentTabIsMain === false) {
        // User is on a developer tab but developer mode is disabled
        // Switch to the default main tab (construct)
        switchTab("construct");
      }
    }
  });

  function handleTabSelect(tabId: string) {
    switchTab(
      tabId as
        | "construct"
        | "browse"
        | "sequence_card"
        | "write"
        | "learn"
        | "about"
        | "animator"
    );
  }

  function handleBackgroundChange(_background: string) {
    // Background change handled
  }

  // Mode change handlers for dropdown navigation
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

<div class="main-interface">
  <!-- Background Canvas -->
  {#if settings.backgroundEnabled}
    <BackgroundCanvas
      backgroundType={settings.backgroundType || BackgroundType.NIGHT_SKY}
      quality={settings.backgroundQuality || "medium"}
    />
  {/if}

  <!-- Navigation Bar -->
  <NavigationBar
    tabs={appTabs()}
    {activeTab}
    onTabSelect={handleTabSelect}
    onBackgroundChange={handleBackgroundChange}
    buildModes={navigationState.buildModes}
    currentBuildMode={navigationState.currentBuildMode}
    onBuildModeChange={handleBuildModeChange}
    learnModes={navigationState.learnModes}
    currentLearnMode={navigationState.currentLearnMode}
    onLearnModeChange={handleLearnModeChange}
  />

  <!-- Main Content Area -->
  <main class="content-area" class:about-active={isTabActive("about")}>
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
            <BuildTab />
          {:else if isTabActive("gallery")}
            <GalleryTab />
          {:else if isTabActive("sequence_card")}
            <WordCardTab />
          {:else if isTabActive("write")}
            <WriteTab />
          {:else if isTabActive("learn")}
            <LearnTab />
          {:else if isTabActive("animator")}
            <AnimatorTab />
          {:else if isTabActive("about")}
            <AboutTab />
          {/if}
        </div>
      {/key}
    {/if}
  </main>

  <!-- Settings Dialog - moved inside BackgroundProvider -->
  {#if showSettings && settings}
    <SettingsDialog />
  {/if}

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
    height: 100vh;
    width: 100%;
    overflow: hidden;
    position: relative;
    transition: all 0.3s ease;
    background: transparent;
  }

  /* Allow main interface to overflow when About tab is active */
  .main-interface:has(.content-area.about-active) {
    overflow: visible !important;
    height: auto !important;
    min-height: 100vh !important;
  }

  .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
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

  /* Responsive design */
  @media (max-width: 768px) {
    .main-interface {
      height: 100vh;
      height: 100dvh; /* Dynamic viewport height for mobile */
    }
  }

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
