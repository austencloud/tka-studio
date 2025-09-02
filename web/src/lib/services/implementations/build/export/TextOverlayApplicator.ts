/**
 * Text Overlay Applicator
 *
 * Handles the application of text overlays (word, user info, difficulty) to composed images.
 * Manages text positioning and rendering within the composition layout.
 */

import type {
  ImageExportOptions,
  LayoutData,
  SequenceData,
  TextRenderOptions,
  UserInfo,
} from "$domain";

import type {
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
  IUserInfoRenderer,
  IWordTextRenderer,
} from "$contracts";

export class TextOverlayApplicator {
  constructor(
    private wordRenderer: IWordTextRenderer,
    private userInfoRenderer: IUserInfoRenderer,
    private difficultyRenderer: IDifficultyBadgeRenderer,
    private textUtils: ITextRenderingUtils
  ) {}

  /**
   * Add all text overlays (word, user info, difficulty)
   */
  addTextOverlays(
    canvas: HTMLCanvasElement,
    sequence: SequenceData,
    layoutData: LayoutData,
    options: ImageExportOptions
  ): void {
    const textOptions = this.createTextOptions(layoutData, options);

    // Add word title if enabled
    if (options.addWord && sequence.word) {
      this.addWordOverlay(canvas, sequence.word, textOptions);
    }

    // Add user info if enabled
    if (options.addUserInfo) {
      this.addUserInfoOverlay(canvas, options, textOptions);
    }

    // Add difficulty level badge if enabled and available
    if (
      options.addDifficultyLevel &&
      sequence.level &&
      layoutData.additionalHeightTop > 0
    ) {
      this.addDifficultyBadge(canvas, sequence.level, layoutData);
    }
  }

  /**
   * Add word title overlay
   */
  private addWordOverlay(
    canvas: HTMLCanvasElement,
    word: string,
    textOptions: TextRenderOptions
  ): void {
    this.wordRenderer.render(canvas, word, textOptions);
  }

  /**
   * Add user info overlay
   */
  private addUserInfoOverlay(
    canvas: HTMLCanvasElement,
    options: ImageExportOptions,
    textOptions: TextRenderOptions
  ): void {
    const userInfo: UserInfo = {
      userName: options.userName,
      notes: options.notes,
      exportDate: options.exportDate,
    };
    this.userInfoRenderer.render(canvas, userInfo, textOptions);
  }

  /**
   * Add difficulty level badge overlay
   */
  private addDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    layoutData: LayoutData
  ): void {
    const badgeSize = Math.floor(layoutData.additionalHeightTop * 0.75);
    const inset = Math.floor(layoutData.additionalHeightTop / 8);

    this.difficultyRenderer.render(canvas, level, [inset, inset], badgeSize);
  }

  /**
   * Create text rendering options
   */
  private createTextOptions(
    layoutData: LayoutData,
    options: ImageExportOptions
  ): TextRenderOptions {
    return {
      margin: Math.floor(options.margin * options.beatScale),
      beatScale: options.beatScale,
      additionalHeightTop: layoutData.additionalHeightTop,
      additionalHeightBottom: layoutData.additionalHeightBottom,
    };
  }

  /**
   * Check if any text overlays are enabled
   */
  hasTextOverlays(options: ImageExportOptions): boolean {
    return options.addWord || options.addUserInfo || options.addDifficultyLevel;
  }

  /**
   * Estimate additional height needed for text overlays
   */
  estimateTextOverlayHeight(
    options: ImageExportOptions,
    beatScale: number
  ): {
    additionalHeightTop: number;
    additionalHeightBottom: number;
  } {
    let additionalHeightTop = 0;
    let additionalHeightBottom = 0;

    if (options.addWord) {
      additionalHeightTop = Math.max(
        additionalHeightTop,
        Math.floor(200 * beatScale)
      );
    }

    if (options.addDifficultyLevel) {
      additionalHeightTop = Math.max(
        additionalHeightTop,
        Math.floor(120 * beatScale)
      );
    }

    if (options.addUserInfo) {
      additionalHeightBottom = Math.max(
        additionalHeightBottom,
        Math.floor(80 * beatScale)
      );
    }

    return { additionalHeightTop, additionalHeightBottom };
  }
}
