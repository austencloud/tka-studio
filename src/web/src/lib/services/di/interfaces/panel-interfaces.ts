/**
 * Panel Management Interfaces
 *
 * Defines contracts for unified panel state management across the application.
 * Supports collapse/expand, resizing, and persistence of panel states.
 */

export interface PanelState {
  id: string;
  width: number;
  isCollapsed: boolean;
  isVisible: boolean;
  minWidth: number;
  maxWidth: number;
  defaultWidth: number;
  collapsedWidth: number;
  isResizing: boolean;
}

export interface PanelConfiguration {
  id: string;
  defaultWidth: number;
  minWidth: number;
  maxWidth: number;
  collapsedWidth: number;
  persistKey: string;
}

export interface ResizeOperation {
  panelId: string;
  startWidth: number;
  startX: number;
  currentX: number;
}

/**
 * Panel Management Service Interface
 *
 * Handles all panel state logic including collapse/expand, resizing, and persistence.
 * Follows microservices pattern with clean separation of business logic.
 */
export interface IPanelManagementService {
  // Panel registration and configuration
  registerPanel(config: PanelConfiguration): void;
  unregisterPanel(panelId: string): void;

  // Panel state management
  getPanelState(panelId: string): PanelState;
  togglePanelCollapse(panelId: string): void;
  setPanelCollapsed(panelId: string, isCollapsed: boolean): void;
  setPanelVisible(panelId: string, isVisible: boolean): void;
  setPanelWidth(panelId: string, width: number): void;

  // Resize operations
  startResize(panelId: string, startX: number): ResizeOperation | null;
  updateResize(operation: ResizeOperation, currentX: number): PanelState;
  endResize(operation: ResizeOperation): void;

  // Validation
  validateWidth(panelId: string, width: number): number;
  canResize(panelId: string): boolean;

  // Persistence
  savePanelStates(): void;
  loadPanelStates(): void;

  // Events
  onPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void,
  ): void;
  offPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void,
  ): void;
}

// Panel resize direction for splitter components
export type ResizeDirection = "left" | "right";

// Splitter configuration
export interface SplitterConfig {
  targetPanelId: string;
  direction: ResizeDirection;
  disabled?: boolean;
  thickness?: number;
}
