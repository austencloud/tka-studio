<script lang="ts">
  import { GridMode } from "$shared";
  import type { ISvgImageService } from "$shared/foundation/services/contracts";
  import { resolve, TYPES } from "$shared/inversify";
  import type { PropState } from "../domain";
  import { CanvasRenderer, SVGGenerator } from "../services/implementations";
  // TODO: Fix missing SVGGenerator and CanvasRenderer imports
  // import { SVGGenerator } from "$utils";
  // import { CanvasRenderer } from "$utils";

  // Modern Svelte 5 props
  let {
    blueProp,
    redProp,
    canvasSize = 500,
    width,
    height,
    gridVisible = true,
    gridMode = GridMode.DIAMOND,
  }: {
    blueProp: PropState;
    redProp: PropState;
    canvasSize?: number;
    width?: number;
    height?: number;
    gridVisible?: boolean;
    gridMode?: GridMode;
  } = $props();

  // Use width/height if provided, otherwise use canvasSize
  const actualSize = width && height ? Math.min(width, height) : canvasSize;

  let canvasElement: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D | null = null;
  let gridImage: HTMLImageElement | null = null;
  let blueStaffImage: HTMLImageElement | null = null;
  let redStaffImage: HTMLImageElement | null = null;
  let imagesLoaded = $state(false);
  let rafId: number | null = null;
  let needsRender = $state(true);

  // Resolve SVG image service
  const svgImageService = resolve(TYPES.ISvgImageService) as ISvgImageService;

  // Track prop changes to trigger re-renders
  $effect(() => {
    blueProp;
    redProp;
    gridVisible;
    gridMode;
    needsRender = true;
    startRenderLoop();
  });

  // Initial load of images and canvas setup
  $effect(() => {
    const loadImages = async () => {
      try {
        [gridImage, blueStaffImage, redStaffImage] = await Promise.all([
          svgImageService.convertSvgStringToImage(
            SVGGenerator.generateGridSvg(gridMode),
            actualSize,
            actualSize
          ),
          svgImageService.convertSvgStringToImage(SVGGenerator.generateBlueStaffSvg(), 252.8, 77.8),
          svgImageService.convertSvgStringToImage(SVGGenerator.generateRedStaffSvg(), 252.8, 77.8),
        ]);

        ctx = canvasElement.getContext("2d");
        imagesLoaded = true;
        needsRender = true;
        startRenderLoop();
      } catch (err) {
        console.error("Failed to load SVG images:", err);
      }
    };

    if (canvasElement) {
      loadImages();
    }

    return () => {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }
    };
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

    CanvasRenderer.renderScene(
      ctx,
      actualSize,
      gridVisible,
      gridImage,
      blueStaffImage,
      redStaffImage,
      blueProp,
      redProp
    );
  }
</script>

<div class="canvas-wrapper">
  <canvas
    bind:this={canvasElement}
    width={actualSize}
    height={actualSize}
    style:width="{actualSize}px"
    style:height="{actualSize}px"
  ></canvas>
</div>

<style>
  .canvas-wrapper {
    position: relative;
    display: inline-block;
  }

  canvas {
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    background: #ffffff;
    transition: all 0.3s ease;
    display: block;
  }
</style>
