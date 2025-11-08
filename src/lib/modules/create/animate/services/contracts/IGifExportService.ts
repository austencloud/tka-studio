/**
 * GIF Export Service Interface
 *
 * Provides functionality to export canvas animations as GIF files.
 */

export interface GifExportOptions {
  /** Frame rate in frames per second (default: 30) */
  fps?: number;
  /** GIF quality (1-20, lower is better, default: 10) */
  quality?: number;
  /** Number of web workers to use (default: 2) */
  workers?: number;
  /** Animation duration in seconds (default: full animation) */
  duration?: number;
  /** Whether to loop the animation (default: 0 = infinite) */
  repeat?: number;
  /** Filename for the download (default: "animation.gif") */
  filename?: string;
  /** Skip auto-download so callers can post-process or batch */
  autoDownload?: boolean;
}

export interface GifExportProgress {
  /** Current progress (0-1) */
  progress: number;
  /** Current stage of export */
  stage: "capturing" | "encoding" | "transcoding" | "complete" | "error";
  /** Current frame being processed */
  currentFrame?: number;
  /** Total frames to process */
  totalFrames?: number;
  /** Error message if stage is 'error' */
  error?: string;
}

export interface IGifExportService {
  /**
   * Export a canvas animation as GIF
   * @param canvas The canvas element to capture
   * @param onProgress Callback for progress updates
   * @param options Export options
   * @returns Promise that resolves when export is complete
   */
  exportAnimation(
    canvas: HTMLCanvasElement,
    onProgress: (progress: GifExportProgress) => void,
    options?: GifExportOptions
  ): Promise<Blob>;

  /**
   * Create a manual GIF exporter for frame-by-frame control
   * @param width Canvas width
   * @param height Canvas height
   * @param options Export options (excluding duration)
   * @returns Promise resolving to exporter methods
   */
  createManualExporter(
    width: number,
    height: number,
    options?: Omit<GifExportOptions, "duration">
  ): Promise<{
    addFrame: (canvas: HTMLCanvasElement, delay?: number) => void;
    finish: () => Promise<Blob>;
    cancel: () => void;
  }>;

  /**
   * Cancel an ongoing export
   */
  cancelExport(): void;

  /**
   * Check if an export is currently in progress
   */
  isExporting(): boolean;
}
