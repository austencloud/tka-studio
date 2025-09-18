<!--
ReversalIndicators.svelte - Reversal Indicator Component

Renders blue and red reversal indicators as large "R" letters stacked vertically.
Based on the desktop app's ReversalGlyph implementation which shows a column of 2 R's
colored according to the motion that is reversing between pictographs.
-->
<script lang="ts">
  let {
    blueReversal = false,
    redReversal = false,
    hasValidData = true
  } = $props<{
    /** Whether to show blue reversal indicator */
    blueReversal?: boolean;
    /** Whether to show red reversal indicator */
    redReversal?: boolean;
    /** Whether the pictograph has valid data */
    hasValidData?: boolean;
  }>();

  // Only render if we have valid data and at least one reversal
  const shouldRender = $derived(() => {
    const render = hasValidData && (blueReversal || redReversal);
    return render;
  });

  // Desktop app colors (HEX_BLUE and HEX_RED from constants)
  const BLUE_COLOR = "#0066CC";  // Desktop app HEX_BLUE
  const RED_COLOR = "#CC0000";   // Desktop app HEX_RED

  // Relative positioning - scales with pictograph size
  // Using percentages of the standard 1000px pictograph dimensions
  const X_POSITION_PERCENT = 5.5;    // 5.5% from left edge
  const CENTER_Y_PERCENT = 50;     // 50% from top (center)
  const FONT_SIZE_PERCENT = 7;     // Slightly larger than before (was 6%)
  const R_SPACING_PERCENT = 7;   // Fixed spacing between R's as percentage

  // Calculate actual positions based on pictograph dimensions
  // Assuming standard SVG viewBox of 1000x1000
  const X_POSITION = X_POSITION_PERCENT * 10;  // Convert to 1000px scale
  const CENTER_Y = CENTER_Y_PERCENT * 9.7;      // Convert to 1000px scale
  const FONT_SIZE = FONT_SIZE_PERCENT * 10;    // Convert to 1000px scale
  const R_SPACING = R_SPACING_PERCENT * 10;    // Convert to 1000px scale

  // Calculate vertical positions when both R's are present
  const redRY = $derived(() => {
    if (blueReversal && redReversal) {
      // Both present: stack vertically with fixed spacing around center
      return CENTER_Y - (R_SPACING / 2);
    } else if (redReversal) {
      // Only red: center it properly (accounting for visual centering)
      return CENTER_Y;
    }
    return CENTER_Y;
  });

  const blueRY = $derived(() => {
    if (blueReversal && redReversal) {
      // Both present: blue below red with fixed spacing
      return CENTER_Y + (R_SPACING / 2);
    } else if (blueReversal) {
      // Only blue: center it properly (accounting for visual centering)
      return CENTER_Y;
    }
    return CENTER_Y;
  });
</script>

{#if shouldRender()}
  <g class="reversal-indicators">
    {#if redReversal}
      <text
        x={X_POSITION}
        y={redRY()}
        font-family="Georgia, serif"
        font-size={FONT_SIZE}
        font-weight="bold"
        fill={RED_COLOR}
        dominant-baseline="middle"
        text-anchor="start"
      >
        R
      </text>
    {/if}
    {#if blueReversal}
      <text
        x={X_POSITION}
        y={blueRY()}
        font-family="Georgia, serif"
        font-size={FONT_SIZE}
        font-weight="bold"
        fill={BLUE_COLOR}
        dominant-baseline="middle"
        text-anchor="start"
      >
        R
      </text>
    {/if}
  </g>
{/if}
