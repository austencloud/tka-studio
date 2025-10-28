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

  // Tool Panel Height (for sizing other panels)
  get toolPanelHeight(): number;
  setToolPanelHeight(height: number): void;

  // Practice Mode
  get practiceBeatIndex(): number | null;
  setPracticeBeatIndex(index: number | null): void;
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

  // Tool panel height tracking
  let toolPanelHeight = $state(0);

  // Practice mode
  let practiceBeatIndex = $state<number | null>(null);

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

    // Tool Panel Height
    get toolPanelHeight() { return toolPanelHeight; },

    setToolPanelHeight(height: number) {
      toolPanelHeight = height;
    },

    // Practice Mode
    get practiceBeatIndex() { return practiceBeatIndex; },

    setPracticeBeatIndex(index: number | null) {
      practiceBeatIndex = index;
    },
  };
}
