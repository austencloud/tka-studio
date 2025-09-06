/**
 * InversifyJS Service Type Identifiers
 *
 * This file defines all the service identifiers used by the InversifyJS container.
 * These replace the string-based tokens from the old custom DI system.
 */

// Core Service Types
export const TYPES = {
  // === CORE SERVICES ===
  ISequenceService: Symbol.for("ISequenceService"),
  ISequenceDomainService: Symbol.for("ISequenceDomainService"),
  ISequenceStateService: Symbol.for("ISequenceStateService"),
  ISequenceImportService: Symbol.for("ISequenceImportService"),
  ISequenceDeletionService: Symbol.for("ISequenceDeletionService"),
  IPersistenceService: Symbol.for("IPersistenceService"),
  ISettingsService: Symbol.for("ISettingsService"),
  IDeviceDetector: Symbol.for("IDeviceDetector"),
  IResourceTracker: Symbol.for("IResourceTracker"),
  IPanelManagementService: Symbol.for("IPanelManagementService"),

  // === BUILD TAB SERVICES ===
  IBuildTabService: Symbol.for("IBuildTabService"),
  IQuizSessionService: Symbol.for("IQuizSessionService"),
  // === WRITE TAB SERVICES ===
  IActService: Symbol.for("IActService"),
  IMusicPlayerService: Symbol.for("IMusicPlayerService"),
  // === OPTION PICKER SERVICES ===
  IOptionPickerLayoutService: Symbol.for("IOptionPickerLayoutService"),
  IOptionPickerDataService: Symbol.for("IOptionPickerDataService"),

  // === RENDERING SERVICES ===
  ISvgUtilityService: Symbol.for("ISvgUtilityService"),
  ISvgConfig: Symbol.for("ISvgConfig"),
  IDataTransformer: Symbol.for("IDataTransformer"),
  IGridRenderingService: Symbol.for("IGridRenderingService"),
  IArrowRenderer: Symbol.for("IArrowRenderer"),
  IOverlayRenderer: Symbol.for("IOverlayRenderer"),
  IPropCoordinator: Symbol.for("IPropCoordinator"),

  // === POSITIONING SERVICES ===
  IArrowPositioningOrchestrator: Symbol.for("IArrowPositioningOrchestrator"),
  IArrowPositioningService: Symbol.for("IArrowPositioningService"),
  IArrowAdjustmentCalculator: Symbol.for("IArrowAdjustmentCalculator"),
  IGridPositionDeriver: Symbol.for("IGridPositionDeriver"),
  IPositionCalculatorService: Symbol.for("IPositionCalculatorService"),
  IBetaOffsetCalculator: Symbol.for("IBetaOffsetCalculator"),
  IOrientationCalculationService: Symbol.for("IOrientationCalculationService"),

  // === MOVEMENT SERVICES ===
  IPositionPatternService: Symbol.for("IPositionPatternService"),
  IPictographValidatorService: Symbol.for("IPictographValidatorService"),
  IGridModeDeriver: Symbol.for("IGridModeDeriver"),
  IPictographGenerator: Symbol.for("IPictographGenerator"),

  // === BROWSE SERVICES ===
  IGalleryService: Symbol.for("IGalleryService"),
  IGalleryThumbnailService: Symbol.for("IGalleryThumbnailService"),
  INavigationService: Symbol.for("INavigationService"),
  IFavoritesService: Symbol.for("IFavoritesService"),
  IDeleteService: Symbol.for("IDeleteService"),
  ISectionService: Symbol.for("ISectionService"),
  ISequenceIndexService: Symbol.for("ISequenceIndexService"),
  IFilterPersistenceService: Symbol.for("IFilterPersistenceService"),
  IGalleryPanelManager: Symbol.for("IGalleryPanelManager"),
  // === WORKBENCH SERVICES ===
  IWorkbenchService: Symbol.for("IWorkbenchService"),
  IWorkbenchCoordinationService: Symbol.for("IWorkbenchCoordinationService"),
  IWorkbenchBeatOperationsService: Symbol.for(
    "IWorkbenchBeatOperationsService"
  ),
  IConstructTabCoordinator: Symbol.for("IConstructTabCoordinator"),
  IStartPositionService: Symbol.for("IStartPositionService"), // UNIFIED SERVICE

  // === BEAT FRAME SERVICES ===
  IBeatFrameService: Symbol.for("IBeatFrameService"),
  IBeatGridService: Symbol.for("IBeatGridService"),
  IBeatFallbackRenderer: Symbol.for("IBeatFallbackRenderer"),

  // === EXPORT SERVICES ===
  IExportService: Symbol.for("IExportService"),
  IPageImageExportService: Symbol.for("IPageImageExportService"),
  IPageFactoryService: Symbol.for("IPageFactoryService"),
  IPrintablePageLayoutService: Symbol.for("IPrintablePageLayoutService"),
  IWordCardExportIntegrationService: Symbol.for(
    "IWordCardExportIntegrationService"
  ),
  IWordCardExportOrchestrator: Symbol.for("IWordCardExportOrchestrator"),
  IImageFormatConverterService: Symbol.for("IImageFormatConverterService"),
  ISVGToCanvasConverterService: Symbol.for("ISVGToCanvasConverterService"),

  // === IMAGE EXPORT SERVICES ===
  ITKAImageExportService: Symbol.for("ITKAImageExportService"),
  ICanvasManagementService: Symbol.for("ICanvasManagementService"),
  IImageCompositionService: Symbol.for("IImageCompositionService"),
  ILayoutCalculationService: Symbol.for("ILayoutCalculationService"),
  IDimensionCalculationService: Symbol.for("IDimensionCalculationService"),
  IFilenameGeneratorService: Symbol.for("IFilenameGeneratorService"),
  IFileExportService: Symbol.for("IFileExportService"),
  IExportConfigManager: Symbol.for("IExportConfigManager"),
  IExportOptionsValidator: Symbol.for("IExportOptionsValidator"),
  IExportMemoryCalculator: Symbol.for("IExportMemoryCalculator"),
  IImagePreviewGenerator: Symbol.for("IImagePreviewGenerator"),
  IBeatRenderingService: Symbol.for("IBeatRenderingService"),
  IGridOverlayService: Symbol.for("IGridOverlayService"),

  // === GENERATION SERVICES ===
  ISequenceGenerationService: Symbol.for("ISequenceGenerationService"),

  // === CODEX SERVICES ===
  ILetterQueryHandler: Symbol.for("ILetterQueryHandler"),
  IPictographTransformationService: Symbol.for(
    "IPictographTransformationService"
  ),
  ICodexLetterMappingRepo: Symbol.for("ICodexLetterMappingRepo"),
  IOptionFilterer: Symbol.for("IOptionFilterer"),

  // === ANIMATOR SERVICES ===
  ISequenceAnimationEngine: Symbol.for("ISequenceAnimationEngine"),
  ISequenceAnimationOrchestrator: Symbol.for("ISequenceAnimationOrchestrator"),

  // === APPLICATION SERVICES ===
  IApplicationInitializer: Symbol.for("IApplicationInitializer"),

  // === SHARED SERVICES ===
  IEnumMapper: Symbol.for("IEnumMapper"),
  ICSVParser: Symbol.for("ICSVParser"),

  // === ADDITIONAL SERVICES ===
  IMotionQueryHandler: Symbol.for("IMotionQueryHandler"),
  ILetterDeriver: Symbol.for("ILetterDeriver"),
  ICSVLoader: Symbol.for("ICsvLoader"),

  // === MISSING SERVICES ===
  IQuizRepoManager: Symbol.for("IQuizRepoManager"),
  ICodexService: Symbol.for("ICodexService"),
  ICodexPictographUpdater: Symbol.for("ICodexPictographUpdater"),
  IBeatCalculationService: Symbol.for("IBeatCalculationService"),
  IPropInterpolationService: Symbol.for("IPropInterpolationService"),
  IAnimationStateService: Symbol.for("IAnimationStateService"),
  IAngleCalculationService: Symbol.for("IAngleCalculationService"),
  IMotionCalculationService: Symbol.for("IMotionCalculationService"),
  IEndpointCalculationService: Symbol.for("IEndpointCalculationService"),
  ICoordinateUpdateService: Symbol.for("ICoordinateUpdateService"),

  IAnimatedPictographDataService: Symbol.for("IAnimatedPictographDataService"),
  IBackgroundService: Symbol.for("IBackgroundService"),
  IBrowseStatePersister: Symbol.for("IBrowseStatePersister"),
  IArrowPlacementService: Symbol.for("IArrowPlacementService"),
  IMotionParameterService: Symbol.for("IMotionParameterService"),
  IAnimationControlService: Symbol.for("IAnimationControlService"),
  IMotionLetterIdentificationService: Symbol.for(
    "IMotionLetterIdentificationService"
  ),
  ICSVPictographLoaderService: Symbol.for("ICSVPictographLoaderService"),
  ICSVPictographParserService: Symbol.for("ICSVPictographParserService"),
  IArrowLocationService: Symbol.for("IArrowLocationService"),
  IArrowPlacementKeyService: Symbol.for("IArrowPlacementKeyService"),
  IPropPlacementService: Symbol.for("IPropPlacementService"),
  IValidationService: Symbol.for("IValidationService"),

  // === MISSING TYPES ===
  IArrowPathResolutionService: Symbol.for("IArrowPathResolutionService"),

  IUltimatePictographRenderingService: Symbol.for(
    "IUltimatePictographRenderingService"
  ),

  // === MISSING ARROW POSITIONING TYPES ===
  IDirectionCalculator: Symbol.for("IDirectionCalculator"),
  IArrowLocationCalculator: Symbol.for("IArrowLocationCalculator"),
  IArrowRotationCalculator: Symbol.for("IArrowRotationCalculator"),
  IDashLocationCalculator: Symbol.for("IDashLocationCalculator"),
  IArrowCoordinateSystemService: Symbol.for("IArrowCoordinateSystemService"),
  ISpecialPlacementService: Symbol.for("ISpecialPlacementService"),
  IDefaultPlacementService: Symbol.for("IDefaultPlacementService"),
  ISpecialPlacementOriKeyGenerator: Symbol.for(
    "ISpecialPlacementOriKeyGenerator"
  ),
  ArrowPlacementKeyService: Symbol.for("ArrowPlacementKeyService"),
  ITurnsTupleKeyGenerator: Symbol.for("ITurnsTupleKeyGenerator"),
  IAttributeKeyGenerator: Symbol.for("IAttributeKeyGenerator"),
  IDirectionalTupleProcessor: Symbol.for("IDirectionalTupleProcessor"),
  IDirectionalTupleCalculator: Symbol.for("IDirectionalTupleCalculator"),
  IQuadrantIndexCalculator: Symbol.for("IQuadrantIndexCalculator"),

  // === MISSING IMAGE EXPORT TYPES ===
  IWordTextRenderer: Symbol.for("IWordTextRenderer"),
  IUserInfoRenderer: Symbol.for("IUserInfoRenderer"),
  IDifficultyBadgeRenderer: Symbol.for("IDifficultyBadgeRenderer"),
  ITextRenderingUtils: Symbol.for("ITextRenderingUtils"),
  ITextRenderingService: Symbol.for("ITextRenderingService"),

  // === UTILITY SERVICES ===
  IBetaDetectionService: Symbol.for("IBetaDetectionService"),
  IErrorHandlingService: Symbol.for("IErrorHandlingService"),

  // === STATE SERVICES ===
  IAppStateInitializer: Symbol.for("IAppStateInitializer"),
  IApplicationStateService: Symbol.for("IApplicationStateService"),
  IMainTabState: Symbol.for("IMainTabState"),
  IPerformanceMetricsState: Symbol.for("IPerformanceMetricsState"),
} as const;

// Type helper for getting service types
export type ServiceType = (typeof TYPES)[keyof typeof TYPES];

// Export individual type groups for easier imports
export const CoreTypes = {
  ISequenceService: TYPES.ISequenceService,
  ISequenceDomainService: TYPES.ISequenceDomainService,
  ISequenceStateService: TYPES.ISequenceStateService,
  IPersistenceService: TYPES.IPersistenceService,
  ISettingsService: TYPES.ISettingsService,
} as const;

export const RenderingTypes = {
  ISvgUtilityService: TYPES.ISvgUtilityService,
  IGridRenderingService: TYPES.IGridRenderingService,
  IArrowRenderer: TYPES.IArrowRenderer,
} as const;

export const PositioningTypes = {
  IArrowPositioningOrchestrator: TYPES.IArrowPositioningOrchestrator,
  IGridPositionDeriver: TYPES.IGridPositionDeriver,
  IPositionCalculatorService: TYPES.IPositionCalculatorService,
  IArrowPositioningService: TYPES.IArrowPositioningService,
  IBetaOffsetCalculator: TYPES.IBetaOffsetCalculator,
} as const;
