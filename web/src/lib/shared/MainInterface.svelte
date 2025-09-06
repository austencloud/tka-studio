<script lang="ts">
  // Import app state management functions - BULLETPROOF RELATIVE IMPORTS
  import {
    getActiveTab,
    getSettings,
    getShowSettings,
    isTabActive,
    switchTab,
  } from "./state/app-state.svelte";
  // Import background types - BULLETPROOF RELATIVE IMPORTS
  import { BackgroundType } from "./domain/ui/backgrounds/BackgroundTypes";

  // Import transition utilities - BULLETPROOF RELATIVE IMPORTS
  import { fade } from "./utils/simple-fade";

  // Cross-module imports: Direct component imports (bulletproof default imports)
  import AboutTab from "../modules/about/components/AboutTab.svelte";
  import AnimatorTab from "../modules/animator/components/AnimatorTab.svelte";
  import BrowseTab from "../modules/browse/shared/components/BrowseTab.svelte";
  import BuildTab from "../modules/build/shared/components/BuildTab.svelte";
  import LearnTab from "../modules/learn/quiz/components/LearnTab.svelte";
  import WordCardTab from "../modules/word-card/components/WordCardTab.svelte";
  import WriteTab from "../modules/write/components/WriteTab.svelte";
  // Shared components: Direct relative paths (bulletproof standard)
  import BackgroundCanvas from "./background/components/BackgroundCanvas.svelte";
  import NavigationBar from "./navigation/components/NavigationBar.svelte";
  import SettingsDialog from "./settings/components/SettingsDialog.svelte";

  // Reactive state for template using proper derived
  let activeTab = $derived(getActiveTab());
  let showSettings = $derived(getShowSettings());
  let settings = $derived(getSettings());

  // Simple transition functions that respect animation settings
  const tabOut = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return fade(node, {
      duration: animationsEnabled ? 250 : 0,
    });
  };

  const tabIn = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return fade(node, {
      duration: animationsEnabled ? 300 : 0,
      delay: animationsEnabled ? 250 : 0, // Wait for out transition
    });
  };

  // App tab configuration
  const allTabs = [
    { id: "build", label: "Build", icon: "🔧", isMain: true },
    { id: "browse", label: "Browse", icon: "🔍", isMain: true },
    { id: "learn", label: "Learn", icon: "🧠", isMain: true },
    { id: "about", label: "About", icon: "ℹ️", isMain: true },
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
        | "word-card"
        | "write"
        | "learn"
        | "about"
        | "animator"
    );
  }

  function handleBackgroundChange(_background: string) {
    // Background change handled
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
  />

  <!-- Main Content Area -->
  <main class="content-area" class:about-active={isTabActive("about")}>
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
        {:else if isTabActive("browse")}
          <BrowseTab />
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
  </main>

  <!-- Settings Dialog - moved inside BackgroundProvider -->
  {#if showSettings}
    <SettingsDialog />
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
    overflow: visible;
  }

  .tab-content.about-tab {
    overflow-y: auto;
    overflow-x: hidden;
    position: static;
    height: auto;
    min-height: 100%;
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
</style>
