/**
 * Page Layout State - Svelte 5 Runes
 *
 * Manages printable page layout state including page creation, layout configuration,
 * and page navigation for the sequence card tab.
 */

import type {
  IPageFactoryService,
  IPrintablePageLayoutService,
} from "$contracts";
import type {
  GridCalculationOptions,
  LayoutCalculationResult,
  Page,
  PageCreationOptions,
  PageLayoutConfig,
  PageOrientation,
  PrintConfiguration,
  SequenceCardPaperSize,
  SequenceData,
} from "$domain";

export interface PageLayoutState {
  // Page data
  readonly pages: Page[];
  readonly currentPage: number;
  readonly totalPages: number;
  readonly isLoading: boolean;
  readonly error: string | null;

  // Layout configuration
  readonly paperSize: SequenceCardPaperSize;
  readonly orientation: PageOrientation;
  readonly sequencesPerPage: number;
  readonly enableOptimization: boolean;
  readonly showPageNumbers: boolean;
  readonly showMargins: boolean;

  // Layout calculation results
  readonly layoutResult: LayoutCalculationResult | null;

  // Actions
  createPages: (sequences: SequenceData[]) => Promise<void>;
  setPaperSize: (size: SequenceCardPaperSize) => void;
  setOrientation: (orientation: PageOrientation) => void;
  setSequencesPerPage: (count: number) => void;
  setOptimization: (enabled: boolean) => void;
  setCurrentPage: (pageIndex: number) => void;
  setShowPageNumbers: (show: boolean) => void;
  setShowMargins: (show: boolean) => void;
  calculateOptimalLayout: (
    sequences: SequenceData[]
  ) => LayoutCalculationResult | null;
  regeneratePages: () => Promise<void>;
  resetToDefaults: () => void;
}

