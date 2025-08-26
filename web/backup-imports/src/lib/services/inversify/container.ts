/**
 * InversifyJS Container Configuration
 *
 * This file sets up the main InversifyJS container and provides
 * the service resolution interface for the TKA application.
 */

import { Container } from "inversify";
import "reflect-metadata";
import { TYPES } from "./types";

// Import service interfaces (these will be added as we convert services)
import type {
  IApplicationInitializationService,
  ISettingsService,
} from "../interfaces/application-interfaces";
import type { IThumbnailService } from "../interfaces/browse-interfaces";
import type { INavigationService } from "../interfaces/browse-interfaces";
import type { IBrowseService } from "../interfaces/browse-interfaces";
import type { IFavoritesService } from "../interfaces/browse-interfaces";
import type { ISequenceImportService } from "../interfaces/sequence-interfaces";
import type { IBeatFallbackRenderingService } from "../interfaces/beat-fallback-interfaces";
import type { IBeatFrameService } from "../interfaces/beat-frame-interfaces";
import type { IDeviceDetectionService } from "../interfaces/device-interfaces";
import type { IPositionMapper } from "../interfaces/movement/IPositionMapper";

// Import service implementations (these will be added as we convert services)
import { DeviceDetectionService } from "../implementations/application/DeviceDetectionService";
import { CSVParserService } from "../implementations/data/CSVParserService";
import { DataTransformationService } from "../implementations/data/DataTransformationService";
import { EnumMappingService } from "../implementations/data/EnumMappingService";
import { GridModeDeriver } from "../implementations/domain/GridModeDeriver";
import { LetterDeriver } from "../implementations/domain/LetterDeriver";
import { PictographValidatorService } from "../implementations/domain/PictographValidatorService";
import { PositionPatternService } from "../implementations/domain/PositionPatternService";
import { FilenameGeneratorService } from "../implementations/image-export/FilenameGeneratorService";
import { SettingsService } from "../implementations/persistence/SettingsService";
import { ArrowPositioningService } from "../implementations/positioning/ArrowPositioningService";
import { SvgConfiguration } from "../implementations/rendering/SvgConfiguration";
import { ArrowAdjustmentCalculator } from "../positioning/arrows/calculation/ArrowAdjustmentCalculator";
// Import interfaces from implementation files (they're defined there)
import { ApplicationInitializationService } from "../implementations/application/ApplicationInitializationService";
import type { ICsvLoaderService } from "../implementations/data/CsvLoaderService";
import { CsvLoaderService } from "../implementations/data/CsvLoaderService";
import type { ICSVParserService } from "../implementations/data/CSVParserService";
import type { IDataTransformationService } from "../implementations/data/DataTransformationService";
import type { IEnumMappingService } from "../implementations/data/EnumMappingService";
import type { ILetterDeriver } from "../implementations/domain/LetterDeriver";
import { SequenceDomainService } from "../implementations/domain/SequenceDomainService";
import { StartPositionService } from "../implementations/domain/StartPositionService";
import { DimensionCalculationService } from "../implementations/image-export/DimensionCalculationService";
import { ExportConfigurationManager } from "../implementations/image-export/ExportConfigurationManager";
import { ExportMemoryCalculator } from "../implementations/image-export/ExportMemoryCalculator";
import { ExportOptionsValidator } from "../implementations/image-export/ExportOptionsValidator";
import { LayoutCalculationService } from "../implementations/image-export/LayoutCalculationService";
import { BeatFrameService } from "../implementations/layout/BeatFrameService";
import { PositionMapper } from "../implementations/movement/PositionMapper";
import type { IFilterPersistenceService } from "../implementations/persistence/FilterPersistenceService";
import { FilterPersistenceService } from "../implementations/persistence/FilterPersistenceService";
import { LocalStoragePersistenceService } from "../implementations/persistence/LocalStoragePersistenceService";
import { BeatFallbackRenderingService } from "../implementations/rendering/BeatFallbackRenderingService";
// TODO: BetaOffsetCalculator and OrientationCalculationService don't have interfaces defined
// import { BetaOffsetCalculator } from "../implementations/positioning/BetaOffsetCalculator";
// import { OrientationCalculationService } from "../implementations/positioning/OrientationCalculationService";
import { ArrowRenderingService } from "../implementations/rendering/ArrowRenderingService";
import { BeatGridService } from "../implementations/rendering/BeatGridService";
import { GridRenderingService } from "../implementations/rendering/GridRenderingService";
import { OverlayRenderingService } from "../implementations/rendering/OverlayRenderingService";
import type { ISvgConfiguration } from "../implementations/rendering/SvgConfiguration";
import type { ISvgUtilityService } from "../implementations/rendering/SvgUtilityService";
import { SvgUtilityService } from "../implementations/rendering/SvgUtilityService";
import type { IStartPositionService } from "../interfaces/application-interfaces";
import type { IBeatGridService } from "../interfaces/beat-grid-interfaces";
import type {
  IPictographValidatorService,
  IPositionPatternService,
} from "../interfaces/generation-interfaces";
import type {
  IDimensionCalculationService,
  IExportConfigurationManager,
  IExportMemoryCalculator,
  IExportOptionsValidator,
  IFilenameGeneratorService,
  ILayoutCalculationService,
} from "../interfaces/image-export-interfaces";
import type { IGridModeDeriver } from "../interfaces/movement/IGridModeDeriver";
import type {
  IArrowRenderingService,
  IGridRenderingService,
  IOverlayRenderingService,
} from "../interfaces/pictograph-interfaces";
import type { IArrowPositioningService } from "../interfaces/positioning-interfaces";
import type {
  IPersistenceService,
  ISequenceDomainService,
} from "../interfaces/sequence-interfaces";
import type { IArrowAdjustmentCalculator } from "../positioning/core-services";
import { SequenceImportService } from "../implementations/sequence/SequenceImportService.ts";
import { ThumbnailService } from "../implementations/export/ThumbnailService.ts";
import { NavigationService } from "../implementations/navigation/NavigationService.ts";
import { BrowseService } from "../implementations/browse/BrowseService.ts";
import { FavoritesService } from "../implementations/browse/FavoritesService.ts";

