import type { GridPosition } from "$shared";
import { TYPES } from "$shared";
import { inject, injectable } from "inversify";
import { CAPType, SliceSize } from "../../domain/models/circular-models";
import type { ICAPEndPositionSelector } from "../contracts/ICAPEndPositionSelector";
import type { IRotatedEndPositionSelector } from "../contracts/IRotatedEndPositionSelector";
import {
	VERTICAL_MIRROR_POSITION_MAP,
	SWAPPED_POSITION_MAP,
} from "../../domain/constants/strict-cap-position-maps";

/**
 * Service for determining required end positions for different CAP types
 *
 * Routes to the appropriate position calculation based on CAP type:
 * - Rotated: Uses rotation-based position maps (depends on slice size)
 * - Mirrored: Uses vertical mirror position map
 * - Swapped: Uses swap position map
 * - Complementary: Returns to start position (no transformation)
 */
@injectable()
export class CAPEndPositionSelector implements ICAPEndPositionSelector {
	constructor(
		@inject(TYPES.IRotatedEndPositionSelector)
		private readonly rotatedEndPositionSelector: IRotatedEndPositionSelector
	) {}

	/**
	 * Determine the required end position based on CAP type
	 */
	determineEndPosition(
		capType: CAPType,
		startPosition: GridPosition,
		sliceSize: SliceSize
	): GridPosition {
		switch (capType) {
			case CAPType.STRICT_ROTATED:
				// Rotated CAP uses rotation maps (halved or quartered)
				return this.rotatedEndPositionSelector.determineRotatedEndPosition(
					sliceSize,
					startPosition
				);

			case CAPType.STRICT_MIRRORED:
				// Mirrored CAP uses vertical mirror map
				const mirroredEnd = VERTICAL_MIRROR_POSITION_MAP[startPosition];
				if (!mirroredEnd) {
					throw new Error(`No mirrored position found for start position: ${startPosition}`);
				}
				return mirroredEnd;

			case CAPType.STRICT_SWAPPED:
				// Swapped CAP uses swap position map
				const swappedEnd = SWAPPED_POSITION_MAP[startPosition];
				if (!swappedEnd) {
					throw new Error(`No swapped position found for start position: ${startPosition}`);
				}
				return swappedEnd;

			case CAPType.STRICT_COMPLEMENTARY:
				// Complementary CAP returns to start position (same position)
				return startPosition;

			default:
				throw new Error(
					`CAP type "${capType}" is not yet supported. ` +
						`Currently only strict CAP types are supported.`
				);
		}
	}
}
