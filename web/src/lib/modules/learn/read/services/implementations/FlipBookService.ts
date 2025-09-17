/**
 * FlipBook Service Implementation
 *
 * Service for managing StPageFlip flipbook instances.
 */

import { injectable } from "inversify";
import { PageFlip, type FlipEvent } from "page-flip";
import type { FlipBookConfig, PDFPageData } from "../../domain";
import type { IFlipBookService } from "../contracts";

@injectable()
export class FlipBookService implements IFlipBookService {
  private pageFlip: PageFlip | null = null;
  private container: HTMLElement | null = null;
  private pageChangeCallback: ((pageNumber: number) => void) | null = null;

  async initialize(container: HTMLElement, config: FlipBookConfig): Promise<void> {
    try {
      console.log("📚 FlipBookService: Initializing flipbook", config);

      this.container = container;

      // Create the PageFlip instance
      this.pageFlip = new PageFlip(container, {
        width: config.width,
        height: config.height,
        showCover: config.showCover,
        drawShadow: config.drawShadow,
        flippingTime: config.flippingTime,
        maxShadowOpacity: config.maxShadowOpacity,
        mobileScrollSupport: config.mobileScrollSupport,
        size: "stretch", // Use stretch to fit container properly
        autoSize: true, // Let the book control its own size
        usePortrait: false, // Use landscape mode to show both pages
      });

      // Set up event listeners
      this.pageFlip.on("flip", (e: FlipEvent) => {
        const currentPage = e.data + 1; // Convert from 0-based to 1-based
        console.log("📚 FlipBookService: Page changed to", currentPage);
        this.pageChangeCallback?.(currentPage);
      });

      console.log("📚 FlipBookService: Flipbook initialized successfully");
    } catch (error) {
      console.error("📚 FlipBookService: Error initializing flipbook", error);
      throw new Error(`Failed to initialize flipbook: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  async loadPages(pages: PDFPageData[]): Promise<void> {
    if (!this.pageFlip) {
      throw new Error("Flipbook not initialized");
    }

    try {
      console.log(`📚 FlipBookService: Loading ${pages.length} pages into flipbook`);

      // Convert page data to image URLs for StPageFlip
      const imageUrls = pages.map(page => page.imageDataUrl);

      // Load images into the flipbook
      this.pageFlip.loadFromImages(imageUrls);

      console.log("📚 FlipBookService: Pages loaded successfully");
    } catch (error) {
      console.error("📚 FlipBookService: Error loading pages", error);
      throw new Error(`Failed to load pages: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  goToPage(pageNumber: number): void {
    if (!this.pageFlip) {
      throw new Error("Flipbook not initialized");
    }

    // Convert from 1-based to 0-based indexing
    const pageIndex = pageNumber - 1;
    this.pageFlip.turnToPage(pageIndex);
    console.log("📚 FlipBookService: Navigated to page", pageNumber);
  }

  nextPage(): void {
    if (!this.pageFlip) {
      throw new Error("Flipbook not initialized");
    }

    this.pageFlip.flipNext("bottom");
    console.log("📚 FlipBookService: Flipped to next page");
  }

  previousPage(): void {
    if (!this.pageFlip) {
      throw new Error("Flipbook not initialized");
    }

    this.pageFlip.flipPrev("top");
    console.log("📚 FlipBookService: Flipped to previous page");
  }

  getCurrentPage(): number {
    if (!this.pageFlip) {
      return 1;
    }

    // Convert from 0-based to 1-based indexing
    return this.pageFlip.getCurrentPageIndex() + 1;
  }

  getTotalPages(): number {
    if (!this.pageFlip) {
      return 0;
    }

    return this.pageFlip.getPageCount();
  }

  onPageChange(callback: (pageNumber: number) => void): void {
    this.pageChangeCallback = callback;
  }

  destroy(): void {
    if (this.pageFlip) {
      this.pageFlip.destroy();
      this.pageFlip = null;
    }
    this.container = null;
    this.pageChangeCallback = null;
    console.log("📚 FlipBookService: Flipbook destroyed");
  }
}