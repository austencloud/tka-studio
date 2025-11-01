/**
 * GIF Export Orchestrator Service Interface
 *
 * Orchestrates the frame-by-frame GIF export process by coordinating
 * the animation playback controller and GIF export service.
 */

import type { IAnimationPlaybackController } from "./IAnimationPlaybackController";
import type { IGifExportService, GifExportProgress } from "./IGifExportService";
import type { AnimationPanelState } from "$build/animate/state/animation-panel-state.svelte";

export interface GifExportOrchestratorOptions {
  /** Custom filename for the export (defaults to sequence word) */
  filename?: string;
  /** Frame rate in FPS (default: 30) */
  fps?: number;
  /** GIF quality 1-20, lower is better (default: 10) */
  quality?: number;
}

export interface IGifExportOrchestrator {
  /**
   * Execute a full GIF export by capturing frames and encoding
   * @param canvas The canvas element to capture frames from
   * @param playbackController The animation playback controller
   * @param panelState The current animation panel state
   * @param onProgress Callback for progress updates
   * @param options Export options
   * @returns Promise that resolves when export is complete
   */
  executeExport(
    canvas: HTMLCanvasElement,
    playbackController: IAnimationPlaybackController,
    panelState: AnimationPanelState,
    onProgress: (progress: GifExportProgress) => void,
    options?: GifExportOrchestratorOptions
  ): Promise<void>;

  /**
   * Cancel an ongoing export
   */
  cancelExport(): void;

  /**
   * Check if an export is currently in progress
   */
  isExporting(): boolean;
}