export function createPageLayoutState(
  layoutService: IPrintablePageLayoutService,
  pageFactoryService: IPageFactoryService,
  initialSequences: SequenceData[] = []
): PageLayoutState {
  // Core state
  let pages = $state<Page[]>([]);
  let currentPage = $state(0);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  // Layout configuration state
  let paperSize = $state<SequenceCardPaperSize>("A4");
  let orientation = $state<PageOrientation>("portrait");
  let sequencesPerPage = $state(6);
  let enableOptimization = $state(true);
  let showPageNumbers = $state(true);
  let showMargins = $state(false);

  // Cached sequences for regeneration
  let cachedSequences = $state<SequenceData[]>(initialSequences);

  // Layout calculation result
  let layoutResult = $state<LayoutCalculationResult | null>(null);

  // Computed values
  const totalPages = $derived(pages.length);

  // Default layout configuration
  const defaultGridOptions: GridCalculationOptions = {
    minCardsPerPage: 2,
    maxCardsPerPage: 12,
    preferSquareLayout: false,
    prioritizeCardSize: true,
    allowPartialLastPage: true,
  };

  // Create layout configuration from current state
  const layoutConfig = $derived(() => {
    const margins = layoutService.calculateMargins(paperSize);

    const printConfiguration: PrintConfiguration = {
      paperSize,
      orientation,
      margins,
      dpi: 300,
      enablePageNumbers: showPageNumbers,
      enableHeader: false,
      enableFooter: false,
    };

    const config: PageLayoutConfig = {
      printConfiguration,
      gridOptions: defaultGridOptions,
      sequencesPerPage: 8, // Default value
      enableOptimization: true,
    };

    return config;
  });

  // Actions
  async function createPages(sequences: SequenceData[]): Promise<void> {
    try {
      isLoading = true;
      error = null;
      cachedSequences = [...sequences];

      // Calculate layout if optimization is enabled
      if (enableOptimization && sequences.length > 0) {
        const cardAspectRatio = 0.7; // Default card aspect ratio
        // const pageDimensions = layoutService.calculatePageDimensions(
        //   paperSize,
        //   orientation
        // ); // For future use
        const margins = layoutService.calculateMargins(paperSize);
        // const contentArea = layoutService.calculateContentArea(
        //   pageDimensions,
        //   margins
        // ); // For future use

        const calculationRequest = {
          paperSize,
          orientation,
          margins,
          gridOptions: defaultGridOptions,
          cardAspectRatio,
          sequenceCount: sequences.length,
          preferredCardsPerPage: sequencesPerPage,
        };

        layoutResult = layoutService.calculateLayout(calculationRequest);

        // Update sequences per page based on optimization
        if (layoutResult.isOptimal) {
          sequencesPerPage =
            layoutResult.gridConfig.rows * layoutResult.gridConfig.columns;
        }
      }

      // Create page creation options
      const options: PageCreationOptions = {
        layout: layoutConfig(),
        sequences,
        startPageNumber: 1,
        enableEmptyPages: sequences.length === 0,
        emptyPageMessage: "No sequences available for this filter",
      };

      // Validate options
      const validation = pageFactoryService.validatePageOptions(options);
      if (!validation.isValid) {
        throw new Error(
          `Invalid page options: ${validation.errors.join(", ")}`
        );
      }

      // Create pages
      const newPages = pageFactoryService.createPages(sequences, options);
      pages = newPages;

      // Reset current page if it's out of bounds
      if (currentPage >= newPages.length) {
        currentPage = Math.max(0, newPages.length - 1);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to create pages";
      pages = [];
      console.error("Page creation failed:", err);
    } finally {
      isLoading = false;
    }
  }

  function setPaperSize(size: SequenceCardPaperSize): void {
    if (paperSize !== size) {
      paperSize = size;
      layoutResult = null; // Reset layout calculation
      // Manually regenerate pages if we have cached sequences
      if (cachedSequences.length > 0) {
        regeneratePages();
      }
    }
  }

  function setOrientation(newOrientation: PageOrientation): void {
    if (orientation !== newOrientation) {
      orientation = newOrientation;
      layoutResult = null; // Reset layout calculation
      // Manually regenerate pages if we have cached sequences
      if (cachedSequences.length > 0) {
        regeneratePages();
      }
    }
  }

  function setSequencesPerPage(count: number): void {
    const validCount = Math.max(1, Math.min(20, count));
    if (sequencesPerPage !== validCount) {
      sequencesPerPage = validCount;
      layoutResult = null; // Reset layout calculation
    }
  }

  function setOptimization(enabled: boolean): void {
    if (enableOptimization !== enabled) {
      enableOptimization = enabled;
      layoutResult = null; // Reset layout calculation
    }
  }

  function setCurrentPage(pageIndex: number): void {
    const validIndex = Math.max(0, Math.min(totalPages - 1, pageIndex));
    currentPage = validIndex;
  }

  function setShowPageNumbers(show: boolean): void {
    showPageNumbers = show;
  }

  function setShowMargins(show: boolean): void {
    showMargins = show;
  }

  function calculateOptimalLayout(
    sequences: SequenceData[]
  ): LayoutCalculationResult | null {
    if (sequences.length === 0) return null;

    try {
      const cardAspectRatio = 0.7; // Default card aspect ratio
      // const pageDimensions = layoutService.calculatePageDimensions(
      //   paperSize,
      //   orientation
      // ); // For future use
      const margins = layoutService.calculateMargins(paperSize);

      const calculationRequest = {
        paperSize,
        orientation,
        margins,
        cardAspectRatio,
        sequenceCount: sequences.length,
        preferredCardsPerPage: sequencesPerPage,
      };

      return layoutService.calculateLayout(calculationRequest);
    } catch (err) {
      console.error("Layout calculation failed:", err);
      return null;
    }
  }

  async function regeneratePages(): Promise<void> {
    if (cachedSequences.length > 0) {
      await createPages(cachedSequences);
    }
  }

  function resetToDefaults(): void {
    paperSize = "A4";
    orientation = "portrait";
    sequencesPerPage = 6;
    enableOptimization = true;
    showPageNumbers = true;
    showMargins = false;
    currentPage = 0;
    layoutResult = null;
    error = null;
  }

  // Note: Auto-regeneration disabled to prevent circular dependencies
  // Layout changes should be handled manually by calling regeneratePages()
  // when needed (e.g., when user changes paper size, orientation, etc.)

  // Initialize with sequences if provided
  if (initialSequences.length > 0) {
    createPages(initialSequences);
  }

  return {
    // State
    get pages() {
      return pages;
    },
    get currentPage() {
      return currentPage;
    },
    get totalPages() {
      return totalPages;
    },
    get isLoading() {
      return isLoading;
    },
    get error() {
      return error;
    },

    // Configuration
    get paperSize() {
      return paperSize;
    },
    get orientation() {
      return orientation;
    },
    get sequencesPerPage() {
      return sequencesPerPage;
    },
    get enableOptimization() {
      return enableOptimization;
    },
    get showPageNumbers() {
      return showPageNumbers;
    },
    get showMargins() {
      return showMargins;
    },

    // Layout result
    get layoutResult() {
      return layoutResult;
    },

    // Actions
    createPages,
    setPaperSize,
    setOrientation,
    setSequencesPerPage,
    setOptimization,
    setCurrentPage,
    setShowPageNumbers,
    setShowMargins,
    calculateOptimalLayout,
    regeneratePages,
    resetToDefaults,
  };
}
