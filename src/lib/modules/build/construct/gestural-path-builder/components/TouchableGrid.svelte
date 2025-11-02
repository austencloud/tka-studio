<!--
TouchableGrid.svelte - Interactive grid for gesture-based hand path drawing

Handles pointer events and converts them to hand path segments.
Provides visual feedback for current position and drawn path.
-->
<script lang="ts">
  import { GridLocation, GridMode, type MotionColor } from "$shared";
  import { onMount } from "svelte";
  import type { GridPositionPoint } from "../domain";
  import type { GesturalPathState } from "../state";

  // Props
  let {
    pathState,
    gridMode = GridMode.DIAMOND,
    onSegmentComplete,
    onAdvancePressed,
    onAdvanceReleased,
  }: {
    pathState: GesturalPathState;
    gridMode?: GridMode;
    onSegmentComplete?: (start: GridLocation, end: GridLocation) => void;
    onAdvancePressed?: () => void;
    onAdvanceReleased?: () => void;
  } = $props();

  // Grid container element
  let containerElement = $state<HTMLDivElement | null>(null);

  // Grid positions with coordinates
  let gridPositions = $state<GridPositionPoint[]>([]);

  // Touch tracking
  let isTracking = $state(false);
  let startX = $state(0);
  let startY = $state(0);
  let currentX = $state(0);
  let currentY = $state(0);
  let startTime = $state(0);
  let startLocation = $state<GridLocation | null>(null);
  let hoverLocation = $state<GridLocation | null>(null);

  // Grid dimensions
  const GRID_SIZE = 300; // Base grid size
  const POSITION_RADIUS = 40; // Hit detection radius
  const MOVEMENT_THRESHOLD = 10; // Minimum pixels to register movement

  // Calculate grid position coordinates based on grid mode
  function calculateGridPositions(): GridPositionPoint[] {
    const center = GRID_SIZE / 2;
    const offset = GRID_SIZE / 3;

    if (gridMode === GridMode.DIAMOND) {
      return [
        {
          location: GridLocation.NORTH,
          x: center,
          y: center - offset,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.EAST,
          x: center + offset,
          y: center,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.SOUTH,
          x: center,
          y: center + offset,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.WEST,
          x: center - offset,
          y: center,
          radius: POSITION_RADIUS,
        },
      ];
    } else {
      // BOX mode
      const diagonalOffset = offset * 0.707; // cos(45°)
      return [
        {
          location: GridLocation.NORTHEAST,
          x: center + diagonalOffset,
          y: center - diagonalOffset,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.SOUTHEAST,
          x: center + diagonalOffset,
          y: center + diagonalOffset,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.SOUTHWEST,
          x: center - diagonalOffset,
          y: center + diagonalOffset,
          radius: POSITION_RADIUS,
        },
        {
          location: GridLocation.NORTHWEST,
          x: center - diagonalOffset,
          y: center - diagonalOffset,
          radius: POSITION_RADIUS,
        },
      ];
    }
  }

  // Find closest grid position to coordinates
  function findClosestPosition(x: number, y: number): GridLocation | null {
    let closest: GridPositionPoint | null = null;
    let minDist = Infinity;

    for (const pos of gridPositions) {
      const dist = Math.sqrt(Math.pow(x - pos.x, 2) + Math.pow(y - pos.y, 2));
      if (dist < minDist) {
        minDist = dist;
        closest = pos;
      }
    }

    return closest?.location || null;
  }

  // Get coordinates from pointer event relative to container
  function getRelativeCoordinates(event: PointerEvent): { x: number; y: number } | null {
    if (!containerElement) return null;

    const rect = containerElement.getBoundingClientRect();
    const scaleX = GRID_SIZE / rect.width;
    const scaleY = GRID_SIZE / rect.height;

    return {
      x: (event.clientX - rect.left) * scaleX,
      y: (event.clientY - rect.top) * scaleY,
    };
  }

  // Handle pointer down
  function handlePointerDown(event: PointerEvent): void {
    const coords = getRelativeCoordinates(event);
    if (!coords) return;

    const location = findClosestPosition(coords.x, coords.y);
    if (!location) return;

    isTracking = true;
    startX = coords.x;
    startY = coords.y;
    currentX = coords.x;
    currentY = coords.y;
    startTime = Date.now();
    startLocation = location;
    hoverLocation = location;

    pathState.updateCurrentLocation(location);

    // Capture pointer for smooth tracking
    (event.target as Element).setPointerCapture(event.pointerId);

    // Notify advance button pressed (for discrete mode)
    onAdvancePressed?.();
  }

  // Handle pointer move
  function handlePointerMove(event: PointerEvent): void {
    if (!isTracking) {
      // Hover feedback when not tracking
      const coords = getRelativeCoordinates(event);
      if (coords) {
        hoverLocation = findClosestPosition(coords.x, coords.y);
      }
      return;
    }

    const coords = getRelativeCoordinates(event);
    if (!coords) return;

    currentX = coords.x;
    currentY = coords.y;

    // Check if moved significantly
    const dist = Math.sqrt(
      Math.pow(currentX - startX, 2) + Math.pow(currentY - startY, 2)
    );

    if (dist > MOVEMENT_THRESHOLD) {
      pathState.markMovementOccurred();
    }

    // Update hover location
    hoverLocation = findClosestPosition(coords.x, coords.y);
  }

  // Handle pointer up
  function handlePointerUp(event: PointerEvent): void {
    if (!isTracking || !startLocation) return;

    const coords = getRelativeCoordinates(event);
    if (!coords) return;

    const endLocation = findClosestPosition(coords.x, coords.y);
    if (!endLocation) return;

    // Calculate movement
    const dist = Math.sqrt(
      Math.pow(currentX - startX, 2) + Math.pow(currentY - startY, 2)
    );

    // If moved significantly, record segment
    if (dist > MOVEMENT_THRESHOLD) {
      onSegmentComplete?.(startLocation, endLocation);
    }

    // Release pointer capture
    (event.target as Element).releasePointerCapture(event.pointerId);

    // Notify advance button released
    onAdvanceReleased?.();

    // Reset tracking
    isTracking = false;
    startLocation = null;
  }

  // Initialize grid positions on mount
  onMount(() => {
    gridPositions = calculateGridPositions();
  });

  // Update grid positions when mode changes
  $effect(() => {
    gridPositions = calculateGridPositions();
  });
