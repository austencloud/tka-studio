// @ts-nocheck
/**
 * Metadata Testing Services Index
 *
 * Clean exports for all metadata testing services.
 * This replaces the monolithic state with focused, testable services.
 */

import { GridMode } from "$lib/domain/enums";

// Domain Types
export type {
  BatchAnalysisConfig,
  BatchAnalysisResult,
  InvalidMotionType,
  MetadataAnalysisResult,
  MetadataStats,
  MetadataTestingConfig,
  MetadataValidationIssue,
  SequenceFile,
  SequenceMetadata,
  ThumbnailFile,
} from "$lib/domain/metadata-testing/types";

// Services
export { BatchAnalysisService } from "./BatchAnalysisService";
export { MetadataAnalysisService } from "./MetadataAnalysisService";
export { MetadataExtractionService } from "./MetadataExtractionService";
export { MetadataTestingStateManager } from "./MetadataTestingStateManager";
export { SequenceDiscoveryService } from "./SequenceDiscoveryService";

// Service Interfaces
export type {
  IBatchAnalysisService,
  IMetadataAnalysisService,
  IMetadataExtractionService,
  ISequenceDiscoveryService,
} from "../../contracts/metadata-testing-interfaces";

// Import for factory function
import type { MetadataTestingConfig } from "$lib/domain/metadata-testing/types";
import { MetadataTestingStateManager } from "./MetadataTestingStateManager";

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

