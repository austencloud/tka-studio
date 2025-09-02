/**
 * InversifyJS Container Configuration - WORKING VERSION WITH ALL DEPENDENCIES
 *
 * This file sets up the main InversifyJS container and provides
 * the service resolution interface for the TKA application.
 */

import { Container } from "inversify";
import "reflect-metadata";

// Import service types
import { TYPES } from "./types";
// Import service implementations
import {
  CodexService,
  CsvLoader,
  CSVParser,
  LessonRepository,
  LetterMappingRepository,
  LetterQueryHandler,
  PictographOperationsService,
} from "$implementations";

// Import application services
import {
  ApplicationInitializer,
  DeviceDetector,
  LocalStoragePersistenceService,
  SettingsService,
} from "$implementations";

// Import sequence services
import {
  SequenceDomainService,
  SequenceImportService,
  SequenceService,
  SequenceStateService,
} from "$implementations";

// Import build tab services
import { BuildTabService } from "$implementations";

// Import layout services
import { BeatFrameService } from "$implementations";

// Import workbench services
import {
  WorkbenchBeatOperationsService,
  WorkbenchCoordinationService,
  WorkbenchService,
} from "$implementations";

// Import domain services
import { GridModeDeriver } from "$implementations";

// Import rendering services
import { PropCoordinator } from "$implementations";

// Import browse services
import { BrowseService, FavoritesService } from "$implementations";

// Import additional data services
import {
  ArrowPlacementService,
  DataTransformer,
  EnumMapper,
  MotionQueryHandler,
  OptionFilterer,
} from "$implementations";

// Import additional domain services
import {
  LetterDeriver,
  PictographValidatorService,
  PositionPatternService,
} from "$implementations";

// Import export services
import {
  ExportService,
  PageImageExportService,
  ThumbnailService,
} from "$implementations";

// Import generation services
import {
  PageFactoryService,
  PictographGenerator,
  SequenceGenerationService,
} from "$implementations";

// Import background services
import { BackgroundService } from "$implementations";

// Import image export services
import {
  BeatFallbackRenderer,
  BeatRenderingService,
  CanvasManagementService,
  ExportConfigurationManager,
  ExportMemoryCalculator,
  ExportOptionsValidator,
  FileExportService,
  FilenameGeneratorService,
  GridOverlayService,
  ImageCompositionService,
  ImagePreviewGenerator,
  LayoutCalculationService,
  TKAImageExportService,
} from "$implementations";

// Import navigation services
import {
  BrowseSectionService,
  NavigationService,
  PanelManagementService,
} from "$implementations";

// Import additional persistence services
import { FilterPersistenceService } from "$implementations";

// Import positioning services
import {
  ArrowLocationService,
  ArrowPlacementKeyService,
  ArrowPositioningService,
  BetaOffsetCalculator,
  PropPlacementService,
} from "$implementations";

// Import additional rendering services
import {
  ArrowRenderer,
  BeatGridService,
  GridRenderingService,
  OverlayRenderer,
  SvgConfiguration,
  SvgUtilityService,
} from "$implementations";

// Import additional sequence services
import {
  DeleteService,
  PrintablePageLayoutService,
  SequenceDeletionService,
  SequenceIndexService,
} from "$implementations";

// Import motion tester services
import {
  AnimationControlService,
  MotionParameterService,
} from "$implementations";

// Import movement services
import { CSVPictographLoaderService } from "$implementations";

// Import missing construct services (these exist)
import { ConstructSubTabCoordinationService } from "$implementations";

// Additional services will be added as needed

// Import missing services that have confirmed implementations
import {
  ArrowAdjustmentCalculator,
  ArrowCoordinateSystemService,
  ArrowLocationCalculator,
  ArrowPathResolutionService,
  ArrowPositionCalculator,
  ArrowRotationCalculator,
  AttributeKeyGenerator,
  DashLocationCalculator,
  DefaultPlacementService,
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  MotionLetterIdentificationService,
  OrientationCalculationService,
  QuadrantIndexCalculator,
  SpecialPlacementOriKeyGenerator,
  SpecialPlacementService,
  TurnsTupleKeyGenerator,
} from "$implementations";

