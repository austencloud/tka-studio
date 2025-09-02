/**
 * Panel Management Service Implementation
 *
 * Provides unified panel state management with collapse/expand, resizing, and persistence.
 * Follows microservices architecture with clean business logic separation.
 */

import type {
  IPanelManagementService,
  PanelConfiguration,
  PanelState,
  ResizeOperation,
} from "$contracts";
import { injectable } from "inversify";

@injectable()
export class PanelManagementService implements IPanelManagementService {
  private panels = new Map<string, PanelState>();
  private configurations = new Map<string, PanelConfiguration>();
  private currentResize: ResizeOperation | null = null;
  private stateChangeCallbacks: Array<
    (panelId: string, state: PanelState) => void
  > = [];

  constructor() {
    this.loadPanelStates();
  }

  // Panel registration
  registerPanel(id: string, config: PanelConfiguration): void {
    // Use the provided id, but also ensure config.id matches
    const panelId = id || config.id;
    const panelConfig = { ...config, id: panelId };

    this.configurations.set(panelId, panelConfig);

    // Create initial state if not exists
    if (!this.panels.has(panelId)) {
      const savedWidth = this.loadPanelWidth(
        panelConfig.persistKey,
        panelConfig.defaultWidth
      );
      const initialState: PanelState = {
        id: panelId,
        width: savedWidth,
        isCollapsed: false,
        isVisible: true,
        minWidth: panelConfig.minWidth,
        maxWidth: panelConfig.maxWidth,
        defaultWidth: panelConfig.defaultWidth,
        collapsedWidth: panelConfig.collapsedWidth,
        isResizing: false,
      };

      this.panels.set(panelId, initialState);
    }
  }

  unregisterPanel(panelId: string): void {
    this.panels.delete(panelId);
    this.configurations.delete(panelId);
  }

  // Panel state management
  getPanelState(panelId: string): PanelState | null {
    const state = this.panels.get(panelId);
    if (!state) {
      // Return null for unregistered panels as per interface contract
      console.warn(`Panel not registered: ${panelId}, returning null`);
      return null;
    }
    return { ...state }; // Return copy to prevent direct mutation
  }

  updatePanelState(id: string, state: Partial<PanelState>): void {
    const currentState = this.panels.get(id);
    if (!currentState) {
      console.warn(`Cannot update state for unregistered panel: ${id}`);
      return;
    }

    const updatedState = { ...currentState, ...state };
    this.panels.set(id, updatedState);
    this.notifyStateChange(id, updatedState);
    this.savePanelStates();
  }

  togglePanelCollapse(panelId: string): void {
    const state = this.panels.get(panelId);
    if (!state) return;

    this.setPanelCollapsed(panelId, !state.isCollapsed);
  }

  setPanelCollapsed(panelId: string, isCollapsed: boolean): void {
    const state = this.panels.get(panelId);
    if (!state) return;

    const updatedState = {
      ...state,
      isCollapsed,
      // Don't change width when collapsing - layout handles this with CSS
    };

    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
    this.savePanelStates();
  }

  setPanelVisible(panelId: string, isVisible: boolean): void {
    const state = this.panels.get(panelId);
    if (!state) return;

    const updatedState = {
      ...state,
      isVisible,
    };

    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
  }

