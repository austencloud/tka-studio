<script lang="ts">
  /**
   * MainInterface
   * Domain: Application Layout Shell
   *
   * Pure layout orchestration component.
   * Delegates all business logic to specialized managers.
   */
  import { onMount } from "svelte";
  import { getActiveTab } from "./application/state/app-state.svelte";
  // import { handleHMRInit } from "./hmr-helper"; // No longer needed
  import {
    layoutState,
    moduleHasPrimaryNav,
    setCurrentWord,
    setLearnHeader,
    setPrimaryNavHeight,
    setPrimaryNavLandscape,
    setTabAccessibility,
    setTopBarHeight,
  } from "./layout/layout-state.svelte";
  import {
    currentModule,
    currentModuleName,
    currentSection,
    handleModuleChange,
    handleSectionChange,
    getModuleDefinitions,
    moduleSections,
    navigationCoordinator,
  } from "./navigation-coordinator/navigation-coordinator.svelte";

  // Get module definitions reactively
  const moduleDefinitions = $derived(getModuleDefinitions());

  // Layout components
  import WordLabel from "../modules/create/workspace-panel/sequence-display/components/WordLabel.svelte";
  import PrimaryNavigation from "./navigation/components/PrimaryNavigation.svelte";
  import TopBar from "./navigation/components/TopBar.svelte";
  import ModuleSwitcher from "./navigation/components/ModuleSwitcher.svelte";
  import DesktopNavigationSidebar from "./navigation/components/DesktopNavigationSidebar.svelte";
  // Domain managers
  import ModuleRenderer from "./modules/ModuleRenderer.svelte";
  import PWAInstallationManager from "./pwa/PWAInstallationManager.svelte";
  import SpotlightRouter from "./spotlight/SpotlightRouter.svelte";
  import InfoModal from "./info/components/InfoModal.svelte";
  import StudioEntryAnimation from "./info/components/StudioEntryAnimation.svelte";
  import { infoUIState } from "./info/state/info-state.svelte";
  import { desktopSidebarState } from "./layout/desktop-sidebar-state.svelte";
  import {
    resolve,
    TYPES,
    type IDeviceDetector,
    type IViewportService,
  } from "$shared";
  import { useDesktopSidebarVisibility } from "./navigation/services/desktop-sidebar-visibility.svelte";
  import { explorerScrollState } from "../modules/explore/shared/state/ExplorerScrollState.svelte";

  // Reactive state
  const activeModule = $derived(getActiveTab()); // Using legacy getActiveTab for now
  const isModuleLoading = $derived(activeModule === null);
  const isAboutActive = $derived(activeModule === "about");

  // Desktop sidebar visibility management
  let desktopSidebarVisibility: ReturnType<
    typeof useDesktopSidebarVisibility
  > | null = null;
  const showDesktopSidebar = $derived(desktopSidebarState.isVisible);

  // Primary navigation visibility - only hide in Explorer module during scroll
  const isPrimaryNavVisible = $derived(
    currentModule() === "explore" ? explorerScrollState.isUIVisible : true
  );

  const createHeaderMatches = [
    "Choose Creation Mode",
    "Choose Starting Position",
    "Guided Builder",
    "Configure Your Settings",
  ];
  const createHeaderPrefixes = ["Blue Hand -", "Red Hand -"];
  const createHeaderFragments = ["Drawing", "Sequence Complete"];

  const isCreateModuleHeaderText = (
    text: string | null | undefined
  ): boolean => {
    if (!text) return false;
    const normalized = text.trim();
    if (!normalized) return false;

    if (createHeaderMatches.some((phrase) => normalized === phrase)) {
      return true;
    }

    if (createHeaderPrefixes.some((prefix) => normalized.startsWith(prefix))) {
      return true;
    }

    return createHeaderFragments.some((fragment) =>
      normalized.includes(fragment)
    );
  };

  // Sync state to coordinators
  $effect(() => {
    navigationCoordinator.canAccessEditAndExportPanels =
      layoutState.canAccessEditAndExportPanels;
  });

  onMount(() => {
    if (typeof window === "undefined") return;
    // handleHMRInit(); // Disabled - causing HMR verification loops

    // Initialize desktop sidebar visibility
    try {
      const deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      const viewportService = resolve<IViewportService>(TYPES.IViewportService);
      desktopSidebarVisibility = useDesktopSidebarVisibility(
        deviceDetector,
        viewportService
      );
    } catch (error) {
      console.warn(
        "MainInterface: Failed to initialize desktop sidebar visibility",
        error
      );
    }

    // No longer auto-opening info page - users go straight into Create module
    // Info page is now an info/resources page accessible via the info button

    return () => {
      desktopSidebarVisibility?.cleanup();
    };
  });
</script>

<div
  class="main-interface"
  class:nav-landscape={layoutState.isPrimaryNavLandscape}
  class:has-desktop-sidebar={showDesktopSidebar}
  class:about-active={isAboutActive}
  style="--top-bar-height: {layoutState.topBarHeight}px; --primary-nav-height: {layoutState.primaryNavHeight}px; --desktop-sidebar-width: {desktopSidebarState.width}px;"
