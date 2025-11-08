/**
 * NUCLEAR CACHE CLEAR - Complete Firebase/Auth Storage Wipeout
 *
 * This utility COMPLETELY removes ALL Firebase-related storage.
 * Use this to fix auth issues caused by old cached data.
 */

export interface CacheDiagnostics {
  indexedDBDatabases: string[];
  localStorageKeys: string[];
  sessionStorageKeys: string[];
  cookies: string[];
}

/**
 * Diagnose what's currently in browser storage
 * This shows EXACTLY what databases and keys exist
 */
export async function diagnoseCacheState(): Promise<CacheDiagnostics> {
  const diagnostics: CacheDiagnostics = {
    indexedDBDatabases: [],
    localStorageKeys: [],
    sessionStorageKeys: [],
    cookies: [],
  };

  // 1. List ALL IndexedDB databases
  try {
    const databases = await window.indexedDB.databases();
    diagnostics.indexedDBDatabases = databases
      .map((db) => db.name || "unnamed")
      .filter(Boolean);

    console.log(
      "📦 [Cache Diagnostics] IndexedDB Databases:",
      diagnostics.indexedDBDatabases
    );
  } catch (error) {
    console.error("❌ [Cache Diagnostics] Failed to list IndexedDB:", error);
  }

  // 2. List ALL localStorage keys
  try {
    diagnostics.localStorageKeys = Object.keys(localStorage);
    console.log(
      "🗄️ [Cache Diagnostics] localStorage Keys:",
      diagnostics.localStorageKeys
    );
  } catch (error) {
    console.error("❌ [Cache Diagnostics] Failed to list localStorage:", error);
  }

  // 3. List ALL sessionStorage keys
  try {
    diagnostics.sessionStorageKeys = Object.keys(sessionStorage);
    console.log(
      "📋 [Cache Diagnostics] sessionStorage Keys:",
      diagnostics.sessionStorageKeys
    );
  } catch (error) {
    console.error(
      "❌ [Cache Diagnostics] Failed to list sessionStorage:",
      error
    );
  }

  // 4. List ALL cookies
  try {
    diagnostics.cookies = document.cookie
      .split(";")
      .map((c) => c.trim().split("=")[0] || "")
      .filter(Boolean) as string[];
    console.log("🍪 [Cache Diagnostics] Cookies:", diagnostics.cookies);
  } catch (error) {
    console.error("❌ [Cache Diagnostics] Failed to list cookies:", error);
  }

  // CRITICAL: Check for old project references
  const oldProjectReferences = {
    indexedDB: diagnostics.indexedDBDatabases.filter((db) =>
      db.includes("the-kinetic-constructor")
    ),
    localStorage: diagnostics.localStorageKeys.filter((key) =>
      localStorage.getItem(key)?.includes("the-kinetic-constructor")
    ),
  };

  if (
    oldProjectReferences.indexedDB.length > 0 ||
    oldProjectReferences.localStorage.length > 0
  ) {
    console.error("🚨 [Cache Diagnostics] OLD PROJECT DATA FOUND!");
    console.error("🚨 IndexedDB:", oldProjectReferences.indexedDB);
    console.error("🚨 localStorage:", oldProjectReferences.localStorage);
  }

  return diagnostics;
}

/**
 * NUCLEAR OPTION: Delete EVERYTHING Firebase/Auth related
 * This is the most aggressive cache clearing possible
 */
