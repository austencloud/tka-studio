// src/lib/components/SvgManager/SvgManager.ts
import {
	PropType,
	type Color,
	type MotionType,
	type Orientation,
	type TKATurns
} from '$lib/types/Types';

/**
 * Enhanced SvgManager that doesn't depend on svgPreloader
 */
export default class SvgManager {
	/**
	 * Cache for SVG content by key to avoid duplicate network requests
	 */
	private static readonly cache: Map<string, string> = new Map();

	/**
	 * Get a unique key for caching SVG content
	 */
	private getCacheKey(parts: string[]): string {
		return parts.join(':');
	}

	/**
	 * Fetch SVG content with error handling and timeout
	 */
	private async fetchSvg(path: string): Promise<string> {
		try {
			if (typeof window === 'undefined') {
				throw new Error('Cannot fetch SVG in SSR context');
			}

			// Use AbortController for timeout control
			const controller = new AbortController();
			const timeoutId = setTimeout(() => controller.abort(), 2000);

			const response = await fetch(path, {
				signal: controller.signal,
				// Add cache control headers
				headers: {
					'Cache-Control': 'max-age=3600'
				}
			});

			clearTimeout(timeoutId);

			if (!response.ok) {
				throw new Error(`Failed to fetch SVG: ${path} (${response.status})`);
			}

			return response.text();
		} catch (error) {
			// Minimal logging in production
			if (import.meta.env.DEV) {
				console.error(`SVG fetch error for ${path}:`, error);
			} else {
				console.error(`SVG fetch error for ${path}`);
			}
			throw error;
		}
	}

	/**
	 * Apply color transformation to SVG content
	 */
	public applyColor(svgData: string, color: Color): string {
		const hexColor = color === 'red' ? '#ED1C24' : '#2E3192';
		return svgData.replace(
			/\.st0{([^}]*fill:#)[0-9A-Fa-f]{6}([^}]*)}/g,
			`.st0{$1${hexColor.slice(1)}$2}`
		);
	}

	/**
	 * Get prop SVG directly from source
	 */
	public async getPropSvg(propType: PropType, color: Color): Promise<string> {
		const cacheKey = this.getCacheKey(['prop', propType, color]);

		// Check local cache first
		if (SvgManager.cache.has(cacheKey)) {
			return SvgManager.cache.get(cacheKey)!;
		}

		try {
			// Fallback to direct fetch
			const path = `/images/props/${propType}.svg`;
			const baseSvg = await this.fetchSvg(path);
			const coloredSvg = propType === PropType.HAND ? baseSvg : this.applyColor(baseSvg, color);

			// Cache for future use
			SvgManager.cache.set(cacheKey, coloredSvg);
			return coloredSvg;
		} catch (error) {
			console.error('Error fetching prop SVG:', error);
			return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="10" y="50" fill="red">Error</text></svg>`;
		}
	}

	/**
	 * Get arrow SVG directly from source
	 */
	public async getArrowSvg(
		motionType: MotionType,
		startOri: Orientation,
		turns: TKATurns,
		color: Color
	): Promise<string> {
		const cacheKey = this.getCacheKey(['arrow', motionType, startOri, String(turns), color]);

		// Check local cache first
		if (SvgManager.cache.has(cacheKey)) {
			return SvgManager.cache.get(cacheKey)!;
		}

		try {
			// Fallback to direct fetch
			const basePath = '/images/arrows';
			const typePath = motionType.toLowerCase();
			const radialPath = startOri === 'out' || startOri === 'in' ? 'from_radial' : 'from_nonradial';
			const fixedTurns = (typeof turns === 'number' ? turns : parseFloat(turns.toString())).toFixed(
				1
			);
			const svgPath = `${basePath}/${typePath}/${radialPath}/${motionType}_${fixedTurns}.svg`;

			const svgData = await this.fetchSvg(svgPath);
			const coloredSvg = this.applyColor(svgData, color);

			// Cache for future use
			SvgManager.cache.set(cacheKey, coloredSvg);
			return coloredSvg;
		} catch (error) {
			console.error('Error fetching arrow SVG:', error);
			return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text x="10" y="50" fill="red">Error</text></svg>`;
		}
	}

	/**
	 * Clear the SVG cache (useful for testing or when memory needs to be reclaimed)
	 */
	public static clearCache(): void {
		SvgManager.cache.clear();
	}

	/**
	 * Get stats about the cache
	 */
	public static getCacheStats(): { size: number } {
		return {
			size: SvgManager.cache.size
		};
	}

	/**
	 * Preload multiple arrow SVGs in parallel for better performance
	 */
	public async preloadArrowSvgs(
		arrowConfigs: Array<{
			motionType: MotionType;
			startOri: Orientation;
			turns: TKATurns;
			color: Color;
		}>
	): Promise<void> {
		// Create an array of promises for all SVGs
		const fetchPromises = arrowConfigs.map((config) => {
			const { motionType, startOri, turns, color } = config;
			const cacheKey = this.getCacheKey(['arrow', motionType, startOri, String(turns), color]);

			// Skip if already cached
			if (SvgManager.cache.has(cacheKey)) {
				return Promise.resolve();
			}

			// Create the path
			const basePath = '/images/arrows';
			const typePath = motionType.toLowerCase();
			const radialPath = startOri === 'out' || startOri === 'in' ? 'from_radial' : 'from_nonradial';
			const fixedTurns = (typeof turns === 'number' ? turns : parseFloat(turns.toString())).toFixed(
				1
			);
			const svgPath = `${basePath}/${typePath}/${radialPath}/${motionType}_${fixedTurns}.svg`;

			// Return a promise that won't reject (to avoid stopping other fetches)
			return this.fetchSvg(svgPath)
				.then((svgData) => {
					const coloredSvg = this.applyColor(svgData, color);
					SvgManager.cache.set(cacheKey, coloredSvg);
				})
				.catch((error) => {
					// Minimal logging in production
					if (import.meta.env.DEV) {
						console.warn(`Preload failed for ${svgPath}:`, error);
					}
				});
		});

		// Wait for all fetches to complete (or fail)
		await Promise.allSettled(fetchPromises);
	}
}
