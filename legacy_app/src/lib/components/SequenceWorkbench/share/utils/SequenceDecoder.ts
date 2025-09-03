/**
 * Utilities for decoding sequences from compact formats
 */
import type { BeatData } from '$lib/state/stores/sequence/SequenceContainer';
import type { MotionData } from '$lib/components/objects/Motion/MotionData';
import type { MotionType, Loc, PropRotDir, TKATurns, Orientation } from '$lib/types/Types';
import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { decompressString } from '$lib/utils/lzstring';

/**
 * Decode a sequence from a compact string format
 * @param encoded The encoded sequence string
 * @returns Array of reconstructed beats
 */
export async function decodeSequenceCompact(encoded: string): Promise<BeatData[]> {
	if (!encoded) return [];
	let decompressed;
	try {
		decompressed = await decompressString(encoded);
	} catch (e) {
		logger.warn('String decompression failed, using original format', {
			error: e instanceof Error ? e : new Error(String(e))
		});
		decompressed = encoded;
	}

	// Split into parts
	const parts = decompressed.split('|');
	if (parts.length < 2) {
		throw new Error('Invalid sequence format: missing parts');
	}

	// Check version
	const version = parts[0];

	// Version 3 is our current format with start position
	if (version === '3') {
		// Parse start position
		const startPosData = decodeStartPosition(parts[1]);

		// Create start position beat
		const startPositionBeat = createStartPositionBeat(startPosData);

		// If there are no beats beyond the start position, return just the start position
		if (parts.length <= 2) {
			return [startPositionBeat];
		}

		// Parse beat data
		const beatData = parts.slice(2).map((beatStr, index) => {
			const [blueStr, redStr] = beatStr.split(':');

			// Decode the motions
			const blueMotion = decodeMotion(blueStr, 'blue', startPosData.blueOri);
			const redMotion = decodeMotion(redStr, 'red', startPosData.redOri);

			// Determine the positions from the motions or start position
			const startPos = index === 0 ? startPosData.position : inferPosition(blueMotion, redMotion);
			const endPos = inferEndPosition(blueMotion, redMotion);

			// Create the beat
			return createBeatFromMotions(blueMotion, redMotion, startPos, endPos, index + 1); // +1 to skip the start position
		});

		// Combine start position with beats
		return [startPositionBeat, ...beatData];
	}

	// Version 2 is our previous ultra-compact format (without start position)
	if (version === '2') {
		return parts.slice(1).map((beatStr, index) => {
			const [blueStr, redStr] = beatStr.split(':');

			// Decode the motions
			const blueMotion = decodeMotion(blueStr, 'blue', 'in');
			const redMotion = decodeMotion(redStr, 'red', 'in');

			// Determine the positions from the motions
			const startPos = inferPosition(blueMotion, redMotion);
			const endPos = inferEndPosition(blueMotion, redMotion);

			// Create the beat
			return createBeatFromMotions(blueMotion, redMotion, startPos, endPos, index);
		});
	}

	throw new Error(`Unknown sequence format version: ${version}`);
}

/**
 * Decode start position data
 * @param encoded The encoded start position string
 * @returns Decoded start position data
 */
export function decodeStartPosition(encoded: string): any {
	const parts = encoded.split(',');

	// Handle the basic 4-part format: BLUE_LOC,RED_LOC,BLUE_ORI,RED_ORI
	const startPosData: any = {
		bluePos: parts[0] || 's',
		redPos: parts[1] || 's',
		blueOri: decodeOrientation(parts[2] || 'i'),
		redOri: decodeOrientation(parts[3] || 'i')
	};

	// If we have a 5th part, it's the position name
	if (parts.length > 4) {
		startPosData.position = decodePosition(parts[4]);
	} else {
		// Infer position from blue/red locations
		startPosData.position = inferPositionFromLocations(startPosData.bluePos, startPosData.redPos);
	}

	return startPosData;
}

/**
 * Decode a single character to an orientation
 * @param encoded The encoded orientation character
 * @returns Full orientation string
 */