// Import additional services with confirmed implementations
import { CSVPictographParserService, PositionMapper } from "$implementations";
import { SequenceAnimationEngine } from "../../animator/core/engine/sequence-animation-engine";
import { AnimationStateService } from "../../animator/core/services/AnimationStateService";
import { BeatCalculationService } from "../../animator/core/services/BeatCalculationService";
import { PropInterpolationService } from "../../animator/core/services/PropInterpolationService";
import { SequenceAnimationOrchestrator } from "../../animator/core/services/SequenceAnimationOrchestrator";
// ValidationService is defined as interface in PictographTransformationService but no implementation found

// Import additional services with confirmed implementations
import {
  DimensionCalculationService,
  ImageFormatConverterService,
  SVGToCanvasConverterService,
} from "$implementations";

// Import text rendering services
import {
  DifficultyBadgeRenderer,
  TextRenderingService,
  TextRenderingUtils,
  UserInfoRenderer,
  WordTextRenderer,
} from "$implementations";

// Import start position service
import { StartPositionService } from "$implementations";

// Import option picker services
import {
  OptionPickerDataService,
  OptionPickerLayoutService,
} from "$implementations";

// Create container
const container = new Container();

// Bind all required dependencies for CodexService
try {
  // Bind repositories
  container.bind(TYPES.ILetterMappingRepository).to(LetterMappingRepository);
  container.bind(TYPES.ILessonRepository).to(LessonRepository);

  // Bind data services (dependencies of LetterQueryHandler)
  container.bind(TYPES.ICSVLoader).to(CsvLoader);
  container.bind(TYPES.ICSVParser).to(CSVParser);

  // Bind services
  container
    .bind(TYPES.IPictographOperationsService)
    .to(PictographOperationsService);
  container.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);

  // Finally bind CodexService
  container.bind(TYPES.ICodexService).to(CodexService);

  // Bind application services
  container.bind(TYPES.ISettingsService).to(SettingsService);
  container.bind(TYPES.IPersistenceService).to(LocalStoragePersistenceService);
  container.bind(TYPES.IDeviceDetector).to(DeviceDetector);
  container.bind(TYPES.IApplicationInitializer).to(ApplicationInitializer);

  // Bind sequence services
  container.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
  container.bind(TYPES.ISequenceImportService).to(SequenceImportService);
  container.bind(TYPES.ISequenceService).to(SequenceService);
  container.bind(TYPES.ISequenceStateService).to(SequenceStateService);

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
  container.bind(TYPES.IPropCoordinator).to(PropCoordinator);

  // Bind additional browse services
  container.bind(TYPES.IFavoritesService).to(FavoritesService);

  // Bind additional data services
  container.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService);
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
  container.bind(TYPES.IExportService).to(ExportService);
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
  container
    .bind(TYPES.IExportConfigurationManager)
    .to(ExportConfigurationManager);
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
  container.bind(TYPES.IPanelManagementService).to(PanelManagementService);
  container.bind(TYPES.ISectionService).to(BrowseSectionService);

  // Bind additional persistence services
  container.bind(TYPES.IFilterPersistenceService).to(FilterPersistenceService);

  // Bind positioning services
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
  container.bind(TYPES.ISvgConfiguration).to(SvgConfiguration);
  container.bind(TYPES.ISvgUtilityService).to(SvgUtilityService);

  // Bind additional sequence services
  container.bind(TYPES.IDeleteService).to(DeleteService);
  container
    .bind(TYPES.IPrintablePageLayoutService)
    .to(PrintablePageLayoutService);
  container.bind(TYPES.ISequenceDeletionService).to(SequenceDeletionService);
  container.bind(TYPES.ISequenceIndexService).to(SequenceIndexService);

  // Bind motion tester services
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
  container.bind(TYPES.IPositionMapper).to(PositionMapper);
  container
    .bind(TYPES.ICSVPictographLoaderService)
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
} catch (error) {
  console.error("❌ TKA Container: Failed to bind services:", error);
}

// Export container
export { container };
export const inversifyContainer = container;

// Export TYPES for convenience (many files expect to import TYPES from container)
export { TYPES } from "./types";

// Export resolve function
export function resolve<T>(serviceType: symbol): T {
  return container.get<T>(serviceType);
}
