<!--
VTGGlyph.svelte - VTG Glyph Component

Renders VTG mode glyphs (SS, SO, TS, TO, QS, QO) in the bottom-right corner
of pictographs. Only displays for Type1 letters.

Based on legacy vtg_glyph.py and vtg_glyph_renderer.py implementations.
-->
<script lang="ts">
  import type { VTGMode } from "../domain/enums";
  import { LetterType } from "../../../foundation/domain/models/LetterType";
  import { type Letter, getLetterType } from "../../../foundation/domain/models/Letter";

  let {
    vtgMode = null,
    letter = null,
    hasValidData = true,
  } = $props<{
    /** The VTG mode to display (SS, SO, TS, TO, QS, QO) */
    vtgMode?: VTGMode | null;
    /** The letter (used to check if Type1) */
    letter?: Letter | null;
    /** Whether the pictograph has valid data */
    hasValidData?: boolean;
  }>();

  // Only render for Type1 letters with valid VTG mode
  const shouldRender = $derived.by(() => {
    if (!hasValidData || !vtgMode) {
      return false;
    }
    // Only show for Type1 letters
    if (letter && getLetterType(letter) !== LetterType.TYPE1) {
      return false;
    }
    return true;
  });

  // SVG path - VTG glyphs are in static/images/vtg_glyphs/
  const svgPath = $derived.by(() => {
    if (!vtgMode) return "";
    return `/images/vtg_glyphs/${vtgMode}.svg`;
  });

  // Positioning based on legacy vtg_glyph_renderer.py:
  // - 4% offset from edges
  // - Positioned in bottom-right corner
  // - Standard pictograph size is 950x950 (viewBox)
  const PICTOGRAPH_SIZE = 950;
  const OFFSET_PERCENTAGE = 0.04;

  // VTG glyph dimensions (from actual SVG viewBox: 201.24 x 133.6)
  const GLYPH_WIDTH = 201.24;
  const GLYPH_HEIGHT = 133.6;

  const offsetWidth = PICTOGRAPH_SIZE * OFFSET_PERCENTAGE;
  const offsetHeight = PICTOGRAPH_SIZE * OFFSET_PERCENTAGE;

  // Position in bottom-right corner
  const xPosition = PICTOGRAPH_SIZE - GLYPH_WIDTH - offsetWidth;
  const yPosition = PICTOGRAPH_SIZE - GLYPH_HEIGHT - offsetHeight;
</script>

{#if shouldRender}
  <g class="vtg-glyph">
    <image
      href={svgPath}
      x={xPosition}
      y={yPosition}
      width={GLYPH_WIDTH}
      height={GLYPH_HEIGHT}
      aria-label={`VTG mode: ${vtgMode}`}
    />
  </g>
{/if}
