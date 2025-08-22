/**
 * CSV Loader Service
 *
 * Handles loading and caching of CSV data from static files or preloaded window data.
 * Provides a single source of truth for raw CSV content without parsing logic.
 */

export interface CsvDataSet {
  diamondData: string;
  boxData: string;
}

export interface ICsvLoaderService {
  loadCsvData(): Promise<CsvDataSet>;
  getCsvData(): CsvDataSet | null;
  clearCache(): void;
}

export class CsvLoaderService implements ICsvLoaderService {
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
      console.log("CSV data loaded successfully");
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
    console.log("CSV cache cleared");
  }

  private async loadFromWindowOrFiles(): Promise<CsvDataSet> {
    if (this.isWindowDataAvailable()) {
      console.log("Loading CSV data from window.csvData");
      return window.csvData as CsvDataSet;
    }

    console.log("Loading CSV data from static files");
    return this.loadFromStaticFiles();
  }

  private isWindowDataAvailable(): boolean {
    return (
      typeof window !== "undefined" &&
      window.csvData !== undefined &&
      window.csvData !== null
    );
  }

  private async loadFromStaticFiles(): Promise<CsvDataSet> {
    const [diamondResponse, boxResponse] = await Promise.all([
      fetch(CsvLoaderService.CSV_FILES.DIAMOND),
      fetch(CsvLoaderService.CSV_FILES.BOX),
    ]);

    this.validateResponses(diamondResponse, boxResponse);

    const [diamondData, boxData] = await Promise.all([
      diamondResponse.text(),
      boxResponse.text(),
    ]);

    return { diamondData, boxData };
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
