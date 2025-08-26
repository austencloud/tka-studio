<script lang="ts">
  // Import app state management functions
  import {
    getActiveTab,
    getSettings,
    getShowSettings,
    isTabActive,
    switchTab,
  } from "$lib/state/app-state.svelte";
  // Import background types
  import { BackgroundType } from "./backgrounds/types/types";

  // Import transition utilities
  import { fade } from "$lib/utils/simple-fade";

  // Import components - App Interface
  import BackgroundCanvas from "./backgrounds/BackgroundCanvas.svelte";
  import BackgroundProvider from "./backgrounds/BackgroundProvider.svelte";
  import NavigationBar from "./navigation/NavigationBar.svelte";
  import SettingsDialog from "./SettingsDialog.svelte";
  import AboutTab from "./tabs/about-tab/AboutTab.svelte";
  import BrowseTab from "./tabs/browse-tab/BrowseTab.svelte";
  import ConstructTab from "./tabs/build-tab/BuildTab.svelte";
  import LearnTab from "./tabs/learn-tab/LearnTab.svelte";
  import MotionTesterTab from "./tabs/motion-tester-tab/MotionTesterTab.svelte";
  import SequenceCardTab from "./tabs/sequence_card/SequenceCardTab.svelte";
  import WriteTab from "./tabs/write-tab/WriteTab.svelte";

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
    { id: "construct", label: "Construct", icon: "🔧", isMain: true },
    { id: "browse", label: "Browse", icon: "🔍", isMain: true },
    { id: "learn", label: "Learn", icon: "🧠", isMain: true },
    { id: "about", label: "About", icon: "ℹ️", isMain: true },
    { id: "sequence_card", label: "Sequence Card", icon: "🎴", isMain: false },
    { id: "write", label: "Write", icon: "✍️", isMain: false },
    { id: "motion-tester", label: "Motion Tester", icon: "🎯", isMain: false },
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
        | "motion-tester"
    );
  }

  function handleBackgroundChange(background: string) {
    // Background change handled
  }
</script>

<BackgroundProvider>
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
    <main class="content-area">
      <!-- App Content with reliable transitions -->
      {#key activeTab}
        <div class="tab-content" in:tabIn out:tabOut>
          {#if isTabActive("construct")}
            <ConstructTab />
          {:else if isTabActive("browse")}
            <BrowseTab />
          {:else if isTabActive("sequence_card")}
            <SequenceCardTab />
          {:else if isTabActive("write")}
            <WriteTab />
          {:else if isTabActive("learn")}
            <LearnTab />
          {:else if isTabActive("motion-tester")}
            <MotionTesterTab />
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
</BackgroundProvider>

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
