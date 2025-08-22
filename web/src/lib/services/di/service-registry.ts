/**
 * Service Registry - String-based service interface mapping
 * Provides backward compatibility for string-based service resolution
 */

import type { ServiceInterface } from "./types";

// Import all service interfaces
import {
  IApplicationInitializationServiceInterface,
  IConstructTabCoordinationServiceInterface,
  IDeviceDetectionServiceInterface,
  IExportServiceInterface,
  IMotionGenerationServiceInterface,
  IPanelManagementServiceInterface,
  IPersistenceServiceInterface,
  IPictographRenderingServiceInterface,
  IPictographServiceInterface,
  // ✅ REMOVED: PropRenderingService is deprecated
  IArrowRenderingServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceGenerationServiceInterface,
  ISequenceServiceInterface,
  IWorkbenchBeatOperationsServiceInterface,
  ISequenceImportServiceInterface,
  ISequenceDeletionServiceInterface,
  ISettingsServiceInterface,
  IStartPositionServiceInterface,
  IPrintablePageLayoutServiceInterface,
  IPageFactoryServiceInterface,
  IPageImageExportServiceInterface,
  ISequenceCardExportIntegrationServiceInterface,
  IStartPositionSelectionServiceInterface,
} from "./interfaces/core-interfaces";

import {
  IArrowAdjustmentCalculatorInterface,
  IArrowCoordinateSystemServiceInterface,
  IArrowLocationCalculatorInterface,
  IArrowPlacementServiceInterface,
  IArrowPlacementKeyServiceInterface,
  IArrowPositioningOrchestratorInterface,
  IArrowRotationCalculatorInterface,
  IDashLocationCalculatorInterface,
  IDirectionalTupleProcessorInterface,
  IPositioningServiceFactoryInterface,
} from "./interfaces/positioning-interfaces";

import {
  IBrowseServiceInterface,
  IDeleteServiceInterface,
  IFavoritesServiceInterface,
  IFilterPersistenceServiceInterface,
  INavigationServiceInterface,
  ISectionServiceInterface,
  ISequenceIndexServiceInterface,
  IThumbnailServiceInterface,
} from "./interfaces/browse-interfaces";

import {
  IBeatCalculationServiceInterface,
  IPropInterpolationServiceInterface,
  IAnimationStateServiceInterface,
  ISequenceAnimationOrchestratorInterface,
  ISequenceAnimationEngineInterface,
} from "./interfaces/animator-interfaces";

// TODO: Uncomment when image export interfaces are implemented
// import {
//   ITKAImageExportServiceInterface,
//   ILayoutCalculationServiceInterface,
//   IDimensionCalculationServiceInterface,
//   IFileExportServiceInterface,
//   IBeatRenderingServiceInterface,
//   ITextRenderingServiceInterface,
//   IImageCompositionServiceInterface,
//   IGridOverlayServiceInterface,
//   ICanvasManagementServiceInterface,
// } from "./interfaces/image-export-interfaces";

import {
  ICodexServiceInterface,
  ILetterMappingRepositoryInterface,
  ILessonRepositoryInterface,
  IPictographOperationsServiceInterface,
} from "./interfaces/codex-interfaces";

import { IOptionFilteringServiceInterface } from "./registration/shared-services";

/**
 * Service interface mapping for string-based resolution
 * Maintains backward compatibility for existing code using string tokens
 */
