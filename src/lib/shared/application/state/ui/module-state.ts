import { browser } from "$app/environment";
import type { ModuleId } from "$shared";
import { authStore } from "../../../auth";
import { loadFeatureModule } from "../../../inversify/container";
import { getPersistenceService } from "../services.svelte";
import {
  getActiveModule,
  getActiveModuleOrDefault,
  setActiveModule,
  setIsTransitioning,
} from "./ui-state.svelte";

const LOCAL_STORAGE_KEY = "tka-active-module-cache";
const TRANSITION_RESET_DELAY = 300;

/**
 * Check if a module is accessible to the current user
 */
function isModuleAccessible(moduleId: ModuleId): boolean {
  // Admin module requires admin permissions
  if (moduleId === "admin") {
    return authStore.isAdmin;
  }

  // For non-admin users, only the Create module is accessible
  // All other modules are disabled/coming soon
  if (!authStore.isAdmin && moduleId !== "create") {
    return false;
  }

  // Admin users have access to all modules
  return true;
}

/**
 * Re-validate current module and section after auth state changes
 * Called when auth initializes to restore any cached module that user now has access to
 * Also validates that current section is accessible (e.g., guided mode requires admin)
 */
export async function revalidateCurrentModule(): Promise<void> {
  const currentModule = getActiveModule();

  // Try to restore any cached module that user now has access to
  if (authStore.isAdmin) {
    try {
      // Check localStorage FIRST (most recent user intent, survives even if Firestore was overwritten)
      const cached = browser ? localStorage.getItem(LOCAL_STORAGE_KEY) : null;
      if (cached) {
        try {
          const parsed = JSON.parse(cached);
          const cachedModuleId = parsed.moduleId as ModuleId;

          // Restore ANY module the user has access to (not just admin)
          if (cachedModuleId && isModuleAccessible(cachedModuleId) && currentModule !== cachedModuleId) {
            console.log(`📦 [module-state] Restoring cached module: ${cachedModuleId}`);

            // Load feature module BEFORE setting active module to ensure services are available
            await loadFeatureModule(cachedModuleId);

            setActiveModule(cachedModuleId);
            // Sync Firestore to match localStorage
            const persistence = getPersistenceService();
            await persistence.saveActiveTab(cachedModuleId);
            return;
          }
        } catch (e) {
          // Ignore parse errors
        }
      }

      // If localStorage doesn't have a valid module, check Firestore as fallback
      const persistence = getPersistenceService();
      const savedFromFirestore = await persistence.getActiveTab();

      // If Firestore has a module the user can access, restore it
      if (savedFromFirestore && isModuleAccessible(savedFromFirestore as ModuleId) && currentModule !== savedFromFirestore) {
        console.log(`📦 [module-state] Restoring module from Firestore: ${savedFromFirestore}`);

        // Load feature module BEFORE setting active module to ensure services are available
        await loadFeatureModule(savedFromFirestore);

        setActiveModule(savedFromFirestore as ModuleId);
        // Update localStorage to match
        if (browser) {
          localStorage.setItem(
            LOCAL_STORAGE_KEY,
            JSON.stringify({ moduleId: savedFromFirestore })
          );
        }
        return;
      }
    } catch (error) {
      console.warn(`⚠️ [module-state] Failed to revalidate module:`, error);
    }
  }

  // Validate current section accessibility (e.g., guided mode requires admin)
  if (currentModule === "create" && !authStore.isAdmin) {
    try {
      // Dynamic import to avoid circular dependency
      const { navigationState } = await import("../../../navigation/state/navigation-state.svelte");
      const currentSection = navigationState.activeTab;

      // If non-admin user is on assembler mode, redirect to constructor
      if (currentSection === "assembler") {
        console.warn("⚠️ [module-state] Non-admin user on assembler mode. Redirecting to constructor.");
        navigationState.setActiveTab("constructor");
      }
    } catch (error) {
      console.warn(`⚠️ [module-state] Failed to validate section:`, error);
    }
  }
}

