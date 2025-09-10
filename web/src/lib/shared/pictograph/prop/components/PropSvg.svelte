<!--
Simple Prop Component - Just renders a prop with provided data
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
    transform="
      translate({propPosition.x}, {propPosition.y})
      rotate({propPosition.rotation})
      translate({-propAssets.center.x}, {-propAssets.center.y})
    "
    class="prop-svg {motionData.color}-prop-svg"
    data-prop-type={motionData?.propType}
  >
    {@html propAssets.imageSrc}
  </g>
{/if}

<style>
  .prop-svg {
    pointer-events: none;
  }
</style>