export function decodeOrientation(encoded: string): string {
	const oriMap: Record<string, string> = {
		i: 'in',
		o: 'out',
		c: 'clock',
		u: 'counter'
	};

	return oriMap[encoded] || 'in';
}

/**
 * Decode a position (e.g., "a5" -> "alpha5")
 * @param encoded The encoded position
 * @returns Full position string
 */
export function decodePosition(encoded: string): string {
	if (!encoded) return '';

	// Map first character to full greek letter
	const letterMap: Record<string, string> = {
		a: 'alpha',
		b: 'beta',
		g: 'gamma',
		d: 'delta',
		e: 'epsilon'
	};

	const letter = letterMap[encoded.charAt(0)] || encoded.charAt(0);
	const number = encoded.substring(1);

	return letter + number;
}

/**
 * Infer position name from blue and red locations
 * @param blueLoc Blue juggler location
 * @param redLoc Red juggler location
 * @returns Inferred position name
 */
export function inferPositionFromLocations(blueLoc: string, redLoc: string): string {
	// Simple mapping of common location pairs to position names
	const posMap: Record<string, string> = {
		'n-s': 'alpha1',
		's-n': 'alpha1',
		'e-w': 'alpha2',
		'w-e': 'alpha2',
		'ne-sw': 'alpha3',
		'sw-ne': 'alpha3',
		'nw-se': 'alpha4',
		'se-nw': 'alpha4'
	};

	const key = `${blueLoc}-${redLoc}`;
	return posMap[key] || 'alpha1'; // Default to alpha1 if unknown
}

/**
 * Decode a motion from a compact string
 * @param encoded The encoded motion string
 * @param color The color of the juggler ('blue' or 'red')
 * @param defaultOri Default orientation if not specified
 * @returns Decoded motion data
 */
