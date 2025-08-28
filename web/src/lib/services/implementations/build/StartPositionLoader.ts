/**
 * StartPositionLoader.ts - Data loading utilities for start positions
 */

import type { PictographData } from "$domain/PictographData";
import type { IStartPositionService } from "$services/interfaces/application-interfaces";
import { GridMode } from "$domain/enums";

/**
 * Handles loading and caching of start position data
 */
export class StartPositionLoader {
  private cache = new Map<string, PictographData[]>();
  private loadingPromises = new Map<string, Promise<PictographData[]>>();

  constructor(private startPositionService: IStartPositionService | null) {}

  /**
   * Load start positions for a specific grid mode
   */
  async loadStartPositions(gridMode: GridMode): Promise<PictographData[]> {
    const cacheKey = `start-positions-${gridMode}`;

    // Return cached result if available
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      return cached || [];
    }

    // Return existing promise if already loading
    if (this.loadingPromises.has(cacheKey)) {
      const promise = this.loadingPromises.get(cacheKey);
      return promise || Promise.resolve([]);
    }

    // Create loading promise
    const loadingPromise = this.performLoad(gridMode, cacheKey);
    this.loadingPromises.set(cacheKey, loadingPromise);

    try {
      const result = await loadingPromise;
      this.cache.set(cacheKey, result);
      return result;
    } finally {
      this.loadingPromises.delete(cacheKey);
    }
  }

  /**
   * Perform the actual loading operation
   */
  private async performLoad(
    gridMode: GridMode,
    _cacheKey: string
  ): Promise<PictographData[]> {
    console.log(
      `🔄 StartPositionLoader: Loading start positions for ${gridMode} mode`
    );

    if (!this.startPositionService) {
      console.error(
        "❌ StartPositionLoader: No start position service available"
      );
      return [];
    }

    try {
      // Convert grid mode string to GridMode enum
      const gridModeEnum =
        gridMode === GridMode.DIAMOND ? GridMode.DIAMOND : GridMode.BOX;
      const positions =
        await this.startPositionService.getDefaultStartPositions(gridModeEnum);

      console.log(
        `✅ StartPositionLoader: Loaded ${positions.length} start positions for ${gridMode} mode`
      );

      return positions;
    } catch (error) {
      console.error(
        `❌ StartPositionLoader: Failed to load start positions for ${gridMode} mode:`,
        error
      );
      return [];
    }
  }

  /**
   * Preload start positions for all grid modes
   */
  async preloadAllStartPositions(): Promise<{
    diamond: PictographData[];
    box: PictographData[];
  }> {
    console.log("🔄 StartPositionLoader: Preloading all start positions");

    const [diamond, box] = await Promise.all([
      this.loadStartPositions(GridMode.DIAMOND),
      this.loadStartPositions(GridMode.BOX),
    ]);

    console.log("✅ StartPositionLoader: All start positions preloaded", {
      diamond: diamond.length,
      box: box.length,
    });

    return { diamond, box };
  }

  /**
   * Clear cache (useful for refreshing data or testing)
   */
  clearCache(): void {
    this.cache.clear();
    this.loadingPromises.clear();
    console.log("🗑️ StartPositionLoader: Cache cleared");
  }

  /**
   * Get cached positions without triggering a load
   */
  getCachedPositions(gridMode: GridMode): PictographData[] | null {
    const cacheKey = `start-positions-${gridMode}`;
    return this.cache.get(cacheKey) || null;
  }

  /**
   * Check if positions are currently loading
   */
  isLoading(gridMode: GridMode): boolean {
    const cacheKey = `start-positions-${gridMode}`;
    return this.loadingPromises.has(cacheKey);
  }

  /**
   * Get loading statistics
   */
  getLoadingStats(): {
    cacheSize: number;
    activeLoads: number;
    cachedModes: string[];
  } {
    return {
      cacheSize: this.cache.size,
      activeLoads: this.loadingPromises.size,
      cachedModes: Array.from(this.cache.keys()),
    };
  }
}

/**
 * Create a new start position loader
 */
export function createStartPositionLoader(
  startPositionService: IStartPositionService | null
): StartPositionLoader {
  return new StartPositionLoader(startPositionService);
}
