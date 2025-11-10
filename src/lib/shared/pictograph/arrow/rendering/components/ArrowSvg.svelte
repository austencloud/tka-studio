<!--
Simple Arrow Component - Just renders an arrow with provided data
Now with click interaction and selection visual feedback
Now with intelligent rotation animation matching prop behavior!
-->
<script lang="ts">
  import {
    resolve,
    TYPES,
    type IHapticFeedbackService,
    type MotionData,
    type PictographData,
    Orientation,
    RotationDirection,
  } from "$shared";
  import type { ArrowAssets, ArrowPosition } from "$shared/pictograph/arrow";
  import { selectedArrowState } from "../../../../../modules/create/shared/state/selected-arrow-state.svelte";

  let {
    motionData,
    arrowAssets,
    arrowPosition,
    shouldMirror = false,
    showArrow = true,
    color,
    pictographData = null,
    isClickable = false,
  } = $props<{
    motionData: MotionData;
    arrowAssets: ArrowAssets;
    arrowPosition: ArrowPosition;
    shouldMirror?: boolean;
    showArrow?: boolean;
    color: string;
    pictographData?: PictographData | null;
    isClickable?: boolean;
  }>();

  // ============================================================================
  // INTELLIGENT ROTATION ANIMATION SYSTEM (matching PropSvg behavior)
  // ============================================================================

  type MotionSnapshot = {
    startOrientation?: Orientation;
    turns?: number | "fl";
    rotationDirection?: RotationDirection;
  };

  type RotationAnimationDirection = "cw" | "ccw" | "auto";

  const ORIENTATION_CYCLE: Orientation[] = [
    Orientation.IN,
    Orientation.COUNTER,
    Orientation.OUT,
    Orientation.CLOCK,
  ];

  const EPSILON = 0.0001;

  // Track rotation state for intelligent animation
  let displayedRotation = $state<number>(arrowPosition?.rotation ?? 0);
  let previousRotation: number | null = null;
  let previousSnapshot: MotionSnapshot | null = null;

  // Determine optimal rotation animation based on motion data changes
  $effect(() => {
    const targetRotation = arrowPosition?.rotation ?? 0;
    const snapshot: MotionSnapshot = {
      startOrientation: motionData?.startOrientation,
      turns: motionData?.turns,
      rotationDirection: motionData?.rotationDirection,
    };

    if (previousSnapshot === null || previousRotation === null) {
      // First render - no transition
      displayedRotation = targetRotation;
    } else {
      // Determine animation direction based on motion data changes
      const direction = determineAnimationDirection(previousSnapshot, snapshot);
      // Resolve rotation to animate in the correct direction
      displayedRotation = resolveRotation(
        previousRotation,
        targetRotation,
        direction
      );
    }

    previousRotation = displayedRotation;
    previousSnapshot = snapshot;
  });

  /**
   * Determines the optimal rotation direction based on motion data changes
   */
  function determineAnimationDirection(
    previous: MotionSnapshot,
    current: MotionSnapshot
  ): RotationAnimationDirection {
    const previousTurns =
      typeof previous.turns === "number" ? previous.turns : null;
    const currentTurns =
      typeof current.turns === "number" ? current.turns : null;

    // Check for turn count changes
    if (
      previousTurns !== null &&
      currentTurns !== null &&
      previousTurns !== currentTurns
    ) {
      const rotationDir = current.rotationDirection;
      if (currentTurns > previousTurns) {
        // Turns increased - rotate in specified direction
        return mapRotationDirection(rotationDir) ?? "cw";
      }
      if (currentTurns < previousTurns) {
        // Turns decreased - rotate in opposite direction
        const direction = mapRotationDirection(rotationDir);
        if (direction === "cw") return "ccw";
        if (direction === "ccw") return "cw";
        return "ccw";
      }
    }

    // Check for orientation changes
    if (
      previous.startOrientation &&
      current.startOrientation &&
      previous.startOrientation !== current.startOrientation
    ) {
      return getOrientationDirection(
        previous.startOrientation,
        current.startOrientation,
        current.rotationDirection
      );
    }

    // Default to auto (shortest path)
    return "auto";
  }

  /**
   * Maps RotationDirection enum to animation direction
   */
  function mapRotationDirection(
    direction?: RotationDirection
  ): RotationAnimationDirection | null {
    if (!direction || direction === RotationDirection.NO_ROTATION) {
      return null;
    }
    return direction === RotationDirection.COUNTER_CLOCKWISE ? "ccw" : "cw";
  }

  /**
   * Determines rotation direction for orientation changes
   */
  function getOrientationDirection(
    previousOrientation: Orientation,
    nextOrientation: Orientation,
    rotationDirection?: RotationDirection
  ): RotationAnimationDirection {
    const previousIndex = ORIENTATION_CYCLE.indexOf(previousOrientation);
    const nextIndex = ORIENTATION_CYCLE.indexOf(nextOrientation);

    if (previousIndex === -1 || nextIndex === -1) {
      return mapRotationDirection(rotationDirection) ?? "cw";
    }

    const cycleLength = ORIENTATION_CYCLE.length;
    const forwardSteps =
      (nextIndex - previousIndex + cycleLength) % cycleLength;
    const backwardSteps =
      (previousIndex - nextIndex + cycleLength) % cycleLength;

    if (forwardSteps === 0) {
      return "auto";
    }

    if (forwardSteps === backwardSteps) {
      // 180° opposite - use explicit rotation direction
      return mapRotationDirection(rotationDirection) ?? "cw";
    }

    // Choose shortest path
    return forwardSteps < backwardSteps ? "cw" : "ccw";
  }

  /**
   * Resolves the actual rotation value that will animate in the correct direction
   */
  function resolveRotation(
    previous: number,
    target: number,
    direction: RotationAnimationDirection
  ): number {
    if (!Number.isFinite(previous)) {
      return target;
    }

    // For auto mode: take shortest path
    if (direction === "auto") {
      const delta = normalizeDelta(target - previous);
      return previous + delta;
    }

    // Normalize both angles to [0, 360) range
    const normalizedPrevious = ((previous % 360) + 360) % 360;
    const normalizedTarget = ((target % 360) + 360) % 360;

    // Calculate the delta in the specified direction
    let delta: number;

    if (direction === "cw") {
      // Clockwise: Calculate positive delta
      delta = ((normalizedTarget - normalizedPrevious) + 360) % 360;
      // If delta is 0, we're at the same angle - no rotation needed
      if (delta < EPSILON) {
        return target;
      }
    } else {
      // Counter-clockwise: Calculate negative delta
      delta = ((normalizedTarget - normalizedPrevious) - 360) % 360;
      // If delta is 0, we're at the same angle - no rotation needed
      if (Math.abs(delta) < EPSILON) {
        return target;
      }
    }

    // Apply the delta to previous rotation
    return previous + delta;
  }

  /**
   * Normalizes rotation delta to [-180, 180] range
   */
  function normalizeDelta(delta: number): number {
    let normalized = ((delta % 360) + 360) % 360;
    if (normalized > 180) normalized -= 360;
    if (normalized <= -180) normalized += 360;
    return normalized;
  }

  // ============================================================================
  // SELECTION & INTERACTION LOGIC
  // ============================================================================

  // Check if this arrow is currently selected
  const isSelected = $derived(
    isClickable && pictographData
      ? selectedArrowState.isSelected(motionData, color)
      : false
  );

  let hapticService: IHapticFeedbackService | null = null;

  // Initialize haptic service on mount (lazy load)
  $effect(() => {
    if (isClickable && !hapticService) {
      try {
        hapticService = resolve<IHapticFeedbackService>(
          TYPES.IHapticFeedbackService
        );
      } catch (error) {
        console.warn("Haptic service not available:", error);
      }
    }
  });

  // Handle arrow click
  function handleArrowClick(event: MouseEvent) {
    if (!isClickable || !pictographData) return;

    event.stopPropagation();

    console.log("[ArrowSvg] Arrow clicked:", {
      color,
      currentPosition: arrowPosition,
      motionData: motionData,
    });

    // Trigger haptic feedback
    hapticService?.trigger("selection");

    // Select the arrow in global state
    selectedArrowState.selectArrow(motionData, color, pictographData);
  }

  // Log when arrow position changes
  $effect(() => {
    console.log(`🎨 [ArrowSvg] ${color} arrow position received:`, arrowPosition);
  });
