import { Container } from "inversify";
import { PageFactoryService, PageImageExportService } from "../../modules";
import {
  AnimationControlService,
  AnimationStateService,
  BeatCalculationService,
  MotionLetterIdentificationService,
  MotionParameterService,
  OverlayRenderer,
  PropInterpolationService,
  SequenceAnimationEngine,
  SequenceAnimationOrchestrator,
  SvgConfig,
  SvgUtilityService,
} from "../../modules/animator/services";
import { BrowseStatePersister } from "../../modules/browse/gallery/services/implementations/BrowseStatePersister";
import { FavoritesService } from "../../modules/browse/gallery/services/implementations/FavoritesService";
import { FilterPersistenceService } from "../../modules/browse/gallery/services/implementations/FilterPersistenceService";
import { GalleryPanelManager } from "../../modules/browse/gallery/services/implementations/GalleryPanelManager";
import { GalleryPersistenceService } from "../../modules/browse/gallery/services/implementations/GalleryPersistenceService";
import { BrowseSectionService } from "../../modules/browse/gallery/services/implementations/GallerySectionService";
import { GalleryService } from "../../modules/browse/gallery/services/implementations/GalleryService";
import { GalleryThumbnailService } from "../../modules/browse/gallery/services/implementations/GalleryThumbnailService";
import { NavigationService } from "../../modules/browse/gallery/services/implementations/NavigationService";
import { SequenceDeleteService } from "../../modules/browse/gallery/services/implementations/SequenceDeleteService";
import { OptionPickerDataService } from "../../modules/build/construct/option-picker/services/implementations/OptionPickerDataService";
import { OptionPickerLayoutService } from "../../modules/build/construct/option-picker/services/implementations/OptionPickerLayoutService";
import { OptionPickerServiceAdapter } from "../../modules/build/construct/option-picker/services/implementations/OptionPickerServiceAdapter";
import { StartPositionService } from "../../modules/build/construct/start-position-picker/services/implementations/StartPositionService";
import {
  ExportMemoryCalculator,
  ExportOptionsValidator,
  FilenameGeneratorService,
  ImagePreviewGenerator,
  TextRenderingService,
  TKAImageExportService
} from "../../modules/build/export/services/implementations";
import { CanvasManagementService } from "../../modules/build/export/services/implementations/CanvasManagementService";
import { DifficultyBadgeRenderer } from "../../modules/build/export/services/implementations/DifficultyBadgeRenderer";
import { DimensionCalculationService } from "../../modules/build/export/services/implementations/DimensionCalculationService";
import { ExportConfig } from "../../modules/build/export/services/implementations/ExportConfig";
import { FileExportService } from "../../modules/build/export/services/implementations/FileExportService";
import { GridOverlayService } from "../../modules/build/export/services/implementations/GridOverlayService";
import { ImageCompositionService } from "../../modules/build/export/services/implementations/ImageCompositionService";
import { ImageFormatConverterService } from "../../modules/build/export/services/implementations/ImageFormatConverterService";
import { LayoutCalculationService } from "../../modules/build/export/services/implementations/LayoutCalculationService";
import { SequenceExportService } from "../../modules/build/export/services/implementations/SequenceExportService";
import { SVGToCanvasConverterService } from "../../modules/build/export/services/implementations/SVGToCanvasConverterService";
import { TextRenderingUtils } from "../../modules/build/export/services/implementations/TextRenderingUtils";
import { UserInfoRenderer } from "../../modules/build/export/services/implementations/UserInfoRenderer";
import { WordTextRenderer } from "../../modules/build/export/services/implementations/WordTextRenderer";
import { CSVPictographLoaderService } from "../../modules/build/generate/services/implementations/CSVPictographLoader";
import { CSVPictographParser } from "../../modules/build/generate/services/implementations/CSVPictographParser";
import { PictographGenerator } from "../../modules/build/generate/services/implementations/PictographGenerator";
import { PositionPatternService } from "../../modules/build/generate/services/implementations/PositionPatternService";
import { SequenceDomainService } from "../../modules/build/generate/services/implementations/SequenceDomainService";
import { SequenceGenerationService } from "../../modules/build/generate/services/implementations/SequenceGenerationService";
import { BuildTabService } from "../../modules/build/shared/services/implementations/BuildTabService";
import { ConstructCoordinator } from "../../modules/build/shared/services/implementations/ConstructCoordinator";
import { BeatGridService } from "../../modules/build/workbench/sequence-display/services/implementations/BeatGridService";
import {
  BeatFallbackRenderer,
  SequenceImportService,
  SequenceIndexService,
  SequenceService,
  SequenceStateService,
  WorkbenchBeatOperationsService
} from "../../modules/build/workbench/shared/services";
import { WorkbenchCoordinationService } from "../../modules/build/workbench/shared/services/implementations/WorkbenchCoordinationService";
import { WorkbenchService } from "../../modules/build/workbench/shared/services/implementations/WorkbenchService";
import { PrintablePageLayoutService } from "../../modules/build/workbench/shared/services/PrintablePageLayoutService";
// Sequence toolkit services
import { BeatRenderingService } from "../../modules/build/export/services/implementations/BeatRenderingService";
import {
  SequenceDeletionService,
  SequenceTransformService
} from "../../modules/build/workbench/sequence-toolkit/services/implementations";
import { CodexService } from "../../modules/learn/codex/services/implementations";
import { CodexLetterMappingRepo } from "../../modules/learn/codex/services/implementations/CodexLetterMappingRepo";
import { CodexPictographUpdater } from "../../modules/learn/codex/services/implementations/CodexPictographUpdater";
import { QuizRepoManager } from "../../modules/learn/quiz/services/implementations/QuizRepoManager";
import { QuizSessionService } from "../../modules/learn/quiz/services/implementations/QuizSessionService";
import { WordCardBatchProcessingService } from "../../modules/word-card/services/implementations/WordCardBatchProcessingService";
import { WordCardCacheService } from "../../modules/word-card/services/implementations/WordCardCacheService";
import { WordCardExportOrchestrator } from "../../modules/word-card/services/implementations/WordCardExportOrchestrator";
import { WordCardExportProgressTracker } from "../../modules/word-card/services/implementations/WordCardExportProgressTracker";
import { WordCardImageConversionService } from "../../modules/word-card/services/implementations/WordCardImageConversionService";
import { WordCardImageGenerationService } from "../../modules/word-card/services/implementations/WordCardImageGenerationService";
import { WordCardMetadataOverlayService } from "../../modules/word-card/services/implementations/WordCardMetadataOverlayService";
import { WordCardSVGCompositionService } from "../../modules/word-card/services/implementations/WordCardSVGCompositionService";
import { ActService } from "../../modules/write/services/implementations/ActService";
import { MusicPlayerService } from "../../modules/write/services/implementations/MusicPlayerService";
import {
  ApplicationInitializer,
  ErrorHandlingService,
} from "../application/services/implementations";
import { BackgroundService } from "../background";
import { DeviceDetector } from "../device/services/implementations/DeviceDetector";
import {
  CsvLoader,
  CSVParser,
  DataTransformer,
  EnumMapper,
  // GridModeDeriver, // Service doesn't exist
  // GridPositionDeriver, // Service doesn't exist
  // LetterDeriver, // Service doesn't exist
  // LetterQueryHandler, // Service doesn't exist
  // MotionQueryHandler, // Service doesn't exist
  OptionFilterer,
} from "../foundation";
import { MotionQueryHandler } from "../pictograph/arrow/services/implementations/MotionQueryHandler";
import { PictographValidatorService } from "../pictograph/services";
import { LetterQueryHandler } from "../pictograph/tka-glyph/services/implementations/LetterQueryHandler";
// Grid services moved to grid module
import { GridModeDeriver, GridPositionDeriver, GridRenderingService } from "../pictograph/grid";
// Prop services moved to prop module
import {
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  QuadrantIndexCalculator,
} from "../pictograph/arrow/services/implementations/DirectionalTupleProcessor";
import { SettingsService } from "../settings/services/implementations/SettingsService";
import { TYPES } from "./types";
// Prop services moved to prop module
import { BetaDetectionService, BetaOffsetCalculator, PropCoordinator, PropPlacementService } from "../pictograph/prop";
// Arrow services moved to arrow module
import {
  ArrowAdjustmentCalculator,
  ArrowCoordinateSystemService,
  ArrowLocationCalculator,
  ArrowLocationService,
  ArrowPathResolutionService,
  ArrowPlacementKeyService,
  ArrowPlacementService,
  ArrowPositionCalculator,
  ArrowPositioningService,
  ArrowRenderer,
  ArrowRotationCalculator,
  DashLocationCalculator,
  DefaultPlacementService,
  SpecialPlacementService,
  TurnsTupleKeyGenerator
} from "../pictograph/arrow";
import { AttributeKeyGenerator } from "../pictograph/arrow/services/implementations/AttributeKeyGenerator";
import { SpecialPlacementOriKeyGenerator } from "../pictograph/arrow/services/implementations/SpecialPlacementOriKeyGenerator";
import { OrientationCalculationService } from "../pictograph/prop/services/implementations/OrientationCalculationService";

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
  // container.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler); // Service has invalid imports

  // Finally bind CodexService
  container.bind(TYPES.ICodexService).to(CodexService);

  // Bind application services
  container.bind(TYPES.ISettingsService).to(SettingsService);
  container.bind(TYPES.IPersistenceService).to(GalleryPersistenceService);
  container.bind(TYPES.IDeviceDetector).to(DeviceDetector);
  container.bind(TYPES.IApplicationInitializer).to(ApplicationInitializer);

  // Bind sequence services
  container.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
  container.bind(TYPES.ISequenceImportService).to(SequenceImportService);
  container.bind(TYPES.ISequenceService).to(SequenceService);
  container.bind(TYPES.ISequenceStateService).to(SequenceStateService);

  // Bind build tab services
  container.bind(TYPES.IBuildTabService).to(BuildTabService);

  // Bind write tab services
  container.bind(TYPES.IActService).to(ActService);
  container.bind(TYPES.IMusicPlayerService).to(MusicPlayerService);

  // Bind word card services
  container
    .bind(TYPES.IWordCardImageGenerationService)
    .to(WordCardImageGenerationService);
  container
    .bind(TYPES.IWordCardImageConversionService)
    .to(WordCardImageConversionService);
  container
    .bind(TYPES.IWordCardBatchProcessingService)
    .to(WordCardBatchProcessingService);
  container
    .bind(TYPES.IWordCardExportProgressTracker)
    .to(WordCardExportProgressTracker);
  container.bind(TYPES.IWordCardCacheService).to(WordCardCacheService);
  container
    .bind(TYPES.IWordCardExportOrchestrator)
    .to(WordCardExportOrchestrator);
  container
    .bind(TYPES.IWordCardSVGCompositionService)
    .to(WordCardSVGCompositionService);
  container
    .bind(TYPES.IWordCardMetadataOverlayService)
    .to(WordCardMetadataOverlayService);

  // Bind option picker services
  container
    .bind(TYPES.IOptionPickerLayoutService)
    .to(OptionPickerLayoutService);
  container.bind(TYPES.IOptionPickerDataService).to(OptionPickerDataService);
  container
    .bind(TYPES.IOptionPickerServiceAdapter)
    .to(OptionPickerServiceAdapter);

  // Bind layout services
  container.bind(TYPES.IBeatGridService).to(BeatGridService);

  // Bind workbench services
  container.bind(TYPES.IWorkbenchService).to(WorkbenchService);
  container
    .bind(TYPES.IWorkbenchCoordinationService)
    .to(WorkbenchCoordinationService);
  container
    .bind(TYPES.IWorkbenchBeatOperationsService)
    .to(WorkbenchBeatOperationsService);

  // Bind domain services (StartPositionService moved to unified service below)
  // container.bind(TYPES.IGridModeDeriver).to(GridModeDeriver); // Service doesn't exist

  // Bind rendering services
  container.bind(TYPES.IPropCoordinator).to(PropCoordinator);

  // Bind additional browse services
  container.bind(TYPES.IFavoritesService).to(FavoritesService);

  // Bind additional data services
  container.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService); // TODO: Restore when positioning directory is recreated
  container.bind(TYPES.IDataTransformer).to(DataTransformer);
  container.bind(TYPES.IEnumMapper).to(EnumMapper);
  container.bind(TYPES.IMotionQueryHandler).to(MotionQueryHandler);
  container.bind(TYPES.ILetterQueryHandler).to(LetterQueryHandler);
  container.bind(TYPES.IOptionFilterer).to(OptionFilterer);

  // Bind additional domain services
  // container.bind(TYPES.ILetterDeriver).to(LetterDeriver); // Service doesn't exist
  container
    .bind(TYPES.IPictographValidatorService)
    .to(PictographValidatorService);
  container.bind(TYPES.IPositionPatternService).to(PositionPatternService);

  // Bind export services
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
  container.bind(TYPES.IFileExportService).to(FileExportService);
  container.bind(TYPES.IGridOverlayService).to(GridOverlayService);
  container.bind(TYPES.IImageCompositionService).to(ImageCompositionService);
  container.bind(TYPES.ILayoutCalculationService).to(LayoutCalculationService);

  // Bind additional export services
  container.bind(TYPES.ITKAImageExportService).to(TKAImageExportService);
  container.bind(TYPES.ISequenceExportService).to(SequenceExportService);
  container.bind(TYPES.IExportMemoryCalculator).to(ExportMemoryCalculator);
  container.bind(TYPES.IExportOptionsValidator).to(ExportOptionsValidator);
  container.bind(TYPES.IFilenameGeneratorService).to(FilenameGeneratorService);
  container.bind(TYPES.IImagePreviewGenerator).to(ImagePreviewGenerator);
  container.bind(TYPES.ITextRenderingService).to(TextRenderingService);

  // Bind text rendering services
  container.bind(TYPES.IWordTextRenderer).to(WordTextRenderer);
  container.bind(TYPES.IUserInfoRenderer).to(UserInfoRenderer);
  container.bind(TYPES.IDifficultyBadgeRenderer).to(DifficultyBadgeRenderer);
  container.bind(TYPES.ITextRenderingUtils).to(TextRenderingUtils);

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
  // IBeatGridService already bound above (line 217)
  container.bind(TYPES.IGridRenderingService).to(GridRenderingService);
  container.bind(TYPES.IOverlayRenderer).to(OverlayRenderer);
  container.bind(TYPES.ISvgConfig).to(SvgConfig);
  container.bind(TYPES.ISvgUtilityService).to(SvgUtilityService);

  // Bind additional sequence services
  container.bind(TYPES.IDeleteService).to(SequenceDeleteService);
  container
    .bind(TYPES.IPrintablePageLayoutService)
    .to(PrintablePageLayoutService);
  container.bind(TYPES.ISequenceDeletionService).to(SequenceDeletionService);
  container.bind(TYPES.ISequenceTransformService).to(SequenceTransformService);
  container.bind(TYPES.ISequenceExportService).to(SequenceExportService);
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
  container.bind(TYPES.IGridModeDeriver).to(GridModeDeriver);
  container.bind(TYPES.IGridPositionDeriver).to(GridPositionDeriver);
  container
    .bind(TYPES.ICSVPictographParserService)
    .to(CSVPictographParser);
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