export function decodeMotion(
	encoded: string,
	color: 'blue' | 'red',
	defaultOri: string
): MotionData | null {
	if (!encoded || encoded === 'x') return null;

	// Parse the parts: START_LOC-END_LOC-ROT_DIR-TURNS
	const parts = encoded.split('-');
	if (parts.length < 4) {
		throw new Error(`Invalid motion format: ${encoded}`);
	}

	const startLoc = parts[0] as Loc;
	const endLoc = parts[1] as Loc;
	const rotDir = parts[2] === 'cw' ? 'cw' : ('ccw' as PropRotDir);
	const turns = parts[3] as TKATurns;

	// Infer motion type from the other data
	const motionType = inferMotionType(startLoc, endLoc, rotDir) as MotionType;

	// Infer orientations based on common patterns
	const { startOri, endOri } = inferOrientations(startLoc, endLoc, motionType, defaultOri);

	// Create the motion object
	return {
		id: `motion-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
		color,
		motionType,
		startLoc,
		endLoc,
		startOri: startOri as Orientation,
		endOri: endOri as Orientation,
		propRotDir: rotDir,
		turns,
		// Default values for other fields
		handRotDir: rotDir === 'cw' ? 'cw_shift' : 'ccw_shift',
		leadState: 'leading',
		prefloatMotionType: null,
		prefloatPropRotDir: null
	};
}

/**
 * Infer motion type based on start/end locations and rotation direction
 * @param startLoc Start location
 * @param endLoc End location
 * @param rotDir Rotation direction (unused in current implementation but kept for API compatibility)
 * @returns Inferred motion type
 */
export function inferMotionType(startLoc: string, endLoc: string, rotDir: string): string {
	// If start and end are the same, it's a static
	if (startLoc === endLoc) {
		return 'static';
	}

	// Otherwise, default to throw
	return 'throw';
}

/**
 * Infer orientations based on motion type and locations
 * @param startLoc Start location (unused in current implementation but kept for API compatibility)
 * @param endLoc End location (unused in current implementation but kept for API compatibility)
 * @param motionType Motion type
 * @param defaultOri Default orientation
 * @returns Start and end orientations
 */
export function inferOrientations(
	startLoc: string,
	endLoc: string,
	motionType: string,
	defaultOri: string
): { startOri: string; endOri: string } {
	// For static motions, orientations are the same
	if (motionType === 'static') {
		return { startOri: defaultOri, endOri: defaultOri };
	}

	// For throws, use common patterns
	// This is a simplified version - in a real app, this would be more complex
	return { startOri: defaultOri, endOri: defaultOri };
}

/**
 * Infer position from blue and red motions
 * @param blueMotion Blue juggler motion
 * @param redMotion Red juggler motion
 * @returns Inferred position name
 */
export function inferPosition(blueMotion: MotionData | null, redMotion: MotionData | null): string {
	if (!blueMotion || !redMotion) return 'alpha1';

	// Use start locations to infer position
	return inferPositionFromLocations(blueMotion.startLoc, redMotion.startLoc);
}

/**
 * Infer end position from blue and red motions
 * @param blueMotion Blue juggler motion
 * @param redMotion Red juggler motion
 * @returns Inferred end position name
 */
export function inferEndPosition(
	blueMotion: MotionData | null,
	redMotion: MotionData | null
): string {
	if (!blueMotion || !redMotion) return 'alpha1';

	// Use end locations to infer position
	return inferPositionFromLocations(blueMotion.endLoc, redMotion.endLoc);
}

/**
 * Create a start position beat from start position data
 * @param startPosData Start position data
 * @returns Start position beat
 */
export function createStartPositionBeat(startPosData: any): BeatData {
	// Create motion data for blue and red
	const blueMotionData: Partial<MotionData> = {
		id: `motion-start-blue-${Date.now()}`,
		color: 'blue',
		motionType: 'static',
		startLoc: startPosData.bluePos,
		endLoc: startPosData.bluePos,
		startOri: startPosData.blueOri,
		endOri: startPosData.blueOri,
		propRotDir: 'cw',
		turns: 0,
		handRotDir: 'cw_shift',
		leadState: 'leading'
	};

	const redMotionData: Partial<MotionData> = {
		id: `motion-start-red-${Date.now()}`,
		color: 'red',
		motionType: 'static',
		startLoc: startPosData.redPos,
		endLoc: startPosData.redPos,
		startOri: startPosData.redOri,
		endOri: startPosData.redOri,
		propRotDir: 'cw',
		turns: 0,
		handRotDir: 'cw_shift',
		leadState: 'leading'
	};

	// Generate a unique ID for the beat
	const id = `beat-start-${Date.now()}`;

	return {
		id,
		number: 0, // Start position is always beat 0
		letter: '',
		position: startPosData.position,
		orientation: '',
		turnsTuple: '',
		redPropData: null,
		bluePropData: null,
		redArrowData: null,
		blueArrowData: null,
		redMotionData: redMotionData as MotionData,
		blueMotionData: blueMotionData as MotionData,
		metadata: {
			isStartPosition: true,
			startPos: startPosData.position,
			endPos: startPosData.position
		}
	};
}

/**
 * Create a beat from blue and red motions
 * @param blueMotion Blue juggler motion
 * @param redMotion Red juggler motion
 * @param startPos Start position
 * @param endPos End position
 * @param beatNumber Beat number
 * @returns Beat data
 */
export function createBeatFromMotions(
	blueMotion: MotionData | null,
	redMotion: MotionData | null,
	startPos: string,
	endPos: string,
	beatNumber: number
): BeatData {
	// Generate a unique ID for the beat
	const id = `beat-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;

	return {
		id,
		number: beatNumber,
		letter: String.fromCharCode(65 + (beatNumber % 26)), // A, B, C, ...
		position: startPos,
		orientation: '',
		turnsTuple: '',
		redPropData: null,
		bluePropData: null,
		redArrowData: null,
		blueArrowData: null,
		redMotionData: redMotion,
		blueMotionData: blueMotion,
		metadata: {
			isStartPosition: false,
			startPos,
			endPos
		}
	};
}
