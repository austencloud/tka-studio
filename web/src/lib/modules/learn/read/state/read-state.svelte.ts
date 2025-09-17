/**
 * Read State Factory
 *
 * Factory function for creating read module state with PDF and flipbook management.
 * Uses persistent PDF state to avoid reloading PDFs when navigating between tabs.
 */

import type { FlipBookConfig } from "../domain";
import type { IFlipBookService, IPDFService } from "../services/contracts";
import { persistentPDFState } from "./persistent-pdf-state.svelte";

/**
 * Create read state for managing PDF loading and flipbook display
 */
export function createReadState(
  pdfService: IPDFService,
  flipBookService: IFlipBookService
) {
  // Track the current PDF URL for page persistence
  let currentPDFUrl = $state<string>("");
  
  // Flipbook state (component-specific)
  let currentPage = $state<number>(1);
  let isFlipBookInitialized = $state<boolean>(false);

  // Default flipbook configuration
  const defaultConfig: FlipBookConfig = {
    width: 400,
    height: 600,
    showCover: true,
    drawShadow: true,
    flippingTime: 1000,
    maxShadowOpacity: 0.8,
    mobileScrollSupport: true,
  };

  /**
   * Load a PDF from the specified URL (uses persistent state)
   */
  async function loadPDF(url: string): Promise<void> {
    console.log(`📚 ReadState: Loading PDF from ${url}`);
    currentPDFUrl = url;
    
    // Get the saved page BEFORE loading to avoid showing page 1 first
    const savedPage = persistentPDFState.getCurrentPage(url);
    currentPage = savedPage;
    console.log(`📚 ReadState: Set current page to ${savedPage} before loading`);
    
    await persistentPDFState.ensurePDFLoaded(url);
    
    console.log(`📚 ReadState: PDF loaded, confirmed page ${currentPage} for ${url}`);
  }

  /**
   * Restore the flipbook to the saved page position (if needed)
   */
  async function restoreToSavedPage(): Promise<void> {
    if (!currentPDFUrl || !isFlipBookInitialized) return;
    
    // Only restore if we're not already on the correct page
    const flipBookCurrentPage = flipBookService.getCurrentPage();
    if (flipBookCurrentPage !== currentPage) {
      console.log(`📚 ReadState: Syncing flipbook page from ${flipBookCurrentPage} to ${currentPage}`);
      flipBookService.goToPage(currentPage);
    }
  }

  /**
   * Initialize the flipbook with the loaded pages
   */
  async function initializeFlipBook(
    container: HTMLElement,
    config: Partial<FlipBookConfig> = {}
  ): Promise<void> {
    if (isFlipBookInitialized) {
      console.log("📚 ReadState: Flipbook already initialized");
      return;
    }

    try {
      console.log("📚 ReadState: Initializing flipbook");

      // Merge with default config
      const finalConfig = { ...defaultConfig, ...config };
      console.log("📚 ReadState: Using flipbook config", finalConfig);

      // Initialize the flipbook
      await flipBookService.initialize(container, finalConfig);

      // Set up page change listener to save current page
      flipBookService.onPageChange((pageNumber) => {
        console.log(`📚 ReadState: Page changed to ${pageNumber}`);
        currentPage = pageNumber;
        // Save the current page for this PDF URL
        if (currentPDFUrl) {
          persistentPDFState.setCurrentPage(currentPDFUrl, pageNumber);
        }
      });

      // Load the pages
      const pages = persistentPDFState.pages;
      if (pages.length > 0) {
        console.log("📚 ReadState: Loading pages into flipbook");
        await flipBookService.loadPages(pages);
        
        // Add a small delay to allow flipbook to fully initialize
        if (currentPage > 1) {
          console.log(`📚 ReadState: Setting flipbook to page ${currentPage} after initialization`);
          // Use setTimeout to ensure flipbook is fully ready
          setTimeout(() => {
            console.log(`📚 ReadState: Now navigating flipbook to page ${currentPage}`);
            flipBookService.goToPage(currentPage);
          }, 100);
        }
      }

      isFlipBookInitialized = true;
      console.log("📚 ReadState: Flipbook initialization complete");
    } catch (error) {
      console.error("📚 ReadState: Error initializing flipbook", error);
      throw new Error(`Failed to initialize flipbook: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  /**
   * Navigate to a specific page
   */
  function goToPage(pageNumber: number): void {
    if (!isFlipBookInitialized) return;
    
    flipBookService.goToPage(pageNumber);
    // Page change listener will handle saving the page
  }

  /**
   * Go to the next page
   */
  function nextPage(): void {
    if (!isFlipBookInitialized) return;
    
    flipBookService.nextPage();
    // Page change listener will handle saving the page
  }

  /**
   * Go to the previous page
   */
  function previousPage(): void {
    if (!isFlipBookInitialized) return;
    
    flipBookService.previousPage();
    // Page change listener will handle saving the page
  }

  /**
   * Clean up resources (only flipbook, keep PDF in persistent state)
   */
  function cleanup(): void {
    console.log("📖 ReadState: Cleaning up resources");
    
    flipBookService.destroy();
    
    // Reset only flipbook state, keep PDF data in persistent state
    currentPage = 1;
    isFlipBookInitialized = false;
  }

  // Computed properties (delegate to persistent state)
  const totalPages = $derived(() => persistentPDFState.totalPages);
  const hasPages = $derived(() => persistentPDFState.hasPages);
  const isReady = $derived(() => persistentPDFState.isReady);

  return {
    // State (delegate to persistent state)
    get documentInfo() { return persistentPDFState.documentInfo; },
    get pages() { return persistentPDFState.pages; },
    get loadingState() { return persistentPDFState.loadingState; },
    get currentPage() { return currentPage; },
    get isFlipBookInitialized() { return isFlipBookInitialized; },
    
    // Computed
    get totalPages() { return totalPages; },
    get hasPages() { return hasPages; },
    get isReady() { return isReady; },
    
    // Actions
    loadPDF,
    initializeFlipBook,
    goToPage,
    nextPage,
    previousPage,
    cleanup,
    restoreToSavedPage,
  };
}