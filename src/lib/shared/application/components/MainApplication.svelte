<!-- Main Application Layout -->
<script lang="ts">
  import type { ISequenceService } from "../../../modules/build/shared/services/contracts";
  import {
    BackgroundCanvas,
    BackgroundType,
    updateBodyBackground,
  } from "../../background";
  import type { IDeviceDetector } from "../../device";
  import { ErrorScreen, LoadingScreen } from "../../foundation";
  import {
    ensureContainerInitialized,
    isContainerReady,
    resolve,
  } from "../../inversify";
  import { TYPES } from "../../inversify/types";
  import { ThemeService } from "../../theme";

  import type { ISettingsService } from "$shared";
  import type { Container } from "inversify";
  import { getContext, onMount } from "svelte";
  import MainInterface from "../../MainInterface.svelte";
  import SettingsSheet from "../../settings/components/SettingsSheet.svelte";
  import type { IApplicationInitializer } from "../services";
  import {
    getInitializationError,
    getInitializationProgress,
    getIsInitialized,
    getSettings,
    getShowSettings,
    hideSettingsDialog,
    initializeAppState,
    restoreApplicationState,
    setInitializationError,
    setInitializationProgress,
    setInitializationState,
    showSettingsDialog,
    switchTab,
    updateSettings,
  } from "../state";
  // Import app state management - BULLETPROOF RELATIVE IMPORTS

  // Get DI container from context
  const getContainer = getContext<() => Container | null>("di-container");

  // Services - resolved lazily
  let initService: IApplicationInitializer | null = $state(null);
  let settingsService: ISettingsService | null = $state(null);
  let sequenceService: ISequenceService | null = $state(null);
  let deviceService: IDeviceDetector | null = $state(null);
  let servicesResolved = $state(false);

  // App state
  let isInitialized = $derived(getIsInitialized());
  let initializationError = $derived(getInitializationError());
  let initializationProgress = $derived(getInitializationProgress());
  let settings = $derived(getSettings());

  // Resolve services when container is available
  $effect(() => {
    const container = getContainer?.();
    if (container && !servicesResolved) {
      try {
        // Container is guaranteed to be ready since layout waited for it
        // But we need to ensure the cached container is set
        if (!isContainerReady()) {
          console.warn(
            "Container available but not cached, ensuring initialization..."
          );
          ensureContainerInitialized().then(() => {
            // Retry service resolution after container is cached
            if (!servicesResolved) {
              try {
                initService = resolve(TYPES.IApplicationInitializer);
                settingsService = resolve(TYPES.ISettingsService);
                sequenceService = resolve(TYPES.ISequenceService);
                deviceService = resolve(TYPES.IDeviceDetector);
                servicesResolved = true;
              } catch (error) {
                console.error(
                  "Failed to resolve services after caching:",
                  error
                );
                setInitializationError(`Service resolution failed: ${error}`);
              }
            }
          });
          return;
        }

        // Use sync resolution (container already initialized and cached)
        initService = resolve(TYPES.IApplicationInitializer);
        settingsService = resolve(TYPES.ISettingsService);
        sequenceService = resolve(TYPES.ISequenceService);
        deviceService = resolve(TYPES.IDeviceDetector);

        servicesResolved = true;
      } catch (error) {
        console.error("Failed to resolve services:", error);
        setInitializationError(`Service resolution failed: ${error}`);
      }
    }
  });

  // Initialize application
  onMount(async () => {
    try {
      // Initialize the app state first
      setInitializationState(false, true, null, 0);
      setInitializationProgress(5);

      // CRITICAL: Initialize container BEFORE resolving services
      await ensureContainerInitialized();
      setInitializationProgress(15);

      await initializeAppState();
      setInitializationProgress(20);

      const container = getContainer?.();
      if (!container) {
        setInitializationError("No DI container available");
        return;
      }

      // Wait for services to be resolved
      while (!servicesResolved) {
        await new Promise((resolve) => setTimeout(resolve, 10));
      }

      // Double-check services are available
      if (
        !initService ||
        !settingsService ||
        !sequenceService ||
        !deviceService
      ) {
        setInitializationError("Services not properly resolved");
        return;
      }

      // Step 1: Restore tab state FIRST (before UI renders)
      setInitializationProgress(30);
      await restoreApplicationState();

      // Step 2: Initialize application services
      setInitializationProgress(50);
      await initService.initialize();

      // Step 3: Load settings
      setInitializationProgress(50);
      await settingsService.loadSettings();
      updateSettings(settingsService.currentSettings);

      // Step 3.5: Initialize theme service (after settings are loaded)
      setInitializationProgress(60);
      ThemeService.initialize();

      // Step 4: Initialize device detection
      setInitializationProgress(70);

      // Step 5: Load initial data
      setInitializationProgress(85);
      // TODO: Individual components should load their own data as needed

      // Step 6: Complete initialization
      setInitializationProgress(100);
      setInitializationState(true, false, null, 100);
    } catch (error) {
      console.error("❌ Application initialization failed:", error);
      setInitializationError(
        error instanceof Error ? error.message : "Unknown initialization error"
      );
    }
  });

  // Handle keyboard shortcuts
  $effect(() => {
    function handleKeydown(event: KeyboardEvent) {
      // Settings dialog toggle (Ctrl/Cmd + ,)
      if ((event.ctrlKey || event.metaKey) && event.key === ",") {
        event.preventDefault();
        if (getShowSettings()) {
          hideSettingsDialog();
        } else {
          showSettingsDialog();
        }
      }

      // Tab navigation (Ctrl/Cmd + 1-5)
      if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
          case "1":
            event.preventDefault();
            switchTab("construct");
            break;
          case "2":
            event.preventDefault();
            switchTab("browse");
            break;
          case "3":
            event.preventDefault();
            switchTab("word_card");
            break;
          case "4":
            event.preventDefault();
            switchTab("write");
            break;
          case "5":
            event.preventDefault();
            switchTab("learn");
            break;
          case "6":
            event.preventDefault();
            switchTab("animator");
            break;
        }
      }
    }

    document.addEventListener("keydown", handleKeydown);
    return () => document.removeEventListener("keydown", handleKeydown);
  });

  // Watch for background type changes and update body background immediately
  $effect(() => {
    // Debug logging removed - this runs on every reactive update
    // console.log("🔍 MainApplication $effect running, isInitialized:", isInitialized);
    // console.log("🔍 MainApplication settings:", settings);
    const backgroundType = settings.backgroundType;
    // console.log("🔍 MainApplication backgroundType from settings:", backgroundType);
    if (backgroundType && isInitialized) {
      // console.log("🎨 Background type changed in MainApplication, updating body background:", backgroundType);
      updateBodyBackground(backgroundType);
      ThemeService.updateTheme(backgroundType);
    }
  });
