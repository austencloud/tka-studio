/**
 * PDF Cache Service
 * 
 * Provides browser-persistent caching for converted PDF pages using IndexedDB.
 * This significantly improves performance by avoiding page reconversion during hot reloads.
 */

interface CachedPageData {
  pageNumber: number;
  imageDataUrl: string;
  width: number;
  height: number;
  timestamp: number;
  pdfHash: string;
}

interface CachedPDFMetadata {
  title: string;
  author: string;
  numPages: number;
  pdfHash: string;
  timestamp: number;
}

export class PDFCacheService {
  private readonly DB_NAME = "tka-pdf-cache";
  private readonly DB_VERSION = 1;
  private readonly PAGES_STORE = "pages";
  private readonly METADATA_STORE = "metadata";
  private readonly CACHE_DURATION_MS = 24 * 60 * 60 * 1000; // 24 hours
  
  private db: IDBDatabase | null = null;

  /**
   * Initialize the IndexedDB database
   */
  async initialize(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.DB_NAME, this.DB_VERSION);

      request.onerror = () => {
        console.error("PDFCacheService: Failed to open database");
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log("📦 PDFCacheService: Database initialized");
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Create pages store
        if (!db.objectStoreNames.contains(this.PAGES_STORE)) {
          const pagesStore = db.createObjectStore(this.PAGES_STORE, { keyPath: "id" });
          pagesStore.createIndex("pdfHash", "pdfHash", { unique: false });
          pagesStore.createIndex("pageNumber", "pageNumber", { unique: false });
        }

        // Create metadata store
        if (!db.objectStoreNames.contains(this.METADATA_STORE)) {
          db.createObjectStore(this.METADATA_STORE, { keyPath: "pdfHash" });
        }

        console.log("📦 PDFCacheService: Database schema created");
      };
    });
  }

  /**
   * Generate a hash for the PDF URL to use as cache key
   */
  private generatePDFHash(url: string): string {
    // Simple hash function for URL
    let hash = 0;
    for (let i = 0; i < url.length; i++) {
      const char = url.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16);
  }

  /**
   * Check if cached pages exist for a PDF
   */
  async hasCachedPages(url: string): Promise<boolean> {
    if (!this.db) return false;

    const pdfHash = this.generatePDFHash(url);
    
    return new Promise((resolve) => {
      const transaction = this.db!.transaction([this.METADATA_STORE], "readonly");
      const store = transaction.objectStore(this.METADATA_STORE);
      const request = store.get(pdfHash);

      request.onsuccess = () => {
        const metadata = request.result as CachedPDFMetadata | undefined;
        if (!metadata) {
          resolve(false);
          return;
        }

        // Check if cache is still valid
        const isValid = Date.now() - metadata.timestamp < this.CACHE_DURATION_MS;
        resolve(isValid);
      };

      request.onerror = () => resolve(false);
    });
  }

  /**
   * Get cached PDF metadata
   */
  async getCachedMetadata(url: string): Promise<CachedPDFMetadata | null> {
    if (!this.db) return null;

    const pdfHash = this.generatePDFHash(url);
    
    return new Promise((resolve) => {
      const transaction = this.db!.transaction([this.METADATA_STORE], "readonly");
      const store = transaction.objectStore(this.METADATA_STORE);
      const request = store.get(pdfHash);

      request.onsuccess = () => {
        const metadata = request.result as CachedPDFMetadata | undefined;
        resolve(metadata || null);
      };

      request.onerror = () => resolve(null);
    });
  }

  /**
   * Get cached pages for a PDF
   */
  async getCachedPages(url: string): Promise<CachedPageData[]> {
    if (!this.db) return [];

    const pdfHash = this.generatePDFHash(url);
    
    return new Promise((resolve) => {
      const transaction = this.db!.transaction([this.PAGES_STORE], "readonly");
      const store = transaction.objectStore(this.PAGES_STORE);
      const index = store.index("pdfHash");
      const request = index.getAll(pdfHash);

      request.onsuccess = () => {
        const pages = request.result as CachedPageData[];
        // Sort by page number
        pages.sort((a, b) => a.pageNumber - b.pageNumber);
        resolve(pages);
      };

      request.onerror = () => resolve([]);
    });
  }

  /**
   * Cache PDF metadata
   */
  async cacheMetadata(url: string, title: string, author: string, numPages: number): Promise<void> {
    if (!this.db) return;

    const pdfHash = this.generatePDFHash(url);
    const metadata: CachedPDFMetadata = {
      title,
      author,
      numPages,
      pdfHash,
      timestamp: Date.now(),
    };

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.METADATA_STORE], "readwrite");
      const store = transaction.objectStore(this.METADATA_STORE);
      const request = store.put(metadata);

      request.onsuccess = () => {
        console.log(`📦 PDFCacheService: Cached metadata for ${url}`);
        resolve();
      };

      request.onerror = () => {
        console.error("PDFCacheService: Failed to cache metadata");
        reject(request.error);
      };
    });
  }

  /**
   * Cache a single page
   */
  async cachePage(url: string, pageData: { pageNumber: number; imageDataUrl: string; width: number; height: number }): Promise<void> {
    if (!this.db) return;

    const pdfHash = this.generatePDFHash(url);
    const cachedPage: CachedPageData = {
      ...pageData,
      pdfHash,
      timestamp: Date.now(),
    };

    // Add unique ID for the page
    const pageId = `${pdfHash}-${pageData.pageNumber}`;
    const pageWithId = { ...cachedPage, id: pageId };

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.PAGES_STORE], "readwrite");
      const store = transaction.objectStore(this.PAGES_STORE);
      const request = store.put(pageWithId);

      request.onsuccess = () => {
        resolve();
      };

      request.onerror = () => {
        console.error(`PDFCacheService: Failed to cache page ${pageData.pageNumber}`);
        reject(request.error);
      };
    });
  }

  /**
   * Clear cache for a specific PDF
   */
  async clearPDFCache(url: string): Promise<void> {
    if (!this.db) return;

    const pdfHash = this.generatePDFHash(url);

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.PAGES_STORE, this.METADATA_STORE], "readwrite");
      
      // Clear pages
      const pagesStore = transaction.objectStore(this.PAGES_STORE);
      const pagesIndex = pagesStore.index("pdfHash");
      const pagesRequest = pagesIndex.openCursor(IDBKeyRange.only(pdfHash));
      
      pagesRequest.onsuccess = (event: Event) => {
        const cursor = (event.target as IDBRequest).result;
        if (cursor) {
          cursor.delete();
          cursor.continue();
        }
      };

      // Clear metadata
      const metadataStore = transaction.objectStore(this.METADATA_STORE);
      metadataStore.delete(pdfHash);

      transaction.oncomplete = () => {
        console.log(`📦 PDFCacheService: Cleared cache for ${url}`);
        resolve();
      };

      transaction.onerror = () => {
        console.error("PDFCacheService: Failed to clear cache");
        reject(transaction.error);
      };
    });
  }

  /**
   * Clear all expired cache entries
   */
  async clearExpiredCache(): Promise<void> {
    if (!this.db) return;

    const cutoffTime = Date.now() - this.CACHE_DURATION_MS;

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.PAGES_STORE, this.METADATA_STORE], "readwrite");

      // Clear expired pages
      const pagesStore = transaction.objectStore(this.PAGES_STORE);
      const pagesRequest = pagesStore.openCursor();
      
      pagesRequest.onsuccess = (event: Event) => {
        const cursor = (event.target as IDBRequest).result;
        if (cursor) {
          const page = cursor.value as CachedPageData;
          if (page.timestamp < cutoffTime) {
            cursor.delete();
          }
          cursor.continue();
        }
      };

      // Clear expired metadata
      const metadataStore = transaction.objectStore(this.METADATA_STORE);
      const metadataRequest = metadataStore.openCursor();
      
      metadataRequest.onsuccess = (event: Event) => {
        const cursor = (event.target as IDBRequest).result;
        if (cursor) {
          const metadata = cursor.value as CachedPDFMetadata;
          if (metadata.timestamp < cutoffTime) {
            cursor.delete();
          }
          cursor.continue();
        }
      };

      transaction.oncomplete = () => {
        console.log("📦 PDFCacheService: Cleared expired cache entries");
        resolve();
      };

      transaction.onerror = () => {
        console.error("PDFCacheService: Failed to clear expired cache");
        reject(transaction.error);
      };
    });
  }
}
