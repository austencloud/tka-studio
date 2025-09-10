<!--
Simple Arrow Component - Just renders an arrow with provided data
-->
<script lang="ts">
  import type { MotionData } from "$shared";
  import type { ArrowAssets, ArrowPosition } from "$shared/pictograph/arrow";

  let {
    motionData,
    arrowAssets,
    arrowPosition,
    shouldMirror = false,
    showArrow = true,
  } = $props<{
    motionData: MotionData;
    arrowAssets: ArrowAssets;
    arrowPosition: ArrowPosition;
    shouldMirror?: boolean;
    showArrow?: boolean;
  }>();
</script>

{#if showArrow}
  <g
    transform="
      translate({arrowPosition.x}, {arrowPosition.y})
      rotate({arrowPosition.rotation})
      translate({-arrowAssets.center.x}, {-arrowAssets.center.y})
      {shouldMirror ? 'scale(-1, 1)' : ''}
    "
    class="arrow-svg {motionData.color}-arrow-svg"
    class:mirrored={shouldMirror}
  >
    {@html arrowAssets.imageSrc}
  </g>
{/if}

<style>
  .arrow-svg {
    pointer-events: none;
  }
</style>
