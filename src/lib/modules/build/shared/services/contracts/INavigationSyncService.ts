/**
 * Build Tab Navigation Sync Service Contract
 *
 * Handles bidirectional synchronization between global navigation state and BuildTab state.
 * Manages tab switching within BuildTab's tool panel (Construct, Generate, Animate, etc.)
 * Includes tab accessibility validation and navigation guard logic for construction workflow.
 *
 * Domain: Build Module - Navigation within Sequence Construction Interface
 * Extracted from BuildTab.svelte monolith to follow DI architecture.
 */

export type BuildSubMode = "construct" | "generate" | "animate" | "share" | "record";

export interface INavigationSyncService {
  /**
   * Sync navigation state changes to build tab state
   * @param buildTabState Build tab state object
   * @param navigationState Navigation state object
   */
  syncNavigationToBuildTab(buildTabState: any, navigationState: any): void;

  /**
   * Sync build tab state changes back to navigation state
   * @param buildTabState Build tab state object
   * @param navigationState Navigation state object
   */
  syncBuildTabToNavigation(buildTabState: any, navigationState: any): void;

  /**
   * Validate if a tab is accessible based on sequence state
   * @param mode Target sub-mode
   * @param canAccessEditTab Whether edit/export tabs are accessible
   * @returns Whether navigation to the tab should be allowed
   */
  validateTabAccess(mode: BuildSubMode, canAccessEditTab: boolean): boolean;

  /**
   * Get the fallback tab when access is denied
   */
  getFallbackTab(): BuildSubMode;
}
