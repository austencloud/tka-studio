
import type { SequenceData } from "$shared/domain";
import type {
    ExportProgress,
    SequenceExportOptions,
    SequenceExportResult
} from "../../domain/models";

export interface IBatchExportService {
  exportInBatches(
    sequences: SequenceData[],
    options: SequenceExportOptions
  ): Promise<SequenceExportResult[]>;
  onProgress(callback: (progress: ExportProgress) => void): void;
  cancelBatchExport(): Promise<void>;
  getBatchStatus(): {
    isRunning: boolean;
    progress: ExportProgress;
    results: Array<{ success: boolean; error?: Error }>;
  };
  cleanup(): Promise<void>;
}