</script>

<div
  class="touchable-grid"
  bind:this={containerElement}
  onpointerdown={handlePointerDown}
  onpointermove={handlePointerMove}
  onpointerup={handlePointerUp}
  role="application"
  aria-label="Hand path drawing grid"
>
  <!-- Grid background -->
  <svg class="grid-svg" viewBox="0 0 {GRID_SIZE} {GRID_SIZE}">
    <!-- Grid lines -->
    <g class="grid-lines">
      {#if gridMode === GridMode.DIAMOND}
        <line
          x1={GRID_SIZE / 2}
          y1={GRID_SIZE / 2 - GRID_SIZE / 3}
          x2={GRID_SIZE / 2}
          y2={GRID_SIZE / 2 + GRID_SIZE / 3}
          stroke="rgba(255, 255, 255, 0.2)"
          stroke-width="2"
        />
        <line
          x1={GRID_SIZE / 2 - GRID_SIZE / 3}
          y1={GRID_SIZE / 2}
          x2={GRID_SIZE / 2 + GRID_SIZE / 3}
          y2={GRID_SIZE / 2}
          stroke="rgba(255, 255, 255, 0.2)"
          stroke-width="2"
        />
      {:else}
        <line
          x1={GRID_SIZE / 2 - GRID_SIZE / 3 * 0.707}
          y1={GRID_SIZE / 2 - GRID_SIZE / 3 * 0.707}
          x2={GRID_SIZE / 2 + GRID_SIZE / 3 * 0.707}
          y2={GRID_SIZE / 2 + GRID_SIZE / 3 * 0.707}
          stroke="rgba(255, 255, 255, 0.2)"
          stroke-width="2"
        />
        <line
          x1={GRID_SIZE / 2 + GRID_SIZE / 3 * 0.707}
          y1={GRID_SIZE / 2 - GRID_SIZE / 3 * 0.707}
          x2={GRID_SIZE / 2 - GRID_SIZE / 3 * 0.707}
          y2={GRID_SIZE / 2 + GRID_SIZE / 3 * 0.707}
          stroke="rgba(255, 255, 255, 0.2)"
          stroke-width="2"
        />
      {/if}
    </g>

    <!-- Grid positions -->
    {#each gridPositions as position (position.location)}
      <circle
        cx={position.x}
        cy={position.y}
        r="30"
        fill={position.location === pathState.currentLocation
          ? "rgba(59, 130, 246, 0.5)"
          : position.location === hoverLocation
            ? "rgba(255, 255, 255, 0.3)"
            : "rgba(255, 255, 255, 0.1)"}
        stroke="rgba(255, 255, 255, 0.5)"
        stroke-width="2"
        class="grid-position"
      />
      <text
        x={position.x}
        y={position.y}
        text-anchor="middle"
        dominant-baseline="middle"
        fill="white"
        font-size="12"
        font-weight="bold"
      >
        {position.location.toUpperCase()}
      </text>
    {/each}

    <!-- Completed path -->
    {#each pathState.completedSegments as segment, i}
      {@const startPos = gridPositions.find((p) => p.location === segment.startLocation)}
      {@const endPos = gridPositions.find((p) => p.location === segment.endLocation)}
      {#if startPos && endPos}
        <line
          x1={startPos.x}
          y1={startPos.y}
          x2={endPos.x}
          y2={endPos.y}
          stroke={pathState.currentHand === "blue" ? "#3b82f6" : "#ef4444"}
          stroke-width="4"
          opacity="0.6"
          marker-end="url(#arrowhead)"
        />
      {/if}
    {/each}

    <!-- Active drag line -->
    {#if isTracking && startLocation}
      {@const startPos = gridPositions.find((p) => p.location === startLocation)}
      {#if startPos}
        <line
          x1={startPos.x}
          y1={startPos.y}
          x2={currentX}
          y2={currentY}
          stroke={pathState.currentHand === "blue" ? "#3b82f6" : "#ef4444"}
          stroke-width="4"
          stroke-dasharray="5,5"
          opacity="0.8"
        />
      {/if}
    {/if}

    <!-- Arrowhead marker -->
    <defs>
      <marker
        id="arrowhead"
        markerWidth="10"
        markerHeight="10"
        refX="5"
        refY="3"
        orient="auto"
      >
        <polygon
          points="0 0, 10 3, 0 6"
          fill={pathState.currentHand === "blue" ? "#3b82f6" : "#ef4444"}
        />
      </marker>
    </defs>
  </svg>
</div>

<style>
  .touchable-grid {
    width: 100%;
    max-width: 500px;
    aspect-ratio: 1;
    touch-action: none;
    user-select: none;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.2);
    cursor: crosshair;
  }

  .grid-svg {
    width: 100%;
    height: 100%;
  }

  .grid-position {
    transition: all 0.2s ease;
  }

  .grid-position:hover {
    filter: brightness(1.2);
  }
</style>
