/**
 * Animation Export Orchestrator
 *
 * Coordinates frame capture, encoding, and final delivery for GIF/WebP exports.
 */

import {
  GIF_EXPORT_FPS,
  GIF_EXPORT_QUALITY,
  GIF_FRAMES_PER_BEAT,
  GIF_INITIAL_CAPTURE_DELAY_MS,
} from "$create/animate/constants/timing";
import type { AnimationPanelState } from "$create/animate/state/animation-panel-state.svelte";
import { Letter, TYPES, type ISvgImageService } from "$shared";
import type { IFileDownloadService } from "$shared/foundation/services/contracts";
import { getLetterImagePath } from "$shared/pictograph/tka-glyph/utils";
import { inject, injectable } from "inversify";
import type { IAnimationPlaybackController } from "../contracts/IAnimationPlaybackController";
import type { ICanvasRenderer } from "../contracts/ICanvasRenderer";
import type {
  AnimationExportFormat,
  GifExportOrchestratorOptions,
  IGifExportOrchestrator,
} from "../contracts/IGifExportOrchestrator";
import type { IAnimatedImageTranscoder } from "../contracts/IAnimatedImageTranscoder";
import type {
  GifExportProgress,
  IGifExportService,
} from "../contracts/IGifExportService";

interface LetterOverlayAssets {
  image: HTMLImageElement | null;
  dimensions: { width: number; height: number };
}

@injectable()
export class GifExportOrchestrator implements IGifExportOrchestrator {
  private _isExporting = false;
  private shouldCancel = false;

  constructor(
    @inject(TYPES.IGifExportService)
    private readonly gifExportService: IGifExportService,
    @inject(TYPES.ICanvasRenderer)
    private readonly canvasRenderer: ICanvasRenderer,
    @inject(TYPES.ISvgImageService)
    private readonly svgImageService: ISvgImageService,
    @inject(TYPES.IFileDownloadService)
    private readonly fileDownloadService: IFileDownloadService,
    @inject(TYPES.IAnimatedImageTranscoder)
    private readonly animatedImageTranscoder: IAnimatedImageTranscoder
  ) {}

  async executeExport(
    canvas: HTMLCanvasElement,
    playbackController: IAnimationPlaybackController,
    panelState: AnimationPanelState,
    onProgress: (progress: GifExportProgress) => void,
    options: GifExportOrchestratorOptions = {}
  ): Promise<void> {
    if (this._isExporting) {
      throw new Error("Export already in progress");
    }

    this._isExporting = true;
    this.shouldCancel = false;

    const exportFormat: AnimationExportFormat = options.format ?? "gif";
    const filename = this.resolveFilename(
      options.filename,
      panelState.sequenceWord,
      exportFormat
    );

    const exporter = await this.gifExportService.createManualExporter(
      canvas.width,
      canvas.height,
      {
        fps: options.fps ?? GIF_EXPORT_FPS,
        quality: options.quality ?? GIF_EXPORT_QUALITY,
        filename,
        autoDownload: false,
      }
    );

    const captureState = {
      wasPlaying: panelState.isPlaying,
      beat: panelState.currentBeat,
    };

    try {
      onProgress({ progress: 0, stage: "capturing" });

      if (captureState.wasPlaying) {
        playbackController.togglePlayback();
      }
      playbackController.jumpToBeat(0);
      await this.delay(GIF_INITIAL_CAPTURE_DELAY_MS);

      const overlayAssets = await this.loadLetterOverlay(panelState);
      const totalFrames = panelState.totalBeats * GIF_FRAMES_PER_BEAT;
      const frameDelay = Math.floor(1000 / (options.fps ?? GIF_EXPORT_FPS));
      const ctx = canvas.getContext("2d");
      const logicalCanvasSize = this.getLogicalCanvasSize(canvas);

      for (let i = 0; i < totalFrames; i++) {
        if (this.shouldCancel) {
          throw new Error("Export cancelled");
        }

        const beat = i / GIF_FRAMES_PER_BEAT;
        playbackController.jumpToBeat(beat);

        // Wait for the UI + canvas to render the new beat
        await this.waitForAnimationFrame();
        await this.waitForAnimationFrame();

        if (overlayAssets.image && ctx) {
          this.canvasRenderer.renderLetterToCanvas(
            ctx,
            logicalCanvasSize,
            overlayAssets.image,
            overlayAssets.dimensions
          );
        }

        exporter.addFrame(canvas, frameDelay);

        onProgress({
          progress: (i + 1) / totalFrames,
          stage: "capturing",
          currentFrame: i + 1,
          totalFrames,
        });
      }

      if (this.shouldCancel) {
        throw new Error("Export cancelled");
      }

      onProgress({ progress: 0, stage: "encoding" });
      const gifBlob = await exporter.finish();

      if (exportFormat === "gif") {
        await this.fileDownloadService.downloadBlob(gifBlob, filename);
      } else {
        onProgress({ progress: 0.9, stage: "transcoding" });
        const webpBlob = await this.animatedImageTranscoder.convertGifToWebp(
          gifBlob,
          options.webp
        );
        await this.fileDownloadService.downloadBlob(webpBlob, filename);
      }

      onProgress({ progress: 1, stage: "complete" });
    } catch (error) {
      if (!this.shouldCancel) {
        onProgress({
          progress: 0,
          stage: "error",
          error: error instanceof Error ? error.message : "Unknown error",
        });
      }
      throw error;
    } finally {
      this.restorePlaybackState(playbackController, captureState);
      this._isExporting = false;
      this.shouldCancel = false;
    }
  }

