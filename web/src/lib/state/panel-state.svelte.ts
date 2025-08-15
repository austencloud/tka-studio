/**
 * Panel State Management with Svelte 5 Runes
 *
 * Provides reactive state layer wrapping PanelManagementService.
 * Follows TKA architecture: services handle logic, runes handle reactivity.
 */

import type {
  IPanelManagementService,
  PanelState,
  ResizeOperation,
} from "$lib/services/di/interfaces/panel-interfaces";

export interface PanelStateManager {
  // Panel state getters (reactive)
  readonly navigationPanel: PanelState;
  readonly animationPanel: PanelState;

  // Current resize operation
  readonly currentResize: ResizeOperation | null;

  // Derived states
  readonly isAnyPanelResizing: boolean;
  readonly navigationWidth: number;
  readonly animationWidth: number;
  readonly isNavigationCollapsed: boolean;
  readonly isAnimationCollapsed: boolean;
  readonly isAnimationVisible: boolean;

  // Actions
  toggleNavigationCollapse(): void;
  toggleAnimationCollapse(): void;
  setAnimationVisible(visible: boolean): void;
  setNavigationWidth(width: number): void;
  setAnimationWidth(width: number): void;

  // Resize operations
  startNavigationResize(startX: number): void;
  startAnimationResize(startX: number): void;
  updateCurrentResize(currentX: number): void;
  endCurrentResize(): void;

  // Utility
  resetPanels(): void;
  cleanup(): void;
}

/**
 * Creates reactive panel state manager using Svelte 5 runes
 */
export function createPanelState(
  panelService: IPanelManagementService
): PanelStateManager {
  // ✅ PURE RUNES: Reactive state for UI
  let navigationPanel = $state<PanelState>(
    panelService.getPanelState("navigation")
  );
  let animationPanel = $state<PanelState>(
    panelService.getPanelState("animation")
  );
  let currentResize = $state<ResizeOperation | null>(null);

  // ✅ DERIVED RUNES: Computed values from state
  const isAnyPanelResizing = $derived(
    navigationPanel.isResizing ||
      animationPanel.isResizing ||
      currentResize !== null
  );

  const navigationWidth = $derived(
    navigationPanel.isCollapsed
      ? navigationPanel.collapsedWidth
      : navigationPanel.width
  );

  const animationWidth = $derived(
    animationPanel.isCollapsed
      ? animationPanel.collapsedWidth
      : animationPanel.width
  );

  const isNavigationCollapsed = $derived(navigationPanel.isCollapsed);
  const isAnimationCollapsed = $derived(animationPanel.isCollapsed);
  const isAnimationVisible = $derived(animationPanel.isVisible);

  // ✅ SERVICE INTEGRATION: Listen to service state changes
  const handleStateChange = (panelId: string, newState: PanelState) => {
    if (panelId === "navigation") {
      navigationPanel = newState;
    } else if (panelId === "animation") {
      animationPanel = newState;
    }
  };

  // Register for state change notifications
  panelService.onPanelStateChanged(handleStateChange);

  // ✅ ACTIONS: Methods that delegate to service
  function toggleNavigationCollapse(): void {
    panelService.togglePanelCollapse("navigation");
  }

  function toggleAnimationCollapse(): void {
    panelService.togglePanelCollapse("animation");
  }

  function setAnimationVisible(visible: boolean): void {
    panelService.setPanelVisible("animation", visible);
  }

  function setNavigationWidth(width: number): void {
    panelService.setPanelWidth("navigation", width);
  }

  function setAnimationWidth(width: number): void {
    panelService.setPanelWidth("animation", width);
  }

  // ✅ RESIZE OPERATIONS: Coordinated through service
  function startNavigationResize(startX: number): void {
    const operation = panelService.startResize("navigation", startX);
    currentResize = operation;
  }

  function startAnimationResize(startX: number): void {
    const operation = panelService.startResize("animation", startX);
    currentResize = operation;
  }

  function updateCurrentResize(currentX: number): void {
    if (!currentResize) return;

    panelService.updateResize(currentResize, currentX);
    // State will be updated through handleStateChange callback
  }

  function endCurrentResize(): void {
    if (!currentResize) return;

    panelService.endResize(currentResize);
    currentResize = null;
  }

  // ✅ UTILITY: Reset and cleanup
  function resetPanels(): void {
    // Reset panels by loading default states
    panelService.loadPanelStates();
  }

  function cleanup(): void {
    panelService.offPanelStateChanged(handleStateChange);
  }

  // ✅ RETURN REACTIVE INTERFACE
  return {
    // Reactive getters
    get navigationPanel() {
      return navigationPanel;
    },
    get animationPanel() {
      return animationPanel;
    },
    get currentResize() {
      return currentResize;
    },

    // Derived states
    get isAnyPanelResizing() {
      return isAnyPanelResizing;
    },
    get navigationWidth() {
      return navigationWidth;
    },
    get animationWidth() {
      return animationWidth;
    },
    get isNavigationCollapsed() {
      return isNavigationCollapsed;
    },
    get isAnimationCollapsed() {
      return isAnimationCollapsed;
    },
    get isAnimationVisible() {
      return isAnimationVisible;
    },

    // Actions
    toggleNavigationCollapse,
    toggleAnimationCollapse,
    setAnimationVisible,
    setNavigationWidth,
    setAnimationWidth,

    // Resize operations
    startNavigationResize,
    startAnimationResize,
    updateCurrentResize,
    endCurrentResize,

    // Utility
    resetPanels,
    cleanup,
  };
}

/**
 * Default panel configurations for browse tab
 */
export const BROWSE_TAB_PANEL_CONFIGS = {
  navigation: {
    id: "navigation",
    defaultWidth: 300,
    minWidth: 200,
    maxWidth: 500,
    collapsedWidth: 60,
    persistKey: "browse-navigation-panel",
  },
  animation: {
    id: "animation",
    defaultWidth: 400,
    minWidth: 300,
    maxWidth: 600,
    collapsedWidth: 60,
    persistKey: "browse-animation-panel",
  },
} as const;
