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

    // Initialize with canvas dimensions
    const rect = canvas.getBoundingClientRect();
    const dimensions = { width: rect.width, height: rect.height };
    currentBackgroundSystem.initialize(dimensions, quality);

    console.log(`✅ Background system created: ${backgroundType} (${quality})`);
  });

  // Animation loop
  function startAnimation() {
    if (!canvas || !currentBackgroundSystem) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const animate = () => {
      if (!currentBackgroundSystem || !canvas) return;

      const rect = canvas.getBoundingClientRect();
      const dimensions = { width: rect.width, height: rect.height };

      // Update and draw
      currentBackgroundSystem.update(dimensions);
      ctx.clearRect(0, 0, dimensions.width, dimensions.height);
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

    isInitialized = true;
    startAnimation();
    onReady?.();

    console.log("✅ Simple background canvas initialized");
  });

  // Cleanup
  onDestroy(() => {
    stopAnimation();
    if (currentBackgroundSystem) {
      currentBackgroundSystem.cleanup();
    }
  });

  // Handle resize
  function handleResize() {
    if (!currentBackgroundSystem || !canvas) return;

    const rect = canvas.getBoundingClientRect();
    const dimensions = { width: rect.width, height: rect.height };

    // Update canvas size
    canvas.width = dimensions.width;
    canvas.height = dimensions.height;

    // Update background system with new dimensions
    currentBackgroundSystem.update(dimensions);
  }
</script>

<svelte:window on:resize={handleResize} />

<canvas
  bind:this={canvas}
  class="background-canvas"
  class:initialized={isInitialized}
  width="800"
  height="600"
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
