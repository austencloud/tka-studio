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
} from "$domain";

// Repository interfaces
export type { ILessonRepository, ILetterMappingRepository } from "$domain";

// Repository implementations
export { LessonRepository } from "../LessonRepository";
export { LetterMappingRepository } from "../LetterMappingRepository";

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
