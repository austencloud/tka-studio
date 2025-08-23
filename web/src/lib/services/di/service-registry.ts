/**
 * Service Registry - String-based service interface mapping
 * Provides backward compatibility for string-based service resolution
 */

import type { ServiceInterface } from "./types";

// Import all service interfaces
import { IBeatFrameServiceInterface } from "./interfaces/beat-frame-interfaces";
import {
  IApplicationInitializationServiceInterface,
  // ✅ REMOVED: PropRenderingService is deprecated
  IArrowRenderingServiceInterface,
  IConstructTabCoordinationServiceInterface,
  IDeviceDetectionServiceInterface,
  IExportServiceInterface,
  IMotionGenerationServiceInterface,
  IPageFactoryServiceInterface,
  IPageImageExportServiceInterface,
  IPanelManagementServiceInterface,
  IPersistenceServiceInterface,
  IPictographRenderingServiceInterface,
  IPictographServiceInterface,
  IPrintablePageLayoutServiceInterface,
  ISequenceCardExportIntegrationServiceInterface,
  ISequenceDeletionServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceGenerationServiceInterface,
  ISequenceImportServiceInterface,
  ISequenceServiceInterface,
  ISettingsServiceInterface,
  IStartPositionSelectionServiceInterface,
  IStartPositionServiceInterface,
  IWorkbenchBeatOperationsServiceInterface,
} from "./interfaces/core-interfaces";
import { ISequenceStateServiceInterface } from "./interfaces/sequence-state-interfaces";
import {
  IWorkbenchCoordinationServiceInterface,
  IWorkbenchServiceInterface,
} from "./interfaces/workbench-interfaces";

import {
  IArrowAdjustmentCalculatorInterface,
  IArrowCoordinateSystemServiceInterface,
  IArrowLocationCalculatorInterface,
  IArrowPlacementKeyServiceInterface,
  IArrowPlacementServiceInterface,
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
  IAnimationStateServiceInterface,
  IBeatCalculationServiceInterface,
  IPropInterpolationServiceInterface,
  ISequenceAnimationEngineInterface,
  ISequenceAnimationOrchestratorInterface,
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
  ILessonRepositoryInterface,
  ILetterMappingRepositoryInterface,
  IPictographOperationsServiceInterface,
} from "./interfaces/codex-interfaces";

import { IOptionFilteringServiceInterface } from "./registration/shared-services";

import { getSequenceCardExportServiceTokens } from "./registration/sequence-card-export-services";

/**
 * Service interface mapping for string-based resolution
 * Maintains backward compatibility for existing code using string tokens
 */
export const serviceInterfaceMap = new Map<string, ServiceInterface<unknown>>([
  // Core services
  ["IBeatFrameService", IBeatFrameServiceInterface],
  ["ISequenceStateService", ISequenceStateServiceInterface],
  ["ISequenceService", ISequenceServiceInterface],
  ["IWorkbenchService", IWorkbenchServiceInterface],
  ["IWorkbenchCoordinationService", IWorkbenchCoordinationServiceInterface],
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

  // Sequence Card Export services
  ...getSequenceCardExportServiceTokens(),

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
