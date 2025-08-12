/**
 * Default Placement Service
 *
 * Provides default arrow placement adjustments by loading data from JSON files.
 * Mirrors the exact functionality from desktop DefaultPlacementService.
 */

import { ArrowPlacementDataService } from '../../../implementations/ArrowPlacementDataService';
import type { GridMode, MotionType } from '../../../interfaces';

/**
 * Interface for Default Placement Service that mirrors Python implementation
 */
export interface IDefaultPlacementServiceJson {
	getDefaultAdjustment(
		placementKey: string,
		turns: number | string,
		motionType: MotionType,
		gridMode: GridMode
	): Promise<{ x: number; y: number }>;

	getAvailablePlacementKeys(motionType: MotionType, gridMode: GridMode): Promise<string[]>;

	isLoaded(): boolean;

	getPlacementData(
		motionType: MotionType,
		placementKey: string,
		gridMode: GridMode
	): Promise<{ [turns: string]: [number, number] }>;

	debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void>;
}

export class DefaultPlacementService implements IDefaultPlacementServiceJson {
	private placementDataService: ArrowPlacementDataService;

	constructor() {
		this.placementDataService = new ArrowPlacementDataService();
	}

	/**
	 * Get default adjustment for arrow placement using placement key and turns.
	 * This mirrors the Python get_default_adjustment() method.
	 *
	 * @param placementKey - The placement identifier
	 * @param turns - Number of turns or turn identifier
	 * @param motionType - Motion type (pro, anti, float, dash, static)
	 * @param gridMode - Grid mode (diamond, box)
	 * @returns Adjustment coordinates {x, y}
	 */
	async getDefaultAdjustment(
		placementKey: string,
		turns: number | string,
		motionType: MotionType,
		gridMode: GridMode
	): Promise<{ x: number; y: number }> {
		console.log(
			`DefaultPlacementService.getDefaultAdjustment() called with:`,
			`placement_key=${placementKey}, turns=${turns}, motion_type=${motionType}, grid_mode=${gridMode}`
		);

		try {
			// Ensure placement data is loaded
			await this._loadAllDefaultPlacements();

			// Get the adjustment from the data service
			const adjustment = await this.placementDataService.getDefaultAdjustment(
				motionType,
				placementKey,
				turns,
				gridMode
			);

			console.log(
				`Found default adjustment for ${placementKey} at ${turns} turns: [${adjustment.x}, ${adjustment.y}]`
			);

			return adjustment;
		} catch (error) {
			console.warn(
				`Failed to get default adjustment for ${placementKey} at ${turns} turns:`,
				error
			);
			return { x: 0, y: 0 };
		}
	}

	/**
	 * Get available placement keys for a given motion type and grid mode.
	 * This mirrors the Python get_available_placement_keys() method.
	 *
	 * @param motionType - Motion type (pro, anti, float, dash, static)
	 * @param gridMode - Grid mode (diamond, box)
	 * @returns Array of available placement key strings
	 */
	async getAvailablePlacementKeys(motionType: MotionType, gridMode: GridMode): Promise<string[]> {
		await this._loadAllDefaultPlacements();
		return this.placementDataService.getAvailablePlacementKeys(motionType, gridMode);
	}

	/**
	 * Check if placement data has been loaded.
	 * This mirrors the Python is_loaded() method.
	 *
	 * @returns true if data is loaded, false otherwise
	 */
	isLoaded(): boolean {
		return this.placementDataService.isLoaded();
	}

	/**
	 * Load all default placement data from JSON files.
	 * This mirrors the Python _load_all_default_placements() method.
	 *
	 * The Python version loads from:
	 * - /data/arrow_placement/{grid_mode}/default/{motion_type}_placements.json
	 *
	 * Our TypeScript version uses the same file structure and loading pattern.
	 */
	private async _loadAllDefaultPlacements(): Promise<void> {
		if (this.placementDataService.isLoaded()) {
			return;
		}

		console.log('DefaultPlacementService: Loading all default placements...');

		try {
			await this.placementDataService.loadPlacementData();
			console.log('✅ DefaultPlacementService: All placement data loaded successfully');
		} catch (error) {
			console.error('❌ DefaultPlacementService: Failed to load placement data:', error);
			throw new Error(
				`Default placement loading failed: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Get raw placement data for debugging purposes.
	 * This mirrors the Python get_placement_data() method.
	 *
	 * @param motionType - Motion type (pro, anti, float, dash, static)
	 * @param placementKey - The placement identifier
	 * @param gridMode - Grid mode (diamond, box)
	 * @returns Raw placement data mapping turns to [x, y] adjustments
	 */
	async getPlacementData(
		motionType: MotionType,
		placementKey: string,
		gridMode: GridMode
	): Promise<{ [turns: string]: [number, number] }> {
		await this._loadAllDefaultPlacements();
		return this.placementDataService.getPlacementData(motionType, placementKey, gridMode);
	}

	/**
	 * Debug method to log available placement keys.
	 * This mirrors the Python debug_available_keys() method.
	 *
	 * @param motionType - Motion type to debug
	 * @param gridMode - Grid mode to debug
	 */
	async debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void> {
		await this._loadAllDefaultPlacements();
		await this.placementDataService.debugAvailableKeys(motionType, gridMode);
	}
}
