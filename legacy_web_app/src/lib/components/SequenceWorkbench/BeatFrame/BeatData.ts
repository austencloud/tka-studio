// src/lib/components/SequenceWorkbench/BeatFrame/BeatData.ts
import type { PictographData } from '$lib/types/PictographData.js';

/**
 * Represents a single beat in a sequence
 */
export interface BeatData {
	/** Unique identifier for the beat */
	id?: string;

	/** The beat's position in the sequence (0 for start position) */
	beatNumber: number;

	/** Whether this beat contains data */
	filled: boolean;

	/** The pictograph data for this beat */
	pictographData: PictographData;

	/** Optional duration in beats (default: 1) */
	duration?: number;

	/** Optional metadata about this beat */
	metadata?: {
		/** If this beat contains a blue reversal */
		blueReversal?: boolean;

		/** If this beat contains a red reversal */
		redReversal?: boolean;

		/** Any tags associated with this beat */
		tags?: string[];
	};
}

/**
 * Create a new beat with the specified data
 */
export function createBeat(
	beatNumber: number,
	pictographData: PictographData,
	options: {
		id?: string;
		filled?: boolean;
		duration?: number;
		blueReversal?: boolean;
		redReversal?: boolean;
		tags?: string[];
	} = {}
): BeatData {
	const {
		id = crypto.randomUUID(), // Generate a unique ID if not provided
		filled = !!pictographData,
		duration = 1,
		blueReversal = false,
		redReversal = false,
		tags = []
	} = options;

	// Only create metadata object if we have reversals or tags
	const hasMetadata = blueReversal || redReversal || tags.length > 0;
	const metadata = hasMetadata
		? {
				blueReversal,
				redReversal,
				tags: [...tags]
			}
		: undefined;

	return {
		id,
		beatNumber,
		filled,
		pictographData,
		duration,
		metadata
	};
}
