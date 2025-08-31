/**
 * Build Service Interfaces
 *
 * Interfaces for build tab services including workbench operations,
 * and construction coordination.
 */

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IBuildTabEventService {
  // Event handling methods for build tab interactions
  handleTabSwitch(tabId: string): void;
  handleWorkbenchUpdate(data: unknown): void;
  handleOptionSelection(option: unknown): void;
}

export interface IBuildTabTransitionService {
  // Transition management for build tab state changes
  transitionToTab(tabId: string): Promise<void>;
  getTransitionState(): string;
  isTransitioning(): boolean;
}

export interface IBuildTabService {
  // Main build tab coordination service
  initialize(): Promise<void>;
  getCurrentTab(): string;
  switchToTab(tabId: string): Promise<void>;
  getTabState(tabId: string): unknown;
  updateTabState(tabId: string, state: unknown): void;

  // Option and start position selection
  selectOption(option: any): Promise<void>;
  selectStartPosition(position: any): Promise<void>;
}
