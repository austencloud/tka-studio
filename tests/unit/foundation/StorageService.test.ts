/**
 * StorageService Tests
 *
 * Comprehensive test suite for the StorageService.
 * Tests localStorage and sessionStorage wrappers with error handling.
 */

import { StorageService } from "$shared/foundation/services/implementations/StorageService";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

describe("StorageService", () => {
  let service: StorageService;
  let localStorageMock: Storage;
  let sessionStorageMock: Storage;

  beforeEach(() => {
    // Create mock storage objects
    const createMockStorage = (): Storage => {
      let store: Record<string, string> = {};
      return {
        getItem: vi.fn((key: string) => store[key] || null),
        setItem: vi.fn((key: string, value: string) => {
          store[key] = value;
        }),
        removeItem: vi.fn((key: string) => {
          delete store[key];
        }),
        clear: vi.fn(() => {
          store = {};
        }),
        key: vi.fn((index: number) => Object.keys(store)[index] || null),
        get length() {
          return Object.keys(store).length;
        },
      };
    };

    localStorageMock = createMockStorage();
    sessionStorageMock = createMockStorage();

    // Replace global storage objects
    Object.defineProperty(window, "localStorage", {
      value: localStorageMock,
      writable: true,
    });
    Object.defineProperty(window, "sessionStorage", {
      value: sessionStorageMock,
      writable: true,
    });

    service = new StorageService();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  // ============================================================================
  // SESSION STORAGE TESTS
  // ============================================================================

  describe("Session Storage Operations", () => {
    describe("safeSessionStorageGet", () => {
      it("should retrieve and parse valid JSON", () => {
        const testData = { name: "Test", value: 42 };
        sessionStorageMock.setItem("test-key", JSON.stringify(testData));

        const result = service.safeSessionStorageGet("test-key");
        expect(result).toEqual(testData);
      });

      it("should return default value for non-existent key", () => {
        const defaultValue = { default: true };
        const result = service.safeSessionStorageGet(
          "missing-key",
          defaultValue
        );
        expect(result).toEqual(defaultValue);
      });

      it("should return null for non-existent key when no default provided", () => {
        const result = service.safeSessionStorageGet("missing-key");
        expect(result).toBeNull();
      });

      it("should handle undefined string value", () => {
        sessionStorageMock.setItem("test-key", "undefined");
        const result = service.safeSessionStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle null string value", () => {
        sessionStorageMock.setItem("test-key", "null");
        const result = service.safeSessionStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle empty string value", () => {
        sessionStorageMock.setItem("test-key", "");
        const result = service.safeSessionStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle whitespace-only value", () => {
        sessionStorageMock.setItem("test-key", "   ");
        const result = service.safeSessionStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle invalid JSON gracefully", () => {
        sessionStorageMock.setItem("test-key", "{invalid json}");
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});

        const result = service.safeSessionStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });

      it("should handle complex nested objects", () => {
        const complexData = {
          user: { name: "John", age: 30 },
          settings: { theme: "dark", notifications: true },
          array: [1, 2, 3],
        };
        sessionStorageMock.setItem("test-key", JSON.stringify(complexData));

        const result = service.safeSessionStorageGet("test-key");
        expect(result).toEqual(complexData);
      });
    });

    describe("safeSessionStorageSet", () => {
      it("should store simple values", () => {
        service.safeSessionStorageSet("test-key", "test-value");
        expect(sessionStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify("test-value")
        );
      });

      it("should store objects", () => {
        const testData = { name: "Test", value: 42 };
        service.safeSessionStorageSet("test-key", testData);
        expect(sessionStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify(testData)
        );
      });

      it("should store arrays", () => {
        const testArray = [1, 2, 3, 4, 5];
        service.safeSessionStorageSet("test-key", testArray);
        expect(sessionStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify(testArray)
        );
      });

      it("should handle storage errors gracefully", () => {
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});
        vi.spyOn(sessionStorageMock, "setItem").mockImplementation(() => {
          throw new Error("Storage quota exceeded");
        });

        service.safeSessionStorageSet("test-key", "value");
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });
    });

    describe("removeSessionStorageItem", () => {
      it("should remove existing item", () => {
        sessionStorageMock.setItem("test-key", "value");
        service.removeSessionStorageItem("test-key");
        expect(sessionStorageMock.removeItem).toHaveBeenCalledWith("test-key");
      });

      it("should handle removal errors gracefully", () => {
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});
        vi.spyOn(sessionStorageMock, "removeItem").mockImplementation(() => {
          throw new Error("Remove failed");
        });

        service.removeSessionStorageItem("test-key");
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });
    });
  });

  // ============================================================================
  // LOCAL STORAGE TESTS
  // ============================================================================

  describe("Local Storage Operations", () => {
    describe("safeLocalStorageGet", () => {
      it("should retrieve and parse valid JSON", () => {
        const testData = { name: "Test", value: 42 };
        localStorageMock.setItem("test-key", JSON.stringify(testData));

        const result = service.safeLocalStorageGet("test-key");
        expect(result).toEqual(testData);
      });

      it("should return default value for non-existent key", () => {
        const defaultValue = { default: true };
        const result = service.safeLocalStorageGet("missing-key", defaultValue);
        expect(result).toEqual(defaultValue);
      });

      it("should return null for non-existent key when no default provided", () => {
        const result = service.safeLocalStorageGet("missing-key");
        expect(result).toBeNull();
      });

      it("should handle undefined string value", () => {
        localStorageMock.setItem("test-key", "undefined");
        const result = service.safeLocalStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle null string value", () => {
        localStorageMock.setItem("test-key", "null");
        const result = service.safeLocalStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle empty string value", () => {
        localStorageMock.setItem("test-key", "");
        const result = service.safeLocalStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle whitespace-only value", () => {
        localStorageMock.setItem("test-key", "   ");
        const result = service.safeLocalStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
      });

      it("should handle invalid JSON gracefully", () => {
        localStorageMock.setItem("test-key", "{invalid json}");
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});

        const result = service.safeLocalStorageGet("test-key", {
          default: true,
        });
        expect(result).toEqual({ default: true });
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });

      it("should handle complex nested objects", () => {
        const complexData = {
          user: { name: "John", age: 30 },
          settings: { theme: "dark", notifications: true },
          array: [1, 2, 3],
        };
        localStorageMock.setItem("test-key", JSON.stringify(complexData));

        const result = service.safeLocalStorageGet("test-key");
        expect(result).toEqual(complexData);
      });
    });

    describe("safeLocalStorageSet", () => {
      it("should store simple values", () => {
        service.safeLocalStorageSet("test-key", "test-value");
        expect(localStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify("test-value")
        );
      });

      it("should store objects", () => {
        const testData = { name: "Test", value: 42 };
        service.safeLocalStorageSet("test-key", testData);
        expect(localStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify(testData)
        );
      });

      it("should store arrays", () => {
        const testArray = [1, 2, 3, 4, 5];
        service.safeLocalStorageSet("test-key", testArray);
        expect(localStorageMock.setItem).toHaveBeenCalledWith(
          "test-key",
          JSON.stringify(testArray)
        );
      });

      it("should handle storage errors gracefully", () => {
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});
        vi.spyOn(localStorageMock, "setItem").mockImplementation(() => {
          throw new Error("Storage quota exceeded");
        });

        service.safeLocalStorageSet("test-key", "value");
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });
    });

    describe("removeLocalStorageItem", () => {
      it("should remove existing item", () => {
        localStorageMock.setItem("test-key", "value");
        service.removeLocalStorageItem("test-key");
        expect(localStorageMock.removeItem).toHaveBeenCalledWith("test-key");
      });

      it("should handle removal errors gracefully", () => {
        const consoleSpy = vi
          .spyOn(console, "warn")
          .mockImplementation(() => {});
        vi.spyOn(localStorageMock, "removeItem").mockImplementation(() => {
          throw new Error("Remove failed");
        });

        service.removeLocalStorageItem("test-key");
        expect(consoleSpy).toHaveBeenCalled();

        consoleSpy.mockRestore();
      });
    });
  });

  // ============================================================================
  // INTEGRATION TESTS
  // ============================================================================

  describe("Integration Tests", () => {
    it("should handle round-trip storage and retrieval", () => {
      const testData = { name: "Integration Test", value: 123 };

      service.safeLocalStorageSet("integration-key", testData);
      const result = service.safeLocalStorageGet("integration-key");

      expect(result).toEqual(testData);
    });

    it("should handle session and local storage independently", () => {
      const sessionData = { type: "session" };
      const localData = { type: "local" };

      service.safeSessionStorageSet("test-key", sessionData);
      service.safeLocalStorageSet("test-key", localData);

      const sessionResult = service.safeSessionStorageGet("test-key");
      const localResult = service.safeLocalStorageGet("test-key");

      expect(sessionResult).toEqual(sessionData);
      expect(localResult).toEqual(localData);
    });

    it("should handle type-safe storage and retrieval", () => {
      interface TestType {
        id: number;
        name: string;
        active: boolean;
      }

      const testData: TestType = { id: 1, name: "Test", active: true };

      service.safeLocalStorageSet<TestType>("typed-key", testData);
      const result = service.safeLocalStorageGet<TestType>("typed-key");

      expect(result).toEqual(testData);
    });
  });
});
