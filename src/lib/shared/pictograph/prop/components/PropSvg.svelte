<!--
Simple Prop Component - Just renders a prop with provided data
Now with smooth transitions when position or orientation changes!
-->
<script lang="ts">
  import type { MotionData } from "$shared";
  import type { PropAssets, PropPosition } from "../domain/models";

  let {
    motionData,
    propAssets,
    propPosition,
    showProp = true,
  } = $props<{
    motionData: MotionData;
    propAssets: PropAssets;
    propPosition: PropPosition;
    showProp?: boolean;
  }>();
</script>

{#if showProp}
  <g
    class="prop-svg {motionData.color}-prop-svg"
    data-prop-type={motionData?.propType}
    style="
      transform: translate({propPosition.x}px, {propPosition.y}px)
                 rotate({propPosition.rotation}deg)
                 translate({-propAssets.center.x}px, {-propAssets.center.y}px);
    "
  >
    {@html propAssets.imageSrc}
  </g>
{/if}

<style>
  .prop-svg {
    pointer-events: none;
    /* Smooth transition for position and rotation changes - matches arrow behavior */
    /* IMPORTANT: transform must be a CSS property (not SVG attribute) for transitions to work */
    transition: transform 0.2s ease;
  }
</style>
