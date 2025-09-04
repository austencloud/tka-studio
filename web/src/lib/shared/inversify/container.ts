/**
 * InversifyJS Container Config - WORKING VERSION WITH ALL DEPENDENCIES
 *
 * This file sets up the main InversifyJS container and provides
 * the service resolution interface for the TKA application.
 */

import { Container } from "inversify";
import "reflect-metadata";

// Import service types
// Import service implementations using new tab-first structure

// TEMPORARY: NO SERVICE IMPORTS - JUST BASIC CONTAINER
// All services commented out until import paths are fixed
// import { SettingsService } from "../services/core/implementations";
// import { BuildTabService } from "../../modules/build/services/implementations";

// Learn services - OLD LAYER-FIRST STRUCTURE (Commented out for now)
// import {
//   CodexService,
//   QuizRepoManager,
//   CodexLetterMappingRepo,
//   CodexPictographUpdater,
// } from "../../modules/learn/services/implementations";

// Word Card services - OLD LAYER-FIRST STRUCTURE (Commented out for now)
// import {
//   PageFactoryService,
//   PageImageExportService,
// } from "../../services/word-card/implementations";

// Additional Build services (Commented out for now)
// import {
//   BeatRenderingService,
//   CanvasManagementService,
//   ConstructSubTabCoordinationService,
//   CSVPictographLoaderService,
//   DeleteService,
//   ExportConfig,
//   ExportMemoryCalculator,
//   ExportOptionsValidator,
//   FileExportService,
//   FilenameGeneratorService,
//   GridOverlayService,
//   ImageCompositionService,
//   ImagePreviewGenerator,
//   LayoutCalculationService,
//   PrintablePageLayoutService,
//   SequenceDeletionService,
//   SequenceIndexService,
//   TKAImageExportService,
// } from "../../modules/build/services/implementations";

// Additional services (Commented out for now)
// import { BeatFallbackRenderer } from "../../services/core/implementations";
// import {
//   BrowsePanelManager,
//   BrowseSectionService,
//   BrowseStatePersister,
//   FilterPersistenceService,
//   NavigationService,
// } from "../../modules/browse/services/implementations";
// import {
//   ArrowLocationService,
//   ArrowPlacementKeyService,
//   ArrowPositioningService,
//   ArrowRenderer,
//   BeatGridService,
//   BetaOffsetCalculator,
//   GridRenderingService,
//   OverlayRenderer,
//   PropPlacementService,
//   SvgConfig,
//   SvgUtilityService,
// } from "../../services/core/implementations";

// Animator services - NEW MODULE-FIRST STRUCTURE (Commented out)
// import {
//   AnimationControlService,
//   MotionParameterService,
// } from "../../modules/animator/services/implementations";

// Additional services will be added as needed

// Additional Core services (positioning, calculation, parsing) - Commented out
// import {
//   ArrowAdjustmentCalculator,
//   ArrowCoordinateSystemService,
//   ArrowLocationCalculator,
//   ArrowPathResolutionService,
//   ArrowPositionCalculator,
//   ArrowRotationCalculator,
//   AttributeKeyGenerator,
//   DashLocationCalculator,
//   DefaultPlacementService,
//   DirectionalTupleProcessor,
//   GridPositionDeriver,
//   OrientationCalculationService,
//   PropCoordinator,
//   SpecialPlacementOriKeyGenerator,
//   SpecialPlacementService,
//   TurnsTupleKeyGenerator,
// } from "../core/implementations";

// All remaining imports commented out
// import {
//   DirectionalTupleCalculator,
//   QuadrantIndexCalculator,
// } from "../core/implementations/pictograph/positioning/processors/DirectionalTupleProcessor";
// import { CSVPictographParserService } from "../../modules/build/services/implementations";
// import {
//   AnimationStateService,
//   BeatCalculationService,
//   MotionLetterIdentificationService,
//   PropInterpolationService,
//   SequenceAnimationEngine,
//   SequenceAnimationOrchestrator,
// } from "../../modules/animator/services/implementations";
// import {
//   DifficultyBadgeRenderer,
//   DimensionCalculationService,
//   ImageFormatConverterService,
//   OptionPickerDataService,
//   OptionPickerLayoutService,
//   StartPositionService,
//   SVGToCanvasConverterService,
//   TextRenderingService,
//   TextRenderingUtils,
//   UserInfoRenderer,
//   WordTextRenderer,
// } from "../../modules/build/services/implementations";

