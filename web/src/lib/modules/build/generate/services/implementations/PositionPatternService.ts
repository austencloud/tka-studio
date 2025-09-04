/**
 * Position Pattern Service - Position sequences and grid patterns
 *
 * Manages position sequences for pictograph generation.
 * Provides standard position sequences for alpha, beta, and gamma systems.
 */

import { GridPosition } from "$domain";
import type { IPositionPatternService } from "$services";
import { injectable } from "inversify";

@injectable()
export class PositionPatternService implements IPositionPatternService {
  getAlphaSequence(): GridPosition[] {
    return [
      GridPosition.ALPHA3,
      GridPosition.ALPHA5,
      GridPosition.ALPHA7,
      GridPosition.ALPHA1,
    ];
  }

  getBetaSequence(): GridPosition[] {
    return [
      GridPosition.BETA3,
      GridPosition.BETA5,
      GridPosition.BETA7,
      GridPosition.BETA1,
    ];
  }

  getGammaSequence(): GridPosition[] {
    return [
      GridPosition.GAMMA3,
      GridPosition.GAMMA5,
      GridPosition.GAMMA7,
      GridPosition.GAMMA1,
      GridPosition.GAMMA11,
      GridPosition.GAMMA13,
      GridPosition.GAMMA15,
      GridPosition.GAMMA9,
    ];
  }

  getCustomSequence(positions: GridPosition[]): GridPosition[] {
    return [...positions];
  }

  generatePositionSequence(
    positionSystem: string,
    length: number = 8
  ): GridPosition[] {
    let baseSequence: GridPosition[];

    switch (positionSystem.toLowerCase()) {
      case "alpha":
        baseSequence = this.getAlphaSequence();
        break;
      case "beta":
        baseSequence = this.getBetaSequence();
        break;
      case "gamma":
        baseSequence = this.getGammaSequence();
        break;
      default:
        baseSequence = this.getAlphaSequence();
    }

    const result: GridPosition[] = [];
    for (let i = 0; i < length; i++) {
      result.push(baseSequence[i % baseSequence.length]);
    }
    return result;
  }
}
