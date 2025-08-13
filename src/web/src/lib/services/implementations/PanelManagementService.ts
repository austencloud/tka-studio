/**
 * Panel Management Service Implementation
 *
 * Provides unified panel state management with collapse/expand, resizing, and persistence.
 * Follows microservices architecture with clean business logic separation.
 */

import type {
  IPanelManagementService,
  PanelState,
  PanelConfiguration,
  ResizeOperation,
} from "../di/interfaces/panel-interfaces";

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
  registerPanel(config: PanelConfiguration): void {
    this.configurations.set(config.id, config);

    // Create initial state if not exists
    if (!this.panels.has(config.id)) {
      const savedWidth = this.loadPanelWidth(
        config.persistKey,
        config.defaultWidth,
      );
      const initialState: PanelState = {
        id: config.id,
        width: savedWidth,
        isCollapsed: false,
        isVisible: true,
        minWidth: config.minWidth,
        maxWidth: config.maxWidth,
        defaultWidth: config.defaultWidth,
        collapsedWidth: config.collapsedWidth,
        isResizing: false,
      };

      this.panels.set(config.id, initialState);
    }
  }

  unregisterPanel(panelId: string): void {
    this.panels.delete(panelId);
    this.configurations.delete(panelId);
  }

  // Panel state management
  getPanelState(panelId: string): PanelState {
    const state = this.panels.get(panelId);
    if (!state) {
      // Return a default state for unregistered panels instead of throwing
      console.warn(`Panel not registered: ${panelId}, returning default state`);
      return {
        id: panelId,
        width: 300,
        isCollapsed: false,
        isVisible: true,
        minWidth: 200,
        maxWidth: 600,
        defaultWidth: 300,
        collapsedWidth: 60,
        isResizing: false,
      };
    }
    return { ...state }; // Return copy to prevent direct mutation
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
  startResize(panelId: string, startX: number): ResizeOperation | null {
    const state = this.panels.get(panelId);
    if (!state || !this.canResize(panelId)) {
      return null;
    }

    const operation: ResizeOperation = {
      panelId,
      startWidth: state.width,
      startX,
      currentX: startX,
    };

    this.currentResize = operation;

    // Mark panel as resizing
    const updatedState = { ...state, isResizing: true };
    this.panels.set(panelId, updatedState);
    this.notifyStateChange(panelId, updatedState);

    return operation;
  }

  updateResize(operation: ResizeOperation, currentX: number): PanelState {
    const state = this.panels.get(operation.panelId);
    if (!state) {
      throw new Error(`Panel not found during resize: ${operation.panelId}`);
    }

    operation.currentX = currentX;
    const deltaX = currentX - operation.startX;
    const newWidth = operation.startWidth + deltaX;
    const validatedWidth = this.validateWidth(operation.panelId, newWidth);

    const updatedState = {
      ...state,
      width: validatedWidth,
    };

    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);

    return updatedState;
  }

  endResize(operation: ResizeOperation): void {
    const state = this.panels.get(operation.panelId);
    if (!state) return;

    const updatedState = { ...state, isResizing: false };
    this.panels.set(operation.panelId, updatedState);
    this.notifyStateChange(operation.panelId, updatedState);

    this.currentResize = null;
    this.savePanelStates();
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

  private loadPanelCollapsed(persistKey: string): boolean {
    const saved = this.savedStates[persistKey];
    return saved?.isCollapsed ?? false;
  }

  // Event handling
  onPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void,
  ): void {
    this.stateChangeCallbacks.push(callback);
  }

  offPanelStateChanged(
    callback: (panelId: string, state: PanelState) => void,
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
