/**
 * Build Tab Navigation Sync Service Implementation
 *
 * Manages bidirectional synchronization between global navigation and BuildTab's tool panel tabs.
 * Prevents infinite loops through guard flags and validates tab accessibility based on sequence state.
 *
 * Domain: Build Module - Tool Panel Navigation (Construct/Generate)
 * Note: Animate and Share are now separate panels, not BuildSections.
 * Extracted from BuildTab.svelte monolith.
 */

import { createComponentLogger } from "$shared";
import { injectable } from "inversify";
import type { BuildSection, INavigationSyncService } from "../contracts/INavigationSyncService";

@injectable()
export class NavigationSyncService implements INavigationSyncService {
  private logger = createComponentLogger('BuildTab:NavigationSync');

  syncNavigationToBuildTab(buildTabState: any, navigationState: any): void {
    const currentMode = navigationState.currentSection;
    const buildTabCurrentMode = buildTabState.activeSection;

    this.logger.log("Navigation → BuildTab sync:", {
      currentMode,
      buildTabCurrentMode,
      isPersistenceInitialized: buildTabState.isPersistenceInitialized,
      isNavigatingBack: buildTabState.isNavigatingBack,
      isUpdatingFromToggle: buildTabState.isUpdatingFromToggle,
    });

    // Skip if navigation is to a non-build section (e.g., "explore", "library")
    const validBuildSections = ["construct", "gestural", "generate"];
    if (!validBuildSections.includes(currentMode)) {
      return;
    }

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
    if (!this.validateTabAccess(currentMode as BuildSection, buildTabState.canAccessEditTab)) {
      console.warn(`🚫 Cannot access ${currentMode} tab without a sequence. Redirecting to construct.`);
      navigationState.setCurrentSection(this.getFallbackTab());
      return;
    }

    this.logger.log("Updating buildTab state from navigation:", currentMode);
    buildTabState.setactiveToolPanel(currentMode);
    this.logger.success("BuildTab state updated to:", buildTabState.activeSection);
  }

  syncBuildTabToNavigation(buildTabState: any, navigationState: any): void {
    // Skip if updating from toggle (toggle already syncs to navigation)
    if (buildTabState.isUpdatingFromToggle) {
      return;
    }

    const buildTabCurrentMode = buildTabState.activeSection;
    const navCurrentMode = navigationState.currentSection;

    if (buildTabCurrentMode && buildTabCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSection(buildTabCurrentMode);
    }
  }

  validateTabAccess(mode: BuildSection, canAccessEditTab: boolean): boolean {
    // Construct, gestural, and generate are always accessible
    return true;
  }

  getFallbackTab(): BuildSection {
    return "construct";
  }
}
