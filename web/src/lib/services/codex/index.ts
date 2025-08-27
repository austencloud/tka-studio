/**
 * Codex Service Module Index
 *
 * Clean exports for the refactored codex system.
 */

// Domain types
export type {
  LetterMapping,
  CodexLetter,
  LetterCategory,
  LetterRow,
  CodexConfiguration,
  LessonConfiguration,
  MotionType,
} from "$lib/domain/codex/types";

// Repositories
export {
  LetterMappingRepository,
  type ILetterMappingRepository,
} from "$lib/repositories/LetterMappingRepository";
export {
  LessonRepository,
  type ILessonRepository,
} from "$lib/repositories/LessonRepository";

// Services
// TODO: Re-enable when PictographQueryService is implemented
// export {
//   PictographQueryService,
//   type IPictographQueryService,
// } from "./PictographQueryService";
export {
  PictographOperationsService,
  type IPictographOperationsService,
  type PictographOperation,
} from "./PictographOperationsService";

// Main service
export { CodexService } from "./CodexService";
export type { ICodexService } from "../interfaces/application-interfaces";

// Migration helper
export { CodexServiceMigrationHelper } from "./CodexServiceMigrationHelper";

// Legacy service (for migration period)
export { CodexService as LegacyCodexService } from "./CodexService";
