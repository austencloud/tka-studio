/**
 * LayoutState
 * Domain: Application Layout State
 *
 * Responsibilities:
 * - Manage layout measurements (heights, widths)
 * - Track layout orientations (landscape/portrait)
 * - Provide layout state to components
 */

// Reactive state object using Svelte 5 $state rune
export const layoutState = $state({
  // TopBar height - measured dynamically by TopBar component
  topBarHeight: 56, // Default fallback

  // Navigation layout state - updated by PrimaryNavigation
  isPrimaryNavLandscape: false,

  // Panel accessibility state - updated by BuildTab
  // Note: Edit and Export are panels, not tabs
  canAccessEditAndExportPanels: false,

  // Current word state - updated by BuildTab
  currentBuildWord: "",

  // Current learn header - updated by LearnTab
  currentLearnHeader: "",
});

// Helper functions
export function setTopBarHeight(height: number) {
  layoutState.topBarHeight = height;
}

export function setPrimaryNavLandscape(isLandscape: boolean) {
  layoutState.isPrimaryNavLandscape = isLandscape;
}

export function setTabAccessibility(canAccess: boolean) {
  layoutState.canAccessEditAndExportPanels = canAccess;
}

export function setCurrentWord(word: string) {
  layoutState.currentBuildWord = word;
}

export function setLearnHeader(header: string) {
  layoutState.currentLearnHeader = header;
}

// Helper to check if module needs primary navigation
export function moduleHasPrimaryNav(moduleId: string): boolean {
  return (
    moduleId === "build" ||
    moduleId === "learn" ||
    moduleId === "explore" ||
    moduleId === "library" ||
    moduleId === "admin"
  );
}
