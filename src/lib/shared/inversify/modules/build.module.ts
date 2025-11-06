import { ContainerModule, type ContainerModuleLoadOptions } from "inversify";
import {
  CreateModuleService,
  ConstructCoordinator,
  ReversalDetectionService,
  SequenceDeletionService,
  SequenceDomainService,
  SequenceExportService,
  SequenceImportService,
  SequenceIndexService,
  SequencePersistenceService,
  SequenceService,
  SequenceTransformService,
  WorkbenchService,
} from "../../../modules";
import { SequenceAnalysisService } from "../../../modules/create/shared/services/implementations/SequenceAnalysisService";
import { CreateModuleHandlers } from "../../../modules/create/shared/services/implementations/CreateModuleHandlers";
import { OptionSizer } from "../../../modules/create/construct/option-picker/option-viewer/services/implementations";
import { StartPositionService } from "../../../modules/create/construct/start-position-picker/services/implementations";
import { CreateModuleLayoutService } from "../../../modules/create/shared/layout/services/CreateModuleLayoutService";
import { BeatNumberingService } from "../../../modules/create/shared/services/implementations/BeatNumberingService";
import { SequenceStatisticsService } from "../../../modules/create/shared/services/implementations/SequenceStatisticsService";
import { SequenceTransformationService } from "../../../modules/create/shared/services/implementations/SequenceTransformationService";
import { SequenceValidationService } from "../../../modules/create/shared/services/implementations/SequenceValidationService";
import { UndoService } from "../../../modules/create/shared/services/implementations/UndoService";
// NEW: CreateModule Refactoring Services (2025-10-28)
import { BeatOperationsService } from "../../../modules/create/shared/services/implementations/BeatOperationsService";
import { KeyboardArrowAdjustmentService } from "../../../modules/create/shared/services/implementations/KeyboardArrowAdjustmentService";
import { CreateModuleInitializationService } from "../../../modules/create/shared/services/implementations/CreateModuleInitializationService";
import { NavigationSyncService } from "../../../modules/create/shared/services/implementations/NavigationSyncService";
import { ResponsiveLayoutService } from "../../../modules/create/shared/services/implementations/ResponsiveLayoutService";
import { CreationMethodPersistenceService } from "../../../modules/create/shared/services/implementations/CreationMethodPersistenceService";
import { CreateModuleEffectCoordinator } from "../../../modules/create/shared/services/implementations/CreateModuleEffectCoordinator";
// Refactored Generation Services
import {
  OptionFilter,
  OptionLoader,
  OptionOrganizer,
  OptionSorter,
  OptionTransitionCoordinator,
  PositionAnalyzer,
  ReversalChecker,
  SectionTitleFormatter,
} from "../../../modules/create/construct/option-picker/option-viewer/services/implementations";
import { FilterPersistenceService } from "../../../modules/create/construct/option-picker/services/FilterPersistenceService";
import { LayoutDetectionService } from "../../../modules/create/construct/option-picker/services/implementations/LayoutDetectionService";
import { TurnControlService } from "../../../modules/create/edit/services/TurnControlService";
// Shared Generation Services - ACTIVE ONLY (deprecated moved to _deprecated/)
import {
  BeatConverterService,
  BeatGenerationOrchestrator,
  ComplementaryLetterService,
  GenerationOrchestrationService,
  PictographFilterService,
  SequenceMetadataService,
  StartPositionSelector,
  TurnAllocationCalculator,
  TurnIntensityLevelService,
  TurnManagementService,
} from "../../../modules/create/generate/shared/services/implementations";
// Circular Generation Services
import {
  CAPEndPositionSelector,
  CAPExecutorSelector,
  MirroredComplementaryCAPExecutor,
  MirroredSwappedCAPExecutor,
  PartialSequenceGenerator,
  RotatedComplementaryCAPExecutor,
  RotatedEndPositionSelector,
  RotatedSwappedCAPExecutor,
  RotationDirectionService,
  StrictComplementaryCAPExecutor,
  StrictMirroredCAPExecutor,
  StrictRotatedCAPExecutor,
  StrictSwappedCAPExecutor,
  SwappedComplementaryCAPExecutor,
} from "../../../modules/create/generate/circular/services/implementations";
// Generation UI Services (SRP Refactoring - Dec 2024) - ACTIVE ONLY
import {
  CAPTypeService,
  CardConfigurationService,
  LevelConversionService,
  ResponsiveTypographyService,
} from "../../../modules/create/generate/shared/services/implementations";
// Gestural Path Builder Services (January 2025)
import {
  HandPathDirectionDetector,
  PathToMotionConverter,
  SwipeDetectionService,
} from "../../../modules/create/construct/handpath-builder/services/implementations";
import { TYPES } from "../types";

