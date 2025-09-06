import { Container } from "inversify";
import { PageFactoryService, PageImageExportService } from "../../modules";
import {
  AnimationControlService,
  AnimationStateService,
  BeatCalculationService,
  MotionLetterIdentificationService,
  MotionParameterService,
  PropInterpolationService,
  SequenceAnimationEngine,
  SequenceAnimationOrchestrator,
} from "../../modules/animator/services";
import { BrowseStatePersister } from "../../modules/browse/gallery/services/implementations/BrowseStatePersister";
import { FavoritesService } from "../../modules/browse/gallery/services/implementations/FavoritesService";
import { FilterPersistenceService } from "../../modules/browse/gallery/services/implementations/FilterPersistenceService";
import { GalleryPanelManager } from "../../modules/browse/gallery/services/implementations/GalleryPanelManager";
import { BrowseSectionService } from "../../modules/browse/gallery/services/implementations/GallerySectionService";
import { GalleryService } from "../../modules/browse/gallery/services/implementations/GalleryService";
import { GalleryThumbnailService } from "../../modules/browse/gallery/services/implementations/GalleryThumbnailService";
import { NavigationService } from "../../modules/browse/gallery/services/implementations/NavigationService";
import { BrowsePersistenceService } from "../../modules/browse/shared/services/implementations/BrowsePersistenceService";
import { OptionPickerDataService } from "../../modules/build/construct/option-picker/services/implementations/OptionPickerDataService";
import { OptionPickerLayoutService } from "../../modules/build/construct/option-picker/services/implementations/OptionPickerLayoutService";
import { ConstructCoordinator } from "../../modules/build/construct/shared/services/implementations/ConstructCoordinator";
import { StartPositionService } from "../../modules/build/construct/start-position-picker/services/implementations/StartPositionService";
import { CanvasManagementService } from "../../modules/build/export/services/implementations/CanvasManagementService";
import { DifficultyBadgeRenderer } from "../../modules/build/export/services/implementations/DifficultyBadgeRenderer";
import { DimensionCalculationService } from "../../modules/build/export/services/implementations/DimensionCalculationService";
import { ExportConfig } from "../../modules/build/export/services/implementations/ExportConfig";
import { ExportMemoryCalculator } from "../../modules/build/export/services/implementations/ExportMemoryCalculator";
import { ExportOptionsValidator } from "../../modules/build/export/services/implementations/ExportOptionsValidator";
import { FileExportService } from "../../modules/build/export/services/implementations/FileExportService";
import { FilenameGeneratorService } from "../../modules/build/export/services/implementations/FilenameGeneratorService";
import { GridOverlayService } from "../../modules/build/export/services/implementations/GridOverlayService";
import { ImageCompositionService } from "../../modules/build/export/services/implementations/ImageCompositionService";
import { ImageFormatConverterService } from "../../modules/build/export/services/implementations/ImageFormatConverterService";
import { ImagePreviewGenerator } from "../../modules/build/export/services/implementations/ImagePreviewGenerator";
import { LayoutCalculationService } from "../../modules/build/export/services/implementations/LayoutCalculationService";
import { ExportService } from "../../modules/build/export/services/implementations/SequenceExportService";
import { SVGToCanvasConverterService } from "../../modules/build/export/services/implementations/SVGToCanvasConverterService";
import { TextRenderingService } from "../../modules/build/export/services/implementations/TextRenderingService";
import { TextRenderingUtils } from "../../modules/build/export/services/implementations/TextRenderingUtils";
import { TKAImageExportService } from "../../modules/build/export/services/implementations/TKAImageExportService";
import { UserInfoRenderer } from "../../modules/build/export/services/implementations/UserInfoRenderer";
import { WordTextRenderer } from "../../modules/build/export/services/implementations/WordTextRenderer";
import { CSVPictographLoaderService } from "../../modules/build/generate/services/implementations/CSVPictographLoader";
import { CSVPictographParserService } from "../../modules/build/generate/services/implementations/CSVPictographParser";
import { PictographGenerator } from "../../modules/build/generate/services/implementations/PictographGenerator";
import { PositionPatternService } from "../../modules/build/generate/services/implementations/PositionPatternService";
import { SequenceDomainService } from "../../modules/build/generate/services/implementations/SequenceDomainService";
import { SequenceGenerationService } from "../../modules/build/generate/services/implementations/SequenceGenerationService";
import { BuildTabService } from "../../modules/build/shared/services/implementations/BuildTabService";
import {
  BeatFrameService,
  BeatRenderingService,
  PrintablePageLayoutService,
  SequenceDeletionService,
  SequenceImportService,
  SequenceIndexService,
  SequenceService,
  SequenceStateService,
  WorkbenchBeatOperationsService,
  WorkbenchCoordinationService,
  WorkbenchDeleteService,
  WorkbenchService,
} from "../../modules/build/workbench";
import { CodexService } from "../../modules/learn/codex/services/implementations";
import { CodexLetterMappingRepo } from "../../modules/learn/codex/services/implementations/CodexLetterMappingRepo";
import { CodexPictographUpdater } from "../../modules/learn/codex/services/implementations/CodexPictographUpdater";
import { QuizRepoManager } from "../../modules/learn/quiz/services/implementations/QuizRepoManager";
import { QuizSessionService } from "../../modules/learn/quiz/services/implementations/QuizSessionService";
import {
  ApplicationInitializer,
  BackgroundService,
  CsvLoader,
  CSVParser,
  DataTransformer,
  DeviceDetector,
  EnumMapper,
  ErrorHandlingService,
  GridModeDeriver,
  GridPositionDeriver,
  LetterDeriver,
  LetterQueryHandler,
  MotionQueryHandler,
  OptionFilterer,
  SettingsService,
} from "../foundation";
import {
  ArrowAdjustmentCalculator,
  ArrowCoordinateSystemService,
  ArrowLocationCalculator,
  ArrowLocationService,
  ArrowPathResolutionService,
  ArrowPlacementKeyService,
  ArrowPositionCalculator,
  ArrowPositioningService,
  ArrowRenderer,
  ArrowRotationCalculator,
  AttributeKeyGenerator,
  BeatFallbackRenderer,
  BeatGridService,
  BetaDetectionService,
  BetaOffsetCalculator,
  DashLocationCalculator,
  DefaultPlacementService,
  DirectionalTupleProcessor,
  GridRenderingService,
  OrientationCalculationService,
  OverlayRenderer,
  PictographValidatorService,
  PropCoordinator,
  PropPlacementService,
  SpecialPlacementOriKeyGenerator,
  SpecialPlacementService,
  SvgConfig,
  SvgUtilityService,
  TurnsTupleKeyGenerator,
} from "../pictograph/services";
import {
  DirectionalTupleCalculator,
  QuadrantIndexCalculator,
} from "../pictograph/services/implementations/positioning/processors/DirectionalTupleProcessor";
import { TYPES } from "./types";

