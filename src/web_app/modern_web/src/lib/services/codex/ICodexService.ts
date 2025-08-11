/**
 * Codex Service Interface
 * 
 * Defines the contract for codex data operations.
 */

import type { PictographData } from '$lib/domain/PictographData';

export interface ICodexService {
	/**
	 * Load all pictographs in alphabetical order
	 */
	loadAllPictographs(): Promise<PictographData[]>;
	
	/**
	 * Search pictographs by letter or pattern
	 */
	searchPictographs(searchTerm: string): Promise<PictographData[]>;
	
	/**
	 * Get a specific pictograph by letter
	 */
	getPictographByLetter(letter: string): Promise<PictographData | null>;
	
	/**
	 * Get pictographs for a specific lesson type
	 */
	getPictographsForLesson(lessonType: string): Promise<PictographData[]>;
}
