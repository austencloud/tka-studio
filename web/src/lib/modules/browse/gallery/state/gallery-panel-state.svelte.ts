/**
 * Panel State Management with Svelte 5 Runes
 *
 * Provides reactive state layer wrapping PanelManagementService.
 * Follows TKA architecture: services handle logic, runes handle reactivity.
 */

import {
  ResizeDirection,
  type GalleryPanelState,
  type GalleryPanelResizeOperation as ResizeOperation,
} from "../domain/models/gallery-panel-models";
import type { IGalleryPanelManager } from "../services/contracts";

export interface GalleryPanelStateManager {
  // Panel state getters (reactive)
  readonly navigationPanel: GalleryPanelState;

  // Current resize operation
  readonly currentResize: ResizeOperation | null;

  // Derived states
  readonly isAnyPanelResizing: boolean;
  readonly navigationWidth: number;
  readonly isNavigationCollapsed: boolean;

  // Actions
  toggleNavigationCollapse(): void;
  setNavigationWidth(width: number): void;

  // Resize operations
  startNavigationResize(startX: number): void;
  updateCurrentResize(currentX: number): void;
  endCurrentResize(): void;

  // Utility
  resetPanels(): void;
  cleanup(): void;
}

/**
 * Default panel state for unregistered panels
 */
function getDefaultPanelState(panelId: string): GalleryPanelState {
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

/**
 * Creates reactive panel state manager using Svelte 5 runes
 */
export function createPanelState(
  panelService: IGalleryPanelManager
): GalleryPanelStateManager {
  // ✅ PURE RUNES: Reactive state for UI with default fallbacks
  let navigationPanel = $state<GalleryPanelState>(
    panelService.getPanelState("navigation") ||
      getDefaultPanelState("navigation")
  );
  let currentResize = $state<ResizeOperation | null>(null);

  // ✅ DERIVED RUNES: Computed values from state with defensive checks
  const isAnyPanelResizing = $derived(
    navigationPanel?.isResizing || false || currentResize !== null
  );

  const navigationWidth = $derived(
    navigationPanel?.isCollapsed
      ? navigationPanel?.collapsedWidth || 60
      : navigationPanel?.width || 300
  );

  const isNavigationCollapsed = $derived(navigationPanel?.isCollapsed || false);

  // ✅ SERVICE INTEGRATION: Listen to service state changes
  const handleStateChange = (panelId: string, newState: GalleryPanelState) => {
    if (panelId === "navigation") {
      navigationPanel = newState;
    }
  };

  // Register for state change notifications
  panelService.onPanelStateChanged(handleStateChange);

  // ✅ ACTIONS: Methods that delegate to service
  function toggleNavigationCollapse(): void {
    panelService.togglePanelCollapse("navigation");
  }

  function setNavigationWidth(width: number): void {
    panelService.setPanelWidth("navigation", width);
  }

  // ✅ RESIZE OPERATIONS: Coordinated through service
  function startNavigationResize(startX: number): void {
    const operation: ResizeOperation = {
      panelId: "navigation",
      direction: ResizeDirection.RIGHT,
      startPosition: { x: startX, y: 0 },
      startSize: { width: navigationPanel.width, height: 0 },
    };
    panelService.startResize(operation);
    currentResize = operation;
  }

  function updateCurrentResize(currentX: number): void {
    if (!currentResize) return;

    // Calculate new width based on resize operation
    const deltaX = currentX - currentResize.startPosition.x;
    const newWidth = currentResize.startSize.width + deltaX;

    // Update panel width through service
    if (currentResize.panelId === "navigation") {
      setNavigationWidth(newWidth);
    }
  }

  function endCurrentResize(): void {
    if (!currentResize) return;

    panelService.endResize();
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
    get isNavigationCollapsed() {
      return isNavigationCollapsed;
    },

    // Actions
    toggleNavigationCollapse,
    setNavigationWidth,

    // Resize operations
    startNavigationResize,
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
    title: "Navigation",
    defaultWidth: 300,
    minWidth: 200,
    maxWidth: 500,
    collapsedWidth: 60,
    persistKey: "browse-navigation-panel",
    resizable: true,
    collapsible: true,
  },
} as const;
