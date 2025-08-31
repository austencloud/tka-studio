// @ts-nocheck
/**
 * Clean Metadata Testing State Manager
 *
 * This replaces the 765-line metadata-tester-state.svelte.ts monolith with
 * a clean, focused state manager using Svelte 5 runes and dependency injection.
 */
import type {
  BatchAnalysisConfig,
  BatchAnalysisResult,
  MetadataAnalysisResult,
  MetadataStats,
  SequenceFile,
  ThumbnailFile,
} from "$lib/domain/metadata-testing/types";
import { BatchAnalysisService } from "./BatchAnalysisService";
import { MetadataAnalysisService } from "./MetadataAnalysisService";
import { MetadataExtractionService } from "./MetadataExtractionService";
import { SequenceDiscoveryService } from "./SequenceDiscoveryService";

interface SummaryStats {
  totalSequences: number;
  healthySequences: number;
  unhealthySequences: number;
  averageHealthScore: number;
  totalErrors: number;
  totalWarnings: number;
}

interface MetadataTestingState {
  // Discovery state
  thumbnails: ThumbnailFile[];
  filteredThumbnails: ThumbnailFile[];
  selectedThumbnails: ThumbnailFile[];

  // Analysis state
  analysisResults: MetadataAnalysisResult[];
  batchResults: BatchAnalysisResult | null;
  currentAnalysis: MetadataAnalysisResult | null;

  // UI state
  isDiscovering: boolean;
  isAnalyzing: boolean;
  analysisProgress: number;
  currentAnalysisFile: string;
  error: string | null; // Legacy compatibility property

  // Config
  batchConfig: BatchAnalysisConfig;

  // Filters
  searchQuery: string;
  showOnlyErrors: boolean;
  showOnlyWarnings: boolean;
  healthScoreFilter: { min: number; max: number };
}

export class MetadataTestingStateManager {
  private discoveryService: SequenceDiscoveryService;
  private extractionService: MetadataExtractionService;
  private analysisService: MetadataAnalysisService;
  private batchService: BatchAnalysisService;

  // State using plain objects (compatible with tests)
  private _state: MetadataTestingState = {
    thumbnails: [],
    filteredThumbnails: [],
    selectedThumbnails: [],
    analysisResults: [],
    batchResults: null,
    currentAnalysis: null,
    isDiscovering: false,
    isAnalyzing: false,
    analysisProgress: 0,
    currentAnalysisFile: "",
    error: null,
    batchConfig: {
      batchSize: 10,
      delayMs: 100,
      exportFormat: "json",
    },
    searchQuery: "",
    showOnlyErrors: false,
    showOnlyWarnings: false,
    healthScoreFilter: { min: 0, max: 100 },
  };

  // Derived state using getters (compatible with tests)
  public get filteredResults(): MetadataAnalysisResult[] {
    return this.filterResults(this._state);
  }

  public get summaryStats(): SummaryStats {
    return this.calculateSummaryStats(this._state);
  }

  // Getter for the state (for external access)
  public get state(): MetadataTestingState {
    return this._state;
  }

  constructor() {
    // Initialize services
    this.discoveryService = new SequenceDiscoveryService();
    this.extractionService = new MetadataExtractionService();
    this.analysisService = new MetadataAnalysisService();
    this.batchService = new BatchAnalysisService(
      this.extractionService,
      this.analysisService
    );
  }

  // Discovery Methods
  async discoverSequences(): Promise<void> {
    this.updateState((state) => ({
      ...state,
      isDiscovering: true,
      error: null,
    }));

    try {
      const thumbnails = await this.discoveryService.discoverSequences();
      this.updateState((state) => ({
        ...state,
        thumbnails,
        filteredThumbnails: this.applySearchFilter(
          thumbnails,
          state.searchQuery
        ),
        isDiscovering: false,
        error: null,
      }));
    } catch (error) {
      console.error("Failed to discover sequences:", error);
      this.updateState((state) => ({
        ...state,
        isDiscovering: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to discover sequences",
      }));
      throw error;
    }
  }

  // Selection Methods
  selectThumbnail(thumbnail: ThumbnailFile): void {
    this.updateState((state) => {
      const isSelected = state.selectedThumbnails.some(
        (t) => t.path === thumbnail.path
      );
      const selectedThumbnails = isSelected
        ? state.selectedThumbnails.filter((t) => t.path !== thumbnail.path)
        : [...state.selectedThumbnails, thumbnail];

      return { ...state, selectedThumbnails };
    });
  }

