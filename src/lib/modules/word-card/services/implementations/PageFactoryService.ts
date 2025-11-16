/**
 * Page Factory Service Implementation
 *
 * Handles creation of printable pages with word cards distributed
 * across them according to layout specifications.
 *
 * Based on desktop application's printable_factory.py functionality.
 */

import type { SequenceData } from "$shared";
import type {
  GridCalculationOptions,
  LayoutCalculationResult,
  LayoutValidationError,
  LayoutValidationResult,
  LayoutValidationWarning,
  Page,
  PageCreationOptions,
  PageLayoutConfig,
  Rectangle,
  WordCardGridConfig,
} from "$wordcard/domain";

// Import the correct interfaces from word-card-models
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IPrintablePageLayoutService } from "../contracts";
import type { IPageFactoryService } from "../contracts";

@injectable()
export class PageFactoryService implements IPageFactoryService {
  constructor(
    @inject(TYPES.IPrintablePageLayoutService)
    private readonly layoutService: IPrintablePageLayoutService
  ) {}

  createPage(sequences: SequenceData[], config: PageCreationOptions): Page {
    // TODO: Implement single page creation
    return this.createPages(sequences, config)[0]!;
  }

  calculateLayout(sequences: SequenceData[]): LayoutCalculationResult {
    // TODO: Implement layout calculation - this is a placeholder
    const defaultGridConfig: WordCardGridConfig = {
      rows: 1,
      columns: sequences.length || 1,
      spacing: 10,
      cardWidth: 100,
      cardHeight: 140,
    };

    const defaultPageConfig: PageLayoutConfig = {
      printConfig: {
        paperSize: "A4",
        orientation: "portrait",
        margins: { top: 36, right: 18, bottom: 36, left: 18 },
        dpi: 300,
        enablePageNumbers: false,
        enableHeader: false,
        enableFooter: false,
      },
      gridOptions: {
        minCardsPerPage: 1,
        maxCardsPerPage: 12,
        preferSquareLayout: false,
        prioritizeCardSize: true,
        allowPartialLastPage: true,
      },
      sequencesPerPage: sequences.length || 1,
      enableOptimization: false,
    };

    return {
      isOptimal: false,
      gridConfig: defaultGridConfig,
      pageConfig: defaultPageConfig,
      utilization: 0.5,
    };
  }

  createPages(sequences: SequenceData[], options: PageCreationOptions): Page[] {
    // Validate options first
    const validation = this.validatePageOptions(options);
    if (!validation.isValid) {
      throw new Error(`Invalid page options: ${validation.errors.join(", ")}`);
    }

    const pages: Page[] = [];
    const { layout, startPageNumber = 1 } = options;

    // If no sequences and empty pages not enabled, return empty array
    if (sequences.length === 0 && !options.enableEmptyPages) {
      return pages;
    }

    // Calculate layout details
    const layoutConfig = layout;
    const pageDimensions = this.layoutService.calculatePageDimensions(
      layoutConfig.printConfig.paperSize,
      layoutConfig.printConfig.orientation
    );
    const margins = layoutConfig.printConfig.margins;
    const contentArea = this.layoutService.calculateContentArea(
      pageDimensions,
      margins
    );

    // Get card aspect ratio from first sequence or use default
    const cardAspectRatio = this.getCardAspectRatio(sequences[0]) || 0.7;

    // Calculate optimal grid if not fixed
    let sequencesPerPage = layoutConfig.sequencesPerPage;
    if (layoutConfig.enableOptimization) {
      const optimalCardsPerPage = this.getOptimalCardsPerPage(
        contentArea,
        cardAspectRatio,
        layoutConfig.gridOptions
      );
      sequencesPerPage = optimalCardsPerPage;
    }

    // If no sequences, create single empty page
    if (sequences.length === 0) {
      const emptyPage = this.createEmptyPage(
        startPageNumber,
        layoutConfig,
        options.emptyPageMessage
      );
      return [emptyPage];
    }

    // Distribute sequences across pages
    const sequenceGroups = this.distributeSequences(
      sequences,
      sequencesPerPage
    );

    // Create pages from sequence groups
    sequenceGroups.forEach((sequenceGroup, index) => {
      const pageNumber = startPageNumber + index;
      const gridConfig = this.calculateGridForSequences(
        sequenceGroup,
        contentArea,
        cardAspectRatio,
        layoutConfig
      );

      const page: Page = {
        id: `page-${pageNumber}`,
        sequences: sequenceGroup,
        layout: gridConfig,
        pageNumber,
        paperSize: layoutConfig.printConfig.paperSize,
        orientation: layoutConfig.printConfig.orientation,
        margins: margins,
      };

      pages.push(page);
    });

    return pages;
  }