// Create container
const container = new Container();

// TEMPORARY: All service bindings commented out until import paths are fixed
/*
// Bind all required dependencies for CodexService
try {
  // Bind repositories
  container.bind(TYPES.ICodexCodexLetterMappingRepo).to(CodexLetterMappingRepo);
  container.bind(TYPES.IQuizRepoManager).to(QuizRepoManager);

  // Bind data services (dependencies of LetterQueryHandler)
  container.bind(TYPES.ICSVLoader).to(CsvLoader);
  container.bind(TYPES.ICSVParser).to(CSVParser);

  // Bind services
  container
    .bind(TYPES.ICodexPictographUpdater)
    .to(CodexPictographUpdater);
  container.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);

  // Finally bind CodexService
  container.bind(TYPES.ICodexService).to(CodexService);

  // Bind application services
  container.bind(TYPES.ISettingsService).to(SettingsService);
  container.bind(TYPES.IPersistenceService).to(FilterPersistenceService);
  container.bind(TYPES.IDeviceDetector).to(DeviceDetector);
  container.bind(TYPES.IApplicationInitializer).to(ApplicationInitializer);

  // Bind sequence services
  container.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
  container.bind(TYPES.ISequenceImportService).to(SequenceImportService);
  container.bind(TYPES.ISequenceService).to(SequenceService);
  container.bind(TYPES.ISequenceStateService).to(SequenceStateService);

  // TEMPORARY: All remaining service bindings commented out
  /*
  // Bind build tab services
  container.bind(TYPES.IBuildTabService).to(BuildTabService);

  // Bind option picker services
  container
    .bind(TYPES.IOptionPickerLayoutService)
    .to(OptionPickerLayoutService);
  container.bind(TYPES.IOptionPickerDataService).to(OptionPickerDataService);

  // Bind layout services
  container.bind(TYPES.IBeatFrameService).to(BeatFrameService);

  // Bind workbench services
  container.bind(TYPES.IWorkbenchService).to(WorkbenchService);
  container
    .bind(TYPES.IWorkbenchCoordinationService)
    .to(WorkbenchCoordinationService);
  container
    .bind(TYPES.IWorkbenchBeatOperationsService)
    .to(WorkbenchBeatOperationsService);

  // Bind domain services (StartPositionService moved to unified service below)
  container.bind(TYPES.IGridModeDeriver).to(GridModeDeriver);

  // Bind rendering services
  // PropCoordinator is exported from core/implementations
  container.bind(TYPES.IPropCoordinator).to(PropCoordinator);

  // Bind additional browse services
  container.bind(TYPES.IFavoritesService).to(FavoritesService);

  // Bind additional data services
  // container.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService); // TODO: Restore when positioning directory is recreated
  container.bind(TYPES.IDataTransformer).to(DataTransformer);
  container.bind(TYPES.IEnumMapper).to(EnumMapper);
  container.bind(TYPES.IMotionQueryHandler).to(MotionQueryHandler);
  container.bind(TYPES.IOptionFilterer).to(OptionFilterer);

  // Bind additional domain services
  container.bind(TYPES.ILetterDeriver).to(LetterDeriver);
  container
    .bind(TYPES.IPictographValidatorService)
    .to(PictographValidatorService);
  container.bind(TYPES.IPositionPatternService).to(PositionPatternService);

  // Bind export services
  // ExportService was renamed - using FileExportService instead
  // container.bind(TYPES.IExportService).to(ExportService);
  container.bind(TYPES.IPageImageExportService).to(PageImageExportService);
  container.bind(TYPES.IThumbnailService).to(ThumbnailService);

  // Bind generation services
  container.bind(TYPES.IPageFactoryService).to(PageFactoryService);
  container.bind(TYPES.IPictographGenerator).to(PictographGenerator);
  container
    .bind(TYPES.ISequenceGenerationService)
    .to(SequenceGenerationService);

  // Bind background services
  container.bind(TYPES.IBackgroundService).to(BackgroundService);

  // Bind image export services
  container.bind(TYPES.IBeatRenderingService).to(BeatRenderingService);
  container.bind(TYPES.IBeatFallbackRenderer).to(BeatFallbackRenderer);
  container.bind(TYPES.ICanvasManagementService).to(CanvasManagementService);
  container.bind(TYPES.IExportConfigManager).to(ExportConfig);
  container.bind(TYPES.IExportMemoryCalculator).to(ExportMemoryCalculator);
  container.bind(TYPES.IExportOptionsValidator).to(ExportOptionsValidator);
  container.bind(TYPES.IFileExportService).to(FileExportService);
  container.bind(TYPES.IFilenameGeneratorService).to(FilenameGeneratorService);
  container.bind(TYPES.IGridOverlayService).to(GridOverlayService);
  container.bind(TYPES.IImageCompositionService).to(ImageCompositionService);
  container.bind(TYPES.IImagePreviewGenerator).to(ImagePreviewGenerator);
  container.bind(TYPES.ILayoutCalculationService).to(LayoutCalculationService);
  container.bind(TYPES.ITKAImageExportService).to(TKAImageExportService);

  // Bind text rendering services
  container.bind(TYPES.IWordTextRenderer).to(WordTextRenderer);
  container.bind(TYPES.IUserInfoRenderer).to(UserInfoRenderer);
  container.bind(TYPES.IDifficultyBadgeRenderer).to(DifficultyBadgeRenderer);
  container.bind(TYPES.ITextRenderingUtils).to(TextRenderingUtils);
  container.bind(TYPES.ITextRenderingService).to(TextRenderingService);

  // Bind start position service as singleton
  container
    .bind(TYPES.IStartPositionService)
    .to(StartPositionService)
    .inSingletonScope();

  // Bind navigation services
  container.bind(TYPES.INavigationService).to(NavigationService);
  container.bind(TYPES.IPanelManagementService).to(BrowsePanelManager);
  container.bind(TYPES.ISectionService).to(BrowseSectionService);

  // Bind additional persistence services
  container.bind(TYPES.IBrowseStatePersister).to(BrowseStatePersister);
  container.bind(TYPES.IFilterPersistenceService).to(FilterPersistenceService);

  // Bind positioning services (from core/pictograph/positioning)
  container.bind(TYPES.IArrowLocationService).to(ArrowLocationService);
  container.bind(TYPES.IArrowPlacementKeyService).to(ArrowPlacementKeyService);
  container.bind(TYPES.IArrowPositioningService).to(ArrowPositioningService);
  container.bind(TYPES.IBetaOffsetCalculator).to(BetaOffsetCalculator);
  container.bind(TYPES.IPropPlacementService).to(PropPlacementService);

  // Bind additional rendering services
  container.bind(TYPES.IArrowRenderer).to(ArrowRenderer);
  container.bind(TYPES.IBeatGridService).to(BeatGridService);
  container.bind(TYPES.IGridRenderingService).to(GridRenderingService);
  container.bind(TYPES.IOverlayRenderer).to(OverlayRenderer);
  container.bind(TYPES.ISvgConfig).to(SvgConfig);
  container.bind(TYPES.ISvgUtilityService).to(SvgUtilityService);

  // Bind additional sequence services
  container.bind(TYPES.IDeleteService).to(DeleteService);
  container
    .bind(TYPES.IPrintablePageLayoutService)
    .to(PrintablePageLayoutService);
  container.bind(TYPES.ISequenceDeletionService).to(SequenceDeletionService);
  container.bind(TYPES.ISequenceIndexService).to(SequenceIndexService);

  // Bind animator services
  container.bind(TYPES.IAnimationControlService).to(AnimationControlService);
  container.bind(TYPES.IMotionParameterService).to(MotionParameterService);

  // Bind movement services
  container
    .bind(TYPES.ICSVPictographLoaderService)
    .to(CSVPictographLoaderService);

  // Bind construct services
  container
    .bind(TYPES.IConstructTabCoordinator)
    .to(ConstructSubTabCoordinationService);
  container.bind(TYPES.IBrowseService).to(BrowseService);
  // Bind arrow positioning orchestrator
  container
    .bind(TYPES.IArrowPositioningOrchestrator)
    .to(ArrowPositionCalculator);
  container
    .bind(TYPES.IArrowAdjustmentCalculator)
    .to(ArrowAdjustmentCalculator);
  container.bind(TYPES.IArrowLocationCalculator).to(ArrowLocationCalculator);
  container.bind(TYPES.IArrowRotationCalculator).to(ArrowRotationCalculator);
  container.bind(TYPES.IDashLocationCalculator).to(DashLocationCalculator);
  container.bind(TYPES.ISpecialPlacementService).to(SpecialPlacementService);
  container.bind(TYPES.IDefaultPlacementService).to(DefaultPlacementService);
  // Bind key generators and processors
  container
    .bind(TYPES.ISpecialPlacementOriKeyGenerator)
    .to(SpecialPlacementOriKeyGenerator);
  container.bind(TYPES.ITurnsTupleKeyGenerator).to(TurnsTupleKeyGenerator);
  container.bind(TYPES.IAttributeKeyGenerator).to(AttributeKeyGenerator);
  container
    .bind(TYPES.IDirectionalTupleProcessor)
    .to(DirectionalTupleProcessor);
  container
    .bind(TYPES.IDirectionalTupleCalculator)
    .to(DirectionalTupleCalculator);
  container.bind(TYPES.IQuadrantIndexCalculator).to(QuadrantIndexCalculator);
  container
    .bind(TYPES.IArrowCoordinateSystemService)
    .to(ArrowCoordinateSystemService);
  container
    .bind(TYPES.IOrientationCalculationService)
    .to(OrientationCalculationService);
  container
    .bind(TYPES.IMotionLetterIdentificationService)
    .to(MotionLetterIdentificationService);
  container
    .bind(TYPES.IArrowPathResolutionService)
    .to(ArrowPathResolutionService);
  container.bind(TYPES.IPositionMapper).to(GridPositionDeriver);
  container
    .bind(TYPES.ICSVPictographParserService)
    .to(CSVPictographParserService);
  container.bind(TYPES.ISequenceAnimationEngine).to(SequenceAnimationEngine);
  container
    .bind(TYPES.ISequenceAnimationOrchestrator)
    .to(SequenceAnimationOrchestrator);
  container.bind(TYPES.IAnimationStateService).to(AnimationStateService);
  container.bind(TYPES.IBeatCalculationService).to(BeatCalculationService);
  container.bind(TYPES.IPropInterpolationService).to(PropInterpolationService);
  container
    .bind(TYPES.IDimensionCalculationService)
    .to(DimensionCalculationService);
  container
    .bind(TYPES.IImageFormatConverterService)
    .to(ImageFormatConverterService);
  container
    .bind(TYPES.ISVGToCanvasConverterService)
    .to(SVGToCanvasConverterService);

  // === UTILITY SERVICES ===
  container.bind(TYPES.IBetaDetectionService).to(BetaDetectionService);
  container.bind(TYPES.IErrorHandlingService).to(ErrorHandlingService);
  */
// } catch (error) {
//   console.error("❌ TKA Container: Failed to bind services:", error);
// }

// Export container
export { container };
export const inversifyContainer = container;

// Export TYPES for convenience (many files expect to import TYPES from container)
export { TYPES } from "./types";

// Export resolve function
export function resolve<T>(serviceType: symbol): T {
  return container.get<T>(serviceType);
}
