<!--
PositionGlyph.svelte - Position Glyph Component

Renders start → end position indicators showing position groups (α, β, Γ)
centered at the top of pictographs. Not shown for static letters (α, β, Γ).

Based on legacy start_to_end_pos_glyph.py implementation.
-->
<script lang="ts">
  import { GridPosition } from "../../grid/domain/enums/grid-enums";
  import { Letter } from "../../../foundation/domain/models/Letter";

  let {
    startPosition = null,
    endPosition = null,
    letter = null,
    hasValidData = true,
  } = $props<{
    /** Start position */
    startPosition?: GridPosition | null;
    /** End position */
    endPosition?: GridPosition | null;
    /** The letter (to filter out static letters) */
    letter?: Letter | null;
    /** Whether the pictograph has valid data */
    hasValidData?: boolean;
  }>();

  // Static letters that don't show position glyph
  const STATIC_LETTERS = [Letter.ALPHA, Letter.BETA, Letter.GAMMA];

  // Extract position group (alpha/beta/gamma) from position string
  function extractPositionGroup(position: GridPosition | null): string | null {
    if (!position) return null;
    // Extract alphabetic characters (e.g., "alpha1" -> "alpha")
    const match = position.match(/[a-z]+/i);
    return match ? match[0].toLowerCase() : null;
  }

  // Only render if we have valid positions and it's not a static letter
  const shouldRender = $derived.by(() => {
    if (!hasValidData || !startPosition || !endPosition) {
      return false;
    }
    // Don't show for static letters (α, β, Γ)
    if (letter && STATIC_LETTERS.includes(letter)) {
      return false;
    }
    return true;
  });

  const startGroup = $derived.by(() => extractPositionGroup(startPosition));
  const endGroup = $derived.by(() => extractPositionGroup(endPosition));

  // Positioning based on legacy start_to_end_pos_glyph.py:
  // - Scale factor: 0.75
  // - Spacing between elements: 25px
  // - Centered horizontally, positioned at y=50
  // - Standard pictograph size is 950x950 (viewBox)
  const PICTOGRAPH_SIZE = 950;
  const SCALE_FACTOR = 0.75;
  const SPACING = 25;
  const Y_POSITION = 50;

  // SVG paths mapping
  const GROUP_TO_SVG: Record<string, string> = {
    alpha: "/images/letters_trimmed/Type6/α.svg",
    beta: "/images/letters_trimmed/Type6/β.svg",
    gamma: "/images/letters_trimmed/Type6/Γ.svg",
  };

  // Actual SVG viewBox dimensions from the source files
  const LETTER_DIMENSIONS = {
    alpha: { width: 92.22, height: 100, yOffset: 10.08 },
    beta: { width: 66.05, height: 100, yOffset: -0.09 },
    gamma: { width: 79, height: 100.11, yOffset: -0.01 },
  } as const;

  // Y-offsets to align visual centers of letters
  // Positive values shift DOWN, negative values shift UP
  // Manually tuned based on visual inspection
  const GROUP_Y_OFFSETS = {
    alpha: 10.0,     // Visual center is ABOVE geometric center - shift DOWN
    beta: 0.0,       // Reference baseline
    gamma: 0.0,      // Reference baseline
  } as const;

  const startSvgPath = $derived.by(() => {
    return startGroup ? GROUP_TO_SVG[startGroup] : "";
  });

  const endSvgPath = $derived.by(() => {
    return endGroup ? GROUP_TO_SVG[endGroup] : "";
  });

  const arrowSvgPath = "/images/arrow.svg";

  const ARROW_WIDTH = 88.9;
  const ARROW_HEIGHT = 34.8;

  // Use a consistent height for all letters (they all have height ~100)
  const LETTER_HEIGHT = 100;
  // Use the widest letter for consistent spacing
  const LETTER_WIDTH = Math.max(...Object.values(LETTER_DIMENSIONS).map(d => d.width));

  // Scaled dimensions
  const scaledLetterWidth = LETTER_WIDTH * SCALE_FACTOR;
  const scaledLetterHeight = LETTER_HEIGHT * SCALE_FACTOR;
  const scaledArrowWidth = ARROW_WIDTH * SCALE_FACTOR;
  const scaledArrowHeight = ARROW_HEIGHT * SCALE_FACTOR;

  // Calculate a common center line for vertical alignment
  // All elements should have their CENTER aligned on the same horizontal line
  const centerLine = scaledLetterHeight / 2;

  // Calculate positions - position each element so its center aligns with centerLine
  // Apply manual offsets to compensate for different viewBox y-values
  const startYOffset = $derived.by(() => {
    if (!startGroup) return 0;
    return GROUP_Y_OFFSETS[startGroup as keyof typeof GROUP_Y_OFFSETS] || 0;
  });

  const endYOffset = $derived.by(() => {
    if (!endGroup) return 0;
    return GROUP_Y_OFFSETS[endGroup as keyof typeof GROUP_Y_OFFSETS] || 0;
  });

  // Start letter - centered vertically on centerLine
  const startX = 0;
  const startY = $derived(centerLine - (scaledLetterHeight / 2) + startYOffset); // Center on line + viewBox compensation

  // Arrow - centered vertically with the letters
  const arrowX = scaledLetterWidth + SPACING * SCALE_FACTOR;
  const arrowY = centerLine - (scaledArrowHeight / 2);

  // End letter - centered vertically on centerLine
  const endX = scaledLetterWidth + scaledArrowWidth + SPACING;
  const endY = $derived(centerLine - (scaledLetterHeight / 2) + endYOffset); // Center on line + viewBox compensation

  // Calculate total width for centering
  const totalWidth = scaledLetterWidth + scaledArrowWidth + scaledLetterWidth + SPACING;
  const groupX = PICTOGRAPH_SIZE / 2 - totalWidth / 2;
</script>

{#if shouldRender}
  <g class="position-glyph" transform="translate({groupX}, {Y_POSITION})">
    <!-- Start position letter -->
    {#if startSvgPath}
      <image
        href={startSvgPath}
        x={startX}
        y={startY}
        width={scaledLetterWidth}
        height={scaledLetterHeight}
        aria-label={`Start position: ${startGroup}`}
      />
    {/if}

    <!-- Arrow -->
    <image
      href={arrowSvgPath}
      x={arrowX}
      y={arrowY}
      width={scaledArrowWidth}
      height={scaledArrowHeight}
      aria-label="to"
    />

    <!-- End position letter -->
    {#if endSvgPath}
      <image
        href={endSvgPath}
        x={endX}
        y={endY}
        width={scaledLetterWidth}
        height={scaledLetterHeight}
        aria-label={`End position: ${endGroup}`}
      />
    {/if}
  </g>
{/if}
