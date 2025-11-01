/**
 * Navigation State - Global Navigation State Management
 *
 * Manages global navigation state including current modes for tabs with sub-modes.
 * This provides a centralized way to track and update navigation state across the app.
 */

import type { ModuleDefinition, ModuleId, Section } from "../domain/types";

// Build tabs configuration - mutable to allow dynamic tab accessibility updates
// Note: Edit functionality is now handled via a slide-out panel, not a tab
// Note: Animate is now a Play button in the button panel with inline animator
// Note: Record removed (not implemented yet, users will use native camera apps)
export const BUILD_TABS: Section[] = [
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

// Learn tabs configuration
export const LEARN_TABS: Section[] = [
  {
    id: "concepts",
    label: "Concepts",
    icon: '<i class="fas fa-lightbulb"></i>',
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

// Explore tabs configuration
export const EXPLORE_TABS: Section[] = [
  {
    id: "explore",
    label: "Explore",
    icon: '<i class="fas fa-compass"></i>',
    description: "Explore and discover sequences",
    color: "#a855f7",
    gradient: "linear-gradient(135deg, #c084fc 0%, #a855f7 100%)",
  },
];

// Library tabs configuration
export const LIBRARY_TABS: Section[] = [
  {
    id: "sequences",
    label: "Sequences",
    icon: '<i class="fas fa-layer-group"></i>',
    description: "My sequences and saved content",
    color: "#10b981",
    gradient: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
  },
  {
    id: "acts",
    label: "Acts",
    icon: '<i class="fas fa-film"></i>',
    description: "My acts (coming soon)",
    color: "#f59e0b",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)",
    disabled: true,
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
    sections: BUILD_TABS,
  },
  {
    id: "explore",
    label: "Explore",
    icon: '<i class="fas fa-compass" style="color: #a855f7;"></i>', // Purple - discovery/exploration
    description: "Explore and discover sequences",
    isMain: true,
    sections: EXPLORE_TABS,
  },
  {
    id: "learn",
    label: "Learn",
    icon: '<i class="fas fa-graduation-cap" style="color: #3b82f6;"></i>', // Blue - education/knowledge
    description: "Study and practice TKA",
    isMain: true,
    sections: LEARN_TABS,
  },
  {
    id: "library",
    label: "Library",
    icon: '<i class="fas fa-book" style="color: #10b981;"></i>', // Green - personal collection/library
    description: "My sequences and saved content",
    isMain: true,
    sections: LIBRARY_TABS,
  },
  {
    id: "write",
    label: "Write",
    icon: '<i class="fas fa-pen" style="color: #14b8a6;"></i>', // Teal - writing/communication
    description: "Write sequences as text",
    isMain: false,
    sections: [
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
    sections: [
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
 * Creates navigation state for managing modules and tabs
 */
export function createNavigationState() {
  // Legacy state - for backward compatibility
  let currentBuildMode = $state<string>("construct");
  let currentLearnMode = $state<string>("concepts");

  // Module-based state
  let currentModule = $state<ModuleId>("build");
  let activeTab = $state<string>("construct"); // Active tab within the current module
  const MODULE_LAST_TABS_KEY = "tka-module-last-tabs";
  let lastTabByModule = $state<Partial<Record<ModuleId, string>>>({});

  // Load persisted state
  if (typeof localStorage !== "undefined") {
    // Load legacy mode persistence
    const savedBuildMode = localStorage.getItem("tka-current-build-mode");
    if (savedBuildMode && BUILD_TABS.some((t) => t.id === savedBuildMode)) {
      currentBuildMode = savedBuildMode;
    }

    const savedLearnMode = localStorage.getItem("tka-current-learn-mode");
    if (savedLearnMode && LEARN_TABS.some((t) => t.id === savedLearnMode)) {
      currentLearnMode = savedLearnMode;
    }

    // Load module persistence
    const savedModule = localStorage.getItem("tka-current-module");
    if (savedModule && MODULE_DEFINITIONS.some((m) => m.id === savedModule)) {
      currentModule = savedModule as ModuleId;
    }

    // Load last active tab for each module
    const savedLastTabs = localStorage.getItem(MODULE_LAST_TABS_KEY);
    if (savedLastTabs) {
      try {
        const parsed = JSON.parse(savedLastTabs) as Record<string, string>;
        const filteredEntries = Object.entries(parsed).filter(
          ([moduleId, tabId]) => {
            const moduleDefinition = MODULE_DEFINITIONS.find(
              (m) => m.id === moduleId
            );
            return (
              moduleDefinition?.sections?.some(
                (tab) => tab.id === tabId
              ) ?? false
            );
          }
        );

        if (filteredEntries.length > 0) {
          lastTabByModule = filteredEntries.reduce<
            Partial<Record<ModuleId, string>>
          >((acc, [moduleId, tabId]) => {
            acc[moduleId as ModuleId] = tabId;
            return acc;
          }, {});
        }
      } catch (error) {
        console.warn(
          "NavigationState: failed to parse saved module tab map:",
          error
        );
      }
    }

    // Load current active tab
    const savedActiveTab = localStorage.getItem("tka-active-tab");
    if (savedActiveTab) {
      activeTab = savedActiveTab;
    }

    // Remember the last active tab for current module
    const getRememberedTab = () => {
      const module = currentModule;
      const lastTabs = lastTabByModule;
      return lastTabs[module];
    };
    const rememberedTab = getRememberedTab();
    if (rememberedTab) {
      const moduleDefinition = MODULE_DEFINITIONS.find(
        (m) => m.id === currentModule
      );
      if (
        moduleDefinition?.sections?.some(
          (tab) => tab.id === rememberedTab
        )
      ) {
        activeTab = rememberedTab;
      }
    }
  }

  // Legacy action functions
  function setBuildMode(mode: string) {
    if (BUILD_TABS.some((t) => t.id === mode)) {
      currentBuildMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-build-mode", mode);
      }
    }
  }

  function setLearnMode(mode: string) {
    if (LEARN_TABS.some((t) => t.id === mode)) {
      currentLearnMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-learn-mode", mode);
      }
      // Sync with new state when in Learn module
      if (currentModule === "learn") {
        activeTab = mode;
      }
    }
  }

  function persistLastTabs() {
    if (typeof localStorage === "undefined") {
      return;
    }

    try {
      localStorage.setItem(
        MODULE_LAST_TABS_KEY,
        JSON.stringify(lastTabByModule)
      );
    } catch (error) {
      console.warn(
        "NavigationState: failed to persist module tab map:",
        error
      );
    }
  }

  // Module-based functions
  function setCurrentModule(moduleId: ModuleId) {
    if (MODULE_DEFINITIONS.some((m) => m.id === moduleId)) {
      currentModule = moduleId;

      // Set default tab for the module
      const moduleDefinition = MODULE_DEFINITIONS.find(
        (m) => m.id === moduleId
      );
      let nextTab = activeTab;
      if (moduleDefinition && moduleDefinition.sections.length > 0) {
        const remembered = lastTabByModule[moduleId];
        const fallbackTab = moduleDefinition.sections[0].id;
        const resolvedTab =
          remembered &&
          moduleDefinition.sections.some((tab) => tab.id === remembered)
            ? remembered
            : fallbackTab;

        nextTab = resolvedTab;
        lastTabByModule = {
          ...lastTabByModule,
          [moduleId]: resolvedTab,
        };
      } else {
        const updatedMap = { ...lastTabByModule };
        delete updatedMap[moduleId];
        lastTabByModule = updatedMap;
      }

      activeTab = nextTab;

      // Persist both module and active tab
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-module", moduleId);
        if (nextTab) {
          localStorage.setItem("tka-active-tab", nextTab);
        }
      }

      persistLastTabs();

      // Sync with legacy state
      const tab = getActiveTab();
      if (moduleId === "build") {
        setBuildMode(tab);
      } else if (moduleId === "learn") {
        setLearnMode(tab);
      }
    }
  }

  function setActiveTab(tabId: string) {
    const moduleDefinition = MODULE_DEFINITIONS.find(
      (m) => m.id === currentModule
    );
    if (
      moduleDefinition &&
      moduleDefinition.sections.some((tab) => tab.id === tabId)
    ) {
      activeTab = tabId;

      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-active-tab", tabId);
      }

      lastTabByModule = {
        ...lastTabByModule,
        [currentModule]: tabId,
      };
      persistLastTabs();

      // Sync with legacy state
      const module = getCurrentModule();
      if (module === "build") {
        setBuildMode(tabId);
      } else if (module === "learn") {
        setLearnMode(tabId);
      }
    }
  }

  function getCurrentModule(): ModuleId {
    return currentModule;
  }

  function getActiveTab(): string {
    return activeTab;
  }

  function getTabsForModule(moduleId: ModuleId): Section[] {
    const moduleDefinition = MODULE_DEFINITIONS.find((m) => m.id === moduleId);
    return moduleDefinition ? moduleDefinition.sections : [];
  }

  function getModuleDefinition(
    moduleId: ModuleId
  ): ModuleDefinition | undefined {
    return MODULE_DEFINITIONS.find((m) => m.id === moduleId);
  }

  function updateTabAccessibility(tabId: string, disabled: boolean) {
    // Find and update the tab in BUILD_TABS (mutate directly)
    const tab = BUILD_TABS.find((t) => t.id === tabId);
    if (tab) {
      tab.disabled = disabled;
    }
  }

  return {
    // Legacy readonly state - for backward compatibility
    get currentBuildMode() {
      return currentBuildMode;
    },
    get currentLearnMode() {
      return currentLearnMode;
    },

    // Module-based readonly state
    get currentModule() {
      return currentModule;
    },
    get activeTab() {
      return activeTab;
    },

    // Tab configurations
    get buildTabs() {
      return BUILD_TABS;
    },
    get learnTabs() {
      return LEARN_TABS;
    },
    get exploreTabs() {
      return EXPLORE_TABS;
    },
    get libraryTabs() {
      return LIBRARY_TABS;
    },
    get moduleDefinitions() {
      return MODULE_DEFINITIONS;
    },

    // Legacy getters (deprecated)
    /** @deprecated Use buildTabs instead */
    get buildModes() {
      return BUILD_TABS;
    },
    /** @deprecated Use learnTabs instead */
    get learnModes() {
      return LEARN_TABS;
    },
    /** @deprecated Use exploreTabs instead */
    get exploreModes() {
      return EXPLORE_TABS;
    },
    /** @deprecated Use exploreTabs instead */
    get ExploreModes() {
      return EXPLORE_TABS;
    },
    /** @deprecated Use activeTab instead */
    get currentSection() {
      return activeTab;
    },

    // Legacy actions - for backward compatibility
    setBuildMode,
    setLearnMode,

    // Module-based actions
    setCurrentModule,
    setActiveTab,
    getCurrentModule,
    getActiveTab,
    getTabsForModule,
    getModuleDefinition,
    updateTabAccessibility,

    // Legacy action aliases (deprecated)
    /** @deprecated Use setActiveTab instead */
    setCurrentSection: setActiveTab,
    /** @deprecated Use getActiveTab instead */
    getCurrentSection: getActiveTab,
    /** @deprecated Use getTabsForModule instead */
    getSectionsForModule: getTabsForModule,
  };
}

// Global navigation state instance
export const navigationState = createNavigationState();
