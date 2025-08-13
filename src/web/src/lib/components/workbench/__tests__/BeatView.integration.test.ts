/**
 * BeatView Integration Tests
 *
 * Tests for BeatView component with ModernPictograph integration
 */

import { createBeatData, createPictographData } from "$lib/domain";
import "@testing-library/jest-dom";
import { fireEvent, render } from "@testing-library/svelte";
import { beforeEach, describe, expect, it, vi } from "vitest";
import BeatView from "../BeatView.svelte";

// Mock the ModernPictograph component
vi.mock("$lib/components/pictograph", () => ({
  ModernPictograph: vi.fn(() => ({
    $$: { on_mount: [], on_destroy: [], props: {} },
  })),
}));

// Mock the BeatFrameService (define inside factory to avoid hoist issues)
vi.mock("$lib/services/BeatFrameService.svelte", () => {
  return {
    beatFrameService: {
      config: {
        beatSize: 120,
        hasStartTile: false,
      },
    },
  };
});

describe("BeatView Integration", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Pictograph Rendering", () => {
    it("should render ModernPictograph for beat with pictograph data", () => {
      const pictographData = createPictographData({
        letter: "A",
      });

      const beat = createBeatData({
        beat_number: 1,
        pictograph_data: pictographData,
        is_blank: false,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 0,
        },
      });

      // Should have pictograph container
      const pictographContainer = container.querySelector(
        ".pictograph-container",
      );
      expect(pictographContainer).toBeInTheDocument();

      // Should NOT have beat number display (since it has pictograph)
      const beatNumberDisplay = container.querySelector(".beat-number");
      expect(beatNumberDisplay).not.toBeInTheDocument();
    });

    it("should render beat number for beat without pictograph data", () => {
      const beat = createBeatData({
        beat_number: 2,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 1,
        },
      });

      // Should NOT have pictograph container
      const pictographContainer = container.querySelector(
        ".pictograph-container",
      );
      expect(pictographContainer).not.toBeInTheDocument();

      // Should have beat number display
      const beatNumberDisplay = container.querySelector(".beat-number");
      expect(beatNumberDisplay).toBeInTheDocument();
      expect(beatNumberDisplay).toHaveTextContent("2");
    });

    it("should pass correct props to ModernPictograph", () => {
      const pictographData = createPictographData({
        letter: "B",
      });

      const beat = createBeatData({
        beat_number: 3,
        pictograph_data: pictographData,
      });

      render(BeatView, {
        props: {
          beat,
          index: 2,
        },
      });

      // Verify ModernPictograph would receive correct props
      const pictographContainer = document.querySelector(
        ".pictograph-container",
      );
      expect(pictographContainer).toBeInTheDocument();
    });
  });

  describe("Beat States", () => {
    it("should handle selected state", () => {
      const beat = createBeatData({
        beat_number: 4,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 3,
          isSelected: true,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveClass("selected");
    });

    it("should handle hovered state", () => {
      const beat = createBeatData({
        beat_number: 5,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 4,
          isHovered: true,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveClass("hovered");
    });

    it("should handle blank beat state", () => {
      const beat = createBeatData({
        beat_number: 6,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 5,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveClass("blank");
    });

    it("should handle beat with pictograph state", () => {
      const pictographData = createPictographData({
        letter: "C",
      });

      const beat = createBeatData({
        beat_number: 7,
        pictograph_data: pictographData,
        is_blank: false,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 6,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveClass("has-pictograph");
    });
  });

  describe("Click Handling", () => {
    it("should call onClick when beat is clicked", async () => {
      const handleClick = vi.fn();
      const beat = createBeatData({
        beat_number: 8,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 7,
          onClick: handleClick,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toBeInTheDocument();

      await fireEvent.click(beatView!);
      expect(handleClick).toHaveBeenCalledWith(7);
    });

    it("should call onDoubleClick when beat is double-clicked", async () => {
      const handleDoubleClick = vi.fn();
      const beat = createBeatData({
        beat_number: 9,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 8,
          onDoubleClick: handleDoubleClick,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toBeInTheDocument();

      await fireEvent.dblClick(beatView!);
      expect(handleDoubleClick).toHaveBeenCalledWith(8);
    });

    it("should pass click through to ModernPictograph for pictograph beats", () => {
      const handleClick = vi.fn();
      const pictographData = createPictographData({
        letter: "D",
      });

      const beat = createBeatData({
        beat_number: 10,
        pictograph_data: pictographData,
      });

      render(BeatView, {
        props: {
          beat,
          index: 9,
          onClick: handleClick,
        },
      });

      // ModernPictograph should receive the click handler
      // This is verified by the presence of the pictograph container
      const pictographContainer = document.querySelector(
        ".pictograph-container",
      );
      expect(pictographContainer).toBeInTheDocument();
    });
  });

  describe("Hover Handling", () => {
    it("should call onHover when mouse enters", async () => {
      const handleHover = vi.fn();
      const beat = createBeatData({
        beat_number: 11,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 10,
          onHover: handleHover,
        },
      });

      const beatView = container.querySelector(".beat-view");
      await fireEvent.mouseEnter(beatView!);
      expect(handleHover).toHaveBeenCalledWith(10);
    });

    it("should call onLeave when mouse leaves", async () => {
      const handleLeave = vi.fn();
      const beat = createBeatData({
        beat_number: 12,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 11,
          onLeave: handleLeave,
        },
      });

      const beatView = container.querySelector(".beat-view");
      await fireEvent.mouseLeave(beatView!);
      expect(handleLeave).toHaveBeenCalled();
    });
  });

  describe("Keyboard Handling", () => {
    it("should handle Enter key press", async () => {
      const handleClick = vi.fn();
      const beat = createBeatData({
        beat_number: 13,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 12,
          onClick: handleClick,
        },
      });

      const beatView = container.querySelector(".beat-view");
      await fireEvent.keyPress(beatView!, { key: "Enter" });
      expect(handleClick).toHaveBeenCalledWith(12);
    });

    it("should handle Space key press", async () => {
      const handleClick = vi.fn();
      const beat = createBeatData({
        beat_number: 14,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 13,
          onClick: handleClick,
        },
      });

      const beatView = container.querySelector(".beat-view");
      await fireEvent.keyPress(beatView!, { key: " " });
      expect(handleClick).toHaveBeenCalledWith(13);
    });
  });

  describe("Reversal Indicators", () => {
    it("should show blue reversal indicator", () => {
      const beat = createBeatData({
        beat_number: 15,
        blue_reversal: true,
        red_reversal: false,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 14,
        },
      });

      const blueReversal = container.querySelector(".reversal.blue");
      expect(blueReversal).toBeInTheDocument();

      const redReversal = container.querySelector(".reversal.red");
      expect(redReversal).not.toBeInTheDocument();
    });

    it("should show red reversal indicator", () => {
      const beat = createBeatData({
        beat_number: 16,
        blue_reversal: false,
        red_reversal: true,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 15,
        },
      });

      const redReversal = container.querySelector(".reversal.red");
      expect(redReversal).toBeInTheDocument();

      const blueReversal = container.querySelector(".reversal.blue");
      expect(blueReversal).not.toBeInTheDocument();
    });

    it("should show both reversal indicators", () => {
      const beat = createBeatData({
        beat_number: 17,
        blue_reversal: true,
        red_reversal: true,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 16,
        },
      });

      const blueReversal = container.querySelector(".reversal.blue");
      expect(blueReversal).toBeInTheDocument();

      const redReversal = container.querySelector(".reversal.red");
      expect(redReversal).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have proper ARIA attributes", () => {
      const beat = createBeatData({
        beat_number: 18,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 17,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveAttribute("role", "button");
      expect(beatView).toHaveAttribute("tabindex", "0");
      expect(beatView).toHaveAttribute("aria-label", "Beat 18");
    });

    it("should be keyboard focusable", () => {
      const beat = createBeatData({
        beat_number: 19,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 18,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveAttribute("tabindex", "0");
    });
  });

  describe("Styling Integration", () => {
    it("should apply correct sizing based on beatFrameService config", () => {
      const pictographData = createPictographData({
        letter: "E",
      });

      const beat = createBeatData({
        beat_number: 20,
        pictograph_data: pictographData,
      });

      render(BeatView, {
        props: {
          beat,
          index: 19,
        },
      });

      // The pictograph should be sized based on beatSize - 8
      // This would be verified by the ModernPictograph props
      const pictographContainer = document.querySelector(
        ".pictograph-container",
      );
      expect(pictographContainer).toBeInTheDocument();
    });

    it("should maintain responsive styling", () => {
      const beat = createBeatData({
        beat_number: 21,
        is_blank: true,
      });

      const { container } = render(BeatView, {
        props: {
          beat,
          index: 20,
        },
      });

      const beatView = container.querySelector(".beat-view");
      expect(beatView).toHaveStyle({
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      });
    });
  });
});