  selectAllThumbnails(): void {
    this.updateState((state) => ({
      ...state,
      selectedThumbnails: [...state.filteredThumbnails],
    }));
  }

  clearSelection(): void {
    this.updateState((state) => ({
      ...state,
      selectedThumbnails: [],
    }));
  }

  // Analysis Methods
  async analyzeSingle(thumbnail: ThumbnailFile): Promise<void> {
    this.updateState((state) => ({
      ...state,
      isAnalyzing: true,
      currentAnalysisFile: thumbnail.name,
    }));

    try {
      const metadata = await this.extractionService.extractMetadata(thumbnail);
      const analysis = this.analysisService.analyzeMetadata(
        metadata.raw,
        thumbnail.name
      );

      this.updateState((state) => ({
        ...state,
        currentAnalysis: analysis,
        analysisResults: [...state.analysisResults, analysis],
        isAnalyzing: false,
        currentAnalysisFile: "",
      }));
    } catch (error) {
      console.error(`Failed to analyze ${thumbnail.name}:`, error);
      this.updateState((state) => ({
        ...state,
        isAnalyzing: false,
        currentAnalysisFile: "",
      }));
      throw error;
    }
  }

  async analyzeBatch(sequences?: SequenceFile[]): Promise<void> {
    const sequencesToAnalyze = sequences || this.convertThumbnailsToSequences();

    if (sequencesToAnalyze.length === 0) {
      throw new Error("No sequences selected for analysis");
    }

    this.updateState((state) => ({
      ...state,
      isAnalyzing: true,
      analysisProgress: 0,
    }));

    try {
      const batchResults = await this.batchService.analyzeSequences(
        sequencesToAnalyze,
        this.getCurrentState().batchConfig,
        (progress, current) => {
          this.updateState((state) => ({
            ...state,
            analysisProgress: progress,
            currentAnalysisFile: current,
          }));
        },
        (results) => {
          this.updateState((state) => ({
            ...state,
            analysisResults: results,
          }));
        }
      );

      this.updateState((state) => ({
        ...state,
        batchResults,
        isAnalyzing: false,
        analysisProgress: 100,
        currentAnalysisFile: "Complete",
      }));
    } catch (error) {
      console.error("Batch analysis failed:", error);
      this.updateState((state) => ({
        ...state,
        isAnalyzing: false,
        analysisProgress: 0,
        currentAnalysisFile: "",
      }));
      throw error;
    }
  }

  // Filter Methods
  setSearchQuery(query: string): void {
    this.updateState((state) => ({
      ...state,
      searchQuery: query,
      filteredThumbnails: this.applySearchFilter(state.thumbnails, query),
    }));
  }

  setErrorFilter(showOnlyErrors: boolean): void {
    this.updateState((state) => ({ ...state, showOnlyErrors }));
  }

  setWarningFilter(showOnlyWarnings: boolean): void {
    this.updateState((state) => ({ ...state, showOnlyWarnings }));
  }

  setHealthScoreFilter(min: number, max: number): void {
    this.updateState((state) => ({
      ...state,
      healthScoreFilter: { min, max },
    }));
  }

  // ============================================================================
  // LEGACY COMPATIBILITY METHODS (for easy migration from old monolith)
  // ============================================================================

  /**
   * Legacy-compatible method: loadThumbnails -> discoverSequences
   */
  async loadThumbnails(): Promise<void> {
    return this.discoverSequences();
  }

  /**
   * Legacy-compatible method: extractMetadata -> analyzeSingle
   */
  async extractMetadata(thumbnail: ThumbnailFile): Promise<void> {
    // Select the thumbnail first (for single-selection compatibility)
    this.updateState((state) => ({
      ...state,
      selectedThumbnails: [thumbnail],
    }));

    return this.analyzeSingle(thumbnail);
  }

  /**
   * Legacy-compatible method: handleBatchAnalyze -> analyzeBatch
   */
  async handleBatchAnalyze(): Promise<void> {
    return this.analyzeBatch();
  }

  /**
   * Legacy-compatible getter: selectedThumbnail (first selected thumbnail)
   */
  get selectedThumbnail(): ThumbnailFile | null {
    return this.state.selectedThumbnails[0] || null;
  }

  /**
   * Legacy-compatible state properties
   */
  get isLoadingThumbnails(): boolean {
    return this.state.isDiscovering;
  }

