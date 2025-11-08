/**
 * Create Module Panel Coordination State Factory
 *
 * Manages panel state for CreateModule's construction interface using Svelte 5 runes pattern.
 * Coordinates Edit Panel, Animation Panel, and Tool Panel interactions.
 *
 * **PANEL MUTUAL EXCLUSIVITY RULES:**
 * - Only ONE modal/slide panel can be open at a time
 * - Opening any panel automatically closes all other panels
 * - Panels: Edit, Animation, Share, Filter, CAP, CreationMethod
 *
 * Domain: Create module - Panel State Management for Sequence Construction
 * Extracted from CreateModule.svelte monolith to follow runes state management pattern.
 */

import { createComponentLogger } from "$shared";

// Lazy logger initialization to avoid circular dependency issues
let logger: ReturnType<typeof createComponentLogger> | null = null;
const getLogger = () => {
  if (!logger) {
    logger = createComponentLogger("PanelCoordinationState");
  }
  return logger;
};

export interface PanelCoordinationState {
  // Edit Panel State
  get isEditPanelOpen(): boolean;
  get editPanelBeatIndex(): number | null;
  get editPanelBeatData(): any | null;
  get editPanelBeatsData(): any[];

  openEditPanel(beatIndex: number, beatData: any): void;
  openBatchEditPanel(beatsData: any[]): void;
  closeEditPanel(): void;

  // Animation Panel State
  get isAnimationPanelOpen(): boolean;
  set isAnimationPanelOpen(value: boolean);
  get isAnimating(): boolean;

  openAnimationPanel(): void;
  closeAnimationPanel(): void;
  setAnimating(animating: boolean): void;

  // Share Panel State
  get isSharePanelOpen(): boolean;

  openSharePanel(): void;
  closeSharePanel(): void;

  // Filter Panel State
  get isFilterPanelOpen(): boolean;

  openFilterPanel(): void;
  closeFilterPanel(): void;

  // Sequence Actions Panel State
  get isSequenceActionsPanelOpen(): boolean;

  openSequenceActionsPanel(): void;
  closeSequenceActionsPanel(): void;

  // Tool Panel Dimensions (for sizing other panels)
  get toolPanelHeight(): number;
  setToolPanelHeight(height: number): void;

  get toolPanelWidth(): number;
  setToolPanelWidth(width: number): void;

  // Button Panel Height (for accurate slide panel positioning)
  get buttonPanelHeight(): number;
  setButtonPanelHeight(height: number): void;

  // Navigation bar height (responsive to bottom nav safe areas)
  get navigationBarHeight(): number;
  setNavigationBarHeight(height: number): void;

  // Combined height for slide panels (tool + button)
  get combinedPanelHeight(): number;

  // Practice Mode
  get practiceBeatIndex(): number | null;
  setPracticeBeatIndex(index: number | null): void;

  // CAP Panel State
  get isCAPPanelOpen(): boolean;
  get capSelectedComponents(): Set<any> | null;
  get capCurrentType(): any | null;
  get capOnChange(): ((capType: any) => void) | null;

  openCAPPanel(
    currentType: any,
    selectedComponents: Set<any>,
    onChange: (capType: any) => void
  ): void;
  closeCAPPanel(): void;

  // Creation Method Panel State
  get isCreationMethodPanelOpen(): boolean;

  openCreationMethodPanel(): void;
  closeCreationMethodPanel(): void;

  // Derived: Any Panel Open (for UI hiding coordination)
  get isAnyPanelOpen(): boolean;
}

