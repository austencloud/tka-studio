// src/lib/utils/SvgPreloader.ts
import type { Color, MotionType, Orientation, TKATurns } from '$lib/types/Types';
import { PropType } from '$lib/types/Types';

// Cache for SVG content
const svgCache: Record<string, string> = {};

export default class SvgPreloader {
	private svgManager: any = null;

	constructor() {
		// Defer creation of SvgManager until needed
		// This breaks the circular dependency
	}

	// Lazy-load SvgManager when needed
	private async getSvgManager() {
		if (!this.svgManager) {
			// Only import when needed, not during module initialization
			// This avoids the circular dependency at module load time
			if (typeof window !== 'undefined') {
				// Only attempt to load in browser context
				const { default: SvgManager } = await import('../components/SvgManager/SvgManager');
				this.svgManager = new SvgManager();
			}
		}
		return this.svgManager;
	}

	/**
	 * Generate a cache key for SVG content
	 */
	private getCacheKey(type: 'prop' | 'arrow', ...args: string[]): string {
		return `${type}:${args.join(':')}`;
	}

	/**
	 * Check if an SVG is already cached
	 */
	private isCached(key: string): boolean {
		return !!svgCache[key];
	}

	/**
	 * Get SVG from cache or fetch and cache it
	 */
	private async getOrFetchSvg(key: string, fetchFn: () => Promise<string>): Promise<string> {
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
	async preloadPropSvg(propType: PropType, color: Color): Promise<string> {
		const key = this.getCacheKey('prop', propType, color);
		const manager = await this.getSvgManager();
		if (!manager) {
			throw new Error('SVG Manager could not be initialized (SSR context)');
		}
		return this.getOrFetchSvg(key, () => manager.getPropSvg(propType, color));
	}

	/**
	 * Preload an arrow SVG
	 */
	async preloadArrowSvg(
		motionType: MotionType,
		startOri: Orientation,
		turns: TKATurns,
		color: Color
	): Promise<string> {
		const key = this.getCacheKey('arrow', motionType, startOri, String(turns), color);
		const manager = await this.getSvgManager();
		if (!manager) {
			throw new Error('SVG Manager could not be initialized (SSR context)');
		}
		return this.getOrFetchSvg(key, () => manager.getArrowSvg(motionType, startOri, turns, color));
	}

	/**
	 * Bulk preload SVGs for common props
	 */
	async preloadCommonProps(): Promise<void> {
		const propTypes: PropType[] = [PropType.STAFF, PropType.CLUB, PropType.HAND];
		const colors: Color[] = ['red', 'blue'];

		try {
			const promises = propTypes.flatMap((propType) =>
				colors.map((color) => this.preloadPropSvg(propType, color))
			);

			await Promise.all(promises);
		} catch (error) {
			console.warn('Prop preloading skipped (possibly SSR context):', error);
		}
	}

	/**
	 * Bulk preload SVGs for common arrows
	 */
	async preloadCommonArrows(): Promise<void> {
		// Common combinations for arrows
		const commonCombinations = [
			// Pro motions with common turns
			{ motionType: 'pro' as MotionType, startOri: 'in' as Orientation, turns: 0 as TKATurns },
			{ motionType: 'pro' as MotionType, startOri: 'out' as Orientation, turns: 0 as TKATurns },
			{ motionType: 'pro' as MotionType, startOri: 'in' as Orientation, turns: 1 as TKATurns },
			// Anti motions with common turns
			{ motionType: 'anti' as MotionType, startOri: 'in' as Orientation, turns: 0 as TKATurns },
			{ motionType: 'anti' as MotionType, startOri: 'out' as Orientation, turns: 0 as TKATurns },
			// Static and dash
			{ motionType: 'static' as MotionType, startOri: 'in' as Orientation, turns: 0 as TKATurns },
			{ motionType: 'dash' as MotionType, startOri: 'in' as Orientation, turns: 0 as TKATurns }
		];

		const colors: Color[] = ['red', 'blue'];

		try {
			const promises = commonCombinations.flatMap((combo) =>
				colors.map((color) =>
					this.preloadArrowSvg(combo.motionType, combo.startOri, combo.turns, color)
				)
			);

			await Promise.all(promises);
			('✅ Common arrow SVGs preloaded');
		} catch (error) {
			console.warn('Arrow preloading skipped (possibly SSR context):', error);
		}
	}

	/**
	 * Preload all common SVGs
	 */
	async preloadCommonSvgs(): Promise<void> {
		try {
			await Promise.all([this.preloadCommonProps(), this.preloadCommonArrows()]);

		} catch (error) {
			console.warn('SVG preloading skipped (possibly SSR context)', error);
		}
	}

	/**
	 * Get SVG cache stats
	 */
	getCacheStats(): { total: number; props: number; arrows: number } {
		const cacheKeys = Object.keys(svgCache);
		return {
			total: cacheKeys.length,
			props: cacheKeys.filter((key) => key.startsWith('prop:')).length,
			arrows: cacheKeys.filter((key) => key.startsWith('arrow:')).length
		};
	}
}

// Create singleton instance
export const svgPreloader = new SvgPreloader();

// Function to initialize preloading at app startup
export async function initSvgPreloading(): Promise<void> {
	// Skip preloading in SSR context
	if (typeof window === 'undefined') {
		return;
	}

	try {
		await svgPreloader.preloadCommonSvgs();
	} catch (error) {
		console.error('SVG preloading failed:', error);
	}
}
