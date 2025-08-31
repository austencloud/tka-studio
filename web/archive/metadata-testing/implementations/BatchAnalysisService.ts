// @ts-nocheck
import type {
  BatchAnalysisConfig,
  BatchAnalysisResult,
  MetadataAnalysisResult,
  SequenceFile,
} from "$lib/domain/metadata-testing/types";
import { MetadataAnalysisService } from "./MetadataAnalysisService";
import { MetadataExtractionService } from "./MetadataExtractionService";

export class BatchAnalysisService {
  private extractionService: MetadataExtractionService;
  private analysisService: MetadataAnalysisService;
  private isAnalyzing = false;
  private currentAnalysisId = "";

  constructor(
    extractionService: MetadataExtractionService,
    analysisService: MetadataAnalysisService
  ) {
    this.extractionService = extractionService;
    this.analysisService = analysisService;
  }

  async analyzeSequences(
    sequences: SequenceFile[],
    config: BatchAnalysisConfig,
    onProgress?: (progress: number, current: string) => void,
    onResults?: (results: MetadataAnalysisResult[]) => void
  ): Promise<BatchAnalysisResult> {
    if (this.isAnalyzing) {
      throw new Error("Batch analysis already in progress");
    }

    this.isAnalyzing = true;
    this.currentAnalysisId = crypto.randomUUID();

    const startTime = Date.now();
    const results: MetadataAnalysisResult[] = [];
    const errors: Array<{ sequence: string; error: string }> = [];

    try {
      for (let i = 0; i < sequences.length; i++) {
        const sequence = sequences[i];

        // Update progress
        const progress = (i / sequences.length) * 100;
        onProgress?.(progress, sequence.name);

        try {
          // Extract metadata
          const metadata = await this.extractionService.extractMetadataFromFile(
            sequence.name
          );

          // Analyze metadata
          const analysis = this.analysisService.analyzeMetadata(
            metadata,
            sequence.name
          );

          results.push(analysis);

          // Call intermediate results callback if provided
          if (onResults && (i + 1) % config.batchSize === 0) {
            onResults([...results]);
          }
        } catch (error) {
          console.error(`Error analyzing ${sequence.name}:`, error);
          errors.push({
            sequence: sequence.name,
            error: error instanceof Error ? error.message : "Unknown error",
          });
        }

        // Respect delay between analyses
        if (config.delayMs && i < sequences.length - 1) {
          await new Promise((resolve) => setTimeout(resolve, config.delayMs));
        }
      }

      // Final progress update
      onProgress?.(100, "Complete");
      onResults?.(results);

      const endTime = Date.now();
      const duration = endTime - startTime;

      return {
        analysisId: this.currentAnalysisId,
        totalSequences: sequences.length,
        successfulAnalyses: results.length,
        failedAnalyses: errors.length,
        results,
        errors,
        duration,
        summary: this.generateSummary(results),
        timestamp: new Date().toISOString(),
      };
    } finally {
      this.isAnalyzing = false;
      this.currentAnalysisId = "";
    }
  }

  private generateSummary(results: MetadataAnalysisResult[]) {
    if (results.length === 0) {
      return {
        averageHealthScore: 0,
        totalErrors: 0,
        totalWarnings: 0,
        commonIssues: [],
        healthDistribution: { excellent: 0, good: 0, fair: 0, poor: 0 },
      };
    }

    const totalHealthScore = results.reduce(
      (sum, result) => sum + result.stats.healthScore,
      0
    );
    const averageHealthScore = totalHealthScore / results.length;

    const totalErrors = results.reduce((sum, result) => {
      return (
        sum +
        Object.values(result.issues.errors).reduce(
          (errorSum, errorArray) => errorSum + errorArray.length,
          0
        )
      );
    }, 0);

    const totalWarnings = results.reduce((sum, result) => {
      return (
        sum +
        Object.values(result.issues.warnings).reduce(
          (warningSum, warningArray) => warningSum + warningArray.length,
          0
        )
      );
    }, 0);

    // Find common issues
    const issueFrequency = new Map<string, number>();
    results.forEach((result) => {
      // Count error types
      Object.entries(result.issues.errors).forEach(([category, errors]) => {
        errors.forEach((error) => {
          const key = `${category}: ${error}`;
          issueFrequency.set(key, (issueFrequency.get(key) || 0) + 1);
        });
      });

      // Count warning types
      Object.entries(result.issues.warnings).forEach(([category, warnings]) => {
        warnings.forEach((warning) => {
          const key = `${category}: ${warning}`;
          issueFrequency.set(key, (issueFrequency.get(key) || 0) + 1);
        });
      });
    });

    const commonIssues = Array.from(issueFrequency.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([issue, count]) => ({
        issue,
        count,
        percentage: (count / results.length) * 100,
      }));

    // Health score distribution
    const healthDistribution = results.reduce(
      (dist, result) => {
        const score = result.stats.healthScore;
        if (score >= 90) dist.excellent++;
        else if (score >= 75) dist.good++;
        else if (score >= 60) dist.fair++;
        else dist.poor++;
        return dist;
      },
      { excellent: 0, good: 0, fair: 0, poor: 0 }
    );

    return {
      averageHealthScore,
      totalErrors,
      totalWarnings,
      commonIssues,
      healthDistribution,
    };
  }

  isRunning(): boolean {
    return this.isAnalyzing;
  }

  getCurrentAnalysisId(): string {
    return this.currentAnalysisId;
  }

  async cancelAnalysis(): Promise<void> {
    this.isAnalyzing = false;
    this.currentAnalysisId = "";
  }

  // Export results to different formats
  exportToCsv(batchResult: BatchAnalysisResult): string {
    const headers = [
      "Sequence Name",
      "Health Score",
      "Has Errors",
      "Has Warnings",
      "Total Beats",
      "Author",
      "Level",
      "Start Position",
      "BPM",
      "Duration",
    ];

    const rows = batchResult.results.map((result: MetadataAnalysisResult) => [
      result.sequenceName,
      result.stats.healthScore.toFixed(2),
      result.stats.hasErrors ? "Yes" : "No",
      result.stats.hasWarnings ? "Yes" : "No",
      result.stats.totalBeats,
      result.stats.authorName || "",
      result.stats.level || "",
      result.stats.startPositionValue || "",
      "", // BPM not in current stats
      "", // Duration not in current stats
    ]);

    return [headers, ...rows]
      .map((row) => row.map((cell) => `"${cell}"`).join(","))
      .join("\n");
  }

  exportToJson(batchResult: BatchAnalysisResult, pretty = true): string {
    return JSON.stringify(batchResult, null, pretty ? 2 : undefined);
  }
}

