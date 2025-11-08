/**
 * Turn Allocation Calculator Implementation
 *
 * Calculates turn distribution across beats.
 * Extracted from SequenceGenerationService for single responsibility.
 */
import { injectable } from "inversify";
import type {
  ITurnAllocator,
  TurnAllocation,
} from "../contracts/ITurnAllocator";

@injectable()
export class TurnAllocator implements ITurnAllocator {
  /**
   * Allocate turns for the sequence
   */
  async allocateTurns(
    beatsToGenerate: number,
    level: number,
    turnIntensity: number
  ): Promise<TurnAllocation> {
    const { TurnIntensityManagerService } = await import(
      "./TurnIntensityManagerService"
    );
    const turnManager = new TurnIntensityManagerService(
      beatsToGenerate,
      level,
      turnIntensity
    );
    return turnManager.allocateTurnsForBlueAndRed();
  }
}
