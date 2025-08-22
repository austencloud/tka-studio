<!-- ModernStartPositionPicker.svelte - Clean orchestrator for start position selection -->
<script lang="ts">
  import type { BeatData } from "$domain/BeatData";
  import type { PictographData } from "$domain/PictographData";
  import { GridMode } from "$lib/domain";
  import { onMount } from "svelte";
  // Import our modular components and services
  import StartPositionGrid from "./components/StartPositionGrid.svelte";
  import { StartPositionLoader } from "./services/StartPositionLoader";
  import { StartPositionServiceResolver } from "./services/StartPositionServiceResolver";
  import {
    createStartPositionBeat,
    createStartPositionData,
    extractEndPosition,
    storePreloadedOptions,
    storeStartPositionData,
  } from "./utils/StartPositionUtils";

  // Props using runes
  const { gridMode = GridMode.DIAMOND, onStartPositionSelected = () => {} } =
    $props<{
      gridMode?: GridMode;
      onStartPositionSelected?: (position: BeatData) => void;
    }>();

  // Reactive state
  let startPositions = $state<PictographData[]>([]);
  let selectedPosition = $state<PictographData | null>(null);
  let isLoading = $state(true);
  let loadingError = $state(false);
  let isTransitioning = $state(false);

  // Service instances
  let serviceResolver: StartPositionServiceResolver;
  let positionLoader: StartPositionLoader;
  let servicesReady = $state(false);

  /**
   * Initialize services and load start positions
   */
  onMount(async () => {
    console.log("🚀 ModernStartPositionPicker: Initializing");

    try {
      // Initialize service resolver
      serviceResolver = new StartPositionServiceResolver();

      // Resolve services
      const { startPositionService, isResolved } =
        await serviceResolver.resolveServices();

      if (!isResolved) {
        console.warn(
          "⚠️ ModernStartPositionPicker: Services not fully resolved"
        );
        loadingError = true;
        isLoading = false;
        return;
      }

      // Initialize position loader
      positionLoader = new StartPositionLoader(startPositionService);
      servicesReady = true;

      // Load start positions
      await loadStartPositions();

      console.log("✅ ModernStartPositionPicker: Initialization complete");
    } catch (error) {
      console.error(
        "❌ ModernStartPositionPicker: Initialization failed",
        error
      );
      loadingError = true;
      isLoading = false;
    }
  });

  /**
   * Load start positions for current grid mode
   */
  async function loadStartPositions() {
    if (!servicesReady) return;

    isLoading = true;
    loadingError = false;

    try {
      console.log(
        `🔄 ModernStartPositionPicker: Loading positions for ${gridMode} mode`
      );

      const positions = await positionLoader.loadStartPositions(gridMode);
      startPositions = positions;

      console.log(
        `✅ ModernStartPositionPicker: Loaded ${positions.length} positions`
      );
    } catch (error) {
      console.error(
        "❌ ModernStartPositionPicker: Failed to load positions",
        error
      );
      loadingError = true;
      startPositions = [];
    } finally {
      isLoading = false;
    }
  }

  /**
   * Handle start position selection
   */
  async function handlePositionSelected(position: PictographData) {
    if (isTransitioning) return;

    console.log(
      "🎯 ModernStartPositionPicker: Position selected",
      position.letter
    );

    selectedPosition = position;
    isTransitioning = true;

    try {
      // Extract end position for OptionPicker integration
      const endPosition = extractEndPosition(position);

      // Create start position data for OptionPicker
      const startPositionData = createStartPositionData(position, endPosition);

      // Create beat data for callback
      const beatData = createStartPositionBeat(position);

      // Store data for OptionPicker integration
      storeStartPositionData(startPositionData);

      // Preload next options if possible
      await preloadNextOptions(endPosition);

      // Notify parent component
      onStartPositionSelected(beatData);

      console.log("✅ ModernStartPositionPicker: Position selection completed");
    } catch (error) {
      console.error(
        "❌ ModernStartPositionPicker: Position selection failed",
        error
      );
    } finally {
      isTransitioning = false;
    }
  }

  /**
   * Preload next options for smoother transitions
   */
  async function preloadNextOptions(endPosition: string) {
    if (!servicesReady) return;

    try {
      console.log("🔄 ModernStartPositionPicker: Preloading next options");

      // This would integrate with OptionPicker service if available
      // For now, just store empty object to prevent errors
      storePreloadedOptions({});

      console.log("✅ ModernStartPositionPicker: Next options preloaded");
    } catch (error) {
      console.error(
        "❌ ModernStartPositionPicker: Failed to preload next options",
        error
      );
    }
  }

  // Reactive effect: reload when grid mode changes
  $effect(() => {
    if (servicesReady) {
      loadStartPositions();
    }
  });
</script>

<!-- Main interface -->
<div class="start-position-picker">
  <!-- Header -->
  <div class="picker-header">
    <h2>Select Starting Position</h2>
    <p class="grid-mode-indicator">Grid Mode: {gridMode}</p>
  </div>

  <!-- Error state -->
  {#if loadingError}
    <div class="error-state">
      <h3>Failed to Load Start Positions</h3>
      <p>
        There was an error loading the start positions. Please try refreshing
        the page.
      </p>
      <button onclick={() => loadStartPositions()} disabled={isLoading}>
        Try Again
      </button>
    </div>
  {:else}
    <!-- Position grid -->
    <StartPositionGrid
      {startPositions}
      {selectedPosition}
      {isLoading}
      onPositionSelected={handlePositionSelected}
    />
  {/if}

  <!-- Transition overlay -->
  {#if isTransitioning}
    <div class="transition-overlay">
      <div class="transition-spinner"></div>
      <p>Preparing sequence...</p>
    </div>
  {/if}
</div>

<style>
  .start-position-picker {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 400px;
    position: relative;
  }

  .picker-header {
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
  }

  .picker-header h2 {
    margin: 0 0 8px 0;
    color: #333;
    font-size: 24px;
    font-weight: 600;
  }

  .grid-mode-indicator {
    margin: 0;
    color: #666;
    font-size: 14px;
    text-transform: capitalize;
  }

  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    text-align: center;
    color: #721c24;
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    margin: 20px;
  }

  .error-state h3 {
    margin: 0 0 12px 0;
    font-size: 18px;
  }

  .error-state p {
    margin: 0 0 20px 0;
    color: #721c24;
  }

  .error-state button {
    padding: 8px 16px;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .error-state button:hover:not(:disabled) {
    background: #c82333;
  }

  .error-state button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .transition-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .transition-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007acc;
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

  .transition-overlay p {
    color: #333;
    font-weight: 500;
  }
</style>
