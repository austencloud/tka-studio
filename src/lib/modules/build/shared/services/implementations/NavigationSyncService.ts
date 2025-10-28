/**
 * Build Tab Navigation Sync Service Implementation
 *
 * Manages bidirectional synchronization between global navigation and BuildTab's tool panel tabs.
 * Prevents infinite loops through guard flags and validates tab accessibility based on sequence state.
 *
 * Domain: Build Module - Tool Panel Navigation (Construct/Generate/Animate/Share/Record)
 * Extracted from BuildTab.svelte monolith.
 */

import { createComponentLogger } from "$shared";
import { injectable } from "inversify";
import type { BuildSubMode, INavigationSyncService } from "../contracts/INavigationSyncService";

@injectable()
export class NavigationSyncService implements INavigationSyncService {
  private logger = createComponentLogger('BuildTab:NavigationSync');

  syncNavigationToBuildTab(buildTabState: any, navigationState: any): void {
    const currentMode = navigationState.currentSubMode;
    const buildTabCurrentMode = buildTabState.activeSubTab;

    this.logger.log("Navigation → BuildTab sync:", {
      currentMode,
      buildTabCurrentMode,
      isPersistenceInitialized: buildTabState.isPersistenceInitialized,
      isNavigatingBack: buildTabState.isNavigatingBack,
      isUpdatingFromToggle: buildTabState.isUpdatingFromToggle,
    });

    // Skip if:
    // 1. Already in sync
    // 2. Persistence not ready
    // 3. Currently navigating back (prevent loop)
    // 4. Updating from toggle (toggle handles its own sync)
    if (
      currentMode === buildTabCurrentMode ||
      !buildTabState.isPersistenceInitialized ||
      buildTabState.isNavigatingBack ||
      buildTabState.isUpdatingFromToggle
    ) {
      return;
    }

    // Validate tab access (guard against invalid navigation)
    if (!this.validateTabAccess(currentMode as BuildSubMode, buildTabState.canAccessEditTab)) {
      console.warn(`🚫 Cannot access ${currentMode} tab without a sequence. Redirecting to construct.`);
      navigationState.setCurrentSubMode(this.getFallbackTab());
      return;
    }

    this.logger.log("Updating buildTab state from navigation:", currentMode);
    buildTabState.setactiveToolPanel(currentMode);
    this.logger.success("BuildTab state updated to:", buildTabState.activeSubTab);
  }

  syncBuildTabToNavigation(buildTabState: any, navigationState: any): void {
    // Skip if updating from toggle (toggle already syncs to navigation)
    if (buildTabState.isUpdatingFromToggle) {
      return;
    }

    const buildTabCurrentMode = buildTabState.activeSubTab;
    const navCurrentMode = navigationState.currentSubMode;

    if (buildTabCurrentMode && buildTabCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSubMode(buildTabCurrentMode);
    }
  }

  validateTabAccess(mode: BuildSubMode, canAccessEditTab: boolean): boolean {
    // Construct and generate are always accessible
    if (mode === "construct" || mode === "generate") {
      return true;
    }

    // Animate, share, record require a valid sequence
    // (canAccessEditTab indicates a sequence exists)
    return canAccessEditTab;
  }

  getFallbackTab(): BuildSubMode {
    return "construct";
  }
}
