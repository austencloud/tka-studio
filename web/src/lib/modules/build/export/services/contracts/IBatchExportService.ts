
import type {
  BatchExportOptions,
  BatchExportResult,
  ExportProgress,
  ImageExportOptions,
  PDFExportOptions,
  Page,
} from "$shared/domain";
export interface IBatchExportService {
  exportInBatches(
    pages: Page[],
    options: BatchExportOptions & (ImageExportOptions | PDFExportOptions)
  ): Promise<BatchExportResult>;
  onProgress(callback: (progress: ExportProgress) => void): void;
  cancelBatchExport(): Promise<void>;
  getBatchStatus(): {
    isRunning: boolean;
    progress: ExportProgress;
    results: Array<{ success: boolean; error?: Error }>;
  };
  cleanup(): Promise<void>;
}
