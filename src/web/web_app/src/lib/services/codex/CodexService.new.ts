/**
 * Codex Service Implementation
 *
 * Handles codex data operations with specific pictograph mapping like the desktop app.
 * Only loads the specific pictographs defined in the codex mapping (39 letters).
 */

import { GridMode } from '$lib/domain';
import type { PictographData } from '$lib/domain/PictographData';
import { CsvDataService, type ParsedCsvRow } from '../implementations/CsvDataService';
import { OptionDataService } from '../implementations/OptionDataService';
import type { ICodexService } from './ICodexService';

// Codex letter mapping (from desktop app's CodexDataService)
const CODEX_LETTER_MAPPING = {
	// A-Z Basic letters
	A: { startPos: 'alpha1', endPos: 'alpha3', blueMotion: 'pro', redMotion: 'pro' },
	B: { startPos: 'alpha1', endPos: 'alpha3', blueMotion: 'anti', redMotion: 'anti' },
	C: { startPos: 'alpha1', endPos: 'alpha3', blueMotion: 'anti', redMotion: 'pro' },
	D: { startPos: 'beta1', endPos: 'alpha3', blueMotion: 'pro', redMotion: 'pro' },
	E: { startPos: 'beta1', endPos: 'alpha3', blueMotion: 'anti', redMotion: 'anti' },
	F: { startPos: 'beta1', endPos: 'alpha3', blueMotion: 'anti', redMotion: 'pro' },
	G: { startPos: 'beta3', endPos: 'beta5', blueMotion: 'pro', redMotion: 'pro' },
	H: { startPos: 'beta3', endPos: 'beta5', blueMotion: 'anti', redMotion: 'anti' },
	I: { startPos: 'beta3', endPos: 'beta5', blueMotion: 'anti', redMotion: 'pro' },
	J: { startPos: 'alpha3', endPos: 'beta5', blueMotion: 'pro', redMotion: 'pro' },
	K: { startPos: 'alpha3', endPos: 'beta5', blueMotion: 'anti', redMotion: 'anti' },
	L: { startPos: 'alpha3', endPos: 'beta5', blueMotion: 'anti', redMotion: 'pro' },
	M: { startPos: 'gamma11', endPos: 'gamma1', blueMotion: 'pro', redMotion: 'pro' },
	N: { startPos: 'gamma11', endPos: 'gamma1', blueMotion: 'anti', redMotion: 'anti' },
	O: { startPos: 'gamma11', endPos: 'gamma1', blueMotion: 'anti', redMotion: 'pro' },
	P: { startPos: 'gamma1', endPos: 'gamma15', blueMotion: 'pro', redMotion: 'pro' },
	Q: { startPos: 'gamma1', endPos: 'gamma15', blueMotion: 'anti', redMotion: 'anti' },
	R: { startPos: 'gamma1', endPos: 'gamma15', blueMotion: 'anti', redMotion: 'pro' },
	S: { startPos: 'gamma13', endPos: 'gamma11', blueMotion: 'pro', redMotion: 'pro' },
	T: { startPos: 'gamma13', endPos: 'gamma11', blueMotion: 'anti', redMotion: 'anti' },
	U: { startPos: 'gamma13', endPos: 'gamma11', blueMotion: 'anti', redMotion: 'pro' },
	V: { startPos: 'gamma13', endPos: 'gamma11', blueMotion: 'pro', redMotion: 'anti' },
	W: { startPos: 'gamma13', endPos: 'alpha3', blueMotion: 'static', redMotion: 'pro' },
	X: { startPos: 'gamma13', endPos: 'alpha3', blueMotion: 'static', redMotion: 'anti' },
	Y: { startPos: 'gamma11', endPos: 'beta5', blueMotion: 'static', redMotion: 'pro' },
	Z: { startPos: 'gamma11', endPos: 'beta5', blueMotion: 'static', redMotion: 'anti' },

	// Greek letters
	Σ: { startPos: 'alpha3', endPos: 'gamma13', blueMotion: 'static', redMotion: 'pro' },
	Δ: { startPos: 'alpha3', endPos: 'gamma13', blueMotion: 'static', redMotion: 'anti' },
	θ: { startPos: 'beta5', endPos: 'gamma11', blueMotion: 'static', redMotion: 'pro' },
	Ω: { startPos: 'beta5', endPos: 'gamma11', blueMotion: 'static', redMotion: 'anti' },

	// Dash variants
	'W-': { startPos: 'gamma5', endPos: 'alpha3', blueMotion: 'dash', redMotion: 'pro' },
	'X-': { startPos: 'gamma5', endPos: 'alpha3', blueMotion: 'dash', redMotion: 'anti' },
	'Y-': { startPos: 'gamma3', endPos: 'beta5', blueMotion: 'dash', redMotion: 'pro' },
	'Z-': { startPos: 'gamma3', endPos: 'beta5', blueMotion: 'dash', redMotion: 'anti' },
	'Σ-': { startPos: 'beta3', endPos: 'gamma13', blueMotion: 'dash', redMotion: 'pro' },
	'Δ-': { startPos: 'beta3', endPos: 'gamma13', blueMotion: 'dash', redMotion: 'anti' },
	'θ-': { startPos: 'alpha5', endPos: 'gamma11', blueMotion: 'dash', redMotion: 'pro' },
	'Ω-': { startPos: 'alpha5', endPos: 'gamma11', blueMotion: 'dash', redMotion: 'anti' },

	// Special letters
	Φ: { startPos: 'beta7', endPos: 'alpha3', blueMotion: 'static', redMotion: 'dash' },
	Ψ: { startPos: 'alpha1', endPos: 'beta5', blueMotion: 'static', redMotion: 'dash' },
	Λ: { startPos: 'gamma7', endPos: 'gamma11', blueMotion: 'static', redMotion: 'dash' },
} as const;

