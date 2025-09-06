// src/lib/components/Pictograph/utils/dataComparison.ts
import type { PictographData } from '$lib/types/PictographData';
import type { MotionData } from '../../objects/Motion/MotionData';
import { logger } from '$lib/core/logging';

/**
 * Interface for storing a snapshot of pictograph data for comparison
 * Contains only the essential fields needed for change detection
 */
export interface PictographDataSnapshot {
	letter?: string;
	gridMode?: string;
	startPos?: string;
	endPos?: string;
	direction?: string;
	redMotionData: MotionDataSnapshot | null;
	blueMotionData: MotionDataSnapshot | null;
}

/**
 * Interface for storing a snapshot of motion data for comparison
 * Contains only the essential fields needed for change detection
 */
export interface MotionDataSnapshot {
	id?: string;
	startLoc?: string;
	endLoc?: string;
	startOri?: string;
	endOri?: string;
	motionType?: string;
}

/**
 * Creates a snapshot of the pictograph data for safe comparison
 * Extracts only the essential fields to avoid circular references
 *
 * @param data The pictograph data to create a snapshot from
 * @returns A snapshot object containing only the essential fields
 */
export function createDataSnapshot(data: PictographData): PictographDataSnapshot {
	return {
		letter: data.letter || undefined,
		gridMode: data.gridMode || undefined,
		startPos: data.startPos || undefined,
		endPos: data.endPos || undefined,
		direction: data.direction || undefined,
		redMotionData: data.redMotionData
			? {
					id: data.redMotionData.id,
					startLoc: data.redMotionData.startLoc,
					endLoc: data.redMotionData.endLoc,
					startOri: data.redMotionData.startOri,
					endOri: data.redMotionData.endOri,
					motionType: data.redMotionData.motionType
				}
			: null,
		blueMotionData: data.blueMotionData
			? {
					id: data.blueMotionData.id,
					startLoc: data.blueMotionData.startLoc,
					endLoc: data.blueMotionData.endLoc,
					startOri: data.blueMotionData.startOri,
					endOri: data.blueMotionData.endOri,
					motionType: data.blueMotionData.motionType
				}
			: null
	};
}

/**
 * Compares the current pictograph data with a previous snapshot
 * to determine if there have been any meaningful changes
 *
 * @param newData The current pictograph data
 * @param lastSnapshot The previous snapshot to compare against
 * @returns True if there are meaningful changes, false otherwise
 */
export function hasDataChanged(
	newData: PictographData,
	lastSnapshot: PictographDataSnapshot | null
): boolean {
	// If this is the first time, always return true
	if (!lastSnapshot) {
		return true;
	}

	try {
		// Compare important fields directly - add any fields that should trigger a rerender
		const fieldsChanged =
			lastSnapshot.letter !== newData.letter ||
			lastSnapshot.gridMode !== newData.gridMode ||
			lastSnapshot.startPos !== newData.startPos ||
			lastSnapshot.endPos !== newData.endPos ||
			lastSnapshot.direction !== newData.direction ||
			compareMotionData('red', lastSnapshot, newData) ||
			compareMotionData('blue', lastSnapshot, newData);

		return fieldsChanged;
	} catch (error) {
		logger.warn('Error comparing pictograph data:', {
			error: error instanceof Error ? error : new Error(String(error))
		});
		return true; // Assume changed on error to be safe
	}
}

/**
 * Helper function to compare motion data between a snapshot and current data
 *
 * @param color The color of the motion data to compare ('red' or 'blue')
 * @param lastSnapshot The previous snapshot to compare against
 * @param newData The current pictograph data
 * @returns True if there are meaningful changes, false otherwise
 */
function compareMotionData(
	color: 'red' | 'blue',
	lastSnapshot: PictographDataSnapshot,
	newData: PictographData
): boolean {
	const key = color === 'red' ? 'redMotionData' : 'blueMotionData';
	const oldMotion = lastSnapshot[key as keyof typeof lastSnapshot] as MotionDataSnapshot | null;
	const newMotion = newData[key as keyof typeof newData] as MotionData | null;

	// If both null/undefined or same reference, no change
	if (oldMotion === newMotion) return false;

	// If one exists and the other doesn't, changed
	if ((!oldMotion && newMotion) || (oldMotion && !newMotion)) return true;

	// Compare critical motion properties
	if (oldMotion && newMotion) {
		return (
			oldMotion.id !== newMotion.id ||
			oldMotion.startLoc !== newMotion.startLoc ||
			oldMotion.endLoc !== newMotion.endLoc ||
			oldMotion.startOri !== newMotion.startOri ||
			oldMotion.endOri !== newMotion.endOri ||
			oldMotion.motionType !== newMotion.motionType
		);
	}

	return false;
}

/**
 * Checks if the pictograph data has the required motion data
 *
 * @param data The pictograph data to check
 * @returns True if the data has red or blue motion data, false otherwise
 */
export function hasRequiredMotionData(data: PictographData): boolean {
	return Boolean(data?.redMotionData || data?.blueMotionData);
}
