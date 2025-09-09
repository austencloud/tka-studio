<!--
Arrow Component - Purely presentational arrow rendering
REFACTORED: Uses ArrowLifecycleManager for all business logic, purely presentational
-->
<script lang="ts">
  import { MotionColor, type MotionData, type PictographData } from "$shared";
  import type { ArrowAssets, ArrowPosition } from "$shared/pictograph/arrow";

  interface Props {
    motionData: MotionData;
    pictographData: PictographData;
    arrowAssets?: ArrowAssets | null; // Pre-loaded assets from lifecycle manager
    arrowPosition?: ArrowPosition | null; // Pre-calculated position from lifecycle manager
    shouldMirror?: boolean; // Pre-calculated mirroring from lifecycle manager
    showArrow?: boolean; // Visibility coordination flag
    onLoaded?: (componentType: string) => void;
    onError?: (componentType: string, error: string) => void;
  }

  let {
    motionData,
    pictographData,
    arrowAssets = null,
    arrowPosition = null,
    shouldMirror = false,
    showArrow = true,
    onLoaded,
    onError,
  }: Props = $props();

  // Purely presentational - all data comes from props
  const isReady = $derived(() => arrowAssets && arrowPosition);
  const hasError = $derived(() => !arrowAssets || !arrowPosition);

  // Notify parent when component is ready or has error
  $effect(() => {
    if (isReady()) {
      onLoaded?.(`${motionData?.color}-arrow`);
    } else if (hasError()) {
      onError?.(`${motionData?.color}-arrow`, 'Missing arrow assets or position');
    }
  });
</script>

<!-- Arrow Group -->
<g
  class="arrow-group {motionData?.color}-arrow"
  class:ready={isReady()}
  data-arrow-color={motionData?.color}
  data-motion-type={motionData?.motionType}
  data-location={motionData?.arrowLocation}
>
  {#if hasError()}
    <!-- Error state -->
    <circle r="10" fill="red" opacity="0.5" />
    <text x="0" y="4" text-anchor="middle" font-size="8" fill="white">!</text>
  {:else if !motionData}
    <!-- No motion data available -->
    <text
      x="0"
      y="4"
      text-anchor="middle"
      font-size="10"
      fill="gray"
      opacity="0.5"
    >
      No motion data
    </text>
  {:else if !isReady()}
    <!-- Loading state -->
    <circle
      r="8"
      fill={motionData?.color === MotionColor.BLUE ? "#2E3192" : "#ED1C24"}
      opacity="0.3"
    />
    <animate
      attributeName="opacity"
      values="0.3;0.8;0.3"
      dur="1s"
      repeatCount="indefinite"
    />
  {:else if showArrow && arrowAssets && arrowPosition}
    <!-- Actual arrow SVG with natural sizing and centering (same as props) -->
    <!-- Native SVG with simplified transform chain -->
    <g
      transform="
        translate({arrowPosition.x}, {arrowPosition.y})
        rotate({arrowPosition.rotation})
        scale({shouldMirror ? -1 : 1}, 1)
        translate({-arrowAssets.center.x}, {-arrowAssets.center.y})
      "
      class="arrow-svg {motionData?.color}-arrow-svg"
      class:mirrored={shouldMirror}
      style:opacity={showArrow ? 1 : 0}
    >
      <!-- ✅ FIXED: Use raw SVG content directly instead of trying to load it as an image -->
      {@html arrowAssets.imageSrc}
    </g>
  {:else}
    <!-- Hidden but loaded arrow (positioning ready but waiting for coordination) -->
    <g opacity="0" aria-hidden="true">
      <circle
        r="2"
        fill={motionData?.color === MotionColor.BLUE ? "#2E3192" : "#ED1C24"}
        opacity="0.1"
      />
    </g>

    <!-- Debug info removed to prevent red rectangle artifacts -->
  {/if}
</g>

<style>
  .arrow-group {
    transition: all 0.2s ease;
    transform-origin: center;
  }

  .arrow-group.loaded {
    opacity: 1;
  }

  .arrow-svg {
    pointer-events: none;
  }

  /* Ensure proper layering */
  .arrow-group {
    z-index: 2;
  }
</style>
