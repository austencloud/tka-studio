<!--
StaticSection.svelte - Static pictograph with motion controls

Combines static pictograph display (no card wrapper) with motion designer controls
(blue/red prop panels) below. Grid toggle positioned as overlay on pictograph.
This is the left 2/3 section of the new layout.
-->
<script lang="ts">
  import {
    createMotionData,
    createPictographData,
    GridLocation,
    Letter,
    MotionColor,
    MotionType,
    Orientation,
    RotationDirection,
  } from "$shared/domain";
  import Pictograph from "$shared/pictograph/components/Pictograph.svelte";
  import type { AnimatorState } from "../state";
  import PropPanel from "./PropPanel.svelte";
  import SimpleGridToggle from "./SimpleGridToggle.svelte";

  interface Props {
    motionState: AnimatorState;
  }

  let { motionState }: Props = $props();

  // Reactive pictograph data derived from motion state
  let pictographData = $derived.by(() => {
    try {
      console.log(
        "🔍 StaticSection: Creating pictograph from motion parameters"
      );

      // Get current motion parameters
      const blueEndLocation = motionState.blueMotionParams
        .endLocation as GridLocation;
      const redEndLocation = motionState.redMotionParams
        .endLocation as GridLocation;

      // TODO: Enhance with letter detection logic
      let letter: Letter = Letter.A;

      // ✅ DIRECT DOMAIN CONSTRUCTOR: No factory needed - positions auto-derived
      const pictographData = createPictographData({
        letter,
        motions: {
          blue: createMotionData({
            startLocation: motionState.blueMotionParams
              .startLocation as GridLocation,
            endLocation: blueEndLocation,
            startOrientation: motionState.blueMotionParams
              .startOrientation as Orientation,
            endOrientation: motionState.blueMotionParams
              .endOrientation as Orientation,
            motionType: motionState.blueMotionParams.motionType as MotionType,
            rotationDirection: motionState.blueMotionParams
              .rotationDirection as RotationDirection,
            turns: motionState.blueMotionParams.turns,
            color: MotionColor.BLUE,
            isVisible: true,
          }),
          red: createMotionData({
            startLocation: motionState.redMotionParams
              .startLocation as GridLocation,
            endLocation: redEndLocation,
            startOrientation: motionState.redMotionParams
              .startOrientation as Orientation,
            endOrientation: motionState.redMotionParams
              .endOrientation as Orientation,
            motionType: motionState.redMotionParams.motionType as MotionType,
            rotationDirection: motionState.redMotionParams
              .rotationDirection as RotationDirection,
            turns: motionState.redMotionParams.turns,
            color: MotionColor.RED,
            isVisible: true,
          }),
        },
      });

      console.log(
        "✅ StaticSection: Pictograph created successfully using domain constructor"
      );
      return pictographData;
    } catch (error) {
      console.error("❌ StaticSection: Error creating pictograph:", error);
      return null;
    }
  });
</script>

<div class="static-section">
  <!-- Static Pictograph with Grid Toggle Overlay -->
  <div class="pictograph-area">
    <div class="grid-toggle-overlay">
      <SimpleGridToggle state={motionState} />
    </div>

    <div class="pictograph-container">
      {#if pictographData}
        {#key pictographData.id}
          <Pictograph {pictographData} />
        {/key}
      {:else}
        <div class="error-state">
          <span class="error-icon">⚠️</span>
          <p>Unable to display pictograph</p>
        </div>
      {/if}
    </div>
  </div>

  <!-- Motion Designer Controls -->
  <div class="motion-controls">
    <!-- Blue Prop Section -->
    <div class="prop-section">
      <PropPanel
        propName="Blue"
        propColor="#60a5fa"
        startLocation={motionState.blueMotionParams.startLocation}
        endLocation={motionState.blueMotionParams.endLocation}
        startOrientation={motionState.blueMotionParams
          .startOrientation as Orientation}
        endOrientation={motionState.blueMotionParams
          .endOrientation as Orientation}
        turns={motionState.blueMotionParams.turns}
        motionType={motionState.blueMotionParams.motionType as MotionType}
        gridMode={motionState.gridMode}
        onStartLocationChange={(location) =>
          motionState.setBlueStartLocation(location)}
        onEndLocationChange={(location) =>
          motionState.setBlueEndLocation(location)}
        onStartOrientationChange={(orientation) =>
          motionState.updateBlueMotionParam("startOrientation", orientation)}
        onEndOrientationChange={(orientation) =>
          motionState.updateBlueMotionParam("endOrientation", orientation)}
        onTurnsChange={(turns) =>
          motionState.updateBlueMotionParam("turns", turns)}
        onMotionTypeChange={(motionType) =>
          motionState.updateBlueMotionParam("motionType", motionType)}
      />
    </div>

    <!-- Red Prop Section -->
    <div class="prop-section">
      <PropPanel
        propName="Red"
        propColor="#f87171"
        startLocation={motionState.redMotionParams.startLocation}
        endLocation={motionState.redMotionParams.endLocation}
        startOrientation={motionState.redMotionParams
          .startOrientation as Orientation}
        endOrientation={motionState.redMotionParams
          .endOrientation as Orientation}
        turns={motionState.redMotionParams.turns}
        motionType={motionState.redMotionParams.motionType as MotionType}
        gridMode={motionState.gridMode}
        onStartLocationChange={(location) =>
          motionState.setRedStartLocation(location)}
        onEndLocationChange={(location) =>
          motionState.setRedEndLocation(location)}
        onStartOrientationChange={(orientation) =>
          motionState.updateRedMotionParam("startOrientation", orientation)}
        onEndOrientationChange={(orientation) =>
          motionState.updateRedMotionParam("endOrientation", orientation)}
        onTurnsChange={(turns) =>
          motionState.updateRedMotionParam("turns", turns)}
        onMotionTypeChange={(motionType) =>
          motionState.updateRedMotionParam("motionType", motionType)}
      />
    </div>
  </div>
</div>

<style>
  .static-section {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: linear-gradient(
      135deg,
      rgba(16, 185, 129, 0.03),
      rgba(59, 130, 246, 0.03)
    );
    border-radius: 8px;
    overflow: hidden;
    container-type: size;
  }

  .pictograph-area {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .grid-toggle-overlay {
    position: absolute;
    top: 16px;
    right: 16px;
    z-index: 10;
  }

  .pictograph-container {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.01);
    padding: 10px;
  }

  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #f87171;
    text-align: center;
    padding: 40px;
  }

  .error-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }

  .error-state p {
    margin: 0;
    font-size: 16px;
    color: #fca5a5;
  }

  .motion-controls {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1cqw;
    padding: 1.5cqw;
    min-height: 0;
    overflow: auto;
    container-type: size;
  }

  .prop-section {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
  }

  /* Container-based responsive layout */
  @container (max-width: 600px) {
    .motion-controls {
      grid-template-columns: 1fr;
      gap: 1.5cqw;
      padding: 2cqw;
    }
  }

  @container (max-width: 400px) {
    .motion-controls {
      gap: 2cqw;
      padding: 2.5cqw;
    }
  }

  /* Fallback media queries for older browsers */
  @media (max-width: 768px) {
    .pictograph-area {
      padding: 1.5vw;
    }

    .motion-controls {
      grid-template-columns: 1fr;
      padding: 2vw;
      gap: 1.5vw;
    }

    .grid-toggle-overlay {
      top: 1vw;
      right: 1vw;
    }
  }
</style>
