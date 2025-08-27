import { afterEach, beforeEach, vi } from "vitest";
import { Container } from "inversify";

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
