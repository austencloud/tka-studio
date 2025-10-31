import type { SequenceData, TabId } from "$shared";
import type { IExploreThumbnailService } from "../../../../modules/explore/display";

// Centralized UI state leveraging Svelte 5 runes.
const uiState = $state({
  activeTab: null as TabId | null,
  showSettings: false,
  isFullScreen: false,
  isTransitioning: false,
  isWaitingForTabLoad: false,
  showSpotlight: false,
  spotlightSequence: null as SequenceData | null,
  spotlightThumbnailService: null as IExploreThumbnailService | null,
});

export function getActiveTab(): TabId | null {
  return uiState.activeTab;
}

export function getActiveTabOrDefault(): TabId {
  return uiState.activeTab || "construct";
}

export function setActiveTab(tab: TabId | null): void {
  uiState.activeTab = tab;
}

export function isTabActive(tab: string): boolean {
  return uiState.activeTab === tab;
}

export function getShowSettings(): boolean {
  return uiState.showSettings;
}

export function setShowSettings(show: boolean): void {
  uiState.showSettings = show;
}

export function toggleShowSettings(): void {
  uiState.showSettings = !uiState.showSettings;
}

export function getIsFullScreen(): boolean {
  return uiState.isFullScreen;
}

export function setFullScreen(fullScreen: boolean): void {
  uiState.isFullScreen = fullScreen;
}

export function getIsTransitioning(): boolean {
  return uiState.isTransitioning;
}

export function setIsTransitioning(isTransitioning: boolean): void {
  uiState.isTransitioning = isTransitioning;
}

export function getIsWaitingForTabLoad(): boolean {
  return uiState.isWaitingForTabLoad;
}

export function setIsWaitingForTabLoad(waiting: boolean): void {
  uiState.isWaitingForTabLoad = waiting;
}

export function getShowSpotlight(): boolean {
  return uiState.showSpotlight;
}

export function getSpotlightSequence(): SequenceData | null {
  return uiState.spotlightSequence;
}

export function getSpotlightThumbnailService(): IExploreThumbnailService | null {
  return uiState.spotlightThumbnailService;
}

export function showSpotlight(
  sequence: SequenceData,
  thumbnailService: IExploreThumbnailService
): void {
  uiState.spotlightSequence = sequence;
  uiState.spotlightThumbnailService = thumbnailService;
  uiState.showSpotlight = true;
}

export function hideSpotlight(): void {
  uiState.showSpotlight = false;
  uiState.spotlightSequence = null;
  uiState.spotlightThumbnailService = null;
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

export function resetUIState(): void {
  uiState.activeTab = "construct";
  uiState.showSettings = false;
  uiState.isFullScreen = false;
  uiState.isTransitioning = false;
  uiState.isWaitingForTabLoad = false;
  uiState.showSpotlight = false;
  uiState.spotlightSequence = null;
  uiState.spotlightThumbnailService = null;
}
