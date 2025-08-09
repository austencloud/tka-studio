// Quick SVG preloader for instant loading
export class QuickSvgPreloader {
  private static cache: Map<string, string> = new Map();
  private static isPreloading = false;

  /**
   * Preload critical SVGs immediately on app start
   */
  static async preloadCriticalSvgs(): Promise<void> {
    if (this.isPreloading || typeof window === 'undefined') return;
    this.isPreloading = true;

    // Generate all arrow SVG paths systematically
    const motionTypes = ['pro', 'anti', 'dash', 'static'];
    const orientations = ['from_radial', 'from_nonradial'];
    const turns = ['0.0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0'];

    const arrowSvgs = [];

    // Add special case arrows
    arrowSvgs.push('/images/arrows/float.svg', '/images/arrows/dash.svg', '/images/arrows/still.svg');

    // Generate all motion type combinations
    for (const motionType of motionTypes) {
      for (const orientation of orientations) {
        for (const turn of turns) {
          arrowSvgs.push(`/images/arrows/${motionType}/${orientation}/${motionType}_${turn}.svg`);
        }
      }
    }

    // All prop SVGs
    const propSvgs = [
      '/images/props/bigbuugeng.svg', '/images/props/bigfan.svg', '/images/props/bigtriad.svg',
      '/images/props/club.svg', '/images/props/fan.svg', '/images/props/hand.svg',
      '/images/props/staff.svg', '/images/props/triad.svg', '/images/props/bigdoublestar.svg',
      '/images/props/bighoop.svg', '/images/props/buugeng.svg', '/images/props/doublestar.svg',
      '/images/props/fractalgeng.svg', '/images/props/minihoop.svg', '/images/props/staff_v2.svg',
      '/images/props/ukulele.svg', '/images/props/bigeightrings.svg', '/images/props/bigstaff.svg',
      '/images/props/chicken.svg', '/images/props/eightrings.svg', '/images/props/guitar.svg',
      '/images/props/quiad.svg', '/images/props/sword.svg'
    ];

    // Other essential SVGs
    const otherSvgs = [
      '/images/arrow.svg',
      '/images/blank.svg',
      '/images/dash.svg',
      '/images/same_opp_dot.svg'
    ];

    const allSvgs = [...arrowSvgs, ...propSvgs, ...otherSvgs];

    // Load all SVGs in parallel with batching for performance
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
  static async getSvg(path: string): Promise<string> {
    // FIRST: Check the global preload cache (highest priority)
    if (typeof window !== 'undefined' && window.svgCache && window.svgCache.has(path)) {
      const cachedSvg = window.svgCache.get(path);
      if (cachedSvg) {
        console.log(`✅ Using global preload cache for: ${path}`);
        // Also store in our local cache for consistency
        this.cache.set(path, cachedSvg);
        return cachedSvg;
      }
    }

    // SECOND: Check our internal cache
    if (this.cache.has(path)) {
      console.log(`✅ Using QuickSvgPreloader cache for: ${path}`);
      return this.cache.get(path)!;
    }

    // LAST RESORT: Fetch immediately (should be rare with proper preloading)
    console.log(`⚠️ Cache miss, fetching: ${path}`);
    try {
      const response = await fetch(path, {
        headers: {
          'Cache-Control': 'max-age=31536000' // Aggressive browser caching
        }
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const svgContent = await response.text();

      // Store in both caches
      this.cache.set(path, svgContent);
      if (typeof window !== 'undefined') {
        if (!window.svgCache) window.svgCache = new Map();
        window.svgCache.set(path, svgContent);
      }

      return svgContent;
    } catch (error) {
      throw new Error(`Failed to load SVG from ${path}: ${error}`);
    }
  }

  /**
   * Clear cache (useful for development)
   */
  static clearCache(): void {
    this.cache.clear();
    this.isPreloading = false;
  }
}
