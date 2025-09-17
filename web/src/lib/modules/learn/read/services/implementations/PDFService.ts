/**
 * PDF Service Implementation
 *
 * Service for processing PDF documents using PDF.js and converting pages to images.
 * Enhanced with IndexedDB caching to avoid reconversion during hot reloads.
 */

import { injectable } from "inversify";
import type { PDFDocumentProxy, PDFPageProxy } from "pdfjs-dist";
import * as pdfjsLib from "pdfjs-dist";
import type { PDFDocumentInfo, PDFPageData } from "../../domain";
import type { IPDFService } from "../contracts";
import { PDFCacheService } from "./PDFCacheService";

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = "/node_modules/pdfjs-dist/build/pdf.worker.min.mjs";

@injectable()
export class PDFService implements IPDFService {
  private document: PDFDocumentProxy | null = null;
  private documentInfo: PDFDocumentInfo | null = null;
  private cacheService: PDFCacheService = new PDFCacheService();
  private cacheInitialized = false;
  private currentPDFUrl: string | null = null;

  private async ensureCacheInitialized(): Promise<void> {
    if (!this.cacheInitialized) {
      try {
        await this.cacheService.initialize();
        this.cacheInitialized = true;
        console.log("📦 PDFService: Cache service initialized");
      } catch (error) {
        console.warn("📦 PDFService: Cache initialization failed, proceeding without cache:", error);
      }
    }
  }

  private getCurrentPDFUrl(): string {
    return this.currentPDFUrl || "/static/Level 1.pdf"; // fallback to known PDF path
  }

  /**
   * Check if we have fully cached data for a PDF URL
   */
  async hasCachedPDF(url: string): Promise<boolean> {
    await this.ensureCacheInitialized();
    if (!this.cacheInitialized) return false;
    
    const hasCachedPages = await this.cacheService.hasCachedPages(url);
    if (!hasCachedPages) return false;
    
    const cachedMetadata = await this.cacheService.getCachedMetadata(url);
    if (!cachedMetadata) return false;
    
    const cachedPages = await this.cacheService.getCachedPages(url);
    return cachedPages.length === cachedMetadata.numPages;
  }

  async loadPDF(url: string): Promise<PDFDocumentInfo> {
    try {
      console.log("📖 PDFService: Loading PDF from", url);
      await this.ensureCacheInitialized();
      
      // Store the current PDF URL for caching
      this.currentPDFUrl = url;

      // Check if we have cached metadata
      if (this.cacheInitialized) {
        const cachedMetadata = await this.cacheService.getCachedMetadata(url);
        if (cachedMetadata) {
          console.log("📦 PDFService: Using cached metadata");
          this.documentInfo = {
            title: cachedMetadata.title,
            author: cachedMetadata.author,
            numPages: cachedMetadata.numPages,
          };
          
          // Still load the document for page access, but we have the metadata
          const loadingTask = pdfjsLib.getDocument(url);
          this.document = await loadingTask.promise;
          
          return this.documentInfo;
        }
      }

      // Load the PDF document
      const loadingTask = pdfjsLib.getDocument(url);
      this.document = await loadingTask.promise;

      // Extract document metadata
      const metadata = await this.document.getMetadata();
      const info = metadata.info as Record<string, unknown>;

      this.documentInfo = {
        title: (info?.Title as string) || "Level 1 Guide",
        author: (info?.Author as string) || "TKA",
        numPages: this.document.numPages,
      };

      // Cache the metadata
      if (this.cacheInitialized) {
        await this.cacheService.cacheMetadata(
          url,
          this.documentInfo.title || "Level 1 Guide",
          this.documentInfo.author || "TKA",
          this.documentInfo.numPages
        );
      }

      console.log("📖 PDFService: PDF loaded successfully", this.documentInfo);
      return this.documentInfo;
    } catch (error) {
      console.error("📖 PDFService: Error loading PDF", error);
      throw new Error(`Failed to load PDF: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  async convertPagesToImages(
    onProgress?: (progress: number, stage: string) => void
  ): Promise<PDFPageData[]> {
    if (!this.document) {
      throw new Error("No PDF document loaded");
    }

    await this.ensureCacheInitialized();
    const totalPages = this.document.numPages;
    
    // Use a consistent URL for caching - get from document URL or default to known PDF path
    const currentUrl = this.getCurrentPDFUrl();
    
    // Check if we have all pages cached
    if (this.cacheInitialized) {
      const hasCachedPages = await this.cacheService.hasCachedPages(currentUrl);
      
      if (hasCachedPages) {
        console.log("📦 PDFService: Loading all pages from cache");
        
        const cachedPages = await this.cacheService.getCachedPages(currentUrl);
        if (cachedPages.length === totalPages) {
          // Convert cached pages to PDFPageData format
          const pages: PDFPageData[] = cachedPages.map(cached => ({
            pageNumber: cached.pageNumber,
            imageDataUrl: cached.imageDataUrl,
            width: cached.width,
            height: cached.height,
          }));
          
          // For cached pages, report 100% immediately to avoid loading UI flash
          onProgress?.(100, "Cached pages loaded");
          console.log("📦 PDFService: All pages loaded from cache");
          return pages;
        }
      }
    }

    // Convert pages and cache them
    const pages: PDFPageData[] = [];
    console.log(`📖 PDFService: Converting ${totalPages} pages to images`);

    for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
      onProgress?.(
        ((pageNum - 1) / totalPages) * 100,
        `Converting page ${pageNum} of ${totalPages}`
      );

      const pageData = await this.convertPageToImage(pageNum);
      pages.push(pageData);

      // Cache each page as it's converted
      if (this.cacheInitialized) {
        await this.cacheService.cachePage(currentUrl, pageData);
      }
    }

    onProgress?.(100, "Conversion complete");
    console.log("📖 PDFService: All pages converted successfully");
    return pages;
  }

  async convertPageToImage(pageNumber: number, scale: number = 1.2): Promise<PDFPageData> {
    if (!this.document) {
      throw new Error("No PDF document loaded");
    }

    try {
      // Get the page
      const page: PDFPageProxy = await this.document.getPage(pageNumber);
      const viewport = page.getViewport({ scale });

      // Create canvas for rendering
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");
      
      if (!context) {
        throw new Error("Failed to get canvas context");
      }

      canvas.height = viewport.height;
      canvas.width = viewport.width;

      // Render the page
      const renderContext = {
        canvasContext: context,
        viewport: viewport,
        canvas: canvas,
      };

      await page.render(renderContext).promise;

      // Convert to data URL with optimized quality
      const imageDataUrl = canvas.toDataURL("image/jpeg", 0.85);

      return {
        pageNumber,
        imageDataUrl,
        width: viewport.width,
        height: viewport.height,
      };
    } catch (error) {
      console.error(`📖 PDFService: Error converting page ${pageNumber}`, error);
      throw new Error(`Failed to convert page ${pageNumber}: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  getDocumentInfo(): PDFDocumentInfo | null {
    return this.documentInfo;
  }

  async clearCache(url?: string): Promise<void> {
    await this.ensureCacheInitialized();
    if (this.cacheInitialized) {
      if (url) {
        await this.cacheService.clearPDFCache(url);
        console.log("📦 PDFService: Cache cleared for specific PDF");
      } else {
        await this.cacheService.clearExpiredCache();
        console.log("📦 PDFService: Expired cache entries cleared");
      }
    }
  }

  cleanup(): void {
    if (this.document) {
      this.document.destroy();
      this.document = null;
    }
    this.documentInfo = null;
    console.log("📖 PDFService: Cleaned up resources");
  }
}