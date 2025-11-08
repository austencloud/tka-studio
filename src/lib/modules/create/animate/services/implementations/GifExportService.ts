/**
 * GIF Export Service Implementation
 *
 * Uses gif.js to capture and encode canvas animations as GIF files.
 * Runs encoding in Web Workers for better performance.
 */

import { base } from "$app/paths";
import { injectable } from "inversify";
import type {
  GifExportOptions,
  GifExportProgress,
  IGifExportService,
} from "../contracts/IGifExportService";

// Dynamic import for gif.js to avoid SSR issues
let GIF: any = null;
const GIF_WORKER_PATH = `${base}/gif.worker.js`;

// Load gif.js dynamically
async function loadGifJs() {
  if (typeof window === "undefined") {
    throw new Error("GIF export is only available in browser environment");
  }

  if (!GIF) {
    // @ts-ignore - gif.js doesn't have proper ESM exports
    const module = await import("gif.js");
    GIF = module.default || module;
  }

  return GIF;
}

@injectable()
export class GifExportService implements IGifExportService {
  private currentGif: any = null;
  private isCurrentlyExporting = false;
  private shouldCancel = false;

  async exportAnimation(
    canvas: HTMLCanvasElement,
    onProgress: (progress: GifExportProgress) => void,
    options: GifExportOptions = {}
  ): Promise<Blob> {
    if (this.isCurrentlyExporting) {
      throw new Error("Export already in progress");
    }

    this.isCurrentlyExporting = true;
    this.shouldCancel = false;

    const {
      fps = 30,
      quality = 10,
      workers = 2,
      duration,
      repeat = 0,
      filename = "animation.gif",
      autoDownload = true,
    } = options;

    try {
      // Load gif.js library
      const GIFConstructor = await loadGifJs();

      // Calculate frame timing
      const frameDelay = Math.floor(1000 / fps); // milliseconds per frame

      // Create GIF encoder instance
      this.currentGif = new GIFConstructor({
        workers,
        quality,
        workerScript: GIF_WORKER_PATH, // Resolves base-aware worker path
        repeat, // 0 = loop forever, -1 = no loop, n = loop n times
        width: canvas.width,
        height: canvas.height,
      });

      // Set up progress event
      this.currentGif.on("progress", (progress: number) => {
        if (this.shouldCancel) return;

        onProgress({
          progress,
          stage: "encoding",
        });
      });

      // Set up finished event
      const gifPromise = new Promise<Blob>((resolve, reject) => {
        this.currentGif.on("finished", (blob: Blob) => {
          if (this.shouldCancel) {
            reject(new Error("Export cancelled"));
            return;
          }

          onProgress({
            progress: 1,
            stage: "complete",
          });

          if (autoDownload) {
            this.downloadBlob(blob, filename);
          }

          resolve(blob);
        });

        this.currentGif.on("abort", () => {
          reject(new Error("GIF encoding aborted"));
        });
      });

      // Capture frames
      await this.captureFrames(
        canvas,
        frameDelay,
        duration,
        (current, total) => {
          if (this.shouldCancel) throw new Error("Export cancelled");

          onProgress({
            progress: current / total,
            stage: "capturing",
            currentFrame: current,
            totalFrames: total,
          });
        }
      );

      if (this.shouldCancel) {
        throw new Error("Export cancelled");
      }

      // Start encoding
      onProgress({
        progress: 0,
        stage: "encoding",
      });

      this.currentGif.render();

      const blob = await gifPromise;

      return blob;
    } catch (error) {
      onProgress({
        progress: 0,
        stage: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      });
      throw error;
    } finally {
      this.isCurrentlyExporting = false;
      this.currentGif = null;
      this.shouldCancel = false;
    }
  }