/**
 * Create and configure the InversifyJS container
 */
function createContainer(): Container {
  const container = new Container({
    defaultScope: "Singleton", // Most TKA services are singletons
  });

  // Bind converted services
  container.bind<ISettingsService>(TYPES.ISettingsService).to(SettingsService);
  container
    .bind<IEnumMappingService>(TYPES.IEnumMappingService)
    .to(EnumMappingService);
  container
    .bind<ICSVParserService>(TYPES.ICSVParsingService)
    .to(CSVParserService);
  container
    .bind<IDataTransformationService>(TYPES.IDataTransformationService)
    .to(DataTransformationService);
  // TODO: LetterQueryService and MotionQueryService have dependencies - convert later
  // container
  //   .bind<ILetterQueryService>(TYPES.ILetterQueryService)
  //   .to(LetterQueryService);
  // container
  //   .bind<IMotionQueryService>(TYPES.IMotionQueryService)
  //   .to(MotionQueryService);
  container.bind<IGridModeDeriver>(TYPES.IGridModeDeriver).to(GridModeDeriver);
  container.bind<ILetterDeriver>(TYPES.ILetterDeriver).to(LetterDeriver);
  container
    .bind<IPictographValidatorService>(TYPES.IPictographValidatorService)
    .to(PictographValidatorService);
  container
    .bind<IPositionPatternService>(TYPES.IPositionPatternService)
    .to(PositionPatternService);
  container
    .bind<ISvgConfiguration>(TYPES.ISvgConfiguration)
    .to(SvgConfiguration);
  container
    .bind<IFilenameGeneratorService>(TYPES.IFilenameGeneratorService)
    .to(FilenameGeneratorService);
  // TODO: ExportOptionsValidator has dependencies - convert later
  // container
  //   .bind<IExportOptionsValidator>(TYPES.IExportOptionsValidator)
  //   .to(ExportOptionsValidator);
  container
    .bind<IDeviceDetectionService>(TYPES.IDeviceDetectionService)
    .to(DeviceDetectionService);

  container
    .bind<IPersistenceService>(TYPES.IPersistenceService)
    .to(LocalStoragePersistenceService);
  container
    .bind<ISequenceDomainService>(TYPES.ISequenceDomainService)
    .to(SequenceDomainService);
  container
    .bind<IStartPositionService>(TYPES.IStartPositionService)
    .to(StartPositionService);
  container
    .bind<IArrowAdjustmentCalculator>(TYPES.IArrowAdjustmentCalculator)
    .toDynamicValue(() => {
      const gridModeService = container.get<IGridModeDeriver>(
        TYPES.IGridModeDeriver
      );
      return new ArrowAdjustmentCalculator(gridModeService);
    });

  // TODO: PictographService has dependencies - convert later
  // container
  //   .bind<IPictographService>(TYPES.IPictographService)
  //   .to(PictographService);
  container
    .bind<ISvgUtilityService>(TYPES.ISvgUtilityService)
    .to(SvgUtilityService);

  container
    .bind<IGridRenderingService>(TYPES.IGridRenderingService)
    .to(GridRenderingService);
  container
    .bind<IArrowRenderingService>(TYPES.IArrowRenderingService)
    .to(ArrowRenderingService);
  container
    .bind<IOverlayRenderingService>(TYPES.IOverlayRenderingService)
    .to(OverlayRenderingService);
  container
    .bind<IFilterPersistenceService>(TYPES.IFilterPersistenceService)
    .to(FilterPersistenceService);
  container
    .bind<IApplicationInitializationService>(
      TYPES.IApplicationInitializationService
    )
    .to(ApplicationInitializationService);

  // TODO: PictographRenderingService has unconverted dependencies - convert later
  // container
  //   .bind<IPictographRenderingService>(TYPES.IPictographRenderingService)
  //   .to(PictographRenderingService);
  container
    .bind<IExportMemoryCalculator>(TYPES.IExportMemoryCalculator)
    .to(ExportMemoryCalculator);
  container
    .bind<IExportOptionsValidator>(TYPES.IExportOptionsValidator)
    .to(ExportOptionsValidator);
  container
    .bind<ICsvLoaderService>(TYPES.ICsvLoaderService)
    .to(CsvLoaderService);
  container.bind<IBeatGridService>(TYPES.IBeatGridService).to(BeatGridService);
  container
    .bind<IExportConfigurationManager>(TYPES.IExportConfigurationManager)
    .to(ExportConfigurationManager);

  container
    .bind<IDimensionCalculationService>(TYPES.IDimensionCalculationService)
    .to(DimensionCalculationService);
  container
    .bind<ILayoutCalculationService>(TYPES.ILayoutCalculationService)
    .to(LayoutCalculationService);
  container
    .bind<IBeatFrameService>(TYPES.IBeatFrameService)
    .to(BeatFrameService);
  container
    .bind<IBeatFallbackRenderingService>(TYPES.IBeatFallbackRenderingService)
    .to(BeatFallbackRenderingService);
  container.bind<IPositionMapper>(TYPES.IPositionMapper).to(PositionMapper);
  container
    .bind<IArrowPositioningService>(TYPES.IArrowPositioningService)
    .to(ArrowPositioningService);
  // TODO: Add bindings for BetaOffsetCalculator and OrientationCalculationService when interfaces are defined

    container.bind<ISequenceImportService>(TYPES.ISequenceImportService).to(SequenceImportService);

    container.bind<IThumbnailService>(TYPES.IThumbnailService).to(ThumbnailService);
  container.bind<INavigationService>(TYPES.INavigationService).to(NavigationService);
  container.bind<IBrowseService>(TYPES.IBrowseService).to(BrowseService);
  container.bind<IFavoritesService>(TYPES.IFavoritesService).to(FavoritesService);

  return container;
}

