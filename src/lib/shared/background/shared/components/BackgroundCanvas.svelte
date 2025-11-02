<!--
Simple Background Canvas - No Context Dependencies

A simplified background canvas component that works directly with BackgroundFactory
without the complex BackgroundContext system.
-->
<script lang="ts">
  import { browser } from "$app/environment";
  import { onDestroy, onMount } from "svelte";
  import type {
    BackgroundSystem,
    BackgroundType,
    PerformanceMetrics,
    QualityLevel,
  } from "../domain";
  import { BackgroundFactory } from "../services/implementations";

  // Props
  const {
    backgroundType = "nightSky" as BackgroundType,
    quality = "medium" as QualityLevel,
    backgroundColor,
    gradientColors,
    gradientDirection,
    thumbnailMode = false,
    onReady,
    onPerformanceReport,
  } = $props<{
    backgroundType?: BackgroundType;
    quality?: QualityLevel;
    backgroundColor?: string;
    gradientColors?: string[];
    gradientDirection?: number;
    thumbnailMode?: boolean;
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
    if (!browser || !canvas) {
      return;
    }

    // Cleanup previous system
    if (currentBackgroundSystem) {
      stopAnimation(); // Stop animation before cleanup
      currentBackgroundSystem.cleanup();
      currentBackgroundSystem = null; // Clear reference immediately
    }

    // Clear the canvas immediately to remove any previous background elements
    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Create background system using BackgroundFactory (async)
    BackgroundFactory.createBackgroundSystem({
      type: backgroundType,
      quality: quality,
      initialQuality: quality,
      thumbnailMode,
      backgroundColor,
      gradientColors,
      gradientDirection,
    }).then((system) => {
      currentBackgroundSystem = system;
      // Set up canvas dimensions properly
      setupCanvasDimensions();
      // Start animation with new system
      startAnimation();
    });
  });

  // Animation loop
  function startAnimation() {
    if (!canvas || !currentBackgroundSystem) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let lastTimestamp = 0;

    const animate = (timestamp: number) => {
      if (!currentBackgroundSystem || !canvas) return;

      // Calculate delta time and frame multiplier
      const deltaTime = timestamp - lastTimestamp;
      lastTimestamp = timestamp;

      // Calculate frame multiplier to normalize animation speed across different refresh rates
      // Target 60fps as baseline: frameMultiplier = actualFrameTime / targetFrameTime
      // At 60fps: deltaTime ≈ 16.67ms, frameMultiplier ≈ 1.0
      // At 144fps: deltaTime ≈ 6.94ms, frameMultiplier ≈ 0.42
      // At 240fps: deltaTime ≈ 4.17ms, frameMultiplier ≈ 0.25
      const targetFrameTime = 1000 / 60; // 16.67ms for 60fps
      const frameMultiplier = deltaTime > 0 ? deltaTime / targetFrameTime : 1.0;

      // Use canvas internal dimensions, not getBoundingClientRect
      const dimensions = { width: canvas.width, height: canvas.height };

      // Update and draw with frame multiplier for consistent animation speed
      currentBackgroundSystem.update(dimensions, frameMultiplier);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      currentBackgroundSystem.draw(ctx, dimensions);

      // Report performance with actual FPS
      if (onPerformanceReport) {
        const actualFPS = deltaTime > 0 ? Math.round(1000 / deltaTime) : 60;
        onPerformanceReport({ fps: actualFPS, warnings: [] });
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

    // Set up ResizeObserver for smooth resize handling
    if (typeof ResizeObserver !== "undefined") {
      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          if (entry.target === canvas) {
            handleResize();
          }
        }
      });
      resizeObserver.observe(canvas);
    }

    isInitialized = true;
    // Animation will be started by $effect after background system is created
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
    if (!currentBackgroundSystem || !canvas) {
      return;
    }

    const rect = canvas.getBoundingClientRect();
    const newDimensions = { width: rect.width, height: rect.height };
    const oldDimensions = { width: canvas.width, height: canvas.height };

    // Only resize if dimensions actually changed
    if (
      newDimensions.width === oldDimensions.width &&
      newDimensions.height === oldDimensions.height
    ) {
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
