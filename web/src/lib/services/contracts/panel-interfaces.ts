/**
 * Panel Management Service Interfaces
 *
 * Interfaces for managing UI panels, layout, and window management.
 * This handles panel resizing, coordination, and state management.
 */

import type { PanelConfiguration, PanelState, ResizeOperation } from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IPanelManagementService {
  registerPanel(id: string, config: PanelConfiguration): void;
  unregisterPanel(id: string): void;
  getPanelState(id: string): PanelState | null;
  updatePanelState(id: string, state: Partial<PanelState>): void;
  startResize(operation: ResizeOperation): void;
  endResize(): void;
  isResizing(): boolean;

  // Additional methods used by panel-state.svelte.ts
  onPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void
  ): void;
  offPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void
  ): void;
  togglePanelCollapse(panelId: string): void;
  setPanelVisible(panelId: string, visible: boolean): void;
  setPanelWidth(panelId: string, width: number): void;
  loadPanelStates(): void;
}

// ============================================================================
// RE-EXPORT TYPES FOR EXTERNAL USE
// ============================================================================

// Re-export types that other modules need to import
export type {
  PanelConfiguration,
  PanelState,
  ResizeDirection,
  ResizeOperation,
} from "$domain";
