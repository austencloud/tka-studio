// barrel star export all directories

export * from "./application";
export * from "./background";
export * from "./device";
export * from "./foundation";
export * from "./inversify";
export * from "./pictograph";
export * from "./settings";
export * from "./validation";

// Export pictograph domain models and enums that are needed across modules
export { ElementalType, GlyphType, HandMotionType, HandPath, MotionColor, MotionType, Orientation, RotationDirection, VTGDirection, VTGMode, VTGTiming } from "./pictograph/shared/domain/enums";
export { createPictographData } from "./pictograph/shared/domain/factories";
export type { ArrowSvgData, CSVRow, ISvgConfig, MotionData, PictographData, SVGDimensions } from "./pictograph/shared/domain/models";
export { createMotionData } from "./pictograph/shared/domain/models/MotionData";

// Export pictograph service contracts that are needed across modules

// Grid interfaces
export type {
  IGridModeDeriver,
  IGridPositionDeriver
} from "./pictograph/grid/services/contracts";

// Export arrow types and services from the new module structure
export type {
  // Data types
  AllPlacementData,
  // Domain types
  ArrowPlacementData, ArrowPosition, GridPlacementData,
  // Orchestration contracts
  IArrowLifecycleManager,
  // Rendering contracts
  IArrowPathResolutionService, IArrowPlacementService,
  // Positioning contracts
  IArrowPositioningOrchestrator, IArrowPositioningService, IDirectionalTupleProcessor, ISvgColorTransformer, ISvgLoader, ISvgParser, JsonPlacementData
} from "./pictograph/arrow";

// Prop interfaces
export type {
  IPropPlacementService
} from "./pictograph/prop/services/contracts";

// Export prop service contracts
export type {
  IBetaDetectionService,
  IBetaOffsetCalculator
} from "./pictograph/prop/services/contracts";


// Export storage service interface and utility functions
export type { IStorageService } from "./foundation/services/contracts/IStorageService";
export { StorageService } from "./foundation/services/implementations/StorageService";

// Export file download service interface
export type { IFileDownloadService } from "./foundation/services/contracts/IFileDownloadService";

// Export CSV parser interfaces
export type { ICSVPictographParser } from "../modules/build/generate/services/contracts/ICsvPictographParserService";

// Import StorageService for utility functions
import { StorageService } from "./foundation/services/implementations/StorageService";

// Export utility functions that were converted to services
export const safeSessionStorageGet = <T>(key: string, defaultValue: T | null = null): T | null => {
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

// Export PNG metadata extractor
export { PngMetadataExtractor } from "./pictograph/shared/utils/png-metadata-extractor";

// Re-export module-specific domain types for global access
// Build module exports - BeatData and workbench models
export * from "../modules/build/workbench/shared/domain/factories";

// Export beat grid models
export type {
  BeatGridConfig,
  ContainerDimensions,
  LayoutInfo
} from "../modules/build/workbench/sequence-display/domain/models/beat-grid-models";
export * from "../modules/build/workbench/shared/domain/models";

// Build generate domain exports
export * from "../modules/build/generate/domain";
export type { CSVParseResult, ParsedCsvRow } from "../modules/build/generate/domain";

// Browse gallery domain exports
export * from "../modules/browse/gallery/domain";

// Learn module exports  
export * from "../modules/learn/codex/domain";
export * from "../modules/learn/quiz/domain";

// Animator module exports
export * from "../modules/animator/domain";

// Word-card module exports
export * from "../modules/word-card/domain";

