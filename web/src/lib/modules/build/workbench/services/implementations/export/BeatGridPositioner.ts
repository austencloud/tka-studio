/**
 * Beat Grid Positioner
 *
 * Handles beat positioning and grid drawing logic for image composition.
 * Manages the rendering and placement of beats within the composition layout.
 */

import type { SequenceData } from "$shared/domain";
// Temporary type definitions
interface LayoutData {
  beatCount: number;
  canvasSize: [number, number];
  layoutDimensions: [number, number];
  beatSize: number;
  spacing: number;
  gridSize: [number, number];
  rows: number;
  columns: number;
  additionalHeightTop: number;
}

interface SequenceExportOptions {
  addBeatNumbers: boolean;
  redVisible: boolean;
  blueVisible: boolean;
  combinedGrids: boolean;
  beatScale: number;
}

interface CompositionOptions {
  addBeatNumbers: boolean;
  redVisible: boolean;
  blueVisible: boolean;
  combinedGrids: boolean;
  beatScale: number;
  includeStartPosition: boolean;
}
// import type { IBeatRenderingService } from "../../contracts";

export class BeatGridPositioner {
  constructor(private beatRenderer: any) {}

  /**
   * Render all beats to individual canvases
   */
  async renderAllBeats(
    sequence: SequenceData,
    layoutData: LayoutData,
    options: SequenceExportOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!sequence.beats || sequence.beats.length === 0) {
      return [];
    }

    const beatRenderOptions = {
      addBeatNumbers: options.addBeatNumbers,
      redVisible: options.redVisible,
      blueVisible: options.blueVisible,
      combinedGrids: options.combinedGrids,
      beatScale: options.beatScale,
    };

    return await this.beatRenderer.renderBeatsToCanvases(
      [...sequence.beats],
      layoutData.beatSize,
      beatRenderOptions
    );
  }

  /**
   * Render start position canvas
   */
  async renderStartPosition(
    sequence: SequenceData,
    layoutData: LayoutData,
    options: SequenceExportOptions
  ): Promise<HTMLCanvasElement> {
    const beatRenderOptions = {
      addBeatNumbers: options.addBeatNumbers,
      redVisible: options.redVisible,
      blueVisible: options.blueVisible,
      combinedGrids: options.combinedGrids,
      beatScale: options.beatScale,
    };

    return await this.beatRenderer.renderStartPositionToCanvas(
      sequence,
      layoutData.beatSize,
      beatRenderOptions
    );
  }

  /**
   * Draw all beats in grid layout
   * Matches desktop grid positioning exactly
   */
  drawBeatsInGrid(
    ctx: CanvasRenderingContext2D,
    beatCanvases: HTMLCanvasElement[],
    layoutData: LayoutData,
    options: CompositionOptions,
    startColumn: number = 0
  ): void {
    let beatIndex = 0;

    // Iterate through grid positions (matches desktop logic)
    for (
      let row = 0;
      row < layoutData.rows && beatIndex < beatCanvases.length;
      row++
    ) {
      for (
        let col = startColumn;
        col < layoutData.columns && beatIndex < beatCanvases.length;
        col++
      ) {
        const beatCanvas = beatCanvases[beatIndex];
        this.drawBeatCanvas(ctx, beatCanvas, col, row, layoutData, options);
        beatIndex++;
      }
    }
  }

  /**
   * Draw a single beat canvas at grid position
   */
  private drawBeatCanvas(
    ctx: CanvasRenderingContext2D,
    beatCanvas: HTMLCanvasElement,
    column: number,
    row: number,
    layoutData: LayoutData,
    _options: CompositionOptions
  ): void {
    const x = column * layoutData.beatSize;
    const y = row * layoutData.beatSize + layoutData.additionalHeightTop;

    ctx.drawImage(beatCanvas, x, y);
  }

  /**
   * Draw start position if included
   */
  drawStartPosition(
    ctx: CanvasRenderingContext2D,
    startPositionCanvas: HTMLCanvasElement | null,
    layoutData: LayoutData,
    options: CompositionOptions
  ): void {
    if (!startPositionCanvas || !options.includeStartPosition) {
      return;
    }

    // Start position goes in first grid position (0, 0)
    this.drawBeatCanvas(ctx, startPositionCanvas, 0, 0, layoutData, options);
  }

  /**
   * Get beat canvas count including start position
   */
  getTotalCanvasCount(
    sequence: SequenceData,
    includeStartPosition: boolean
  ): number {
    const beatCount = sequence.beats ? sequence.beats.length : 0;
    return beatCount + (includeStartPosition ? 1 : 0);
  }

  /**
   * Calculate starting column for beats when start position is included
   */
  getBeatsStartColumn(includeStartPosition: boolean): number {
    return includeStartPosition ? 1 : 0;
  }
}
