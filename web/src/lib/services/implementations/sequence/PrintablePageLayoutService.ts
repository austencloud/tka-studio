/**
 * Printable Page Layout Service Implementation
 *
 * Handles calculations for printable page layouts including paper sizes,
 * margins, grid configurations, and measurement conversions.
 *
 * Based on desktop application's printable_layout.py functionality.
 */

import type { IPrintablePageLayoutService } from "$contracts";
import type {
  DPIConfiguration,
  GridCalculationOptions,
  LayoutCalculationRequest,
  LayoutCalculationResult,
  LayoutValidationError,
  LayoutValidationResult,
  LayoutValidationWarning,
  PageDimensions,
  PageLayoutConfig,
  PageMargins,
  PageOrientation,
  Rectangle,
  SequenceCardGridConfig,
  SequenceCardPaperSize,
} from "$domain";
import { injectable } from "inversify";

@injectable()
export class PrintablePageLayoutService implements IPrintablePageLayoutService {
  private readonly paperSizes = {
    A4: { width: 595, height: 842 },
    A3: { width: 842, height: 1191 },
    Letter: { width: 612, height: 792 },
    Legal: { width: 612, height: 1008 },
    Tabloid: { width: 792, height: 1224 },
  };

  private readonly defaultMargins: PageMargins = {
    top: 36, // 0.5 inch
    right: 18, // 0.25 inch
    bottom: 36, // 0.5 inch
    left: 18, // 0.25 inch
  };

  private readonly dpiConfig: DPIConfiguration = {
    screen: 96,
    print: 300,
  };

  calculatePageDimensions(
    paperSize: SequenceCardPaperSize,
    orientation: PageOrientation
  ): PageDimensions {
    const dimensions = this.paperSizes[paperSize];

    if (orientation === "landscape") {
      return {
        width: dimensions.height,
        height: dimensions.width,
      };
    }

    return {
      width: dimensions.width,
      height: dimensions.height,
    };
  }

  calculateMargins(_paperSize: SequenceCardPaperSize): PageMargins {
    // For now, use default margins for all paper sizes
    // Could be extended to have paper-specific margins
    return { ...this.defaultMargins };
  }

  calculateContentArea(
    pageSize: PageDimensions,
    margins: PageMargins
  ): Rectangle {
    return {
      x: margins.left,
      y: margins.top,
      width: pageSize.width - margins.left - margins.right,
      height: pageSize.height - margins.top - margins.bottom,
    };
  }

  calculateOptimalGrid(
    cardAspectRatio: number,
    contentArea: Rectangle,
    options: Partial<GridCalculationOptions> = {}
  ): SequenceCardGridConfig {
    const opts: GridCalculationOptions = {
      minCardsPerPage: 2,
      maxCardsPerPage: 12,
      preferSquareLayout: false,
      prioritizeCardSize: true,
      allowPartialLastPage: true,
      ...options,
    };

    let bestGrid: SequenceCardGridConfig | null = null;
    let bestScore = 0;

    // Try different grid configurations
    for (
      let totalCards = opts.minCardsPerPage;
      totalCards <= opts.maxCardsPerPage;
      totalCards++
    ) {
      for (let rows = 1; rows <= Math.ceil(Math.sqrt(totalCards)); rows++) {
        const cols = Math.ceil(totalCards / rows);

        if (rows * cols < totalCards && !opts.allowPartialLastPage) {
          continue;
        }

        const cellWidth = contentArea.width / cols;
        const cellHeight = contentArea.height / rows;

        // Calculate card dimensions maintaining aspect ratio
        let cardWidth = cellWidth * 0.9; // Leave some spacing
        let cardHeight = cardWidth / cardAspectRatio;

        if (cardHeight > cellHeight * 0.9) {
          cardHeight = cellHeight * 0.9;
          cardWidth = cardHeight * cardAspectRatio;
        }

        // Calculate score based on card size and layout efficiency
        const cardArea = cardWidth * cardHeight;
        const totalUsedArea = totalCards * cardArea;
        const totalAvailableArea = contentArea.width * contentArea.height;
        const utilization = totalUsedArea / totalAvailableArea;

        // Prefer layouts that maximize card size if prioritizeCardSize is true
        const cardSizeScore = opts.prioritizeCardSize
          ? cardArea / (contentArea.width * contentArea.height)
          : 0.5;
        const utilizationScore = Math.min(utilization, 1.0);
        const layoutScore = opts.preferSquareLayout
          ? 1 - Math.abs(rows - cols) / Math.max(rows, cols)
          : 0.5;

        const score =
          cardSizeScore * 0.4 + utilizationScore * 0.4 + layoutScore * 0.2;

        if (score > bestScore) {
          bestScore = score;
          bestGrid = {
            rows,
            columns: cols,
            spacing: Math.min(
              (cellWidth - cardWidth) / 2,
              (cellHeight - cardHeight) / 2
            ),
            cardWidth,
            cardHeight,
          };
        }
      }
    }

    // Fallback to simple 2x2 if no optimal grid found
    if (!bestGrid) {
      const cellWidth = contentArea.width / 2;
      const cellHeight = contentArea.height / 2;
      const cardWidth = cellWidth * 0.9;
      const cardHeight = cardWidth / cardAspectRatio;

      bestGrid = {
        rows: 2,
        columns: 2,
        spacing: Math.min(
          (cellWidth - cardWidth) / 2,
          (cellHeight - cardHeight) / 2
        ),
        cardWidth,
        cardHeight,
      };
    }

    return bestGrid;
  }