  /**
   * Capture frames from the canvas
   * This needs to be done by the caller's animation system
   * For now, we'll create a helper that works with the animation loop
   */
  private async captureFrames(
    canvas: HTMLCanvasElement,
    frameDelay: number,
    duration: number | undefined,
    onProgress: (current: number, total: number) => void
  ): Promise<void> {
    if (this.shouldCancel) {
      throw new Error("Export cancelled");
    }

    // If no duration was provided, capture a single frame so callers still get output
    if (!duration || duration <= 0) {
      this.addFrameFromCanvas(canvas, frameDelay);
      onProgress(1, 1);
      return;
    }

    const totalFrames = Math.max(Math.floor((duration * 1000) / frameDelay), 1);

    for (let index = 0; index < totalFrames; index++) {
      if (this.shouldCancel) {
        throw new Error("Export cancelled");
      }

      // Wait for the browser to paint the latest canvas updates
      await this.waitForNextAnimationFrame();
      this.addFrameFromCanvas(canvas, frameDelay);

      onProgress(index + 1, totalFrames);
    }
  }

  /**
   * Add a frame to the current GIF from a canvas
   * This should be called by the animation loop
   */
  addFrameFromCanvas(canvas: HTMLCanvasElement, delay?: number): void {
    if (!this.currentGif || !this.isCurrentlyExporting) {
      console.warn("No GIF export in progress");
      return;
    }

    // Add the current canvas state as a frame
    this.currentGif.addFrame(canvas, {
      copy: true, // Copy pixel data instead of reference
      delay: delay, // Frame delay in milliseconds
    });
  }

  /**
   * Start the GIF rendering process after all frames have been added
   */
  startRendering(): void {
    if (!this.currentGif) {
      throw new Error("No GIF initialized");
    }

    this.currentGif.render();
  }

  cancelExport(): void {
    this.shouldCancel = true;

    if (this.currentGif) {
      this.currentGif.abort();
      this.currentGif = null;
    }

    this.isCurrentlyExporting = false;
  }

  isExporting(): boolean {
    return this.isCurrentlyExporting;
  }

  /**
   * Trigger browser download of the blob
   */
  private downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Clean up the URL after a short delay
    setTimeout(() => URL.revokeObjectURL(url), 100);
  }

  /**
   * Create a new GIF encoder instance for manual frame-by-frame export
   * Returns methods to add frames and finalize
   */
  async createManualExporter(
    width: number,
    height: number,
    options: Omit<GifExportOptions, "duration"> = {}
  ): Promise<{
    addFrame: (canvas: HTMLCanvasElement, delay?: number) => void;
    finish: () => Promise<Blob>;
    cancel: () => void;
  }> {
    if (this.isCurrentlyExporting) {
      throw new Error("Export already in progress");
    }

    this.isCurrentlyExporting = true;
    this.shouldCancel = false;

    const {
      fps = 30,
      quality = 10,
      workers = 2,
      repeat = 0,
      filename = "animation.gif",
      autoDownload = true,
    } = options;

    const frameDelay = Math.floor(1000 / fps);

    // Load gif.js library
    const GIFConstructor = await loadGifJs();

    // Create GIF encoder instance
    this.currentGif = new GIFConstructor({
      workers,
      quality,
      workerScript: GIF_WORKER_PATH, // Resolves base-aware worker path
      repeat,
      width,
      height,
    });

    const addFrame = (canvas: HTMLCanvasElement, delay?: number) => {
      if (this.shouldCancel || !this.currentGif) return;

      this.currentGif.addFrame(canvas, {
        copy: true,
        delay: delay ?? frameDelay,
      });
    };

    const finish = (): Promise<Blob> => {
      return new Promise((resolve, reject) => {
        if (!this.currentGif) {
          reject(new Error("GIF encoder not initialized"));
          return;
        }

        this.currentGif.on("finished", (blob: Blob) => {
          if (autoDownload) {
            this.downloadBlob(blob, filename);
          }
          this.isCurrentlyExporting = false;
          this.currentGif = null;
          resolve(blob);
        });

        this.currentGif.on("abort", () => {
          this.isCurrentlyExporting = false;
          this.currentGif = null;
          reject(new Error("GIF encoding aborted"));
        });

        this.currentGif.render();
      });
    };

    const cancel = () => {
      this.cancelExport();
    };

    return { addFrame, finish, cancel };
  }

  private waitForNextAnimationFrame(): Promise<void> {
    return new Promise((resolve) => requestAnimationFrame(() => resolve()));
  }
}
