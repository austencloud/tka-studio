/**
 * CSV Loader Service Implementation
 *
 * Handles loading and caching of CSV data from static files or preloaded window data.
 * Provides a single source of truth for raw CSV content without parsing logic.
 */

import type { CsvDataSet } from "$shared";
import { GridMode } from "$shared";
import { injectable } from "inversify";
import type { ICSVLoader } from "../../contracts";

@injectable()
export class CsvLoader implements ICSVLoader {
  async loadCSVFile(filename: string): Promise<{
    success: boolean;
    data?: string;
    error?: string;
    source: "fetch" | "window" | "cache";
  }> {
    try {
      const csvData = await this.loadCsvData();

      // Determine which file was requested and return appropriate data
      if (filename.includes("Diamond") || filename.includes("diamond")) {
        return {
          success: true,
          data: csvData.diamondData,
          source: this.isWindowDataAvailable() ? "window" : "fetch",
        };
      } else if (filename.includes("Box") || filename.includes("box")) {
        return {
          success: true,
          data: csvData.boxData,
          source: this.isWindowDataAvailable() ? "window" : "fetch",
        };
      } else {
        return {
          success: false,
          error: `Unknown file: ${filename}`,
          source: "fetch",
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
        source: "fetch",
      };
    }
  }
  async loadCSVDataSet(): Promise<{
    success: boolean;
    data?: { diamondData: string; boxData: string };
    error?: string;
    sources: {
      diamond: "fetch" | "window" | "cache";
      box: "fetch" | "window" | "cache";
    };
  }> {
    try {
      const csvData = await this.loadCsvData();
      return {
        success: true,
        data: csvData,
        sources: {
          diamond: this.isWindowDataAvailable() ? "window" : "fetch",
          box: this.isWindowDataAvailable() ? "window" : "fetch",
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
        sources: {
          diamond: "fetch",
          box: "fetch",
        },
      };
    }
  }
  async loadCSVForGridMode(gridMode: GridMode): Promise<{
    success: boolean;
    data?: string;
    error?: string;
    source: "fetch" | "window" | "cache";
  }> {
    try {
      const csvData = await this.loadCsvData();

      // Return appropriate data based on grid mode
      let data: string;
      if (gridMode === GridMode.DIAMOND || gridMode === GridMode.SKEWED) {
        data = csvData.diamondData;
      } else if (gridMode === GridMode.BOX) {
        data = csvData.boxData;
      } else {
        return {
          success: false,
          error: `Unknown grid mode: ${gridMode}`,
          source: "fetch",
        };
      }

      return {
        success: true,
        data,
        source: this.isWindowDataAvailable() ? "window" : "fetch",
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
        source: "fetch",
      };
    }
  }

  isDataCached(): boolean {
    return this.isLoaded && this.csvData !== null;
  }
  private static readonly CSV_FILES = {
    DIAMOND: "/DiamondPictographDataframe.csv",
    BOX: "/BoxPictographDataframe.csv",
  } as const;

  private csvData: CsvDataSet | null = null;
  private isLoaded = false;

  /**
   * Loads CSV data with caching. Returns cached data on subsequent calls.
   * Attempts to load from window.csvData first, then falls back to static files.
   */
  async loadCsvData(): Promise<CsvDataSet> {
    if (this.isLoaded && this.csvData) {
      return this.csvData;
    }

    try {
      this.csvData = await this.loadFromWindowOrFiles();
      this.isLoaded = true;
      return this.csvData;
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      console.error("Failed to load CSV data:", message);
      throw new Error(`CSV loading failed: ${message}`);
    }
  }

  /**
   * Returns cached CSV data or null if not yet loaded.
   */
  getCsvData(): CsvDataSet | null {
    return this.csvData;
  }

  /**
   * Clears cached data and loading state.
   */
  clearCache(): void {
    this.csvData = null;
    this.isLoaded = false;
  }

  private async loadFromWindowOrFiles(): Promise<CsvDataSet> {
    if (this.isWindowDataAvailable()) {
      return window.csvData as CsvDataSet;
    }

    return this.loadFromStaticFiles();
  }

  private isWindowDataAvailable(): boolean {
    return window.csvData !== undefined && window.csvData !== null;
  }

  private async loadFromStaticFiles(): Promise<CsvDataSet> {
    const [diamondResponse, boxResponse] = await Promise.all([
      fetch(CsvLoader.CSV_FILES.DIAMOND),
      fetch(CsvLoader.CSV_FILES.BOX),
    ]);

    this.validateResponses(diamondResponse, boxResponse);

    const [diamondData, boxData] = await Promise.all([
      diamondResponse.text(),
      boxResponse.text(),
    ]);

    return {
      diamondData,
      boxData,
    };
  }

  private validateResponses(
    diamondResponse: Response,
    boxResponse: Response
  ): void {
    if (!diamondResponse.ok || !boxResponse.ok) {
      throw new Error(
        `HTTP error - Diamond: ${diamondResponse.status}, Box: ${boxResponse.status}`
      );
    }
  }
}
