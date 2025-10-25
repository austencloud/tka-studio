/**
 * Pictograph Generator Implementation
 *
 * Adapter service that wraps ILetterQueryHandler to provide pictograph generation functionality.
 * This service acts as a facade for the generate module.
 */

import type { ILetterQueryHandler, PictographData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IPictographGenerator } from "../contracts/IPictographGenerator";

@injectable()
export class PictographGenerator implements IPictographGenerator {
  constructor(
    @inject(TYPES.ILetterQueryHandler)
    private readonly letterQueryHandler: ILetterQueryHandler
  ) {}

  /**
   * Get all pictographs for a specific letter
   * TODO: This needs to be refactored to handle async ILetterQueryHandler methods
   */
  getPictographsByLetter(letter: string): PictographData[] | null {
    throw new Error("PictographGenerator.getPictographsByLetter not yet implemented - ILetterQueryHandler is async");
  }

  /**
   * Get all available pictographs across all letters
   * TODO: This needs to be refactored to handle async ILetterQueryHandler methods
   */
  getAllPictographs(): PictographData[] {
    throw new Error("PictographGenerator.getAllPictographs not yet implemented - ILetterQueryHandler is async");
  }
}
