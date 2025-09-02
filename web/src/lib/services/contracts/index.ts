/**
 * Service Contracts Index
 *
 * Central export for all service behavioral contracts.
 * These define what operations and behaviors are available.
 */

// ENTERPRISE PATTERN: One-to-one interface-to-implementation mapping
// Organized by domain structure that mirrors implementations

// Animation Domain
export * from "./animation/IAnimationControlService";
export * from "./animation/IAnimationStateService";
export * from "./animation/IBeatCalculationService";
export * from "./animation/IPropInterpolationService";
export * from "./animation/ISequenceAnimationEngine";
export * from "./animation/ISequenceAnimationOrchestrator";

// Application Domain
export * from "./application/IApplicationInitializer";
export * from "./application/ICodexService";
export * from "./application/IConstructTabCoordinator";
export * from "./application/ICSVLoader";
export * from "./application/ICSVParser";
export * from "./application/IDeviceDetector";
export * from "./application/IEnumMapper";
export * from "./application/IOptionDataService";
export * from "./application/ISettingsService";
export * from "./application/IStartPositionSelectionService";
export * from "./application/IStartPositionService";

// Background Domain
export * from "./background/IBackgroundFactory";
export * from "./background/IBackgroundService";
export * from "./background/IBackgroundSystem";

// Build Domain - TODO: Move to individual interface files
export * from "./build-interfaces";

// Browse Domain
export * from "./browse-interfaces";
export * from "./browse/IBrowseSectionService";
export * from "./browse/IMetadataExtractionService";

// Beat Frame Domain
export * from "./beat-frame-interfaces";

// Beat Grid Domain
export * from "./beat-grid-interfaces";

// Beat Fallback Domain
export * from "./beat-fallback-interfaces";

// Data Domain - Selective exports to avoid conflicts
export type {
  ILetterQueryHandler,
  IMotionQueryHandler,
} from "./data-interfaces";

// Export Domain
export * from "./export-interfaces";
export * from "./IBatchExportService";

// Generation Domain - Selective exports to avoid conflicts
export type {
  IDirectionCalculator,
  ILetterDeriver,
  ILetterGenerator,
  IOrientationCalculationService,
  IPictographGenerator,
  IPictographValidatorService,
  IPositionPatternService,
  ISequenceGenerationService,
} from "./generation-interfaces";

// NOTE: Domain types should be imported directly from $domain, not re-exported from contracts

// Image Export Domain
export * from "./image-export-interfaces";

// Pictograph Domain - Selective exports to avoid conflicts
export type {
  IArrowRenderer,
  IFallbackArrowService,
  IGridRenderingService,
  IOverlayRenderer,
  ISvgColorTransformer,
  ISvgConfiguration,
  ISvgLoader,
  ISvgParser,
  ISvgUtilityService,
} from "./pictograph-interfaces";

// TODO: Replace these consolidated interface files with individual domain-organized interfaces
// Following the one-to-one interface-to-implementation pattern

// Learn Domain - Individual interfaces (correct pattern)
export * from "./learn/ILessonRepository";
export * from "./learn/ILetterMappingRepository";

// Sequence Domain - Individual interface (correct pattern)
export * from "./sequence/ISequenceStateService";

// Temporary exports until migration to individual interfaces is complete
// TEMPORARILY REMOVED: export * from "./motion-tester-interfaces"; (conflicts with IAnimationControlService)
export type { IMotionParameterService } from "./motion-tester-interfaces";
export * from "./option-picker-interfaces";
export * from "./panel-interfaces";
// TEMPORARILY REMOVED: export * from "./pictograph-interfaces"; (conflicts with IArrowPathResolutionService, IArrowPositioningService)
// Positioning Domain - Explicit exports to avoid conflicts
export * from "./positioning-interfaces";
export * from "./responsive-layout-interfaces";

// Export sequence-interfaces but exclude conflicting types that are now in browse domain
// Only export service interfaces, not data models (which belong in domain)
export {
  type IPageFactoryService,
  type IPersistenceService,
  type IPrintablePageLayoutService,
  type ISequenceCardExportIntegrationService,
  type ISequenceDeletionService,
  type ISequenceDomainService,
  type ISequenceImportService,
  // Service interfaces (excluding conflicting IDeleteService)
  type ISequenceService,
  type IWorkbenchBeatOperationsService,
  // Domain types re-exported for service contracts
  type SequenceCardGridConfig,
} from "./sequence-interfaces";

// NOTE: Domain types should be imported directly from $domain, not re-exported from contracts

// TEMPORARILY REMOVED: export * from "./sequence-state-interfaces"; (conflicts with ISequenceStateService)
export * from "./svg-conversion-interfaces";
export * from "./text-rendering-interfaces";
export * from "./workbench-interfaces";

// Movement Domain - Individual interfaces (correct pattern)
export * from "./movement/ICSVPictographParserService";
