<!--
GlyphRenderer.svelte - Renders TKAGlyph to SVG for canvas conversion

This component renders a complete TKAGlyph (letter + turns + future same/opp dots)
as an SVG element, which can then be serialized and converted to an image for
canvas rendering. This ensures the entire glyph fades as a unified unit.
-->
<script lang="ts">
  import TKAGlyph from "$shared/pictograph/tka-glyph/components/TKAGlyph.svelte";
  import type { PictographData, BeatData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { ITurnsTupleGeneratorService } from "$shared";
  import { onMount } from "svelte";

  // Resolve service
  const turnsTupleGenerator = resolve(
    TYPES.ITurnsTupleGeneratorService
  ) as ITurnsTupleGeneratorService;

  let {
    letter = null,
    beatData = null,
    pictographData = null,
    onSvgReady,
  } = $props<{
    letter: string | null;
    beatData?: BeatData | null;
    pictographData?: PictographData | null;
    onSvgReady?: (
      svgString: string,
      width: number,
      height: number,
      x: number,
      y: number
    ) => void;
  }>();

  // Generate turns tuple from beat data
  const turnsTuple = $derived.by(() => {
    if (!beatData || !beatData.motions?.blue || !beatData.motions?.red) {
      return "(s, 0, 0)";
    }
    return turnsTupleGenerator.generateTurnsTuple(beatData);
  });

  let svgElement: SVGSVGElement | null = $state(null);
  let isReady = $state(false);

  // When the glyph changes, serialize the SVG and notify parent
  $effect(() => {
    // Track all dependencies that should trigger re-serialization
    const currentLetter = letter;
    const currentTurnsTuple = turnsTuple;

    if (currentLetter && svgElement && isReady) {
      // Give the DOM a tick to fully render the TKAGlyph
      setTimeout(() => {
        serializeAndNotify();
      }, 50); // Increased timeout to ensure TKAGlyph is fully rendered
    }
  });

  onMount(() => {
    isReady = true;
  });

  async function serializeAndNotify() {
    if (!svgElement || !onSvgReady) {
      return;
    }

    try {
      // Get the bounding box of the glyph group
      const glyphGroup = svgElement.querySelector(".tka-glyph");
      if (!glyphGroup) {
        return;
      }

      const bbox = (glyphGroup as SVGGraphicsElement).getBBox();

      // TKAGlyph has transform="translate(50, 800)", so bbox is relative to that transform
      // We need to get the actual position in the 950px viewBox coordinate system
      // The glyph is positioned at (50, 800) by default in TKAGlyph.svelte
      const glyphBaseX = 50;
      const glyphBaseY = 800;

      // The actual position in the viewBox is the base position plus the bbox offset
      const viewBoxX = glyphBaseX + bbox.x;
      const viewBoxY = glyphBaseY + bbox.y;
      const viewBoxWidth = bbox.width;
      const viewBoxHeight = bbox.height;

      // Create a new SVG with proper viewBox for just the glyph
      const svgCopy = svgElement.cloneNode(true) as SVGSVGElement;

      // CRITICAL FIX: Inline external SVG images
      // When SVG is converted to data URL and drawn to canvas, external resources
      // (like <image href="...">) are blocked for security reasons.
      // We must fetch and inline the SVG content directly.
      const imageElements = svgCopy.querySelectorAll("image");

      for (const img of imageElements) {
        const href = img.getAttribute("href");
        if (href && href.endsWith(".svg")) {
          try {
            const response = await fetch(href);
            const svgText = await response.text();

            // Parse the external SVG
            const parser = new DOMParser();
            const externalSvgDoc = parser.parseFromString(
              svgText,
              "image/svg+xml"
            );
            const externalSvgRoot = externalSvgDoc.documentElement;

            // Create a <g> wrapper to preserve the image's position and size
            const g = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "g"
            );

            // Copy image attributes to the group
            const x = parseFloat(img.getAttribute("x") || "0");
            const y = parseFloat(img.getAttribute("y") || "0");
            const width = parseFloat(img.getAttribute("width") || "100");
            const height = parseFloat(img.getAttribute("height") || "100");

            // Get the external SVG's viewBox
            const viewBox = externalSvgRoot.getAttribute("viewBox");
            let scaleX = 1;
            let scaleY = 1;

            if (viewBox) {
              const [, , vbWidth, vbHeight] = viewBox
                .split(" ")
                .map(parseFloat);
              if (vbWidth && vbHeight) {
                scaleX = width / vbWidth;
                scaleY = height / vbHeight;
              }
            }

            // Apply transform to position and scale the inlined content
            g.setAttribute(
              "transform",
              `translate(${x}, ${y}) scale(${scaleX}, ${scaleY})`
            );

            // Copy all children from external SVG to the group
            while (externalSvgRoot.firstChild) {
              g.appendChild(externalSvgRoot.firstChild);
            }

            // Replace the <image> with the <g>
            img.parentNode?.replaceChild(g, img);
          } catch (error) {
            console.error("[GlyphRenderer] Failed to inline SVG:", href, error);
          }
        }
      }

      // CRITICAL FIX: Set viewBox to the FULL 950x950 pictograph space
      // This ensures the glyph appears in the correct position when rendered to canvas
      // The canvas will show the entire pictograph area, with the glyph at the bottom left
      svgCopy.setAttribute("viewBox", "0 0 950 950");
      svgCopy.setAttribute("width", "950");
      svgCopy.setAttribute("height", "950");

      const serializer = new XMLSerializer();
      const svgString = serializer.serializeToString(svgCopy);

      if (onSvgReady) {
        // Pass the glyph bbox dimensions so AnimatorCanvas knows where to draw it
        // The SVG viewBox is the full 950x950, but we tell the canvas where the glyph is within that space
        onSvgReady(svgString, viewBoxWidth, viewBoxHeight, viewBoxX, viewBoxY);
      } else {
        console.error("[GlyphRenderer] onSvgReady callback is not defined!");
      }
    } catch (error) {
      console.error("[GlyphRenderer] Failed to serialize glyph SVG:", error);
    }
  }
</script>

<!-- Hidden SVG container for rendering the glyph -->
<svg
  bind:this={svgElement}
  xmlns="http://www.w3.org/2000/svg"
  style="position: absolute; left: -9999px; top: -9999px; width: 950px; height: 950px;"
  viewBox="0 0 950 950"
>
  {#if letter}
    <TKAGlyph {letter} {turnsTuple} {pictographData} x={50} y={800} scale={1} />
  {/if}
</svg>