// Create the global container instance
export const container = createContainer();

/**
 * Resolve a service from the container
 * This replaces the old resolve() function from bootstrap.ts
 */
export function resolve<T>(serviceType: symbol): T {
  try {
    return container.get<T>(serviceType);
  } catch (error) {
    console.error(`❌ Failed to resolve service:`, serviceType.toString());
    console.error(`❌ Error:`, error);

    // Log available services for debugging
    const bindings = container.getAll(serviceType);
    console.error(
      `❌ Available bindings for ${serviceType.toString()}:`,
      bindings.length
    );

    throw error;
  }
}

/**
 * Check if a service is bound in the container
 */
export function isBound(serviceType: symbol): boolean {
  return container.isBound(serviceType);
}

/**
 * Get container debug information
 */
export function getContainerDebugInfo(): {
  boundServices: string[];
  serviceCount: number;
} {
  // Get all bound service identifiers
  const boundServices: string[] = [];

  // InversifyJS doesn't provide a direct way to get all bindings,
  // so we'll check our known types
  Object.entries(TYPES).forEach(([name, symbol]) => {
    if (container.isBound(symbol)) {
      boundServices.push(name);
    }
  });

  return {
    boundServices,
    serviceCount: boundServices.length,
  };
}

/**
 * Validate container configuration
 * This helps ensure all expected services are properly bound
 */
export function validateContainer(): {
  isValid: boolean;
  missingServices: string[];
  boundServices: string[];
} {
  const missingServices: string[] = [];
  const boundServices: string[] = [];

  Object.entries(TYPES).forEach(([name, symbol]) => {
    if (container.isBound(symbol)) {
      boundServices.push(name);
    } else {
      missingServices.push(name);
    }
  });

  return {
    isValid: missingServices.length === 0,
    missingServices,
    boundServices,
  };
}

// Export the container for direct access when needed
export { container as inversifyContainer };

// Export types for convenience
export { TYPES } from "./types";
