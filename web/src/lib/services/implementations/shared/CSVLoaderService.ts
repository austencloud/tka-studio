/**
 * CSVLoaderService - Centralized CSV loading utilities
 * 
 * Handles CSV file loading from multiple sources (static files, window.csvData)
 * with consistent error handling and caching strategies.
 */

import { GridMode } from "$lib/domain";

export interface CsvDataSet {
  diamondData: string;
  boxData: string;
}

export interface CSVLoadResult {
  success: boolean;
  data?: string;
  error?: string;
  source: 'fetch' | 'window' | 'cache';
}

export interface CSVDataSetResult {
  success: boolean;
  data?: CsvDataSet;
  error?: string;
  sources: {
    diamond: 'fetch' | 'window' | 'cache';
    box: 'fetch' | 'window' | 'cache';
  };
}

export interface ICSVLoaderService {
  loadCSVFile(filename: string): Promise<CSVLoadResult>;
  loadCSVDataSet(): Promise<CSVDataSetResult>;
  loadCSVForGridMode(gridMode: GridMode): Promise<CSVLoadResult>;
  clearCache(): void;
  isDataCached(): boolean;
}

declare global {
  interface Window {
    csvData?: CsvDataSet;
  }
}

export class CSVLoaderService implements ICSVLoaderService {
  private cache = new Map<string, string>();
  private dataSetCache: CsvDataSet | null = null;
  private loadingPromises = new Map<string, Promise<CSVLoadResult>>();

  /**
   * Load a single CSV file with caching and multiple source fallback
   */
  async loadCSVFile(filename: string): Promise<CSVLoadResult> {
    // Check cache first
    if (this.cache.has(filename)) {
      return {
        success: true,
        data: this.cache.get(filename)!,
        source: 'cache'
      };
    }

    // Check if already loading to prevent duplicate requests
    if (this.loadingPromises.has(filename)) {
      return await this.loadingPromises.get(filename)!;
    }

    // Create loading promise
    const loadingPromise = this.performCSVLoad(filename);
    this.loadingPromises.set(filename, loadingPromise);

    try {
      const result = await loadingPromise;
      
      // Cache successful results
      if (result.success && result.data) {
        this.cache.set(filename, result.data);
      }

      return result;
    } finally {
      // Clean up loading promise
      this.loadingPromises.delete(filename);
    }
  }

  /**
   * Load complete CSV dataset (diamond + box)
   */
  async loadCSVDataSet(): Promise<CSVDataSetResult> {
    // Check cache first
    if (this.dataSetCache) {
      return {
        success: true,
        data: this.dataSetCache,
        sources: { diamond: 'cache', box: 'cache' }
      };
    }

    try {
      // Try to get data from global window.csvData first (set by layout)
      if (typeof window !== "undefined" && window.csvData) {
        this.dataSetCache = window.csvData;
        return {
          success: true,
          data: this.dataSetCache,
          sources: { diamond: 'window', box: 'window' }
        };
      }

      // Fallback: Load both files from static directory
      const [diamondResult, boxResult] = await Promise.all([
        this.loadCSVFile("DiamondPictographDataframe.csv"),
        this.loadCSVFile("BoxPictographDataframe.csv")
      ]);

      if (!diamondResult.success || !boxResult.success) {
        return {
          success: false,
          error: `Failed to load CSV files: Diamond=${diamondResult.error || 'unknown'}, Box=${boxResult.error || 'unknown'}`,
          sources: { diamond: 'fetch', box: 'fetch' }
        };
      }

      this.dataSetCache = {
        diamondData: diamondResult.data!,
        boxData: boxResult.data!
      };

      return {
        success: true,
        data: this.dataSetCache,
        sources: { 
          diamond: diamondResult.source, 
          box: boxResult.source 
        }
      };

    } catch (error) {
      return {
        success: false,
        error: `Failed to load CSV dataset: ${error instanceof Error ? error.message : 'Unknown error'}`,
        sources: { diamond: 'fetch', box: 'fetch' }
      };
    }
  }

  /**
   * Load CSV for specific grid mode
   */
  async loadCSVForGridMode(gridMode: GridMode): Promise<CSVLoadResult> {
    const dataSetResult = await this.loadCSVDataSet();
    
    if (!dataSetResult.success || !dataSetResult.data) {
      return {
        success: false,
        error: dataSetResult.error || 'Failed to load CSV dataset',
        source: 'fetch'
      };
    }

    const data = gridMode === GridMode.DIAMOND 
      ? dataSetResult.data.diamondData 
      : dataSetResult.data.boxData;

    return {
      success: true,
      data,
      source: dataSetResult.sources[gridMode === GridMode.DIAMOND ? 'diamond' : 'box']
    };
  }

  /**
   * Clear all caches
   */
  clearCache(): void {
    this.cache.clear();
    this.dataSetCache = null;
    this.loadingPromises.clear();
  }

  /**
   * Check if data is cached
   */
  isDataCached(): boolean {
    return this.dataSetCache !== null;
  }

  /**
   * Perform the actual CSV loading with error handling
   */
  private async performCSVLoad(filename: string): Promise<CSVLoadResult> {
    try {
      // Construct URL for static file
      const url = filename.startsWith('/') ? filename : `/${filename}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        return {
          success: false,
          error: `HTTP ${response.status}: ${response.statusText}`,
          source: 'fetch'
        };
      }

      const data = await response.text();
      
      if (!data || data.trim().length === 0) {
        return {
          success: false,
          error: 'CSV file is empty',
          source: 'fetch'
        };
      }

      return {
        success: true,
        data,
        source: 'fetch'
      };

    } catch (error) {
      return {
        success: false,
        error: `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        source: 'fetch'
      };
    }
  }

  /**
   * Get cache statistics for debugging
   */
  getCacheStats(): { 
    filesCached: number; 
    dataSetCached: boolean; 
    activeLoads: number;
    cacheKeys: string[];
  } {
    return {
      filesCached: this.cache.size,
      dataSetCached: this.dataSetCache !== null,
      activeLoads: this.loadingPromises.size,
      cacheKeys: Array.from(this.cache.keys())
    };
  }

  /**
   * Preload common CSV files
   */
  async preloadCommonFiles(): Promise<void> {
    try {
      await Promise.all([
        this.loadCSVFile("DiamondPictographDataframe.csv"),
        this.loadCSVFile("BoxPictographDataframe.csv")
      ]);
    } catch (error) {
      console.warn("⚠️ Failed to preload CSV files:", error);
    }
  }
}
