/**
 * Complementary Letter Service Implementation
 *
 * Provides complementary letter mappings for CAP (Circular Arrangement Pattern) generation.
 * Uses the existing complementary letter mapping from the circular generation constants.
 */
import { injectable } from "inversify";
import { getComplementaryLetter } from "../../../circular/domain/constants/strict-cap-position-maps";
import type { IComplementaryLetterService } from "../contracts/IComplementaryLetterService";

@injectable()
export class ComplementaryLetterService implements IComplementaryLetterService {
  /**
   * Get the complementary letter for a given letter
   * @param letter - The input letter
   * @returns The complementary letter
   * @throws Error if no complementary mapping exists for the letter
   */
  getComplementaryLetter(letter: string): string {
    return getComplementaryLetter(letter);
  }
}
