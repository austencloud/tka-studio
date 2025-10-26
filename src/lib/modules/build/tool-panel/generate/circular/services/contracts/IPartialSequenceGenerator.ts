/**
 * Partial Sequence Generator Interface
 *
 * Generates partial sequences for circular mode (CAP preparation).
 */
import type { BeatData } from "$shared";
import type { GenerationOptions } from "../../../shared/domain/models/generate-models";

export interface IPartialSequenceGenerator {
  /**
   * Generate a partial sequence ending at a specific position
   * Used for circular mode CAP generation
   * @param startPos - Start grid position
   * @param endPos - Required end grid position
   * @param sliceSize - Halved or quartered
   * @param options - Generation options
   * @returns Promise resolving to partial sequence (start position + intermediate beats + final beat)
   */
  generatePartialSequence(
    startPos: any,
    endPos: any,
    sliceSize: any,
    options: GenerationOptions
  ): Promise<BeatData[]>;
}
