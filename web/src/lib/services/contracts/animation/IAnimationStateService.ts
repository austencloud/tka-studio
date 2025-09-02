/**
 * Animation State Service Interface
 *
 * Interface for managing animation state.
 * Handles prop state updates and management.
 */

import type { PropState } from "$lib/components/tabs/browse-tab/animator/types/PropState";
import type { PropStates } from "./ISequenceAnimationEngine";

export interface IAnimationStateService {
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getPropStates(): PropStates;
  updatePropStates(interpolationResult: InterpolationResult): PropStates;
  updateBluePropState(updates: Partial<PropState>): void;
  updateRedPropState(updates: Partial<PropState>): void;
  setPropStates(blue: PropState, red: PropState): void;
  resetPropStates(): void;
}

export interface InterpolationResult {
  blueAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  redAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  isValid: boolean;
}
