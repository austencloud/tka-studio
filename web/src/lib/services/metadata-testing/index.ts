/**
 * Metadata Testing Services Index
 *
 * Clean exports for all metadata testing services.
 * This replaces the monolithic state with focused, testable services.
 */

import { GridMode } from "$lib/domain/enums";

// Domain Types
export type {
  ThumbnailFile,
  SequenceFile,
  MetadataAnalysisResult,
  BatchAnalysisResult,
  BatchAnalysisConfig,
  MetadataStats,
  SequenceMetadata,
  MetadataTestingConfig,
  InvalidMotionType,
  MetadataValidationIssue,
} from "$lib/domain/metadata-testing/types";

// Services
export { SequenceDiscoveryService } from "./SequenceDiscoveryService";
export { MetadataExtractionService } from "./MetadataExtractionService";
export { MetadataAnalysisService } from "./MetadataAnalysisService";
export { BatchAnalysisService } from "./BatchAnalysisService";
export { MetadataTestingStateManager } from "./MetadataTestingStateManager";

// Service Interfaces
export type {
  ISequenceDiscoveryService,
  IMetadataExtractionService,
  IMetadataAnalysisService,
  IBatchAnalysisService,
} from "../interfaces/metadata-testing-interfaces";

// Import for factory function
import { MetadataTestingStateManager } from "./MetadataTestingStateManager";
import type { MetadataTestingConfig } from "$lib/domain/metadata-testing/types";

// Factory function for creating a configured state manager
export function createMetadataTestingStateManager(): MetadataTestingStateManager {
  return new MetadataTestingStateManager();
}

// Configuration presets
export const defaultMetadataTestingConfig: MetadataTestingConfig = {
  validMotionTypes: [
    "contact",
    "no_contact",
    "roll",
    "isolation",
    "plane_bend",
    "antiplane_bend",
    "pop",
    "wallplane_pop",
    "antiwall_pop",
    GridMode.BOX,
    GridMode.DIAMOND,
    "figure8",
  ],
  requiredFields: ["letter", "beatNumber"],
  healthScoreWeights: {
    authorWeight: 0.15,
    levelWeight: 0.15,
    startPositionWeight: 0.1,
    beatIntegrityWeight: 0.4,
    motionDataWeight: 0.2,
  },
};