export async function nuclearCacheClear(): Promise<void> {
  console.log("💣 [NUCLEAR] Starting complete cache wipeout...");

  const deletedItems: string[] = [];
  const failedItems: string[] = [];

  // ============================================================================
  // 1. DELETE ALL INDEXEDDB DATABASES (not just Firebase ones)
  // ============================================================================
  try {
    const databases = await window.indexedDB.databases();
    console.log(`💣 [NUCLEAR] Found ${databases.length} IndexedDB databases`);

    for (const db of databases) {
      if (!db.name) continue;

      // Delete ALL databases (Firebase, Firestore, everything)
      try {
        await new Promise<void>((resolve, reject) => {
          const deleteRequest = window.indexedDB.deleteDatabase(db.name!);

          deleteRequest.onsuccess = () => {
            console.log(`✅ [NUCLEAR] Deleted IndexedDB: ${db.name}`);
            deletedItems.push(`IndexedDB: ${db.name}`);
            resolve();
          };

          deleteRequest.onerror = () => {
            console.error(
              `❌ [NUCLEAR] Failed to delete IndexedDB: ${db.name}`
            );
            failedItems.push(`IndexedDB: ${db.name}`);
            reject(deleteRequest.error);
          };

          deleteRequest.onblocked = () => {
            console.warn(
              `⚠️ [NUCLEAR] Delete blocked (close other tabs): ${db.name}`
            );
            // Resolve anyway - we'll retry on next load
            resolve();
          };
        });
      } catch (error) {
        console.error(`❌ [NUCLEAR] Error deleting ${db.name}:`, error);
        failedItems.push(`IndexedDB: ${db.name}`);
      }
    }
  } catch (error) {
    console.error("❌ [NUCLEAR] Failed to list IndexedDB databases:", error);
  }

  // ============================================================================
  // 2. CLEAR ALL LOCALSTORAGE
  // ============================================================================
  try {
    const keysBefore = Object.keys(localStorage);
    console.log(
      `💣 [NUCLEAR] Clearing ${keysBefore.length} localStorage items`
    );

    localStorage.clear();

    const keysAfter = Object.keys(localStorage);
    if (keysAfter.length === 0) {
      console.log("✅ [NUCLEAR] localStorage completely cleared");
      deletedItems.push(`localStorage: ${keysBefore.length} items`);
    } else {
      console.error(
        `⚠️ [NUCLEAR] localStorage still has ${keysAfter.length} items`
      );
      failedItems.push(`localStorage: ${keysAfter.length} items remaining`);
    }
  } catch (error) {
    console.error("❌ [NUCLEAR] Failed to clear localStorage:", error);
  }

  // ============================================================================
  // 3. CLEAR ALL SESSIONSTORAGE
  // ============================================================================
  try {
    const keysBefore = Object.keys(sessionStorage);
    console.log(
      `💣 [NUCLEAR] Clearing ${keysBefore.length} sessionStorage items`
    );

    sessionStorage.clear();

    const keysAfter = Object.keys(sessionStorage);
    if (keysAfter.length === 0) {
      console.log("✅ [NUCLEAR] sessionStorage completely cleared");
      deletedItems.push(`sessionStorage: ${keysBefore.length} items`);
    } else {
      console.error(
        `⚠️ [NUCLEAR] sessionStorage still has ${keysAfter.length} items`
      );
      failedItems.push(`sessionStorage: ${keysAfter.length} items remaining`);
    }
  } catch (error) {
    console.error("❌ [NUCLEAR] Failed to clear sessionStorage:", error);
  }

  // ============================================================================
  // 4. DELETE ALL COOKIES
  // ============================================================================
  try {
    const cookies = document.cookie.split(";");
    console.log(`💣 [NUCLEAR] Deleting ${cookies.length} cookies`);

    for (const cookie of cookies) {
      const cookieName = cookie.split("=")[0]?.trim();
      if (!cookieName) continue;
      // Delete for all possible domains and paths
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname};`;
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.${window.location.hostname};`;
      deletedItems.push(`Cookie: ${cookieName}`);
    }
    console.log("✅ [NUCLEAR] All cookies deleted");
  } catch (error) {
    console.error("❌ [NUCLEAR] Failed to delete cookies:", error);
  }

  // ============================================================================
  // 5. CLEAR CACHE STORAGE (Service Worker caches)
  // ============================================================================
  try {
    if ("caches" in window) {
      const cacheNames = await caches.keys();
      console.log(`💣 [NUCLEAR] Deleting ${cacheNames.length} cache storages`);

      for (const cacheName of cacheNames) {
        await caches.delete(cacheName);
        console.log(`✅ [NUCLEAR] Deleted cache: ${cacheName}`);
        deletedItems.push(`Cache: ${cacheName}`);
      }
    }
  } catch (error) {
    console.error("❌ [NUCLEAR] Failed to clear cache storage:", error);
  }

  // ============================================================================
  // SUMMARY
  // ============================================================================
  console.log("");
  console.log("🎉 [NUCLEAR] Cache wipeout complete!");
  console.log(`✅ Successfully deleted: ${deletedItems.length} items`);
  console.log(`❌ Failed to delete: ${failedItems.length} items`);

  if (failedItems.length > 0) {
    console.error("⚠️ [NUCLEAR] Failed items:", failedItems);
    console.error(
      "⚠️ You may need to close other tabs or restart your browser"
    );
  }

  // Verify the clear worked
  console.log("");
  console.log("🔍 [NUCLEAR] Verifying cache is clear...");
  const postClearDiagnostics = await diagnoseCacheState();

  const hasRemainingFirebaseData =
    postClearDiagnostics.indexedDBDatabases.some(
      (db) => db.includes("firebase") || db.includes("firestore")
    ) ||
    postClearDiagnostics.localStorageKeys.some(
      (key) => key.includes("firebase") || key.includes("firestore")
    );

  if (hasRemainingFirebaseData) {
    console.error(
      "🚨 [NUCLEAR] WARNING: Firebase data still present after clear!"
    );
    console.error("🚨 You MUST close all other tabs and restart the browser");
  } else {
    console.log("✅ [NUCLEAR] Verification passed - cache is clean!");
  }
}

/**
 * Show diagnostics in a user-friendly alert
 */
export async function showCacheDiagnostics(): Promise<void> {
  const diagnostics = await diagnoseCacheState();

  const message = `
📦 CACHE DIAGNOSTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IndexedDB Databases (${diagnostics.indexedDBDatabases.length}):
${diagnostics.indexedDBDatabases.map((db) => `  • ${db}`).join("\n") || "  (none)"}

localStorage Keys (${diagnostics.localStorageKeys.length}):
${diagnostics.localStorageKeys
  .slice(0, 10)
  .map((key) => `  • ${key}`)
  .join("\n")}
${diagnostics.localStorageKeys.length > 10 ? `  ... and ${diagnostics.localStorageKeys.length - 10} more` : ""}

sessionStorage Keys (${diagnostics.sessionStorageKeys.length}):
${diagnostics.sessionStorageKeys.map((key) => `  • ${key}`).join("\n") || "  (none)"}

Cookies (${diagnostics.cookies.length}):
${diagnostics.cookies
  .slice(0, 10)
  .map((c) => `  • ${c}`)
  .join("\n")}
${diagnostics.cookies.length > 10 ? `  ... and ${diagnostics.cookies.length - 10} more` : ""}
  `.trim();

  alert(message);
  console.log(message);
}
