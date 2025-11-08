/**
 * Rotation Direction Service Implementation
 *
 * Determines rotation directions for blue and red props.
 * Extracted from SequenceGenerationService for single responsibility.
 */
import { RotationDirection } from "$shared/pictograph/shared/domain/enums/pictograph-enums";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import { PropContinuity } from "../../../shared/domain/models/generate-models";
import type { IPictographFilterService } from "../../../shared/services/contracts";
import type {
  IRotationDirectionService,
  RotationDirections,
} from "../contracts/IRotationDirectionService";

@injectable()
export class RotationDirectionService implements IRotationDirectionService {
  constructor(
    @inject(TYPES.IPictographFilterService)
    private pictographFilterService: IPictographFilterService
  ) {}

  /**
   * Determine rotation directions based on prop continuity
   */
  determineRotationDirections(
    propContinuity?: PropContinuity
  ): RotationDirections {
    if (propContinuity === PropContinuity.CONTINUOUS) {
      return {
        blueRotationDirection: this.pictographFilterService.selectRandom([
          RotationDirection.CLOCKWISE,
          RotationDirection.COUNTER_CLOCKWISE,
        ]),
        redRotationDirection: this.pictographFilterService.selectRandom([
          RotationDirection.CLOCKWISE,
          RotationDirection.COUNTER_CLOCKWISE,
        ]),
      };
    }

    return { blueRotationDirection: "", redRotationDirection: "" };
  }
}
