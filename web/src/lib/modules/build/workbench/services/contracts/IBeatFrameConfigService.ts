/**
 * Beat Frame Configuration Service Interface
 *
 * Service contract for managing beat frame configuration settings.
 * One-to-one mapping with BeatFrameConfigService implementation.
 */

import type {
    BeatFrameConfig,
    ContainerDimensions,
} from "$domain";

/**
 * Service for managing beat frame configuration
 */
export interface IBeatFrameConfigService {
  getConfig(): BeatFrameConfig;
  updateConfig(updates: Partial<BeatFrameConfig>): BeatFrameConfig;
  resetToDefaults(): BeatFrameConfig;

  // Container dimension management
  getContainerDimensions(): ContainerDimensions;
  updateContainerDimensions(
    dimensions: Partial<ContainerDimensions>
  ): ContainerDimensions;
}
