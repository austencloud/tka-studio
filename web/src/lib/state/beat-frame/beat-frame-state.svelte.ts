/**
 * Beat Frame State Factory
 *
 * Reactive state wrapper around the pure BeatFrameService.
 * Follows the established TKA state factory pattern.
 */

import type { BeatData } from "$domain";
import type {
  BeatFrameConfig,
  ContainerDimensions,
} from "$domain/build/workbench/beat-frame";
import type { IBeatFrameService } from "$lib/services/contracts/beat-frame-interfaces";

/**
 * Creates component-scoped beat frame state
 *
 * @param beatFrameService - Injected via DI container
 * @returns Reactive state object with getters and actions
 */
export function createBeatFrameState(beatFrameService: IBeatFrameService) {
  // ============================================================================
  // REACTIVE STATE (Component-scoped)
  // ============================================================================

  let config = $state<BeatFrameConfig>(beatFrameService.getDefaultConfig());
  let containerDimensions = $state<ContainerDimensions>({
    width: 0,
    height: 0,
    isFullscreen: false,
  });

  // Interaction state
  let hoveredBeatIndex = $state<number>(-1);
  let draggedBeatIndex = $state<number>(-1);

  // ============================================================================
  // DERIVED STATE (Reactive computations)
  // ============================================================================

  const layoutInfo = $derived(() => {
    // This will reactively update when config or containerDimensions change
    return beatFrameService.calculateLayoutInfo(0, config, containerDimensions);
  });

  // ============================================================================
  // GETTERS (Reactive access to state)
  // ============================================================================

  return {
    // Configuration getters
    get config() {
      return config;
    },

    get containerDimensions() {
      return containerDimensions;
    },

    // Interaction state getters
    get hoveredBeatIndex() {
      return hoveredBeatIndex;
    },

    get draggedBeatIndex() {
      return draggedBeatIndex;
    },

    // Derived state getters
    get layoutInfo() {
      return layoutInfo;
    },

    // ============================================================================
    // ACTIONS (State mutations and service calls)
    // ============================================================================

    // Configuration actions
    setConfig(updates: Partial<BeatFrameConfig>) {
      config = beatFrameService.validateConfig({ ...config, ...updates });
    },

    resetConfig() {
      config = beatFrameService.getDefaultConfig();
    },

    // Container dimension actions
    updateContainerDimensions(dimensions: Partial<ContainerDimensions>) {
      containerDimensions = { ...containerDimensions, ...dimensions };
    },

    // Interaction actions
    setHoveredBeatIndex(index: number) {
      hoveredBeatIndex = index;
    },

    clearHover() {
      hoveredBeatIndex = -1;
    },

    setDraggedBeatIndex(index: number) {
      draggedBeatIndex = index;
    },

    clearDrag() {
      draggedBeatIndex = -1;
    },

    // ============================================================================
    // SERVICE DELEGATION (Pure business logic calls)
    // ============================================================================

    // Layout calculation methods (delegated to service)
    calculateBeatPosition(index: number, beatCount?: number) {
      return beatFrameService.calculateBeatPosition(index, beatCount, config);
    },

    calculateStartPosition(beatCount: number) {
      return beatFrameService.calculateStartPosition(beatCount, config);
    },

    calculateFrameDimensions(beatCount: number) {
      return beatFrameService.calculateFrameDimensions(beatCount, config);
    },

    calculateLayoutInfo(beatCount: number) {
      return beatFrameService.calculateLayoutInfo(
        beatCount,
        config,
        containerDimensions
      );
    },

    // Beat interaction helpers (delegated to service)
    getBeatAtPosition(x: number, y: number, beatCount: number) {
      return beatFrameService.getBeatAtPosition(x, y, beatCount, config);
    },

    isBeatVisible(beat: BeatData) {
      return beatFrameService.isBeatVisible(beat);
    },

    getBeatDisplayText(beat: BeatData) {
      return beatFrameService.getBeatDisplayText(beat);
    },

    // Layout optimization methods (delegated to service)
    autoAdjustLayout(beatCount: number) {
      return beatFrameService.autoAdjustLayout(beatCount);
    },

    // ============================================================================
    // CONVENIENCE METHODS
    // ============================================================================

    // Check interaction state
    isHovered(index: number) {
      return hoveredBeatIndex === index;
    },

    isDragged(index: number) {
      return draggedBeatIndex === index;
    },

    // Update beat size based on container (reactive effect trigger)
    updateBeatSizeFromContainer(beatCount = 0) {
      if (containerDimensions.width <= 0 || containerDimensions.height <= 0) {
        return; // Wait for valid dimensions
      }

      const [rows, cols] = beatFrameService.autoAdjustLayout(beatCount);
      const totalCols = cols + (config.hasStartTile ? 1 : 0);

      const newCellSize = beatFrameService.calculateCellSize(
        beatCount,
        containerDimensions.width,
        containerDimensions.height,
        rows,
        totalCols,
        config.gap
      );

      // Update configuration with new size and layout
      config = {
        ...config,
        beatSize: newCellSize,
        columns: cols,
      };
    },
  };
}

/**
 * Type definition for the beat frame state
 */
export type BeatFrameState = ReturnType<typeof createBeatFrameState>;
