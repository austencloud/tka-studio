/**
 * Panel Coordination State Tests
 * 
 * Comprehensive test suite verifying panel mutual exclusivity rules:
 * - Only ONE panel can be open at a time
 * - Opening a panel automatically closes all other panels
 * - Panel state is properly reset when closing
 */

import { describe, it, expect, beforeEach } from "vitest";
import { createPanelCoordinationState } from "$lib/modules/create/shared/state/panel-coordination-state.svelte";
import type { PanelCoordinationState } from "$lib/modules/create/shared/state/panel-coordination-state.svelte";

describe("Panel Coordination State - Mutual Exclusivity", () => {
  let panelState: PanelCoordinationState;

  beforeEach(() => {
    panelState = createPanelCoordinationState();
  });

  describe("Initial State", () => {
    it("should have all panels closed initially", () => {
      expect(panelState.isEditPanelOpen).toBe(false);
      expect(panelState.isAnimationPanelOpen).toBe(false);
      expect(panelState.isSharePanelOpen).toBe(false);
      expect(panelState.isFilterPanelOpen).toBe(false);
      expect(panelState.isCAPPanelOpen).toBe(false);
      expect(panelState.isCreationMethodPanelOpen).toBe(false);
    });
  });

  describe("Edit Panel", () => {
    it("should open edit panel", () => {
      const mockBeatData = { id: 1, name: "Test Beat" };
      panelState.openEditPanel(0, mockBeatData);

      expect(panelState.isEditPanelOpen).toBe(true);
      expect(panelState.editPanelBeatIndex).toBe(0);
      expect(panelState.editPanelBeatData).toEqual(mockBeatData);
    });

    it("should close other panels when opening edit panel", () => {
      // Open animation panel first
      panelState.openAnimationPanel();
      expect(panelState.isAnimationPanelOpen).toBe(true);

      // Open edit panel - animation should close
      panelState.openEditPanel(0, { id: 1 });
      expect(panelState.isEditPanelOpen).toBe(true);
      expect(panelState.isAnimationPanelOpen).toBe(false);
    });

    it("should close edit panel properly", () => {
      panelState.openEditPanel(0, { id: 1 });
      panelState.closeEditPanel();

      expect(panelState.isEditPanelOpen).toBe(false);
      expect(panelState.editPanelBeatIndex).toBe(null);
      expect(panelState.editPanelBeatData).toBe(null);
    });
  });

  describe("Batch Edit Panel", () => {
    it("should open batch edit panel", () => {
      const mockBeatsData = [{ id: 1 }, { id: 2 }];
      panelState.openBatchEditPanel(mockBeatsData);

      expect(panelState.isEditPanelOpen).toBe(true);
      expect(panelState.editPanelBeatsData).toEqual(mockBeatsData);
      expect(panelState.editPanelBeatIndex).toBe(null);
    });

    it("should close other panels when opening batch edit", () => {
      panelState.openSharePanel();
      expect(panelState.isSharePanelOpen).toBe(true);

      panelState.openBatchEditPanel([{ id: 1 }]);
      expect(panelState.isEditPanelOpen).toBe(true);
      expect(panelState.isSharePanelOpen).toBe(false);
    });
  });

  describe("Animation Panel", () => {
    it("should open animation panel", () => {
      panelState.openAnimationPanel();
      expect(panelState.isAnimationPanelOpen).toBe(true);
    });

    it("should close other panels when opening animation", () => {
      panelState.openEditPanel(0, { id: 1 });
      panelState.openFilterPanel();
      
      panelState.openAnimationPanel();
      
      expect(panelState.isAnimationPanelOpen).toBe(true);
      expect(panelState.isEditPanelOpen).toBe(false);
      expect(panelState.isFilterPanelOpen).toBe(false);
    });

    it("should close animation panel", () => {
      panelState.openAnimationPanel();
      panelState.closeAnimationPanel();
      
      expect(panelState.isAnimationPanelOpen).toBe(false);
    });
  });

  describe("Share Panel", () => {
    it("should open share panel", () => {
      panelState.openSharePanel();
      expect(panelState.isSharePanelOpen).toBe(true);
    });

    it("should close other panels when opening share", () => {
      panelState.openAnimationPanel();
      panelState.openEditPanel(0, { id: 1 });
      
      panelState.openSharePanel();
      
      expect(panelState.isSharePanelOpen).toBe(true);
      expect(panelState.isAnimationPanelOpen).toBe(false);
      expect(panelState.isEditPanelOpen).toBe(false);
    });

    it("should close share panel", () => {
      panelState.openSharePanel();
      panelState.closeSharePanel();
      
      expect(panelState.isSharePanelOpen).toBe(false);
    });
  });

  describe("Filter Panel", () => {
    it("should open filter panel", () => {
      panelState.openFilterPanel();
      expect(panelState.isFilterPanelOpen).toBe(true);
    });

    it("should close other panels when opening filter", () => {
      panelState.openCAPPanel({}, new Set(), () => {});
      
      panelState.openFilterPanel();
      
      expect(panelState.isFilterPanelOpen).toBe(true);
      expect(panelState.isCAPPanelOpen).toBe(false);
    });

    it("should close filter panel", () => {
      panelState.openFilterPanel();
      panelState.closeFilterPanel();
      
      expect(panelState.isFilterPanelOpen).toBe(false);
    });
  });

  describe("CAP Panel", () => {
    it("should open CAP panel with data", () => {
      const mockType = { name: "test" };
      const mockComponents = new Set(["comp1"]);
      const mockOnChange = () => {};

      panelState.openCAPPanel(mockType, mockComponents, mockOnChange);

      expect(panelState.isCAPPanelOpen).toBe(true);
      expect(panelState.capCurrentType).toEqual(mockType);
      expect(panelState.capSelectedComponents).toEqual(mockComponents);
      expect(panelState.capOnChange).toBe(mockOnChange);
    });

    it("should close other panels when opening CAP", () => {
      panelState.openSharePanel();
      panelState.openFilterPanel();
      
      panelState.openCAPPanel({}, new Set(), () => {});
      
      expect(panelState.isCAPPanelOpen).toBe(true);
      expect(panelState.isSharePanelOpen).toBe(false);
      expect(panelState.isFilterPanelOpen).toBe(false);
    });

    it("should close CAP panel and reset state", () => {
      panelState.openCAPPanel({ name: "test" }, new Set(["comp1"]), () => {});
      panelState.closeCAPPanel();

      expect(panelState.isCAPPanelOpen).toBe(false);
      expect(panelState.capCurrentType).toBe(null);
      expect(panelState.capSelectedComponents).toBe(null);
      expect(panelState.capOnChange).toBe(null);
    });
  });

  describe("Creation Method Panel", () => {
    it("should open creation method panel", () => {
      panelState.openCreationMethodPanel();
      expect(panelState.isCreationMethodPanelOpen).toBe(true);
    });

    it("should close other panels when opening creation method", () => {
      panelState.openAnimationPanel();
      panelState.openCreationMethodPanel();
      
      expect(panelState.isCreationMethodPanelOpen).toBe(true);
      expect(panelState.isAnimationPanelOpen).toBe(false);
    });

    it("should close creation method panel", () => {
      panelState.openCreationMethodPanel();
      panelState.closeCreationMethodPanel();
      
      expect(panelState.isCreationMethodPanelOpen).toBe(false);
    });
  });

  describe("Complex Scenarios - Sequential Panel Opening", () => {
    it("should handle rapid panel switching", () => {
      // Simulate user rapidly switching between panels
      panelState.openEditPanel(0, { id: 1 });
      expect(panelState.isEditPanelOpen).toBe(true);

      panelState.openAnimationPanel();
      expect(panelState.isAnimationPanelOpen).toBe(true);
      expect(panelState.isEditPanelOpen).toBe(false);

      panelState.openSharePanel();
      expect(panelState.isSharePanelOpen).toBe(true);
      expect(panelState.isAnimationPanelOpen).toBe(false);

      panelState.openFilterPanel();
      expect(panelState.isFilterPanelOpen).toBe(true);
      expect(panelState.isSharePanelOpen).toBe(false);
    });

    it("should verify only one panel is open after multiple operations", () => {
      // Open multiple panels in sequence
      panelState.openEditPanel(0, { id: 1 });
      panelState.openAnimationPanel();
      panelState.openSharePanel();
      panelState.openFilterPanel();
      panelState.openCAPPanel({}, new Set(), () => {});

      // Only CAP panel should be open
      expect(panelState.isCAPPanelOpen).toBe(true);
      expect(panelState.isEditPanelOpen).toBe(false);
      expect(panelState.isAnimationPanelOpen).toBe(false);
      expect(panelState.isSharePanelOpen).toBe(false);
      expect(panelState.isFilterPanelOpen).toBe(false);
      expect(panelState.isCreationMethodPanelOpen).toBe(false);
    });

    it("should handle close-then-open same panel", () => {
      // Open and close same panel multiple times
      panelState.openSharePanel();
      expect(panelState.isSharePanelOpen).toBe(true);

      panelState.closeSharePanel();
      expect(panelState.isSharePanelOpen).toBe(false);

      panelState.openSharePanel();
      expect(panelState.isSharePanelOpen).toBe(true);
    });
  });

  describe("Panel State Cleanup", () => {
    it("should properly clean up edit panel state when opening another panel", () => {
      const mockBeatData = { id: 1, name: "Test" };
      panelState.openEditPanel(5, mockBeatData);
      
      // Verify state is set
      expect(panelState.editPanelBeatIndex).toBe(5);
      expect(panelState.editPanelBeatData).toEqual(mockBeatData);
      
      // Open another panel
      panelState.openAnimationPanel();
      
      // Edit panel state should be cleared
      expect(panelState.editPanelBeatIndex).toBe(null);
      expect(panelState.editPanelBeatData).toBe(null);
      expect(panelState.editPanelBeatsData).toEqual([]);
    });

    it("should properly clean up CAP panel state when opening another panel", () => {
      const mockType = { name: "test" };
      const mockComponents = new Set(["comp1"]);
      const mockOnChange = () => {};

      panelState.openCAPPanel(mockType, mockComponents, mockOnChange);
      
      // Open another panel
      panelState.openEditPanel(0, { id: 1 });
      
      // CAP panel state should be cleared
      expect(panelState.capCurrentType).toBe(null);
      expect(panelState.capSelectedComponents).toBe(null);
      expect(panelState.capOnChange).toBe(null);
    });
  });

  describe("Edge Cases", () => {
    it("should handle opening same panel twice", () => {
      panelState.openAnimationPanel();
      expect(panelState.isAnimationPanelOpen).toBe(true);

      // Open again - should remain open
      panelState.openAnimationPanel();
      expect(panelState.isAnimationPanelOpen).toBe(true);
    });

    it("should handle closing already closed panel", () => {
      expect(panelState.isSharePanelOpen).toBe(false);
      
      // Close already closed panel - should not error
      panelState.closeSharePanel();
      expect(panelState.isSharePanelOpen).toBe(false);
    });
  });
});
