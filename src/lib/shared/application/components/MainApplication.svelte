<!-- Main Application Layout -->
<script lang="ts">
  import type { ISequenceService } from "../../../modules/build/shared/services/contracts";
  import {
    BackgroundCanvas,
    BackgroundType,
    updateBodyBackground,
  } from "../../background";
  import type { IDeviceDetector } from "../../device";
  import { ErrorScreen } from "../../foundation";
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
    getIsInitialized,
    getSettings,
    getShowSettings,
    hideSettingsDialog,
    initializeAppState,
    restoreApplicationState,
    setInitializationError,
    setInitializationState,
    showSettingsDialog,
    switchTab,
    updateSettings,
  } from "../state";
  import { getCurrentSheet, onSheetChange, closeSheet, openSheet } from "../../navigation/utils/sheet-router";
  import type { SheetType } from "../../navigation/utils/sheet-router";
  import ProfileSettingsSheet from "../../navigation/components/ProfileSettingsSheet.svelte";
  import AuthSheet from "../../navigation/components/AuthSheet.svelte";
  import TermsSheet from "../../navigation/components/TermsSheet.svelte";
  import PrivacySheet from "../../navigation/components/PrivacySheet.svelte";
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
  let settings = $derived(getSettings());

  // Route-based sheet state
  let currentSheetType = $state<SheetType>(null);
  let showProfileSettings = $derived(() => currentSheetType === 'profile-settings');
  let showRouteBasedSettings = $derived(() => currentSheetType === 'settings');
  let showAuthSheet = $derived(() => currentSheetType === 'auth');
  let showTermsSheet = $derived(() => currentSheetType === 'terms');
  let showPrivacySheet = $derived(() => currentSheetType === 'privacy');

  // Resolve services when container is available
  $effect(() => {
    console.log('[DEBUG-MAIN] 🔧 Service resolution $effect triggered');
    const container = getContainer?.();
    console.log('[DEBUG-MAIN] Container from context:', container ? 'valid' : 'null', 'servicesResolved:', servicesResolved);

    if (container && !servicesResolved) {
      try {
        // Container is guaranteed to be ready since layout waited for it
        // But we need to ensure the cached container is set
        if (!isContainerReady()) {
          console.warn(
            "[DEBUG-MAIN] ⚠️ Container available but not cached, ensuring initialization..."
          );
          ensureContainerInitialized().then(() => {
            // Retry service resolution after container is cached
            if (!servicesResolved) {
              try {
                console.log('[DEBUG-MAIN] 🔄 Retrying service resolution after container cache...');
                initService = resolve(TYPES.IApplicationInitializer);
                settingsService = resolve(TYPES.ISettingsService);
                sequenceService = resolve(TYPES.ISequenceService);
                deviceService = resolve(TYPES.IDeviceDetector);
                servicesResolved = true;
                console.log('[DEBUG-MAIN] ✅ Services resolved successfully (after cache)');
              } catch (error) {
                console.error(
                  "[DEBUG-MAIN] ❌ Failed to resolve services after caching:",
                  error
                );
                setInitializationError(`Service resolution failed: ${error}`);
              }
            }
          });
          return;
        }

        console.log('[DEBUG-MAIN] 🚀 Resolving services synchronously...');
        // Use sync resolution (container already initialized and cached)
        initService = resolve(TYPES.IApplicationInitializer);
        settingsService = resolve(TYPES.ISettingsService);
        sequenceService = resolve(TYPES.ISequenceService);
        deviceService = resolve(TYPES.IDeviceDetector);

        servicesResolved = true;
        console.log('[DEBUG-MAIN] ✅ Services resolved successfully');
      } catch (error) {
        console.error("[DEBUG-MAIN] ❌ Failed to resolve services:", error);
        setInitializationError(`Service resolution failed: ${error}`);
      }
    }
  });

  // Initialize application
  onMount(async () => {
    console.log('[DEBUG-MAIN] 🏁 MainApplication onMount called');

    // Set up route-based sheet listening
    currentSheetType = getCurrentSheet();

    const cleanupSheetListener = onSheetChange((sheetType) => {
      currentSheetType = sheetType;

      // Sync with legacy settings dialog state
      if (sheetType === 'settings') {
        // Opening settings via route
        if (!getShowSettings()) {
          showSettingsDialog();
        }
      } else if (sheetType === null && getShowSettings()) {
        // Closing settings via back button
        hideSettingsDialog();
      }
    });

    try {
      console.log('[DEBUG-MAIN] 📊 Initializing app state...');
      // Initialize the app state first
      setInitializationState(false, true, null, 0);

      console.log('[DEBUG-MAIN] 🔧 Ensuring container initialized...');
      // CRITICAL: Initialize container BEFORE resolving services
      await ensureContainerInitialized();
      console.log('[DEBUG-MAIN] ✅ Container initialization confirmed');

      console.log('[DEBUG-MAIN] 📊 Initializing app state...');
      await initializeAppState();
      console.log('[DEBUG-MAIN] ✅ App state initialized');

      const container = getContainer?.();
      console.log('[DEBUG-MAIN] 🔍 Checking container from context:', container ? 'valid' : 'null');
      if (!container) {
        console.error('[DEBUG-MAIN] ❌ No DI container available');
        setInitializationError("No DI container available");
        return;
      }

      console.log('[DEBUG-MAIN] ⏳ Waiting for services to be resolved...');
      // Wait for services to be resolved with timeout
      let waitCount = 0;
      const MAX_WAIT = 500; // 5 seconds max (500 * 10ms)
      while (!servicesResolved && waitCount < MAX_WAIT) {
        await new Promise((resolve) => setTimeout(resolve, 10));
        waitCount++;
        if (waitCount % 100 === 0) {
          console.log(`[DEBUG-MAIN] Still waiting for services... (${waitCount * 10}ms)`);
        }
      }

      if (!servicesResolved) {
        console.error('[DEBUG-MAIN] ❌ Service resolution timeout');
        setInitializationError("Service resolution timeout - services failed to initialize");
        return;
      }
      console.log('[DEBUG-MAIN] ✅ Services resolved, proceeding...');

      // Double-check services are available
      if (
        !initService ||
        !settingsService ||
        !sequenceService ||
        !deviceService
      ) {
        console.error('[DEBUG-MAIN] ❌ Services not properly resolved');
        setInitializationError("Services not properly resolved");
        return;
      }
      console.log('[DEBUG-MAIN] ✅ All services validated');

      // Step 1: Restore tab state FIRST (before UI renders)
      console.log('[DEBUG-MAIN] 💾 Restoring application state...');
      await restoreApplicationState();
      console.log('[DEBUG-MAIN] ✅ Application state restored');

      // Step 2: Initialize application services
      console.log('[DEBUG-MAIN] 🚀 Initializing application services...');
      await initService.initialize();
      console.log('[DEBUG-MAIN] ✅ Application services initialized');

      // Step 3: Load settings
      console.log('[DEBUG-MAIN] ⚙️ Loading settings...');
      await settingsService.loadSettings();
      updateSettings(settingsService.currentSettings);
      console.log('[DEBUG-MAIN] ✅ Settings loaded');

      // Step 3.5: Initialize theme service (after settings are loaded)
      console.log('[DEBUG-MAIN] 🎨 Initializing theme service...');
      ThemeService.initialize();
      console.log('[DEBUG-MAIN] ✅ Theme service initialized');

      // Step 4: Initialize device detection
      // (placeholder for future device detection init)

      // Step 5: Load initial data
      // TODO: Individual components should load their own data as needed

      // Step 6: Complete initialization
      console.log('[DEBUG-MAIN] 🎉 Initialization complete!');
      setInitializationState(true, false, null, 0);
    } catch (error) {
      console.error("[DEBUG-MAIN] ❌ Application initialization failed:", error);
      setInitializationError(
        error instanceof Error ? error.message : "Unknown initialization error"
      );
    }

    return () => {
      cleanupSheetListener();
    };
  });

  // Handle keyboard shortcuts
  $effect(() => {
    function handleKeydown(event: KeyboardEvent) {
      // Settings dialog toggle (Ctrl/Cmd + ,)
      if ((event.ctrlKey || event.metaKey) && event.key === ",") {
        event.preventDefault();
        if (getShowSettings() || currentSheetType === 'settings') {
          closeSheet();
          hideSettingsDialog();
        } else {
          openSheet('settings');
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
  {:else}
    <!-- Main Interface - Always shown, progressive loading inside -->
    <MainInterface />

    <!-- Settings slide panel (route-aware) -->
    <SettingsSheet isOpen={getShowSettings() || showRouteBasedSettings()} />

    <!-- Profile Settings sheet (route-based, 95vh) -->
    <ProfileSettingsSheet
      isOpen={showProfileSettings()}
      onClose={() => closeSheet()}
    />

    <!-- Auth sheet (route-based) -->
    <AuthSheet
      isOpen={showAuthSheet()}
      onClose={() => closeSheet()}
    />

    <!-- Terms sheet (route-based) -->
    <TermsSheet
      isOpen={showTermsSheet()}
      onClose={() => closeSheet()}
    />

    <!-- Privacy sheet (route-based) -->
    <PrivacySheet
      isOpen={showPrivacySheet()}
      onClose={() => closeSheet()}
    />
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
