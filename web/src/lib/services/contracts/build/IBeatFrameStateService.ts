/**
 * Beat Frame State Service Interface
 *
 * Service contract for managing beat frame interaction state.
 * One-to-one mapping with BeatFrameStateService implementation.
 */

/**
 * Service for managing beat frame interaction state (hover, drag, selection)
 */
export interface IBeatFrameStateService {
  // Hover state
  getHoveredBeatIndex(): number;
  setHoveredBeatIndex(index: number): void;
  clearHover(): void;

  // Drag state
  getDraggedBeatIndex(): number;
  setDraggedBeatIndex(index: number): void;
  clearDrag(): void;

  // Selection helpers
  isHovered(index: number): boolean;
  isDragged(index: number): boolean;
}
