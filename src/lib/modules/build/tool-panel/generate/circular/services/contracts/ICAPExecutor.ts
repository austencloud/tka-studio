import type { BeatData } from "$build/workbench";
import type { SliceSize } from "../../domain/models/circular-models";

/**
 * Common interface for all CAP executors
 *
 * Provides a consistent contract for executing Circular Arrangement Patterns
 * regardless of the specific transformation type (rotated, mirrored, swapped, etc.)
 *
 * NOTE: Some executors only support halved mode (mirrored, swapped, complementary)
 * and will ignore the sliceSize parameter, but it must still be provided for interface consistency.
 */
export interface ICAPExecutor {
	/**
	 * Execute the CAP transformation on a partial sequence
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Whether to use halved (180°) or quartered (90°) transformation
	 *                    Note: Some executors only support halved and will ignore this parameter
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[];
}
