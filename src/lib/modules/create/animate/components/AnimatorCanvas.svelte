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
    type BeatData,
  } from "$shared";
  import type { PropState } from "../domain/types/PropState";
  import type { ICanvasRenderer } from "../services/contracts/ICanvasRenderer";
  import type { ISVGGenerator } from "../services/contracts/ISVGGenerator";
  import GlyphRenderer from "./GlyphRenderer.svelte";

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
    beatData = null,
    onCanvasReady = () => {},
  }: {
    blueProp: PropState | null;
    redProp: PropState | null;
    gridVisible?: boolean;
    gridMode?: GridMode | null;
    letter?: import("$shared").Letter | null;
    beatData?: BeatData | null;
    onCanvasReady?: (canvas: HTMLCanvasElement | null) => void;
  } = $props();

  // Canvas size is now controlled by CSS container queries
  // Default size for initial render and image loading
  const DEFAULT_CANVAS_SIZE = 500;
  let canvasSize = $state(DEFAULT_CANVAS_SIZE);
  let canvasResolution = $state(DEFAULT_CANVAS_SIZE);

  let canvasElement: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D | null = null;
  let gridImage: HTMLImageElement | null = null;
  let blueStaffImage: HTMLImageElement | null = null;
  let redStaffImage: HTMLImageElement | null = null;
  // Glyph state - unified rendering of complete TKAGlyph (letter + turns + future same/opp dots)
  let glyphImage: HTMLImageElement | null = null;
  let previousGlyphImage: HTMLImageElement | null = null;
  let glyphDimensions = { width: 0, height: 0, x: 0, y: 0 };
  let previousGlyphDimensions = { width: 0, height: 0, x: 0, y: 0 };
  let resizeObserver: ResizeObserver | null = null;

  // ViewBox dimensions from the prop SVGs (default to staff dimensions)
  let bluePropDimensions = { width: 252.8, height: 77.8 };
  let redPropDimensions = { width: 252.8, height: 77.8 };
  let imagesLoaded = $state(false);
  let rafId: number | null = null;
  let needsRender = $state(true);
  let currentPropType = $state<string>("staff");

  // Fade transition state
  let fadeProgress = $state(0); // 0 = show previous, 1 = show current
  let isFading = $state(false);
  let fadeStartTime: number | null = null;
  const FADE_DURATION_MS = 150; // 150ms crossfade

  // Resolve SVG image service
  const svgImageService = resolve(TYPES.ISvgImageService) as ISvgImageService;

  // Track prop changes
  $effect(() => {
    letter;
    beatData;
  });

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
      bluePropDimensions = {
        width: bluePropData.width,
        height: bluePropData.height,
      };
      redPropDimensions = {
        width: redPropData.width,
        height: redPropData.height,
      };

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

  function resizeCanvasToWrapper() {
    if (!canvasElement) return;

    const rect = canvasElement.getBoundingClientRect();
    const nextDisplaySize =
      Math.min(
        rect.width || DEFAULT_CANVAS_SIZE,
        rect.height || DEFAULT_CANVAS_SIZE
      ) || DEFAULT_CANVAS_SIZE;
    const pixelRatio =
      typeof window !== "undefined" && window.devicePixelRatio
        ? window.devicePixelRatio
        : 1;

    canvasSize = nextDisplaySize;
    canvasResolution = Math.max(1, Math.round(nextDisplaySize * pixelRatio));

    canvasElement.width = canvasResolution;
    canvasElement.height = canvasResolution;

    if (ctx) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(pixelRatio, pixelRatio);
    }

    needsRender = true;
  }

  function teardownResizeObservers() {
    resizeObserver?.disconnect();
    resizeObserver = null;
    if (typeof window !== "undefined") {
      window.removeEventListener("resize", resizeCanvasToWrapper);
    }
  }

  // Initial load of images and canvas setup
  $effect(() => {
    // Track canvasElement so effect re-runs when it's bound
    if (!canvasElement) return;
    onCanvasReady?.(canvasElement);

    const loadImages = async () => {
      try {
        gridImage = await svgImageService.convertSvgStringToImage(
          svgGenerator.generateGridSvg(gridMode ?? GridMode.DIAMOND),
          canvasSize,
          canvasSize
        );

        // Check if canvas still exists after async operations
        if (!canvasElement) {
          return;
        }

        ctx = canvasElement.getContext("2d");
        if (!ctx) {
          console.error("Failed to get 2D context from canvas");
          return;
        }

        resizeCanvasToWrapper();
        teardownResizeObservers();
        if (typeof ResizeObserver !== "undefined") {
          resizeObserver = new ResizeObserver(() => resizeCanvasToWrapper());
          resizeObserver.observe(canvasElement);
        }
        if (typeof window !== "undefined") {
          window.addEventListener("resize", resizeCanvasToWrapper);
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
      teardownResizeObservers();
      onCanvasReady?.(null);
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

  // Callback from GlyphRenderer when SVG is ready
  function handleGlyphSvgReady(
    svgString: string,
    width: number,
    height: number,
    x: number,
    y: number
  ) {
    loadGlyphFromSvg(svgString, width, height, x, y);
  }

  /**
   * Load glyph from SVG string (called by GlyphRenderer)
   * Converts the complete TKAGlyph SVG to an image for canvas rendering
   */
  async function loadGlyphFromSvg(
    svgString: string,
    width: number,
    height: number,
    x: number,
    y: number
  ) {
    try {
      // Save previous glyph for fade transition
      const hadPreviousGlyph = glyphImage !== null;
      if (hadPreviousGlyph) {
        previousGlyphImage = glyphImage;
        previousGlyphDimensions = glyphDimensions;
      }

      // Convert SVG string to image
      // IMPORTANT: The SVG has viewBox="0 0 950 950", so we must create the image at 950x950
      // The width/height/x/y parameters tell us where the glyph is within that 950x950 space
      const newImage = await svgImageService.convertSvgStringToImage(
        svgString,
        950,
        950
      );

      glyphImage = newImage;
      glyphDimensions = { width, height, x, y };

      // Start fade transition if we had a previous glyph
      if (hadPreviousGlyph) {
        startFadeTransition();
      } else {
        // First glyph - no fade
        needsRender = true;
        startRenderLoop();
      }
    } catch (err) {
      console.error("[AnimatorCanvas] Failed to load glyph from SVG:", err);
      glyphImage = null;
      glyphDimensions = { width: 0, height: 0, x: 0, y: 0 };
    }
  }

  function startFadeTransition() {
    isFading = true;
    fadeProgress = 0;
    fadeStartTime = performance.now();
    needsRender = true;
    startRenderLoop();
  }

  function updateFadeProgress(currentTime: number) {
    if (!isFading || fadeStartTime === null) return;

    const elapsed = currentTime - fadeStartTime;
    fadeProgress = Math.min(elapsed / FADE_DURATION_MS, 1);

    if (fadeProgress >= 1) {
      // Fade complete - clear previous glyph
      isFading = false;
      fadeProgress = 1;
      previousGlyphImage = null;
      previousGlyphDimensions = { width: 0, height: 0, x: 0, y: 0 };
    }

    needsRender = true;
  }

  function renderLoop(currentTime?: number): void {
    if (!ctx || !imagesLoaded) {
      rafId = null;
      return;
    }

    // Update fade progress if fading
    if (isFading && currentTime !== undefined) {
      updateFadeProgress(currentTime);
    }

    if (needsRender || isFading) {
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

    // Render complete glyph (letter + turns + future same/opp dots) with crossfade
    if (isFading) {
      // Draw previous glyph fading out
      if (previousGlyphImage && previousGlyphDimensions.width > 0) {
        ctx.globalAlpha = 1 - fadeProgress;
        renderGlyphToCanvas(previousGlyphImage, previousGlyphDimensions);
      }

      // Draw current glyph fading in
      if (glyphImage && glyphDimensions.width > 0) {
        ctx.globalAlpha = fadeProgress;
        renderGlyphToCanvas(glyphImage, glyphDimensions);
      }

      // Reset alpha
      ctx.globalAlpha = 1;
    } else {
      // Normal rendering - no fade
      if (glyphImage && glyphDimensions.width > 0) {
        renderGlyphToCanvas(glyphImage, glyphDimensions);
      }
    }
  }

  /**
   * Render a complete glyph image to canvas
   * The glyph image has a full 950x950 viewBox, so we draw the entire image scaled to canvas
   * The dimensions parameter tells us where the glyph is within that viewBox (for reference only)
   */
  function renderGlyphToCanvas(
    image: HTMLImageElement,
    dimensions: { width: number; height: number; x: number; y: number }
  ): void {
    if (!ctx) return;

    // Calculate scale factor from 950px viewBox to canvas
    const scale = canvasSize / 950;

    // The image contains the full 950x950 viewBox, so we draw it at (0, 0) covering the entire canvas
    // The glyph will appear in the correct position because it's positioned correctly within the SVG
    ctx.drawImage(image, 0, 0, canvasSize, canvasSize);
  }
</script>

<!-- Hidden GlyphRenderer that converts TKAGlyph to SVG for canvas rendering -->
{#if letter}
  <GlyphRenderer {letter} {beatData} onSvgReady={handleGlyphSvgReady} />
{/if}

<div class="canvas-wrapper">
  <canvas
    bind:this={canvasElement}
    width={canvasResolution}
    height={canvasResolution}
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
