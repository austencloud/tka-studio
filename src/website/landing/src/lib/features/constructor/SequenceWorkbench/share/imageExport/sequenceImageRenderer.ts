/**
 * Types for sequence image rendering
 */

/**
 * Result of rendering a sequence to an image
 */
export interface SequenceRenderResult {
  /**
   * The data URL of the rendered image
   */
  dataUrl: string;

  /**
   * The width of the rendered image
   */
  width: number;

  /**
   * The height of the rendered image
   */
  height: number;

  /**
   * The MIME type of the rendered image
   */
  mimeType: string;
}