  getPageSizeInPixels(
    paperSize: SequenceCardPaperSize,
    orientation: PageOrientation,
    dpi: number = this.dpiConfig.screen
  ): PageDimensions {
    const pointDimensions = this.calculatePageDimensions(
      paperSize,
      orientation
    );
    const scaleFactor = dpi / 72; // Convert from points to pixels

    return {
      width: Math.round(pointDimensions.width * scaleFactor),
      height: Math.round(pointDimensions.height * scaleFactor),
    };
  }

  calculateLayout(request: LayoutCalculationRequest): LayoutCalculationResult {
    const pageDimensions = this.calculatePageDimensions(
      request.paperSize,
      request.orientation
    );
    const margins = request.margins || this.calculateMargins(request.paperSize);
    const contentArea = this.calculateContentArea(pageDimensions, margins);

    const gridOptions: GridCalculationOptions = {
      minCardsPerPage: 2,
      maxCardsPerPage: request.preferredCardsPerPage || 12,
      preferSquareLayout: false,
      prioritizeCardSize: true,
      allowPartialLastPage: true,
    };

    const gridConfig = this.calculateOptimalGrid(
      request.cardAspectRatio,
      contentArea,
      gridOptions
    );

    const cardsPerPage = gridConfig.rows * gridConfig.columns;
    const pagesNeeded = Math.ceil(request.sequenceCount / cardsPerPage);
    const cardDimensions = {
      width: gridConfig.cardWidth,
      height: gridConfig.cardHeight,
    };

    // Calculate utilization
    const cardArea = gridConfig.cardWidth * gridConfig.cardHeight;
    const totalCardArea = cardsPerPage * cardArea;
    const contentAreaSize = contentArea.width * contentArea.height;
    const utilization = Math.min(totalCardArea / contentAreaSize, 1.0);

    // Consider layout optimal if utilization > 0.6 and card size is reasonable
    const minCardSize = Math.min(contentArea.width, contentArea.height) * 0.2;
    const isOptimal =
      utilization > 0.6 &&
      Math.min(gridConfig.cardWidth, gridConfig.cardHeight) > minCardSize;

    return {
      gridConfig,
      pagesNeeded,
      cardDimensions,
      contentArea,
      utilization,
      isOptimal,
    };
  }

  validateLayout(config: PageLayoutConfig): LayoutValidationResult {
    const errors: LayoutValidationError[] = [];
    const warnings: LayoutValidationWarning[] = [];

    // Validate margins
    const margins = config.printConfiguration.margins;
    if (
      margins.top < 0 ||
      margins.right < 0 ||
      margins.bottom < 0 ||
      margins.left < 0
    ) {
      errors.push({
        code: "NEGATIVE_MARGINS",
        message: "Margins cannot be negative",
        field: "margins",
        severity: "error" as const,
      });
    }

    // Validate sequences per page
    if (config.sequencesPerPage < 1) {
      errors.push({
        code: "INVALID_SEQUENCES_PER_PAGE",
        message: "Sequences per page must be at least 1",
        field: "sequencesPerPage",
        severity: "error" as const,
      });
    }

    if (config.sequencesPerPage > 20) {
      warnings.push({
        code: "HIGH_SEQUENCES_PER_PAGE",
        message:
          "High number of sequences per page may result in very small cards",
        suggestion:
          "Consider reducing sequences per page for better readability",
      });
    }

    // Check if margins are too large
    const pageDimensions = this.calculatePageDimensions(
      config.printConfiguration.paperSize,
      config.printConfiguration.orientation
    );
    const totalMarginWidth = margins.left + margins.right;
    const totalMarginHeight = margins.top + margins.bottom;

    if (totalMarginWidth > pageDimensions.width * 0.5) {
      warnings.push({
        code: "LARGE_HORIZONTAL_MARGINS",
        message: "Horizontal margins are very large",
        suggestion: "Consider reducing left and right margins",
      });
    }

    if (totalMarginHeight > pageDimensions.height * 0.5) {
      warnings.push({
        code: "LARGE_VERTICAL_MARGINS",
        message: "Vertical margins are very large",
        suggestion: "Consider reducing top and bottom margins",
      });
    }

    return {
      isValid: errors.length === 0,
      errors: errors.map((e) => e.message),
      warnings: warnings.map((w) => w.message),
    };
  }

  getDPIConfiguration(): DPIConfiguration {
    return { ...this.dpiConfig };
  }

  convertMeasurement(value: number, fromUnit: string, toUnit: string): number {
    const units = {
      points: 1,
      inches: 72,
      millimeters: 72 / 25.4,
      centimeters: 72 / 2.54,
    } as const;

    const fromPoints = units[fromUnit as keyof typeof units];
    const toPoints = units[toUnit as keyof typeof units];

    if (!fromPoints || !toPoints) {
      throw new Error(
        `Invalid measurement unit. Supported: ${Object.keys(units).join(", ")}`
      );
    }

    // Convert to points, then to target unit
    const valueInPoints = value * fromPoints;
    return valueInPoints / toPoints;
  }
}
