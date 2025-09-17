/**
 * Read State Factory
 *
 * Factory function for creating read module state with PDF and flipbook management.
 * Uses persistent PDF state to avoid reloading PDFs when navigating between tabs.
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
    await persistentPDFState.ensurePDFLoaded(url);
    
    // Restore the saved page number for this PDF
    const savedPage = persistentPDFState.getCurrentPage(url);
    currentPage = savedPage;
    console.log(`📚 ReadState: Restored page ${savedPage} for ${url}`);
  }

  /**
   * Restore the flipbook to the saved page position
   */
  async function restoreToSavedPage(): Promise<void> {
    if (!currentPDFUrl || !isFlipBookInitialized) return;
    
    // Get the saved page AFTER the flipbook is fully initialized
    const savedPage = persistentPDFState.getCurrentPage(currentPDFUrl);
    currentPage = savedPage;
    
    console.log(`📚 ReadState: Attempting to restore to page ${savedPage}`);
    
    // Set the flipbook to the saved page
    if (savedPage > 1) {
      // Use multiple attempts with increasing delays to ensure it works
      setTimeout(() => {
        console.log(`📚 ReadState: First attempt to go to page ${savedPage}`);
        flipBookService.goToPage(savedPage);
      }, 100);
      
      setTimeout(() => {
        console.log(`📚 ReadState: Second attempt to go to page ${savedPage}`);
        flipBookService.goToPage(savedPage);
      }, 500);
      
      setTimeout(() => {
        console.log(`📚 ReadState: Final attempt to go to page ${savedPage}`);
        flipBookService.goToPage(savedPage);
      }, 1000);
    }
    
    console.log(`📚 ReadState: Page restoration initiated for page ${savedPage}`);
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

      if (persistentPDFState.pages.length > 0) {
        const firstPage = persistentPDFState.pages[0];
        console.log("📚 ReadState: PDF page dimensions", {
          width: firstPage.width,
          height: firstPage.height,
          aspectRatio: firstPage.width / firstPage.height
        });
      }

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
          console.log(`📚 ReadState: Saved page ${pageNumber} for ${currentPDFUrl}`);
        }
      });

      // Load pages if available
      if (persistentPDFState.hasPages) {
        await flipBookService.loadPages(persistentPDFState.pages);
      }

      isFlipBookInitialized = true;
      
      // CRITICAL: Get the saved page AFTER the flipbook is initialized and pages are loaded
      await restoreToSavedPage();

      console.log(`📚 ReadState: Flipbook initialized successfully`);
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