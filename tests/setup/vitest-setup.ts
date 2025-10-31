import "@testing-library/jest-dom";
import { readFileSync } from "fs";
import { Container } from "inversify";
import { resolve } from "path";
import { afterEach, beforeEach, vi } from "vitest";

// Preload CSV data into window for tests
// This allows CsvLoader to use window.csvData instead of trying to fetch files
const diamondCsvPath = resolve(
  __dirname,
  "../../static/DiamondPictographDataframe.csv"
);
const boxCsvPath = resolve(
  __dirname,
  "../../static/BoxPictographDataframe.csv"
);
const letterMappingsPath = resolve(
  __dirname,
  "../../static/data/learn/letter-mappings.json"
);

try {
  const diamondData = readFileSync(diamondCsvPath, "utf-8");
  const boxData = readFileSync(boxCsvPath, "utf-8");
  const letterMappingsData = readFileSync(letterMappingsPath, "utf-8");

  // Inject CSV data into window for test environment
  (globalThis as any).window = (globalThis as any).window || {};
  (globalThis as any).window.csvData = {
    diamondData,
    boxData,
  };

  // Mock fetch for static files
  const originalFetch = globalThis.fetch;
  globalThis.fetch = vi.fn(
    (url: string | URL | Request, init?: RequestInit) => {
      const urlStr = typeof url === "string" ? url : url.toString();

      // Handle letter-mappings.json
      if (urlStr.includes("letter-mappings.json")) {
        return Promise.resolve(
          new Response(letterMappingsData, {
            status: 200,
            headers: { "Content-Type": "application/json" },
          })
        );
      }

      // Fall back to original fetch for other URLs
      return originalFetch(url, init);
    }
  ) as any;

  console.log("✅ Preloaded CSV data and mocked fetch for tests");
} catch (error) {
  console.warn("⚠️ Failed to preload test data:", error);
}

// Use vi.hoisted to ensure critical modules are imported and initialized BEFORE any service classes
// This prevents "Cannot read properties of undefined" errors with InversifyJS decorators and enums
vi.hoisted(async () => {
  // Import TYPES first to ensure it's available when service decorators execute
  await import("../../src/lib/shared/inversify/types");
  // Import domain enums that are used in module-level object literals
  await import("../../src/lib/shared/pictograph/grid/domain/enums/grid-enums");
  await import(
    "../../src/lib/shared/pictograph/shared/domain/enums/pictograph-enums"
  );
  await import("../../src/lib/shared/foundation/domain/models/LetterType");
  // Import files that use enums in module-level object literals
  await import(
    "../../src/lib/shared/pictograph/shared/domain/constants/pictograph-constants"
  );
  // Import factory functions that are used by services
  await import(
    "../../src/lib/shared/pictograph/shared/domain/factories/createPictographData"
  );
});

// Global Inversify container for tests
let testContainer: Container;

// Mock browser APIs BEFORE any imports that might use them
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: query === "(pointer: fine)" ? true : false, // Return true for pointer: fine
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Global test setup
beforeEach(async () => {
  // Initialize a fresh Inversify container for each test
  try {
    testContainer = new Container();
    // Note: Services will need to be registered manually in individual tests
    // as they require the new Inversify configuration
  } catch (error) {
    console.warn(
      "Failed to initialize Inversify container in test setup:",
      error
    );
  }

  // Ensure CSV data is available in window for tests
  if (typeof window !== "undefined" && !window.csvData) {
    const diamondData = readFileSync(diamondCsvPath, "utf-8");
    const boxData = readFileSync(boxCsvPath, "utf-8");
    (window as any).csvData = {
      diamondData,
      boxData,
    };
  }
});

afterEach(() => {
  // Clean up the container after each test
  if (testContainer) {
    testContainer.unbindAll();
  }
});

// Mock $app/stores for SvelteKit
vi.mock("$app/stores", () => ({
  page: {
    subscribe: vi.fn(),
  },
  navigating: {
    subscribe: vi.fn(),
  },
  updated: {
    subscribe: vi.fn(),
  },
}));

// Mock $app/environment
vi.mock("$app/environment", () => ({
  browser: false,
  dev: true,
  building: false,
  version: "test",
}));

// Mock SequenceData to avoid loading the entire module graph
vi.mock("../../src/lib/shared/foundation/domain/models/SequenceData", () => ({
  // Export a minimal SequenceData interface for testing
  // This prevents loading BeatData from $build/workbench and types from $shared
}));
