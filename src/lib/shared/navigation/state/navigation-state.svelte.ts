/**
 * Navigation State - Global Navigation State Management
 *
 * Manages global navigation state including current modes for tabs with sub-modes.
 * This provides a centralized way to track and update navigation state across the app.
 */

import type { ModeOption, ModuleDefinition, ModuleId } from "../domain/types";

// Build modes configuration - mutable to allow dynamic tab accessibility updates
// Note: Edit functionality is now handled via a slide-out panel, not a tab
// Note: Animate is now a Play button in the button panel with inline animator
// Note: Record removed (not implemented yet, users will use native camera apps)
export const BUILD_MODES: ModeOption[] = [
  {
    id: "construct",
    label: "Construct",
    icon: '<i class="fas fa-hammer"></i>',
    description: "Build sequences step by step",
    color: "#3b82f6",
    gradient: "linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)",
  },
  {
    id: "generate",
    label: "Generate",
    icon: '<i class="fas fa-bolt"></i>',
    description: "Auto-create sequences",
    color: "#f59e0b",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #f97316 100%)",
  },
];

// Learn modes configuration
export const LEARN_MODES: ModeOption[] = [
  {
    id: "concepts",
    label: "Concepts",
    icon: '<i class="fas fa-graduation-cap"></i>',
    description: "Progressive concept mastery path",
    color: "#60a5fa",
    gradient: "linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)",
  },
  {
    id: "drills",
    label: "Drills",
    icon: '<i class="fas fa-bolt"></i>',
    description: "Quick pictograph flash card quizzes",
    color: "#f472b6",
    gradient: "linear-gradient(135deg, #f472b6 0%, #ec4899 100%)",
  },
  {
    id: "read",
    label: "Read",
    icon: '<i class="fas fa-book-open"></i>',
    description: "Beautiful PDF flipbook reader",
    color: "#5eead4",
    gradient: "linear-gradient(135deg, #5eead4 0%, #14b8a6 100%)",
  },
];

// Explore modes configuration
export const EXPLORE_MODES: ModeOption[] = [
  {
    id: "explore",
    label: "Explore",
    icon: '<i class="fas fa-compass"></i>',
    description: "Explore and discover sequences",
    color: "#a855f7",
    gradient: "linear-gradient(135deg, #c084fc 0%, #a855f7 100%)",
  },
];

// Module definitions for the new navigation system
export const MODULE_DEFINITIONS: ModuleDefinition[] = [
  {
    id: "build",
    label: "Build",
    icon: '<i class="fas fa-tools" style="color: #f59e0b;"></i>', // Amber - construction/creation
    description: "Create and edit sequences",
    isMain: true,
    subModes: BUILD_MODES,
  },
  {
    id: "explore",
    label: "Explore",
    icon: '<i class="fas fa-compass" style="color: #a855f7;"></i>', // Purple - discovery/exploration
    description: "Explore and discover sequences",
    isMain: true,
    subModes: EXPLORE_MODES,
  },
  {
    id: "learn",
    label: "Learn",
    icon: '<i class="fas fa-graduation-cap" style="color: #3b82f6;"></i>', // Blue - education/knowledge
    description: "Study and practice TKA",
    isMain: true,
    subModes: LEARN_MODES,
  },
  {
    id: "write",
    label: "Write",
    icon: '<i class="fas fa-pen" style="color: #14b8a6;"></i>', // Teal - writing/communication
    description: "Write sequences as text",
    isMain: false,
    subModes: [
      {
        id: "write",
        label: "Write",
        icon: '<i class="fas fa-pen" style="color: #14b8a6;"></i>',
        description: "Write sequences as text",
      },
    ],
  },
  {
    id: "word_card",
    label: "Word Card",
    icon: '<i class="fas fa-id-card" style="color: #ec4899;"></i>', // Pink - cards/printables
    description: "Generate word cards",
    isMain: false,
    subModes: [
      {
        id: "word_card",
        label: "Word Card",
        icon: '<i class="fas fa-id-card" style="color: #ec4899;"></i>',
        description: "Generate word cards",
      },
    ],
  },
];

