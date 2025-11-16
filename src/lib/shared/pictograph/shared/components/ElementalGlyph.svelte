<!--
ElementalGlyph.svelte - Elemental Glyph Component

Renders elemental symbols (water, fire, earth, air, sun, moon) in the top-right corner
of pictographs based on VTG mode classification. Only displays for Type1 letters.

Based on legacy elemental_glyph.py implementation.
-->
<script lang="ts">
  import type { ElementalType } from "../domain/enums";
  import { LetterType } from "../../../foundation/domain/models/LetterType";
  import { type Letter, getLetterType } from "../../../foundation/domain/models/Letter";

  let {
    elementalType = null,
    letter = null,
    hasValidData = true,
  } = $props<{
    /** The elemental type to display (water, fire, earth, air, sun, moon) */
    elementalType?: ElementalType | null;
    /** The letter (used to check if Type1) */
    letter?: Letter | null;
    /** Whether the pictograph has valid data */
    hasValidData?: boolean;
  }>();

  // Only render for Type1 letters with valid elemental type
  const shouldRender = $derived.by(() => {
    if (!hasValidData || !elementalType) {
      return false;
    }
    // Only show for Type1 letters
    if (letter && getLetterType(letter) !== LetterType.TYPE1) {
      return false;
    }
    return true;
  });

  // SVG path - elements are in static/images/elements/
  const svgPath = $derived.by(() => {
    if (!elementalType) return "";
    return `/images/elements/${elementalType}.svg`;
  });

  // Positioning based on legacy elemental_glyph.py:
  // - 4% offset from edges
  // - Positioned in top-right corner
  // - Standard pictograph size is 950x950 (viewBox)
  // - SVGs have natural size around 85-100px wide x 125px tall
  const PICTOGRAPH_SIZE = 950;
  const OFFSET_PERCENTAGE = 0.04;

  // Use natural SVG size (approximately 95px wide, 125px tall on average)
  // This matches the legacy behavior where boundingRect is used directly
  const GLYPH_WIDTH = 95;
  const GLYPH_HEIGHT = 125;

  const offsetWidth = PICTOGRAPH_SIZE * OFFSET_PERCENTAGE;
  const offsetHeight = PICTOGRAPH_SIZE * OFFSET_PERCENTAGE;

  // Position in top-right corner
  const xPosition = PICTOGRAPH_SIZE - GLYPH_WIDTH - offsetWidth;
  const yPosition = offsetHeight;
</script>

{#if shouldRender}
  <g class="elemental-glyph">
    <image
      href={svgPath}
      x={xPosition}
      y={yPosition}
      width={GLYPH_WIDTH}
      height={GLYPH_HEIGHT}
      aria-label={`Elemental symbol: ${elementalType}`}
    />
  </g>
{/if}
