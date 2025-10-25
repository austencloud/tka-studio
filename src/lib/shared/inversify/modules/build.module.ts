import { ContainerModule, type ContainerModuleLoadOptions } from "inversify";
import {
    BuildTabService,
    ConstructCoordinator,
    OptionSizer,
    ReversalDetectionService,
    SequenceDeletionService,
    SequenceDomainService,
    SequenceExportService,
    SequenceImportService,
    SequenceIndexService,
    SequencePersistenceService,
    SequenceService,
    SequenceTransformService,
    StartPositionService,
    WorkbenchService,
} from "../../../modules";
import { BuildTabLayoutService } from "../../../modules/build/shared/layout/services/BuildTabLayoutService";
import { BeatNumberingService } from "../../../modules/build/shared/services/implementations/BeatNumberingService";
import { SequenceStatisticsService } from "../../../modules/build/shared/services/implementations/SequenceStatisticsService";
import { SequenceTransformationService } from "../../../modules/build/shared/services/implementations/SequenceTransformationService";
import { SequenceValidationService } from "../../../modules/build/shared/services/implementations/SequenceValidationService";
import { UndoService } from "../../../modules/build/shared/services/implementations/UndoService";
// Refactored Generation Services
import {
    OptionFilter,
    OptionLoader,
    OptionOrganizer,
    OptionSorter,
    PositionAnalyzer,
    ReversalChecker,
} from "../../../modules/build/construct/option-picker/option-viewer/services/implementations";
import { FilterPersistenceService } from "../../../modules/build/construct/option-picker/services/FilterPersistenceService";
import { LayoutDetectionService } from "../../../modules/build/construct/option-picker/services/implementations/LayoutDetectionService";
import { TurnControlService } from "../../../modules/build/edit/services/TurnControlService";
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
    TurnManagementService
} from "../../../modules/build/generate/shared/services/implementations";
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
} from "../../../modules/build/generate/circular/services/implementations";
// Generation UI Services (SRP Refactoring - Dec 2024) - ACTIVE ONLY
import {
    CAPTypeService,
    CardConfigurationService,
    LevelConversionService,
    ResponsiveTypographyService,
} from "../../../modules/build/generate/shared/services/implementations";
import { TYPES } from "../types";

export const buildModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === BUILD TAB SERVICES ===
    options.bind(TYPES.IBuildTabService).to(BuildTabService);
    options.bind(TYPES.IBuildTabLayoutService).to(BuildTabLayoutService);
    options.bind(TYPES.IUndoService).to(UndoService);
    options.bind(TYPES.IConstructTabCoordinator).to(ConstructCoordinator);
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

    // === START POSITION SERVICES ===
    options
      .bind(TYPES.IStartPositionService)
      .to(StartPositionService)
      .inSingletonScope();

    // === GENERATION SERVICES === (restored active services 2025-10-25)
    options.bind(TYPES.IBeatConverterService).to(BeatConverterService);
    options.bind(TYPES.IPictographFilterService).to(PictographFilterService);
    options.bind(TYPES.ITurnManagementService).to(TurnManagementService);
    // TurnIntensityLevelService provides UI-level turn intensity values
    // TurnIntensityManagerService is instantiated directly with constructor params for sequence generation
    options.bind(TYPES.ITurnIntensityManagerService).to(TurnIntensityLevelService);
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
    options.bind(TYPES.IComplementaryLetterService).to(ComplementaryLetterService);
    options
      .bind(TYPES.IRotatedEndPositionSelector)
      .to(RotatedEndPositionSelector);
    options.bind(TYPES.ICAPEndPositionSelector).to(CAPEndPositionSelector);
    options.bind(TYPES.IStrictRotatedCAPExecutor).to(StrictRotatedCAPExecutor);
    options.bind(TYPES.IStrictMirroredCAPExecutor).to(StrictMirroredCAPExecutor);
    options.bind(TYPES.IStrictSwappedCAPExecutor).to(StrictSwappedCAPExecutor);
    options.bind(TYPES.IStrictComplementaryCAPExecutor).to(StrictComplementaryCAPExecutor);
    options.bind(TYPES.IMirroredSwappedCAPExecutor).to(MirroredSwappedCAPExecutor);
    options.bind(TYPES.ISwappedComplementaryCAPExecutor).to(SwappedComplementaryCAPExecutor);
    options.bind(TYPES.IMirroredComplementaryCAPExecutor).to(MirroredComplementaryCAPExecutor);
    options.bind(TYPES.IRotatedSwappedCAPExecutor).to(RotatedSwappedCAPExecutor);
    options.bind(TYPES.IRotatedComplementaryCAPExecutor).to(RotatedComplementaryCAPExecutor);
    options.bind(TYPES.ICAPExecutorSelector).to(CAPExecutorSelector);

    // Generation UI Services (SRP Refactoring - Dec 2024)
    options.bind(TYPES.ILevelConversionService).to(LevelConversionService);
    options.bind(TYPES.IResponsiveTypographyService).to(ResponsiveTypographyService);
    options.bind(TYPES.ICardConfigurationService).to(CardConfigurationService);
    options.bind(TYPES.ICAPTypeService).to(CAPTypeService);

    // Generation Orchestration Services (SRP Refactoring - Dec 2024)
    options.bind(TYPES.IGenerationOrchestrationService).to(GenerationOrchestrationService);

    // === BEAT GRID SERVICES ===
    // Note: BeatFallbackRenderer moved to render module

    // === WORKBENCH SERVICES ===
    options.bind(TYPES.IWorkbenchService).to(WorkbenchService);

    // === SEQUENCE SERVICES ===
    options.bind(TYPES.IReversalDetectionService).to(ReversalDetectionService);
    options.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);

    // Focused sequence services (refactored from monolithic SequenceStateService)
    options.bind(TYPES.IBeatNumberingService).to(BeatNumberingService);
    options.bind(TYPES.ISequenceValidationService).to(SequenceValidationService);
    options.bind(TYPES.ISequenceStatisticsService).to(SequenceStatisticsService);
    options.bind(TYPES.ISequenceTransformationService).to(SequenceTransformationService);

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
