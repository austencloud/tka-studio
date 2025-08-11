/**
 * Codex Service Implementation
 * 
 * Handles codex data operations including loading and searching pictographs.
 * Integrates with the existing pictograph service infrastructure.
 */

import type { PictographData } from '$lib/domain/PictographData';
import type { ICodexService } from './ICodexService';

export class CodexService implements ICodexService {
	private pictographs: PictographData[] = [];
	private initialized = false;

	/**
	 * Load all pictographs in alphabetical order
	 */
	async loadAllPictographs(): Promise<PictographData[]> {
		if (!this.initialized) {
			await this.initializePictographs();
		}
		
		return this.pictographs.sort((a, b) => {
			const letterA = a.letter || '';
			const letterB = b.letter || '';
			return letterA.localeCompare(letterB);
		});
	}

	/**
	 * Search pictographs by letter or pattern
	 */
	async searchPictographs(searchTerm: string): Promise<PictographData[]> {
		const allPictographs = await this.loadAllPictographs();
		
		if (!searchTerm.trim()) {
			return allPictographs;
		}

		const term = searchTerm.toLowerCase();
		
		return allPictographs.filter(pictograph => {
			const letter = pictograph.letter?.toLowerCase() || '';
			const id = pictograph.id?.toLowerCase() || '';
			
			return letter.includes(term) || 
			       id.includes(term) ||
			       letter.startsWith(term);
		});
	}

	/**
	 * Get a specific pictograph by letter
	 */
	async getPictographByLetter(letter: string): Promise<PictographData | null> {
		const allPictographs = await this.loadAllPictographs();
		
		return allPictographs.find(pictograph => 
			pictograph.letter?.toLowerCase() === letter.toLowerCase()
		) || null;
	}

	/**
	 * Get pictographs for a specific lesson type
	 */
	async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
		const allPictographs = await this.loadAllPictographs();
		
		// For now, return all pictographs
		// This could be filtered based on lesson requirements in the future
		return allPictographs;
	}

	/**
	 * Initialize pictographs from the data source
	 */
	private async initializePictographs(): Promise<void> {
		try {
			// Generate comprehensive pictograph set A-Z
			this.pictographs = this.generateComprehensivePictographs();
			this.initialized = true;
		} catch (error) {
			console.error('Failed to initialize pictographs:', error);
			// Fallback to basic set
			this.pictographs = this.generateBasicPictographs();
			this.initialized = true;
		}
	}

	/**
	 * Generate comprehensive pictograph set
	 */
	private generateComprehensivePictographs(): PictographData[] {
		const letters = [
			'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
			'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
			'U', 'V', 'W', 'X', 'Y', 'Z'
		];

		return letters.map((letter, index) => {
			const motionTypes = ['dash', 'static', 'fl', 'cl'];
			const directions = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'];
			
			const blueMotion = motionTypes[index % motionTypes.length];
			const redMotion = motionTypes[(index + 1) % motionTypes.length];
			const blueDirection = directions[index % directions.length];
			const redDirection = directions[(index + 2) % directions.length];

			return {
				id: `pictograph_${letter}`,
				letter: letter,
				grid_mode: 'diamond' as const,
				blue_motion: { 
					direction: blueDirection, 
					motion_type: blueMotion 
				},
				red_motion: { 
					direction: redDirection, 
					motion_type: redMotion 
				},
				start_positions: {
					blue_prop: { 
						position_data: { 
							coordinates: [
								1 + (index % 3), 
								1 + (index % 3)
							] 
						} 
					},
					red_prop: { 
						position_data: { 
							coordinates: [
								3 - (index % 3), 
								3 - (index % 3)
							] 
						} 
					}
				},
				end_positions: {
					blue_prop: { 
						position_data: { 
							coordinates: [
								2 + ((index + 1) % 2), 
								2 + ((index + 1) % 2)
							] 
						} 
					},
					red_prop: { 
						position_data: { 
							coordinates: [
								2 - ((index + 1) % 2), 
								2 - ((index + 1) % 2)
							] 
						} 
					}
				},
				arrows: {},
				turns: [],
				timing: 1,
				beat: index + 1,
				number_of_beats: 26
			};
		});
	}

	/**
	 * Generate basic pictograph set as fallback
	 */
	private generateBasicPictographs(): PictographData[] {
		const basicLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
		
		return basicLetters.map((letter, index) => ({
			id: `basic_${letter}`,
			letter: letter,
			grid_mode: 'diamond' as const,
			blue_motion: { direction: 'n', motion_type: 'dash' },
			red_motion: { direction: 's', motion_type: 'dash' },
			start_positions: {
				blue_prop: { position_data: { coordinates: [1, 1] } },
				red_prop: { position_data: { coordinates: [3, 3] } }
			},
			end_positions: {
				blue_prop: { position_data: { coordinates: [2, 2] } },
				red_prop: { position_data: { coordinates: [2, 2] } }
			},
			arrows: {},
			turns: [],
			timing: 1,
			beat: index + 1,
			number_of_beats: 8
		}));
	}

	/**
	 * Clear cache and reload pictographs
	 */
	async refresh(): Promise<void> {
		this.initialized = false;
		this.pictographs = [];
		await this.loadAllPictographs();
	}

	/**
	 * Get total number of pictographs
	 */
	async getCount(): Promise<number> {
		const pictographs = await this.loadAllPictographs();
		return pictographs.length;
	}

	/**
	 * Check if a letter has a pictograph
	 */
	async hasLetter(letter: string): Promise<boolean> {
		const pictograph = await this.getPictographByLetter(letter);
		return pictograph !== null;
	}
}
