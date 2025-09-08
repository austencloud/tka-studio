import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import { WordCardBatchProcessingService } from "../../../modules/word-card/services/implementations/WordCardBatchProcessingService";
import { WordCardCacheService } from "../../../modules/word-card/services/implementations/WordCardCacheService";
import { WordCardExportOrchestrator } from "../../../modules/word-card/services/implementations/WordCardExportOrchestrator";
import { WordCardExportProgressTracker } from "../../../modules/word-card/services/implementations/WordCardExportProgressTracker";
import { WordCardImageConversionService } from "../../../modules/word-card/services/implementations/WordCardImageConversionService";
import { WordCardImageGenerationService } from "../../../modules/word-card/services/implementations/WordCardImageGenerationService";
import { WordCardMetadataOverlayService } from "../../../modules/word-card/services/implementations/WordCardMetadataOverlayService";
import { WordCardSVGCompositionService } from "../../../modules/word-card/services/implementations/WordCardSVGCompositionService";
import { TYPES } from "../types";

export const wordCardModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === WORD CARD SERVICES ===
    options.bind(TYPES.IWordCardImageGenerationService).to(WordCardImageGenerationService);
    options.bind(TYPES.IWordCardImageConversionService).to(WordCardImageConversionService);
    options.bind(TYPES.IWordCardBatchProcessingService).to(WordCardBatchProcessingService);
    options.bind(TYPES.IWordCardExportProgressTracker).to(WordCardExportProgressTracker);
    options.bind(TYPES.IWordCardCacheService).to(WordCardCacheService);
    options.bind(TYPES.IWordCardExportOrchestrator).to(WordCardExportOrchestrator);
    options.bind(TYPES.IWordCardSVGCompositionService).to(WordCardSVGCompositionService);
    options.bind(TYPES.IWordCardMetadataOverlayService).to(WordCardMetadataOverlayService);
  }
);
