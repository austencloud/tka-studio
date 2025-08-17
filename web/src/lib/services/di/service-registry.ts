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
  IOptionDataServiceInterface,
  IPanelManagementServiceInterface,
  IPersistenceServiceInterface,
  IPictographRenderingServiceInterface,
  IPictographServiceInterface,
  IPropRenderingServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceGenerationServiceInterface,
  ISequenceServiceInterface,
  ISettingsServiceInterface,
  IStartPositionServiceInterface,
  IPrintablePageLayoutServiceInterface,
  IPageFactoryServiceInterface,
  IPageImageExportServiceInterface,
  ISequenceCardExportIntegrationServiceInterface,
} from "./interfaces/core-interfaces";

import {
  IArrowAdjustmentCalculatorInterface,
  IArrowCoordinateSystemServiceInterface,
  IArrowLocationCalculatorInterface,
  IArrowPlacementDataServiceInterface,
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
import { IAnimatedPictographDataServiceInterface } from "./interfaces/motion-tester-interfaces";
import {
  IBeatCalculationServiceInterface,
  IPropInterpolationServiceInterface,
  IAnimationStateServiceInterface,
  ISequenceAnimationOrchestratorInterface,
  ISequenceAnimationEngineInterface,
} from "./interfaces/animator-interfaces";

/**
 * Service interface mapping for string-based resolution
 * Maintains backward compatibility for existing code using string tokens
 */
export const serviceInterfaceMap = new Map<string, ServiceInterface<unknown>>([
  // Core services
  ["ISequenceService", ISequenceServiceInterface],
  ["ISequenceDomainService", ISequenceDomainServiceInterface],
  ["IPictographService", IPictographServiceInterface],
  ["IPictographRenderingService", IPictographRenderingServiceInterface],
  ["IPropRenderingService", IPropRenderingServiceInterface],
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
  ["IOptionDataService", IOptionDataServiceInterface],
  ["IStartPositionService", IStartPositionServiceInterface],
  ["IPanelManagementService", IPanelManagementServiceInterface],
  ["IPrintablePageLayoutService", IPrintablePageLayoutServiceInterface],
  ["IPageFactoryService", IPageFactoryServiceInterface],
  ["IPageImageExportService", IPageImageExportServiceInterface],
  ["ISequenceCardExportIntegrationService", ISequenceCardExportIntegrationServiceInterface],

  // Positioning services
  ["IArrowPositioningOrchestrator", IArrowPositioningOrchestratorInterface],
  ["IArrowPlacementDataService", IArrowPlacementDataServiceInterface],
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

  // Motion Tester services
  ["IAnimatedPictographDataService", IAnimatedPictographDataServiceInterface],

  // Animator services
  ["IBeatCalculationService", IBeatCalculationServiceInterface],
  ["IPropInterpolationService", IPropInterpolationServiceInterface],
  ["IAnimationStateService", IAnimationStateServiceInterface],
  ["ISequenceAnimationOrchestrator", ISequenceAnimationOrchestratorInterface],
  ["ISequenceAnimationEngine", ISequenceAnimationEngineInterface],
]);
