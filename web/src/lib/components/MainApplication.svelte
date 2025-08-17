<!-- Main Application Layout -->
<script lang="ts">
  import { resolve } from "$services/bootstrap";
  import type { ServiceContainer } from "$services/di/ServiceContainer";
  import type {
    IApplicationInitializationService,
    ISettingsService,
  } from "$services/interfaces/application-interfaces";
  import type { ISequenceService } from "$services/interfaces/sequence-interfaces";
  import type { IDeviceDetectionService } from "$services/interfaces/device-interfaces";
  import { getContext, onMount } from "svelte";

  // Import app state management
  import {
    getInitializationError,
    getInitializationProgress,
    getIsInitialized,
    getShowSettings,
    hideSettingsDialog,
    restoreApplicationState,
    setInitializationError,
    setInitializationProgress,
    setInitializationState,
    showSettingsDialog,
    switchTab,
    updateSettings,
  } from "$lib/state/app-state.svelte";

  // Import components
  import ErrorScreen from "$components/ErrorScreen.svelte";
  import LoadingScreen from "$components/LoadingScreen.svelte";
  import MainInterface from "$components/MainInterface.svelte";
  import SettingsDialog from "$components/SettingsDialog.svelte";

  // Get DI container from context
  const getContainer =
    getContext<() => ServiceContainer | null>("di-container");

  // Services - resolved lazily
  let initService: IApplicationInitializationService | null = $state(null);
  let settingsService: ISettingsService | null = $state(null);
  let sequenceService: ISequenceService | null = $state(null);
  let deviceService: IDeviceDetectionService | null = $state(null);
  let servicesResolved = $state(false);

  // App state
  let isInitialized = $derived(getIsInitialized());
  let initializationError = $derived(getInitializationError());
  let initializationProgress = $derived(getInitializationProgress());

  // Resolve services when container is available - ONCE ONLY
  $effect(() => {
    const container = getContainer?.();
    if (container && !servicesResolved) {
      try {
        console.log(
          "🚀 MainApplication container ready, resolving services..."
        );

        // Use resolve which will use the global container once it's ready
        initService = resolve("IApplicationInitializationService");
        settingsService = resolve("ISettingsService");
        sequenceService = resolve("ISequenceService");
        deviceService = resolve("IDeviceDetectionService");

        servicesResolved = true;
        console.log("✅ MainApplication services resolved successfully");
      } catch (error) {
        console.error("Failed to resolve services:", error);
        setInitializationError(`Service resolution failed: ${error}`);
      }
    }
  });

  // Initialize application
  onMount(async () => {
    const container = getContainer?.();
    if (!container) {
      setInitializationError("No DI container available");
      return;
    }

    // Wait for services to be resolved
    let attempts = 0;
    while (!servicesResolved && attempts < 10) {
      await new Promise((resolve) => setTimeout(resolve, 100));
      attempts++;
    }

    if (
      !servicesResolved ||
      !initService ||
      !settingsService ||
      !sequenceService ||
      !deviceService
    ) {
      setInitializationError("Failed to resolve required services");
      return;
    }

    try {
      setInitializationState(false, true, null, 0);

      // Step 1: Initialize application services
      setInitializationProgress(20);
      await initService.initialize();

      // Step 2: Load settings
      setInitializationProgress(40);
      await settingsService.loadSettings();
      updateSettings(settingsService.currentSettings);

      // Step 3: Initialize device detection
      setInitializationProgress(50);

      // Step 4: Load initial data
      setInitializationProgress(70);
      // TODO: Individual components should load their own data as needed

      // Step 5: Restore application state (tab memory)
      setInitializationProgress(85);
      await restoreApplicationState();

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
            switchTab("sequence_card");
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
            switchTab("motion-tester");
            break;
          case "7":
            event.preventDefault();
            switchTab("arrow-debug");
            break;
        }
      }
    }

    document.addEventListener("keydown", handleKeydown);
    return () => document.removeEventListener("keydown", handleKeydown);
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

    <!-- Settings dialog -->
    {#if getShowSettings()}
      <SettingsDialog />
    {/if}
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
