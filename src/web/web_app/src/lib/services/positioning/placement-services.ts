/**
 * Placement and adjustment service interfaces for arrow positioning.
 */

import type { GridMode, MotionData, PictographData } from '$lib/domain';
import type { MotionType, Point } from './types';

export interface ISpecialPlacementService {
	getSpecialAdjustment(
		motionData: MotionData,
		pictographData: PictographData,
		arrowColor?: string
	): Promise<Point | null>;
}

export interface IDefaultPlacementService {
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

export interface IArrowAdjustmentLookup {
	getBaseAdjustment(
		pictographData: PictographData,
		motionData: MotionData,
		letter: string,
		arrowColor?: string
	): Promise<Point>;
}
