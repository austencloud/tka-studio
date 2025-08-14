/**
 * ConstructTabState Tests
 *
 * Tests for the centralized state management using Svelte 5 runes
 */

import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  state,
  setActiveRightPanel,
  setError,
  setGridMode,
  updateShouldShowStartPositionPicker,
  getCurrentSequence,
  getHasError,
  getIsInBuildMode,
  clearError,
} from "../constructTabState.svelte";

// Mock the sequence state
vi.mock("../../state/sequenceState.svelte", () => {
  const mockState = {
    currentSequence: null,
  };
  return {
    state: mockState,
    __mockState: mockState, // Export for test manipulation
  };
});

describe("ConstructTabState", () => {
  let mockSequenceState: any;

  beforeEach(async () => {
    // Get the mock state for manipulation
    const sequenceStateMock = await import("../../state/sequenceState.svelte");
    mockSequenceState = (sequenceStateMock as any).__mockState;

    // Reset state to defaults
    state.activeRightPanel = "build";
    state.gridMode = "diamond";
    state.isTransitioning = false;
    state.isSubTabTransitionActive = false;
    state.currentSubTabTransition = null;
    state.errorMessage = null;
    mockSequenceState.currentSequence = null;
  });

  describe("Initial State", () => {
    it("should have correct default values", () => {
      expect(state.activeRightPanel).toBe("build");
      expect(state.gridMode).toBe("diamond");
      expect(state.isTransitioning).toBe(false);
      expect(state.isSubTabTransitionActive).toBe(false);
      expect(state.currentSubTabTransition).toBe(null);
      expect(state.errorMessage).toBe(null);
    });

    it("should show start position picker when no sequence", () => {
      mockSequenceState.currentSequence = null;
      updateShouldShowStartPositionPicker();
      expect(state.shouldShowStartPositionPicker).toBe(true);
    });

    it("should show start position picker when sequence has no start position", () => {
      mockSequenceState.currentSequence = {
        id: "test",
        name: "Test Sequence",
        word: "test",
        beats: [{ beat_number: 1 }],
        thumbnails: [],
        is_favorite: false,
        is_circular: false,
        tags: [],
        metadata: {},
      } as any;
      updateShouldShowStartPositionPicker();
      expect(state.shouldShowStartPositionPicker).toBe(true);
    });

    it("should not show start position picker when sequence has start position", () => {
      mockSequenceState.currentSequence = {
        id: "test",
        name: "Test Sequence",
        word: "test",
        beats: [{ beat_number: 1 }],
        start_position: { endPos: "alpha1" },
        thumbnails: [],
        is_favorite: false,
        is_circular: false,
        tags: [],
        metadata: {},
      } as any;
      updateShouldShowStartPositionPicker();
      expect(state.shouldShowStartPositionPicker).toBe(false);
    });
  });

  describe("State Management Functions", () => {
    it("should update active right panel", () => {
      setActiveRightPanel("generate");
      expect(state.activeRightPanel).toBe("generate");

      setActiveRightPanel("edit");
      expect(state.activeRightPanel).toBe("edit");

      setActiveRightPanel("export");
      expect(state.activeRightPanel).toBe("export");
    });

    it("should update grid mode", () => {
      setGridMode("box");
      expect(state.gridMode).toBe("box");

      setGridMode("diamond");
      expect(state.gridMode).toBe("diamond");
    });

    it("should update error message", () => {
      setError("Test error");
      expect(state.errorMessage).toBe("Test error");
      expect(getHasError()).toBe(true);

      clearError();
      expect(state.errorMessage).toBe(null);
      expect(getHasError()).toBe(false);
    });
  });

  describe("Derived State Getters", () => {
    it("should return current sequence", () => {
      const testSequence = {
        id: "test",
        name: "Test Sequence",
        word: "test",
        beats: [],
        thumbnails: [],
        is_favorite: false,
        is_circular: false,
        tags: [],
        metadata: {},
      } as any;
      mockSequenceState.currentSequence = testSequence;
      expect(getCurrentSequence()).toBe(testSequence);
    });

    it("should return hasError correctly", () => {
      expect(getHasError()).toBe(false);

      setError("Some error");
      expect(getHasError()).toBe(true);

      clearError();
      expect(getHasError()).toBe(false);
    });

    it("should return mode checks correctly", () => {
      expect(getIsInBuildMode()).toBe(true);

      setActiveRightPanel("generate");
      expect(getIsInBuildMode()).toBe(false);

      setActiveRightPanel("build");
      expect(getIsInBuildMode()).toBe(true);
    });
  });
});
