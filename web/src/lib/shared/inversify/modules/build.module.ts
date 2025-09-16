import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { OptionSizer } from "../../../modules";
import { OptionPickerService } from "../../../modules/build/construct/option-picker/option-viewer/services/implementations/OptionPickerService";
import { StartPositionService } from "../../../modules/build/construct/start-position-picker/services/implementations/StartPositionService";
import { PictographValidatorService } from "../../../modules/build/generate/services";
import { CSVPictographLoaderService } from "../../../modules/build/generate/services/implementations/CSVPictographLoader";
import { CSVPictographParser } from "../../../modules/build/generate/services/implementations/CSVPictographParser";
import { PictographGenerator } from "../../../modules/build/generate/services/implementations/PictographGenerator";
import { PositionPatternService } from "../../../modules/build/generate/services/implementations/PositionPatternService";
import { SequenceDomainService } from "../../../modules/build/generate/services/implementations/SequenceDomainService";
import { SequenceGenerationService } from "../../../modules/build/generate/services/implementations/SequenceGenerationService";
import {
    ReversalDetectionService,
    SequenceImportService,
    SequenceIndexService,
    SequencePersistenceService,
    SequenceService,
    SequenceStateService
} from "../../../modules/build/shared/services/implementations";
import { BuildTabService } from "../../../modules/build/shared/services/implementations/BuildTabService";
import { ConstructCoordinator } from "../../../modules/build/shared/services/implementations/ConstructCoordinator";

import {
    SequenceDeletionService,
    SequenceTransformService,
} from "../../../modules/build/workbench/sequence-toolkit/services/implementations";
import { BeatFallbackRenderer } from "../../../modules/build/workbench/shared/services";
import { WorkbenchService } from "../../../modules/build/workbench/shared/services/implementations/WorkbenchService";
import { PrintablePageLayoutService } from "../../../modules/word-card/services/implementations/PrintablePageLayoutService";
import { TYPES } from "../types";

export const buildModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === BUILD TAB SERVICES ===
    options.bind(TYPES.IBuildTabService).to(BuildTabService);
    options.bind(TYPES.IConstructTabCoordinator).to(ConstructCoordinator);

    // === OPTION PICKER SERVICES ===
    options.bind(TYPES.IOptionPickerService).to(OptionPickerService);
    options.bind(TYPES.IOptionPickerSizingService).to(OptionSizer);

    // === START POSITION SERVICES ===
    options
      .bind(TYPES.IStartPositionService)
      .to(StartPositionService)
      .inSingletonScope();

    // === GENERATION SERVICES ===
    options
      .bind(TYPES.ICSVPictographLoaderService)
      .to(CSVPictographLoaderService);
    options.bind(TYPES.ICSVPictographParserService).to(CSVPictographParser);
    options.bind(TYPES.IPictographGenerator).to(PictographGenerator);
    options.bind(TYPES.IPositionPatternService).to(PositionPatternService);
    options.bind(TYPES.ISequenceDomainService).to(SequenceDomainService);
    options
      .bind(TYPES.ISequenceGenerationService)
      .to(SequenceGenerationService);
    options
      .bind(TYPES.IPictographValidatorService)
      .to(PictographValidatorService);

    // === BEAT GRID SERVICES ===
    options.bind(TYPES.IBeatFallbackRenderer).to(BeatFallbackRenderer);

    // === WORKBENCH SERVICES ===
    options.bind(TYPES.IWorkbenchService).to(WorkbenchService);

    // === SEQUENCE SERVICES ===
    options.bind(TYPES.IReversalDetectionService).to(ReversalDetectionService);
    options.bind(TYPES.ISequenceImportService).to(SequenceImportService);
    options.bind(TYPES.ISequenceService).to(SequenceService);
    options.bind(TYPES.ISequenceStateService).to(SequenceStateService);
    options.bind(TYPES.ISequencePersistenceService).to(SequencePersistenceService);
    options.bind(TYPES.ISequenceIndexService).to(SequenceIndexService);
    options.bind(TYPES.ISequenceDeletionService).to(SequenceDeletionService);
    options.bind(TYPES.ISequenceTransformService).to(SequenceTransformService);

    // === LAYOUT SERVICES ===
    options
      .bind(TYPES.IPrintablePageLayoutService)
      .to(PrintablePageLayoutService);
  }
);
