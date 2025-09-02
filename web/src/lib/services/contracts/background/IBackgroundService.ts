/**
 * Background Service Interface
 *
 * Service for creating and managing background animation systems.
 * Provides factory methods for background systems and quality detection.
 */

import type { BackgroundSystem, BackgroundType, QualityLevel } from "$domain";

export interface IBackgroundService {
  /**
   * Create a background system of the specified type and quality
   */
  createSystem(
    type: BackgroundType,
    quality: QualityLevel
  ): Promise<BackgroundSystem>;
}
