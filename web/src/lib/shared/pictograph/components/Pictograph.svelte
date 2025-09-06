<!--
Pictograph.svelte - Modern Rune-Based Pictograph Component (Refactored)

This is the refactored version of the Pictograph component, broken down into logical,
easy-to-understand parts using focused hooks and components for different concerns.

ARCHITECTURE:
- usePictographData: Handles data transformation and derivation
- useComponentLoading: Manages component loading state coordination
- useArrowPositioning: Coordinates arrow positioning
- PictographSvg: Handles SVG rendering
- Main component: Focuses on state management and layout
-->
<script lang="ts">
  import type { PictographData } from "$shared/domain";
  import { onMount } from "svelte";
  import PictographSvg from "./PictographSvg.svelte";
// Import our focused hooks
  import {
    useArrowPositioning,
    useComponentLoading,
    usePictographData,
  } from "../services/implementations";

  // Simplified Props interface - removed beat-specific properties
  interface Props {
    pictographData?: PictographData | null;
  }

  let { pictographData = null }: Props = $props();

  // =============================================================================
  // HOOK-BASED STATE MANAGEMENT
  // =============================================================================

  // Data transformation and derivation
  const dataState = usePictographData({
    pictographData,
  });

  // Component loading management factory
  const loadingFactory = useComponentLoading();

  // Arrow positioning factory
  const arrowFactory = useArrowPositioning({
    pictographData: dataState.effectivePictographData,
  });

  // =============================================================================
  // REACTIVE STATE (using Svelte runes)
  // =============================================================================

  // Component loading state
  let errorMessage = $state<string | null>(null);
  let loadedComponents = $state(new Set<string>());

  // Arrow positioning state
  let arrowPositions = $state<
    Record<string, { x: number; y: number; rotation: number }>
  >({});
  let arrowMirroring = $state<Record<string, boolean>>({});
  let showArrows = $state(false);

  // Derived states
  const requiredComponents = $derived(() => {
    return loadingFactory.getRequiredComponents(
      dataState.effectivePictographData
    );
  });

  const allComponentsLoaded = $derived(() => {
    return requiredComponents().every((component: string) =>
      loadedComponents.has(component)
    );
  });

  const isLoading = $derived(() => !allComponentsLoaded());
  const isLoaded = $derived(() => allComponentsLoaded());

  // =============================================================================
  // EVENT HANDLERS
  // =============================================================================

  function handleComponentLoaded(componentName: string) {
    loadedComponents.add(componentName);
  }

  function handleComponentError(componentName: string, error: string) {
    errorMessage = `${componentName}: ${error}`;
    // Still mark as loaded to prevent blocking
    handleComponentLoaded(componentName);
  }

  // =============================================================================
  // LIFECYCLE & EFFECTS
  // =============================================================================

  // Clear loading state when data changes (but preserve arrow visibility)
  $effect(() => {
    if (dataState.effectivePictographData) {
      errorMessage = null;
      loadedComponents.clear();
      // Don't reset showArrows here - let onMount handle arrow positioning
    }
  });

  // Calculate arrow positions when component mounts
  onMount(async () => {
    const result = await arrowFactory.calculateArrowPositions(
      dataState.effectivePictographData
    );
    arrowPositions = result.positions;
    arrowMirroring = result.mirroring;
    showArrows = result.showArrows;
  });

  // =============================================================================
  // UI STATE
  // =============================================================================

  // SVG viewBox calculation
  const viewBox = $derived(`0 0 950 950`);
</script>

<!-- =============================================================================
     MAIN CONTAINER
     ============================================================================= -->
<div
  class="pictograph"
  class:loading={isLoading}
  class:loaded={isLoaded}
  class:has-error={errorMessage}
>
  <PictographSvg
    pictographData={dataState.effectivePictographData}
    hasValidData={dataState.hasValidData}
    displayLetter={dataState.displayLetter}
    motionsToRender={dataState.motionsToRender}
    width="100%"
    height="100%"
    {viewBox}
    {arrowPositions}
    {arrowMirroring}
    {showArrows}
    onComponentLoaded={handleComponentLoaded}
    onComponentError={handleComponentError}
    ariaLabel={dataState.hasValidData ? "Pictograph" : "Empty Pictograph"}
  />
</div>

<!-- =============================================================================
     STYLES (updated for container-only styles)
     ============================================================================= -->
<style>
  .pictograph {
    position: relative;
    border-radius: 8px;
    transition: all 0.2s ease;
    background: white;
    border: 1px solid #e5e7eb;
    width: 100%;
    height: 100%;
    display: block;
  }

  .pictograph.loading {
    opacity: 0.8;
  }

  .pictograph.has-error {
    border-color: #ef4444;
  }

  :global(.component-loading) {
    opacity: 0.5;
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 0.5;
    }
    50% {
      opacity: 0.8;
    }
    100% {
      opacity: 0.5;
    }
  }
</style>
