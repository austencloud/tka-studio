import { injectable } from 'inversify';
import type { BeatData } from '$shared';

export interface ITurnControlService {
  getTurnValues(): number[];
  canDecrementTurn(turnValue: number | "fl" | undefined): boolean;
  canIncrementTurn(turnValue: number | "fl" | undefined): boolean;
  incrementTurn(currentValue: number | "fl" | undefined): number;
  decrementTurn(currentValue: number | "fl" | undefined): number;
  getTurnValue(turns: number | "fl" | undefined): string;
  getTurnDescription(turns: number | "fl" | undefined): string;
  getCurrentTurnValue(beatData: BeatData | null, color: 'blue' | 'red'): number;
  formatTurnDisplay(turnAmount: number): string;
}

@injectable()
export class TurnControlService implements ITurnControlService {
  private readonly turnValues = [0, 0.5, 1, 1.5, 2, 2.5, 3];

  getTurnValues(): number[] {
    return [...this.turnValues];
  }

  canDecrementTurn(turnValue: number | "fl" | undefined): boolean {
    if (typeof turnValue !== 'number') return false;
    return this.turnValues.indexOf(turnValue) > 0;
  }

  canIncrementTurn(turnValue: number | "fl" | undefined): boolean {
    if (typeof turnValue !== 'number') return false;
    return this.turnValues.indexOf(turnValue) < this.turnValues.length - 1;
  }

  incrementTurn(currentValue: number | "fl" | undefined): number {
    if (typeof currentValue !== 'number') return 0;
    const currentIndex = this.turnValues.indexOf(currentValue);
    if (currentIndex < this.turnValues.length - 1) {
      return this.turnValues[currentIndex + 1];
    }
    return currentValue;
  }

  decrementTurn(currentValue: number | "fl" | undefined): number {
    if (typeof currentValue !== 'number') return 0;
    const currentIndex = this.turnValues.indexOf(currentValue);
    if (currentIndex > 0) {
      return this.turnValues[currentIndex - 1];
    }
    return currentValue;
  }

  getTurnValue(turns: number | "fl" | undefined): string {
    if (turns === undefined || turns === null) return "0";
    return turns.toString();
  }

  getTurnDescription(turns: number | "fl" | undefined): string {
    if (turns === undefined || turns === null || turns === 0) return "No turn";
    if (turns === "fl") return "Float";
    if (typeof turns === "number") {
      return turns > 0 ? "Clockwise" : "Counter-clockwise";
    }
    return "Unknown";
  }

  getCurrentTurnValue(beatData: BeatData | null, color: 'blue' | 'red'): number {
    const turnValue = color === 'blue'
      ? beatData?.motions?.blue?.turns
      : beatData?.motions?.red?.turns;
    return typeof turnValue === 'number' ? turnValue : 0;
  }

  formatTurnDisplay(turnAmount: number): string {
    if (turnAmount === 0) return "0";
    return turnAmount > 0 ? `+${turnAmount}` : `${turnAmount}`;
  }
}
