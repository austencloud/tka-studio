<!--
Arrow Component - Renders SVG arrows with proper positioning and natural sizing
Follows the same pattern as Prop component for consistent sizing behavior
REFACTORED: Now purely presentational, uses ArrowRenderingService for business logic
-->
<script lang="ts">
  import { MotionColor, type MotionData } from "$lib/domain";
  import { resolve } from "$lib/services/bootstrap";
  import type { IArrowRenderingService } from "$lib/services/interfaces/pictograph-interfaces";
  import { onMount } from "svelte";

  interface Props {
    motionData: MotionData; // Single source of truth - contains embedded arrow placement data
    preCalculatedPosition?:
      | { x: number; y: number; rotation: number }
      | undefined; // Pre-calculated position from parent
    preCalculatedMirroring?: boolean | undefined; // Pre-calculated mirroring from parent
    showArrow?: boolean; // Whether to show the arrow (coordination flag)
    onLoaded?: (componentType: string) => void;
    onError?: (componentType: string, error: string) => void;
  }

  let {
    motionData,
    preCalculatedPosition,
    preCalculatedMirroring,
    showArrow = true,
    onLoaded,
    onError,
  }: Props = $props();

  // Get arrow rendering service from DI container
  const arrowRenderingService = resolve(
    "IArrowRenderingService"
  ) as IArrowRenderingService;

  let loaded = $state(false);
  let error = $state<string | null>(null);
  let svgData = $state<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } | null>(null);

  // SINGLE SOURCE OF TRUTH: Use ONLY pre-calculated positions from ArrowPositioningOrchestrator
  const position = $derived(() => {
    if (!motionData) return { x: 475.0, y: 475.0, rotation: 0 };

    // ONLY use preCalculatedPosition - no more redundant calculations!
    if (preCalculatedPosition) {
      return preCalculatedPosition;
    }

    // Fallback: use position data from embedded arrow placement data
    const arrowPlacement = motionData.arrowPlacementData;
    if (arrowPlacement.positionX !== 0 || arrowPlacement.positionY !== 0) {
      return {
        x: arrowPlacement.positionX,
        y: arrowPlacement.positionY,
        rotation: arrowPlacement.rotationAngle || 0,
      };
    }

    return { x: 475.0, y: 475.0, rotation: 0 };
  });

  // SINGLE SOURCE OF TRUTH: Use only the position from the derived function
  const calculatedPosition = $derived(() => position());
  const shouldMirror = $derived(() => preCalculatedMirroring ?? false);

  // Load SVG data using ArrowRenderingService (business logic now in service)
  const loadSvg = async () => {
    try {
      if (!motionData) throw new Error("No motion data available");

      // TODO: Update ArrowRenderingService to work with embedded placement data
      // const svgDataResult = await arrowRenderingService.loadArrowPlacementData(motionData);

      // Temporary: Create mock SVG data until service is updated
      const svgDataResult = {
        imageSrc: `<svg viewBox="0 0 100 100"><path d="M50,10 L90,90 L50,70 L10,90 Z" fill="${motionData.color === "blue" ? "#2E3192" : "#ED1C24"}"/></svg>`,
        viewBox: { width: 100, height: 100 },
        center: { x: 50, y: 50 },
      };

      svgData = svgDataResult;
      loaded = true;
      onLoaded?.(`${motionData?.color}-arrow`);
    } catch (e) {
      error = `Failed to load arrow SVG: ${e}`;
      onError?.(`${motionData?.color}-arrow`, error);
      // Still mark as loaded to prevent blocking
      loaded = true;
    }
  };

  onMount(() => {
    loadSvg();
  });

  // Reload SVG when arrow path changes - REMOVED $effect TO PREVENT INFINITE LOOP
  // SVG will be loaded once on mount, no reactive reloading to avoid loops
</script>

<!-- Arrow Group -->
<g
  class="arrow-group {motionData?.color}-arrow"
  class:loaded
  data-arrow-color={motionData?.color}
  data-motion-type={motionData?.motionType}
  data-location={motionData?.arrowLocation}
>
  {#if error}
    <!-- Error state -->
    <circle r="10" fill="red" opacity="0.5" />
    <text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
  {:else if !motionData}
    <!-- No motion data available -->
    <text
      x="0"
      y="4"
      text-anchor="middle"
      font-size="10"
      fill="gray"
      opacity="0.5"
    >
      No motion data
    </text>
  {:else if !loaded || !svgData}
    <!-- Loading state -->
    <circle
      r="8"
      fill={motionData?.color === MotionColor.BLUE ? "#2E3192" : "#ED1C24"}
      opacity="0.3"
    />
    <animate
      attributeName="opacity"
      values="0.3;0.8;0.3"
      dur="1s"
      repeatCount="indefinite"
    />
  {:else if showArrow}
    <!-- Actual arrow SVG with natural sizing and centering (same as props) -->
    <!-- Native SVG with simplified transform chain -->
    <g
      transform="
        translate({calculatedPosition().x}, {calculatedPosition().y})
        rotate({calculatedPosition().rotation ||
        motionData?.arrowPlacementData?.rotationAngle ||
        0})
        scale({shouldMirror() ? -1 : 1}, 1)
        translate({-svgData.center.x}, {-svgData.center.y})
      "
      class="arrow-svg {motionData?.color}-arrow-svg"
      class:mirrored={shouldMirror}
      style:opacity={showArrow ? 1 : 0}
    >
      <!-- ✅ FIXED: Use raw SVG content directly instead of trying to load it as an image -->
      {@html svgData.imageSrc}
    </g>
  {:else}
    <!-- Hidden but loaded arrow (positioning ready but waiting for coordination) -->
    <g opacity="0" aria-hidden="true">
      <circle
        r="2"
        fill={motionData?.color === MotionColor.BLUE ? "#2E3192" : "#ED1C24"}
        opacity="0.1"
      />
    </g>

    <!-- Debug info (if needed) -->
    {#if import.meta.env.DEV}
      <circle r="2" fill="red" opacity="0.5" />
      <text x="0" y="-25" text-anchor="middle" font-size="6" fill="black">
        {motionData?.arrowLocation}
      </text>
    {/if}
  {/if}
</g>

<style>
  .arrow-group {
    transition: all 0.2s ease;
    transform-origin: center;
  }

  .arrow-group.loaded {
    opacity: 1;
  }

  .arrow-svg {
    pointer-events: none;
  }

  /* Ensure proper layering */
  .arrow-group {
    z-index: 2;
  }
</style>
