/**
 * Navigation State - Global Navigation State Management
 *
 * Manages global navigation state including current modes for tabs with sub-modes.
 * This provides a centralized way to track and update navigation state across the app.
 */

import type { ModuleDefinition, ModuleId, Section } from "../domain/types";

// Create tabs configuration - mutable to allow dynamic tab accessibility updates
// Note: Edit functionality is now handled via a slide-out panel, not a tab
// Note: Animate is now a Play button in the button panel with inline animator
// Note: Record removed (not implemented yet, users will use native camera apps)
// Note: HandPath (gestural) temporarily removed - not ready for production
export const CREATE_TABS: Section[] = [
  {
    id: "guided",
    label: "Guided",
    icon: '<i class="fas fa-compass"></i>',
    description: "Build sequences one hand at a time (6 simple choices)",
    color: "#8b5cf6",
    gradient: "linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)",
  },
  {
    id: "construct",
    label: "Standard",
    icon: '<i class="fas fa-hammer"></i>',
    description: "Create sequences step by step (all options)",
    color: "#3b82f6",
    gradient: "linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)",
  },
  {
    id: "generate",
    label: "Generate",
    icon: '<i class="fas fa-wand-magic-sparkles"></i>',
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
    id: "sequences",
    label: "Sequences",
    icon: '<i class="fas fa-layer-group"></i>',
    description: "Browse and discover sequences",
    color: "#a855f7",
    gradient: "linear-gradient(135deg, #c084fc 0%, #a855f7 100%)",
  },
  {
    id: "users",
    label: "Users",
    icon: '<i class="fas fa-users"></i>',
    description: "Discover creators and contributors",
    color: "#06b6d4",
    gradient: "linear-gradient(135deg, #22d3ee 0%, #06b6d4 100%)",
  },
  {
    id: "collections",
    label: "Collections",
    icon: '<i class="fas fa-folder"></i>',
    description: "Browse curated playlists",
    color: "#f59e0b",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)",
  },
];

// Collect tabs configuration (formerly Library/Collection)
export const COLLECT_TABS: Section[] = [
  {
    id: "gallery",
    label: "Gallery",
    icon: '<i class="fas fa-images"></i>',
    description: "My saved sequences",
    color: "#10b981",
    gradient: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
  },
  {
    id: "achievements",
    label: "Achievements",
    icon: '<i class="fas fa-trophy"></i>',
    description: "Progress, stats, and unlocked achievements",
    color: "#ffd700",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #ffd700 100%)",
  },
  {
    id: "challenges",
    label: "Challenges",
    icon: '<i class="fas fa-bullseye"></i>',
    description: "Daily challenges and active quests",
    color: "#667eea",
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  },
];

// Legacy exports for backwards compatibility during migration
export const BUILD_TABS = CREATE_TABS; // Legacy name
export const LIBRARY_TABS = COLLECT_TABS; // Legacy name
export const COLLECTION_TABS = COLLECT_TABS; // Legacy name

// Admin tabs configuration
export const ADMIN_TABS: Section[] = [
  {
    id: "challenges",
    label: "Challenges",
    icon: '<i class="fas fa-calendar-day"></i>',
    description: "Manage daily challenges",
    color: "#ffd700",
    gradient: "linear-gradient(135deg, #fbbf24 0%, #ffd700 100%)",
  },
  {
    id: "analytics",
    label: "Analytics",
    icon: '<i class="fas fa-chart-line"></i>',
    description: "View app usage and metrics",
    color: "#3b82f6",
    gradient: "linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)",
  },
  {
    id: "users",
    label: "Users",
    icon: '<i class="fas fa-users"></i>',
    description: "Manage users and permissions",
    color: "#10b981",
    gradient: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
  },
];

