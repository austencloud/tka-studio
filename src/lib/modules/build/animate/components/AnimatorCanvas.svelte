<!--
AnimatorCanvas.svelte

Canvas component for rendering animated prop positions.
Handles prop visualization, SVG rendering, and canvas drawing
for sequence animation playback.
-->
<script lang="ts">
  import {
    GridMode,
    resolve,
    TYPES,
    type ISettingsService,
    type ISvgImageService,
  } from "$shared";
  import { getLetterImagePath } from "$shared/pictograph/tka-glyph/utils";
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
    blueProp: PropState | null;
    redProp: PropState | null;
    gridVisible?: boolean;
    gridMode?: GridMode | null;
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
  let letterImage: HTMLImageElement | null = null;
  // ViewBox dimensions from the prop SVGs (default to staff dimensions)
  let bluePropDimensions = { width: 252.8, height: 77.8 };
  let redPropDimensions = { width: 252.8, height: 77.8 };
  let letterDimensions = { width: 0, height: 0 };
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
          svgGenerator.generateGridSvg(gridMode ?? GridMode.DIAMOND),
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
        rafId = null;
      }
    };
  });

  // Watch for prop type changes in settings
  $effect(() => {
    const settings = settingsService.currentSettings;
    const newPropType = settings.propType || "staff";
    if (newPropType !== currentPropType) {
      currentPropType = newPropType;
      imagesLoaded = false;
      loadPropImages();
    }
  });

  // Load letter image when letter changes
  $effect(() => {
    if (letter) {
      loadLetterImage();
    } else {
      letterImage = null;
      letterDimensions = { width: 0, height: 0 };
      needsRender = true;
      startRenderLoop();
    }
  });

  async function loadLetterImage() {
    if (!letter) {
      letterImage = null;
      letterDimensions = { width: 0, height: 0 };
      return;
    }

    try {
      const imagePath = getLetterImagePath(letter);
      const response = await fetch(imagePath);
      if (!response.ok) {
        console.warn(`Failed to load letter image: ${imagePath}`);
        letterImage = null;
        letterDimensions = { width: 0, height: 0 };
        return;
      }

      const svgText = await response.text();

      // Parse SVG dimensions from viewBox
      const viewBoxMatch = svgText.match(/viewBox\s*=\s*"[\d.-]+\s+[\d.-]+\s+([\d.-]+)\s+([\d.-]+)"/i);
      const width = viewBoxMatch ? parseFloat(viewBoxMatch[1] || '100') : 100;
      const height = viewBoxMatch ? parseFloat(viewBoxMatch[2] || '100') : 100;

      // Store the viewBox dimensions
      letterDimensions = { width, height };

      // Convert SVG to image
      letterImage = await svgImageService.convertSvgStringToImage(svgText, width, height);
      needsRender = true;
      startRenderLoop();
    } catch (err) {
      console.error("Failed to load letter image:", err);
      letterImage = null;
      letterDimensions = { width: 0, height: 0 };
    }
  }

  function renderLoop(): void {
    if (!ctx || !imagesLoaded) {
      rafId = null;
      return;
    }

    if (needsRender) {
      render();
      needsRender = false;
      rafId = requestAnimationFrame(renderLoop);
    } else {
      // Stop loop when no render is needed
      rafId = null;
    }
  }

  function startRenderLoop(): void {
    if (rafId === null && ctx && imagesLoaded) {
      rafId = requestAnimationFrame(renderLoop);
    }
  }

  function render(): void {
    if (!ctx || !imagesLoaded || !blueProp || !redProp) return;

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

    // Render letter on top if we have one
    if (letterImage && letterDimensions.width > 0) {
      canvasRenderer.renderLetterToCanvas(ctx, canvasSize, letterImage, letterDimensions);
    }
  }
</script>

<div class="canvas-wrapper">
  <canvas
    bind:this={canvasElement}
    width={canvasSize}
    height={canvasSize}
  ></canvas>
</div>

<style>
  .canvas-wrapper {
    position: relative;
    display: inline-block;
    /* CRITICAL: Always maintain 1:1 aspect ratio */
    aspect-ratio: 1 / 1;
    /* Size based on the SMALLER of container width or height to ensure it fits */
    /* Use min() to take the smaller dimension, but allow it to grow larger */
    width: min(95cqw, 95cqh);
    max-width: 600px;
    max-height: 600px;
  }

  /* Responsive sizing using container queries based on BOTH dimensions */
  @container (min-width: 300px) and (min-height: 300px) {
    .canvas-wrapper {
      width: min(92cqw, 92cqh);
    }
  }

  @container (min-width: 400px) and (min-height: 400px) {
    .canvas-wrapper {
      width: min(90cqw, 90cqh);
    }
  }

  @container (min-width: 600px) and (min-height: 600px) {
    .canvas-wrapper {
      width: min(85cqw, 85cqh);
    }
  }

  @container (min-width: 800px) and (min-height: 800px) {
    .canvas-wrapper {
      width: min(80cqw, 80cqh);
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
</style>