export const serviceInterfaceMap = new Map<string, ServiceInterface<unknown>>([
  // Core services
  ["ISequenceService", ISequenceServiceInterface],
  ["IWorkbenchBeatOperationsService", IWorkbenchBeatOperationsServiceInterface],
  ["ISequenceImportService", ISequenceImportServiceInterface],
  ["ISequenceDeletionService", ISequenceDeletionServiceInterface],
  ["ISequenceDomainService", ISequenceDomainServiceInterface],
  ["IPictographService", IPictographServiceInterface],
  ["IPictographRenderingService", IPictographRenderingServiceInterface],
  // ✅ REMOVED: PropRenderingService is deprecated
  ["IArrowRenderingService", IArrowRenderingServiceInterface],
  ["IPersistenceService", IPersistenceServiceInterface],
  ["ISettingsService", ISettingsServiceInterface],
  ["IDeviceDetectionService", IDeviceDetectionServiceInterface],
  [
    "IApplicationInitializationService",
    IApplicationInitializationServiceInterface,
  ],
  ["IExportService", IExportServiceInterface],
  ["IMotionGenerationService", IMotionGenerationServiceInterface],
  ["ISequenceGenerationService", ISequenceGenerationServiceInterface],
  [
    "IConstructTabCoordinationService",
    IConstructTabCoordinationServiceInterface,
  ],

  ["IStartPositionService", IStartPositionServiceInterface],
  ["IStartPositionSelectionService", IStartPositionSelectionServiceInterface],
  ["IPanelManagementService", IPanelManagementServiceInterface],
  ["IPrintablePageLayoutService", IPrintablePageLayoutServiceInterface],
  ["IPageFactoryService", IPageFactoryServiceInterface],
  ["IPageImageExportService", IPageImageExportServiceInterface],
  [
    "ISequenceCardExportIntegrationService",
    ISequenceCardExportIntegrationServiceInterface,
  ],

  // Positioning services
  ["IArrowPositioningOrchestrator", IArrowPositioningOrchestratorInterface],
  ["IArrowPlacementService", IArrowPlacementServiceInterface],
  ["IArrowPlacementKeyService", IArrowPlacementKeyServiceInterface],
  ["IArrowLocationCalculator", IArrowLocationCalculatorInterface],
  ["IArrowRotationCalculator", IArrowRotationCalculatorInterface],
  ["IArrowAdjustmentCalculator", IArrowAdjustmentCalculatorInterface],
  ["IArrowCoordinateSystemService", IArrowCoordinateSystemServiceInterface],
  ["IDashLocationCalculator", IDashLocationCalculatorInterface],
  ["IDirectionalTupleProcessor", IDirectionalTupleProcessorInterface],
  ["IArrowPositioningOrchestrator", IArrowPositioningOrchestratorInterface],
  ["IPositioningServiceFactory", IPositioningServiceFactoryInterface],

  // Browse services
  ["IBrowseService", IBrowseServiceInterface],
  ["IThumbnailService", IThumbnailServiceInterface],
  ["ISequenceIndexService", ISequenceIndexServiceInterface],
  ["IFavoritesService", IFavoritesServiceInterface],
  ["INavigationService", INavigationServiceInterface],
  ["ISectionService", ISectionServiceInterface],
  ["IFilterPersistenceService", IFilterPersistenceServiceInterface],
  ["IDeleteService", IDeleteServiceInterface],

  // Animator services
  ["IBeatCalculationService", IBeatCalculationServiceInterface],
  ["IPropInterpolationService", IPropInterpolationServiceInterface],
  ["IAnimationStateService", IAnimationStateServiceInterface],
  ["ISequenceAnimationOrchestrator", ISequenceAnimationOrchestratorInterface],
  ["ISequenceAnimationEngine", ISequenceAnimationEngineInterface],

  // Codex services
  ["ICodexService", ICodexServiceInterface],
  ["ILetterMappingRepository", ILetterMappingRepositoryInterface],
  ["ILessonRepository", ILessonRepositoryInterface],

  ["IPictographOperationsService", IPictographOperationsServiceInterface],

  // Shared utility services
  ["IOptionFilteringService", IOptionFilteringServiceInterface],

  // TODO: Uncomment when TKA Image Export services are implemented
  // ["ITKAImageExportService", ITKAImageExportServiceInterface],
  // ["ILayoutCalculationService", ILayoutCalculationServiceInterface],
  // ["IDimensionCalculationService", IDimensionCalculationServiceInterface],
  // ["IFileExportService", IFileExportServiceInterface],
  // ["IBeatRenderingService", IBeatRenderingServiceInterface],
  // ["ITextRenderingService", ITextRenderingServiceInterface],
  // ["IImageCompositionService", IImageCompositionServiceInterface],
  // ["IGridOverlayService", IGridOverlayServiceInterface],
  // ["ICanvasManagementService", ICanvasManagementServiceInterface],
]);
