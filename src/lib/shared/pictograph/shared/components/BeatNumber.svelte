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
    hasValidData = true,
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
  const shouldRender = $derived.by(() => {
    return (
      showBeatNumber &&
      !isStartPosition &&
      hasValidData &&
      beatNumber !== null &&
      beatNumber !== -1
    ); // Hide beat numbers for option picker previews
  });

  // Show "Start" text for beat number 0 (start position)
  // Note: showBeatNumber is false for start positions, but we still want to show "Start" text
  const shouldRenderStartText = $derived.by(() => {
    return hasValidData && beatNumber === 0;
  });

  // Get display text - either beat number or "Start"
  const displayText = $derived.by(() => {
    if (beatNumber === 0) {
      return "Start";
    }
    return beatNumber?.toString() || "";
  });
</script>

{#if shouldRender}
  <text
    x="50"
    y="50"
    dominant-baseline="hanging"
    text-anchor="start"
    font-size="100"
    font-family="Georgia, serif"
    font-weight="bold"
    fill="#000"
    stroke="#fff"
    stroke-width="6"
    paint-order="stroke"
  >
    {beatNumber}
  </text>
{:else if shouldRenderStartText}
  <text
    x="50"
    y="50"
    dominant-baseline="hanging"
    text-anchor="start"
    font-size="80"
    font-family="Georgia, serif"
    font-weight="bold"
    fill="#000"
    stroke="#fff"
    stroke-width="5"
    paint-order="stroke"
  >
    {displayText}
  </text>
{/if}
