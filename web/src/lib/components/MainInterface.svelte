<script lang="ts">
  // Import app state management functions
  import {
    getActiveTab,
    getSettings,
    getShowSettings,
    isTabActive,
    switchTab,
  } from "$lib/state/appState.svelte";

  // Import transition utilities
  import { fade } from "$lib/utils/simpleFade";

  // Import components - App Interface
  import BackgroundCanvas from "./backgrounds/BackgroundCanvas.svelte";
  import BackgroundProvider from "./backgrounds/BackgroundProvider.svelte";
  import NavigationBar from "./navigation/NavigationBar.svelte";
  import SettingsDialog from "./SettingsDialog.svelte";
  import BrowseTab from "./tabs/BrowseTab.svelte";
  import ConstructTab from "./tabs/ConstructTab.svelte";
  import LearnTab from "./tabs/LearnTab.svelte";
  import SequenceCardTab from "./tabs/SequenceCardTab.svelte";
  import WriteTab from "./tabs/WriteTab.svelte";
  import AboutTab from "./tabs/AboutTab.svelte";
  import MotionTesterTab from "./tabs/MotionTesterTab.svelte";
  import ArrowDebugTab from "./tabs/ArrowDebugTab.svelte";

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
    { id: "arrow-debug", label: "Arrow Debug", icon: "🏹", isMain: false },
  ] as const;

  // Filter tabs based on developer mode
  const appTabs = $derived(() => {
    console.log(
      "🔄 AppTabs derived function called, developerMode:",
      settings.developerMode
    );
    console.log(
      "🔄 All available tabs:",
      allTabs.map((t) => ({ id: t.id, label: t.label, isMain: t.isMain }))
    );

    if (settings.developerMode) {
      // In developer mode, show main tabs first, then developer tabs
      const mainTabs = allTabs.filter((tab) => tab.isMain);
      const devTabs = allTabs.filter((tab) => !tab.isMain);
      const result = [...mainTabs, ...devTabs];
      console.log(
        "🔧 Developer mode ON - showing tabs:",
        result.map((t) => t.label)
      );
      return result;
    } else {
      // In consumer mode, only show main tabs
      const result = allTabs.filter((tab) => tab.isMain);
      console.log(
        "👤 Consumer mode ON - showing tabs:",
        result.map((t) => t.label)
      );
      return result;
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
        console.log(
          `🔄 Developer mode disabled, switching from ${activeTab} to construct`
        );
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
        | "arrow-debug"
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
        backgroundType={settings.backgroundType === "auroraBorealis" ||
        settings.backgroundType === "starfield"
          ? "aurora"
          : settings.backgroundType || "aurora"}
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
          {:else if isTabActive("arrow-debug")}
            <ArrowDebugTab />
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
