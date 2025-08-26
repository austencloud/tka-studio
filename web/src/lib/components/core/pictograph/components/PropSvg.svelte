<script lang="ts">
  import type { MotionData, PictographData } from "$lib/domain";
  import { resolve } from "$lib/services/bootstrap";
  import { IPropCoordinatorServiceInterface } from "$lib/services/di/interfaces/core-interfaces";
  import type { IPropCoordinatorService } from "$lib/services/implementations/rendering/PropCoordinatorService";
  interface Props {
    motionData: MotionData; // Single source of truth - contains embedded prop placement data
    pictographData: PictographData; // ✅ SIMPLIFIED: Complete pictograph data contains gridMode
  }

  interface RenderData {
    position: { x: number; y: number };
    rotation: number;
    svgData: {
      svgContent: string;
      viewBox: { width: number; height: number };
      center: { x: number; y: number };
    } | null;
    loaded: boolean;
  }

  let { motionData, pictographData }: Props = $props();

  // Derive color from motionData (single source of truth)
  const color = $derived(motionData.color);

  // Debug logging removed for performance

  // Native SVG content scales automatically with the parent SVG container
  // No manual scaling needed - the 950x950 coordinate system handles this naturally

  const propCoordinator: IPropCoordinatorService = resolve(
    IPropCoordinatorServiceInterface
  );

  let renderData = $state<RenderData>({
    position: { x: 475, y: 475 },
    rotation: 0,
    svgData: null,
    loaded: false,
  });

  $effect(() => {
    if (!motionData || !motionData.propPlacementData) return;

    // Use async function inside effect
    const loadPropData = async () => {
      try {
        // Use the actual PropCoordinatorService to load real prop SVGs
        const propRenderData = await propCoordinator.calculatePropRenderData(
          motionData.propPlacementData,
          motionData,
          pictographData
        );

        renderData = propRenderData;
      } catch (error) {
        console.error("❌ PropSvg: Error loading prop data:", error);

        // Fallback to mock render data if service fails
        const fallbackRenderData = {
          position: {
            x: motionData.propPlacementData.positionX || 475,
            y: motionData.propPlacementData.positionY || 475,
          },
          rotation: motionData.propPlacementData.rotationAngle || 0,
          svgData: {
            svgContent: `<svg viewBox="0 0 100 100"><rect x="25" y="10" width="50" height="80" fill="${motionData.color === "blue" ? "#2E3192" : "#ED1C24"}"/></svg>`,
            viewBox: { width: 100, height: 100 },
            center: { x: 50, y: 50 },
          },
          loaded: true,
          error: error instanceof Error ? error.message : "Unknown error",
        };

        renderData = fallbackRenderData;
      }
    };

    loadPropData();
  });
</script>

<g
  class="prop-group {color}-prop"
  data-prop-color={color}
  data-prop-type={motionData?.propType}
  data-location={motionData?.endLocation}
>
  {#if renderData.svgData}
    <!-- Native SVG with proper scaling to match image behavior -->
    <g
      transform="
        translate({renderData.position.x}, {renderData.position.y})
        rotate({renderData.rotation})
        translate({-renderData.svgData.center.x}, {-renderData.svgData.center
        .y})
      "
      class="prop-svg"
    >
      {@html renderData.svgData.svgContent}
    </g>
  {/if}
</g>

<style>
  .prop-group {
    transition: all 0.2s ease;
    transform-origin: center;
    z-index: 1;
  }

  .prop-svg {
    pointer-events: none;
  }
</style>
