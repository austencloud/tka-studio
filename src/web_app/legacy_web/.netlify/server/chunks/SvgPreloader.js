var PropType = /* @__PURE__ */ ((PropType2) => {
  PropType2["HAND"] = "hand";
  PropType2["STAFF"] = "staff";
  PropType2["TRIAD"] = "triad";
  PropType2["MINIHOOP"] = "minihoop";
  PropType2["FAN"] = "fan";
  PropType2["CLUB"] = "club";
  PropType2["BUUGENG"] = "buugeng";
  return PropType2;
})(PropType || {});
const svgCache = {};
class SvgPreloader {
  svgManager = null;
  constructor() {
  }
  // Lazy-load SvgManager when needed
  async getSvgManager() {
    if (!this.svgManager) {
      if (typeof window !== "undefined") {
        const { default: SvgManager } = await import("./SvgManager.js");
        this.svgManager = new SvgManager();
      }
    }
    return this.svgManager;
  }
  /**
   * Generate a cache key for SVG content
   */
  getCacheKey(type, ...args) {
    return `${type}:${args.join(":")}`;
  }
  /**
   * Check if an SVG is already cached
   */
  isCached(key) {
    return !!svgCache[key];
  }
  /**
   * Get SVG from cache or fetch and cache it
   */
  async getOrFetchSvg(key, fetchFn) {
    if (this.isCached(key)) {
      return svgCache[key];
    }
    try {
      const svgContent = await fetchFn();
      svgCache[key] = svgContent;
      return svgContent;
    } catch (error) {
      console.error(`Failed to fetch SVG for key ${key}:`, error);
      throw error;
    }
  }
  /**
   * Preload a prop SVG
   */
  async preloadPropSvg(propType, color) {
    const key = this.getCacheKey("prop", propType, color);
    const manager = await this.getSvgManager();
    if (!manager) {
      throw new Error("SVG Manager could not be initialized (SSR context)");
    }
    return this.getOrFetchSvg(key, () => manager.getPropSvg(propType, color));
  }
  /**
   * Preload an arrow SVG
   */
  async preloadArrowSvg(motionType, startOri, turns, color) {
    const key = this.getCacheKey("arrow", motionType, startOri, String(turns), color);
    const manager = await this.getSvgManager();
    if (!manager) {
      throw new Error("SVG Manager could not be initialized (SSR context)");
    }
    return this.getOrFetchSvg(key, () => manager.getArrowSvg(motionType, startOri, turns, color));
  }
  /**
   * Bulk preload SVGs for common props
   */
  async preloadCommonProps() {
    const propTypes = [PropType.STAFF, PropType.CLUB, PropType.HAND];
    const colors = ["red", "blue"];
    try {
      const promises = propTypes.flatMap(
        (propType) => colors.map((color) => this.preloadPropSvg(propType, color))
      );
      await Promise.all(promises);
    } catch (error) {
      console.warn("Prop preloading skipped (possibly SSR context):", error);
    }
  }
  /**
   * Bulk preload SVGs for common arrows
   */
  async preloadCommonArrows() {
    const commonCombinations = [
      // Pro motions with common turns
      { motionType: "pro", startOri: "in", turns: 0 },
      { motionType: "pro", startOri: "out", turns: 0 },
      { motionType: "pro", startOri: "in", turns: 1 },
      // Anti motions with common turns
      { motionType: "anti", startOri: "in", turns: 0 },
      { motionType: "anti", startOri: "out", turns: 0 },
      // Static and dash
      { motionType: "static", startOri: "in", turns: 0 },
      { motionType: "dash", startOri: "in", turns: 0 }
    ];
    const colors = ["red", "blue"];
    try {
      const promises = commonCombinations.flatMap(
        (combo) => colors.map(
          (color) => this.preloadArrowSvg(combo.motionType, combo.startOri, combo.turns, color)
        )
      );
      await Promise.all(promises);
      "✅ Common arrow SVGs preloaded";
    } catch (error) {
      console.warn("Arrow preloading skipped (possibly SSR context):", error);
    }
  }
  /**
   * Preload all common SVGs
   */
  async preloadCommonSvgs() {
    try {
      await Promise.all([this.preloadCommonProps(), this.preloadCommonArrows()]);
    } catch (error) {
      console.warn("SVG preloading skipped (possibly SSR context)", error);
    }
  }
  /**
   * Get SVG cache stats
   */
  getCacheStats() {
    const cacheKeys = Object.keys(svgCache);
    return {
      total: cacheKeys.length,
      props: cacheKeys.filter((key) => key.startsWith("prop:")).length,
      arrows: cacheKeys.filter((key) => key.startsWith("arrow:")).length
    };
  }
}
const svgPreloader = new SvgPreloader();
async function initSvgPreloading() {
  if (typeof window === "undefined") {
    return;
  }
  try {
    await svgPreloader.preloadCommonSvgs();
  } catch (error) {
    console.error("SVG preloading failed:", error);
  }
}
const SvgPreloader$1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  initSvgPreloading,
  svgPreloader
}, Symbol.toStringTag, { value: "Module" }));
export {
  PropType as P,
  SvgPreloader$1 as S
};
