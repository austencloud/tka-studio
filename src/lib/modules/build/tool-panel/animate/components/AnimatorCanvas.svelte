<script lang="ts">
  import {
    GridMode,
    resolve,
    TKAGlyph,
    TYPES,
    type ISettingsService,
    type ISvgImageService,
  } from "$shared";
  import type { PropState } from "../domain/types/PropState";
  import type { ICanvasRenderer } from "../services/contracts/ICanvasRenderer";
  import type { ISVGGenerator } from "../services/contracts/ISVGGenerator";

  // Resolve services from DI container
  const canvasRenderer = resolve(TYPES.ICanvasRenderer) as ICanvasRenderer;
  const svgGenerator = resolve(TYPES.ISVGGenerator) as ISVGGenerator;
  const settingsService = resolve(TYPES.ISettingsService) as ISettingsService;

  // Modern Svelte 5 props
  let {
    blueProp,
    redProp,
    gridVisible = true,
    gridMode = GridMode.DIAMOND,
    letter = null,
  }: {
    blueProp: PropState;
    redProp: PropState;
    gridVisible?: boolean;
    gridMode?: GridMode;
    letter?: import("$shared").Letter | null;
  } = $props();

  // Canvas size is now controlled by CSS container queries
  // Default size for initial render and image loading
  const canvasSize = 500;

  let canvasElement: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D | null = null;
  let gridImage: HTMLImageElement | null = null;
  let blueStaffImage: HTMLImageElement | null = null;
  let redStaffImage: HTMLImageElement | null = null;
  // ViewBox dimensions from the prop SVGs (default to staff dimensions)
  let bluePropDimensions = { width: 252.8, height: 77.8 };
  let redPropDimensions = { width: 252.8, height: 77.8 };
  let imagesLoaded = $state(false);
  let rafId: number | null = null;
  let needsRender = $state(true);
  let currentPropType = $state<string>("staff");

  // Resolve SVG image service
  const svgImageService = resolve(TYPES.ISvgImageService) as ISvgImageService;

  // Track prop changes to trigger re-renders
  $effect(() => {
    blueProp;
    redProp;
    gridVisible;
    gridMode;
    letter;
    needsRender = true;
    startRenderLoop();
  });

  // Load prop images with current prop type
  async function loadPropImages() {
    try {
      const [bluePropData, redPropData] = await Promise.all([
        svgGenerator.generateBluePropSvg(currentPropType),
        svgGenerator.generateRedPropSvg(currentPropType),
      ]);

      // Store the viewBox dimensions
      bluePropDimensions = { width: bluePropData.width, height: bluePropData.height };
      redPropDimensions = { width: redPropData.width, height: redPropData.height };

      [blueStaffImage, redStaffImage] = await Promise.all([
        svgImageService.convertSvgStringToImage(
          bluePropData.svg,
          bluePropData.width,
          bluePropData.height
        ),
        svgImageService.convertSvgStringToImage(
          redPropData.svg,
          redPropData.width,
          redPropData.height
        ),
      ]);

      imagesLoaded = true;
      needsRender = true;
      startRenderLoop();
    } catch (err) {
      console.error("Failed to load prop images:", err);
    }
  }

  // Initial load of images and canvas setup
  $effect(() => {
    // Track canvasElement so effect re-runs when it's bound
    if (!canvasElement) return;

    const loadImages = async () => {
      try {
        gridImage = await svgImageService.convertSvgStringToImage(
          svgGenerator.generateGridSvg(gridMode),
          canvasSize,
          canvasSize
        );

        // Check if canvas still exists after async operations
        if (!canvasElement) {
          console.warn("Canvas element became null during image loading");
          return;
        }

        ctx = canvasElement.getContext("2d");
        if (!ctx) {
          console.error("Failed to get 2D context from canvas");
          return;
        }

        // Load prop images
        await loadPropImages();
      } catch (err) {
        console.error("Failed to load SVG images:", err);
      }
    };

    loadImages();

    return () => {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }
    };
  });

  // Watch for prop type changes in settings
  $effect(() => {
    const settings = settingsService.currentSettings;
    const newPropType = settings.propType || "staff";
    if (newPropType !== currentPropType) {
      console.log("🎨 Prop type changed in animator, reloading images:", newPropType);
      currentPropType = newPropType;
      imagesLoaded = false;
      loadPropImages();
    }
  });



  function renderLoop(): void {
    if (!ctx || !imagesLoaded) return;

    if (needsRender) {
      render();
      needsRender = false;
      rafId = requestAnimationFrame(renderLoop);
    } else {
      rafId = null;
    }
  }

  function startRenderLoop(): void {
    if (rafId === null && ctx && imagesLoaded) {
      rafId = requestAnimationFrame(renderLoop);
    }
  }

  function render(): void {
    if (!ctx || !imagesLoaded) return;

    canvasRenderer.renderScene(
      ctx,
      canvasSize,
      gridVisible,
      gridImage,
      blueStaffImage,
      redStaffImage,
      blueProp,
      redProp,
      bluePropDimensions,
      redPropDimensions
    );
  }
</script>

<div class="canvas-wrapper">
  <canvas
    bind:this={canvasElement}
    width={canvasSize}
    height={canvasSize}
  ></canvas>

  <!-- SVG overlay for TKA Glyph - positioned absolutely on top of canvas -->
  <svg
    class="glyph-overlay"
    viewBox="0 0 950 950"
  >
    {#if letter}
      <TKAGlyph {letter} />
    {/if}
  </svg>
</div>

<style>
  .canvas-wrapper {
    position: relative;
    display: inline-block;
    /* CRITICAL: Always maintain 1:1 aspect ratio */
    aspect-ratio: 1 / 1;
    /* Size based on the SMALLER of container width or height to ensure it fits */
    /* Use min() to take the smaller dimension, then apply percentage */
    width: min(90cqw, 90cqh, 350px);
    max-width: 600px;
    max-height: 600px;
  }

  /* Responsive sizing using container queries based on BOTH dimensions */
  @container (min-width: 400px) and (min-height: 400px) {
    .canvas-wrapper {
      width: min(85cqw, 85cqh, 400px);
    }
  }

  @container (min-width: 600px) and (min-height: 600px) {
    .canvas-wrapper {
      width: min(80cqw, 80cqh, 500px);
    }
  }

  @container (min-width: 800px) and (min-height: 800px) {
    .canvas-wrapper {
      width: min(75cqw, 75cqh, 600px);
    }
  }

  canvas {
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    background: #ffffff;
    transition: all 0.3s ease;
    display: block;
    /* CRITICAL: Canvas must be perfectly square - 100% of wrapper which has aspect-ratio 1/1 */
    width: 100%;
    height: 100%;
  }

  .glyph-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none; /* Allow clicks to pass through to canvas */
    z-index: 10; /* Render on top of canvas */
  }
</style>
