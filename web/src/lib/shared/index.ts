/**
 * Shared Library Exports
 *
 * Clean barrel exports for all shared functionality.
 * This is the main entry point for importing shared types, services, and utilities.
 */

// === SHARED INFRASTRUCTURE ===
export * from "./application";
export * from "./background";
export * from "./device";
export * from "./foundation";
export * from "./inversify";
export * from "./navigation";
export * from "./persistence";
export * from "./pictograph";
export * from "./settings";
export * from "./validation";

// === MODULE EXPORTS ===
export * from "../modules/animator/domain";
export * from "../modules/build/generate/domain";
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
export type { ICSVPictographParser } from "../modules/build/generate/services/contracts/ICsvPictographParserService";

// Beat grid models (needed by workbench)
export type {
    BeatGridConfig,
    ContainerDimensions,
    LayoutInfo
} from "../modules/build/workbench/sequence-display/domain/models/beat-grid-models";

