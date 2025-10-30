/**
 * Panel Height Tracker
 *
 * Consolidates panel height tracking effects using ResizeObserver.
 * Tracks tool panel and button panel heights for accurate positioning.
 *
 * Domain: Build Module - Panel Height Management
 */

import type { PanelCoordinationState } from "../panel-coordination-state.svelte";

export interface PanelHeightTrackerConfig {
  toolPanelElement: HTMLElement | null;
  buttonPanelElement: HTMLElement | null;
  panelState: PanelCoordinationState;
}

/**
 * Creates panel height tracking effects
 * @returns Cleanup function
 */
export function createPanelHeightTracker(config: PanelHeightTrackerConfig): () => void {
  const { toolPanelElement, buttonPanelElement, panelState } = config;

  const cleanups: (() => void)[] = [];

  // Track tool panel height
  if (toolPanelElement) {
    const toolResizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        panelState.setToolPanelHeight(entry.contentRect.height);
      }
    });
    toolResizeObserver.observe(toolPanelElement);
    cleanups.push(() => toolResizeObserver.disconnect());
  }

  // Track button panel height
  if (buttonPanelElement) {
    const buttonResizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        panelState.setButtonPanelHeight(entry.contentRect.height);
      }
    });
    buttonResizeObserver.observe(buttonPanelElement);
    cleanups.push(() => buttonResizeObserver.disconnect());
  }

  return () => {
    cleanups.forEach(cleanup => cleanup());
  };
}
