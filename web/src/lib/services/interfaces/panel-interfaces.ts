/**
 * Panel Management Service Interfaces
 *
 * Interfaces for managing UI panels, layout, and window management.
 * This handles panel resizing, coordination, and state management.
 */

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

export interface PanelState {
  id: string;
  isVisible: boolean;
  isCollapsed: boolean;
  width: number;
  height?: number;
  position?: { x: number; y: number };
  // Extended properties for TKA panel management
  minWidth: number;
  maxWidth: number;
  defaultWidth: number;
  collapsedWidth: number;
  isResizing: boolean;
}

export interface PanelConfiguration {
  id: string;
  title: string;
  defaultWidth: number;
  defaultHeight?: number;
  minWidth: number;
  maxWidth: number;
  minHeight?: number;
  resizable?: boolean;
  collapsible?: boolean;
  collapsedWidth: number;
  persistKey: string;
}

export interface ResizeOperation {
  panelId: string;
  direction: ResizeDirection;
  startPosition: { x: number; y: number };
  startSize: { width: number; height: number };
}

export enum ResizeDirection {
  HORIZONTAL = "horizontal",
  VERTICAL = "vertical",
  BOTH = "both",
}

export interface SplitterConfig {
  orientation: "horizontal" | "vertical";
  initialPosition: number;
  minPosition: number;
  maxPosition: number;
}
