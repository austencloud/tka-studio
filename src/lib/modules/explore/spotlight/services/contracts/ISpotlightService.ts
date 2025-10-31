import type { SequenceData } from "$shared";
import type { SpotlightViewState } from "../../domain";

export interface ISpotlightService {
  initializeSpotlight(sequence: SequenceData): void;

  resetSpotlightState(): void;

  handleVariationChange(newIndex: number): void;

  handleImageLoad(): void;

  handleImageError(): void;

  handleShow(): void;

  handleClose(): void;

  getCurrentState(): SpotlightViewState;

  calculateNavigationState(sequence: SequenceData, currentIndex: number): void;
}