export function createPanelCoordinationState(): PanelCoordinationState {
  // Edit panel state
  let isEditPanelOpen = $state(false);
  let editPanelBeatIndex = $state<number | null>(null);
  let editPanelBeatData = $state<any>(null);
  let editPanelBeatsData = $state<any[]>([]);

  // Animation panel state
  let isAnimationPanelOpen = $state(false);
  let isAnimating = $state(false);

  // Share panel state
  let isSharePanelOpen = $state(false);

  // Filter panel state
  let isFilterPanelOpen = $state(false);

  // Sequence Actions panel state
  let isSequenceActionsPanelOpen = $state(false);

  // Tool panel dimensions tracking
  let toolPanelHeight = $state(0);
  let toolPanelWidth = $state(0);

  // Button panel height tracking
  let buttonPanelHeight = $state(0);

  // Navigation bar height tracking (default to 64px)
  let navigationBarHeight = $state(64);

  // Practice mode
  let practiceBeatIndex = $state<number | null>(null);

  // CAP panel state
  let isCAPPanelOpen = $state(false);
  let capSelectedComponents = $state<Set<any> | null>(null);
  let capCurrentType = $state<any>(null);
  let capOnChange = $state<((capType: any) => void) | null>(null);

  // Creation method panel state
  let isCreationMethodPanelOpen = $state(false);

  /**
   * CRITICAL: Close all panels to enforce mutual exclusivity
   * This ensures only ONE panel is open at a time, preventing state conflicts
   */
  function closeAllPanels() {
    getLogger().log("🚪 Closing all panels for mutual exclusivity");

    // Close all modal/slide panels
    isEditPanelOpen = false;
    editPanelBeatIndex = null;
    editPanelBeatData = null;
    editPanelBeatsData = [];

    isAnimationPanelOpen = false;
    isAnimating = false;

    isSharePanelOpen = false;
    isFilterPanelOpen = false;
    isSequenceActionsPanelOpen = false;

    isCAPPanelOpen = false;
    capSelectedComponents = null;
    capCurrentType = null;
    capOnChange = null;

    isCreationMethodPanelOpen = false;
  }

  return {
    // Edit Panel Getters
    get isEditPanelOpen() {
      return isEditPanelOpen;
    },
    get editPanelBeatIndex() {
      return editPanelBeatIndex;
    },
    get editPanelBeatData() {
      return editPanelBeatData;
    },
    get editPanelBeatsData() {
      return editPanelBeatsData;
    },

    openEditPanel(beatIndex: number, beatData: any) {
      getLogger().log("📝 Opening Edit Panel for beat", beatIndex);
      closeAllPanels(); // Close others first
      editPanelBeatIndex = beatIndex;
      editPanelBeatData = beatData;
      editPanelBeatsData = [];
      isEditPanelOpen = true;
    },

    openBatchEditPanel(beatsData: any[]) {
      getLogger().log(
        "📝 Opening Batch Edit Panel for",
        beatsData.length,
        "beats"
      );
      closeAllPanels(); // Close others first
      editPanelBeatsData = beatsData;
      editPanelBeatIndex = null;
      editPanelBeatData = null;
      isEditPanelOpen = true;
    },

    closeEditPanel() {
      getLogger().log("✖️ Closing Edit Panel");
      isEditPanelOpen = false;
      editPanelBeatIndex = null;
      editPanelBeatData = null;
      editPanelBeatsData = [];
    },

    // Animation Panel Getters
    get isAnimationPanelOpen() {
      return isAnimationPanelOpen;
    },
    set isAnimationPanelOpen(value: boolean) {
      isAnimationPanelOpen = value;
    },
    get isAnimating() {
      return isAnimating;
    },

    openAnimationPanel() {
      getLogger().log("🎬 Opening Animation Panel");
      closeAllPanels(); // Close others first
      isAnimationPanelOpen = true;
    },

    closeAnimationPanel() {
      getLogger().log("✖️ Closing Animation Panel");
      isAnimationPanelOpen = false;
    },

    setAnimating(animating: boolean) {
      isAnimating = animating;
    },

    // Share Panel Getters
    get isSharePanelOpen() {
      return isSharePanelOpen;
    },

    openSharePanel() {
      getLogger().log("📤 Opening Share Panel");
      closeAllPanels(); // Close others first
      isSharePanelOpen = true;
    },

    closeSharePanel() {
      getLogger().log("✖️ Closing Share Panel");
      isSharePanelOpen = false;
    },

    // Filter Panel Getters
    get isFilterPanelOpen() {
      return isFilterPanelOpen;
    },

    openFilterPanel() {
      getLogger().log("🔍 Opening Filter Panel");
      closeAllPanels(); // Close others first
      isFilterPanelOpen = true;
    },

    closeFilterPanel() {
      getLogger().log("✖️ Closing Filter Panel");
      isFilterPanelOpen = false;
    },

    // Sequence Actions Panel Getters
    get isSequenceActionsPanelOpen() {
      return isSequenceActionsPanelOpen;
    },

    openSequenceActionsPanel() {
      getLogger().log("Opening Sequence Actions Panel");
      closeAllPanels(); // Close others first
      isSequenceActionsPanelOpen = true;
    },

    closeSequenceActionsPanel() {
      getLogger().log("Closing Sequence Actions Panel");
      isSequenceActionsPanelOpen = false;
    },

    // Tool Panel Dimensions
    get toolPanelHeight() {
      return toolPanelHeight;
    },

    setToolPanelHeight(height: number) {
      toolPanelHeight = height;
    },

    get toolPanelWidth() {
      return toolPanelWidth;
    },

    setToolPanelWidth(width: number) {
      toolPanelWidth = width;
    },

    // Button Panel Height
    get buttonPanelHeight() {
      return buttonPanelHeight;
    },

    setButtonPanelHeight(height: number) {
      buttonPanelHeight = height;
    },

    // Navigation Bar Height
    get navigationBarHeight() {
      return navigationBarHeight;
    },

    setNavigationBarHeight(height: number) {
      navigationBarHeight = height > 0 ? height : 64;
    },

    // Combined Height (navigation bar + tool + button panels)
    // Navigation bar is 64px (min-height from PrimaryNavigation.svelte)
    get combinedPanelHeight() {
      return navigationBarHeight + toolPanelHeight + buttonPanelHeight;
    },

    // Practice Mode
    get practiceBeatIndex() {
      return practiceBeatIndex;
    },

    setPracticeBeatIndex(index: number | null) {
      practiceBeatIndex = index;
    },

    // CAP Panel Getters
    get isCAPPanelOpen() {
      return isCAPPanelOpen;
    },
    get capSelectedComponents() {
      return capSelectedComponents;
    },
    get capCurrentType() {
      return capCurrentType;
    },
    get capOnChange() {
      return capOnChange;
    },

    openCAPPanel(
      currentType: any,
      selectedComponents: Set<any>,
      onChange: (capType: any) => void
    ) {
      getLogger().log("🎯 Opening CAP Panel");
      closeAllPanels(); // Close others first
      capCurrentType = currentType;
      capSelectedComponents = selectedComponents;
      capOnChange = onChange;
      isCAPPanelOpen = true;
    },

    closeCAPPanel() {
      getLogger().log("✖️ Closing CAP Panel");
      isCAPPanelOpen = false;
      capCurrentType = null;
      capSelectedComponents = null;
      capOnChange = null;
    },

    // Creation Method Panel Getters
    get isCreationMethodPanelOpen() {
      return isCreationMethodPanelOpen;
    },

    openCreationMethodPanel() {
      getLogger().log("🛠️ Opening Creation Method Panel");
      closeAllPanels(); // Close others first
      isCreationMethodPanelOpen = true;
    },

    closeCreationMethodPanel() {
      getLogger().log("✖️ Closing Creation Method Panel");
      isCreationMethodPanelOpen = false;
    },

    // Derived: Check if any modal/slide panel is open
    get isAnyPanelOpen() {
      return (
        isEditPanelOpen ||
        isAnimationPanelOpen ||
        isSharePanelOpen ||
        isFilterPanelOpen ||
        isSequenceActionsPanelOpen ||
        isCAPPanelOpen ||
        isCreationMethodPanelOpen
      );
    },
  };
}
