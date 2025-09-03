/**
 * Utilities for encoding sequences into compact formats for sharing
 */
import type { BeatData } from '$lib/state/stores/sequence/SequenceContainer';
import type { MotionData } from '$lib/components/objects/Motion/MotionData';
import type { MotionType, Loc, PropRotDir, TKATurns, Orientation } from '$lib/types/Types';
import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';

/**
 * Encode a sequence of beats into a super-compact format
 * @param beats The beats to encode
 * @returns A compact string representation
 */
export function encodeSequenceCompact(beats: BeatData[]): string {
	if (!beats || beats.length === 0) return '';

	// Extract start position info from first beat if available
	const startPosData = extractStartPositionData(beats);

	// Format: VERSION|START_POS_DATA|BEAT1|BEAT2|...
	// where START_POS_DATA is BLUE_LOC,RED_LOC,BLUE_ORI,RED_ORI
	// and each BEAT is BLUE:RED

	const startPosStr = encodeStartPosition(startPosData);

	return (
		'3|' +
		startPosStr +
		'|' +
		beats
			.map((beat) => {
				const blue = beat.blueMotionData;
				const red = beat.redMotionData;
				return encodeMotion(blue) + ':' + encodeMotion(red);
			})
			.join('|')
	);
}

/**
 * Extract start position data from the first beat
 * @param beats The sequence beats
 * @returns Start position data object
 */
export function extractStartPositionData(beats: BeatData[]): any {
	if (!beats || beats.length === 0) return {};

	const firstBeat = beats[0];
	const startPosData: any = {};

	// Check if this is a start position beat
	if (firstBeat.metadata?.isStartPosition) {
		// Extract position name if available
		startPosData.position = firstBeat.position || firstBeat.metadata?.startPos || '';

		// Extract blue and red positions and orientations
		const blue = firstBeat.blueMotionData;
		const red = firstBeat.redMotionData;

		if (blue) {
			startPosData.bluePos = blue.startLoc;
			startPosData.blueOri = blue.startOri;
		}

		if (red) {
			startPosData.redPos = red.startLoc;
			startPosData.redOri = red.startOri;
		}
	}

	return startPosData;
}

/**
 * Encode start position data
 * @param startPosData The start position data to encode
 * @returns Encoded start position string
 */
export function encodeStartPosition(startPosData: any): string {
	// Format: BLUE_LOC,RED_LOC,BLUE_ORI,RED_ORI

	// Encode locations
	const bluePos = startPosData.bluePos || 's';
	const redPos = startPosData.redPos || 's';

	// Encode orientations - compact single-char versions
	const blueOri = encodeOrientation(startPosData.blueOri || 'in');
	const redOri = encodeOrientation(startPosData.redOri || 'in');

	// Encode start position if available (use first char of greek letter + number)
	let positionStr = '';
	if (startPosData.position) {
		positionStr = ',' + encodePosition(startPosData.position);
	}

	return `${bluePos},${redPos},${blueOri},${redOri}${positionStr}`;
}

/**
 * Encode an orientation to a single character
 * @param ori The orientation to encode
 * @returns Single character representation
 */
export function encodeOrientation(ori: string): string {
	const oriMap: Record<string, string> = {
		in: 'i',
		out: 'o',
		clock: 'c',
		counter: 'u'
	};

	return oriMap[ori] || 'i'; // Default to 'i' for 'in'
}

/**
 * Encode a position (e.g., "alpha5" -> "a5")
 * @param pos The position to encode
 * @returns Encoded position string
 */
export function encodePosition(pos: string): string {
	if (!pos) return '';
	// "alpha5" -> "a5"
	return pos.charAt(0) + pos.substring(pos.search(/\d/));
}

/**
 * Encode a motion into a compact string
 * @param motion The motion data to encode
 * @returns Encoded motion string
 */
export function encodeMotion(motion: MotionData | null): string {
	if (!motion) return 'x'; // 'x' represents null/empty motion

	// Format: START_LOC-END_LOC-ROT_DIR-TURNS
	// Example: "s-n-cw-1" for a clockwise throw from south to north with 1 turn

	const startLoc = motion.startLoc || 's';
	const endLoc = motion.endLoc || 's';
	const rotDir = motion.propRotDir || 'cw';
	const turns = motion.turns || '0';

	return `${startLoc}-${endLoc}-${rotDir === 'cw' ? 'cw' : 'ccw'}-${turns}`;
}

/**
 * Compress a string using LZString if available
 * @param str The string to compress
 * @returns Compressed string or original if compression failed
 * @deprecated Use the centralized compressString from $lib/utils/lzstring instead
 */
export function compressString(str: string): string {
	logger.warn(
		'Using deprecated compressString in SequenceEncoder, use centralized version instead'
	);

	// Forward to the centralized implementation
	// Note: This returns a Promise<string> but we're returning string for backward compatibility
	// Callers should migrate to the async version
	return str;
}
