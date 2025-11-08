/**
 * Admin Module - Barrel Export
 */

// Domain Models
export type {
  ChallengeScheduleEntry,
  SequenceSelection,
  ChallengeFormData,
} from "./domain/models";

// Service Contracts
export type { IAdminChallengeService } from "./services/contracts";

// Service Implementations
export { AdminChallengeService } from "./services/implementations";

// Components
export { default as AdminDashboard } from "./components/AdminDashboard.svelte";
export { default as DailyChallengeScheduler } from "./components/DailyChallengeScheduler.svelte";
export { default as ChallengeCalendar } from "./components/ChallengeCalendar.svelte";
export { default as SequenceBrowser } from "./components/SequenceBrowser.svelte";
