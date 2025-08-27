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
import { CodexService } from "../codex/CodexService";
import { LetterMappingRepository } from "../../repositories/LetterMappingRepository";
import { LessonRepository } from "../../repositories/LessonRepository";
import { PictographOperationsService } from "../codex/PictographOperationsService";
import { LetterQueryService } from "../implementations/data/LetterQueryService";
import { CsvLoaderService } from "../implementations/data/CsvLoaderService";
import { CSVParserService } from "../implementations/data/CSVParserService";

// Import application services
import { ApplicationInitializationService } from "../implementations/application/ApplicationInitializationService";
import { DeviceDetectionService } from "../implementations/application/DeviceDetectionService";
import { SettingsService } from "../implementations/persistence/SettingsService";
import { LocalStoragePersistenceService } from "../implementations/persistence/LocalStoragePersistenceService";

// Import sequence services
import { SequenceService } from "../implementations/sequence/SequenceService";
import { SequenceDomainService } from "../implementations/domain/SequenceDomainService";
import { SequenceImportService } from "../implementations/sequence/SequenceImportService";
import { SequenceStateService } from "../implementations/sequence/SequenceStateService";

// Import layout services
import { BeatFrameService } from "../implementations/layout/BeatFrameService";

// Import workbench services
import { WorkbenchService } from "../implementations/workbench/WorkbenchService";
import { WorkbenchCoordinationService } from "../implementations/workbench/WorkbenchCoordinationService";

// Import domain services
import { StartPositionService } from "../implementations/domain/StartPositionService";
import { GridModeDeriver } from "../implementations/domain/GridModeDeriver";

// Import rendering services
import { PropCoordinatorService } from "../implementations/rendering/PropCoordinatorService";

// Import browse services
import { BrowseService } from "../implementations/browse/BrowseService";
import { FavoritesService } from "../implementations/browse/FavoritesService";

// Import additional data services
import { ArrowPlacementService } from "../implementations/data/ArrowPlacementService";
import { DataTransformationService } from "../implementations/data/DataTransformationService";
import { EnumMappingService } from "../implementations/data/EnumMappingService";
import { MotionQueryService } from "../implementations/data/MotionQueryService";
import { OptionFilteringService } from "../implementations/data/OptionFilteringService";
import { ExampleSequenceService } from "../implementations/data/PictographTransformationService";

// Import additional domain services
import { LetterDeriver } from "../implementations/domain/LetterDeriver";
import { PictographValidatorService } from "../implementations/domain/PictographValidatorService";
import { PositionPatternService } from "../implementations/domain/PositionPatternService";

// Import export services
import { ExportService } from "../implementations/export/ExportService";
import { PageImageExportService } from "../implementations/export/PageImageExportService";
import { ThumbnailService } from "../implementations/export/ThumbnailService";

// Import generation services
import { PageFactoryService } from "../implementations/generation/PageFactoryService";
import { PictographGenerator } from "../implementations/generation/PictographGenerator";
import { SequenceGenerationService } from "../implementations/generation/SequenceGenerationService";

// Import background services
import { BackgroundService } from "../implementations/background/BackgroundService";

// Import image export services
import { BeatRenderingService } from "../implementations/image-export/BeatRenderingService";
import { CanvasManagementService } from "../implementations/image-export/CanvasManagementService";
import { ExportConfigurationManager } from "../implementations/image-export/ExportConfigurationManager";
import { ExportMemoryCalculator } from "../implementations/image-export/ExportMemoryCalculator";
import { ExportOptionsValidator } from "../implementations/image-export/ExportOptionsValidator";
import { FileExportService } from "../implementations/image-export/FileExportService";
import { FilenameGeneratorService } from "../implementations/image-export/FilenameGeneratorService";
import { GridOverlayService } from "../implementations/image-export/GridOverlayService";
import { ImageCompositionService } from "../implementations/image-export/ImageCompositionService";
import { ImagePreviewGenerator } from "../implementations/image-export/ImagePreviewGenerator";
import { LayoutCalculationService } from "../implementations/image-export/LayoutCalculationService";
import { TKAImageExportService } from "../implementations/image-export/TKAImageExportService";