// Create container
const container = new Container();

// Bind all required dependencies for CodexService
try {
  // Bind repositories
  container.bind(TYPES.ICodexLetterMappingRepo).to(CodexLetterMappingRepo);
  container.bind(TYPES.IQuizRepoManager).to(QuizRepoManager);
  container.bind(TYPES.IQuizSessionService).to(QuizSessionService);

  // Bind data services (dependencies of LetterQueryHandler)
  container.bind(TYPES.ICSVLoader).to(CsvLoader);
  container.bind(TYPES.ICSVParser).to(CSVParser);

  // Bind services
  container.bind(TYPES.ICodexPictographUpdater).to(CodexPictographUpdater);
  container.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);

  // Finally bind CodexService
  container.bind(TYPES.ICodexService).to(CodexService);

  // Bind application services
  container.bind(TYPES.ISettingsService).to(SettingsService);
  container.bind(TYPES.IPersistenceService).to(BrowsePersistenceService);
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
  container.bind(TYPES.IExportService).to(ExportService);
  container.bind(TYPES.IPageImageExportService).to(PageImageExportService);
  container.bind(TYPES.IGalleryThumbnailService).to(GalleryThumbnailService);

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
  container.bind(TYPES.IGalleryPanelManager).to(GalleryPanelManager);
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
  container.bind(TYPES.IDeleteService).to(WorkbenchDeleteService);
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
  container.bind(TYPES.IConstructTabCoordinator).to(ConstructCoordinator);
  container.bind(TYPES.IGalleryService).to(GalleryService);
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
  container.bind(TYPES.IGridPositionDeriver).to(GridPositionDeriver);
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

  // === STATE SERVICES ===
  // Note: These services use $state runes and should be bound as singletons
  // They will be imported and bound when needed
  // container.bind(TYPES.IAppStateInitializer).to(AppStateInitializer).inSingletonScope();
  // container.bind(TYPES.IApplicationStateService).to(ApplicationStateService).inSingletonScope();
  // container.bind(TYPES.IMainTabState).to(MainTabState).inSingletonScope();
  // container.bind(TYPES.IPerformanceMetricsState).to(PerformanceMetricsState).inSingletonScope();
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
