/**
 * Build Tab Panel Coordination State Factory
 *
 * Manages panel state for BuildTab's construction interface using Svelte 5 runes pattern.
 * Coordinates Edit Panel, Animation Panel, and Tool Panel interactions.
 *
 * Domain: Build Module - Panel State Management for Sequence Construction
 * Extracted from BuildTab.svelte monolith to follow runes state management pattern.
 */


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

  // Tool Panel Height (for sizing other panels)
  get toolPanelHeight(): number;
  setToolPanelHeight(height: number): void;

  // Button Panel Height (for accurate slide panel positioning)
  get buttonPanelHeight(): number;
  setButtonPanelHeight(height: number): void;

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

  openCAPPanel(currentType: any, selectedComponents: Set<any>, onChange: (capType: any) => void): void;
  closeCAPPanel(): void;
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

  // Tool panel height tracking
  let toolPanelHeight = $state(0);

  // Button panel height tracking
  let buttonPanelHeight = $state(0);

  // Practice mode
  let practiceBeatIndex = $state<number | null>(null);

  // CAP panel state
  let isCAPPanelOpen = $state(false);
  let capSelectedComponents = $state<Set<any> | null>(null);
  let capCurrentType = $state<any>(null);
  let capOnChange = $state<((capType: any) => void) | null>(null);

  return {
    // Edit Panel Getters
    get isEditPanelOpen() { return isEditPanelOpen; },
    get editPanelBeatIndex() { return editPanelBeatIndex; },
    get editPanelBeatData() { return editPanelBeatData; },
    get editPanelBeatsData() { return editPanelBeatsData; },

    openEditPanel(beatIndex: number, beatData: any) {
      editPanelBeatIndex = beatIndex;
      editPanelBeatData = beatData;
      editPanelBeatsData = [];
      isEditPanelOpen = true;
    },

    openBatchEditPanel(beatsData: any[]) {
      editPanelBeatsData = beatsData;
      editPanelBeatIndex = null;
      editPanelBeatData = null;
      isEditPanelOpen = true;
    },

    closeEditPanel() {
      isEditPanelOpen = false;
      editPanelBeatIndex = null;
      editPanelBeatData = null;
      editPanelBeatsData = [];
    },

    // Animation Panel Getters
    get isAnimationPanelOpen() { return isAnimationPanelOpen; },
    get isAnimating() { return isAnimating; },

    openAnimationPanel() {
      isAnimationPanelOpen = true;
    },

    closeAnimationPanel() {
      isAnimationPanelOpen = false;
    },

    setAnimating(animating: boolean) {
      isAnimating = animating;
    },

    // Share Panel Getters
    get isSharePanelOpen() { return isSharePanelOpen; },

    openSharePanel() {
      isSharePanelOpen = true;
    },

    closeSharePanel() {
      isSharePanelOpen = false;
    },

    // Filter Panel Getters
    get isFilterPanelOpen() { return isFilterPanelOpen; },

    openFilterPanel() {
      isFilterPanelOpen = true;
    },

    closeFilterPanel() {
      isFilterPanelOpen = false;
    },

    // Tool Panel Height
    get toolPanelHeight() { return toolPanelHeight; },

    setToolPanelHeight(height: number) {
      toolPanelHeight = height;
    },

    // Button Panel Height
    get buttonPanelHeight() { return buttonPanelHeight; },

    setButtonPanelHeight(height: number) {
      buttonPanelHeight = height;
    },

    // Combined Height (navigation bar + tool + button panels)
    // Navigation bar is 64px (min-height from PrimaryNavigation.svelte)
    get combinedPanelHeight() {
      const navigationBarHeight = 64;
      return navigationBarHeight + toolPanelHeight + buttonPanelHeight;
    },

    // Practice Mode
    get practiceBeatIndex() { return practiceBeatIndex; },

    setPracticeBeatIndex(index: number | null) {
      practiceBeatIndex = index;
    },

    // CAP Panel Getters
    get isCAPPanelOpen() { return isCAPPanelOpen; },
    get capSelectedComponents() { return capSelectedComponents; },
    get capCurrentType() { return capCurrentType; },
    get capOnChange() { return capOnChange; },

    openCAPPanel(currentType: any, selectedComponents: Set<any>, onChange: (capType: any) => void) {
      capCurrentType = currentType;
      capSelectedComponents = selectedComponents;
      capOnChange = onChange;
      isCAPPanelOpen = true;
    },

    closeCAPPanel() {
      isCAPPanelOpen = false;
      capCurrentType = null;
      capSelectedComponents = null;
      capOnChange = null;
    },
  };
}