export function getInitialModuleFromCache(): ModuleId {
  if (!browser) {
    return "create";
  }

  try {
    const savedModuleData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedModuleData) {
      const parsed = JSON.parse(savedModuleData);
      if (parsed && typeof parsed.moduleId === "string") {
        const moduleId = parsed.moduleId as ModuleId;
        // Return the cached module even if it's admin
        // If user doesn't have access, initializeModulePersistence will handle it
        return moduleId;
      }
    }
  } catch (error) {
    console.warn("⚠️ Failed to pre-load saved module from cache:", error);
  }

  return "create";
}

/**
 * Preload the cached module's services immediately to prevent UI flicker
 * This should be called as early as possible in the app lifecycle
 */
export function preloadCachedModuleServices(): void {
  if (!browser) return;

  try {
    const savedModuleData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedModuleData) {
      const parsed = JSON.parse(savedModuleData);
      if (parsed && typeof parsed.moduleId === "string") {
        const moduleId = parsed.moduleId as ModuleId;
        console.log(`⚡ [module-state] Preloading services for cached module: ${moduleId}`);

        // Start loading feature module immediately (non-blocking)
        // This prevents the UI flicker where it shows "create" first
        loadFeatureModule(moduleId).catch((error) => {
          console.warn(`⚠️ Failed to preload module services for "${moduleId}":`, error);
        });
      }
    }
  } catch (error) {
    console.warn("⚠️ Failed to preload cached module services:", error);
  }
}

export async function switchModule(module: ModuleId): Promise<void> {
  if (getActiveModule() === module) {
    return;
  }

  // Check if user has access to the module
  if (!isModuleAccessible(module)) {
    console.warn(`⚠️ switchModule: User does not have access to module "${module}"`);
    setIsTransitioning(false);
    return;
  }

  setIsTransitioning(true);

  try {
    // ⚡ PERFORMANCE: Load feature module on-demand (Tier 3)
    // Only loads the DI services needed for this specific tab
    await loadFeatureModule(module);

    setActiveModule(module);

    const persistence = getPersistenceService();
    await persistence.saveActiveTab(module);

    if (browser) {
      localStorage.setItem(
        LOCAL_STORAGE_KEY,
        JSON.stringify({ moduleId: module })
      );
    }
  } catch (error) {
    console.warn(
      "⚠️ switchModule: Failed to save module to persistence:",
      error
    );
  }

  setTimeout(() => {
    setIsTransitioning(false);
  }, TRANSITION_RESET_DELAY);
}

export function isModuleActive(module: string): boolean {
  return getActiveModule() === module;
}

export async function initializeModulePersistence(): Promise<void> {
  try {
    // Try localStorage FIRST (faster, synchronous)
    let savedModule: string | null = null;
    if (browser) {
      try {
        const cached = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (cached) {
          const parsed = JSON.parse(cached);
          savedModule = parsed.moduleId;
        }
      } catch (e) {
        // Ignore parse errors
      }
    }

    // Fallback to Firestore if not in localStorage
    if (!savedModule) {
      const persistence = getPersistenceService();
      await persistence.initialize();
      savedModule = await persistence.getActiveTab();
    }

    if (savedModule) {
      // Cast to ModuleId since we're checking if it's a valid module
      const moduleId = savedModule as ModuleId;

      // IMPORTANT: During initial load, skip access check because auth might not be ready yet
      // revalidateCurrentModule() will correct this after auth loads if needed

      // ⚡ CRITICAL: Load module services BEFORE setting activeModule
      // This prevents the UI from trying to render before services are ready
      await loadFeatureModule(moduleId);

      setActiveModule(moduleId);

      if (browser) {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify({ moduleId }));
      }
    } else {
      // No saved module
      const defaultModule = "create" as ModuleId;

      // Load default module's DI services
      await loadFeatureModule(defaultModule);

      setActiveModule(defaultModule);

      const persistence = getPersistenceService();
      await persistence.initialize();
      await persistence.saveActiveTab(defaultModule);
      if (browser) {
        localStorage.setItem(
          LOCAL_STORAGE_KEY,
          JSON.stringify({ moduleId: defaultModule })
        );
      }
    }
  } catch (error) {
    console.warn("⚠️ Failed to initialize module persistence:", error);
    // Fallback to create module on error
    try {
      await loadFeatureModule("create");
      setActiveModule("create");
    } catch (fallbackError) {
      console.error("❌ Failed to load fallback create module:", fallbackError);
    }
  }
}