/**
 * Creates navigation state for managing current modes
 */
export function createNavigationState() {
  // State - existing modes for backward compatibility
  let currentBuildMode = $state<string>("construct");
  let currentLearnMode = $state<string>("concepts");

  // New module-based state
  let currentModule = $state<ModuleId>("build");
  let currentSubMode = $state<string>("construct");
  const MODULE_LAST_SUB_MODES_KEY = "tka-module-last-sub-modes";
  let lastSubModeByModule = $state<Partial<Record<ModuleId, string>>>({});

  // Load persisted state
  if (typeof localStorage !== "undefined") {
    // Load existing mode persistence
    const savedBuildMode = localStorage.getItem("tka-current-build-mode");
    if (savedBuildMode && BUILD_MODES.some((m) => m.id === savedBuildMode)) {
      currentBuildMode = savedBuildMode;
    }

    const savedLearnMode = localStorage.getItem("tka-current-learn-mode");
    if (savedLearnMode && LEARN_MODES.some((m) => m.id === savedLearnMode)) {
      currentLearnMode = savedLearnMode;
    }

    // Load new module-based persistence
    const savedModule = localStorage.getItem("tka-current-module");
    if (savedModule && MODULE_DEFINITIONS.some((m) => m.id === savedModule)) {
      currentModule = savedModule as ModuleId;
    }

    const savedLastSubModes = localStorage.getItem(MODULE_LAST_SUB_MODES_KEY);
    if (savedLastSubModes) {
      try {
        const parsed = JSON.parse(savedLastSubModes) as Record<string, string>;
        const filteredEntries = Object.entries(parsed).filter(
          ([moduleId, subModeId]) => {
            const moduleDefinition = MODULE_DEFINITIONS.find(
              (m) => m.id === moduleId
            );
            return (
              moduleDefinition?.subModes?.some((mode) => mode.id === subModeId) ??
              false
            );
          }
        );

        if (filteredEntries.length > 0) {
          lastSubModeByModule = filteredEntries.reduce<
            Partial<Record<ModuleId, string>>
          >((acc, [moduleId, subModeId]) => {
            acc[moduleId as ModuleId] = subModeId;
            return acc;
          }, {});
        }
      } catch (error) {
        console.warn(
          "NavigationState: failed to parse saved module sub-mode map:",
          error
        );
      }
    }

    const savedSubMode = localStorage.getItem("tka-current-sub-mode");
    if (savedSubMode) {
      // Will validate and set in the getter functions
      currentSubMode = savedSubMode;
    }

    const rememberedSubMode = lastSubModeByModule[currentModule];
    if (rememberedSubMode) {
      const moduleDefinition = MODULE_DEFINITIONS.find(
        (m) => m.id === currentModule
      );
      if (
        moduleDefinition?.subModes?.some((mode) => mode.id === rememberedSubMode)
      ) {
        currentSubMode = rememberedSubMode;
      }
    }
  }

  // Actions
  function setBuildMode(mode: string) {
    if (BUILD_MODES.some((m) => m.id === mode)) {
      currentBuildMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-build-mode", mode);
      }
      // Sync with new state - will be handled by the getter functions
    }
  }

  function setLearnMode(mode: string) {
    if (LEARN_MODES.some((m) => m.id === mode)) {
      currentLearnMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-learn-mode", mode);
      }
      // Sync with new state - will be handled by the getter functions
    }
  }

  function persistLastSubModes() {
    if (typeof localStorage === "undefined") {
      return;
    }

    try {
      localStorage.setItem(
        MODULE_LAST_SUB_MODES_KEY,
        JSON.stringify(lastSubModeByModule)
      );
    } catch (error) {
      console.warn(
        "NavigationState: failed to persist module sub-mode map:",
        error
      );
    }
  }

  // New module-based functions
  function setCurrentModule(moduleId: ModuleId) {
    if (MODULE_DEFINITIONS.some((m) => m.id === moduleId)) {
      currentModule = moduleId;

      // Set default sub-mode for the module
      const moduleDefinition = MODULE_DEFINITIONS.find(
        (m) => m.id === moduleId
      );
      let nextSubMode = currentSubMode;
      if (moduleDefinition && moduleDefinition.subModes.length > 0) {
        const remembered = lastSubModeByModule[moduleId];
        const fallbackSubMode = moduleDefinition.subModes[0].id;
        const resolvedSubMode =
          remembered &&
          moduleDefinition.subModes.some((mode) => mode.id === remembered)
            ? remembered
            : fallbackSubMode;

        nextSubMode = resolvedSubMode;
        lastSubModeByModule = {
          ...lastSubModeByModule,
          [moduleId]: resolvedSubMode,
        };
      } else {
        const updatedMap = { ...lastSubModeByModule };
        delete updatedMap[moduleId];
        lastSubModeByModule = updatedMap;
      }

      currentSubMode = nextSubMode;

      // Persist both module and sub-mode
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-module", moduleId);
        if (nextSubMode) {
          localStorage.setItem("tka-current-sub-mode", nextSubMode);
        }
      }

      persistLastSubModes();

      // Sync with legacy state - use getters to avoid state reference warnings
      const subMode = getCurrentSubMode();
      if (moduleId === "build") {
        setBuildMode(subMode);
      } else if (moduleId === "learn") {
        setLearnMode(subMode);
      }
    }
  }

  function setCurrentSubMode(subModeId: string) {
    const moduleDefinition = MODULE_DEFINITIONS.find(
      (m) => m.id === currentModule
    );
    if (
      moduleDefinition &&
      moduleDefinition.subModes.some((sm) => sm.id === subModeId)
    ) {
      currentSubMode = subModeId;

      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-sub-mode", subModeId);
      }

      lastSubModeByModule = {
        ...lastSubModeByModule,
        [currentModule]: subModeId,
      };
      persistLastSubModes();

      // Sync with legacy state - use getters to avoid state reference warnings
      const module = getCurrentModule();
      if (module === "build") {
        setBuildMode(subModeId);
      } else if (module === "learn") {
        setLearnMode(subModeId);
      }
    }
  }

  function getCurrentModule(): ModuleId {
    return currentModule;
  }

  function getCurrentSubMode(): string {
    return currentSubMode;
  }

  function getSubModesForModule(moduleId: ModuleId): ModeOption[] {
    const moduleDefinition = MODULE_DEFINITIONS.find((m) => m.id === moduleId);
    return moduleDefinition ? moduleDefinition.subModes : [];
  }

  function getModuleDefinition(
    moduleId: ModuleId
  ): ModuleDefinition | undefined {
    return MODULE_DEFINITIONS.find((m) => m.id === moduleId);
  }

  function updateTabAccessibility(tabId: string, disabled: boolean) {
    // Find and update the tab in BUILD_MODES (mutate directly)
    const tab = BUILD_MODES.find((m) => m.id === tabId);
    if (tab) {
      tab.disabled = disabled;
    }
  }

  return {
    // Readonly state - existing for backward compatibility
    get currentBuildMode() {
      return currentBuildMode;
    },
    get currentLearnMode() {
      return currentLearnMode;
    },

    // New module-based readonly state
    get currentModule() {
      return currentModule;
    },
    get currentSubMode() {
      return currentSubMode;
    },

    // Mode configurations
    get buildModes() {
      return BUILD_MODES;
    },
    get learnModes() {
      return LEARN_MODES;
    },
    get exploreModes() {
      return EXPLORE_MODES;
    },
    // Legacy getter for backward compatibility
    get ExploreModes() {
      return EXPLORE_MODES;
    },
    get moduleDefinitions() {
      return MODULE_DEFINITIONS;
    },

    // Actions - existing for backward compatibility
    setBuildMode,
    setLearnMode,

    // New module-based actions
    setCurrentModule,
    setCurrentSubMode,
    getCurrentModule,
    getCurrentSubMode,
    getSubModesForModule,
    getModuleDefinition,
    updateTabAccessibility,
  };
}

// Global navigation state instance
export const navigationState = createNavigationState();
