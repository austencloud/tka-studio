/**
 * Simple Image Composition Service
 *
 * Dead-simple approach: Render pictographs directly onto a single canvas.
 * No intermediate canvases, no complex calculations, just straightforward rendering.
 */

import type { BeatData, PictographData, SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { SequenceExportOptions } from "../../domain/models";
import { renderPictographToSVG } from "../../utils/pictograph-to-svg";
import type { IDimensionCalculationService, ILayoutCalculationService, ITextRenderingService } from "../contracts";
import {  } from "../contracts";
import type { IImageCompositionService } from "../contracts";

@injectable()
export class ImageCompositionService implements IImageCompositionService {
  constructor(
    @inject(TYPES.ILayoutCalculationService)
    private readonly layoutService: ILayoutCalculationService,
    @inject(TYPES.ITextRenderingService)
    private readonly textRenderingService: ITextRenderingService,
    @inject(TYPES.IDimensionCalculationService)
    private readonly dimensionCalculationService: IDimensionCalculationService
  ) {}
  /**
   * Compose complete sequence image from sequence data
   */
  async composeSequenceImage(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): Promise<HTMLCanvasElement> {
    if (!sequence.beats || sequence.beats.length === 0) {
      throw new Error("Sequence must have at least one beat");
    }

    // Step 1: Calculate layout using LayoutCalculationService
    // This service has the proper lookup tables matching the desktop application
    const beatCount = sequence.beats.length;
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );

    // Step 2: Calculate canvas dimensions including title space
    const beatSize = options.beatSize || 120;
    const canvasWidth = columns * beatSize;

    // Calculate title height if word should be included (using desktop-compatible logic)
    const titleHeight =
      options.addWord && sequence.word
        ? this.calculateTitleHeight(beatCount, options.beatScale || 1)
        : 0;
    const canvasHeight = rows * beatSize + titleHeight;

    const canvas = document.createElement("canvas");
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context");
    }

    // Step 3: Fill white background
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);

    // Step 4: Render title if enabled
    if (options.addWord && sequence.word && titleHeight > 0) {
      this.textRenderingService.renderWordText(
        canvas,
        sequence.word,
        {
          margin: options.margin || 0,
          beatScale: options.beatScale || 1,
        },
        beatCount
      ); // Pass beat count for proper font scaling
    }

    // Step 4.5: Render difficulty badge if enabled and title area exists
    if (options.addDifficultyLevel && titleHeight > 0) {
      this.renderDifficultyBadge(canvas, sequence, titleHeight);
    }

    // Step 5: Render each pictograph directly onto the canvas (offset by title height)
    // Render start position if needed (always at column 0, row 0)
    if (options.includeStartPosition && sequence.startPosition) {
      await this.renderPictographAt(
        ctx,
        sequence.startPosition,
        0,
        0,
        beatSize,
        0,
        titleHeight
      ); // beatNumber = 0 for start position
    }

    // Step 6: Render all beats in the grid (offset by title height)
    // Calculate how many beats per row based on the layout
    const startColumn = options.includeStartPosition ? 1 : 0;
    const beatsPerRow = columns - startColumn; // Available columns for beats

    for (let i = 0; i < sequence.beats.length; i++) {
      const beat = sequence.beats[i];
      // Calculate position: beats fill remaining columns, then wrap to next row
      const col = startColumn + (i % beatsPerRow);
      const row = Math.floor(i / beatsPerRow);
      const beatNumber = i + 1; // Beat numbers start from 1
      await this.renderPictographAt(
        ctx,
        beat!,
        col,
        row,
        beatSize,
        beatNumber,
        titleHeight
      );
    }

    // Step 7: Draw cell borders only between occupied cells (offset by title)
    this.drawSmartCellBorders(
      ctx,
      columns,
      rows,
      beatSize,
      sequence,
      options,
      titleHeight
    );

    return canvas;
  }

  /**
   * Render a single pictograph directly onto the canvas at the specified grid position
   */
  private async renderPictographAt(
    ctx: CanvasRenderingContext2D,
    pictographData: BeatData | PictographData,
    column: number,
    row: number,
    beatSize: number,
    beatNumber?: number,
    titleOffset: number = 0
  ): Promise<void> {
    try {
      // Generate SVG with beat number
      const svgString = await renderPictographToSVG(
        pictographData,
        beatSize,
        beatNumber
      );

      // Convert SVG to image
      const img = await this.svgStringToImage(svgString);

      // Draw directly onto the canvas at the correct position (offset by title)
      const x = column * beatSize;
      const y = row * beatSize + titleOffset;

      ctx.drawImage(img, x, y, beatSize, beatSize);
    } catch (error) {
      console.error(`❌ Failed to render beat at (${column}, ${row}):`, error);
      // Draw error placeholder
      const x = column * beatSize;
      const y = row * beatSize;
      ctx.fillStyle = "#ffeeee";
      ctx.fillRect(x + 5, y + 5, beatSize - 10, beatSize - 10);
      ctx.fillStyle = "#cc0000";
      ctx.font = "14px Arial";
      ctx.textAlign = "center";
      ctx.fillText("Error", x + beatSize / 2, y + beatSize / 2);
    }
  }

  /**
   * Draw cell borders only between occupied cells (smart grid)
   */
  private drawSmartCellBorders(
    ctx: CanvasRenderingContext2D,
    columns: number,
    rows: number,
    beatSize: number,
    sequence: SequenceData,
    options: SequenceExportOptions,
    titleOffset: number = 0
  ): void {
    ctx.strokeStyle = "#e0e0e0"; // Light gray border color (matching workbench)
    ctx.lineWidth = 1;

    // Create a map of occupied cells
    const occupiedCells = this.getOccupiedCells(sequence, options, columns);

    // Helper function to check if a cell is occupied
    const isOccupied = (col: number, row: number): boolean => {
      return occupiedCells.has(`${col},${row}`);
    };

    // Draw vertical lines between horizontally adjacent occupied cells
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns - 1; col++) {
        if (isOccupied(col, row) && isOccupied(col + 1, row)) {
          const x = (col + 1) * beatSize;
          ctx.beginPath();
          ctx.moveTo(x, row * beatSize + titleOffset);
          ctx.lineTo(x, (row + 1) * beatSize + titleOffset);
          ctx.stroke();
        }
      }
    }

    // Draw horizontal lines between vertically adjacent occupied cells
    for (let col = 0; col < columns; col++) {
      for (let row = 0; row < rows - 1; row++) {
        if (isOccupied(col, row) && isOccupied(col, row + 1)) {
          const y = (row + 1) * beatSize + titleOffset;
          ctx.beginPath();
          ctx.moveTo(col * beatSize, y);
          ctx.lineTo((col + 1) * beatSize, y);
          ctx.stroke();
        }
      }
    }
  }

  /**
   * Get a set of occupied cell coordinates
   */
  private getOccupiedCells(
    sequence: SequenceData,
    options: SequenceExportOptions,
    columns: number
  ): Set<string> {
    const occupied = new Set<string>();

    // Add start position if included
    if (options.includeStartPosition && sequence.startPosition) {
      occupied.add("0,0");
    }

    // Add all beats
    const startColumn = options.includeStartPosition ? 1 : 0;
    const beatsPerRow = columns - startColumn;

    for (let i = 0; i < sequence.beats.length; i++) {
      const col = startColumn + (i % beatsPerRow);
      const row = Math.floor(i / beatsPerRow);
      occupied.add(`${col},${row}`);
    }

    return occupied;
  }

  /**
   * Convert SVG string to HTMLImageElement
   */
  private async svgStringToImage(svgString: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();

      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error("Failed to load SVG as image"));

      // Convert SVG string to data URL
      const blob = new Blob([svgString], { type: "image/svg+xml" });
      const url = URL.createObjectURL(blob);
      img.src = url;

      // Clean up blob URL after image loads
      img.onload = () => {
        URL.revokeObjectURL(url);
        resolve(img);
      };
    });
  }

  // Stub methods to satisfy interface (not used in simple version)
  async composeFromCanvases(): Promise<HTMLCanvasElement> {
    throw new Error("Not implemented in simple version");
  }

  applyBackground(canvas: HTMLCanvasElement): HTMLCanvasElement {
    return canvas;
  }

  optimizeForExport(canvas: HTMLCanvasElement): HTMLCanvasElement {
    // Simple version doesn't need optimization
    return canvas;
  }

  /**
   * Calculate title height based on beat count (matches desktop logic)
   * This must match the calculation in TextRenderingService
   */
  private calculateTitleHeight(beatCount: number, beatScale: number): number {
    let baseHeight = 0;

    // Match desktop logic exactly based on beat count
    if (beatCount === 0) {
      baseHeight = 0;
    } else if (beatCount === 1) {
      baseHeight = 150;
    } else if (beatCount === 2) {
      baseHeight = 200;
    } else {
      // beatCount >= 3
      baseHeight = 300;
    }

    // Apply beat scale
    return Math.floor(baseHeight * beatScale);
  }

  /**
   * Render difficulty badge in the title area
   * Positioned in the top-right corner of the title area
   */
  private renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    sequence: SequenceData,
    titleHeight: number
  ): void {
    // Get difficulty level from sequence
    const difficultyLevel = this.getDifficultyLevel(sequence);
    if (difficultyLevel === 0) {
      return;
    }

    // Calculate badge dimensions using desktop logic
    const badgeArea =
      this.dimensionCalculationService.calculateDifficultyBadgeArea(
        titleHeight
      );
    if (!badgeArea.available) {
      return;
    }

    // Position badge in top-right corner of title area
    const x = canvas.width - badgeArea.size - badgeArea.inset;
    const y = badgeArea.inset;

    // Render the badge using TextRenderingService
    this.textRenderingService.renderDifficultyBadge(
      canvas,
      difficultyLevel,
      [x, y],
      badgeArea.size
    );
  }

  /**
   * Extract difficulty level from sequence data
   * Returns numeric level (1-7) for badge rendering
   */
  private getDifficultyLevel(sequence: SequenceData): number {
    // First try the numeric level property
    if (typeof sequence.level === "number" && sequence.level > 0) {
      return sequence.level;
    }

    // Fall back to string difficultyLevel property
    if (typeof sequence.difficultyLevel === "string") {
      switch (sequence.difficultyLevel.toLowerCase()) {
        case "beginner":
          return 1;
        case "intermediate":
          return 3;
        case "advanced":
          return 5;
        default:
          return 1;
      }
    }

    // Default fallback
    return 0; // No badge
  }
}
