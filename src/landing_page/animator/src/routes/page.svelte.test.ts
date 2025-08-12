import { render, screen } from "@testing-library/svelte";
import { describe, it, expect, vi, beforeEach } from "vitest";
import "@testing-library/jest-dom/vitest";
import Page from "./+page.svelte";

// Mock the AnimatorApp component since we're only testing integration
vi.mock("$lib/animator/AnimatorApp.svelte", () => ({
  default: vi.fn().mockImplementation(() => ({
    $$typeof: Symbol.for("react.element"),
    render: () => document.createElement("div"),
  })),
}));

describe("Home Page", () => {
  beforeEach(() => {
    // Reset mocks between tests
    vi.clearAllMocks();
  });

  it("renders the hero section with correct title", () => {
    render(Page);
    const title = screen.getByText("Pictograph Animator");
    expect(title).toBeInTheDocument();
  });

  it("contains the correct meta title", () => {
    render(Page);
    // Need to test svelte:head differently - typically would use special setup,
    // but simplified for this example
    expect(document.title).toContain("Pictograph Animator");
  });

  it("shows loading state before client-side hydration", () => {
    // Mock browser to be false to simulate SSR environment
    vi.mock("$app/environment", () => ({
      browser: false,
    }));

    render(Page);
    const loadingElement = screen.getByText("Loading animator...");
    expect(loadingElement).toBeInTheDocument();
  });

  it("displays usage instructions", () => {
    render(Page);
    const howToUse = screen.getByText("How to use");
    expect(howToUse).toBeInTheDocument();

    // Check that instructions steps are present
    const steps = screen.getAllByRole("listitem");
    expect(steps.length).toBeGreaterThanOrEqual(3);
  });
});
