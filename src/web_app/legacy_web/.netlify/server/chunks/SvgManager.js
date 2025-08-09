import { P as PropType } from "./SvgPreloader.js";
class QuickSvgPreloader {
  static cache = /* @__PURE__ */ new Map();
  static isPreloading = false;
  /**
   * Preload critical SVGs immediately on app start
   */
  static async preloadCriticalSvgs() {
    if (this.isPreloading || typeof window === "undefined") return;
    this.isPreloading = true;
    const motionTypes = ["pro", "anti", "dash", "static"];
    const orientations = ["from_radial", "from_nonradial"];
    const turns = ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"];
    const arrowSvgs = [];
    arrowSvgs.push("/images/arrows/float.svg", "/images/arrows/dash.svg", "/images/arrows/still.svg");
    for (const motionType of motionTypes) {
      for (const orientation of orientations) {
        for (const turn of turns) {
          arrowSvgs.push(`/images/arrows/${motionType}/${orientation}/${motionType}_${turn}.svg`);
        }
      }
    }
    const propSvgs = [
      "/images/props/bigbuugeng.svg",
      "/images/props/bigfan.svg",
      "/images/props/bigtriad.svg",
      "/images/props/club.svg",
      "/images/props/fan.svg",
      "/images/props/hand.svg",
      "/images/props/staff.svg",
      "/images/props/triad.svg",
      "/images/props/bigdoublestar.svg",
      "/images/props/bighoop.svg",
      "/images/props/buugeng.svg",
      "/images/props/doublestar.svg",
      "/images/props/fractalgeng.svg",
      "/images/props/minihoop.svg",
      "/images/props/staff_v2.svg",
      "/images/props/ukulele.svg",
      "/images/props/bigeightrings.svg",
      "/images/props/bigstaff.svg",
      "/images/props/chicken.svg",
      "/images/props/eightrings.svg",
      "/images/props/guitar.svg",
      "/images/props/quiad.svg",
      "/images/props/sword.svg"
    ];
    const otherSvgs = [
      "/images/arrow.svg",
      "/images/blank.svg",
      "/images/dash.svg",
      "/images/same_opp_dot.svg"
    ];
    const allSvgs = [...arrowSvgs, ...propSvgs, ...otherSvgs];
    const batchSize = 20;
    for (let i = 0; i < allSvgs.length; i += batchSize) {
      const batch = allSvgs.slice(i, i + batchSize);
      const batchPromises = batch.map(async (path) => {
        try {
          const response = await fetch(path);
          if (response.ok) {
            const svgContent = await response.text();
            this.cache.set(path, svgContent);
          }
        } catch (error) {
          console.warn(`⚠️ Error preloading: ${path}`, error);
        }
      });
      await Promise.all(batchPromises);
    }
    console.log(`🚀 Preloaded ${this.cache.size} SVGs for instant performance`);
  }
  /**
   * Get SVG from cache or fetch immediately
   */
  static async getSvg(path) {
    if (this.cache.has(path)) {
      return this.cache.get(path);
    }
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const svgContent = await response.text();
      this.cache.set(path, svgContent);
      return svgContent;
    } catch (error) {
      throw new Error(`Failed to load SVG from ${path}: ${error}`);
    }
  }
  /**
   * Clear cache (useful for development)
   */
  static clearCache() {
    this.cache.clear();
    this.isPreloading = false;
  }
}
class SvgManager {
  /**
   * Cache for SVG content by key to avoid duplicate network requests
   */
  static cache = /* @__PURE__ */ new Map();
  /**
   * Get a unique key for caching SVG content
   */
  getCacheKey(parts) {
    return parts.join(":");
  }
  /**
   * Fetch SVG content with optimized error handling
   */
  async fetchSvg(path) {
    try {
      if (typeof window === "undefined") {
        throw new Error("Cannot fetch SVG in SSR context");
      }
      return await QuickSvgPreloader.getSvg(path);
    } catch (error) {
      throw error;
    }
  }
  /**
   * Apply color transformation to SVG content
   * Uses comprehensive patterns matching legacy desktop implementation
   */
  applyColor(svgData, color) {
    const hexColor = color === "red" ? "#ED1C24" : "#2E3192";
    const classColorPattern = /(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)(#[a-fA-F0-9]{6})([^}]*?\})/g;
    const fillPattern = /(fill=")(#[a-fA-F0-9]{6})(")/g;
    const stylePattern = /(fill:\s*)(#[a-fA-F0-9]{6})(\s*;?)/g;
    let result = svgData;
    result = result.replace(classColorPattern, `$1${hexColor}$4`);
    result = result.replace(fillPattern, `$1${hexColor}$3`);
    result = result.replace(stylePattern, `$1${hexColor}$3`);
    return result;
  }
  /**
   * Get prop SVG directly from source
   */
  async getPropSvg(propType, color) {
    const cacheKey = this.getCacheKey(["prop", propType, color]);
    if (SvgManager.cache.has(cacheKey)) {
      return SvgManager.cache.get(cacheKey);
    }
    try {
      const path = `/images/props/${propType}.svg`;
      const baseSvg = await this.fetchSvg(path);
      const coloredSvg = propType === PropType.HAND ? baseSvg : this.applyColor(baseSvg, color);
      SvgManager.cache.set(cacheKey, coloredSvg);
      return coloredSvg;
    } catch (error) {
      console.error("Error fetching prop SVG:", error);
      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="10" y="50" fill="red">Error</text></svg>`;
    }
  }
  /**
   * Get arrow SVG directly from source
   */
  async getArrowSvg(motionType, startOri, turns, color) {
    const cacheKey = this.getCacheKey(["arrow", motionType, startOri, String(turns), color]);
    if (SvgManager.cache.has(cacheKey)) {
      return SvgManager.cache.get(cacheKey);
    }
    try {
      const basePath = "/images/arrows";
      const typePath = motionType.toLowerCase();
      const radialPath = startOri === "out" || startOri === "in" ? "from_radial" : "from_nonradial";
      const fixedTurns = (typeof turns === "number" ? turns : parseFloat(turns.toString())).toFixed(
        1
      );
      const svgPath = `${basePath}/${typePath}/${radialPath}/${motionType}_${fixedTurns}.svg`;
      const svgData = await this.fetchSvg(svgPath);
      const coloredSvg = this.applyColor(svgData, color);
      SvgManager.cache.set(cacheKey, coloredSvg);
      return coloredSvg;
    } catch (error) {
      console.error("Error fetching arrow SVG:", error);
      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="10" y="50" fill="red">Error</text></svg>`;
    }
  }
  /**
   * Clear the SVG cache (useful for testing or when memory needs to be reclaimed)
   */
  static clearCache() {
    SvgManager.cache.clear();
  }
  /**
   * Get stats about the cache
   */
  static getCacheStats() {
    return {
      size: SvgManager.cache.size
    };
  }
  /**
   * Preload multiple arrow SVGs in parallel for better performance
   */
  async preloadArrowSvgs(arrowConfigs) {
    const fetchPromises = arrowConfigs.map((config) => {
      const { motionType, startOri, turns, color } = config;
      const cacheKey = this.getCacheKey(["arrow", motionType, startOri, String(turns), color]);
      if (SvgManager.cache.has(cacheKey)) {
        return Promise.resolve();
      }
      const basePath = "/images/arrows";
      const typePath = motionType.toLowerCase();
      const radialPath = startOri === "out" || startOri === "in" ? "from_radial" : "from_nonradial";
      const fixedTurns = (typeof turns === "number" ? turns : parseFloat(turns.toString())).toFixed(
        1
      );
      const svgPath = `${basePath}/${typePath}/${radialPath}/${motionType}_${fixedTurns}.svg`;
      return this.fetchSvg(svgPath).then((svgData) => {
        const coloredSvg = this.applyColor(svgData, color);
        SvgManager.cache.set(cacheKey, coloredSvg);
      }).catch((error) => {
      });
    });
    await Promise.allSettled(fetchPromises);
  }
}
export {
  SvgManager as default
};
