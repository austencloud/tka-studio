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
  import HMRTest from "../../dev/HMRTest.svelte";
  import AchievementNotificationToast from "../../gamification/components/AchievementNotificationToast.svelte";

  import type { ISettingsService } from "$shared";
  import type { Container } from "inversify";
  import { getContext, onMount } from "svelte";
  import MainInterface from "../../MainInterface.svelte";
  import AuthSheet from "../../navigation/components/AuthSheet.svelte";
  import PrivacySheet from "../../navigation/components/PrivacySheet.svelte";
  import ProfileSettingsSheet from "../../navigation/components/ProfileSettingsSheet.svelte";
  import TermsSheet from "../../navigation/components/TermsSheet.svelte";
  import type { SheetType } from "../../navigation/utils/sheet-router";
  import {
    closeSheet,
    getCurrentSheet,
    onSheetChange,
    openSheet,
  } from "../../navigation/utils/sheet-router";
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
  let showProfileSettings = $derived(
    () => currentSheetType === "profile-settings"
  );
  let showRouteBasedSettings = $derived(() => currentSheetType === "settings");
  let showAuthSheet = $derived(() => currentSheetType === "auth");
  let showTermsSheet = $derived(() => currentSheetType === "terms");
  let showPrivacySheet = $derived(() => currentSheetType === "privacy");

  // Resolve services when container is available
  $effect(() => {
    const container = getContainer?.();

    if (container && !servicesResolved) {
      try {
        if (!isContainerReady()) {
          console.warn(
            "Container available but not cached, ensuring initialization..."
          );
          ensureContainerInitialized().then(() => {
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
    currentSheetType = getCurrentSheet();

    const cleanupSheetListener = onSheetChange((sheetType) => {
      currentSheetType = sheetType;

      // Sync with legacy settings dialog state
      if (sheetType === "settings") {
        if (!getShowSettings()) {
          showSettingsDialog();
        }
      } else if (sheetType === null && getShowSettings()) {
        hideSettingsDialog();
      }
    });

    try {
      setInitializationState(false, true, null, 0);
      await ensureContainerInitialized();
      await initializeAppState();

      const container = getContainer?.();
      if (!container) {
        console.error("No DI container available");
        setInitializationError("No DI container available");
        return;
      }

      // Wait for services to be resolved with timeout
      let waitCount = 0;
      const MAX_WAIT = 500; // 5 seconds max
      while (!servicesResolved && waitCount < MAX_WAIT) {
        await new Promise((resolve) => setTimeout(resolve, 10));
        waitCount++;
      }

      if (!servicesResolved) {
        console.error("Service resolution timeout");
        setInitializationError(
          "Service resolution timeout - services failed to initialize"
        );
        return;
      }

      if (
        !initService ||
        !settingsService ||
        !sequenceService ||
        !deviceService
      ) {
        console.error("Services not properly resolved");
        setInitializationError("Services not properly resolved");
        return;
      }

      await restoreApplicationState();
      await initService.initialize();
      await settingsService.loadSettings();
      updateSettings(settingsService.currentSettings);
      ThemeService.initialize();

      // Initialize gamification system
      try {
        const { initializeGamification } = await import("../../gamification/init/gamification-initializer");
        await initializeGamification();
        console.log("✅ Gamification initialized");
      } catch (gamError) {
        console.error("⚠️ Gamification failed to initialize (non-blocking):", gamError);
      }

      setInitializationState(true, false, null, 0);
    } catch (error) {
      console.error("Application initialization failed:", error);
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
        if (getShowSettings() || currentSheetType === "settings") {
          closeSheet();
          hideSettingsDialog();
        } else {
          openSheet("settings");
          showSettingsDialog();
        }
      }

      // Tab navigation (Ctrl/Cmd + 1-6)
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
    const backgroundType = settings.backgroundType;
    if (backgroundType && isInitialized) {
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
    <AuthSheet isOpen={showAuthSheet()} onClose={() => closeSheet()} />

    <!-- Terms sheet (route-based) -->
    <TermsSheet isOpen={showTermsSheet()} onClose={() => closeSheet()} />

    <!-- Privacy sheet (route-based) -->
    <PrivacySheet isOpen={showPrivacySheet()} onClose={() => closeSheet()} />

    <!-- Gamification Toast Notifications -->
    <AchievementNotificationToast />
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
