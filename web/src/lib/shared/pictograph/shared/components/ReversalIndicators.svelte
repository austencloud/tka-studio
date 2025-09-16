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
    if (blueReversal || redReversal) {
      console.log(`🎨 ReversalIndicators: Rendering decision:`, {
        blueReversal,
        redReversal,
        hasValidData,
        shouldRender: render
      });
    }
    return render;
  });

  // Desktop app colors (HEX_BLUE and HEX_RED from constants)
  const BLUE_COLOR = "#0066CC";  // Desktop app HEX_BLUE
  const RED_COLOR = "#CC0000";   // Desktop app HEX_RED

  // Position calculations based on desktop app logic
  const X_POSITION = 40;  // Desktop app x position
  const CENTER_Y = 500;   // Center of 1000px pictograph height
  const FONT_SIZE = 60;   // Desktop app font size
  const R_HEIGHT = FONT_SIZE * 0.8; // Approximate text height

  // Calculate vertical positions when both R's are present
  const redRY = $derived(() => {
    if (blueReversal && redReversal) {
      // Both present: stack vertically around center
      const totalHeight = R_HEIGHT * 2;
      return CENTER_Y - totalHeight / 2;
    } else if (redReversal) {
      // Only red: center it
      return CENTER_Y;
    }
    return CENTER_Y;
  });

  const blueRY = $derived(() => {
    if (blueReversal && redReversal) {
      // Both present: blue below red
      return redRY() + R_HEIGHT;
    } else if (blueReversal) {
      // Only blue: center it
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
