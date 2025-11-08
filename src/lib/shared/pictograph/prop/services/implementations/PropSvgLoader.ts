/**
 * Prop SVG Loader Service - OPTIMIZED (2025 Best Practices)
 *
 * Fast, direct SVG loading for props with aggressive caching.
 *
 * Key optimizations:
 * - Multi-level caching (raw SVG + transformed SVG by color)
 * - Request deduplication (prevents duplicate concurrent fetches)
 * - Cached metadata parsing (viewBox, center)
 * - Performance monitoring (cache hit/miss tracking)
 */

import type { MotionData } from "../../../shared/domain/models/MotionData";
import type { PropPlacementData } from "../../domain/models/PropPlacementData";
import { injectable } from "inversify";
import type { PropRenderData } from "../../domain/models/PropRenderData";
import type { IPropSvgLoader } from "../contracts/IPropSvgLoader";
import { MotionColor } from "../../../shared/domain/enums/pictograph-enums";

@injectable()
export class PropSvgLoader implements IPropSvgLoader {
  // 🚀 OPTIMIZATION: Multi-level caching
  private rawSvgCache = new Map<string, string>(); // path -> raw SVG text
  private transformedSvgCache = new Map<string, PropRenderData>(); // path:color -> transformed data
  private loadingPromises = new Map<string, Promise<string>>(); // path -> loading promise (deduplication)
  private metadataCache = new Map<
    string,
    {
      viewBox: { width: number; height: number };
      center: { x: number; y: number };
    }
  >();

  // Performance monitoring
  private cacheHits = 0;
  private cacheMisses = 0;
  /**
   * Load prop SVG data with color transformation
   * 🚀 OPTIMIZED: Checks transformed cache first, then raw cache, then fetches
   */
  async loadPropSvg(
    propData: PropPlacementData,
    motionData: MotionData
  ): Promise<PropRenderData> {
    try {
      // Get prop type and color
      const propType = motionData.propType || "staff";
      const color = motionData.color || MotionColor.BLUE;

      // Create cache key including color for transformed prop cache
      const path = `/images/props/${propType}.svg`;
      const transformedCacheKey = `${path}:${color}`;

      // 🚀 OPTIMIZATION: Check transformed cache first (fastest path)
      if (this.transformedSvgCache.has(transformedCacheKey)) {
        this.cacheHits++;
        const cached = this.transformedSvgCache.get(transformedCacheKey)!;
        // Return with updated position/rotation (these are per-instance)
        return {
          ...cached,
          position: { x: propData.positionX, y: propData.positionY },
          rotation: propData.rotationAngle,
        };
      }

      this.cacheMisses++;

      // Fetch raw SVG (uses raw cache + deduplication)
      const originalSvgText = await this.fetchSvgContentCached(path);

      // Parse SVG for viewBox and center (uses metadata cache)
      const { viewBox, center } = this.parsePropSvgCached(
        originalSvgText,
        path
      );

      // Apply color transformation
      const coloredSvgText = this.applyColorToSvg(originalSvgText, color);

      // Extract SVG content
      const svgContent = this.extractSvgContent(coloredSvgText);

      const result: PropRenderData = {
        position: { x: propData.positionX, y: propData.positionY },
        rotation: propData.rotationAngle,
        svgData: {
          svgContent,
          viewBox,
          center,
        },
        loaded: true,
        error: null,
      };

      // 🚀 OPTIMIZATION: Cache transformed result
      this.transformedSvgCache.set(transformedCacheKey, result);

      return result;
    } catch (error) {
      console.error("❌ PropSvgLoader: Error loading prop SVG:", error);
      return {
        position: { x: 475, y: 475 },
        rotation: 0,
        svgData: null,
        loaded: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * 🚀 NEW: Fetch SVG content with caching and deduplication
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
   * Fetch SVG content from a given path - direct fetch
   */
  async fetchSvgContent(path: string): Promise<string> {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch SVG: ${response.status}`);
    }
    return await response.text();
  }

  /**
   * 🚀 NEW: Parse prop SVG with caching
   */
  private parsePropSvgCached(
    svgText: string,
    cacheKey: string
  ): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    // Check metadata cache
    if (this.metadataCache.has(cacheKey)) {
      return this.metadataCache.get(cacheKey)!;
    }

    // Parse and cache
    const result = this.parsePropSvg(svgText);
    this.metadataCache.set(cacheKey, result);
    return result;
  }

  /**
   * Parse prop SVG to extract viewBox and center
   */
  private parsePropSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  } {
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const svgElement = doc.querySelector("svg");

    if (!svgElement) {
      throw new Error("Invalid SVG: No SVG element found");
    }

    // Extract viewBox
    const viewBoxAttr = svgElement.getAttribute("viewBox");
    let width = 100,
      height = 100;

    if (viewBoxAttr) {
      const [, , w, h] = viewBoxAttr.split(" ").map(Number);
      width = w || 100;
      height = h || 100;
    }

    return {
      viewBox: { width, height },
      center: { x: width / 2, y: height / 2 },
    };
  }

  /**
   * Apply color transformation to SVG - sophisticated approach matching arrows
   * Simple and correct: props are blue by default, change to red when needed
   * Also makes CSS class names unique to prevent conflicts between different colored props
   */
  private applyColorToSvg(svgText: string, color: MotionColor): string {
    const colorMap: Record<MotionColor, string> = {
      [MotionColor.BLUE]: "#2E3192",
      [MotionColor.RED]: "#ED1C24",
    };

    const targetColor = colorMap[color] || colorMap[MotionColor.BLUE];

    // Replace fill colors in both attribute and CSS style formats
    let coloredSvg = svgText.replace(
      /fill="#[0-9A-Fa-f]{6}"/g,
      `fill="${targetColor}"`
    );
    coloredSvg = coloredSvg.replace(
      /fill:\s*#[0-9A-Fa-f]{6}/g,
      `fill:${targetColor}`
    );

    // Make CSS class names unique for each color to prevent conflicts
    // Replace .st0, .st1, etc. with .st0-blue, .st1-blue, etc.
    const colorSuffix = color.toLowerCase();
    coloredSvg = coloredSvg.replace(/\.st(\d+)/g, `.st$1-${colorSuffix}`);

    // Also update class references in elements
    coloredSvg = coloredSvg.replace(
      /class="st(\d+)"/g,
      `class="st$1-${colorSuffix}"`
    );

    // Remove the centerPoint circle entirely to prevent unwanted visual elements
    coloredSvg = coloredSvg.replace(
      /<circle[^>]*id="centerPoint"[^>]*\/?>/,
      ""
    );

    return coloredSvg;
  }

  /**
   * Extract SVG content (remove outer SVG wrapper)
   */
  private extractSvgContent(svgText: string): string {
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const svgElement = doc.querySelector("svg");

    if (!svgElement) {
      return svgText;
    }

    return svgElement.innerHTML;
  }

  /**
   * 🚀 NEW: Clear caches (useful for testing or memory management)
   */
  clearCache(): void {
    this.rawSvgCache.clear();
    this.transformedSvgCache.clear();
    this.loadingPromises.clear();
    this.metadataCache.clear();
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
      metadataCacheSize: this.metadataCache.size,
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