// Module definitions for the new navigation system
export const MODULE_DEFINITIONS: ModuleDefinition[] = [
  {
    id: "create",
    label: "Create",
    icon: '<i class="fas fa-tools" style="color: #f59e0b;"></i>', // Amber - construction/creation
    description: "Construct and generate sequences",
    isMain: true,
    sections: CREATE_TABS,
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
    id: "collect",
    label: "Collect",
    icon: '<i class="fas fa-box-archive" style="color: #10b981;"></i>', // Green - collect/archive
    description: "My gallery, achievements, and challenges",
    isMain: true,
    sections: COLLECT_TABS,
  },
  // Removed: write and word_card modules (not currently in use)
  {
    id: "admin",
    label: "Admin",
    icon: '<i class="fas fa-crown" style="color: #ffd700;"></i>', // Gold - admin/privileged
    description: "System management & configuration",
    isMain: false, // Only visible to admins
    sections: ADMIN_TABS,
  },
];

/**
 * Creates navigation state for managing modules and tabs
 */
export function createNavigationState() {
  // Current state
  let currentCreateMode = $state<string>("construct");
  let currentLearnMode = $state<string>("concepts");

  // Module-based state
  let currentModule = $state<ModuleId>("create");
  let activeTab = $state<string>("construct"); // Active tab within the current module
  const MODULE_LAST_TABS_KEY = "tka-module-last-tabs";
  let lastTabByModule = $state<Partial<Record<ModuleId, string>>>({});

  // Creation method selector visibility (for hiding tabs when selector is shown)
  let isCreationMethodSelectorVisible = $state<boolean>(false);

  // Load persisted state
  if (typeof localStorage !== "undefined") {
    // Load create mode persistence
    const savedCreateMode = localStorage.getItem("tka-current-create-mode");
    if (savedCreateMode && CREATE_TABS.some((t) => t.id === savedCreateMode)) {
      currentCreateMode = savedCreateMode;
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
              moduleDefinition?.sections?.some((tab) => tab.id === tabId) ??
              false
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
      if (moduleDefinition?.sections?.some((tab) => tab.id === rememberedTab)) {
        activeTab = rememberedTab;
      }
    }
  }

  // Action functions
  function setCreateMode(mode: string) {
    if (CREATE_TABS.some((t) => t.id === mode)) {
      currentCreateMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-create-mode", mode);
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
      console.warn("NavigationState: failed to persist module tab map:", error);
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
        const fallbackTab = moduleDefinition.sections[0]!.id;
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

      // Sync with mode-specific state
      const tab = getActiveTab();
      if (moduleId === "create") {
        setCreateMode(tab);
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

      // Sync with mode-specific state
      const module = getCurrentModule();
      if (module === "create") {
        setCreateMode(tabId);
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
    // Find and update the tab in CREATE_TABS (mutate directly)
    const tab = CREATE_TABS.find((t) => t.id === tabId);
    if (tab) {
      tab.disabled = disabled;
    }
  }

  return {
    // Current state
    get currentCreateMode() {
      return currentCreateMode;
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
    get createTabs() {
      return CREATE_TABS;
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
    get adminTabs() {
      return ADMIN_TABS;
    },
    get moduleDefinitions() {
      return MODULE_DEFINITIONS;
    },

    // Legacy getters (deprecated)
    /** @deprecated Use createTabs instead */
    get CreateModules() {
      return CREATE_TABS;
    },
    /** @deprecated Use createTabs instead */
    get buildModes() {
      return CREATE_TABS;
    },
    /** @deprecated Use createTabs instead */
    get createModes() {
      return CREATE_TABS;
    },
    /** @deprecated Use currentCreateMode instead */
    get currentBuildMode() {
      return currentCreateMode;
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

    // Actions
    setCreateMode,
    setLearnMode,

    // Module-based actions
    setCurrentModule,
    setActiveTab,
    getCurrentModule,
    getActiveTab,
    getTabsForModule,
    getModuleDefinition,
    updateTabAccessibility,

    // Creation method selector visibility
    get isCreationMethodSelectorVisible() {
      return isCreationMethodSelectorVisible;
    },
    setCreationMethodSelectorVisible(visible: boolean) {
      isCreationMethodSelectorVisible = visible;
    },

    // Legacy action aliases (deprecated)
    /** @deprecated Use setCreateMode instead */
    setBuildMode: setCreateMode,
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
