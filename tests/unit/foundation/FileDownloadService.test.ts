/**
 * FileDownloadService Tests
 *
 * Comprehensive test suite for the FileDownloadService.
 * Tests file download functionality with blob handling and batch downloads.
 */

import { FileDownloadService } from "$shared/foundation/services/implementations/FileDownloadService";
import type { MockInstance } from "vitest";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

describe("FileDownloadService", () => {
  let service: FileDownloadService;
  let mockAnchor: HTMLAnchorElement;
  let createElementSpy: MockInstance;
  let createObjectURLSpy: MockInstance;
  let revokeObjectURLSpy: MockInstance;

  beforeEach(() => {
    service = new FileDownloadService();

    // Create mock anchor element
    mockAnchor = {
      href: "",
      download: "",
      style: { display: "" },
      click: vi.fn(),
    } as unknown as HTMLAnchorElement;

    // Mock document.createElement
    createElementSpy = vi.spyOn(document, "createElement").mockReturnValue(mockAnchor);

    // Mock document.body methods
    vi.spyOn(document.body, "appendChild").mockImplementation(() => mockAnchor);
    vi.spyOn(document.body, "removeChild").mockImplementation(() => mockAnchor);

    // Mock URL methods (jsdom doesn't have these by default)
    if (!URL.createObjectURL) {
      Object.defineProperty(URL, "createObjectURL", {
        writable: true,
        value: vi.fn(),
      });
    }
    if (!URL.revokeObjectURL) {
      Object.defineProperty(URL, "revokeObjectURL", {
        writable: true,
        value: vi.fn(),
      });
    }

    createObjectURLSpy = vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:mock-url");
    revokeObjectURLSpy = vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ============================================================================
  // SINGLE FILE DOWNLOAD TESTS
  // ============================================================================

  describe("downloadBlob", () => {
    it("should download a blob successfully", async () => {
      const blob = new Blob(["test content"], { type: "text/plain" });
      const filename = "test.txt";

      const result = await service.downloadBlob(blob, filename);

      expect(result.success).toBe(true);
      expect(result.filename).toBe(filename);
      expect(createObjectURLSpy).toHaveBeenCalledWith(blob);
      expect(mockAnchor.href).toBe("blob:mock-url");
      expect(mockAnchor.download).toBe(filename);
      expect(mockAnchor.click).toHaveBeenCalled();
      expect(revokeObjectURLSpy).toHaveBeenCalledWith("blob:mock-url");
    });

    it("should set anchor display to none", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      await service.downloadBlob(blob, "test.txt");

      expect(mockAnchor.style.display).toBe("none");
    });

    it("should append and remove anchor from DOM", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      await service.downloadBlob(blob, "test.txt");

      expect(document.body.appendChild).toHaveBeenCalledWith(mockAnchor);
      expect(document.body.removeChild).toHaveBeenCalledWith(mockAnchor);
    });

    it("should handle download errors gracefully", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      const filename = "test.txt";

      // Mock click to throw error
      vi.spyOn(mockAnchor, "click").mockImplementation(() => {
        throw new Error("Download failed");
      });

      const result = await service.downloadBlob(blob, filename);

      expect(result.success).toBe(false);
      expect(result.filename).toBe(filename);
      expect(result.error).toBeInstanceOf(Error);
      expect(result.error?.message).toBe("Download failed");
    });

    it("should handle different blob types", async () => {
      const testCases = [
        { content: "text content", type: "text/plain", filename: "test.txt" },
        { content: '{"key":"value"}', type: "application/json", filename: "data.json" },
        { content: "<html></html>", type: "text/html", filename: "page.html" },
      ];

      for (const testCase of testCases) {
        const blob = new Blob([testCase.content], { type: testCase.type });
        const result = await service.downloadBlob(blob, testCase.filename);

        expect(result.success).toBe(true);
        expect(result.filename).toBe(testCase.filename);
      }
    });

    it("should handle empty blobs", async () => {
      const blob = new Blob([], { type: "text/plain" });
      const result = await service.downloadBlob(blob, "empty.txt");

      expect(result.success).toBe(true);
    });

    it("should handle large filenames", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      const longFilename = "a".repeat(255) + ".txt";

      const result = await service.downloadBlob(blob, longFilename);

      expect(result.success).toBe(true);
      expect(result.filename).toBe(longFilename);
    });

    it("should handle special characters in filename", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      const specialFilename = "test-file_2024 (1).txt";

      const result = await service.downloadBlob(blob, specialFilename);

      expect(result.success).toBe(true);
      expect(result.filename).toBe(specialFilename);
    });
  });

  // ============================================================================
  // BATCH DOWNLOAD TESTS
  // ============================================================================

  describe("downloadBlobBatch", () => {
    it("should download multiple blobs successfully", async () => {
      const blobs = [
        { blob: new Blob(["content 1"], { type: "text/plain" }), filename: "file1.txt" },
        { blob: new Blob(["content 2"], { type: "text/plain" }), filename: "file2.txt" },
        { blob: new Blob(["content 3"], { type: "text/plain" }), filename: "file3.txt" },
      ];

      const results = await service.downloadBlobBatch(blobs, { delay: 0 });

      expect(results).toHaveLength(3);
      expect(results.every((r) => r.success)).toBe(true);
      expect(results[0].filename).toBe("file1.txt");
      expect(results[1].filename).toBe("file2.txt");
      expect(results[2].filename).toBe("file3.txt");
    });

    it("should apply delay between downloads", async () => {
      const blobs = [
        { blob: new Blob(["1"], { type: "text/plain" }), filename: "file1.txt" },
        { blob: new Blob(["2"], { type: "text/plain" }), filename: "file2.txt" },
      ];

      const startTime = Date.now();
      await service.downloadBlobBatch(blobs, { delay: 100 });
      const endTime = Date.now();

      // Should take at least 100ms (one delay between two files)
      expect(endTime - startTime).toBeGreaterThanOrEqual(90); // Allow some margin
    });

    it("should use default delay of 100ms when not specified", async () => {
      const blobs = [
        { blob: new Blob(["1"], { type: "text/plain" }), filename: "file1.txt" },
        { blob: new Blob(["2"], { type: "text/plain" }), filename: "file2.txt" },
      ];

      const startTime = Date.now();
      await service.downloadBlobBatch(blobs);
      const endTime = Date.now();

      expect(endTime - startTime).toBeGreaterThanOrEqual(90);
    });

    it("should not delay after last download", async () => {
      const blobs = [
        { blob: new Blob(["1"], { type: "text/plain" }), filename: "file1.txt" },
      ];

      const startTime = Date.now();
      await service.downloadBlobBatch(blobs, { delay: 1000 });
      const endTime = Date.now();

      // Should complete quickly since there's only one file
      expect(endTime - startTime).toBeLessThan(500);
    });

    it("should handle empty batch", async () => {
      const results = await service.downloadBlobBatch([]);
      expect(results).toHaveLength(0);
    });

    it("should continue batch download even if one fails", async () => {
      const blobs = [
        { blob: new Blob(["1"], { type: "text/plain" }), filename: "file1.txt" },
        { blob: new Blob(["2"], { type: "text/plain" }), filename: "file2.txt" },
        { blob: new Blob(["3"], { type: "text/plain" }), filename: "file3.txt" },
      ];

      // Make the second download fail
      let callCount = 0;
      vi.spyOn(mockAnchor, "click").mockImplementation(() => {
        callCount++;
        if (callCount === 2) {
          throw new Error("Download failed");
        }
      });

      const results = await service.downloadBlobBatch(blobs, { delay: 0 });

      expect(results).toHaveLength(3);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(false);
      expect(results[2].success).toBe(true);
    });

    it("should handle zero delay", async () => {
      const blobs = [
        { blob: new Blob(["1"], { type: "text/plain" }), filename: "file1.txt" },
        { blob: new Blob(["2"], { type: "text/plain" }), filename: "file2.txt" },
      ];

      const results = await service.downloadBlobBatch(blobs, { delay: 0 });

      expect(results).toHaveLength(2);
      expect(results.every((r) => r.success)).toBe(true);
    });
  });

  // ============================================================================
  // INTEGRATION TESTS
  // ============================================================================

  describe("Integration Tests", () => {
    it("should handle mixed content types in batch", async () => {
      const blobs = [
        { blob: new Blob(["text"], { type: "text/plain" }), filename: "text.txt" },
        { blob: new Blob(['{"key":"value"}'], { type: "application/json" }), filename: "data.json" },
        { blob: new Blob(["<html></html>"], { type: "text/html" }), filename: "page.html" },
      ];

      const results = await service.downloadBlobBatch(blobs, { delay: 0 });

      expect(results).toHaveLength(3);
      expect(results.every((r) => r.success)).toBe(true);
    });

    it("should properly cleanup resources for each download", async () => {
      const blob = new Blob(["test"], { type: "text/plain" });
      await service.downloadBlob(blob, "test.txt");

      expect(document.body.appendChild).toHaveBeenCalled();
      expect(document.body.removeChild).toHaveBeenCalled();
      expect(revokeObjectURLSpy).toHaveBeenCalled();
    });
  });
});
