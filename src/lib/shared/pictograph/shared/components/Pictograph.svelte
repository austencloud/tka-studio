<script lang="ts">
  import {
    BeatNumber,
    EmptyStateIndicator,
    GridMode,
    ReversalIndicators,
    type BeatData,
    type IAnimationService,
    type ITurnsTupleGeneratorService,
    type PictographData,
  } from "$shared";
  import { onMount, onDestroy } from "svelte";
  import { resolve, tryResolve, TYPES } from "../../../inversify";
  import ArrowSvg from "../../arrow/rendering/components/ArrowSvg.svelte";
  import GridSvg from "../../grid/components/GridSvg.svelte";
  import type { IGridModeDeriver } from "../../grid/services/contracts";
  import PropSvg from "../../prop/components/PropSvg.svelte";
  import { TKAGlyph } from "../../tka-glyph";
  import { createPictographState } from "../state/pictograph-state.svelte";

  // Simplified Props interface - accepts either BeatData (with beat context) or PictographData (without)
  let {
    pictographData = null,
    disableContentTransitions = false,
    arrowsClickable = false,
    visibleHand = null,
    gridMode: overrideGridMode = null,
  } = $props<{
    pictographData?: (BeatData | PictographData) | null;
    disableContentTransitions?: boolean;
    arrowsClickable?: boolean; // Enable arrow selection for adjustment
    visibleHand?: "blue" | "red" | null; // Show only one hand's prop/arrow (for Guided Construct mode)
    gridMode?: GridMode | null; // Override grid mode (useful for single-motion start positions)
  }>();

  // Extract beat context from pictographData (if it's BeatData)
  const beatNumber = $derived((pictographData as any)?.beatNumber ?? null);
  const isStartPosition = $derived(beatNumber === 0);
  const isSelected = $derived((pictographData as any)?.isSelected ?? false);
  const blueReversal = $derived((pictographData as any)?.blueReversal ?? false);
  const redReversal = $derived((pictographData as any)?.redReversal ?? false);
  const showBeatNumber = $derived(beatNumber !== null && !isStartPosition); // Show beat number when in beat context and not start position

  // =============================================================================
  // STATE MANAGEMENT (using pictograph-state.svelte.ts)
  // =============================================================================

  // Lazy-resolved services (resolved on first access to avoid initialization race)
  let animationService: IAnimationService | null = null;
  let turnsTupleGenerator: ITurnsTupleGeneratorService | null = null;

  // Lazy service resolver - resolves on first access
  function getAnimationService(): IAnimationService | null {
    if (!animationService) {
      animationService = tryResolve<IAnimationService>(TYPES.IAnimationService);
    }
    return animationService;
  }

  function getTurnsTupleGenerator(): ITurnsTupleGeneratorService | null {
    if (!turnsTupleGenerator) {
      turnsTupleGenerator = tryResolve<ITurnsTupleGeneratorService>(
        TYPES.ITurnsTupleGeneratorService
      );
    }
    return turnsTupleGenerator;
  }

  // Synchronized fade-in for pictograph elements (props, arrows, glyph)
  const pictographFadeIn = (node: Element) => {
    const service = getAnimationService();
    if (!service) {
      return { duration: 0 };
    }

    return service.createFadeTransition({
      duration: 350, // Smooth fade-in duration
      delay: 0, // No delay for synchronized appearance
    });
  };

  // Synchronized fade-out for pictograph elements
  const pictographFadeOut = (node: Element) => {
    const service = getAnimationService();
    if (!service) {
      return { duration: 0 };
    }

    return service.createFadeOutTransition();
  };

  // Create pictograph state with reactive data management
  const pictographState = createPictographState(pictographData);

  // Track if component is mounted (services are ready)
  let isMounted = $state(false);

  // Update pictograph state when props change
  $effect(() => {
    pictographState.updatePictographData(pictographData);
  });

  // Recalculate prop and arrow positions when pictograph data changes
  // Only after component is mounted and services are initialized
  $effect(() => {
    if (pictographData && isMounted) {
      pictographState.calculatePropPositions();
      pictographState.calculateArrowPositions();
    }
  });

  // Generate turns tuple from pictograph data for TKA glyph
  const turnsTuple = $derived.by(() => {
    if (
      !pictographData ||
      !pictographData.motions?.blue ||
      !pictographData.motions?.red
    ) {
      return "(s, 0, 0)"; // Default fallback
    }
    const generator = getTurnsTupleGenerator();
    if (!generator) {
      return "(s, 0, 0)"; // Fallback if service not available yet
    }
    return generator.generateTurnsTuple(pictographData);
  });

  // Create a content key that changes when pictograph content changes
  // This triggers transitions when turn values, motions, or letter changes
  // IMPORTANT: Use pictographData directly (reactive prop) not pictographState
  // NOTE: Reversal state is NOT included here - it updates mid-fade via delayed state below
  const pictographContentKey = $derived.by(() => {
    if (!pictographData) return "empty";

    // Serialize the actual pictograph data to detect any changes
    return JSON.stringify({
      id: pictographData.id,
      letter: pictographData.letter,
      blueMotion: pictographData.motions.blue,
      redMotion: pictographData.motions.red,
    });
  });

  // Delayed reversal state - updates halfway through fade-out (125ms delay)
  // This creates the effect of reversals swapping at 50% opacity during transitions
  let delayedBlueReversal = $state(false);
  let delayedRedReversal = $state(false);
  let reversalUpdateTimeout: ReturnType<typeof setTimeout> | null = null;

  $effect(() => {
    // Track current reversal values
    const currentBlue = blueReversal;
    const currentRed = redReversal;

    // Clear any pending timeout
    if (reversalUpdateTimeout) {
      clearTimeout(reversalUpdateTimeout);
    }

    // Schedule reversal update for halfway through fade-out (125ms of 250ms)
    reversalUpdateTimeout = setTimeout(() => {
      delayedBlueReversal = currentBlue;
      delayedRedReversal = currentRed;
    }, 125);

    // Cleanup on component unmount
    return () => {
      if (reversalUpdateTimeout) {
        clearTimeout(reversalUpdateTimeout);
      }
    };
  });

  // =============================================================================
  // SVG RENDERING STATE (previously in PictographSvg)
  // =============================================================================

  // Loading coordination state
  let loadedComponents = $state(new Set<string>());

  // Track if all components are loaded for coordinated display
  const allComponentsLoaded = $derived.by(() => {
    if (!pictographState.hasValidData) return false;

    // Required components: grid only (props and arrows are pre-loaded by parent)
    const requiredComponents = ["grid"];

    return requiredComponents.every((component) =>
      loadedComponents.has(component)
    );
  });

  // Derive grid mode from pictograph data using Svelte 5 runes
  // Use override gridMode if provided (for single-motion start positions in Guided mode)
  const gridMode = $derived(
    (() => {
      // Use override if provided
      if (overrideGridMode !== null) {
        return overrideGridMode;
      }

      if (
        !pictographState.effectivePictographData ||
        !pictographState.effectivePictographData.motions?.blue ||
        !pictographState.effectivePictographData.motions?.red
      ) {
        return GridMode.DIAMOND; // Default fallback
      }

      try {
        const gridModeService = resolve<IGridModeDeriver>(
          TYPES.IGridModeDeriver
        );
        return gridModeService.deriveGridMode(
          pictographState.effectivePictographData.motions.blue,
          pictographState.effectivePictographData.motions.red
        );
      } catch (error) {
        console.error("Failed to derive grid mode:", error);
        return GridMode.DIAMOND; // Fallback to default on error
      }
    })()
  );

  // Standard pictograph viewBox
  const viewBox = "0 0 950 950";

  // Filter motions based on visibleHand prop (for Guided Construct mode)
  const filteredMotionsToRender = $derived.by(() => {
    if (!visibleHand) {
      // Show both hands (default behavior)
      return pictographState.motionsToRender;
    }

    // Show only the specified hand's motion
    return pictographState.motionsToRender.filter(
      ({ color }) => color === visibleHand
    );
  });

  // =============================================================================
  // EVENT HANDLERS
  // =============================================================================

  // Enhanced component loading handler
  function handleComponentLoaded(componentName: string) {
    loadedComponents.add(componentName);
    loadedComponents = new Set(loadedComponents); // Trigger reactivity
    pictographState.handleComponentLoaded(componentName);
  }

  function handleComponentError(componentName: string, error: string) {
    pictographState.handleComponentError(componentName, error);
  }

  // =============================================================================
  // LIFECYCLE & EFFECTS
  // =============================================================================

  // Handle rotation override changes
  function handleRotationOverrideChanged(event: CustomEvent) {
    // Recalculate arrow positions when rotation override changes
    pictographState.calculateArrowPositions();
  }

  // Calculate arrow and prop positions when component mounts
  onMount(async () => {
    // Wait for services to initialize and calculate initial positions
    await pictographState.calculateArrowPositions();
    await pictographState.calculatePropPositions();

    // Mark as mounted - now $effect can handle reactive updates
    isMounted = true;

    // Listen for rotation override changes
    window.addEventListener(
      "rotation-override-changed",
      handleRotationOverrideChanged as EventListener
    );
  });

  onDestroy(() => {
    // Clean up event listener
    window.removeEventListener(
      "rotation-override-changed",
      handleRotationOverrideChanged as EventListener
    );
  });
