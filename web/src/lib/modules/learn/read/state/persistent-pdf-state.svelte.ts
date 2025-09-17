/**
 * Persistent PDF State
 *
 * Global state that persists PDF data across component unmounting/remounting.
 * This ensures the PDF only loads once and stays in memory while navigating between tabs.
 */

import { resolve, TYPES } from "$shared";
import type { PDFDocumentInfo, PDFLoadingState, PDFPageData } from "../domain";
import type { IPDFService } from "../services/contracts";

class PersistentPDFState {
  // PDF state
  private _documentInfo = $state<PDFDocumentInfo | null>(null);
  private _pages = $state<PDFPageData[]>([]);
  private _loadingState = $state<PDFLoadingState>({
    isLoading: false,
    progress: 0,
    stage: "",
    error: undefined,
  });

  // Track loaded URLs to avoid reloading
  private _loadedUrls = new Set<string>();
  
  // Track current page for each PDF URL
  private _currentPages = new Map<string, number>();
  
  // Services (lazy loaded)
  private pdfService: IPDFService | null = null;

  constructor() {
    // Services will be resolved lazily when needed
  }

  private getPDFService(): IPDFService {
    if (!this.pdfService) {
      this.pdfService = resolve(TYPES.IPDFService) as IPDFService;
    }
    return this.pdfService;
  }

  /**
   * Load PDF if not already loaded
   */
  async ensurePDFLoaded(url: string): Promise<void> {
    // If already loaded for this URL, skip loading
    if (this._loadedUrls.has(url) && this._pages.length > 0) {
      console.log("📖 PersistentPDFState: PDF already loaded, skipping reload");
      return;
    }

    // Check if we have cached data in IndexedDB to avoid loading UI
    const pdfService = this.getPDFService();
    const hasCachedData = await pdfService.hasCachedPDF(url);
    
    if (hasCachedData) {
      console.log("📖 PersistentPDFState: Found cached data, loading silently");
      await this.loadPDFSilently(url);
    } else {
      console.log("📖 PersistentPDFState: No cached data, showing loading UI");
      await this.loadPDF(url);
    }
  }

  /**
   * Force reload PDF (for cache busting if needed)
   */
  async reloadPDF(url: string): Promise<void> {
    this._loadedUrls.delete(url);
    await this.loadPDF(url);
  }

  /**
   * Load a PDF from the specified URL
   */
  private async loadPDF(url: string): Promise<void> {
    try {
      console.log("📖 PersistentPDFState: Loading PDF from", url);
      
      this._loadingState.isLoading = true;
      this._loadingState.progress = 0;
      this._loadingState.stage = "Loading PDF document...";
      this._loadingState.error = undefined;

      // Load the PDF document
      const pdfService = this.getPDFService();
      const documentInfo = await pdfService.loadPDF(url);
      this._documentInfo = documentInfo;

      this._loadingState.stage = "Converting pages to images...";

      // Convert all pages to images
      const pages = await pdfService.convertPagesToImages((progress, stage) => {
        this._loadingState.progress = progress;
        this._loadingState.stage = stage;
      });
      this._pages = pages;

      this._loadingState.isLoading = false;
      this._loadingState.stage = "";
      
      // Mark this URL as loaded
      this._loadedUrls.add(url);
      
      console.log("📖 PersistentPDFState: PDF loaded with", this._pages.length, "pages");
    } catch (error) {
      console.error("📖 PersistentPDFState: Error loading PDF", error);
      this._loadingState.isLoading = false;
      this._loadingState.error = error instanceof Error ? error.message : "Unknown error";
      this._loadingState.stage = "Error loading PDF";
    }
  }

  /**
   * Load a PDF silently without showing loading UI (for cached data)
   */
  private async loadPDFSilently(url: string): Promise<void> {
    try {
      console.log("📖 PersistentPDFState: Loading PDF silently (cached) from", url);
      
      // Show simple loading state without progress
      this._loadingState.isLoading = true;
      this._loadingState.progress = 0;
      this._loadingState.stage = "Loading from cache...";
      this._loadingState.error = undefined;

      // Load the PDF document
      const pdfService = this.getPDFService();
      const documentInfo = await pdfService.loadPDF(url);
      this._documentInfo = documentInfo;

      // Convert all pages to images (should be fast with cache)
      const pages = await pdfService.convertPagesToImages();
      this._pages = pages;

      this._loadingState.isLoading = false;
      this._loadingState.stage = "";
      
      // Mark this URL as loaded
      this._loadedUrls.add(url);
      
      console.log("📖 PersistentPDFState: PDF loaded silently with", this._pages.length, "pages");
    } catch (error) {
      console.error("📖 PersistentPDFState: Error loading PDF silently", error);
      this._loadingState.isLoading = false;
      this._loadingState.error = error instanceof Error ? error.message : "Unknown error";
      this._loadingState.stage = "Error loading PDF";
    }
  }