</script>

<svelte:head>
  <title>TKA Constructor - The Kinetic Alphabet</title>
  <meta
    name="description"
    content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for staffs, fans, and other flow arts. Create, learn, and share movement sequences."
  />
</svelte:head>

<!-- Application Container -->
<div class="tka-app" data-testid="tka-application">
  <!-- Background Canvas - Uses reactive settings -->
  {#if settings.backgroundEnabled}
    <BackgroundCanvas
      backgroundType={settings.backgroundType || BackgroundType.NIGHT_SKY}
      quality={settings.backgroundQuality || "medium"}
      backgroundColor={settings.backgroundColor}
      gradientColors={settings.gradientColors}
      gradientDirection={settings.gradientDirection}
    />
  {/if}

  {#if initializationError}
    <ErrorScreen
      error={initializationError}
      onRetry={() => window.location.reload()}
    />
  {:else if !isInitialized}
    <LoadingScreen
      progress={initializationProgress}
      message="Initializing Constructor..."
    />
  {:else}
    <!-- Main Interface -->
    <MainInterface />

    <!-- Settings slide panel -->
    <SettingsSheet isOpen={getShowSettings()} />
  {/if}
</div>

<style>
  .tka-app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    width: 100%;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    background: transparent;
    --text-color: rgba(255, 255, 255, 0.95);
    --foreground: rgba(255, 255, 255, 0.95);
    --muted-foreground: rgba(255, 255, 255, 0.7);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .tka-app {
      /* Dynamic viewport height for mobile app */
      min-height: 100dvh;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .tka-app {
      transition: none;
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .tka-app {
      --text-color: white;
      --foreground: white;
    }
  }

  /* Print styles */
  @media print {
    .tka-app {
      min-height: auto;
      overflow: visible;
    }
  }
</style>
