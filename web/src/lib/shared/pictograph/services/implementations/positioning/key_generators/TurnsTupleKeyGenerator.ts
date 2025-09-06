import type { PictographData } from "$shared/domain";
import type { ITurnsTupleKeyGenerator } from "$shared/pictograph/services/contracts/positioning-interfaces";
import { injectable } from "inversify";

/**
 * TurnsTupleKeyGenerator
 * Generates turns tuple array matching advanced lookup expectations.
 */
@injectable()
export class TurnsTupleKeyGenerator implements ITurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData: PictographData): number[] {
    try {
      const blueTurns = this.getTurns(pictographData.motions?.blue?.turns);
      const redTurns = this.getTurns(pictographData.motions?.red?.turns);
      return [blueTurns, redTurns];
    } catch {
      return [0, 0];
    }
  }

  private getTurns(value: unknown): number {
    if (typeof value === "number") return value;
    return 0;
  }
}
