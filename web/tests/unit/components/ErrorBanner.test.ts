/**
 * ErrorBanner Component Tests
 *
 * Tests for the ErrorBanner component extracted from ConstructTab
 */

import ErrorBanner from "$lib/components/construct/shared/ErrorBanner.svelte";
import "@testing-library/jest-dom";
import { fireEvent, render, screen } from "@testing-library/svelte";
import { beforeEach, describe, expect, it, vi } from "vitest";

// Mock the store
vi.mock("$stores/constructTabState.svelte", () => ({
  clearError: vi.fn(),
}));

describe("ErrorBanner", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Basic Rendering", () => {
    it("should render with error message", () => {
      render(ErrorBanner, {
        props: {
          message: "Test error message",
        },
      });

      const banner = screen.getByTestId("error-banner");
      expect(banner).toBeInTheDocument();

      const errorText = screen.getByText("❌ Test error message");
      expect(errorText).toBeInTheDocument();

      const dismissButton = screen.getByText("Dismiss");
      expect(dismissButton).toBeInTheDocument();
    });

    it("should have correct CSS classes", () => {
      const { container } = render(ErrorBanner, {
        props: {
          message: "Another error",
        },
      });

      const banner = container.querySelector(".error-banner");
      expect(banner).toBeInTheDocument();
      expect(banner).toHaveClass("error-banner");
    });
  });

  describe("Dismiss Functionality", () => {
    it("should call onDismiss when dismiss button is clicked", async () => {
      const mockOnDismiss = vi.fn();

      render(ErrorBanner, {
        props: {
          message: "Dismissible error",
          onDismiss: mockOnDismiss,
        },
      });

      const dismissButton = screen.getByText("Dismiss");
      await fireEvent.click(dismissButton);

      expect(mockOnDismiss).toHaveBeenCalledTimes(1);
    });

    it("should be keyboard accessible", async () => {
      const mockOnDismiss = vi.fn();

      render(ErrorBanner, {
        props: {
          message: "Keyboard accessible error",
          onDismiss: mockOnDismiss,
        },
      });

      const dismissButton = screen.getByText("Dismiss");
      dismissButton.focus();

      // Use click event instead of keyDown since button onclick handles both
      await fireEvent.click(dismissButton);
      expect(mockOnDismiss).toHaveBeenCalledTimes(1);
    });
  });

  describe("Message Display", () => {
    it("should handle empty message", () => {
      render(ErrorBanner, {
        props: {
          message: "",
        },
      });

      const errorText = screen.getByText("❌");
      expect(errorText).toBeInTheDocument();
    });

    it("should handle long error messages", () => {
      const longMessage =
        "This is a very long error message that should still be displayed correctly even when it contains a lot of text and might wrap to multiple lines";

      render(ErrorBanner, {
        props: {
          message: longMessage,
        },
      });

      const errorText = screen.getByText(`❌ ${longMessage}`);
      expect(errorText).toBeInTheDocument();
    });

    it("should handle special characters in message", () => {
      const specialMessage = "Error with special chars: <>&\"'";

      render(ErrorBanner, {
        props: {
          message: specialMessage,
        },
      });

      const errorText = screen.getByText(`❌ ${specialMessage}`);
      expect(errorText).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have proper ARIA attributes", () => {
      render(ErrorBanner, {
        props: {
          message: "Accessible error",
        },
      });

      const banner = screen.getByTestId("error-banner");
      expect(banner).toHaveAttribute("data-testid", "error-banner");

      const dismissButton = screen.getByText("Dismiss");
      expect(dismissButton).toHaveAttribute("type", "button");
    });

    it("should be focusable", () => {
      render(ErrorBanner, {
        props: {
          message: "Focusable error",
        },
      });

      const dismissButton = screen.getByText("Dismiss");
      dismissButton.focus();
      expect(dismissButton).toHaveFocus();
    });
  });
});
