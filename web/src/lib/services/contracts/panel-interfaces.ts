/**
 * Panel Management Service Interfaces
 *
 * Interfaces for managing UI panels, layout, and window management.
 * This handles panel resizing, coordination, and state management.
 */

import type {
  BrowsePanelConfig,
  BrowsePanelState,
  ResizeOperation,
} from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IBrowsePanelManager {
  registerPanel(id: string, config: BrowsePanelConfig): void;
  unregisterPanel(id: string): void;
  getPanelState(id: string): BrowsePanelState | null;
  updatePanelState(id: string, state: Partial<BrowsePanelState>): void;
  startResize(operation: ResizeOperation): void;
  endResize(): void;
  isResizing(): boolean;

  // Additional methods used by panel-state.svelte.ts
  onPanelStateChanged(
    callback: (panelId: string, state: BrowsePanelState) => void
  ): void;
  offPanelStateChanged(
    callback: (panelId: string, state: BrowsePanelState) => void
  ): void;
  togglePanelCollapse(panelId: string): void;
  setPanelVisible(panelId: string, visible: boolean): void;
  setPanelWidth(panelId: string, width: number): void;
  loadPanelStates(): void;
}