  setPanelWidth(panelId: string, width: number): void {
    const state = this.panels.get(panelId);
    if (!state) return;

    const validatedWidth = this.validateWidth(panelId, width);
    const updatedState = {
      ...state,
      width: validatedWidth,
    };

    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);
    this.savePanelStates();
  }

  // Resize operations
  startResize(operation: ResizeOperation): void {
    const state = this.panels.get(operation.panelId);
    if (!state || !this.canResize(operation.panelId)) {
      return;
    }

    this.currentResize = operation;

    // Mark panel as resizing
    const updatedState = { ...state, isResizing: true };
    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);
  }

  endResize(): void {
    if (!this.currentResize) return;

    const state = this.panels.get(this.currentResize.panelId);
    if (state) {
      const updatedState = { ...state, isResizing: false };
      this.panels.set(this.currentResize.panelId, updatedState);
      this.notifyStateChange(this.currentResize.panelId, updatedState);
    }

    this.currentResize = null;
    this.savePanelStates();
  }

  isResizing(): boolean {
    return this.currentResize !== null;
  }

  // Legacy methods for backward compatibility (can be removed later)
  updateResize(operation: ResizeOperation, currentX: number): PanelState {
    const state = this.panels.get(operation.panelId);
    if (!state) {
      throw new Error(`Panel not found during resize: ${operation.panelId}`);
    }

    const deltaX = currentX - operation.startPosition.x;
    const newWidth = operation.startSize.width + deltaX;
    const validatedWidth = this.validateWidth(operation.panelId, newWidth);

    const updatedState = {
      ...state,
      width: validatedWidth,
    };

    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);

    return updatedState;
  }

  // Legacy method - use endResize() instead
  endResizeOperation(_operation: ResizeOperation): void {
    this.endResize();
  }

  // Validation
  validateWidth(panelId: string, width: number): number {
    const state = this.panels.get(panelId);
    if (!state) return width;

    return Math.max(state.minWidth, Math.min(state.maxWidth, width));
  }

  canResize(panelId: string): boolean {
    const state = this.panels.get(panelId);
    return !!(state && state.isVisible && !state.isCollapsed);
  }

  // Persistence
  savePanelStates(): void {
    try {
      const states: Record<string, { width: number; isCollapsed: boolean }> =
        {};

      for (const [panelId, state] of this.panels) {
        const config = this.configurations.get(panelId);
        if (config) {
          states[config.persistKey] = {
            width: state.width,
            isCollapsed: state.isCollapsed,
          };
        }
      }

      localStorage.setItem("tka-panel-states", JSON.stringify(states));
    } catch (error) {
      console.warn("Failed to save panel states:", error);
    }
  }

  loadPanelStates(): void {
    try {
      const saved = localStorage.getItem("tka-panel-states");
      if (!saved) return;

      const states = JSON.parse(saved);

      // Will apply to panels when they are registered
      this.savedStates = states;
    } catch (error) {
      console.warn("Failed to load panel states:", error);
    }
  }

  private savedStates: Record<string, { width: number; isCollapsed: boolean }> =
    {};

  private loadPanelWidth(persistKey: string, defaultWidth: number): number {
    const saved = this.savedStates[persistKey];
    return saved?.width ?? defaultWidth;
  }

  // Event handling
  onPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void
  ): void {
    this.stateChangeCallbacks.push(callback);
  }

  offPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void
  ): void {
    const index = this.stateChangeCallbacks.indexOf(callback);
    if (index > -1) {
      this.stateChangeCallbacks.splice(index, 1);
    }
  }

  private notifyStateChange(panelId: string, state: PanelState): void {
    this.stateChangeCallbacks.forEach((callback) => {
      try {
        callback(panelId, { ...state });
      } catch (error) {
        console.error("Error in panel state change callback:", error);
      }
    });
  }

  // Utility methods
  getAllPanelStates(): Record<string, PanelState> {
    const states: Record<string, PanelState> = {};
    for (const [panelId, state] of this.panels) {
      states[panelId] = { ...state };
    }
    return states;
  }

  resetPanel(panelId: string): void {
    const config = this.configurations.get(panelId);
    if (!config) return;

    const resetState: PanelState = {
      id: panelId,
      width: config.defaultWidth,
      isCollapsed: false,
      isVisible: true,
      minWidth: config.minWidth,
      maxWidth: config.maxWidth,
      defaultWidth: config.defaultWidth,
      collapsedWidth: config.collapsedWidth,
      isResizing: false,
    };

    this.panels.set(panelId, resetState);
    this.notifyStateChange(panelId, resetState);
    this.savePanelStates();
  }

  resetAllPanels(): void {
    for (const panelId of this.panels.keys()) {
      this.resetPanel(panelId);
    }
  }
}
