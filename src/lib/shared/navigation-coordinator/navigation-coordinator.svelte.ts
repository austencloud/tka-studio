/**
 * NavigationCoordinator
 * Domain: Navigation State Coordination
 *
 * Responsibilities:
 * - Coordinate between legacy system and new module/section system
 * - Manage module definitions and current module state
 * - Calculate available module sections based on context
 * - Synchronize navigation state changes
 */
import type { ModuleId } from "../navigation/domain/types";
import {
  MODULE_DEFINITIONS,
  navigationState,
} from "../navigation/state/navigation-state.svelte";
import { setActiveModule } from "../application/state/app-state.svelte";

// Reactive state object using Svelte 5 $state rune
export const navigationCoordinator = $state({
  // Note: Edit and Export are slide-out panels, not navigation sections
  canAccessEditAndExportPanels: false,
});

// Derived state as functions (Svelte 5 doesn't allow exporting $derived directly)
export function currentModule() {
  return navigationState.currentModule;
}

export function currentSection() {
  return navigationState.currentSection;
}

export function currentModuleDefinition() {
  return navigationState.getModuleDefinition(currentModule());
}

export function currentModuleName() {
  return currentModuleDefinition()?.label || "Unknown";
}

// Get sections for current module
// Build module: Construct and Generate sections are shown when no sequence exists.
// When a sequence exists (canAccessEditAndExportPanels = true), all sections are shown.
export function moduleSections() {
  const baseSections = currentModuleDefinition()?.sections || [];
  const module = currentModule();

  // Build module section filtering
  if (module === "build") {
    if (!navigationCoordinator.canAccessEditAndExportPanels) {
      return baseSections.filter((section: { id: string }) => {
        // Show construct and generate sections when no sequence exists
        return section.id === "construct" || section.id === "generate";
      });
    }

    // When sequence exists (edit/export panels accessible), show all sections
    return baseSections;
  }

  return baseSections;
}

// Module change handler
export function handleModuleChange(moduleId: ModuleId) {
  navigationState.setCurrentModule(moduleId);
  // Sync with legacy ui-state so ModuleRenderer knows to switch modules
  setActiveModule(moduleId);
}

// Section change handler
export function handleSectionChange(sectionId: string) {
  const module = currentModule();

  if (module === "learn") {
    navigationState.setLearnMode(sectionId);
  } else {
    // All other modules use the new navigation system
    navigationState.setCurrentSection(sectionId);
  }
}

export const moduleDefinitions = MODULE_DEFINITIONS;
