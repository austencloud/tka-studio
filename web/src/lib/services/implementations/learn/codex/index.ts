/**
 * Codex Service Module Index
 *
 * Clean exports for the refactored codex system.
 */

// Domain types
export type {
  CodexConfiguration,
  CodexLetter,
  LessonConfiguration,
  LetterCategory,
  LetterMapping,
  LetterRow,
} from "$domain/learn/codex/types";

// Repositories
export {
  LetterMappingRepository,
  type ILetterMappingRepository,
} from "$domain/learn/codex/LetterMappingRepository";
export {
  LessonRepository,
  type ILessonRepository,
} from "$domain/learn/LessonRepository";

// Services
// TODO: Re-enable when PictographQueryService is implemented
// export {
//   PictographQueryService,
//   type IPictographQueryService,
// } from "./PictographQueryService";
export {
  PictographOperationsService,
  type IPictographOperationsService,
  type PictographTransformOperation,
} from "./PictographOperationsService";

// Main service
export { CodexService } from "./CodexService";

// Migration helper
export { CodexServiceMigrationHelper } from "./CodexServiceMigrationHelper";

// Legacy service (for migration period)
export { CodexService as LegacyCodexService } from "./CodexService";
