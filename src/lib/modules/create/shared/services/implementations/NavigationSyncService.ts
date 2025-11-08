/**
 * Create Module Navigation Sync Service Implementation
 *
 * Manages bidirectional synchronization between global navigation and CreateModule's tool panel tabs.
 * Prevents infinite loops through guard flags and validates tab accessibility based on sequence state.
 *
 * Domain: Create module - Tool Panel Navigation (Construct/Generate)
 * Note: Animate and Share are now separate panels, not BuildSections.
 * Extracted from CreateModule.svelte monolith.
 */

import { createComponentLogger } from "$shared";
import { injectable } from "inversify";
import type {
  BuildSection,
  INavigationSyncService,
} from "../contracts/INavigationSyncService";

@injectable()
export class NavigationSyncService implements INavigationSyncService {
  private logger = createComponentLogger("CreateModule:NavigationSync");

  syncNavigationToCreateModule(
    CreateModuleState: any,
    navigationState: any
  ): void {
    const currentMode = navigationState.currentSection;
    const CreateModuleCurrentMode = CreateModuleState.activeSection;

    this.logger.log("Navigation → CreateModule sync:", {
      currentMode,
      CreateModuleCurrentMode,
      isPersistenceInitialized: CreateModuleState.isPersistenceInitialized,
      isNavigatingBack: CreateModuleState.isNavigatingBack,
      isUpdatingFromToggle: CreateModuleState.isUpdatingFromToggle,
    });

    // Skip if navigation is to a non-Create tab (e.g., "explore", "library")
    const validCreateTabs = ["guided", "construct", "gestural", "generate"];
    if (!validCreateTabs.includes(currentMode)) {
      return;
    }

    // Skip if:
    // 1. Already in sync
    // 2. Persistence not ready
    // 3. Currently navigating back (prevent loop)
    // 4. Updating from toggle (toggle handles its own sync)
    if (
      currentMode === CreateModuleCurrentMode ||
      !CreateModuleState.isPersistenceInitialized ||
      CreateModuleState.isNavigatingBack ||
      CreateModuleState.isUpdatingFromToggle
    ) {
      return;
    }

    // Validate tab access (guard against invalid navigation)
    if (
      !this.validateTabAccess(
        currentMode as BuildSection,
        CreateModuleState.canAccessEditTab
      )
    ) {
      console.warn(
        `🚫 Cannot access ${currentMode} tab without a sequence. Redirecting to construct.`
      );
      navigationState.setCurrentSection(this.getFallbackTab());
      return;
    }

    this.logger.log(
      "Updating CreateModule state from navigation:",
      currentMode
    );
    CreateModuleState.setactiveToolPanel(currentMode);
    this.logger.success(
      "CreateModule state updated to:",
      CreateModuleState.activeSection
    );
  }

  syncCreateModuleToNavigation(
    CreateModuleState: any,
    navigationState: any
  ): void {
    // Skip if updating from toggle (toggle already syncs to navigation)
    if (CreateModuleState.isUpdatingFromToggle) {
      return;
    }

    const CreateModuleCurrentMode = CreateModuleState.activeSection;
    const navCurrentMode = navigationState.currentSection;

    if (CreateModuleCurrentMode && CreateModuleCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSection(CreateModuleCurrentMode);
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