// Import navigation services
import { NavigationService } from "../implementations/navigation/NavigationService";
import { PanelManagementService } from "../implementations/navigation/PanelManagementService";
import { SectionService } from "../implementations/navigation/SectionService";

// Import additional persistence services
import { FilterPersistenceService } from "../implementations/persistence/FilterPersistenceService";

// Import positioning services
import { ArrowLocationService } from "../implementations/positioning/ArrowLocationService";
import { ArrowPlacementKeyService } from "../implementations/positioning/ArrowPlacementKeyService";
import { ArrowPositioningService } from "../implementations/positioning/ArrowPositioningService";
import { BetaOffsetCalculator } from "../implementations/positioning/BetaOffsetCalculator";
import { PropPlacementService } from "../implementations/positioning/PropPlacementService";

// Import additional rendering services
import { ArrowRenderingService } from "../implementations/rendering/ArrowRenderingService";
import { BeatGridService } from "../implementations/rendering/BeatGridService";
import { GridRenderingService } from "../implementations/rendering/GridRenderingService";
import { OverlayRenderingService } from "../implementations/rendering/OverlayRenderingService";
import { SvgConfiguration } from "../implementations/rendering/SvgConfiguration";
import { SvgUtilityService } from "../implementations/rendering/SvgUtilityService";

// Import additional sequence services
import { DeleteService } from "../implementations/sequence/DeleteService";
import { PrintablePageLayoutService } from "../implementations/sequence/PrintablePageLayoutService";
import { SequenceDeletionService } from "../implementations/sequence/SequenceDeletionService";
import { SequenceIndexService } from "../implementations/sequence/SequenceIndexService";

// Import motion tester services
import { AnimationControlService } from "../implementations/motion-tester/AnimationControlService";
import { MotionParameterService } from "../implementations/motion-tester/MotionParameterService";

// Import movement services
import { CSVPictographLoaderService } from "../implementations/movement/CSVPictographLoaderService";

// Import missing construct services (these exist)
import { ConstructTabCoordinationService } from "../implementations/construct/ConstructTabCoordinationService";

// Additional services will be added as needed

// Import missing services that have confirmed implementations
import { ArrowPositionCalculator } from "../positioning/arrows/orchestration/ArrowPositionCalculator";
import { ArrowAdjustmentCalculator } from "../positioning/arrows/calculation/ArrowAdjustmentCalculator";
import { OrientationCalculationService } from "../implementations/positioning/OrientationCalculationService";
import { MotionLetterIdentificationService } from "../implementations/motion-tester/MotionLetterIdentificationService";
import { ArrowPathResolutionService } from "../implementations/rendering/arrow/ArrowPathResolutionService";

// Import additional services with confirmed implementations
import { PositionMapper } from "../implementations/movement/PositionMapper";
import { SequenceAnimationEngine } from "../../animator/core/engine/sequence-animation-engine";
import { SequenceAnimationOrchestrator } from "../../animator/core/services/SequenceAnimationOrchestrator";
import { AnimationStateService } from "../../animator/core/services/AnimationStateService";
import { BeatCalculationService } from "../../animator/core/services/BeatCalculationService";
import { PropInterpolationService } from "../../animator/core/services/PropInterpolationService";
// ValidationService is defined as interface in PictographTransformationService but no implementation found

// Import additional services with confirmed implementations
import { DimensionCalculationService } from "../implementations/image-export/DimensionCalculationService";
import { ImageFormatConverterService } from "../implementations/conversion/ImageFormatConverterService";
import { SVGToCanvasConverterService } from "../implementations/conversion/SVGToCanvasConverterService";

console.log("✅ TKA Container: Initializing dependency injection container");

// Create container
const container = new Container();

