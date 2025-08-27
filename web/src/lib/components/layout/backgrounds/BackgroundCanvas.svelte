<!--
Simple Background Canvas - No Context Dependencies

A simplified background canvas component that works directly with BackgroundFactory
without the complex BackgroundContext system.
-->
<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { BackgroundFactory } from "$lib/services/implementations/background/BackgroundFactory";
  import type {
    BackgroundType,
    PerformanceMetrics,
    QualityLevel,
    BackgroundSystem,
  } from "$lib/domain/background/BackgroundTypes";
  import { browser } from "$app/environment";

  // Props
  const {
    backgroundType = "nightSky" as BackgroundType,
    quality = "medium" as QualityLevel,
    onReady,
    onPerformanceReport,
  } = $props<{
    backgroundType?: BackgroundType;
    quality?: QualityLevel;
    onReady?: () => void;
    onPerformanceReport?: (metrics: PerformanceMetrics) => void;
  }>();

  // State
  let canvas: HTMLCanvasElement;
  let isInitialized = $state(false);
  let currentBackgroundSystem: BackgroundSystem | null = null;
  let animationId: number | null = null;
  let resizeObserver: ResizeObserver | null = null;

  // Create background system when props change
  $effect(() => {
    if (!browser || !canvas) return;

    // Cleanup previous system
    if (currentBackgroundSystem) {
      currentBackgroundSystem.cleanup();
    }

    // Create new system
    currentBackgroundSystem = BackgroundFactory.createBackgroundSystem({
      type: backgroundType,
      initialQuality: quality,
    });

    // Set up canvas dimensions properly
    setupCanvasDimensions();
  });

  // Animation loop
  function startAnimation() {
    if (!canvas || !currentBackgroundSystem) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const animate = () => {
      if (!currentBackgroundSystem || !canvas) return;

      // Use canvas internal dimensions, not getBoundingClientRect
      const dimensions = { width: canvas.width, height: canvas.height };

      // Update and draw
      currentBackgroundSystem.update(dimensions);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      currentBackgroundSystem.draw(ctx, dimensions);

      // Report performance
      if (onPerformanceReport) {
        onPerformanceReport({ fps: 60, warnings: [] });
      }

      animationId = requestAnimationFrame(animate);
    };

    animationId = requestAnimationFrame(animate);
  }

  function stopAnimation() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
  }

  // Mount lifecycle
  onMount(() => {
    if (!browser || !canvas) return;

    // Ensure canvas dimensions are set up correctly on mount
    setupCanvasDimensions();

    // Set up ResizeObserver for smooth resize handling
    if (typeof ResizeObserver !== "undefined") {
      console.log("CANVAS SETUP: Creating ResizeObserver");
      resizeObserver = new ResizeObserver((entries) => {
        console.log(
          "RESIZE OBSERVER: triggered with",
          entries.length,
          "entries"
        );
        for (const entry of entries) {
          if (entry.target === canvas) {
            console.log(
              "RESIZE OBSERVER: canvas entry found, calling handleResize"
            );
            handleResize();
          }
        }
      });
      resizeObserver.observe(canvas);
      console.log("CANVAS SETUP: ResizeObserver observing canvas");
    } else {
      console.log("CANVAS SETUP: ResizeObserver not available");
    }

    isInitialized = true;
    startAnimation();
    onReady?.();
  });

  // Cleanup
  onDestroy(() => {
    stopAnimation();
    if (currentBackgroundSystem) {
      currentBackgroundSystem.cleanup();
    }
    if (resizeObserver) {
      resizeObserver.disconnect();
      resizeObserver = null;
    }
  });

  // Set up canvas dimensions to match display size
  function setupCanvasDimensions() {
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const dimensions = { width: rect.width, height: rect.height };

    // Set canvas internal dimensions to match display dimensions
    canvas.width = dimensions.width;
    canvas.height = dimensions.height;

    // Initialize background system with correct dimensions
    if (currentBackgroundSystem) {
      currentBackgroundSystem.initialize(dimensions, quality);

      // Immediately draw one frame to ensure background is visible
      const ctx = canvas.getContext("2d");
      if (ctx) {
        currentBackgroundSystem.draw(ctx, dimensions);
      }
    }
  }

  // Handle resize - preserve existing content and smoothly adapt
  function handleResize() {
    console.log("CANVAS RESIZE: handleResize called");
    if (!currentBackgroundSystem || !canvas) {
      console.log("CANVAS RESIZE: early return - no system or canvas");
      return;
    }

    const rect = canvas.getBoundingClientRect();
    const newDimensions = { width: rect.width, height: rect.height };
    const oldDimensions = { width: canvas.width, height: canvas.height };

    console.log(
      `CANVAS RESIZE: dimensions ${oldDimensions.width}x${oldDimensions.height} -> ${newDimensions.width}x${newDimensions.height}`
    );

    // Only resize if dimensions actually changed
    if (
      newDimensions.width === oldDimensions.width &&
      newDimensions.height === oldDimensions.height
    ) {
      console.log("CANVAS RESIZE: no change in dimensions, skipping");
      return;
    }

    // Store current canvas content if we need to preserve it
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Update canvas size (this will clear the canvas)
    canvas.width = newDimensions.width;
    canvas.height = newDimensions.height;

    // Use handleResize method if available, otherwise just update
    if (currentBackgroundSystem.handleResize) {
      currentBackgroundSystem.handleResize(oldDimensions, newDimensions);
    } else {
      // Fallback to update method
      currentBackgroundSystem.update(newDimensions);
    }

    // Immediately draw one frame to prevent showing blank/fallback content
    currentBackgroundSystem.draw(ctx, newDimensions);
  }
</script>

<canvas
  bind:this={canvas}
  class="background-canvas"
  class:initialized={isInitialized}
  aria-label="Background animation"
>
  <!-- Fallback for non-canvas browsers -->
  <p>Background animation not supported</p>
</canvas>

<style>
  .background-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
  }

  .background-canvas.initialized {
    opacity: 1;
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .background-canvas {
      transition: none;
    }
  }
</style>