export class CodexService implements ICodexService {
	private csvDataService: CsvDataService;
	private optionDataService: OptionDataService;
	private initialized = false;
	private codexPictographs: PictographData[] = [];

	constructor() {
		this.csvDataService = new CsvDataService();
		this.optionDataService = new OptionDataService();
		console.log('🔧 CodexService initialized with specific letter mapping');
	}

	/**
	 * Load all pictographs in alphabetical order
	 */
	async loadAllPictographs(): Promise<PictographData[]> {
		if (!this.initialized) {
			await this.initializePictographs();
		}

		return [...this.codexPictographs].sort((a, b) => {
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

		return allPictographs.filter((pictograph) => {
			const letter = pictograph.letter?.toLowerCase() || '';
			const id = pictograph.id?.toLowerCase() || '';

			return letter.includes(term) || id.includes(term) || letter.startsWith(term);
		});
	}

	/**
	 * Get a specific pictograph by letter
	 */
	async getPictographByLetter(letter: string): Promise<PictographData | null> {
		const allPictographs = await this.loadAllPictographs();

		return (
			allPictographs.find(
				(pictograph) => pictograph.letter?.toLowerCase() === letter.toLowerCase()
			) || null
		);
	}

	/**
	 * Get pictographs for a specific lesson type
	 */
	async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
		const allPictographs = await this.loadAllPictographs();

		// For now, return all pictographs
		// This could be filtered based on lesson requirements in the future
		console.log(`📚 Getting pictographs for lesson type: ${lessonType}`);
		return allPictographs;
	}

	/**
	 * Initialize pictographs from CSV data using codex mapping
	 */
	private async initializePictographs(): Promise<void> {
		try {
			// Load real CSV data using existing infrastructure
			await this.csvDataService.loadCsvData();

			// Get specific pictographs from both grid modes based on mapping
			this.codexPictographs = [
				...this.getCodexPictographsForGridMode(GridMode.DIAMOND),
				...this.getCodexPictographsForGridMode(GridMode.BOX),
			];

			this.initialized = true;
			console.log(
				`✅ CodexService initialized with ${this.codexPictographs.length} specific pictographs from mapping`
			);
		} catch (error) {
			console.error('❌ Failed to initialize CodexService:', error);
			this.initialized = false;
		}
	}

	/**
	 * Get codex pictographs for a specific grid mode using the letter mapping
	 */
	private getCodexPictographsForGridMode(gridMode: GridMode): PictographData[] {
		const csvRows = this.csvDataService.getParsedData(gridMode);
		const codexPictographs: PictographData[] = [];

		// For each letter in our codex mapping, find matching CSV row
		Object.entries(CODEX_LETTER_MAPPING).forEach(([letter, mapping]) => {
			const matchingRow = csvRows.find(
				(row) =>
					row.letter === letter &&
					row.startPos === mapping.startPos &&
					row.endPos === mapping.endPos &&
					row.blueMotionType === mapping.blueMotion &&
					row.redMotionType === mapping.redMotion
			);

			if (matchingRow) {
				const pictograph = this.convertCsvRowToPictographData(
					matchingRow,
					gridMode,
					codexPictographs.length // Use codex index for unique IDs
				);
				if (pictograph) {
					codexPictographs.push(pictograph);
				}
			} else {
				console.warn(`⚠️ No CSV data found for codex letter ${letter} in ${gridMode} mode`);
			}
		});

		return codexPictographs;
	}

	/**
	 * Convert CSV row to PictographData using existing infrastructure
	 */
	private convertCsvRowToPictographData(
		row: ParsedCsvRow,
		gridMode: GridMode,
		index: number
	): PictographData | null {
		try {
			// Use the public conversion method from OptionDataService
			return this.optionDataService.convertCsvRowToPictographData(row, gridMode, index);
		} catch (error) {
			console.error('❌ Error converting CSV row to PictographData:', error, row);
			return null;
		}
	}
}
