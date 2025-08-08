<script lang="ts">
  import { onMount } from 'svelte';
  import { animationState, sequenceData } from '../stores/animation.js';
  import { loadAllImages, drawGrid, drawStaff } from '../utils/images.js';
  import { calculateStepEndpoints } from '../utils/physics.js';
  import { lerpAngle, normalizeAnglePositive, calculateTurnAngle } from '../utils/math.js';
  import type { RenderingState } from '../types.js';

  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D;
  let animationFrameId: number | null = null;
  let lastTimestamp: number | null = null;

  const canvasSize = 600;
  const PI = Math.PI;

  // ✅ FIXED: Pro motion calculation with turns support
  function calculateProIsolationStaffAngle(
    centerPathAngle: number,
    propRotDir?: string,
    turns = 0
  ): number {
    const basePro = normalizeAnglePositive(centerPathAngle + PI);
    const additionalTurns = calculateTurnAngle(turns); // Uses 2π * turns
    return normalizeAnglePositive(basePro + additionalTurns);
  }

  let renderingState = $state<RenderingState>({
    canvasReady: false,
    imagesLoaded: false,
    gridImage: null,
    blueStaffImage: null,
    redStaffImage: null
  });

  // Reactive animation loop
  $effect(() => {
    const state = $animationState;

    if (state.isPlaying && renderingState.canvasReady && renderingState.imagesLoaded) {
      if (!animationFrameId) {
        lastTimestamp = null;
        animationFrameId = requestAnimationFrame(animationLoop);
      }
    } else {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
    }
  });

  // Render when state changes (even when paused)
  $effect(() => {
    const state = $animationState;
    if (renderingState.canvasReady && renderingState.imagesLoaded) {
      render();
    }
  });

  onMount(async () => {
    ctx = canvas.getContext('2d')!;
    canvas.width = canvasSize;
    canvas.height = canvasSize;
    renderingState.canvasReady = true;

    try {
      const images = await loadAllImages();
      renderingState.gridImage = images.gridImage;
      renderingState.blueStaffImage = images.blueStaffImage;
      renderingState.redStaffImage = images.redStaffImage;
      renderingState.imagesLoaded = true;

      render(); // Initial render
    } catch (error) {
      console.error('Failed to load images:', error);
    }
  });

  function animationLoop(timestamp: number): void {
    if (!$animationState.isPlaying) return;

    if (lastTimestamp === null) lastTimestamp = timestamp;
    const deltaTime = timestamp - lastTimestamp;
    lastTimestamp = timestamp;

    const effectiveSpeed = Math.max(0.01, $animationState.speed);
    const newBeat = $animationState.currentBeat + (deltaTime / 1000) * effectiveSpeed;

    // Handle looping
    if (newBeat >= $animationState.totalBeats) {
      if ($animationState.loop) {
        animationState.update(state => ({ ...state, currentBeat: 0 }));
        lastTimestamp = timestamp;
      } else {
        animationState.update(state => ({ ...state, currentBeat: $animationState.totalBeats, isPlaying: false }));
        return;
      }
    } else {
      animationState.update(state => ({ ...state, currentBeat: newBeat }));
    }

    updatePropStates();

    if ($animationState.isPlaying) {
      animationFrameId = requestAnimationFrame(animationLoop);
    }
  }

  function updatePropStates(): void {
    const sequence = $sequenceData;
    if (sequence.length < 3) return; // Need metadata + start + at least one step

    const clampedBeat = Math.max(0, Math.min($animationState.currentBeat, $animationState.totalBeats));
    const currentStepIndex = Math.floor(clampedBeat === $animationState.totalBeats ? $animationState.totalBeats - 1 : clampedBeat);
    const t = clampedBeat === $animationState.totalBeats ? 1.0 : clampedBeat - currentStepIndex;

    const stepDefinition = sequence[currentStepIndex + 2]; // Account for metadata and start state

    if (stepDefinition && 'blue_attributes' in stepDefinition) {
      const blueEndpoints = calculateStepEndpoints(stepDefinition, 'blue');
      const redEndpoints = calculateStepEndpoints(stepDefinition, 'red');

      if (blueEndpoints && redEndpoints) {
        const blueCenterAngle = lerpAngle(blueEndpoints.startCenterAngle, blueEndpoints.targetCenterAngle, t);
        let blueStaffAngle = lerpAngle(blueEndpoints.startStaffAngle, blueEndpoints.targetStaffAngle, t);

        const redCenterAngle = lerpAngle(redEndpoints.startCenterAngle, redEndpoints.targetCenterAngle, t);
        let redStaffAngle = lerpAngle(redEndpoints.startStaffAngle, redEndpoints.targetStaffAngle, t);

        // ✅ CRITICAL: Pro motion override (like HTML version)
        if (stepDefinition.blue_attributes.motion_type === 'pro') {
          blueStaffAngle = calculateProIsolationStaffAngle(
            blueCenterAngle,
            stepDefinition.blue_attributes.prop_rot_dir,
            stepDefinition.blue_attributes.turns || 0
          );
        }
        if (stepDefinition.red_attributes.motion_type === 'pro') {
          redStaffAngle = calculateProIsolationStaffAngle(
            redCenterAngle,
            stepDefinition.red_attributes.prop_rot_dir,
            stepDefinition.red_attributes.turns || 0
          );
        }

        animationState.update(state => ({
          ...state,
          blueProp: {
            centerPathAngle: blueCenterAngle,
            staffRotationAngle: blueStaffAngle,
            x: 0, y: 0 // Calculated in render
          },
          redProp: {
            centerPathAngle: redCenterAngle,
            staffRotationAngle: redStaffAngle,
            x: 0, y: 0 // Calculated in render
          }
        }));
      }
    }
  }

  function render(): void {
    if (!ctx || !renderingState.imagesLoaded) return;

    ctx.clearRect(0, 0, canvasSize, canvasSize);

    // Draw grid
    if (renderingState.gridImage) {
      drawGrid(ctx, renderingState.gridImage, canvasSize);
    }

    // Draw staffs
    if (renderingState.blueStaffImage && renderingState.redStaffImage) {
      const state = $animationState;

      drawStaff(
        ctx,
        renderingState.blueStaffImage,
        state.blueProp.centerPathAngle,
        state.blueProp.staffRotationAngle,
        canvasSize
      );

      drawStaff(
        ctx,
        renderingState.redStaffImage,
        state.redProp.centerPathAngle,
        state.redProp.staffRotationAngle,
        canvasSize
      );
    }
  }
</script>

<div class="canvas-container">
  <canvas bind:this={canvas}></canvas>
  {#if !renderingState.imagesLoaded}
    <div class="loading-overlay">
      <p>Loading images...</p>
    </div>
  {/if}
</div>

<style>
  .canvas-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    border: 1px solid #e5e7eb;
  }

  canvas {
    display: block;
    max-width: 100%;
    height: auto;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(255, 255, 255, 0.9);
    color: #6b7280;
  }
</style>