  get isBatchAnalyzing(): boolean {
    return this.state.isAnalyzing;
  }

  get isExtractingMetadata(): boolean {
    return this.state.isAnalyzing;
  }

  /**
   * Legacy-compatible data getters
   */
  get rawMetadata(): string | null {
    if (!this.state.currentAnalysis) return null;
    // Return a simplified representation for legacy compatibility
    return JSON.stringify(this.state.currentAnalysis.stats, null, 2);
  }

  get extractedMetadata(): Record<string, unknown>[] | null {
    // For legacy compatibility, return empty array since we don't store raw metadata anymore
    return this.state.currentAnalysis ? [] : null;
  }

  get metadataStats(): MetadataStats | null {
    return this.state.currentAnalysis?.stats || null;
  }

  // ============================================================================
  // END LEGACY COMPATIBILITY METHODS
  // ============================================================================

  // Export Methods
  exportResults(format: "json" | "csv" = "json"): string {
    const state = this.getCurrentState();

    if (!state.batchResults) {
      throw new Error("No batch results to export");
    }

    return format === "csv"
      ? this.batchService.exportToCsv(state.batchResults)
      : this.batchService.exportToJson(state.batchResults);
  }

  // Clear Methods
  clearResults(): void {
    this.updateState((state) => ({
      ...state,
      analysisResults: [],
      batchResults: null,
      currentAnalysis: null,
    }));
  }

  clearAll(): void {
    this.updateState((state) => ({
      ...state,
      thumbnails: [],
      filteredThumbnails: [],
      selectedThumbnails: [],
      analysisResults: [],
      batchResults: null,
      currentAnalysis: null,
      searchQuery: "",
      showOnlyErrors: false,
      showOnlyWarnings: false,
      healthScoreFilter: { min: 0, max: 100 },
    }));
  }

  // Private Helper Methods
  private updateState(
    updater: (state: MetadataTestingState) => MetadataTestingState
  ): void {
    this._state = updater(this._state);
  }

  private getCurrentState(): MetadataTestingState {
    return this._state;
  }

  private applySearchFilter(
    thumbnails: ThumbnailFile[],
    query: string
  ): ThumbnailFile[] {
    if (!query.trim()) return thumbnails;

    const lowerQuery = query.toLowerCase();
    return thumbnails.filter(
      (thumbnail) =>
        thumbnail.name.toLowerCase().includes(lowerQuery) ||
        (thumbnail.metadata?.word || thumbnail.name)
          .toLowerCase()
          .includes(lowerQuery)
    );
  }

  private filterResults(state: MetadataTestingState): MetadataAnalysisResult[] {
    let filtered = [...state.analysisResults];

    // Apply error filter
    if (state.showOnlyErrors) {
      filtered = filtered.filter((result) => result.stats.hasErrors);
    }

    // Apply warning filter
    if (state.showOnlyWarnings) {
      filtered = filtered.filter((result) => result.stats.hasWarnings);
    }

    // Apply health score filter
    filtered = filtered.filter(
      (result) =>
        result.stats.healthScore >= state.healthScoreFilter.min &&
        result.stats.healthScore <= state.healthScoreFilter.max
    );

    return filtered;
  }

  private calculateSummaryStats(state: MetadataTestingState): SummaryStats {
    const results = state.analysisResults;

    if (results.length === 0) {
      return {
        totalSequences: 0,
        healthySequences: 0,
        unhealthySequences: 0,
        averageHealthScore: 0,
        totalErrors: 0,
        totalWarnings: 0,
      };
    }

    const totalHealthScore = results.reduce(
      (sum, result) => sum + result.stats.healthScore,
      0
    );
    const healthySequences = results.filter(
      (result) => result.stats.healthScore >= 80
    ).length;
    const totalErrors = results.reduce(
      (sum, result) => sum + result.stats.errorCount,
      0
    );
    const totalWarnings = results.reduce(
      (sum, result) => sum + result.stats.warningCount,
      0
    );

    return {
      totalSequences: results.length,
      healthySequences,
      unhealthySequences: results.length - healthySequences,
      averageHealthScore: totalHealthScore / results.length,
      totalErrors,
      totalWarnings,
    };
  }

  private convertThumbnailsToSequences(): SequenceFile[] {
    const state = this.getCurrentState();
    return state.selectedThumbnails.map((thumbnail) => ({
      name: thumbnail.name,
      file: new File([], thumbnail.name), // This would need proper file handling
    }));
  }
}

