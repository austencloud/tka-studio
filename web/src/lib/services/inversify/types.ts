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
  IDeviceDetectionService: Symbol.for("IDeviceDetectionService"),
  IPanelManagementService: Symbol.for("IPanelManagementService"),

  // === RENDERING SERVICES ===
  ISvgUtilityService: Symbol.for("ISvgUtilityService"),
  ISvgConfiguration: Symbol.for("ISvgConfiguration"),
  IDataTransformationService: Symbol.for("IDataTransformationService"),
  IGridRenderingService: Symbol.for("IGridRenderingService"),
  IArrowRenderingService: Symbol.for("IArrowRenderingService"),
  IOverlayRenderingService: Symbol.for("IOverlayRenderingService"),
  IPropCoordinatorService: Symbol.for("IPropCoordinatorService"),

  // === POSITIONING SERVICES ===
  IArrowPositioningOrchestrator: Symbol.for("IArrowPositioningOrchestrator"),
  IArrowPositioningService: Symbol.for("IArrowPositioningService"),
  IArrowAdjustmentCalculator: Symbol.for("IArrowAdjustmentCalculator"),
  IPositionMapper: Symbol.for("IPositionMapper"),
  IPositionCalculatorService: Symbol.for("IPositionCalculatorService"),
  IBetaOffsetCalculator: Symbol.for("IBetaOffsetCalculator"),
  IOrientationCalculationService: Symbol.for("IOrientationCalculationService"),

  // === MOVEMENT SERVICES ===
  IPositionPatternService: Symbol.for("IPositionPatternService"),
  IPictographValidatorService: Symbol.for("IPictographValidatorService"),
  IGridModeDeriver: Symbol.for("IGridModeDeriver"),
  IPictographGenerator: Symbol.for("IPictographGenerator"),

  // === BROWSE SERVICES ===
  IBrowseService: Symbol.for("IBrowseService"),
  IThumbnailService: Symbol.for("IThumbnailService"),
  INavigationService: Symbol.for("INavigationService"),
  IFavoritesService: Symbol.for("IFavoritesService"),
  IDeleteService: Symbol.for("IDeleteService"),
  ISectionService: Symbol.for("ISectionService"),
  ISequenceIndexService: Symbol.for("ISequenceIndexService"),
  IFilterPersistenceService: Symbol.for("IFilterPersistenceService"),

  // === WORKBENCH SERVICES ===
  IWorkbenchService: Symbol.for("IWorkbenchService"),
  IWorkbenchCoordinationService: Symbol.for("IWorkbenchCoordinationService"),
  IWorkbenchBeatOperationsService: Symbol.for(
    "IWorkbenchBeatOperationsService"
  ),
  IConstructTabCoordinationService: Symbol.for(
    "IConstructTabCoordinationService"
  ),
  IStartPositionService: Symbol.for("IStartPositionService"),
  IStartPositionSelectionService: Symbol.for("IStartPositionSelectionService"),

  // === BEAT FRAME SERVICES ===
  IBeatFrameService: Symbol.for("IBeatFrameService"),
  IBeatGridService: Symbol.for("IBeatGridService"),
  IBeatFallbackRenderingService: Symbol.for("IBeatFallbackRenderingService"),

  // === EXPORT SERVICES ===
  IExportService: Symbol.for("IExportService"),
  IPageImageExportService: Symbol.for("IPageImageExportService"),
  IPageFactoryService: Symbol.for("IPageFactoryService"),
  IPrintablePageLayoutService: Symbol.for("IPrintablePageLayoutService"),
  ISequenceCardExportIntegrationService: Symbol.for(
    "ISequenceCardExportIntegrationService"
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
  IFileExportService: Symbol.for("IFileExportService"),
  IExportConfigurationManager: Symbol.for("IExportConfigurationManager"),
  IExportOptionsValidator: Symbol.for("IExportOptionsValidator"),
  IExportMemoryCalculator: Symbol.for("IExportMemoryCalculator"),
  IImagePreviewGenerator: Symbol.for("IImagePreviewGenerator"),
  IBeatRenderingService: Symbol.for("IBeatRenderingService"),
  IGridOverlayService: Symbol.for("IGridOverlayService"),

  // === GENERATION SERVICES ===
  ISequenceGenerationService: Symbol.for("ISequenceGenerationService"),

  // === CODEX SERVICES ===
  ILetterQueryService: Symbol.for("ILetterQueryService"),
  IPictographTransformationService: Symbol.for(
    "IPictographTransformationService"
  ),
  ILetterMappingRepository: Symbol.for("ILetterMappingRepository"),
  IOptionFilteringService: Symbol.for("IOptionFilteringService"),

  // === ANIMATOR SERVICES ===
  ISequenceAnimationEngine: Symbol.for("ISequenceAnimationEngine"),
  ISequenceAnimationOrchestrator: Symbol.for("ISequenceAnimationOrchestrator"),

  // === APPLICATION SERVICES ===
  IApplicationInitializationService: Symbol.for(
    "IApplicationInitializationService"
  ),

  // === SHARED SERVICES ===
  IEnumMappingService: Symbol.for("IEnumMappingService"),
  ICSVParsingService: Symbol.for("ICSVParsingService"),

  // === ADDITIONAL SERVICES ===
  IMotionQueryService: Symbol.for("IMotionQueryService"),
  ILetterDeriver: Symbol.for("ILetterDeriver"),
  ICsvLoaderService: Symbol.for("ICsvLoaderService"),

  // === MISSING SERVICES ===
  IExampleSequenceService: Symbol.for("IExampleSequenceService"),
  ILessonRepository: Symbol.for("ILessonRepository"),
  ICodexService: Symbol.for("ICodexService"),
  IPictographOperationsService: Symbol.for("IPictographOperationsService"),
  IBeatCalculationService: Symbol.for("IBeatCalculationService"),
  IPropInterpolationService: Symbol.for("IPropInterpolationService"),
  IAnimationStateService: Symbol.for("IAnimationStateService"),
  IAngleCalculationService: Symbol.for("IAngleCalculationService"),
  IMotionCalculationService: Symbol.for("IMotionCalculationService"),
  IEndpointCalculationService: Symbol.for("IEndpointCalculationService"),
  ICoordinateUpdateService: Symbol.for("ICoordinateUpdateService"),

  IAnimatedPictographDataService: Symbol.for("IAnimatedPictographDataService"),
  IBackgroundService: Symbol.for("IBackgroundService"),
  IBrowseStatePersistenceService: Symbol.for("IBrowseStatePersistenceService"),
  IArrowPlacementService: Symbol.for("IArrowPlacementService"),
  ICSVParserService: Symbol.for("ICSVParserService"),
  IMotionParameterService: Symbol.for("IMotionParameterService"),
  IAnimationControlService: Symbol.for("IAnimationControlService"),
  IMotionLetterIdentificationService: Symbol.for(
    "IMotionLetterIdentificationService"
  ),
  ICSVPictographLoaderService: Symbol.for("ICSVPictographLoaderService"),
  IArrowLocationService: Symbol.for("IArrowLocationService"),
  IArrowPlacementKeyService: Symbol.for("IArrowPlacementKeyService"),
  IPropPlacementService: Symbol.for("IPropPlacementService"),

  // === MISSING TYPES ===
  IArrowPathResolutionService: Symbol.for("IArrowPathResolutionService"),

  IUltimatePictographRenderingService: Symbol.for(
    "IUltimatePictographRenderingService"
  ),

  // === MISSING ARROW POSITIONING TYPES ===
  IDirectionCalculator: Symbol.for("IDirectionCalculator"),
  IArrowLocationCalculator: Symbol.for("IArrowLocationCalculator"),
  IArrowRotationCalculator: Symbol.for("IArrowRotationCalculator"),
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

  // === MISSING IMAGE EXPORT TYPES ===
  IWordTextRenderer: Symbol.for("IWordTextRenderer"),
  IUserInfoRenderer: Symbol.for("IUserInfoRenderer"),
  IDifficultyBadgeRenderer: Symbol.for("IDifficultyBadgeRenderer"),
  ITextRenderingUtils: Symbol.for("ITextRenderingUtils"),
  ITextRenderingService: Symbol.for("ITextRenderingService"),
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
  IArrowRenderingService: TYPES.IArrowRenderingService,
} as const;

export const PositioningTypes = {
  IArrowPositioningOrchestrator: TYPES.IArrowPositioningOrchestrator,
  IPositionMapper: TYPES.IPositionMapper,
  IPositionCalculatorService: TYPES.IPositionCalculatorService,
  IArrowPositioningService: TYPES.IArrowPositioningService,
  IBetaOffsetCalculator: TYPES.IBetaOffsetCalculator,
} as const;