</script>

{#snippet loadingPlaceholder()}
  <g class="loading-placeholder" opacity="0.3">
    <rect width="950" height="950" fill="#f3f4f6" />
    <text
      x="475"
      y="475"
      text-anchor="middle"
      dominant-baseline="middle"
      font-family="Arial, sans-serif"
      font-size="24"
      fill="#6b7280"
    >
      Loading...
    </text>
  </g>
{/snippet}

<!-- =============================================================================
     MAIN CONTAINER
     ============================================================================= -->
<div
  class="pictograph"
  class:loading={pictographState.isLoading}
  class:loaded={pictographState.isLoaded}
  class:has-error={pictographState.errorMessage}
  class:selected={isSelected}
>
  <svg
    width="100%"
    height="100%"
    {viewBox}
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label={pictographState.hasValidData
      ? "Pictograph"
      : "Empty Pictograph"}
  >
    <!-- Background -->
    <rect width="950" height="950" fill="white" />

    {#if pictographState.hasValidData}
      <!-- Show loading placeholder until all components are loaded -->
      {#if !allComponentsLoaded}
        {@render loadingPlaceholder()}
      {/if}

      <!-- Grid (static - no fade transitions) -->
      <GridSvg
        {gridMode}
        onLoaded={() => handleComponentLoaded("grid")}
        onError={(error) => handleComponentError("grid", error)}
      />

      <!-- Wrapper group for synchronized fade-in/out of dynamic elements -->
      {#if disableContentTransitions}
        <!-- No transitions - render content directly -->
        <g class="pictograph-elements">
          <!-- Props (rendered first so arrows appear on top) -->
          {#each filteredMotionsToRender as { color, motionData } (color)}
            {#if pictographState.effectivePictographData && pictographState.propAssets[color] && pictographState.propPositions[color]}
              <PropSvg
                {motionData}
                propAssets={pictographState.propAssets[color]}
                propPosition={pictographState.propPositions[color]}
                showProp={pictographState.showProps}
              />
            {/if}
          {/each}

          <!-- Arrows (rendered after props) -->
          {#each filteredMotionsToRender as { color, motionData } (color)}
            {#if pictographState.effectivePictographData && pictographState.arrowAssets[color] && pictographState.arrowPositions[color]}
              <ArrowSvg
                {motionData}
                {color}
                pictographData={pictographState.effectivePictographData}
                arrowAssets={pictographState.arrowAssets[color]}
                arrowPosition={pictographState.arrowPositions[color]}
                shouldMirror={pictographState.arrowMirroring[color] || false}
                showArrow={pictographState.showArrows}
                isClickable={arrowsClickable}
              />
            {/if}
          {/each}

          <!-- Letter/Glyph overlay -->
          {#if pictographState.displayLetter || pictographData?.letter}
            <TKAGlyph
              letter={pictographState.displayLetter || pictographData?.letter}
              {turnsTuple}
              pictographData={pictographState.effectivePictographData}
            />
          {/if}

          <!-- Beat number overlay -->
          <BeatNumber
            {beatNumber}
            {showBeatNumber}
            {isStartPosition}
            hasValidData={pictographState.hasValidData}
          />

          <!-- Reversal indicators -->
          <ReversalIndicators
            blueReversal={delayedBlueReversal}
            redReversal={delayedRedReversal}
            hasValidData={pictographState.hasValidData}
          />
        </g>
      {:else}
        <!-- With transitions - use key block for fade in/out -->
        {#key pictographContentKey}
          <g
            class="pictograph-elements"
            in:pictographFadeIn
            out:pictographFadeOut
          >
            <!-- Props (rendered first so arrows appear on top) -->
            {#each filteredMotionsToRender as { color, motionData } (color)}
              {#if pictographState.effectivePictographData && pictographState.propAssets[color] && pictographState.propPositions[color]}
                <PropSvg
                  {motionData}
                  propAssets={pictographState.propAssets[color]}
                  propPosition={pictographState.propPositions[color]}
                  showProp={pictographState.showProps}
                />
              {/if}
            {/each}

            <!-- Arrows (rendered after props) -->
            {#each filteredMotionsToRender as { color, motionData } (color)}
              {#if pictographState.effectivePictographData && pictographState.arrowAssets[color] && pictographState.arrowPositions[color]}
                <ArrowSvg
                  {motionData}
                  {color}
                  pictographData={pictographState.effectivePictographData}
                  arrowAssets={pictographState.arrowAssets[color]}
                  arrowPosition={pictographState.arrowPositions[color]}
                  shouldMirror={pictographState.arrowMirroring[color] || false}
                  showArrow={pictographState.showArrows}
                  isClickable={arrowsClickable}
                />
              {/if}
            {/each}

            <!-- Letter/Glyph overlay -->
            {#if pictographState.displayLetter || pictographData?.letter}
              <TKAGlyph
                letter={pictographState.displayLetter || pictographData?.letter}
                {turnsTuple}
                pictographData={pictographState.effectivePictographData}
              />
            {/if}

            <!-- Beat number overlay -->
            <BeatNumber
              {beatNumber}
              {showBeatNumber}
              {isStartPosition}
              hasValidData={pictographState.hasValidData}
            />

            <!-- Reversal indicators -->
            <ReversalIndicators
              blueReversal={delayedBlueReversal}
              redReversal={delayedRedReversal}
              hasValidData={pictographState.hasValidData}
            />
          </g>
        {/key}
      {/if}
    {:else}
      <!-- Empty state -->
      <EmptyStateIndicator
        {beatNumber}
        hasValidData={pictographState.hasValidData}
      />
    {/if}
  </svg>
</div>

<!-- =============================================================================
     STYLES (unified container and SVG styles)
     ============================================================================= -->
<style>
  .pictograph {
    position: relative;
    border-radius: 0; /* Remove border radius so pictographs touch */
    transition: all 0.2s ease;
    border: none; /* REMOVE BORDER - testing if this causes white line */
    width: 100%;
    height: 100%;
    max-width: 100%; /* Prevent overflow beyond parent */
    max-height: 100%; /* Prevent overflow beyond parent */
    display: block;
    margin: 0; /* Remove any margin */
    padding: 0; /* Remove any padding */
    box-sizing: border-box; /* Include border in width/height calculations */
    background: transparent; /* Transparent - SVG has white background */
  }

  /* Selected state - rounded corners to match selection border */
  .pictograph.selected {
    border-radius: 9px; /* 12px outer - 3px border = 9px inner radius */
    border-color: transparent; /* Hide gray border when selected */
    overflow: hidden; /* Ensure SVG content respects rounded corners */
  }

  .pictograph.loading {
    opacity: 1;
  }

  .pictograph.has-error {
    border-color: #ef4444;
  }

  /* SVG styles (from PictographSvg) */
  svg {
    display: block;
    box-sizing: border-box;
  }

  /* SVG inherits border-radius when selected */
  .pictograph.selected svg {
    border-radius: 9px;
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