  createEmptyPage(
    pageNumber: number,
    layout: PageLayoutConfig,
    _message?: string
  ): Page {
    const pageDimensions = this.layoutService.calculatePageDimensions(
      layout.printConfig.paperSize,
      layout.printConfig.orientation
    );
    const margins = layout.printConfig.margins;
    const contentArea = this.layoutService.calculateContentArea(
      pageDimensions,
      margins
    );

    // Create minimal grid config for empty page
    const gridConfig: WordCardGridConfig = {
      rows: 1,
      columns: 1,
      spacing: 0,
      cardWidth: contentArea.width,
      cardHeight: contentArea.height,
    };

    return {
      id: `empty-page-${pageNumber}`,
      sequences: [],
      layout: gridConfig,
      pageNumber,
      paperSize: layout.printConfig.paperSize,
      orientation: layout.printConfig.orientation,
      margins: margins,
    };
  }

  calculatePagesNeeded(
    sequenceCount: number,
    sequencesPerPage: number
  ): number {
    if (sequenceCount === 0) return 1; // At least one page for empty state
    return Math.ceil(sequenceCount / sequencesPerPage);
  }

  distributeSequences(
    sequences: SequenceData[],
    sequencesPerPage: number
  ): SequenceData[][] {
    const groups: SequenceData[][] = [];

    for (let i = 0; i < sequences.length; i += sequencesPerPage) {
      const group = sequences.slice(i, i + sequencesPerPage);
      groups.push(group);
    }

    return groups;
  }

  generatePageNumbers(pageCount: number, startNumber: number = 1): number[] {
    return Array.from({ length: pageCount }, (_, index) => startNumber + index);
  }

  validatePageOptions(options: PageCreationOptions): LayoutValidationResult {
    const errors: LayoutValidationError[] = [];
    const warnings: LayoutValidationWarning[] = [];

    // Validate sequences per page
    const optionsLayout = options.layout;
    if (optionsLayout.sequencesPerPage < 1) {
      errors.push({
        code: "INVALID_SEQUENCES_PER_PAGE",
        message: "Sequences per page must be at least 1",
        field: "sequencesPerPage",
        severity: "error" as const,
      });
    }

    // Validate start page number
    if (options.startPageNumber < 1) {
      errors.push({
        code: "INVALID_START_PAGE",
        message: "Start page number must be at least 1",
        field: "startPageNumber",
        severity: "error" as const,
      });
    }

    // Check if sequences array is too large
    if (options.sequences.length > 1000) {
      warnings.push({
        code: "LARGE_SEQUENCE_COUNT",
        message: "Large number of sequences may impact performance",
        severity: "warning" as const,
        suggestion: "Consider processing sequences in batches",
      });
    }

    // Validate layout configuration
    const layoutValidation = this.layoutService.validateLayout(optionsLayout);
    // Convert layout validation results to our format
    layoutValidation.errors.forEach((error: string) => {
      errors.push({
        code: "LAYOUT_ERROR",
        message: error,
        field: "layout",
        severity: "error" as const,
      });
    });

    layoutValidation.warnings.forEach((warning: string) => {
      warnings.push({
        code: "LAYOUT_WARNING",
        message: warning,
        severity: "warning" as const,
        suggestion: "Review layout configuration",
      });
    });
    // Note: LayoutValidationResult doesn't have suggestions property
    // suggestions.push(...layoutValidation.suggestions);

    return {
      isValid: errors.length === 0,
      errors: errors.map((e) => e.message),
      warnings: warnings.map((w) => w.message),
    };
  }

  getOptimalCardsPerPage(
    contentArea: Rectangle,
    cardAspectRatio: number,
    options: Partial<GridCalculationOptions> = {}
  ): number {
    const gridConfig = this.layoutService.calculateOptimalGrid(
      cardAspectRatio,
      contentArea,
      options
    );

    return gridConfig.rows * gridConfig.columns;
  }

  private calculateGridForSequences(
    sequences: SequenceData[],
    contentArea: Rectangle,
    cardAspectRatio: number,
    layout: PageLayoutConfig
  ): WordCardGridConfig {
    // If we have a fixed sequences per page, use that
    const targetSequences = Math.max(sequences.length, layout.sequencesPerPage);

    // Calculate grid based on actual sequence count on this page
    const gridOptions: GridCalculationOptions = {
      minCardsPerPage: sequences.length,
      maxCardsPerPage: targetSequences,
      preferSquareLayout: layout.gridOptions.preferSquareLayout || false,
      prioritizeCardSize: layout.gridOptions.prioritizeCardSize || true,
      allowPartialLastPage: layout.gridOptions.allowPartialLastPage || true,
    };

    return this.layoutService.calculateOptimalGrid(
      cardAspectRatio,
      contentArea,
      gridOptions
    );
  }

  private getCardAspectRatio(_sequence?: SequenceData): number {
    // For now, return default aspect ratio
    // This could be enhanced to calculate based on actual sequence content
    // or read from sequence metadata
    return 0.7; // Width/Height ratio typical for word cards
  }
}
