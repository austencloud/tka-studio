<!--
Pictograph.svelte - Modern Rune-Based Pictograph Component

This is the modern equivalent of the legacy Pictograph.svelte, but using pure Svelte 5 runes
instead of stores. It orchestrates the rendering of Grid, Props, Arrows, and Glyphs.
-->
<script lang="ts">
  import type {
    ArrowData,
    BeatData,
    MotionColor,
    PictographData,
  } from "$lib/domain";
  import type { IArrowPositioningOrchestrator } from "$lib/services/positioning/core-services";
  import { onMount } from "svelte";
  import Arrow from "./Arrow.svelte";
  import Grid from "./Grid.svelte";
  import Prop from "./Prop.svelte";
  import TKAGlyph from "./TKAGlyph.svelte";
  import { resolve } from "$lib/services/bootstrap";

  interface Props {
    /** Pictograph data to render */
    pictographData?: PictographData | null;
    /** Beat data (alternative to pictographData) */
    beatData?: BeatData | null;
    /** Click handler */
    onClick?: () => void;
    /** Debug mode */
    debug?: boolean;
    /** Animation duration for transitions */
    animationDuration?: number;
    /** Show loading indicator */
    showLoadingIndicator?: boolean;
    /** Beat number for display */
    beatNumber?: number | null;
    /** Is this a start position? */
    isStartPosition?: boolean;
    /** SVG dimensions */
    width?: number;
    height?: number;
  }

  let {
    pictographData = null,
    beatData = null,
    onClick,
    debug = false,
    beatNumber = null,
    isStartPosition = false,
    width = undefined,
    height = undefined,
  }: Props = $props();

  // Determine if we should use responsive sizing (no width/height specified)
  const isResponsive = $derived(
    () => width === undefined && height === undefined
  );

  // Get the orchestrator - SINGLE SOURCE OF TRUTH for arrow positioning
  const orchestrator = resolve(
    "IArrowPositioningOrchestrator"
  ) as IArrowPositioningOrchestrator;

  // State using runes - isLoading and isLoaded are now derived from allComponentsLoaded()
  let errorMessage = $state<string | null>(null);
  let loadedComponents = $state(new Set<string>());

  // Arrow positioning coordination state
  let arrowPositions = $state<
    Record<string, { x: number; y: number; rotation: number }>
  >({});
  let arrowMirroring = $state<Record<string, boolean>>({});
  let showArrows = $state(false);

  // Derived state - get effective pictograph data
  const effectivePictographData = $derived(() => {
    if (pictographData) return pictographData;
    if (beatData?.pictograph_data) return beatData.pictograph_data;
    return null;
  });

  // Derived state - check if we have required data
  const hasValidData = $derived(() => {
    return effectivePictographData() != null;
  });

  // Derived state - display letter
  const displayLetter = $derived(() => {
    const data = effectivePictographData();
    if (data?.letter) return data.letter;
    if (beatData && !beatData.isBlank) return beatData.beat_number.toString();
    return null;
  });

  // Derived state - arrows to render
  const arrowsToRender = $derived(() => {
    const data = effectivePictographData();
    if (!data?.arrows) return [];

    return Object.entries(data.arrows)
      .filter(([_, arrowData]) => arrowData != null)
      .map(([color, arrowData]) => ({
        color: color as MotionColor,
        arrowData,
      }));
  });

  // Derived state - props to render
  const propsToRender = $derived(() => {
    const data = effectivePictographData();
    if (!data?.props) return [];

    return Object.entries(data.props)
      .filter(([_, propData]) => propData != null)
      .map(([color, propData]) => ({
        color: color as MotionColor,
        propData,
      }));
  });

  // Component loading tracking
  let requiredComponents = $derived(() => {
    let components = ["grid"];

    const data = effectivePictographData();
    if (data?.arrows?.blue) components.push("blue-arrow");
    if (data?.arrows?.red) components.push("red-arrow");
    if (data?.props?.blue) components.push("blue-prop");
    if (data?.props?.red) components.push("red-prop");

    return components;
  });

  const allComponentsLoaded = $derived(() => {
    const required = requiredComponents();
    return required.every((component) => loadedComponents.has(component));
  });

  // Reactively update loading state - CONVERTED TO $derived TO PREVENT INFINITE LOOPS
  const isLoading = $derived(() => !allComponentsLoaded());
  const isLoaded = $derived(() => allComponentsLoaded());

  // Initialize loading when data changes - REMOVED REACTIVE STATE MODIFICATIONS TO PREVENT INFINITE LOOP
  $effect(() => {
    if (hasValidData()) {
      // isLoading and isLoaded are now derived, don't modify them directly
      errorMessage = null;
      loadedComponents.clear();

      // DO NOT reset arrow positioning here - it causes infinite loops!
      // Arrow positioning will be handled by calculateArrowPositions() function
      showArrows = false;
    }
  });

  // MANUAL ARROW POSITIONING: Calculate positions when needed without reactive loops
  async function calculateArrowPositions() {
    const data = effectivePictographData();
    if (!data?.arrows) {
      showArrows = true; // No arrows to position
      return;
    }

    try {
      // Use the orchestrator's calculateAllArrowPositions() method - the ONLY positioning authority
      const updatedPictographData =
        await orchestrator.calculateAllArrowPositions(data);

      // Extract calculated positions and mirroring from the updated pictograph data
      const newPositions: Record<
        string,
        { x: number; y: number; rotation: number }
      > = {};
      const newMirroring: Record<string, boolean> = {};

      if (updatedPictographData.arrows) {
        Object.entries(updatedPictographData.arrows).forEach(
          ([color, arrowData]) => {
            if (arrowData) {
              // Type assertion to ArrowData from the orchestrator
              const arrow = arrowData as ArrowData;
              newPositions[color] = {
                x: arrow.position_x || 475,
                y: arrow.position_y || 475,
                rotation: arrow.rotation_angle || 0,
              };
              newMirroring[color] = arrow.isMirrored || false;
            }
          }
        );
      }

      arrowPositions = newPositions;
      arrowMirroring = newMirroring;

      showArrows = true;
    } catch (error) {
      console.error("Orchestrator positioning failed:", error);
      // Fallback: show arrows without coordination
      showArrows = true;
    }
  }

  // Call arrow positioning once when component mounts (no reactive dependencies)
  onMount(() => {
    calculateArrowPositions();
  });

  // Component event handlers
  function handleComponentLoaded(componentName: string) {
    loadedComponents.add(componentName);
    if (debug) {
      console.log(`Component loaded: ${componentName}`, {
        loaded: loadedComponents.size,
        required: requiredComponents().length,
      });
    }
  }

  function handleComponentError(componentName: string, error: string) {
    errorMessage = `${componentName}: ${error}`;
    if (debug) {
      console.error(`Component error: ${componentName}`, error);
    }
    // Still mark as loaded to prevent blocking
    handleComponentLoaded(componentName);
  }

  function handleSvgClick() {
    onClick?.();
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onClick?.();
    }
  }

  // SVG viewBox calculation
  const viewBox = $derived(() => `0 0 950 950`);

  // Compute beat number from explicit prop or fallback to beatData
  const computedBeatNumber = $derived(() => {
    return beatNumber ?? beatData?.beat_number ?? null;
  });
