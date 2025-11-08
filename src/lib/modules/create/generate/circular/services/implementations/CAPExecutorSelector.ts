import { inject, injectable } from "inversify";
import { TYPES } from "$shared/inversify/types";
import { CAPType } from "../../domain/models/circular-models";
import type { ICAPExecutor } from "../contracts/ICAPExecutor";
import type { ICAPExecutorSelector } from "../contracts/ICAPExecutorSelector";

/**
 * Service for selecting the appropriate CAP executor based on CAP type
 *
 * Provides dependency injection-based executor selection, resolving
 * the correct executor instance from the inversify container based
 * on the requested CAP type.
 */
@injectable()
export class CAPExecutorSelector implements ICAPExecutorSelector {
  constructor(
    @inject(TYPES.IStrictRotatedCAPExecutor)
    private readonly strictRotatedExecutor: ICAPExecutor,

    @inject(TYPES.IStrictMirroredCAPExecutor)
    private readonly strictMirroredExecutor: ICAPExecutor,

    @inject(TYPES.IStrictSwappedCAPExecutor)
    private readonly strictSwappedExecutor: ICAPExecutor,

    @inject(TYPES.IStrictComplementaryCAPExecutor)
    private readonly strictComplementaryExecutor: ICAPExecutor,

    @inject(TYPES.IMirroredSwappedCAPExecutor)
    private readonly mirroredSwappedExecutor: ICAPExecutor,

    @inject(TYPES.ISwappedComplementaryCAPExecutor)
    private readonly swappedComplementaryExecutor: ICAPExecutor,

    @inject(TYPES.IMirroredComplementaryCAPExecutor)
    private readonly mirroredComplementaryExecutor: ICAPExecutor,

    @inject(TYPES.IRotatedSwappedCAPExecutor)
    private readonly rotatedSwappedExecutor: ICAPExecutor,

    @inject(TYPES.IRotatedComplementaryCAPExecutor)
    private readonly rotatedComplementaryExecutor: ICAPExecutor
  ) {}

  /**
   * Get the appropriate CAP executor for the given CAP type
   */
  getExecutor(capType: CAPType): ICAPExecutor {
    switch (capType) {
      case CAPType.STRICT_ROTATED:
        return this.strictRotatedExecutor;

      case CAPType.STRICT_MIRRORED:
        return this.strictMirroredExecutor;

      case CAPType.STRICT_SWAPPED:
        return this.strictSwappedExecutor;

      case CAPType.STRICT_COMPLEMENTARY:
        return this.strictComplementaryExecutor;

      case CAPType.MIRRORED_SWAPPED:
        return this.mirroredSwappedExecutor;

      case CAPType.SWAPPED_COMPLEMENTARY:
        return this.swappedComplementaryExecutor;

      case CAPType.MIRRORED_COMPLEMENTARY:
        return this.mirroredComplementaryExecutor;

      case CAPType.ROTATED_SWAPPED:
        return this.rotatedSwappedExecutor;

      case CAPType.ROTATED_COMPLEMENTARY:
        return this.rotatedComplementaryExecutor;

      default:
        throw new Error(
          `CAP type "${capType}" is not yet implemented. ` +
            `Currently supported: STRICT_ROTATED, STRICT_MIRRORED, STRICT_SWAPPED, ` +
            `STRICT_COMPLEMENTARY, MIRRORED_SWAPPED, SWAPPED_COMPLEMENTARY, MIRRORED_COMPLEMENTARY, ` +
            `ROTATED_SWAPPED, ROTATED_COMPLEMENTARY`
        );
    }
  }

  /**
   * Check if a CAP type is supported
   */
  isSupported(capType: CAPType): boolean {
    return [
      CAPType.STRICT_ROTATED,
      CAPType.STRICT_MIRRORED,
      CAPType.STRICT_SWAPPED,
      CAPType.STRICT_COMPLEMENTARY,
      CAPType.MIRRORED_SWAPPED,
      CAPType.SWAPPED_COMPLEMENTARY,
      CAPType.MIRRORED_COMPLEMENTARY,
      CAPType.ROTATED_SWAPPED,
      CAPType.ROTATED_COMPLEMENTARY,
    ].includes(capType);
  }
}
