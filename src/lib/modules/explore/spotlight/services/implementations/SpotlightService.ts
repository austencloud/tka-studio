/**
 * Spotlight Service Implementation
 *
 * Handles spotlight business logic and state coordination.
 */

import type { SequenceData } from "$shared";
import { injectable } from "inversify";
import type {
  SpotlightDisplayState,
  SpotlightImageState,
  SpotlightNavigationState,
  SpotlightViewState,
} from "../../domain/models";
import {
  createDefaultImageState,
  createDefaultNavigationState,
  createDefaultSpotlightDisplayState,
} from "../../domain/models";
import type { ISpotlightService } from "../contracts";

@injectable()
export class SpotlightService implements ISpotlightService {
  private displayState: SpotlightDisplayState =
    createDefaultSpotlightDisplayState();
  private imageState: SpotlightImageState = createDefaultImageState();
  private navigationState: SpotlightNavigationState =
    createDefaultNavigationState();

  initializeSpotlight(sequence: SequenceData): void {
    console.log("🎭 Initializing spotlight for sequence:", sequence.id);

    // Reset to defaults
    this.displayState = createDefaultSpotlightDisplayState();
    this.imageState = createDefaultImageState();
    this.imageState.loadStartTime = performance.now();

    // Calculate navigation state
    this.calculateNavigationState(sequence, 0);

    console.log("✅ Spotlight initialized");
  }

  resetSpotlightState(): void {
    this.displayState = createDefaultSpotlightDisplayState();
    this.imageState = createDefaultImageState();
    this.navigationState = createDefaultNavigationState();
  }

  handleVariationChange(newIndex: number): void {
    console.log(`🔄 Variation changed to index: ${newIndex}`);
    this.displayState.currentVariationIndex = newIndex;
    this.displayState.isContentVisible = false;
    this.imageState.isLoading = true;
    this.imageState.hasError = false;
    this.imageState.loadStartTime = performance.now();
  }

  handleImageLoad(): void {
    const loadEndTime = performance.now();
    const loadDuration = loadEndTime - this.imageState.loadStartTime;

    console.log(
      `📸 [TIMING] Image loading completed at ${loadEndTime.toFixed(2)}ms (duration: ${loadDuration.toFixed(2)}ms)`
    );

    this.imageState.isLoading = false;
    this.imageState.hasError = false;
    this.displayState.isContentVisible = true;
  }

  handleImageError(): void {
    console.warn("❌ Image failed to load");
    this.imageState.isLoading = false;
    this.imageState.hasError = true;
  }

  handleShow(): void {
    const viewerStartTime = performance.now();
    console.log(
      `🎭 [TIMING] Spotlight viewer opened at ${viewerStartTime.toFixed(2)}ms`
    );

    this.displayState.isVisible = true;
    this.displayState.isClosing = false;
    this.displayState.isContentVisible = false;
  }

  handleClose(): void {
    console.log("❌ Closing spotlight viewer");
    this.displayState.isClosing = true;
  }

  getCurrentState(): SpotlightViewState {
    return {
      display: { ...this.displayState },
      image: { ...this.imageState },
      navigation: { ...this.navigationState },
    };
  }

  calculateNavigationState(sequence: SequenceData, currentIndex: number): void {
    const totalVariations = sequence.thumbnails?.length || 0;

    this.navigationState = {
      hasMultipleVariations: totalVariations > 1,
      totalVariations,
      canGoPrev: currentIndex > 0,
      canGoNext: currentIndex < totalVariations - 1,
    };

    this.displayState.currentVariationIndex = currentIndex;
  }
}
