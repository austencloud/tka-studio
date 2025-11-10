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
  // All other modules are accessible to everyone
  return true;
}

/**
 * Re-validate current module after auth state changes
 * Called when auth initializes to restore admin module if needed
 */
export async function revalidateCurrentModule(): Promise<void> {
  const currentModule = getActiveModule();

  // Try to restore admin module if user is now admin
  if (authStore.isAdmin && currentModule !== "admin") {
    try {
      // Check localStorage FIRST (most recent user intent, survives even if Firestore was overwritten)
      const cached = browser ? localStorage.getItem(LOCAL_STORAGE_KEY) : null;
      if (cached) {
        try {
          const parsed = JSON.parse(cached);
          if (parsed.moduleId === "admin") {
            setActiveModule("admin");
            // Sync Firestore to match localStorage
            const persistence = getPersistenceService();
            await persistence.saveActiveTab("admin");
            return;
          }
        } catch (e) {
          // Ignore parse errors
        }
      }

      // If localStorage doesn't have admin, check Firestore as fallback
      const persistence = getPersistenceService();
      const savedFromFirestore = await persistence.getActiveTab();

      // If Firestore has "admin", restore it
      if (savedFromFirestore === "admin") {
        setActiveModule("admin");
        // Update localStorage to match
        if (browser) {
          localStorage.setItem(
            LOCAL_STORAGE_KEY,
            JSON.stringify({ moduleId: "admin" })
          );
        }
        return;
      }
    } catch (error) {
      console.warn(`⚠️ [module-state] Failed to revalidate module:`, error);
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

export async function switchModule(module: ModuleId): Promise<void> {
  if (getActiveModule() === module) {
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
    const persistence = getPersistenceService();
    await persistence.initialize();

    const savedModule = await persistence.getActiveTab();

    if (savedModule) {
      // Cast to ModuleId since we're checking if it's a valid module
      const moduleId = savedModule as ModuleId;
      const hasAccess = isModuleAccessible(moduleId);

      if (hasAccess) {
        // Valid saved module that user has access to

        // ⚡ PERFORMANCE: Load initial module's DI services
        await loadFeatureModule(moduleId);

        setActiveModule(moduleId);
        if (browser) {
          localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify({ moduleId }));
        }
      } else {
        // User doesn't have access YET (auth might still be loading)
        // DON'T overwrite the cache - just use default temporarily
        // The cache will be restored by revalidateCurrentModule() when auth loads
        const defaultModule = getActiveModuleOrDefault();

        // Load default module's DI services
        await loadFeatureModule(defaultModule);

        setActiveModule(defaultModule);
        // DON'T save to persistence or localStorage - preserve the cached admin preference
      }
    } else {
      // No saved module
      const defaultModule = getActiveModuleOrDefault();

      // Load default module's DI services
      await loadFeatureModule(defaultModule);

      setActiveModule(defaultModule);
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
  }
}