</script>

{#if showArrow}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <g
    class="arrow-svg {motionData.color}-arrow-svg"
    class:mirrored={shouldMirror}
    class:clickable={isClickable}
    class:selected={isSelected}
    onclick={handleArrowClick}
    role={isClickable ? "button" : null}
    tabindex={isClickable ? 0 : -1}
    aria-label={isClickable
      ? `${color} arrow - ${motionData.motion} ${motionData.turns}`
      : undefined}
    style="
      transform: translate({arrowPosition.x}px, {arrowPosition.y}px)
                 rotate({displayedRotation}deg)
                 {shouldMirror ? 'scale(-1, 1)' : ''};
    "
  >
    <!-- Position group at calculated coordinates, let SVG handle its own centering -->
    <g transform="translate({-arrowAssets.center.x}, {-arrowAssets.center.y})">
      {@html arrowAssets.imageSrc}
    </g>

    <!-- Selection highlight overlay -->
    {#if isSelected}
      <circle
        cx="0"
        cy="0"
        r="60"
        fill="none"
        stroke="var(--color-accent, #fbbf24)"
        stroke-width="4"
        class="selection-glow"
        opacity="0.8"
      />
    {/if}
  </g>
{/if}

<style>
  .arrow-svg {
    pointer-events: none;
    /* Smooth transition for position and rotation changes - matches prop behavior */
    /* IMPORTANT: transform must be a CSS property (not SVG attribute) for transitions to work */
    /* Intelligent rotation direction is calculated in the component logic above */
    transition:
      transform 0.2s ease,
      filter 0.2s ease;
  }

  .arrow-svg.clickable {
    pointer-events: all;
    cursor: pointer;
  }

  .arrow-svg.clickable:hover {
    filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.6));
  }

  .arrow-svg.clickable:active {
    filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.4));
  }

  .arrow-svg.selected {
    filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.9));
  }

  .selection-glow {
    animation: pulse-glow 2s ease-in-out infinite;
  }

  @keyframes pulse-glow {
    0%,
    100% {
      opacity: 0.6;
      stroke-width: 4;
    }
    50% {
      opacity: 1;
      stroke-width: 6;
    }
  }
</style>
