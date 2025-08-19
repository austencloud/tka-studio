/**
 * CSV Movement Loader Service - Loads and groups movement data from CSV
 *
 * Loads the BoxPictographDataframe.csv file and provides grouped access to movement data.
 * Integrates with existing CSV loading infrastructure.
 */

import type { MovementData } from '$lib/domain/MovementData';
import { CSVMovementParserService } from './CSVMovementParserService';

interface CSVRow {
  letter: string;
  startPosition: string;
  endPosition: string;
  timing: string;
  direction: string;
  blueMotionType: string;
  blueRotationDirection: string;
  blueStartLocation: string;
  blueEndLocation: string;
  redMotionType: string;
  redRotationDirection: string;
  redStartLocation: string;
  redEndLocation: string;
}

export class CSVMovementLoaderService {
  private csvData: CSVRow[] | null = null;
  private letterGroups: Record<string, MovementData[]> | null = null;
  private readonly parser: CSVMovementParserService;

  constructor() {
    this.parser = new CSVMovementParserService();
  }

  /**
   * Load and parse the CSV data
   */
  async loadCSVData(): Promise<void> {
    if (this.csvData) {
      return; // Already loaded
    }

    try {
      // Use the existing CSV loader service pattern
      const response = await fetch('/BoxPictographDataframe.csv');
      if (!response.ok) {
        throw new Error(`Failed to load CSV: ${response.statusText}`);
      }
      
      const csvText = await response.text();
      
      // Parse CSV manually since we need exact control
      const lines = csvText.trim().split('\n');
      const headers = lines[0].split(',');
      
      this.csvData = lines.slice(1).map(line => {
        const values = this.parseCSVLine(line);
        const row: any = {};
        headers.forEach((header, i) => {
          row[header] = values[i]?.trim() || '';
        });
        return row as CSVRow;
      }).filter(row => this.parser.validateCSVRow(row));

      // Group by letter and parse to MovementData
      this.letterGroups = {};
      this.csvData.forEach(row => {
        if (!this.letterGroups![row.letter]) {
          this.letterGroups![row.letter] = [];
        }
        
        const movement = this.parser.parseCSVRowToMovement(row);
        this.letterGroups![row.letter].push(movement);
      });

      console.log(`Loaded ${this.csvData.length} movements for ${Object.keys(this.letterGroups).length} letters`);
      
    } catch (error) {
      console.error('Failed to load CSV movement data:', error);
      throw new Error(`CSV loading failed: ${error}`);
    }
  }

  /**
   * Get movements for a specific letter
   */
  async getMovementsForLetter(letter: string): Promise<MovementData[]> {
    await this.loadCSVData();
    
    const movements = this.letterGroups?.[letter] || [];
    if (movements.length === 0) {
      console.warn(`No movements found for letter: ${letter}`);
    }
    
    return movements;
  }

  /**
   * Get all available letters
   */
  async getAvailableLetters(): Promise<string[]> {
    await this.loadCSVData();
    return Object.keys(this.letterGroups || {}).sort();
  }

  /**
   * Get movement counts per letter
   */
  async getMovementCounts(): Promise<Record<string, number>> {
    await this.loadCSVData();
    
    const counts: Record<string, number> = {};
    Object.entries(this.letterGroups || {}).forEach(([letter, movements]) => {
      counts[letter] = movements.length;
    });
    
    return counts;
  }

  /**
   * Parse a CSV line handling quoted values
   */
  private parseCSVLine(line: string): string[] {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        result.push(current);
        current = '';
      } else {
        current += char;
      }
    }
    
    result.push(current);
    return result;
  }
}
