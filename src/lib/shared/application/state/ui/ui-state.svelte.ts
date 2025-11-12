import type { SequenceData, TabId } from "$shared";
import type { IExploreThumbnailService } from "../../../../modules/explore/display";
import { browser } from "$app/environment";

// Get initial module from localStorage (synchronous, fast)
function getInitialModuleSync(): TabId | null {
  if (!browser) return null;

  try {
    const cached = localStorage.getItem("tka-active-module-cache");
    if (cached) {
      const parsed = JSON.parse(cached);
      if (parsed?.moduleId) {
        console.log(
          `📦 [ui-state] Initial module from localStorage:`,
          parsed.moduleId
        );
        return parsed.moduleId as TabId;
      }
    }
  } catch (e) {
    // Ignore errors
  }

  return null;
}

// Centralized UI state leveraging Svelte 5 runes.
// Uses TabId (which includes both ModuleId and LegacyTabId) for backwards compatibility
export const uiState = $state({
  activeModule: getInitialModuleSync(), // Load from localStorage immediately
  showSettings: false,
  isFullScreen: false,
  isTransitioning: false,
  isWaitingForModuleLoad: false,
  showSpotlight: false,
  spotlightSequence: null as SequenceData | null,
  spotlightThumbnailService: null as IExploreThumbnailService | null,
});

// ============================================================================
// MODULE STATE (Primary API)
// ============================================================================

export function getActiveModule(): TabId | null {
  return uiState.activeModule;
}

export function getActiveModuleOrDefault(): TabId {
  return uiState.activeModule || "create";
}

export function setActiveModule(module: TabId | null): void {
  uiState.activeModule = module;
}

export function isModuleActive(module: string): boolean {
  return uiState.activeModule === module;
}

// ============================================================================
// LEGACY TAB API (for backwards compatibility)
// @deprecated Use module functions instead
// ============================================================================

/** @deprecated Use getActiveModule() instead */
export function getActiveTab(): TabId | null {
  return getActiveModule();
}

/** @deprecated Use getActiveModuleOrDefault() instead */
export function getActiveTabOrDefault(): TabId {
  return getActiveModuleOrDefault();
}

/** @deprecated Use setActiveModule() instead */
export function setActiveTab(module: TabId | null): void {
  setActiveModule(module);
}

/** @deprecated Use isModuleActive() instead */
export function isTabActive(module: string): boolean {
  return isModuleActive(module);
}

// ============================================================================
// SETTINGS STATE
// ============================================================================

export function getShowSettings(): boolean {
  return uiState.showSettings;
}

export function setShowSettings(show: boolean): void {
  uiState.showSettings = show;
}

export function toggleShowSettings(): void {
  uiState.showSettings = !uiState.showSettings;
}

export function showSettingsDialog(): void {
  setShowSettings(true);
}

export function hideSettingsDialog(): void {
  setShowSettings(false);
}

export function toggleSettingsDialog(): void {
  toggleShowSettings();
}

// ============================================================================
// FULLSCREEN STATE
// ============================================================================

export function getIsFullScreen(): boolean {
  return uiState.isFullScreen;
}

export function setFullScreen(fullScreen: boolean): void {
  uiState.isFullScreen = fullScreen;
}

// ============================================================================
// TRANSITION STATE
// ============================================================================

export function getIsTransitioning(): boolean {
  return uiState.isTransitioning;
}

export function setIsTransitioning(isTransitioning: boolean): void {
  uiState.isTransitioning = isTransitioning;
}

// ============================================================================
// MODULE LOADING STATE
// ============================================================================

export function getIsWaitingForModuleLoad(): boolean {
  return uiState.isWaitingForModuleLoad;
}

export function setIsWaitingForModuleLoad(waiting: boolean): void {
  uiState.isWaitingForModuleLoad = waiting;
}

/** @deprecated Use getIsWaitingForModuleLoad() instead */
export function getIsWaitingForTabLoad(): boolean {
  return getIsWaitingForModuleLoad();
}

/** @deprecated Use setIsWaitingForModuleLoad() instead */
export function setIsWaitingForTabLoad(waiting: boolean): void {
  setIsWaitingForModuleLoad(waiting);
}

// ============================================================================
// SPOTLIGHT STATE
// ============================================================================

export function getShowSpotlight(): boolean {
  return uiState.showSpotlight;
}

export function getSpotlightSequence(): SequenceData | null {
  return uiState.spotlightSequence;
}

export function getSpotlightThumbnailService(): IExploreThumbnailService | null {
  return uiState.spotlightThumbnailService;
}

export function openSpotlightViewer(
  sequence: SequenceData,
  thumbnailService: IExploreThumbnailService
): void {
  uiState.spotlightSequence = sequence;
  uiState.spotlightThumbnailService = thumbnailService;
  uiState.showSpotlight = true;
}

export function closeSpotlightViewer(): void {
  uiState.showSpotlight = false;
  uiState.spotlightSequence = null;
  uiState.spotlightThumbnailService = null;
}

// ============================================================================
// RESET STATE
// ============================================================================

export function resetUIState(): void {
  uiState.activeModule = "create";
  uiState.showSettings = false;
  uiState.isFullScreen = false;
  uiState.isTransitioning = false;
  uiState.isWaitingForModuleLoad = false;
  uiState.showSpotlight = false;
  uiState.spotlightSequence = null;
  uiState.spotlightThumbnailService = null;
}
