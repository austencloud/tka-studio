<!--
PropPanel.svelte - Enhanced visual prop motion parameter controls

Beautiful, intuitive visual controls replacing boring dropdowns:
- Visual location grids for start/end positions
- Circular orientation wheels for start/end orientations
- Styled motion type buttons with icons
- Enhanced turns control
-->
<script lang="ts">
  import LocationGrid from "./LocationGrid.svelte";
  import OrientationButton from "./OrientationButton.svelte";
  import StyledTurnsControl from "./StyledTurnsControl.svelte";
  import MotionTypeButtons from "./MotionTypeButtons.svelte";
  import { getAvailableMotionTypes } from "../utils/motion-helpers";
  import { MotionColor } from "$lib/domain/enums";
  import {
    type Orientation,
    type MotionType,
    type Location,
    GridMode,
  } from "$lib/domain/enums";

  interface Props {
    propName: string;
    propColor: string;
    startLocation: string;
    endLocation: string;
    startOrientation: Orientation;
    endOrientation: Orientation;
    turns: number | "fl";
    motionType: MotionType;
    gridMode?: GridMode;
    onStartLocationChange: (location: Location) => void;
    onEndLocationChange: (location: Location) => void;
    onStartOrientationChange: (orientation: Orientation) => void;
    onEndOrientationChange: (orientation: Orientation) => void;
    onTurnsChange: (turns: number | "fl") => void;
    onMotionTypeChange: (motionType: MotionType) => void;
  }

  let {
    propName,
    propColor,
    startLocation,
    endLocation,
    startOrientation,
    endOrientation,
    turns,
    motionType,
    gridMode = GridMode.DIAMOND,
    onStartLocationChange,
    onEndLocationChange,
    onStartOrientationChange,
    onTurnsChange,
    onMotionTypeChange,
  }: Props = $props();

  // Convert hex color to RGB values for CSS custom properties
  function hexToRgb(hex: string): string {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (result) {
      const r = parseInt(result[1], 16);
      const g = parseInt(result[2], 16);
      const b = parseInt(result[3], 16);
      return `${r}, ${g}, ${b}`;
    }
    // Fallback colors
    return propName.toLowerCase() === MotionColor.BLUE
      ? "96, 165, 250"
      : "248, 113, 113";
  }

  let rgbColor = $derived(hexToRgb(propColor));

  // Calculate available motion types based on start/end locations
  let availableMotionTypes = $derived.by(() => {
    return getAvailableMotionTypes(
      startLocation.toLowerCase(),
      endLocation.toLowerCase()
    );
  });
</script>

<div class="prop-panel" style="--prop-color: {rgbColor}">
  <div class="prop-header" style="color: {propColor}">
    {propName}
  </div>

  <div class="prop-controls">
    <!-- Location Controls -->
    <div class="control-row location-row">
      <LocationGrid
        selectedLocation={startLocation}
        onLocationChange={onStartLocationChange}
        label="Start"
        color={rgbColor}
        {gridMode}
      />
      <div class="arrow-connector">→</div>
      <LocationGrid
        selectedLocation={endLocation}
        onLocationChange={onEndLocationChange}
        label="End"
        color={rgbColor}
        {gridMode}
      />
    </div>

    <!-- Orientation Controls -->
    <div class="control-row orientation-row">
      <OrientationButton
        selectedOrientation={startOrientation}
        onOrientationChange={onStartOrientationChange}
        label="Start"
        color={rgbColor}
        disabled={false}
      />
      <div class="arrow-connector">→</div>
      <OrientationButton
        selectedOrientation={endOrientation}
        onOrientationChange={() => {}}
        label="End"
        color={rgbColor}
        disabled={true}
      />
    </div>

    <!-- Motion Type and Turns -->
    <div class="control-row motion-row">
      <MotionTypeButtons
        selectedMotionType={motionType}
        {onMotionTypeChange}
        {onTurnsChange}
        color={rgbColor}
        {availableMotionTypes}
        currentTurns={turns}
      />
      <StyledTurnsControl
        {turns}
        {onTurnsChange}
        {onMotionTypeChange}
        currentMotionType={motionType}
        color={rgbColor}
      />
    </div>
  </div>
</div>

<style>
  .prop-panel {
    border: 1px solid rgba(var(--prop-color), 0.3);
    border-radius: 0.75cqw;
    padding: 1.5cqw;
    background: linear-gradient(
      135deg,
      rgba(var(--prop-color), 0.08),
      rgba(var(--prop-color), 0.03)
    );
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    min-width: 0;
    overflow: visible;
    container-type: size;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .prop-header {
    font-size: 1.8cqw;
    font-weight: 800;
    margin-bottom: 1.5cqw;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.15cqw;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    flex-shrink: 0;
  }

  .prop-controls {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    flex: 1;
    min-height: 0;
    padding: 1cqw 0;
  }

  .control-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1cqw;
  }

  .location-row,
  .orientation-row {
    justify-content: center;
    gap: 0.8cqw;
  }

  .motion-row {
    flex-direction: column;
    gap: 1cqw;
  }

  .arrow-connector {
    font-size: 4.5cqw;
    font-weight: 900;
    color: rgba(var(--prop-color), 1);
    text-shadow:
      0 0 8px rgba(var(--prop-color), 0.6),
      0 2px 4px rgba(0, 0, 0, 0.4);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 16px;
    min-height: 80px;
    filter: drop-shadow(0 0 4px rgba(var(--prop-color), 0.4));
  }

  /* Container queries for responsive scaling */
  @container (max-height: 400px) {
    .prop-header {
      font-size: 1cqw;
      margin-bottom: 1cqw;
    }

    .prop-controls {
      padding: 0.5cqw 0;
    }

    .arrow-connector {
      font-size: 2.5cqw;
    }
  }

  @container (max-height: 300px) {
    .prop-header {
      font-size: 0.9cqw;
      margin-bottom: 0.8cqw;
    }

    .prop-controls {
      padding: 0.3cqw 0;
    }

    .control-row {
      gap: 0.8cqw;
    }

    .arrow-connector {
      font-size: 2cqw;
    }
  }

  /* Fallback media queries for older browsers */
  @media (max-width: 768px) {
    .prop-panel {
      padding: 1.5vw;
    }

    .prop-header {
      font-size: 2vw;
      margin-bottom: 1.5vw;
    }

    .prop-controls {
      padding: 1vw 0;
    }

    .arrow-connector {
      font-size: 4vw;
    }
  }
</style>
