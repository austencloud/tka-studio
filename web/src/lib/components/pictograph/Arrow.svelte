<!--
Arrow Component - Renders SVG arrows with proper positioning and natural sizing
Follows the same pattern as Prop component for consistent sizing behavior
-->
<script lang="ts">
  import type { ArrowData, MotionData } from "$lib/domain";
  import { onMount } from "svelte";

  interface Props {
    arrowData: ArrowData;
    motionData?: MotionData; // MotionData from pictograph
    preCalculatedPosition?:
      | { x: number; y: number; rotation: number }
      | undefined; // Pre-calculated position from parent
    preCalculatedMirroring?: boolean | undefined; // Pre-calculated mirroring from parent
    showArrow?: boolean; // Whether to show the arrow (coordination flag)
    onLoaded?: (componentType: string) => void;
    onError?: (componentType: string, error: string) => void;
  }

  let {
    arrowData,
    motionData,
    preCalculatedPosition,
    preCalculatedMirroring,
    showArrow = true,
    onLoaded,
    onError,
  }: Props = $props();

  let loaded = $state(false);
  let error = $state<string | null>(null);
  let svgData = $state<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } | null>(null);

  // SINGLE SOURCE OF TRUTH: Use ONLY pre-calculated positions from ArrowPositioningOrchestrator
  const position = $derived(() => {
    if (!arrowData) return { x: 475.0, y: 475.0, rotation: 0 };

    // ONLY use preCalculatedPosition - no more redundant calculations!
    if (preCalculatedPosition) {
      return preCalculatedPosition;
    }

    // Fallback: use position data from arrowData if available (for legacy compatibility)
    if (arrowData.position_x !== 0 || arrowData.position_y !== 0) {
      return {
        x: arrowData.position_x,
        y: arrowData.position_y,
        rotation: arrowData.rotation_angle || 0,
      };
    }

    // Final fallback: center position
    console.warn(
      `⚠️ Arrow.svelte: No position data available for ${arrowData.color}, using center fallback`
    );
    return { x: 475.0, y: 475.0, rotation: 0 };
  });

  // SINGLE SOURCE OF TRUTH: Use only the position from the derived function
  const calculatedPosition = $derived(() => position());
  const shouldMirror = $derived(() => preCalculatedMirroring ?? false);

  // Get arrow SVG path based on motion type and properties
  const arrowPath = $derived(() => {
    if (!arrowData || !motionData) {
      console.warn(
        "🚫 Arrow.svelte: Missing arrowData or motionData, cannot determine arrow path"
      );
      return null;
    }

    const { motion_type, turns } = motionData;
    const baseDir = `/images/arrows/${motion_type}`;

    // For motion types that have turn-based subdirectories (pro, anti, static)
    if (["pro", "anti", "static"].includes(motion_type)) {
      // Determine if we should use radial vs non-radial arrows
      // Use non-radial only for clock/counter orientations, radial for everything else
      const startOri =
        arrowData.start_orientation || motionData.start_ori || "in";
      const endOri = arrowData.end_orientation || motionData.end_ori || "in";

      const isNonRadial =
        startOri === "clock" ||
        startOri === "counter" ||
        endOri === "clock" ||
        endOri === "counter";

      const subDir = isNonRadial ? "from_nonradial" : "from_radial";
      const turnValue = typeof turns === "number" ? turns.toFixed(1) : "0.0";
      const path = `${baseDir}/${subDir}/${motion_type}_${turnValue}.svg`;

      return path;
    }

    // For simple motion types (dash, float) - use base directory
    const path = `${baseDir}.svg`;
    return path;
  });

  // Parse SVG to get proper dimensions and center point (same as Prop component)
  const parseArrowSvg = (
    svgText: string
  ): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } => {
    const doc = new DOMParser().parseFromString(svgText, "image/svg+xml");
    const svg = doc.documentElement;

    // Get viewBox dimensions
    const viewBoxValues = svg.getAttribute("viewBox")?.split(/\s+/) || [
      "0",
      "0",
      "100",
      "100",
    ];
    const viewBox = {
      width: parseFloat(viewBoxValues[2] || "100") || 100,
      height: parseFloat(viewBoxValues[3] || "100") || 100,
    };

    // Get center point from SVG
    let center = { x: viewBox.width / 2, y: viewBox.height / 2 };

    try {
      const centerElement = doc.getElementById("centerPoint");
      if (centerElement) {
        center = {
          x: parseFloat(centerElement.getAttribute("cx") || "0") || center.x,
          y: parseFloat(centerElement.getAttribute("cy") || "0") || center.y,
        };
      }
    } catch {
      // SVG center calculation failed, using default center
    }

    return { viewBox, center };
  };

  // Apply color transformation to SVG content (same as Prop component)
  const applyColorToSvg = (svgText: string, color: "blue" | "red"): string => {
    const colorMap = new Map([
      ["blue", "#2E3192"],
      ["red", "#ED1C24"],
    ]);

    const targetColor = colorMap.get(color) || "#2E3192";

    // Use regex replacement to change fill colors directly
    let coloredSvg = svgText.replace(
      /fill="#[0-9A-Fa-f]{6}"/g,
      `fill="${targetColor}"`
    );
    coloredSvg = coloredSvg.replace(
      /fill:\s*#[0-9A-Fa-f]{6}/g,
      `fill:${targetColor}`
    );

    // Remove the centerPoint circle entirely to prevent unwanted visual elements
    coloredSvg = coloredSvg.replace(
      /<circle[^>]*id="centerPoint"[^>]*\/?>/,
      ""
    );

    return coloredSvg;
  };

  // Load SVG data (same pattern as Prop component)
  const loadSvg = async () => {
    try {
      if (!arrowData) throw new Error("No arrow data available");

      const path = arrowPath();
      if (!path)
        throw new Error("No arrow path available - missing motion data");

      const response = await fetch(path);
      if (!response.ok) throw new Error("Failed to fetch SVG");

      const originalSvgText = await response.text();
      const { viewBox, center } = parseArrowSvg(originalSvgText);

      // Apply color transformation to the SVG
      const coloredSvgText = applyColorToSvg(
        originalSvgText,
        arrowData.color as "blue" | "red"
      );

      svgData = {
        imageSrc: `data:image/svg+xml;base64,${btoa(coloredSvgText)}`,
        viewBox,
        center,
      };

      loaded = true;
      onLoaded?.(`${arrowData?.color}-arrow`);
    } catch (e) {
      error = `Failed to load arrow SVG: ${e}`;
      onError?.(`${arrowData?.color}-arrow`, error);
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
  class="arrow-group {arrowData?.color}-arrow"
  class:loaded
  data-arrow-color={arrowData?.color}
  data-motion-type={motionData?.motion_type}
  data-location={arrowData?.location}
>
  {#if error}
    <!-- Error state -->
    <circle r="10" fill="red" opacity="0.5" />
    <text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
  {:else if !arrowPath()}
    <!-- No arrow path available (missing motion data) -->
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
      fill={arrowData?.color === "blue" ? "#2E3192" : "#ED1C24"}
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
    <image
      href={svgData.imageSrc}
      transform="
				translate({calculatedPosition().x}, {calculatedPosition().y})
				rotate({calculatedPosition().rotation || arrowData?.rotation_angle || 0})
				scale({shouldMirror() ? -1 : 1}, 1)
				translate({-svgData.center.x}, {-svgData.center.y})
			"
      width={svgData.viewBox.width}
      height={svgData.viewBox.height}
      preserveAspectRatio="xMidYMid meet"
      class="arrow-svg {arrowData?.color}-arrow-svg"
      class:mirrored={shouldMirror}
      style:opacity={showArrow ? 1 : 0}
      onerror={() => {
        error = "Failed to load arrow SVG";
        onError?.(`${arrowData?.color}-arrow`, error);
      }}
      onload={() => {
        // SVG loaded - no debug logging needed for performance
      }}
    />
  {:else}
    <!-- Hidden but loaded arrow (positioning ready but waiting for coordination) -->
    <g opacity="0" aria-hidden="true">
      <circle
        r="2"
        fill={arrowData?.color === "blue" ? "#2E3192" : "#ED1C24"}
        opacity="0.1"
      />
    </g>

    <!-- Debug info (if needed) -->
    {#if import.meta.env.DEV}
      <circle r="2" fill="red" opacity="0.5" />
      <text x="0" y="-25" text-anchor="middle" font-size="6" fill="black">
        {arrowData?.location}
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
