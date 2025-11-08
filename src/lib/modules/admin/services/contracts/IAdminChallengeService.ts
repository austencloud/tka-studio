/**
 * Admin Challenge Service Interface
 *
 * Handles admin operations for daily challenges
 */

import type { DailyChallenge } from "$shared/gamification/domain/models";
import type { SequenceData } from "$shared";
import type {
  ChallengeScheduleEntry,
  ChallengeFormData,
} from "../../domain/models";

export interface IAdminChallengeService {
  /**
   * Get all scheduled challenges for a date range
   */
  getScheduledChallenges(
    startDate: Date,
    endDate: Date
  ): Promise<ChallengeScheduleEntry[]>;

  /**
   * Create a new daily challenge
   */
  createChallenge(formData: ChallengeFormData): Promise<DailyChallenge>;

  /**
   * Update an existing daily challenge
   */
  updateChallenge(
    challengeId: string,
    formData: Partial<ChallengeFormData>
  ): Promise<DailyChallenge>;

  /**
   * Delete a daily challenge
   */
  deleteChallenge(challengeId: string): Promise<void>;

  /**
   * Get user's saved sequences (for selection)
   */
  getUserSequences(): Promise<SequenceData[]>;

  /**
   * Get a specific challenge by date
   */
  getChallengeByDate(date: string): Promise<DailyChallenge | null>;
}