  /**
   * Check if a specific URL is already loaded
   */
  isLoaded(url: string): boolean {
    return this._loadedUrls.has(url) && this._pages.length > 0;
  }

  /**
   * Get the current page number for a specific PDF URL
   */
  getCurrentPage(url: string): number {
    console.log(`📖 PersistentPDFState: Getting current page for ${url}`);
    
    // First check in-memory cache
    const memoryPage = this._currentPages.get(url);
    if (memoryPage) {
      console.log(`📖 PersistentPDFState: Found page ${memoryPage} in memory for ${url}`);
      return memoryPage;
    }
    
    // Fallback to localStorage
    try {
      const storageKey = `pdf-page-${url}`;
      const savedPage = localStorage.getItem(storageKey);
      console.log(`📖 PersistentPDFState: localStorage key ${storageKey} = ${savedPage}`);
      
      if (savedPage) {
        const pageNumber = parseInt(savedPage, 10);
        // Use document numPages if available, otherwise fall back to loaded pages count
        const maxPages = this._documentInfo?.numPages ?? this.totalPages;
        if (pageNumber >= 1 && (maxPages === 0 || pageNumber <= maxPages)) {
          console.log(`📖 PersistentPDFState: Restored page ${pageNumber} from localStorage for ${url}`);
          // Update in-memory cache
          this._currentPages.set(url, pageNumber);
          return pageNumber;
        } else {
          console.log(`📖 PersistentPDFState: Page ${pageNumber} out of range (1-${maxPages}) for ${url}`);
        }
      }
    } catch (error) {
      console.warn("📖 PersistentPDFState: Could not read from localStorage:", error);
    }
    
    console.log(`📖 PersistentPDFState: No saved page found for ${url}, defaulting to page 1`);
    return 1; // Default to page 1
  }

  /**
   * Set the current page number for a specific PDF URL
   */
  setCurrentPage(url: string, pageNumber: number): void {
    if (pageNumber >= 1 && pageNumber <= this.totalPages) {
      // Update in-memory cache
      this._currentPages.set(url, pageNumber);
      
      // Save to localStorage for persistence across sessions
      try {
        const storageKey = `pdf-page-${url}`;
        localStorage.setItem(storageKey, pageNumber.toString());
        console.log(`📖 PersistentPDFState: Saved page ${pageNumber} to localStorage with key ${storageKey}`);
      } catch (error) {
        console.warn("📖 PersistentPDFState: Could not save to localStorage:", error);
      }
      
      console.log(`📖 PersistentPDFState: Saved page ${pageNumber} for ${url}`);
    } else {
      console.warn(`📖 PersistentPDFState: Page ${pageNumber} out of range (1-${this.totalPages}) for ${url}`);
    }
  }

  /**
   * Clear all cached data (for memory management)
   */
  clearCache(): void {
    console.log("📖 PersistentPDFState: Clearing cache");
    
    // Clear localStorage entries for page positions
    try {
      for (const url of this._loadedUrls) {
        const storageKey = `pdf-page-${url}`;
        localStorage.removeItem(storageKey);
      }
    } catch (error) {
      console.warn("📖 PersistentPDFState: Could not clear localStorage:", error);
    }
    
    this._documentInfo = null;
    this._pages = [];
    this._loadingState = {
      isLoading: false,
      progress: 0,
      stage: "",
      error: undefined,
    };
    this._loadedUrls.clear();
    this._currentPages.clear();
  }

  // Getters
  get documentInfo() { return this._documentInfo; }
  get pages() { return this._pages; }
  get loadingState() { return this._loadingState; }
  
  // Computed properties
  get hasPages() { return this._pages.length > 0; }
  get isReady() { return this.hasPages && !this._loadingState.isLoading; }
  get totalPages() { return this._pages.length; }
}

// Create singleton instance
export const persistentPDFState = new PersistentPDFState();
