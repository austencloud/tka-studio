import type { PictographData } from "$lib/domain/PictographData";
import { fireEvent, render, screen } from "@testing-library/svelte";
import { beforeEach, describe, expect, it, vi } from "vitest";
import OptionPickerSection from "../OptionPickerSection.svelte";

// Mock ModernPictograph component
vi.mock("$lib/components/pictograph/ModernPictograph.svelte", () => ({
  default: vi.fn(() => ({
    $$: { fragment: null },
    $set: vi.fn(),
    $destroy: vi.fn(),
  })),
}));

describe("OptionPickerSection", () => {
  const mockPictographs: PictographData[] = [
    {
      id: "test-1",
      letter: "A",
      end_position: "beta1",
      grid_data: {
        grid_mode: "diamond",
        center_x: 475,
        center_y: 475,
        radius: 400,
        grid_points: {},
      },
      arrows: {},
      props: {},
      motions: {},
      beat: 1,
      is_blank: false,
      is_mirrored: false,
      metadata: {},
    } as PictographData,
    {
      id: "test-2",
      letter: "B",
      end_position: "beta2",
      grid_data: {
        grid_mode: "diamond",
        center_x: 475,
        center_y: 475,
        radius: 400,
        grid_points: {},
      },
      arrows: {},
      props: {},
      motions: {},
      beat: 1,
      is_blank: false,
      is_mirrored: false,
      metadata: {},
    } as PictographData,
  ];

  const defaultProps = {
    letterType: "Type1",
    pictographs: mockPictographs,
    onPictographSelected: vi.fn(),
    containerWidth: 800,
    isExpanded: true,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Basic Rendering", () => {
    it("should render section with correct letter type", () => {
      render(OptionPickerSection, { props: defaultProps });

      // Should render the section
      const section = screen.getByRole("region", { name: /Type1/i });
      expect(section).toBeInTheDocument();
    });

    it("should render pictographs when expanded", () => {
      render(OptionPickerSection, { props: defaultProps });

      // Should render pictograph containers (excluding the header toggle button)
      const pictographContainers =
        screen.getAllByLabelText(/Select .* pictograph/);
      expect(pictographContainers).toHaveLength(2);
    });

    it("should not render pictographs when collapsed", () => {
      render(OptionPickerSection, {
        props: { ...defaultProps, isExpanded: false },
      });

      // Should not render pictograph containers when collapsed (but header button should still be there)
      const pictographContainers =
        screen.queryAllByLabelText(/Select .* pictograph/);
      expect(pictographContainers).toHaveLength(0);

      // Header toggle button should still be present
      const toggleButton = screen.getByRole("button", {
        name: /Type1: Dual-Shift/i,
      });
      expect(toggleButton).toBeInTheDocument();
    });
  });

  describe("Layout Configuration", () => {
    it("should calculate layout based on container width", () => {
      render(OptionPickerSection, {
        props: { ...defaultProps, containerWidth: 400 },
      });

      // Should render with appropriate grid layout
      const section = screen.getByRole("region");
      expect(section).toBeInTheDocument();
    });

    it("should handle different container sizes", () => {
      render(OptionPickerSection, {
        props: { ...defaultProps, containerWidth: 1200 },
      });

      // Should render with appropriate grid layout for larger container
      const section = screen.getByRole("region");
      expect(section).toBeInTheDocument();
    });
  });

  describe("Pictograph Selection", () => {
    it("should call onPictographSelected when pictograph is clicked", async () => {
      const mockOnSelect = vi.fn();
      render(OptionPickerSection, {
        props: { ...defaultProps, onPictographSelected: mockOnSelect },
      });

      const pictographButtons =
        screen.getAllByLabelText(/Select .* pictograph/);
      if (pictographButtons[0]) {
        await pictographButtons[0].click();
      }

      expect(mockOnSelect).toHaveBeenCalledWith(mockPictographs[0]);
    });

    it("should handle keyboard selection", async () => {
      const mockOnSelect = vi.fn();
      render(OptionPickerSection, {
        props: { ...defaultProps, onPictographSelected: mockOnSelect },
      });

      const pictographButtons =
        screen.getAllByLabelText(/Select .* pictograph/);
      if (pictographButtons[0]) {
        pictographButtons[0].focus();
        // Use fireEvent for better compatibility with Svelte event handlers
        await fireEvent.keyDown(pictographButtons[0], { key: "Enter" });
      }

      expect(mockOnSelect).toHaveBeenCalledWith(mockPictographs[0]);
    });
  });

  describe("Empty State", () => {
    it("should show empty message when no pictographs provided", () => {
      render(OptionPickerSection, {
        props: { ...defaultProps, pictographs: [] },
      });

      expect(
        screen.getByText(/No options available for this type/i)
      ).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have proper ARIA attributes", () => {
      render(OptionPickerSection, { props: defaultProps });

      // Check that pictograph containers have proper accessibility attributes
      const pictographButtons =
        screen.getAllByLabelText(/Select .* pictograph/);
      pictographButtons.forEach((button) => {
        expect(button).toHaveAttribute("tabindex", "0");
        expect(button).toHaveAttribute("role", "button");
        expect(button).toHaveAttribute("aria-label");
      });

      // Check that the section has proper region role
      const section = screen.getByRole("region");
      expect(section).toHaveAttribute("aria-label");
    });
  });
});
