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
  ISequenceAnalysisService: Symbol.for("ISequenceAnalysisService"),
  IBeatNumberingService: Symbol.for("IBeatNumberingService"),
  ISequenceValidationService: Symbol.for("ISequenceValidationService"),
  ISequenceStatisticsService: Symbol.for("ISequenceStatisticsService"),
  ISequenceTransformationService: Symbol.for("ISequenceTransformationService"),
  ISequenceImportService: Symbol.for("ISequenceImportService"),
  ISequenceDeletionService: Symbol.for("ISequenceDeletionService"),
  ISequenceTransformService: Symbol.for("ISequenceTransformService"),
  ISequenceExportService: Symbol.for("ISequenceExportService"),
  ISequencePersistenceService: Symbol.for("ISequencePersistenceService"),
  IPersistenceService: Symbol.for("IPersistenceService"),
  IPersistenceInitializationService: Symbol.for(
    "IPersistenceInitializationService"
  ),
  ISettingsService: Symbol.for("ISettingsService"),
  IDeviceDetector: Symbol.for("IDeviceDetector"),
  IResourceTracker: Symbol.for("IResourceTracker"),
  IPanelManagementService: Symbol.for("IPanelManagementService"),

  // === FOUNDATION SERVICES ===
  IFileDownloadService: Symbol.for("IFileDownloadService"),
  IStorageService: Symbol.for("IStorageService"),
  ISeoService: Symbol.for("ISeoService"),
  ISvgImageService: Symbol.for("ISvgImageService"),

  // === APPLICATION SERVICES ===
  IComponentManagementService: Symbol.for("IComponentManagementService"),
  IDataTransformationService: Symbol.for("IDataTransformationService"),
  IPictographCoordinator: Symbol.for("IPictographCoordinator"),
  IAnimationService: Symbol.for("IAnimationService"),
  IHapticFeedbackService: Symbol.for("IHapticFeedbackService"),
  IRippleEffectService: Symbol.for("IRippleEffectService"),

  // === MOBILE SERVICES ===
  IMobileFullscreenService: Symbol.for("IMobileFullscreenService"),
  IPlatformDetectionService: Symbol.for("IPlatformDetectionService"),
  IGestureService: Symbol.for("IGestureService"),
  IPWAEngagementService: Symbol.for("IPWAEngagementService"),
  IPWAInstallDismissalService: Symbol.for("IPWAInstallDismissalService"),

  // === NAVIGATION UI SERVICES ===
  IViewportService: Symbol.for("IViewportService"),
  IModuleSelectionService: Symbol.for("IModuleSelectionService"),
  IKeyboardNavigationService: Symbol.for("IKeyboardNavigationService"),

  // === BUILD TAB SERVICES ===
  IBuildTabService: Symbol.for("IBuildTabService"),
  IBuildTabInitializationService: Symbol.for("IBuildTabInitializationService"),
  IBuildTabLayoutService: Symbol.for("IBuildTabLayoutService"),
  IResponsiveLayoutService: Symbol.for("IResponsiveLayoutService"),
  INavigationSyncService: Symbol.for("INavigationSyncService"),
  IBeatOperationsService: Symbol.for("IBeatOperationsService"),
  IUndoService: Symbol.for("IUndoService"),
  IQuizSessionService: Symbol.for("IQuizSessionService"),
  IQuizGradingService: Symbol.for("IQuizGradingService"),
  IQuizFeedbackService: Symbol.for("IQuizFeedbackService"),
  IQuizAchievementService: Symbol.for("IQuizAchievementService"),
  IQuizFormatterService: Symbol.for("IQuizFormatterService"),
  ITurnControlService: Symbol.for("ITurnControlService"),
  // === WRITE TAB SERVICES ===
  IActService: Symbol.for("IActService"),
  IMusicPlayerService: Symbol.for("IMusicPlayerService"),
  // === OPTION PICKER SERVICES ===
  IOptionPickerSizingService: Symbol.for("IOptionPickerSizingService"),
  IOptionPickerFilterPersistenceService: Symbol.for(
    "IOptionPickerFilterPersistenceService"
  ),
  IReversalChecker: Symbol.for("IReversalChecker"),
  IPositionAnalyzer: Symbol.for("IPositionAnalyzer"),
  IOptionSorter: Symbol.for("IOptionSorter"),
  IOptionFilter: Symbol.for("IOptionFilter"),
  IOptionOrganizerService: Symbol.for("IOptionOrganizerService"),
  IOptionLoader: Symbol.for("IOptionLoader"),
  ILayoutDetectionService: Symbol.for("ILayoutDetectionService"),

  // === START POSITION PICKER SERVICES ===
  // Simplified - only the core service needed

  // === RENDERING SERVICES ===
  ISvgUtilityService: Symbol.for("ISvgUtilityService"),
  ISvgPreloadService: Symbol.for("ISvgPreloadService"),
  ISvgConfig: Symbol.for("ISvgConfig"),
  IDataTransformer: Symbol.for("IDataTransformer"),
  IGridRenderingService: Symbol.for("IGridRenderingService"),
  IGridService: Symbol.for("IGridService"),
  IArrowRenderer: Symbol.for("IArrowRenderer"),
  IArrowLifecycleManager: Symbol.for("IArrowLifecycleManager"),

  // === ARROW RENDERING SERVICES ===
  IArrowPathResolver: Symbol.for("IArrowPathResolver"),
  IArrowSvgLoader: Symbol.for("IArrowSvgLoader"),
  IArrowSvgParser: Symbol.for("IArrowSvgParser"),
  IArrowSvgColorTransformer: Symbol.for("IArrowSvgColorTransformer"),

  IOverlayRenderer: Symbol.for("IOverlayRenderer"),
  IPropSvgLoader: Symbol.for("IPropSvgLoader"),

  // === POSITIONING SERVICES ===
  IArrowPositioningOrchestrator: Symbol.for("IArrowPositioningOrchestrator"),
  IArrowAdjustmentCalculator: Symbol.for("IArrowAdjustmentCalculator"),
  IGridPositionDeriver: Symbol.for("IGridPositionDeriver"),
  IPositionCalculatorService: Symbol.for("IPositionCalculatorService"),
  IOrientationCalculationService: Symbol.for("IOrientationCalculationService"),

  // === MOVEMENT SERVICES ===
  IPositionPatternService: Symbol.for("IPositionPatternService"),
  IPictographValidatorService: Symbol.for("IPictographValidatorService"),
  IGridModeDeriver: Symbol.for("IGridModeDeriver"),

  // === BROWSE SERVICES ===
  // Specialized gallery services (no orchestration layer - use directly!)
  IGalleryThumbnailService: Symbol.for("IGalleryThumbnailService"),
  IGalleryCacheService: Symbol.for("IGalleryCacheService"),
  IGalleryFilterService: Symbol.for("IGalleryFilterService"),
  IGalleryLoader: Symbol.for("IGalleryLoader"),
  IGalleryMetadataExtractor: Symbol.for("IGalleryMetadataExtractor"),
  IGallerySortService: Symbol.for("IGallerySortService"),
  IOptimizedGalleryService: Symbol.for("IOptimizedGalleryService"),
  INavigationService: Symbol.for("INavigationService"),
  IFavoritesService: Symbol.for("IFavoritesService"),
  IDeleteService: Symbol.for("IDeleteService"),
  ISectionService: Symbol.for("ISectionService"),
  ISequenceIndexService: Symbol.for("ISequenceIndexService"),
  IGalleryPanelManager: Symbol.for("IGalleryPanelManager"),
  IFilterPersistenceService: Symbol.for("IFilterPersistenceService"),
  // === WORKBENCH SERVICES ===
  IWorkbenchService: Symbol.for("IWorkbenchService"),
  IConstructTabCoordinator: Symbol.for("IConstructTabCoordinator"),
  IStartPositionService: Symbol.for("IStartPositionService"), // UNIFIED SERVICE

  // === EXPORT SERVICES ===
  IExportService: Symbol.for("IExportService"),
  IShareService: Symbol.for("IShareService"),
  IPageImageExportService: Symbol.for("IPageImageExportService"),
  IPageFactoryService: Symbol.for("IPageFactoryService"),
  IPrintablePageLayoutService: Symbol.for("IPrintablePageLayoutService"),
  IWordCardExportIntegrationService: Symbol.for(
    "IWordCardExportIntegrationService"
  ),
  IWordCardExportOrchestrator: Symbol.for("IWordCardExportOrchestrator"),
  IWordCardImageGenerationService: Symbol.for(
    "IWordCardImageGenerationService"
  ),
  IWordCardImageConversionService: Symbol.for(
    "IWordCardImageConversionService"
  ),
  IWordCardBatchProcessingService: Symbol.for(
    "IWordCardBatchProcessingService"
  ),
  IWordCardExportProgressTracker: Symbol.for("IWordCardExportProgressTracker"),
  IWordCardCacheService: Symbol.for("IWordCardCacheService"),
  IWordCardSVGCompositionService: Symbol.for("IWordCardSVGCompositionService"),
  IWordCardMetadataOverlayService: Symbol.for(
    "IWordCardMetadataOverlayService"
  ),
  IImageFormatConverterService: Symbol.for("IImageFormatConverterService"),
  ISVGToCanvasConverterService: Symbol.for("ISVGToCanvasConverterService"),

  // === IMAGE EXPORT SERVICES ===
  ITKAImageExportService: Symbol.for("ITKAImageExportService"),
  ICanvasManagementService: Symbol.for("ICanvasManagementService"),
  IImageCompositionService: Symbol.for("IImageCompositionService"),
  ILayoutCalculationService: Symbol.for("ILayoutCalculationService"),
  IDimensionCalculationService: Symbol.for("IDimensionCalculationService"),
  IFilenameGeneratorService: Symbol.for("IFilenameGeneratorService"),

  // === RENDER SERVICES ===
  ISequenceRenderService: Symbol.for("ISequenceRenderService"),
  ITextRenderingService: Symbol.for("ITextRenderingService"),
  IGlyphCacheService: Symbol.for("IGlyphCacheService"),
  IExportConfigManager: Symbol.for("IExportConfigManager"),
  IExportOptionsValidator: Symbol.for("IExportOptionsValidator"),
  IExportMemoryCalculator: Symbol.for("IExportMemoryCalculator"),
  IImagePreviewGenerator: Symbol.for("IImagePreviewGenerator"),
  IReversalDetectionService: Symbol.for("IReversalDetectionService"),

  // === GENERATION SERVICES ===
  // Refactored Generation Services (Single Responsibility)
  IRandomSelectionService: Symbol.for("IRandomSelectionService"),
  IPictographFilterService: Symbol.for("IPictographFilterService"),
  IBeatConverterService: Symbol.for("IBeatConverterService"),
  ITurnManagementService: Symbol.for("ITurnManagementService"),
  ITurnIntensityManagerService: Symbol.for("ITurnIntensityManagerService"),
  ISequenceMetadataService: Symbol.for("ISequenceMetadataService"),
  // New Focused Generation Services (replaced monolithic SequenceGenerationService)
  IStartPositionSelector: Symbol.for("IStartPositionSelector"),
  IRotationDirectionService: Symbol.for("IRotationDirectionService"),
  ITurnAllocationCalculator: Symbol.for("ITurnAllocationCalculator"),
  IBeatGenerationOrchestrator: Symbol.for("IBeatGenerationOrchestrator"),
  IPartialSequenceGenerator: Symbol.for("IPartialSequenceGenerator"),
  // Circular Generation (CAP) Services
  IComplementaryLetterService: Symbol.for("IComplementaryLetterService"),
  IRotatedEndPositionSelector: Symbol.for("IRotatedEndPositionSelector"),
  ICAPEndPositionSelector: Symbol.for("ICAPEndPositionSelector"),
  IStrictRotatedCAPExecutor: Symbol.for("IStrictRotatedCAPExecutor"),
  IStrictMirroredCAPExecutor: Symbol.for("IStrictMirroredCAPExecutor"),
  IStrictSwappedCAPExecutor: Symbol.for("IStrictSwappedCAPExecutor"),
  IStrictComplementaryCAPExecutor: Symbol.for("IStrictComplementaryCAPExecutor"),
  IMirroredSwappedCAPExecutor: Symbol.for("IMirroredSwappedCAPExecutor"),
  ISwappedComplementaryCAPExecutor: Symbol.for("ISwappedComplementaryCAPExecutor"),
  IMirroredComplementaryCAPExecutor: Symbol.for("IMirroredComplementaryCAPExecutor"),
  IRotatedSwappedCAPExecutor: Symbol.for("IRotatedSwappedCAPExecutor"),
  IRotatedComplementaryCAPExecutor: Symbol.for("IRotatedComplementaryCAPExecutor"),
  ICAPExecutorSelector: Symbol.for("ICAPExecutorSelector"),
  // Generation UI Services (SRP Refactoring - Dec 2024)
  ILevelConversionService: Symbol.for("ILevelConversionService"),
  IResponsiveTypographyService: Symbol.for("IResponsiveTypographyService"),
  ICardConfigurationService: Symbol.for("ICardConfigurationService"),
  ICAPTypeService: Symbol.for("ICAPTypeService"),
  IGenerationOrchestrationService: Symbol.for("IGenerationOrchestrationService"),
  IPresetFormatterService: Symbol.for("IPresetFormatterService"),

  // === CODEX SERVICES ===
  ILetterQueryHandler: Symbol.for("ILetterQueryHandler"),
  IPictographTransformationService: Symbol.for(
    "IPictographTransformationService"
  ),
  ICodexLetterMappingRepo: Symbol.for("ICodexLetterMappingRepo"),

  // === ANIMATOR SERVICES ===
  ISequenceAnimationOrchestrator: Symbol.for("ISequenceAnimationOrchestrator"),
  IAnimationLoopService: Symbol.for("IAnimationLoopService"),
  IAnimationPlaybackController: Symbol.for("IAnimationPlaybackController"),
  IAnimationStateService: Symbol.for("IAnimationStateService"),
  IBeatCalculationService: Symbol.for("IBeatCalculationService"),
  IPropInterpolationService: Symbol.for("IPropInterpolationService"),

  // Animator Calculation Services
  IAngleCalculator: Symbol.for("IAngleCalculator"),
  ICoordinateUpdater: Symbol.for("ICoordinateUpdater"),
  IMotionCalculator: Symbol.for("IMotionCalculator"),
  IEndpointCalculator: Symbol.for("IEndpointCalculator"),

  // Animator Rendering Services
  ICanvasRenderer: Symbol.for("ICanvasRenderer"),
  ISVGGenerator: Symbol.for("ISVGGenerator"),

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

  // Learn Module - Read
  IPDFService: Symbol.for("IPDFService"),
  IFlipBookService: Symbol.for("IFlipBookService"),
  ICodexService: Symbol.for("ICodexService"),
  ICodexPictographUpdater: Symbol.for("ICodexPictographUpdater"),
  IAngleCalculationService: Symbol.for("IAngleCalculationService"),
  IMotionCalculationService: Symbol.for("IMotionCalculationService"),
  IEndpointCalculationService: Symbol.for("IEndpointCalculationService"),
  ICoordinateUpdateService: Symbol.for("ICoordinateUpdateService"),

  IAnimatedPictographDataService: Symbol.for("IAnimatedPictographDataService"),
  IBackgroundService: Symbol.for("IBackgroundService"),
  IBackgroundManager: Symbol.for("IBackgroundManager"),
  IBackgroundRenderingService: Symbol.for("IBackgroundRenderingService"),
  IBackgroundPreloader: Symbol.for("IBackgroundPreloader"),
  IBackgroundConfigurationService: Symbol.for(
    "IBackgroundConfigurationService"
  ),
  INightSkyCalculationService: Symbol.for("INightSkyCalculationService"),
  IBrowseStatePersister: Symbol.for("IBrowseStatePersister"),
  IArrowPlacementService: Symbol.for("IArrowPlacementService"),
  IMotionParameterService: Symbol.for("IMotionParameterService"),
  IAnimationControlService: Symbol.for("IAnimationControlService"),
  IMotionLetterIdentificationService: Symbol.for(
    "IMotionLetterIdentificationService"
  ),
  ICSVPictographLoader: Symbol.for("ICSVPictographLoader"),
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
  IArrowGridCoordinateService: Symbol.for("IArrowGridCoordinateService"),
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

  // === ARROW ORCHESTRATION TYPES ===
  IArrowAdjustmentProcessor: Symbol.for("IArrowAdjustmentProcessor"),
  IArrowCoordinateTransformer: Symbol.for("IArrowCoordinateTransformer"),
  IArrowDataProcessor: Symbol.for("IArrowDataProcessor"),
  IArrowQuadrantCalculator: Symbol.for("IArrowQuadrantCalculator"),

  // === MISSING IMAGE EXPORT TYPES ===
  IFileExportService: Symbol.for("IFileExportService"),

  // === UTILITY SERVICES ===
  IBetaDetectionService: Symbol.for("IBetaDetectionService"),
  IErrorHandlingService: Symbol.for("IErrorHandlingService"),

  // === STATE SERVICES ===
  IAppState: Symbol.for("IAppState"),
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
  IBeatNumberingService: TYPES.IBeatNumberingService,
  ISequenceValidationService: TYPES.ISequenceValidationService,
  ISequenceStatisticsService: TYPES.ISequenceStatisticsService,
  ISequenceTransformationService: TYPES.ISequenceTransformationService,
  IPersistenceService: TYPES.IPersistenceService,
  ISettingsService: TYPES.ISettingsService,
} as const;

export const RenderingTypes = {
  ISvgUtilityService: TYPES.ISvgUtilityService,
  IGridRenderingService: TYPES.IGridRenderingService,
  IGridService: TYPES.IGridService,
  IArrowRenderer: TYPES.IArrowRenderer,
} as const;

export const PositioningTypes = {
  IArrowPositioningOrchestrator: TYPES.IArrowPositioningOrchestrator,
  IGridPositionDeriver: TYPES.IGridPositionDeriver,
  IPositionCalculatorService: TYPES.IPositionCalculatorService,
} as const;

export const BackgroundTypes = {
  IBackgroundService: TYPES.IBackgroundService,
  IBackgroundManager: TYPES.IBackgroundManager,
  IBackgroundRenderingService: TYPES.IBackgroundRenderingService,
  IBackgroundPreloader: TYPES.IBackgroundPreloader,
  IBackgroundConfigurationService: TYPES.IBackgroundConfigurationService,
  INightSkyCalculationService: TYPES.INightSkyCalculationService,
} as const;