export const buildModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === Create Module ServiceS ===
    options.bind(TYPES.ICreateModuleService).to(CreateModuleService);
    options.bind(TYPES.ICreateModuleHandlers).to(CreateModuleHandlers);
    options
      .bind(TYPES.ICreateModuleLayoutService)
      .to(CreateModuleLayoutService);
    options
      .bind(TYPES.ICreateModuleInitializationService)
      .to(CreateModuleInitializationService);
    options
      .bind(TYPES.ICreateModuleEffectCoordinator)
      .to(CreateModuleEffectCoordinator);
    options
      .bind(TYPES.ICreationMethodPersistenceService)
      .to(CreationMethodPersistenceService);
    options.bind(TYPES.IResponsiveLayoutService).to(ResponsiveLayoutService);
    options.bind(TYPES.INavigationSyncService).to(NavigationSyncService);
    options.bind(TYPES.IBeatOperationsService).to(BeatOperationsService);
    options
      .bind(TYPES.IKeyboardArrowAdjustmentService)
      .to(KeyboardArrowAdjustmentService);
    options.bind(TYPES.IUndoService).to(UndoService);
    options.bind(TYPES.IBuildConstructTabCoordinator).to(ConstructCoordinator);
    options.bind(TYPES.ITurnControlService).to(TurnControlService);

    // === OPTION PICKER SERVICES ===
    options.bind(TYPES.IOptionPickerSizingService).to(OptionSizer);
    options
      .bind(TYPES.IOptionPickerFilterPersistenceService)
      .to(FilterPersistenceService);
    options.bind(TYPES.IReversalChecker).to(ReversalChecker);
    options.bind(TYPES.IPositionAnalyzer).to(PositionAnalyzer);
    options.bind(TYPES.IOptionSorter).to(OptionSorter);
    options.bind(TYPES.IOptionFilter).to(OptionFilter);
    options.bind(TYPES.IOptionOrganizerService).to(OptionOrganizer);
    options.bind(TYPES.IOptionLoader).to(OptionLoader);
    options.bind(TYPES.ILayoutDetectionService).to(LayoutDetectionService);
    options
      .bind(TYPES.IOptionTransitionCoordinator)
      .to(OptionTransitionCoordinator);
    options.bind(TYPES.ISectionTitleFormatter).to(SectionTitleFormatter);

    // === START POSITION SERVICES ===
    options
      .bind(TYPES.IStartPositionService)
      .to(StartPositionService)
      .inSingletonScope();

    // === GESTURAL PATH BUILDER SERVICES === (January 2025)
    options
      .bind(TYPES.IHandPathDirectionDetector)
      .to(HandPathDirectionDetector);
    options.bind(TYPES.ISwipeDetectionService).to(SwipeDetectionService);
    options.bind(TYPES.IPathToMotionConverter).to(PathToMotionConverter);

    // === GENERATION SERVICES === (restored active services 2025-10-25)
    options.bind(TYPES.IBeatConverterService).to(BeatConverterService);
    options.bind(TYPES.IPictographFilterService).to(PictographFilterService);
    options.bind(TYPES.ITurnManagementService).to(TurnManagementService);
    // TurnIntensityLevelService provides UI-level turn intensity values
    // TurnIntensityManagerService is instantiated directly with constructor params for sequence generation
    options
      .bind(TYPES.ITurnIntensityManagerService)
      .to(TurnIntensityLevelService);
    options.bind(TYPES.ISequenceMetadataService).to(SequenceMetadataService);

    // New Focused Generation Services (composable, single-responsibility)
    options.bind(TYPES.IStartPositionSelector).to(StartPositionSelector);
    options.bind(TYPES.IRotationDirectionService).to(RotationDirectionService);
    options.bind(TYPES.ITurnAllocationCalculator).to(TurnAllocationCalculator);
    options
      .bind(TYPES.IBeatGenerationOrchestrator)
      .to(BeatGenerationOrchestrator);
    options.bind(TYPES.IPartialSequenceGenerator).to(PartialSequenceGenerator);

    // Circular Generation (CAP) Services
    options
      .bind(TYPES.IComplementaryLetterService)
      .to(ComplementaryLetterService);
    options
      .bind(TYPES.IRotatedEndPositionSelector)
      .to(RotatedEndPositionSelector);
    options.bind(TYPES.ICAPEndPositionSelector).to(CAPEndPositionSelector);
    options.bind(TYPES.IStrictRotatedCAPExecutor).to(StrictRotatedCAPExecutor);
    options
      .bind(TYPES.IStrictMirroredCAPExecutor)
      .to(StrictMirroredCAPExecutor);
    options.bind(TYPES.IStrictSwappedCAPExecutor).to(StrictSwappedCAPExecutor);
    options
      .bind(TYPES.IStrictComplementaryCAPExecutor)
      .to(StrictComplementaryCAPExecutor);
    options
      .bind(TYPES.IMirroredSwappedCAPExecutor)
      .to(MirroredSwappedCAPExecutor);
    options
      .bind(TYPES.ISwappedComplementaryCAPExecutor)
      .to(SwappedComplementaryCAPExecutor);
    options
      .bind(TYPES.IMirroredComplementaryCAPExecutor)
      .to(MirroredComplementaryCAPExecutor);
    options
      .bind(TYPES.IRotatedSwappedCAPExecutor)
      .to(RotatedSwappedCAPExecutor);
    options
      .bind(TYPES.IRotatedComplementaryCAPExecutor)
      .to(RotatedComplementaryCAPExecutor);
    options.bind(TYPES.ICAPExecutorSelector).to(CAPExecutorSelector);

    // Generation UI Services (SRP Refactoring - Dec 2024)
    options.bind(TYPES.ILevelConversionService).to(LevelConversionService);
    options
      .bind(TYPES.IResponsiveTypographyService)
      .to(ResponsiveTypographyService);
    options.bind(TYPES.ICardConfigurationService).to(CardConfigurationService);
    options.bind(TYPES.ICAPTypeService).to(CAPTypeService);

    // Generation Orchestration Services (SRP Refactoring - Dec 2024)
    options
      .bind(TYPES.IGenerationOrchestrationService)
      .to(GenerationOrchestrationService);

    // === BEAT GRID SERVICES ===
    // Note: BeatFallbackRenderer moved to render module

    // === WORKBENCH SERVICES ===
    options.bind(TYPES.IWorkbenchService).to(WorkbenchService);

    // === SEQUENCE SERVICES ===
    options.bind(TYPES.IReversalDetectionService).to(ReversalDetectionService);
    options.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
    options.bind(TYPES.ISequenceAnalysisService).to(SequenceAnalysisService);

    // Focused sequence services (refactored from monolithic SequenceStateService)
    options.bind(TYPES.IBeatNumberingService).to(BeatNumberingService);
    options
      .bind(TYPES.ISequenceValidationService)
      .to(SequenceValidationService);
    options
      .bind(TYPES.ISequenceStatisticsService)
      .to(SequenceStatisticsService);
    options
      .bind(TYPES.ISequenceTransformationService)
      .to(SequenceTransformationService);

    options.bind(TYPES.ISequenceExportService).to(SequenceExportService);
    options.bind(TYPES.ISequenceImportService).to(SequenceImportService);
    options.bind(TYPES.ISequenceService).to(SequenceService);
    options
      .bind(TYPES.ISequencePersistenceService)
      .to(SequencePersistenceService);
    options.bind(TYPES.ISequenceIndexService).to(SequenceIndexService);
    options.bind(TYPES.ISequenceDeletionService).to(SequenceDeletionService);
    options.bind(TYPES.ISequenceTransformService).to(SequenceTransformService);

    // === LAYOUT SERVICES ===
    // Note: PrintablePageLayoutService handled in word-card module
  }
);
