<!--
Pictograph.svelte - Modern Rune-Based Pictograph Component (Refactored)

This is the refactored version of the Pictograph component using the new pictograph-state.svelte.ts
for proper Svelte 5 runes state management without warnings.

ARCHITECTURE:
- createPictographState: Handles all pictograph state management with Svelte 5 runes
- PictographSvg: Handles SVG rendering
- Main component: Focuses on state coordination and layout
-->
<script lang="ts">
  import type { PictographData } from "$shared";
  import { onMount } from "svelte";
  import { createPictographState } from "../state/pictograph-state.svelte";
  import PictographSvg from "./PictographSvg.svelte";

  // Simplified Props interface - removed beat-specific properties
  interface Props {
    pictographData?: PictographData | null;
  }

  let { pictographData = null }: Props = $props();

  // =============================================================================
  // STATE MANAGEMENT (using pictograph-state.svelte.ts)
  // =============================================================================

  // Create pictograph state with reactive data management
  const pictographState = createPictographState(pictographData);

  // Update state when props change
  $effect(() => {
    pictographState.updatePictographData(pictographData);
  });

  // =============================================================================
  // DERIVED STATE (from pictograph state)
  // =============================================================================

  // All state is now managed by pictographState - no local state needed

  // Standard pictograph viewBox
  const viewBox = "0 0 950 950";

  // =============================================================================
  // EVENT HANDLERS (delegated to pictograph state)
  // =============================================================================

  function handleComponentLoaded(componentName: string) {
    pictographState.handleComponentLoaded(componentName);
  }

  function handleComponentError(componentName: string, error: string) {
    pictographState.handleComponentError(componentName, error);
  }

  // =============================================================================
  // LIFECYCLE & EFFECTS
  // =============================================================================

  // Calculate arrow and prop positions when component mounts
  onMount(async () => {
    await pictographState.calculateArrowPositions();
    await pictographState.calculatePropPositions();
  });

  // =============================================================================
  // UI STATE
  // =============================================================================

  // SVG viewBox is already defined above
</script>

<!-- =============================================================================
     MAIN CONTAINER
     ============================================================================= -->
<div
  class="pictograph"
  class:loading={pictographState.isLoading}
  class:loaded={pictographState.isLoaded}
  class:has-error={pictographState.errorMessage}
>
  <PictographSvg
    pictographData={pictographState.effectivePictographData}
    hasValidData={pictographState.hasValidData}
    displayLetter={pictographState.displayLetter}
    motionsToRender={pictographState.motionsToRender}
    width="100%"
    height="100%"
    {viewBox}
    arrowPositions={pictographState.arrowPositions}
    arrowMirroring={pictographState.arrowMirroring}
    arrowAssets={pictographState.arrowAssets}
    showArrows={pictographState.showArrows}
    propPositions={pictographState.propPositions}
    propAssets={pictographState.propAssets}
    showProps={pictographState.showProps}
    onComponentLoaded={handleComponentLoaded}
    onComponentError={handleComponentError}
    ariaLabel={pictographState.hasValidData ? "Pictograph" : "Empty Pictograph"}
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