// Bind all required dependencies for CodexService
try {
  // Bind repositories
  container.bind(TYPES.ILetterMappingRepository).to(LetterMappingRepository);
  container.bind(TYPES.ILessonRepository).to(LessonRepository);

  // Bind data services (dependencies of LetterQueryService)
  container.bind(TYPES.ICsvLoaderService).to(CsvLoaderService);
  container.bind(TYPES.ICSVParsingService).to(CSVParserService);

  // Bind services
  container
    .bind(TYPES.IPictographOperationsService)
    .to(PictographOperationsService);
  container.bind(TYPES.ILetterQueryService).to(LetterQueryService);

  // Finally bind CodexService
  container.bind(TYPES.ICodexService).to(CodexService);

  // Bind application services
  container.bind(TYPES.ISettingsService).to(SettingsService);
  container.bind(TYPES.IPersistenceService).to(LocalStoragePersistenceService);
  container.bind(TYPES.IDeviceDetectionService).to(DeviceDetectionService);
  container
    .bind(TYPES.IApplicationInitializationService)
    .to(ApplicationInitializationService);

  // Bind sequence services
  container.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
  container.bind(TYPES.ISequenceImportService).to(SequenceImportService);
  container.bind(TYPES.ISequenceService).to(SequenceService);
  container.bind(TYPES.ISequenceStateService).to(SequenceStateService);

  // Bind layout services
  container.bind(TYPES.IBeatFrameService).to(BeatFrameService);

  // Bind workbench services
  container.bind(TYPES.IWorkbenchService).to(WorkbenchService);
  container
    .bind(TYPES.IWorkbenchCoordinationService)
    .to(WorkbenchCoordinationService);

  // Bind domain services
  container.bind(TYPES.IStartPositionService).to(StartPositionService);
  container.bind(TYPES.IGridModeDeriver).to(GridModeDeriver);

  // Bind rendering services
  container.bind(TYPES.IPropCoordinatorService).to(PropCoordinatorService);

  // Bind additional browse services
  container.bind(TYPES.IFavoritesService).to(FavoritesService);

  // Bind additional data services
  container.bind(TYPES.IArrowPlacementService).to(ArrowPlacementService);
  container
    .bind(TYPES.IDataTransformationService)
    .to(DataTransformationService);
  container.bind(TYPES.IEnumMappingService).to(EnumMappingService);
  container.bind(TYPES.IMotionQueryService).to(MotionQueryService);
  container.bind(TYPES.IOptionFilteringService).to(OptionFilteringService);
  container.bind(TYPES.IExampleSequenceService).to(ExampleSequenceService);

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
  // container.bind(TYPES.ITextRenderingService).to(TextRenderingService); // TODO: Add to TYPES
  container.bind(TYPES.ITKAImageExportService).to(TKAImageExportService);

  // Bind navigation services
  container.bind(TYPES.INavigationService).to(NavigationService);
  container.bind(TYPES.IPanelManagementService).to(PanelManagementService);
  container.bind(TYPES.ISectionService).to(SectionService);

  // Bind additional persistence services
  container.bind(TYPES.IFilterPersistenceService).to(FilterPersistenceService);

  // Bind positioning services
  container.bind(TYPES.IArrowLocationService).to(ArrowLocationService);
  container.bind(TYPES.IArrowPlacementKeyService).to(ArrowPlacementKeyService);
  container.bind(TYPES.IArrowPositioningService).to(ArrowPositioningService);
  container.bind(TYPES.IBetaOffsetCalculator).to(BetaOffsetCalculator);
  container.bind(TYPES.IPropPlacementService).to(PropPlacementService);

  // Bind additional rendering services
  container.bind(TYPES.IArrowRenderingService).to(ArrowRenderingService);
  container.bind(TYPES.IBeatGridService).to(BeatGridService);
  container.bind(TYPES.IGridRenderingService).to(GridRenderingService);
  container.bind(TYPES.IOverlayRenderingService).to(OverlayRenderingService);
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
    .bind(TYPES.IConstructTabCoordinationService)
    .to(ConstructTabCoordinationService);
  container.bind(TYPES.IBrowseService).to(BrowseService);
  container.bind(TYPES.ICSVParserService).to(CSVParserService);
  container
    .bind(TYPES.IArrowPositioningOrchestrator)
    .to(ArrowPositionCalculator);
  container
    .bind(TYPES.IArrowAdjustmentCalculator)
    .to(ArrowAdjustmentCalculator);
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

  console.log("✅ TKA Container: All available services bound successfully");
  console.log(
    `📊 Container initialized with ${Object.keys(TYPES).length} service types defined`
  );
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

console.log("✅ TKA Container: Dependency injection setup complete");
