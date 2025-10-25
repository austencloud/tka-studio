import type { ContainerModuleLoadOptions } from "inversify";
import { ContainerModule } from "inversify";
import {
  CodexService,
  CodexLetterMappingRepo,
  CodexPictographUpdater,
} from "../../../modules/learn/codex/services/implementations";
import {
  QuizRepoManager,
  QuizSessionService,
} from "../../../modules/learn/quiz/services/implementations";
import { QuizGradingService } from "../../../modules/learn/quiz/services/QuizGradingService";
import { QuizFeedbackService } from "../../../modules/learn/quiz/services/QuizFeedbackService";
import { QuizAchievementService } from "../../../modules/learn/quiz/services/QuizAchievementService";
import { QuizFormatterService } from "../../../modules/learn/quiz/services/QuizFormatterService";
import {
  FlipBookService,
  PDFService,
} from "../../../modules/learn/read/services/implementations";
import { TYPES } from "../types";

export const learnModule = new ContainerModule(
  async (options: ContainerModuleLoadOptions) => {
    // === CODEX SERVICES ===
    options.bind(TYPES.ICodexLetterMappingRepo).to(CodexLetterMappingRepo);
    options.bind(TYPES.ICodexPictographUpdater).to(CodexPictographUpdater);
    options.bind(TYPES.ICodexService).to(CodexService);

    // === QUIZ SERVICES ===
    options.bind(TYPES.IQuizRepoManager).to(QuizRepoManager);
    options.bind(TYPES.IQuizSessionService).to(QuizSessionService);
    options.bind(TYPES.IQuizGradingService).to(QuizGradingService);
    options.bind(TYPES.IQuizFeedbackService).to(QuizFeedbackService);
    options.bind(TYPES.IQuizAchievementService).to(QuizAchievementService);
    options.bind(TYPES.IQuizFormatterService).to(QuizFormatterService);

    // === READ SERVICES ===
    options.bind(TYPES.IPDFService).to(PDFService);
    options.bind(TYPES.IFlipBookService).to(FlipBookService);
  }
);
