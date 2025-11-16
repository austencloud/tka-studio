/**
 * SVG Loading Service - OPTIMIZED (2025 Best Practices)
 *
 * Handles fetching and loading SVG files with aggressive caching.
 *
 * Key optimizations:
 * - Multi-level caching (raw SVG + transformed SVG by color)
 * - Request deduplication (prevents duplicate concurrent fetches)
 * - Performance monitoring (cache hit/miss tracking)
 *
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type { IArrowPathResolver, IArrowSvgParser, ISvgColorTransformer } from "$shared";

import {  } from "$shared";
import type {
  ArrowPlacementData,
  ArrowSvgData,
  IArrowSvgLoader,
  MotionData,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class ArrowSvgLoader implements IArrowSvgLoader {
  // 🚀 OPTIMIZATION: Multi-level caching
  private rawSvgCache = new Map<string, string>(); // path -> raw SVG text
  private transformedSvgCache = new Map<string, ArrowSvgData>(); // path:color -> transformed data
  private loadingPromises = new Map<string, Promise<string>>(); // path -> loading promise (deduplication)

  // Performance monitoring
  private cacheHits = 0;
  private cacheMisses = 0;

  constructor(
    @inject(TYPES.IArrowPathResolver) private pathResolver: IArrowPathResolver,
    @inject(TYPES.IArrowSvgParser) private svgParser: IArrowSvgParser,
    @inject(TYPES.IArrowSvgColorTransformer)
    private colorTransformer: ISvgColorTransformer
  ) {}

  /**
   * Load arrow SVG data with color transformation based on placement data (extracted from Arrow.svelte)
   * 🚀 OPTIMIZED: Checks transformed cache first, then raw cache, then fetches
   */
  async loadArrowSvg(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<ArrowSvgData> {
    const path = this.pathResolver.getArrowPath(arrowData, motionData);

    if (!path) {
      console.error(
        "❌ ArrowSvgLoader: No arrow path available - missing motion data"
      );
      throw new Error("No arrow path available - missing motion data");
    }

    // Create cache key including color for transformed SVG cache
    const transformedCacheKey = `${path}:${motionData.color}`;

    // 🚀 OPTIMIZATION: Check transformed cache first (fastest path)
    if (this.transformedSvgCache.has(transformedCacheKey)) {
      this.cacheHits++;
      return this.transformedSvgCache.get(transformedCacheKey)!;
    }

    this.cacheMisses++;

    // Fetch raw SVG (uses raw cache + deduplication)
    const originalSvgText = await this.fetchSvgContentCached(path);

    const parsedSvg = this.svgParser.parseArrowSvg(originalSvgText);

    // Apply color transformation to the SVG
    const coloredSvgText = this.colorTransformer.applyColorToSvg(
      originalSvgText,
      motionData.color
    );

    // Extract just the inner SVG content (no scaling needed - arrows are already correctly sized)
    const svgContent = this.svgParser.extractSvgContent(coloredSvgText);

    const result: ArrowSvgData = {
      id: `arrow-${Date.now()}`,
      svgContent: svgContent,
      imageSrc: svgContent,
      viewBox: parsedSvg.viewBox || "100 100",
      center: parsedSvg.center ?? undefined,
      dimensions: {
        width: parsedSvg.width || 100,
        height: parsedSvg.height || 100,
        viewBox: parsedSvg.viewBox || "100 100",
        center: parsedSvg.center ?? undefined,
      },
    };

    // 🚀 OPTIMIZATION: Cache transformed result
    this.transformedSvgCache.set(transformedCacheKey, result);

    return result;
  }

  /**
   * 🚀 NEW: Fetch SVG content with caching and deduplication
   * This method checks the raw cache first, then deduplicates concurrent requests
   */
  private async fetchSvgContentCached(path: string): Promise<string> {
    // Check raw SVG cache
    if (this.rawSvgCache.has(path)) {
      return this.rawSvgCache.get(path)!;
    }

    // Check if already loading (prevents duplicate concurrent requests)
    if (this.loadingPromises.has(path)) {
      return this.loadingPromises.get(path)!;
    }

    // Create loading promise
    const loadingPromise = this.fetchSvgContent(path);
    this.loadingPromises.set(path, loadingPromise);

    try {
      const svgText = await loadingPromise;

      // Cache the raw SVG
      this.rawSvgCache.set(path, svgText);

      // Clean up loading promise
      this.loadingPromises.delete(path);

      return svgText;
    } catch (error) {
      // Clean up on error
      this.loadingPromises.delete(path);
      throw error;
    }
  }

  /**
   * Fetch SVG content from a given path
   * Note: Public for interface compliance, but internal code should use fetchSvgContentCached
   */
  async fetchSvgContent(path: string): Promise<string> {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch SVG: ${response.status}`);
    }
    return await response.text();
  }

  /**
   * 🚀 NEW: Clear caches (useful for testing or memory management)
   */
  clearCache(): void {
    this.rawSvgCache.clear();
    this.transformedSvgCache.clear();
    this.loadingPromises.clear();
    this.cacheHits = 0;
    this.cacheMisses = 0;
  }

  /**
   * 🚀 NEW: Get cache statistics for performance monitoring
   */
  getCacheStats() {
    return {
      rawCacheSize: this.rawSvgCache.size,
      transformedCacheSize: this.transformedSvgCache.size,
      cacheHits: this.cacheHits,
      cacheMisses: this.cacheMisses,
      hitRate:
        this.cacheHits + this.cacheMisses > 0
          ? (
              (this.cacheHits / (this.cacheHits + this.cacheMisses)) *
              100
            ).toFixed(2) + "%"
          : "0%",
    };
  }
}
