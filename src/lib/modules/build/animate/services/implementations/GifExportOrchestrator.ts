/**
 * GIF Export Orchestrator Service Implementation
 *
 * Coordinates frame-by-frame capture and GIF encoding by managing
 * animation playback state and interfacing with the GIF export service.
 */

import { injectable, inject } from "inversify";
import type {
  IGifExportOrchestrator,
  GifExportOrchestratorOptions,
} from "../contracts/IGifExportOrchestrator";
import type { IAnimationPlaybackController } from "../contracts/IAnimationPlaybackController";
import type { IGifExportService, GifExportProgress } from "../contracts/IGifExportService";
import type { AnimationPanelState } from "$build/animate/state/animation-panel-state.svelte";
import { TYPES } from "$shared";
import {
  GIF_EXPORT_FPS,
  GIF_EXPORT_QUALITY,
  GIF_FRAMES_PER_BEAT,
  GIF_FRAME_RENDER_DELAY_MS,
  GIF_INITIAL_CAPTURE_DELAY_MS,
} from "$build/animate/constants/timing";

@injectable()
export class GifExportOrchestrator implements IGifExportOrchestrator {
  private _isExporting = false;
  private shouldCancel = false;

  constructor(
    @inject(TYPES.IGifExportService) private gifExportService: IGifExportService
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

    try {
      // Initialize progress
      onProgress({ progress: 0, stage: 'capturing' });

      // Create manual exporter with specified options
      const { addFrame, finish } = await this.gifExportService.createManualExporter(
        canvas.width,
        canvas.height,
        {
          fps: options.fps ?? GIF_EXPORT_FPS,
          quality: options.quality ?? GIF_EXPORT_QUALITY,
          filename: options.filename ?? `${panelState.sequenceWord || 'animation'}.gif`,
        }
      );

      // Preserve current animation state
      const wasPlaying = panelState.isPlaying;
      const currentBeat = panelState.currentBeat;

      // Stop animation and reset to beginning
      if (wasPlaying) {
        playbackController.togglePlayback();
      }
      playbackController.jumpToBeat(0);

      // Wait for initial render
      await this.delay(GIF_INITIAL_CAPTURE_DELAY_MS);

      // Calculate frame capture parameters
      const totalBeats = panelState.totalBeats;
      const totalFrames = totalBeats * GIF_FRAMES_PER_BEAT;
      const frameDelay = Math.floor(1000 / (options.fps ?? GIF_EXPORT_FPS));

      // Capture frames through one full loop
      for (let i = 0; i < totalFrames; i++) {
        // Check for cancellation
        if (this.shouldCancel) {
          throw new Error('Export cancelled');
        }

        // Calculate beat position
        const beat = i / GIF_FRAMES_PER_BEAT;
        playbackController.jumpToBeat(beat);

        // Wait for frame to render
        await this.delay(GIF_FRAME_RENDER_DELAY_MS);

        // Capture the frame
        addFrame(canvas, frameDelay);

        // Update progress
        onProgress({
          progress: i / totalFrames,
          stage: 'capturing',
          currentFrame: i,
          totalFrames,
        });
      }

      // Check for cancellation before encoding
      if (this.shouldCancel) {
        throw new Error('Export cancelled');
      }

      // Start encoding
      onProgress({ progress: 0, stage: 'encoding' });
      await finish();

      // Export complete
      onProgress({ progress: 1, stage: 'complete' });

      // Restore original animation state
      playbackController.jumpToBeat(currentBeat);
      if (wasPlaying) {
        playbackController.togglePlayback();
      }

    } catch (error) {
      // Handle errors
      if (!this.shouldCancel) {
        onProgress({
          progress: 0,
          stage: 'error',
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      throw error;
    } finally {
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

  /**
   * Utility delay function
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
