/**
 * CSV Data Service - Implementation (Updated for Global Data Access)
 *
 * Loads and manages CSV data for the modern web app.
 * Based on the legacy system's CSV loading approach.
 */

export interface CsvDataSet {
	diamondData: string;
	boxData: string;
}

export interface ParsedCsvRow {
	letter: string;
	startPos: string;
	endPos: string;
	timing: string;
	direction: string;
	blueMotionType: string;
	bluePropRotDir: string;
	blueStartLoc: string;
	blueEndLoc: string;
	redMotionType: string;
	redPropRotDir: string;
	redStartLoc: string;
	redEndLoc: string;
}

export class CsvDataService {
	private csvData: CsvDataSet | null = null;
	private parsedData: { diamond: ParsedCsvRow[]; box: ParsedCsvRow[] } | null = null;
	private isInitialized = false;

	constructor() {
		console.log('📊 CsvDataService initialized');
	}

	/**
	 * Load CSV data from multiple sources (global data or static files)
	 */
	async loadCsvData(): Promise<void> {
		if (this.isInitialized) {
			console.log('📊 CSV data already loaded');
			return;
		}

		try {
			// First try to get data from global window.csvData (set by layout)
			if (typeof window !== 'undefined' && (window as any).csvData) {
				this.csvData = (window as any).csvData;
			} else {
				// Fallback: Fetch CSV files from static directory
				const [diamondResponse, boxResponse] = await Promise.all([
					fetch('/DiamondPictographDataframe.csv'),
					fetch('/BoxPictographDataframe.csv'),
				]);

				if (!diamondResponse.ok || !boxResponse.ok) {
					throw new Error(
						`Failed to load CSV files: Diamond=${diamondResponse.status}, Box=${boxResponse.status}`
					);
				}

				const diamondData = await diamondResponse.text();
				const boxData = await boxResponse.text();

				this.csvData = { diamondData, boxData };
			}

			// Parse the CSV data
			this.parsedData = {
				diamond: this.parseCSV(this.csvData.diamondData),
				box: this.parseCSV(this.csvData.boxData),
			};

			this.isInitialized = true;

			console.log(
				`✅ CSV data loaded: ${this.parsedData.diamond.length} diamond, ${this.parsedData.box.length} box entries`
			);
		} catch (error) {
			console.error('❌ Error loading CSV data:', error);
			throw new Error(
				`Failed to load CSV data: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Get CSV data (similar to legacy layout data)
	 */
	getCsvData(): CsvDataSet | null {
		return this.csvData;
	}

	/**
	 * Get parsed data for a specific grid mode
	 */
	getParsedData(gridMode: 'diamond' | 'box'): ParsedCsvRow[] {
		if (!this.parsedData) {
			console.warn('⚠️ CSV data not parsed yet');
			return [];
		}
		return this.parsedData[gridMode];
	}

	/**
	 * Get available options for a given end position (like legacy OptionDataService)
	 */
	getNextOptions(endPosition: string, gridMode: 'diamond' | 'box' = 'diamond'): ParsedCsvRow[] {
		if (!this.parsedData) {
			console.warn('⚠️ CSV data not initialized');
			return [];
		}

		try {
			// Get the appropriate dataset based on grid mode
			const dataset = this.parsedData[gridMode];

			// Filter options where startPos matches the endPosition (positional continuity)
			const matchingOptions = dataset.filter((row) => row.startPos === endPosition);

			console.log(
				`🎯 Found ${matchingOptions.length} options for end position: ${endPosition} in ${gridMode} mode`
			);

			// Debug: Show first few matches
			if (matchingOptions.length > 0) {
				console.log(
					`🔍 Sample options:`,
					matchingOptions.slice(0, 3).map((opt) => ({
						letter: opt.letter,
						startPos: opt.startPos,
						endPos: opt.endPos,
						blueMotion: opt.blueMotionType,
						redMotion: opt.redMotionType,
					}))
				);
			}

			return matchingOptions;
		} catch (error) {
			console.error('❌ Error getting next options:', error);
			return [];
		}
	}

	/**
	 * Parse CSV text into array of objects (same as legacy)
	 */
	private parseCSV(csvText: string): ParsedCsvRow[] {
		const lines = csvText.trim().split('\n');
		if (lines.length < 2) return [];

		// Parse header
		const headers = lines[0].split(',').map((h) => h.trim());
		const data: ParsedCsvRow[] = [];

		// Parse each data row
		for (let i = 1; i < lines.length; i++) {
			const values = lines[i].split(',').map((v) => v.trim());
			const row: Record<string, string> = {};

			// Create row object
			headers.forEach((header, index) => {
				row[header] = values[index] || '';
			});

			// Type-safe conversion to ParsedCsvRow
			data.push({
				letter: row.letter || '',
				startPos: row.startPos || '',
				endPos: row.endPos || '',
				timing: row.timing || '',
				direction: row.direction || '',
				blueMotionType: row.blueMotionType || '',
				bluePropRotDir: row.bluePropRotDir || '',
				blueStartLoc: row.blueStartLoc || '',
				blueEndLoc: row.blueEndLoc || '',
				redMotionType: row.redMotionType || '',
				redPropRotDir: row.redPropRotDir || '',
				redStartLoc: row.redStartLoc || '',
				redEndLoc: row.redEndLoc || '',
			});
		}

		return data;
	}

	/**
	 * Get all available start positions for a given grid mode
	 */
	getAvailableStartPositions(gridMode: 'diamond' | 'box' = 'diamond'): string[] {
		if (!this.parsedData) return [];

		const dataset = this.parsedData[gridMode];
		const startPositions = [...new Set(dataset.map((row) => row.startPos))];
		return startPositions.sort();
	}

	/**
	 * Get all available end positions for a given grid mode
	 */
	getAvailableEndPositions(gridMode: 'diamond' | 'box' = 'diamond'): string[] {
		if (!this.parsedData) return [];

		const dataset = this.parsedData[gridMode];
		const endPositions = [...new Set(dataset.map((row) => row.endPos))];
		return endPositions.sort();
	}

	/**
	 * Get statistics about the loaded data
	 */
	getDataStats() {
		if (!this.parsedData) return null;

		return {
			diamond: {
				total: this.parsedData.diamond.length,
				letters: [...new Set(this.parsedData.diamond.map((row) => row.letter))].length,
				startPositions: this.getAvailableStartPositions('diamond').length,
				endPositions: this.getAvailableEndPositions('diamond').length,
			},
			box: {
				total: this.parsedData.box.length,
				letters: [...new Set(this.parsedData.box.map((row) => row.letter))].length,
				startPositions: this.getAvailableStartPositions('box').length,
				endPositions: this.getAvailableEndPositions('box').length,
			},
		};
	}

	/**
	 * Check if the service is initialized
	 */
	isReady(): boolean {
		return this.isInitialized && this.parsedData !== null;
	}

	/**
	 * Debug method to inspect specific position data
	 */
	debugPosition(position: string, gridMode: 'diamond' | 'box' = 'diamond'): void {
		if (!this.parsedData) {
			console.log('❌ CSV data not loaded');
			return;
		}

		const dataset = this.parsedData[gridMode];
		const positionData = {
			asStartPos: dataset.filter((row) => row.startPos === position),
			asEndPos: dataset.filter((row) => row.endPos === position),
		};

		console.log(`🔍 Position ${position} in ${gridMode} mode:`, {
			appearsAsStartPos: positionData.asStartPos.length,
			appearsAsEndPos: positionData.asEndPos.length,
			sampleAsStart: positionData.asStartPos.slice(0, 2),
			sampleAsEnd: positionData.asEndPos.slice(0, 2),
		});
	}
}
