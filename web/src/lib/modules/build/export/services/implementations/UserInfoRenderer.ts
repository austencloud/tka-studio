/**
 * User Info Renderer
 *
 * Handles rendering of user information (name, date, notes) in 3-column layout.
 * Matches desktop UserInfoDrawer exactly.
 */

import { injectable } from "inversify";
import type { TextRenderOptions, UserInfo } from "../../domain/models";
import type { IUserInfoRenderer } from "../contracts";
import { createFont, getCanvasContext } from "./TextRenderingTypes";

@injectable()
export class UserInfoRenderer implements IUserInfoRenderer {
  // Font constants matching desktop application
  private static readonly USER_INFO_FONT_FAMILY = "Georgia";
  private static readonly USER_INFO_BASE_FONT_SIZE = 50;

  /**
   * Render user information (name, date, notes)
   * Matches desktop UserInfoDrawer exactly with 3-column layout
   */
  render(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void {
    const ctx = getCanvasContext(canvas);

    const margin = options.margin;
    const bottomY = canvas.height - margin;

    // Calculate scaled font sizes
    const baseFontSize = UserInfoRenderer.USER_INFO_BASE_FONT_SIZE;
    const { fontSize } = this.adjustFontAndMargin(
      baseFontSize,
      margin,
      3,
      options.beatScale
    );

    // Format export date (match desktop formatting)
    const formattedDate = this.formatExportDate(userInfo.exportDate);
    const notes = userInfo.notes || "Created using The Kinetic Alphabet";

    // Left: User name (bold italic)
    ctx.font = createFont(
      UserInfoRenderer.USER_INFO_FONT_FAMILY,
      fontSize,
      "bold",
      "italic"
    );
    ctx.fillStyle = "black";
    ctx.textAlign = "left";
    ctx.textBaseline = "bottom";
    ctx.fillText(userInfo.userName, margin, bottomY);

    // Center: Notes (italic)
    ctx.font = createFont(
      UserInfoRenderer.USER_INFO_FONT_FAMILY,
      fontSize,
      "normal",
      "italic"
    );
    ctx.textAlign = "center";
    ctx.fillText(notes, canvas.width / 2, bottomY);

    // Right: Export date (italic)
    ctx.textAlign = "right";
    ctx.fillText(formattedDate, canvas.width - margin, bottomY);
  }

  /**
   * Adjust font size and margin based on beat count
   * Matches desktop FontMarginHelper.adjust_font_and_margin exactly
   */
  private adjustFontAndMargin(
    baseFontSize: number,
    baseMargin: number,
    beatCount: number,
    beatScale: number
  ): { fontSize: number; margin: number } {
    let fontScale: number;
    let marginScale: number;

    // Match desktop scaling logic exactly
    if (beatCount <= 1) {
      fontScale = 1 / 2.3;
      marginScale = 1 / 3;
    } else if (beatCount === 2) {
      fontScale = 1 / 1.5;
      marginScale = 1 / 2;
    } else {
      fontScale = 1.0;
      marginScale = 1.0;
    }

    const fontSize = Math.max(
      1,
      Math.floor(baseFontSize * fontScale * beatScale)
    );
    const margin = Math.max(
      1,
      Math.floor(baseMargin * marginScale * beatScale)
    );

    return { fontSize, margin };
  }

  /**
   * Format export date to match desktop formatting
   * Matches desktop _format_export_date exactly
   */
  private formatExportDate(dateStr: string): string {
    // Convert "MM-DD-YYYY" to "M-D-YYYY" (remove leading zeros)
    return dateStr
      .split("-")
      .map((part) => parseInt(part).toString())
      .join("-");
  }

  /**
   * Get recommended user info text settings
   */
  getRecommendedSettings(
    beatCount: number,
    beatScale: number
  ): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  } {
    const { fontSize } = this.adjustFontAndMargin(
      UserInfoRenderer.USER_INFO_BASE_FONT_SIZE,
      50,
      beatCount,
      beatScale
    );
    return {
      fontFamily: UserInfoRenderer.USER_INFO_FONT_FAMILY,
      fontSize,
      fontWeight: "normal",
      italic: true,
    };
  }
}
