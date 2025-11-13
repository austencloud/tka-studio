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
  import GridModeToggle from "../../construct/shared/components/GridModeToggle.svelte";

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
    padding: min(2cqmin, 1.5rem);
    gap: min(2cqmin, 1rem);
    container-type: size;
    container-name: start-picker;
    box-sizing: border-box;
  }

  .picker-header {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: min(2cqmin, 1rem);
    padding: min(1cqmin, 0.5rem);
    flex-shrink: 0;
  }

  .grid-toggle-container {
    display: flex;
    justify-content: flex-end;
  }

  /* Intelligent auto-flowing grid - adapts to any container size */
  .position-grid {
    display: grid;
    /* Auto-fit ensures grid reorganizes based on available space */
    /* Each cell gets minimum 35% of container width, maximum 1fr of space */
    grid-template-columns: repeat(auto-fit, minmax(min(35cqw, 100%), 1fr));
    gap: min(3cqmin, 1.5rem);
    flex: 1;
    align-items: center;
    justify-items: center;
    width: 100%;
    margin: 0 auto;
    padding: min(2cqmin, 1rem);
    /* Ensure grid takes full available height */
    align-content: center;
  }

  .position-button {
    /* Fluid sizing relative to grid cell */
    width: 100%;
    aspect-ratio: 1 / 1;

    /* Constrain to fit within grid cell and container */
    max-width: min(100%, 30cqh, 280px);
    max-height: min(100%, 22cqh);

    min-width: 0;
    min-height: 0;

    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: min(2cqmin, 16px);
    padding: min(2cqmin, 1rem);

    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: min(1cqmin, 0.75rem);

    position: relative;
    overflow: hidden;
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
    min-width: 0;
    /* Ensure pictograph scales to fit available space */
    container-type: size;
  }

  .position-label {
    font-size: min(2cqmin, 1rem);
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
</style>
