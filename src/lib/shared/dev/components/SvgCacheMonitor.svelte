<script lang="ts">
  /**
   * SVG Cache Performance Monitor
   *
   * 🚀 2025 OPTIMIZATION: Development tool to track cache performance
   *
   * Displays real-time cache statistics for arrows and props:
   * - Cache hit rate (% of cached vs fresh fetches)
   * - Number of cached items
   * - Memory usage estimate
   *
   * Usage: Add to bottom of MainInterface.svelte in dev mode
   */

  import { onMount } from "svelte";
  import { resolve, TYPES } from "$shared/inversify";
  import type { IArrowSvgLoader, IPropSvgLoader } from "$shared";

  let arrowStats = $state({ rawCacheSize: 0, transformedCacheSize: 0, cacheHits: 0, cacheMisses: 0, hitRate: "0%" });
  let propStats = $state({ rawCacheSize: 0, transformedCacheSize: 0, metadataCacheSize: 0, cacheHits: 0, cacheMisses: 0, hitRate: "0%" });
  let updateInterval: ReturnType<typeof setInterval> | null = null;
  let isExpanded = $state(false);

  function updateStats() {
    try {
      const arrowLoader = resolve<any>(TYPES.IArrowSvgLoader);
      const propLoader = resolve<any>(TYPES.IPropSvgLoader);

      if (arrowLoader && typeof arrowLoader.getCacheStats === "function") {
        arrowStats = arrowLoader.getCacheStats();
      }

      if (propLoader && typeof propLoader.getCacheStats === "function") {
        propStats = propLoader.getCacheStats();
      }
    } catch (error) {
      console.error("SvgCacheMonitor: Error reading cache stats:", error);
    }
  }

  onMount(() => {
    updateStats();
    updateInterval = setInterval(updateStats, 1000); // Update every second

    return () => {
      if (updateInterval) {
        clearInterval(updateInterval);
      }
    };
  });

  function toggleExpanded() {
    isExpanded = !isExpanded;
  }

  function clearCaches() {
    try {
      const arrowLoader = resolve<any>(TYPES.IArrowSvgLoader);
      const propLoader = resolve<any>(TYPES.IPropSvgLoader);

      if (arrowLoader && typeof arrowLoader.clearCache === "function") {
        arrowLoader.clearCache();
      }

      if (propLoader && typeof propLoader.clearCache === "function") {
        propLoader.clearCache();
      }

      updateStats();
    } catch (error) {
      console.error("SvgCacheMonitor: Error clearing caches:", error);
    }
  }
</script>

<div class="svg-cache-monitor" class:expanded={isExpanded}>
  <!-- Collapsed view - just the summary bar -->
  <button class="monitor-header" onclick={toggleExpanded}>
    <span class="title">🚀 SVG Cache Monitor</span>
    <span class="summary">
      Arrows: {arrowStats.hitRate} | Props: {propStats.hitRate}
    </span>
    <span class="toggle">{isExpanded ? "▼" : "▲"}</span>
  </button>

  {#if isExpanded}
    <div class="monitor-body">
      <!-- Arrow Stats -->
      <div class="stats-section">
        <h4>Arrow Cache</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Hit Rate:</span>
            <span class="stat-value" class:good={parseFloat(arrowStats.hitRate) > 80}>
              {arrowStats.hitRate}
            </span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Hits:</span>
            <span class="stat-value">{arrowStats.cacheHits}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Misses:</span>
            <span class="stat-value">{arrowStats.cacheMisses}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Raw Cache:</span>
            <span class="stat-value">{arrowStats.rawCacheSize} items</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Transformed:</span>
            <span class="stat-value">{arrowStats.transformedCacheSize} items</span>
          </div>
        </div>
      </div>

      <!-- Prop Stats -->
      <div class="stats-section">
        <h4>Prop Cache</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Hit Rate:</span>
            <span class="stat-value" class:good={parseFloat(propStats.hitRate) > 80}>
              {propStats.hitRate}
            </span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Hits:</span>
            <span class="stat-value">{propStats.cacheHits}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Misses:</span>
            <span class="stat-value">{propStats.cacheMisses}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Raw Cache:</span>
            <span class="stat-value">{propStats.rawCacheSize} items</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Transformed:</span>
            <span class="stat-value">{propStats.transformedCacheSize} items</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Metadata:</span>
            <span class="stat-value">{propStats.metadataCacheSize} items</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="actions">
        <button class="btn-clear" onclick={clearCaches}>
          Clear Caches
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .svg-cache-monitor {
    position: fixed;
    bottom: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.9);
    color: #00ff00;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    z-index: 9999;
    border-top-left-radius: 8px;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
    max-width: 400px;
  }

  .monitor-header {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    background: rgba(0, 0, 0, 0.8);
    border: none;
    color: inherit;
    cursor: pointer;
    font-family: inherit;
    font-size: inherit;
  }

  .monitor-header:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .title {
    font-weight: bold;
  }

  .summary {
    flex: 1;
    color: #00aa00;
  }

  .toggle {
    opacity: 0.5;
  }

  .monitor-body {
    padding: 12px;
    max-height: 400px;
    overflow-y: auto;
  }

  .stats-section {
    margin-bottom: 16px;
  }

  .stats-section:last-of-type {
    margin-bottom: 0;
  }

  h4 {
    margin: 0 0 8px 0;
    color: #00ff00;
    font-size: 14px;
    border-bottom: 1px solid rgba(0, 255, 0, 0.3);
    padding-bottom: 4px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .stat-item {
    display: flex;
    justify-content: space-between;
    gap: 8px;
  }

  .stat-label {
    color: #888;
  }

  .stat-value {
    color: #00ff00;
    font-weight: bold;
  }

  .stat-value.good {
    color: #00ff00;
    text-shadow: 0 0 4px rgba(0, 255, 0, 0.5);
  }

  .actions {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(0, 255, 0, 0.3);
  }

  .btn-clear {
    width: 100%;
    padding: 6px 12px;
    background: rgba(255, 0, 0, 0.2);
    border: 1px solid rgba(255, 0, 0, 0.5);
    color: #ff6666;
    cursor: pointer;
    font-family: inherit;
    font-size: inherit;
    border-radius: 4px;
  }

  .btn-clear:hover {
    background: rgba(255, 0, 0, 0.3);
  }
</style>
