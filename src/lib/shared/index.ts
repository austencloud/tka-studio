/**
 * Shared Library Exports
 *
 * Clean barrel exports for all shared functionality.
 * This is the main entry point for importing shared types, services, and utilities.
 */

// === SHARED INFRASTRUCTURE ===
export * from "./application";
export * from "./background";
// Export device module explicitly to avoid any re-export ambiguities
export * from "./device/domain";
export * from "./device/services";
export * from "./foundation";
// Modern Swipe Components (Embla-based)
export { BottomSheet, FontAwesomeIcon, HorizontalSwipeContainer } from "./foundation/ui";
export * from "./inversify";
export * from "./navigation";
export * from "./persistence";
export * from "./pictograph";
export * from "./settings";
export * from "./theme";
export * from "./utils";
export { createComponentLogger, debugLogger } from "./utils/debug-logger";
export * from "./validation";

// === MODULE EXPORTS ===
export * from "../modules/build/animate/domain";
export * from "../modules/build/generate/circular/domain";
export * from "../modules/build/generate/shared/domain";
export * from "../modules/build/shared/domain/factories";
export * from "../modules/build/shared/domain/models";
export * from "../modules/gallery/shared/domain";
export * from "../modules/learn/codex/domain";
export * from "../modules/learn/quiz/domain";
export * from "../modules/word-card/domain";

// === SPECIFIC EXPORTS FOR CROSS-MODULE DEPENDENCIES ===

// Storage utility functions (needed by modules)
import { StorageService } from "./foundation/services/implementations/StorageService";

export const safeSessionStorageGet = <T>(
  key: string,
  defaultValue: T | null = null
): T | null => {
  const storageService = new StorageService();
  return storageService.safeSessionStorageGet(key, defaultValue);
};

export const safeSessionStorageSet = <T>(key: string, value: T): void => {
  const storageService = new StorageService();
  storageService.safeSessionStorageSet(key, value);
};

export const safeSessionStorageRemove = (key: string): void => {
  const storageService = new StorageService();
  storageService.removeSessionStorageItem(key);
};

// PNG metadata extractor (needed by modules)
export { PngMetadataExtractor } from "./pictograph/shared/utils/png-metadata-extractor";

// CSV parser interface (needed by modules)
export type { ICSVPictographParserService as ICSVPictographParser } from "./foundation/services/contracts/data/ICSVPictographParserService";

// CAP Type service (needed by CAPCard component)
export type { ICAPTypeService } from "../modules/build/generate/shared/services/contracts/ICAPTypeService";

// Generation orchestration service (needed by generate-actions state)
export type { IGenerationOrchestrationService } from "../modules/build/generate/shared/services/contracts/IGenerationOrchestrationService";

// Sequence export service (needed by button components)
export type { ISequenceExportService } from "../modules/build/shared/services/contracts/ISequenceExportService";

// Mobile services (needed by components)
export type { IMobileFullscreenService } from "./mobile/services/contracts/IMobileFullscreenService";
export type { IPlatformDetectionService } from "./mobile/services/contracts/IPlatformDetectionService";
export type { IGestureService } from "./mobile/services/contracts/IGestureService";

// Beat grid models (needed by workbench)
export type {
    BeatGridConfig,
    ContainerDimensions,
    LayoutInfo
} from "../modules/build/workspace-panel/sequence-display/domain/models/beat-grid-models";
