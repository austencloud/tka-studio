<!--
BeatNumber.svelte - Beat Number Overlay Component

Renders beat numbers as SVG text overlays on pictographs.
Based on the legacy BeatNumberLabel.svelte component architecture.
-->
<script lang="ts">
  let {
    beatNumber = null,
    showBeatNumber = true,
    isStartPosition = false,
    hasValidData = true
  } = $props<{
    /** The beat number to display */
    beatNumber?: number | null;
    /** Whether to show the beat number */
    showBeatNumber?: boolean;
    /** Whether this is a start position (no beat number) */
    isStartPosition?: boolean;
    /** Whether the pictograph has valid data */
    hasValidData?: boolean;
  }>();

  // Only render if conditions are met
  const shouldRender = $derived(() => {
    return showBeatNumber && 
           !isStartPosition && 
           hasValidData && 
           beatNumber !== null;
  });
</script>

{#if shouldRender()}
  <text
    x="50"
    y="50"
    dominant-baseline="hanging"
    text-anchor="start"
    font-size="100"
    font-weight="bold"
    fill="#000"
    stroke="#fff"
    stroke-width="6"
    paint-order="stroke"
  >
    {beatNumber}
  </text>
{/if}