</script>

<!-- Main SVG Container -->
<div
  class="pictograph"
  class:loading={isLoading}
  class:loaded={isLoaded}
  class:has-error={errorMessage}
  class:clickable={onClick}
  class:debug-mode={debug}
  class:responsive={isResponsive()}
  style:width={isResponsive() ? "100%" : `${width}px`}
  style:height={isResponsive() ? "100%" : `${height}px`}
>
  <svg
    width={isResponsive() ? "100%" : width || 144}
    height={isResponsive() ? "100%" : height || 144}
    viewBox={viewBox()}
    xmlns="http://www.w3.org/2000/svg"
    onclick={handleSvgClick}
    onkeydown={handleKeyDown}
    role={onClick ? "button" : "img"}
    {...onClick ? { tabindex: 0 } : {}}
    aria-label={isStartPosition
      ? "Start Position"
      : `Beat ${computedBeatNumber() || ""} Pictograph`}
  >
    <!-- Background -->
    <rect width="950" height="950" fill="white" />

    {#if hasValidData()}
      <!-- Grid (always rendered first) -->
      <Grid
        gridMode={effectivePictographData()?.gridData?.gridMode || "diamond"}
        onLoaded={() => handleComponentLoaded("grid")}
        onError={(error) => handleComponentError("grid", error)}
        {debug}
      />

      <!-- Props (rendered first so arrows appear on top) -->
      {#each propsToRender() as { color, propData } (color)}
        {@const motionData = effectivePictographData()?.motions?.[color]}
        <Prop
          {propData}
          {...motionData && { motionData }}
          gridMode={effectivePictographData()?.gridData?.gridMode || "diamond"}
          allProps={Object.values(effectivePictographData()?.props || {})}
          onLoaded={() => handleComponentLoaded(`${color}-prop`)}
          onError={(error) => handleComponentError(`${color}-prop`, error)}
        />
      {/each}

      <!-- Arrows (rendered after props) -->
      {#each arrowsToRender() as { color, arrowData } (color)}
        {@const motionData = effectivePictographData()?.motions?.[color]}
        <Arrow
          {arrowData}
          {...motionData && { motionData }}
          preCalculatedPosition={arrowPositions[color]}
          preCalculatedMirroring={arrowMirroring[color]}
          showArrow={showArrows}
          onLoaded={() => handleComponentLoaded(`${color}-arrow`)}
          onError={(error) => handleComponentError(`${color}-arrow`, error)}
        />
      {/each}
      <!-- Letter/Glyph overlay -->
      {#if displayLetter()}
        <TKAGlyph letter={displayLetter()} turnsTuple="(s, 0, 0)" />
      {/if}

      <!-- Beat label -->
      {#if computedBeatNumber() && !isStartPosition}
        <text
          x="475"
          y="50"
          text-anchor="middle"
          font-family="Arial, sans-serif"
          font-size="24"
          font-weight="bold"
          fill="#4b5563"
        >
          {computedBeatNumber()}
        </text>
      {/if}

      <!-- Start position label -->
      {#if isStartPosition}
        <text
          x="475"
          y="50"
          text-anchor="middle"
          font-family="Arial, sans-serif"
          font-size="20"
          font-weight="bold"
          fill="#059669"
        >
          START
        </text>
      {/if}
    {:else}
      <!-- Empty state -->
      <g class="empty-state">
        <circle
          cx="475"
          cy="475"
          r="100"
          fill="#f3f4f6"
          stroke="#e5e7eb"
          stroke-width="2"
        />
        <text
          x="475"
          y="475"
          text-anchor="middle"
          font-family="Arial, sans-serif"
          font-size="16"
          fill="#6b7280"
        >
          {computedBeatNumber() || "Empty"}
        </text>
      </g>
    {/if}
  </svg>
</div>

<style>
  .pictograph {
    position: relative;
    border-radius: 8px;
    transition: all 0.2s ease;
    background: white;
    border: 1px solid #e5e7eb;
    /* add a border radius */
  }

  .pictograph.responsive {
    width: 100% !important;
    height: 100% !important;
    display: block;
  }

  .pictograph.clickable {
    cursor: pointer;
  }

  .pictograph.clickable:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    transform: translateY(-1px);
  }

  .pictograph.loading {
    opacity: 0.8;
  }

  .pictograph.has-error {
    border-color: #ef4444;
  }

  .pictograph.debug-mode {
    border-color: #8b5cf6;
    border-width: 2px;
  }

  svg {
    display: block;
    box-sizing: border-box;
  }

  /* Only use 100% size when responsive */
  .responsive svg {
    width: 100%;
    height: 100%;
  }

  .pictograph:focus-within {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  }

  /* Animation classes for component loading */
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