  cancelExport(): void {
    this.shouldCancel = true;
    this.gifExportService.cancelExport();
    this._isExporting = false;
  }

  isExporting(): boolean {
    return this._isExporting;
  }

  private restorePlaybackState(
    playbackController: IAnimationPlaybackController,
    snapshot: { wasPlaying: boolean; beat: number }
  ): void {
    playbackController.jumpToBeat(snapshot.beat);
    if (snapshot.wasPlaying) {
      playbackController.togglePlayback();
    }
  }

  private resolveFilename(
    explicitFilename: string | undefined,
    sequenceWord: string | null,
    format: AnimationExportFormat
  ): string {
    if (explicitFilename) {
      return explicitFilename;
    }

    const baseName = sequenceWord || "animation";
    const extension = format === "gif" ? "gif" : "webp";
    return this.fileDownloadService.generateTimestampedFilename(
      baseName,
      extension
    );
  }

  private async loadLetterOverlay(
    panelState: AnimationPanelState
  ): Promise<LetterOverlayAssets> {
    if (!panelState.sequenceWord) {
      return { image: null, dimensions: { width: 0, height: 0 } };
    }

    try {
      const letter = panelState.sequenceWord as Letter;
      const imagePath = getLetterImagePath(letter);
      const response = await fetch(imagePath);

      if (!response.ok) {
        return { image: null, dimensions: { width: 0, height: 0 } };
      }

      const svgText = await response.text();
      const viewBoxMatch = svgText.match(
        /viewBox\s*=\s*"[\d.-]+\s+[\d.-]+\s+([\d.-]+)\s+([\d.-]+)"/i
      );
      const width = viewBoxMatch ? parseFloat(viewBoxMatch[1]!) : 100;
      const height = viewBoxMatch ? parseFloat(viewBoxMatch[2]!) : 100;
      const image = await this.svgImageService.convertSvgStringToImage(
        svgText,
        width,
        height
      );

      return { image, dimensions: { width, height } };
    } catch (error) {
      console.warn("Failed to load letter image for animation export:", error);
      return { image: null, dimensions: { width: 0, height: 0 } };
    }
  }

  private waitForAnimationFrame(): Promise<void> {
    if (typeof window === "undefined") {
      return Promise.resolve();
    }

    return new Promise((resolve) => requestAnimationFrame(() => resolve()));
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private getLogicalCanvasSize(canvas: HTMLCanvasElement): number {
    const rect = canvas.getBoundingClientRect();
    if (rect.width > 0) {
      return rect.width;
    }
    return canvas.width;
  }
}
