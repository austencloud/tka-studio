/**
 * Background Factory Interface
 *
 * Interface for factory service that creates background animation systems.
 * Provides static methods for creating and managing background systems.
 */

import type { BackgroundSystem, BackgroundType } from "$shared/domain";

// BackgroundFactoryParams doesn't exist in domain - define locally
interface BackgroundFactoryParams {
  type: BackgroundType;
  quality: string;
  initialQuality: string;
  accessibility?: any;
  settings?: Record<string, any>;
}

export interface IBackgroundFactory {
  /**
   * Create a background system with the specified parameters
   */
  createBackgroundSystem(options: BackgroundFactoryParams): BackgroundSystem;

  /**
   * Create an optimal background system with auto-detected quality
   */
  createOptimalBackgroundSystem(): BackgroundSystem;

  /**
   * Check if a background type is supported on the current device
   */
  isBackgroundSupported(type: string): boolean;

  /**
   * Get list of all supported background types
   */
  getSupportedBackgroundTypes(): BackgroundType[];
}
