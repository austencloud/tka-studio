import { GridMode } from '$lib/domain';

declare global {
	// Extend window typing for csvData injection
	interface Window {
		csvData?: CsvDataSet;
	}
}
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
	private parsedData: Record<GridMode, ParsedCsvRow[]> | null = null;
	private isInitialized = false;

	constructor() {
		// CsvDataService initialized
	}

	/**
	 * Load CSV data from multiple sources (global data or static files)
	 */
	async loadCsvData(): Promise<void> {
		if (this.isInitialized) {
			return;
		}

		try {
			// First try to get data from global window.csvData (set by layout)
			if (typeof window !== 'undefined' && window.csvData) {
				this.csvData = window.csvData;
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
			if (this.csvData) {
				this.parsedData = {
					[GridMode.DIAMOND]: this.parseCSV(this.csvData.diamondData),
					[GridMode.BOX]: this.parseCSV(this.csvData.boxData),
				};
			}

			this.isInitialized = true;
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
	getParsedData(gridMode: GridMode): ParsedCsvRow[] {
		if (!this.parsedData) {
			return [];
		}
		return this.parsedData[gridMode];
	}

	/**
	 * Get available options for a given end position (like legacy OptionDataService)
	 */
	getNextOptions(endPosition: string, gridMode: GridMode = GridMode.DIAMOND): ParsedCsvRow[] {
		if (!this.parsedData) {
			return [];
		}

		try {
			// Get the appropriate dataset based on grid mode
			const dataset = this.parsedData[gridMode];

			// Filter options where startPos matches the endPosition (positional continuity)
			const matchingOptions = dataset.filter((row) => row.startPos === endPosition);

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
		const headerLine = lines[0] ?? '';
		const headers = headerLine.split(',').map((h) => h.trim());
		const data: ParsedCsvRow[] = [];

		// Parse each data row
		for (let i = 1; i < lines.length; i++) {
			const line = lines[i] ?? '';
			const values = line.split(',').map((v) => v.trim());
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
	getAvailableStartPositions(gridMode: GridMode = GridMode.DIAMOND): string[] {
		if (!this.parsedData) return [];

		const dataset = this.parsedData[gridMode];
		const startPositions = [...new Set(dataset.map((row) => row.startPos))];
		return startPositions.sort();
	}

	/**
	 * Get all available end positions for a given grid mode
	 */
	getAvailableEndPositions(gridMode: GridMode = GridMode.DIAMOND): string[] {
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
			[GridMode.DIAMOND]: {
				total: this.parsedData.diamond.length,
				letters: [...new Set(this.parsedData.diamond.map((row) => row.letter))].length,
				startPositions: this.getAvailableStartPositions(GridMode.DIAMOND).length,
				endPositions: this.getAvailableEndPositions(GridMode.DIAMOND).length,
			},
			[GridMode.BOX]: {
				total: this.parsedData.box.length,
				letters: [...new Set(this.parsedData.box.map((row) => row.letter))].length,
				startPositions: this.getAvailableStartPositions(GridMode.BOX).length,
				endPositions: this.getAvailableEndPositions(GridMode.BOX).length,
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
	debugPosition(_position: string, gridMode: GridMode = GridMode.DIAMOND): void {
		if (!this.parsedData) {
			return;
		}

		// Intentionally minimal to avoid unused variable warnings
		void this.parsedData[gridMode];
	}
}
