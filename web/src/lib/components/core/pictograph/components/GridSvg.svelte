<!--
Grid.svelte - Modern Rune-Based Grid Component

Renders the diamond or box grid background using real SVG assets.
Uses pure runes instead of stores for reactivity.
-->
<script lang="ts">
  import { GridMode } from "$domain";
  import { createGridPointData } from "$domain";

  interface Props {
    /** Grid mode - diamond or box */
    gridMode?: GridMode;
    /** Called when grid is successfully loaded */
    onLoaded?: () => void;
    /** Called when grid loading fails */
    onError?: (error: string) => void;
  }

  let { gridMode = GridMode.DIAMOND, onLoaded, onError }: Props = $props();

  // State using runes
  let isLoaded = $state(false);
  let hasError = $state(false);
  let errorMessage = $state<string | null>(null);

  // Load grid SVG as native content for better performance
  async function loadGridSvg(): Promise<string> {
    try {
      const response = await fetch(`/images/grid/${gridMode}_grid.svg`);
      if (!response.ok) throw new Error(`Failed to load ${gridMode} grid`);

      const svgText = await response.text();

      // Mark as loaded
      isLoaded = true;
      hasError = false;
      errorMessage = null;
      onLoaded?.();

      return svgText;
    } catch (error) {
      hasError = true;
      errorMessage = `Failed to load ${gridMode} grid`;
      onError?.(errorMessage);
      throw error;
    }
  }

  // Derived state - grid data for positioning (in case parent components need it)
  const gridData = $derived(() => {
    return createGridPointData(gridMode);
  });

  // Initialize loading state when grid mode changes
  $effect(() => {
    isLoaded = false;
    hasError = false;
    errorMessage = null;
  });

  // Cleanup - removed unused image handlers since we're using native SVG

  // Fallback grid rendering using coordinates
  const fallbackGridPath = $derived(() => {
    const data = gridData();

    if (gridMode === GridMode.DIAMOND) {
      // Create diamond shape from hand points
      const points = [
        data.allHandPointsNormal.n_diamond_hand_point?.coordinates,
        data.allHandPointsNormal.e_diamond_hand_point?.coordinates,
        data.allHandPointsNormal.s_diamond_hand_point?.coordinates,
        data.allHandPointsNormal.w_diamond_hand_point?.coordinates,
      ].filter(Boolean);

      if (points.length === 4) {
        return `M ${points[0]!.x},${points[0]!.y} L ${points[1]!.x},${points[1]!.y} L ${points[2]!.x},${points[2]!.y} L ${points[3]!.x},${points[3]!.y} Z`;
      }
    } else {
      // Create box shape from hand points
      const points = [
        data.allHandPointsNormal.nw_box_hand_point?.coordinates,
        data.allHandPointsNormal.ne_box_hand_point?.coordinates,
        data.allHandPointsNormal.se_box_hand_point?.coordinates,
        data.allHandPointsNormal.sw_box_hand_point?.coordinates,
      ].filter(Boolean);

      if (points.length === 4) {
        return `M ${points[0]!.x},${points[0]!.y} L ${points[1]!.x},${points[1]!.y} L ${points[2]!.x},${points[2]!.y} L ${points[3]!.x},${points[3]!.y} Z`;
      }
    }

    // Ultimate fallback - simple centered shape
    const center = { x: 475, y: 475 };
    const size = 143;

    if (gridMode === GridMode.DIAMOND) {
      return `M ${center.x},${center.y - size} L ${center.x + size},${center.y} L ${center.x},${center.y + size} L ${center.x - size},${center.y} Z`;
    } else {
      return `M ${center.x - size},${center.y - size} L ${center.x + size},${center.y - size} L ${center.x + size},${center.y + size} L ${center.x - size},${center.y + size} Z`;
    }
  });
</script>

<!-- Grid Group -->
<g
  class="grid"
  class:grid-loaded={isLoaded}
  class:grid-error={hasError}
  data-grid-mode={gridMode}
>
  {#if !hasError}
    <!-- Native SVG grid for better performance -->
    {#await loadGridSvg() then gridSvgContent}
      <g class="grid-svg">
        {@html gridSvgContent}
      </g>
    {:catch}
      <!-- Fallback grid rendering -->
      <g class="fallback-grid">
        <path
          d={fallbackGridPath()}
          fill="none"
          stroke="#e5e7eb"
          stroke-width="2"
          stroke-dasharray="5,5"
        />

        <!-- Center point -->
        <circle cx="475" cy="475" r="3" fill="#9ca3af" />
      </g>
    {/await}
  {:else}
    <!-- Error fallback -->
    <g class="fallback-grid">
      <path
        d={fallbackGridPath()}
        fill="none"
        stroke="#e5e7eb"
        stroke-width="2"
        stroke-dasharray="5,5"
      />

      <!-- Center point -->
      <circle cx="475" cy="475" r="3" fill="#9ca3af" />
    </g>
  {/if}
</g>

<style>
  .grid {
    /* Grid is rendered first, so it's in the background */
    z-index: 1;
  }

  .grid-loaded {
    opacity: 1;
    transition: opacity 0.3s ease;
  }

  .grid-error .fallback-grid {
    opacity: 0.7;
  }

  .fallback-grid path {
    animation: dash 2s linear infinite;
  }

  @keyframes dash {
    to {
      stroke-dashoffset: -10;
    }
  }
</style>
