<!--
Simple Prop Component - Just renders a prop with provided data
Now with smooth transitions when position or orientation changes!
-->
<script lang="ts">
  import {
    Orientation,
    RotationDirection,
    type MotionData,
  } from "$shared";
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

  let displayedRotation = $state<number>(propPosition?.rotation ?? 0);
  let previousRotation: number | null = null;
  let previousSnapshot: MotionSnapshot | null = null;

  $effect(() => {
    const targetRotation = propPosition?.rotation ?? 0;
    const snapshot: MotionSnapshot = {
      startOrientation: motionData?.startOrientation,
      turns: motionData?.turns,
      rotationDirection: motionData?.rotationDirection,
    };

    if (previousSnapshot === null || previousRotation === null) {
      displayedRotation = targetRotation;
    } else {
      const direction = determineAnimationDirection(previousSnapshot, snapshot);
      displayedRotation = resolveRotation(
        previousRotation,
        targetRotation,
        direction
      );
    }

    previousRotation = displayedRotation;
    previousSnapshot = snapshot;
  });

  function determineAnimationDirection(
    previous: MotionSnapshot,
    current: MotionSnapshot
  ): RotationAnimationDirection {
    const previousTurns =
      typeof previous.turns === "number" ? previous.turns : null;
    const currentTurns =
      typeof current.turns === "number" ? current.turns : null;

    if (
      previousTurns !== null &&
      currentTurns !== null &&
      previousTurns !== currentTurns
    ) {
      const rotationDir = current.rotationDirection;
      if (currentTurns > previousTurns) {
        return mapRotationDirection(rotationDir) ?? "cw";
      }
      if (currentTurns < previousTurns) {
        const direction = mapRotationDirection(rotationDir);
        if (direction === "cw") return "ccw";
        if (direction === "ccw") return "cw";
        return "ccw";
      }
    }

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

    return "auto";
  }

  function mapRotationDirection(
    direction?: RotationDirection
  ): RotationAnimationDirection | null {
    if (!direction || direction === RotationDirection.NO_ROTATION) {
      return null;
    }
    return direction === RotationDirection.COUNTER_CLOCKWISE ? "ccw" : "cw";
  }

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
    const forwardSteps = (nextIndex - previousIndex + cycleLength) % cycleLength;
    const backwardSteps =
      (previousIndex - nextIndex + cycleLength) % cycleLength;

    if (forwardSteps === 0) {
      return "auto";
    }

    if (forwardSteps === backwardSteps) {
      return mapRotationDirection(rotationDirection) ?? "cw";
    }

    return forwardSteps < backwardSteps ? "cw" : "ccw";
  }

  function resolveRotation(
    previous: number,
    target: number,
    direction: RotationAnimationDirection
  ): number {
    if (!Number.isFinite(previous)) {
      return target;
    }

    if (direction === "cw") {
      let candidate = target;
      while (candidate <= previous + EPSILON) {
        candidate += 360;
      }
      return candidate;
    }

    if (direction === "ccw") {
      let candidate = target;
      while (candidate >= previous - EPSILON) {
        candidate -= 360;
      }
      return candidate;
    }

    const delta = normalizeDelta(target - previous);
    return previous + delta;
  }

  function normalizeDelta(delta: number): number {
    let normalized = ((delta % 360) + 360) % 360;
    if (normalized > 180) normalized -= 360;
    if (normalized <= -180) normalized += 360;
    return normalized;
  }
</script>

{#if showProp}
  <g
    class="prop-svg {motionData.color}-prop-svg"
    data-prop-type={motionData?.propType}
    style="
      transform: translate({propPosition.x}px, {propPosition.y}px)
                 rotate({displayedRotation}deg)
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