>
  <!-- Module Switcher -->
  <ModuleSwitcher
    currentModule={currentModule()}
    currentModuleName={currentModuleName()}
    modules={moduleDefinitions}
    onModuleChange={handleModuleChange}
  />

  <!-- Desktop Navigation Sidebar (only on desktop in side-by-side layout) -->
  {#if showDesktopSidebar}
    <DesktopNavigationSidebar
      currentModule={currentModule()}
      currentSection={currentSection()}
      modules={moduleDefinitions}
      onModuleChange={handleModuleChange}
      onSectionChange={handleSectionChange}
    />
  {/if}

  <!-- Top Bar with Dynamic Content -->
  <TopBar
    navigationLayout={layoutState.isPrimaryNavLandscape ? "left" : "top"}
    onHeightChange={setTopBarHeight}
  >
    {#snippet content()}
      {#if currentModule() === "create" && layoutState.currentCreateWord}
        <!-- Check if it's a contextual message (not a sequence word) -->
        {#if isCreateModuleHeaderText(layoutState.currentCreateWord)}
          <div class="module-header">{layoutState.currentCreateWord}</div>
        {:else}
          <WordLabel word={layoutState.currentCreateWord} />
        {/if}
      {:else if currentModule() === "learn" && layoutState.currentLearnHeader}
        <div class="learn-header">{layoutState.currentLearnHeader}</div>
      {:else if currentModule() === "admin"}
        <div class="admin-header">
          <i class="fas fa-crown"></i>
          Admin Dashboard
        </div>
      {/if}
    {/snippet}
  </TopBar>

  <!-- Main Content Area -->
  <main
    class="content-area"
    class:about-active={isAboutActive}
    class:has-primary-nav={moduleHasPrimaryNav(currentModule()) &&
      !showDesktopSidebar}
    class:nav-hidden={!isPrimaryNavVisible}
    class:nav-landscape={layoutState.isPrimaryNavLandscape}
    class:has-top-bar={true}
  >
    <ModuleRenderer
      {activeModule}
      {isModuleLoading}
      onTabAccessibilityChange={setTabAccessibility}
      onCurrentWordChange={setCurrentWord}
      onLearnHeaderChange={setLearnHeader}
    />
  </main>

  <!-- Primary Navigation (conditionally rendered) -->
  {#if moduleHasPrimaryNav(currentModule()) && !showDesktopSidebar}
    <PrimaryNavigation
      sections={moduleSections()}
      currentSection={currentSection()}
      onSectionChange={handleSectionChange}
      onModuleSwitcherTap={() => {
        window.dispatchEvent(new CustomEvent("module-switcher-toggle"));
      }}
      onLayoutChange={setPrimaryNavLandscape}
      onHeightChange={setPrimaryNavHeight}
      isUIVisible={isPrimaryNavVisible}
    />
  {/if}

  <!-- Domain Managers -->
  <PWAInstallationManager />
  <SpotlightRouter />
  <InfoModal />

  <!-- Studio Entry Animation (first-time only) -->
  {#if infoUIState.isEnteringStudio}
    <StudioEntryAnimation />
  {/if}
</div>

<style>
  .main-interface {
    display: flex;
    flex-direction: column;
    height: 100vh;
    height: var(--viewport-height, 100vh);
    height: 100dvh;
    width: 100%;
    overflow: hidden;
    position: relative;
    background: transparent;
    transition: padding-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .main-interface.about-active {
    overflow: visible !important;
    height: auto !important;
    min-height: 100vh !important;
    min-height: var(--viewport-height, 100vh) !important;
    min-height: 100dvh !important;
  }

  /* Desktop sidebar support */
  .main-interface.has-desktop-sidebar {
    padding-left: var(--desktop-sidebar-width, 280px);
  }

  .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    min-height: 0;
  }

  .content-area.has-top-bar {
    padding-top: var(--top-bar-height, 56px);
  }

  .content-area.has-primary-nav {
    padding-bottom: var(--primary-nav-height, 64px);
    padding-left: 0;
    transition: padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .content-area.has-primary-nav.nav-landscape {
    padding-bottom: 0 !important;
    padding-left: 72px !important;
    padding-left: max(72px, env(safe-area-inset-left)) !important;
  }

  /* Reset padding when desktop sidebar is visible */
  .main-interface.has-desktop-sidebar .content-area {
    padding-left: 0 !important;
  }

  .content-area.has-top-bar.nav-landscape {
    padding-top: var(--top-bar-height, 56px);
  }

  .content-area.about-active {
    overflow: visible !important;
  }

  .module-header {
    font-size: clamp(16px, 4.5vw, 22px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
    line-height: 1.2;
    padding: 0 8px;
  }

  .learn-header {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-align: center;
  }

  .admin-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-align: center;
  }

  .admin-header i {
    color: #ffd700;
    font-size: 18px;
  }

  @media (prefers-reduced-motion: reduce) {
    .main-interface {
      transition: none !important;
      animation: none !important;
    }
  }

  @media (prefers-contrast: high) {
    .main-interface {
      border: 2px solid #667eea;
    }
  }

  @media print {
    .main-interface {
      height: auto;
      overflow: visible;
    }

    .content-area {
      overflow: visible;
      height: auto;
    }
  }
</style>
