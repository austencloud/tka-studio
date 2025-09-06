<!--
PictographSvg.svelte - SVG Rendering Component

Handles the actual SVG rendering of the pictograph content.
This component is focused solely on rendering the SVG elements
and leaves state management to the parent component.
-->
<script lang="ts">
	import TKAGlyph from './TKAGlyph.svelte';
	import ArrowSvg from './ArrowSvg.svelte';
  import {
    GridMode,
    type MotionColor,
    type MotionData,
    type PictographData,
  } from "../../domain";
  import { resolve, TYPES } from "../../inversify";
  import type { IGridModeDeriver } from "../services";
  import GridSvg from "./GridSvg.svelte";
  import PropSvg from "./PropSvg.svelte";

  interface Props {
    /** Pictograph data to render */
    pictographData: PictographData | null;
    /** Whether we have valid data to render */
    hasValidData: boolean;
    /** Display letter for glyph */
    displayLetter: string | null;
    /** Motions to render (embedded approach) */
    motionsToRender: Array<{ color: MotionColor; motionData: MotionData }>;
    /** SVG dimensions */
    width: number | string;
    height: number | string;
    /** SVG viewBox */
    viewBox: string;
    /** Arrow positioning state */
    arrowPositions: Record<string, { x: number; y: number; rotation: number }>;
    arrowMirroring: Record<string, boolean>;
    showArrows: boolean;
    /** Event handlers */
    onComponentLoaded: (componentName: string) => void;
    onComponentError: (componentName: string, error: string) => void;
    /** Accessibility */
    ariaLabel: string;
  }

  let {
    pictographData,
    hasValidData,
    displayLetter,
    motionsToRender,
    width,
    height,
    viewBox,
    arrowPositions,
    arrowMirroring,
    showArrows,
    onComponentLoaded,
    onComponentError,
    ariaLabel,
  }: Props = $props();

  // Derive grid mode from pictograph data using Svelte 5 runes
  const gridMode = $derived(
    (() => {
      if (
        !pictographData ||
        !pictographData.motions?.blue ||
        !pictographData.motions?.red
      ) {
        return GridMode.DIAMOND; // Default fallback
      }

      try {
        const gridModeService = resolve<IGridModeDeriver>(
          TYPES.IGridModeDeriver
        );
        return gridModeService.deriveGridMode(
          pictographData.motions.blue,
          pictographData.motions.red
        );
      } catch (error) {
        console.warn("Failed to derive grid mode, using default:", error);
        return GridMode.DIAMOND; // Fallback to default on error
      }
    })()
  );

  // ✅ REMOVED: High-level beta calculation - now handled in PropPlacementService with complete pictograph data
</script>

<svg
  {width}
  {height}
  {viewBox}
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label={ariaLabel}
>
  <!-- Background -->
  <rect width="950" height="950" fill="white" />

  {#if hasValidData}
    <!-- Grid (always rendered first) -->
    <GridSvg
      {gridMode}
      onLoaded={() => onComponentLoaded("grid")}
      onError={(error) => onComponentError("grid", error)}
    />

    <!-- Props (rendered first so arrows appear on top) -->
    {#each motionsToRender as { color, motionData } (color)}
      {#if pictographData}
        <PropSvg {motionData} {pictographData} />
      {/if}
    {/each}

    <!-- Arrows (rendered after props) -->
    {#each motionsToRender as { color, motionData } (color)}
      <ArrowSvg
        {motionData}
        preCalculatedPosition={arrowPositions[color]}
        preCalculatedMirroring={arrowMirroring[color]}
        showArrow={showArrows}
        onLoaded={() => onComponentLoaded(`${color}-arrow`)}
        onError={(error) => onComponentError(`${color}-arrow`, error)}
      />
    {/each}

    <!-- Letter/Glyph overlay -->
    {#if displayLetter}
      <TKAGlyph letter={displayLetter} turnsTuple="(s, 0, 0)" />
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
        Empty
      </text>
    </g>
  {/if}
</svg>

<style>
  svg {
    display: block;
    box-sizing: border-box;
  }
</style>
