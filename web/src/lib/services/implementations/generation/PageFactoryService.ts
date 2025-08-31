/**
 * Page Factory Service Implementation
 *
 * Handles creation of printable pages with sequence cards distributed
 * across them according to layout specifications.
 *
 * Based on desktop application's printable_factory.py functionality.
 */

import type { SequenceData } from "$domain";
import type {
  IPageFactoryService,
  IPrintablePageLayoutService,
} from "$lib/services/contracts/sequence-interfaces";
import { inject, injectable } from "inversify";
import type {
  GridCalculationOptions,
  LayoutSuggestion,
  LayoutValidationError,
  LayoutValidationResult,
  LayoutValidationWarning,
  Page,
  PageCreationOptions,
  PageLayoutConfig,
  Rectangle,
  SequenceCardGridConfig,
} from "../../../domain/sequence-card/PageLayoutTypes";
import { TYPES } from "../../inversify/types";

@injectable()
export class PageFactoryService implements IPageFactoryService {
  constructor(
    @inject(TYPES.IPrintablePageLayoutService)
    private readonly layoutService: IPrintablePageLayoutService
  ) {}

  createPages(sequences: SequenceData[], options: PageCreationOptions): Page[] {
    // Validate options first
    const validation = this.validatePageOptions(options);
    if (!validation.isValid) {
      throw new Error(
        `Invalid page options: ${validation.errors.map((e) => e.message).join(", ")}`
      );
    }

    const pages: Page[] = [];
    const { layout, startPageNumber = 1 } = options;

    // If no sequences and empty pages not enabled, return empty array
    if (sequences.length === 0 && !options.enableEmptyPages) {
      return pages;
    }

    // Calculate layout details
    const pageDimensions = this.layoutService.calculatePageDimensions(
      layout.printConfiguration.paperSize,
      layout.printConfiguration.orientation
    );
    const margins = layout.printConfiguration.margins;
    const contentArea = this.layoutService.calculateContentArea(
      pageDimensions,
      margins
    );

    // Get card aspect ratio from first sequence or use default
    const cardAspectRatio = this.getCardAspectRatio(sequences[0]) || 0.7;

    // Calculate optimal grid if not fixed
    let sequencesPerPage = layout.sequencesPerPage;
    if (layout.enableOptimization) {
      const optimalCardsPerPage = this.getOptimalCardsPerPage(
        contentArea,
        cardAspectRatio,
        layout.gridOptions
      );
      sequencesPerPage = optimalCardsPerPage;
    }

    // If no sequences, create single empty page
    if (sequences.length === 0) {
      const emptyPage = this.createEmptyPage(
        startPageNumber,
        layout,
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
        layout
      );

      const page: Page = {
        id: `page-${pageNumber}`,
        sequences: sequenceGroup,
        layout: gridConfig,
        pageNumber,
        paperSize: layout.printConfiguration.paperSize,
        orientation: layout.printConfiguration.orientation,
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
      layout.printConfiguration.paperSize,
      layout.printConfiguration.orientation
    );
    const margins = layout.printConfiguration.margins;
    const contentArea = this.layoutService.calculateContentArea(
      pageDimensions,
      margins
    );

    // Create minimal grid config for empty page
    const gridConfig: SequenceCardGridConfig = {
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
      paperSize: layout.printConfiguration.paperSize,
      orientation: layout.printConfiguration.orientation,
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
    const suggestions: LayoutSuggestion[] = [];

    // Validate sequences per page
    if (options.layout.sequencesPerPage < 1) {
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
        suggestion: "Consider processing sequences in batches",
      });
    }

    // Validate layout configuration
    const layoutValidation = this.layoutService.validateLayout(options.layout);
    errors.push(...layoutValidation.errors);
    warnings.push(...layoutValidation.warnings);
    // Note: LayoutValidationResult doesn't have suggestions property
    // suggestions.push(...layoutValidation.suggestions);

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      suggestions,
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
  ): SequenceCardGridConfig {
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
    return 0.7; // Width/Height ratio typical for sequence cards
  }
}
