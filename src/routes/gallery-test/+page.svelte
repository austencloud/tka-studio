<!--
Optimized Explore Test Page

Test the new mobile-optimized Explore implementation with:
- Progressive loading
- Infinite scroll
- Skeleton states
- Performance monitoring
-->
<script lang="ts">
  import OptimizedExploreGrid from "$lib/modules/explore/display/components/OptimizedExploreGrid.svelte";
  import type { IExploreThumbnailService } from "$lib/modules/explore/display/services/contracts/IExploreThumbnailService";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  // Services (resolved immediately, no need for reactivity)
  const thumbnailService = resolve<IExploreThumbnailService>(
    TYPES.IExploreThumbnailService
  );
  let hapticService: IHapticFeedbackService;

  // State
  let viewMode: "grid" | "list" = $state("grid");
  let performanceMetrics = $state({
    pageLoadTime: 0,
    firstImageTime: 0,
    totalLoadTime: 0,
  });

  onMount(() => {
    const startTime = performance.now();

    // Initialize haptic service
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Track page load performance
    performanceMetrics.pageLoadTime = Math.round(performance.now() - startTime);

    console.log("🚀 Explore Test Page: Initialized");
  });

  function handleAction(action: string, sequence: any) {
    console.log(`Explore Action: ${action}`, sequence);
  }

  function toggleViewMode() {
    // Trigger selection haptic feedback for view mode toggle
    hapticService?.trigger("selection");
    viewMode = viewMode === "grid" ? "list" : "grid";
  }
</script>

<svelte:head>
  <title>Explore Performance Test - TKA</title>
  <meta name="description" content="Testing optimized Explore performance" />
</svelte:head>

<div class="test-page">
  <!-- Header -->
  <header class="test-header">
    <h1>🚀 Optimized Explore Test</h1>
    <p>Mobile-first Explore with progressive loading</p>

    <!-- Controls -->
    <div class="controls">
      <button class="view-toggle" onclick={toggleViewMode}>
        {viewMode === "grid" ? "📋 List View" : "🔲 Grid View"}
      </button>
    </div>

    <!-- Performance Metrics -->
    <div class="performance-metrics">
      <div class="metric">
        <span class="label">Page Load:</span>
        <span class="value">{performanceMetrics.pageLoadTime}ms</span>
      </div>
    </div>
  </header>

  <!-- Explore -->
  <main class="Explore-main">
    <OptimizedExploreGrid
      {thumbnailService}
      {viewMode}
      onAction={handleAction}
    />
  </main>

  <!-- Footer -->
  <footer class="test-footer">
    <p>
      🔬 This is a test page for the optimized Explore implementation.
      <br />
      Check browser DevTools for performance metrics and network activity.
    </p>
  </footer>
</div>

<style>
  .test-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    color: white;
    padding: 20px;
  }

  .test-header {
    max-width: 1200px;
    margin: 0 auto 40px;
    text-align: center;
  }

  .test-header h1 {
    font-size: 2.5rem;
    margin-bottom: 8px;
    background: linear-gradient(45deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .test-header p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 1.1rem;
    margin-bottom: 24px;
  }

  .controls {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 24px;
  }

  .view-toggle {
    padding: 12px 24px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s ease;
  }

  .view-toggle:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
  }

  .performance-metrics {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 16px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }

  .metric .label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .metric .value {
    font-size: 18px;
    font-weight: bold;
    color: #60a5fa;
  }

  .Explore-main {
    max-width: 1200px;
    margin: 0 auto;
  }

  .test-footer {
    max-width: 1200px;
    margin: 60px auto 0;
    text-align: center;
    padding: 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
    line-height: 1.6;
  }

  /* Mobile optimizations */
  @media (max-width: 768px) {
    .test-page {
      padding: 16px;
    }

    .test-header h1 {
      font-size: 2rem;
    }

    .performance-metrics {
      flex-direction: column;
      gap: 12px;
    }

    .controls {
      flex-direction: column;
      align-items: center;
    }

    .view-toggle {
      width: 200px;
    }
  }

  @media (max-width: 480px) {
    .test-page {
      padding: 12px;
    }

    .test-header h1 {
      font-size: 1.75rem;
    }

    .test-header {
      margin-bottom: 24px;
    }
  }
</style>
