<!--
SinglePropStartPositionPicker.svelte - Start position picker for Guided Construct

Shows 4 cardinal positions (N, E, S, W) or 4 corner positions (NE, SE, SW, NW)
With grid mode toggle to switch between Diamond and Box mode
-->
<script lang="ts">
  import type {
    GridMode,
    IHapticFeedbackService,
    PictographData,
  } from "$shared";
  import {
    GridLocation,
    GridMode as GridModeEnum,
    Pictograph,
    resolve,
    TYPES,
    createPictographData,
    createMotionData,
    MotionColor,
    MotionType,
    Orientation,
    PropType,
    RotationDirection,
  } from "$shared";
  import { onMount } from "svelte";
  import GridModeToggle from "../../shared/components/GridModeToggle.svelte";

  const {
    onPositionSelected,
    onGridModeChange,
    currentGridMode = GridModeEnum.DIAMOND,
    handColor = MotionColor.BLUE,
    showInlineGridToggle = true,
  } = $props<{
    onPositionSelected: (
      position: PictographData,
      location: GridLocation
    ) => void;
    onGridModeChange?: (gridMode: GridMode) => void;
    currentGridMode?: GridMode;
    handColor?: MotionColor;
    showInlineGridToggle?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Generate 4 starting position options based on grid mode
  const startPositions = $derived.by(() => {
    const locations =
      currentGridMode === GridModeEnum.DIAMOND
        ? [
            GridLocation.NORTH,
            GridLocation.EAST,
            GridLocation.SOUTH,
            GridLocation.WEST,
          ]
        : [
            GridLocation.NORTHEAST,
            GridLocation.SOUTHEAST,
            GridLocation.SOUTHWEST,
            GridLocation.NORTHWEST,
          ];

    return locations.map((location) =>
      createStartPositionPictograph(location, handColor, currentGridMode)
    );
  });

  // Create a single-prop starting position pictograph
  function createStartPositionPictograph(
    location: GridLocation,
    color: MotionColor,
    gridMode: GridMode
  ): PictographData {
    const motion = createMotionData({
      color,
      startLocation: location,
      endLocation: location,
      motionType: MotionType.STATIC,
      rotationDirection: RotationDirection.NO_ROTATION,
      gridMode,
      propType: PropType.HAND,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      turns: 0,
      arrowLocation: location,
      isVisible: true,
    });

    return createPictographData({
      motions: {
        [color]: motion,
      },
    });
  }

  // Handle position selection
  function handlePositionSelect(
    pictograph: PictographData,
    location: GridLocation
  ) {
    hapticService?.trigger("selection");
    onPositionSelected(pictograph, location);
  }

  // Handle grid mode change
  function handleGridModeChange(newGridMode: GridMode) {
    onGridModeChange?.(newGridMode);
  }
</script>

<div class="start-position-picker">
  <!-- Header with title and grid mode toggle -->
  {#if showInlineGridToggle}
    <div class="picker-header">
      <div class="header-spacer"></div>
      <div class="grid-toggle-container">
        <GridModeToggle
          {currentGridMode}
          onGridModeChange={handleGridModeChange}
        />
      </div>
    </div>
  {/if}

  <!-- 4 Position Grid -->
  <div class="position-grid">
    {#each startPositions as pictograph, index}
      {@const location =
        currentGridMode === GridModeEnum.DIAMOND
          ? [
              GridLocation.NORTH,
              GridLocation.EAST,
              GridLocation.SOUTH,
              GridLocation.WEST,
            ][index]
          : [
              GridLocation.NORTHEAST,
              GridLocation.SOUTHEAST,
              GridLocation.SOUTHWEST,
              GridLocation.NORTHWEST,
            ][index]}

      {#if location}
        <button
          class="position-button"
          onclick={() => handlePositionSelect(pictograph, location)}
          aria-label={`Select starting position ${location}`}
        >
          <div class="pictograph-wrapper">
            <Pictograph
              pictographData={pictograph}
              visibleHand={handColor}
              gridMode={currentGridMode}
            />
          </div>
          <span class="position-label">{location.toUpperCase()}</span>
        </button>
      {/if}
    {/each}
  </div>
</div>

<style>
  .start-position-picker {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    padding: clamp(0.5rem, 2cqmin, 1.5rem);
    gap: clamp(0.75rem, 3cqmin, 1.5rem);
    container-type: size;
    container-name: start-picker;
  }

  .picker-header {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem;
    flex-shrink: 0;
  }

  .grid-toggle-container {
    display: flex;
    justify-content: flex-end;
  }

  /* Default: 2x2 grid for balanced/square containers */
  .position-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: clamp(0.75rem, 3cqmin, 2rem);
    flex: 1;
    align-items: center;
    justify-items: center;
    width: 100%;
    max-width: min(100%, 700px);
    margin: 0 auto;
    padding: clamp(0.5rem, 2cqmin, 1rem);
    container-type: inline-size;
  }

  /* Wide landscape: 1 row × 4 columns */
  @container start-picker (aspect-ratio > 1.8) {
    .position-grid {
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 1fr;
      max-width: min(100%, 1200px);
    }
  }

  /* Moderate landscape: optimize 2x2 for width */
  @container start-picker (aspect-ratio > 1.4) and (aspect-ratio <= 1.8) {
    .position-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      max-width: min(90%, 800px);
    }
  }

  /* Tall portrait: 4 rows × 1 column - more generous threshold */
  @container start-picker (aspect-ratio < 0.85) {
    .position-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr);
      max-width: min(100%, 400px);
    }
  }

  /* Very tall and narrow: stack vertically with smaller gaps */
  @container start-picker (aspect-ratio < 0.6) {
    .position-grid {
      gap: clamp(0.5rem, 2cqmin, 1rem);
      padding: 0.25rem;
    }
  }

  .position-button {
    width: 100%;
    height: 100%;
    aspect-ratio: 1 / 1;
    min-width: 0;
    min-height: 0;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(8px, 2cqmin, 16px);
    padding: clamp(0.5rem, 2cqmin, 1rem);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(0.25rem, 1cqmin, 0.75rem);
    position: relative;
    overflow: hidden;
  }

  /* Constrain button max size based on grid layout */
  @container start-picker (aspect-ratio > 1.8) {
    .position-button {
      max-width: 280px;
      max-height: 280px;
    }
  }

  @container start-picker (aspect-ratio > 1.4) and (aspect-ratio <= 1.8) {
    .position-button {
      max-width: 300px;
      max-height: 300px;
    }
  }

  @container start-picker (aspect-ratio >= 0.85) and (aspect-ratio <= 1.4) {
    .position-button {
      max-width: 250px;
      max-height: 250px;
    }
  }

  @container start-picker (aspect-ratio < 0.85) {
    .position-button {
      max-width: 100%;
      max-height: min(180px, 20cqh);
    }
  }

  .position-button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(100, 200, 255, 0.1),
      rgba(100, 150, 255, 0.05)
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .pictograph-wrapper {
    flex: 1;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    min-height: 0;
  }

  .position-label {
    font-size: clamp(0.6875rem, 2cqmin, 1rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    flex-shrink: 0;
  }

  /* Hover effects */
  @media (hover: hover) {
    .position-button:hover {
      border-color: rgba(100, 200, 255, 0.5);
      transform: translateY(-4px) scale(1.02);
      box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.2),
        0 0 20px rgba(100, 200, 255, 0.2);
    }

    .position-button:hover::before {
      opacity: 1;
    }

    .position-button:hover .position-label {
      color: rgba(147, 197, 253, 1);
    }
  }

  .position-button:active {
    transform: translateY(-2px) scale(0.98);
    transition: transform 0.1s ease;
  }

  /* Small container adjustments */
  @container start-picker (max-width: 500px) {
    .position-grid {
      gap: clamp(0.5rem, 2cqmin, 1rem);
    }

    .position-button {
      padding: clamp(0.375rem, 1.5cqmin, 0.75rem);
    }
  }

  /* Header adjustments for small containers */
  @container start-picker (max-width: 400px) {
    .picker-header {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }

    .header-spacer {
      display: none;
    }

    .grid-toggle-container {
      justify-content: center;
    }
  }
</style>
