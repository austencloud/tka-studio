/**
 * Clear Firebase Cache Utility
 *
 * Clears all Firebase-related browser storage to fix authentication issues.
 * Use this when OAuth redirects are failing or auth state is corrupted.
 */

/**
 * Clears all Firebase-related storage from the browser
 * This includes:
 * - IndexedDB databases (firebaseLocalStorage, firestore)
 * - localStorage keys (firebase:*)
 * - sessionStorage keys (firebase:*)
 */
export async function clearAllFirebaseCache(): Promise<void> {
  console.log(
    "🧹 [Cache Clear] Starting comprehensive Firebase cache clear..."
  );

  const clearedItems: string[] = [];

  // ============================================================================
  // 1. Clear IndexedDB
  // ============================================================================
  try {
    const databases = await window.indexedDB.databases();
    console.log("📦 [Cache Clear] Found IndexedDB databases:", databases);

    for (const db of databases) {
      if (db.name) {
        // Delete Firebase and Firestore databases
        if (
          db.name.includes("firebase") ||
          db.name.includes("firestore") ||
          db.name.includes("the-kinetic")
        ) {
          const deleteRequest = window.indexedDB.deleteDatabase(db.name);

          await new Promise((resolve, reject) => {
            deleteRequest.onsuccess = () => {
              console.log(`✅ [Cache Clear] Deleted IndexedDB: ${db.name}`);
              clearedItems.push(`IndexedDB: ${db.name}`);
              resolve(null);
            };
            deleteRequest.onerror = () => {
              console.warn(
                `⚠️ [Cache Clear] Failed to delete IndexedDB: ${db.name}`
              );
              reject(deleteRequest.error);
            };
            deleteRequest.onblocked = () => {
              console.warn(`⚠️ [Cache Clear] Delete blocked for: ${db.name}`);
              // Resolve anyway - user may need to close tabs
              resolve(null);
            };
          }).catch((error) => {
            console.error(`❌ [Cache Clear] Error deleting ${db.name}:`, error);
          });
        }
      }
    }
  } catch (error) {
    console.error("❌ [Cache Clear] Error listing/deleting IndexedDB:", error);
  }

  // ============================================================================
  // 2. Clear localStorage
  // ============================================================================
  try {
    const localStorageKeys = Object.keys(localStorage);
    console.log("🗄️ [Cache Clear] localStorage keys:", localStorageKeys);

    const firebaseKeys = localStorageKeys.filter(
      (key) =>
        key.includes("firebase") ||
        key.includes("FIREBASE") ||
        key.includes("the-kinetic")
    );

    for (const key of firebaseKeys) {
      localStorage.removeItem(key);
      console.log(`✅ [Cache Clear] Removed localStorage: ${key}`);
      clearedItems.push(`localStorage: ${key}`);
    }
  } catch (error) {
    console.error("❌ [Cache Clear] Error clearing localStorage:", error);
  }

  // ============================================================================
  // 3. Clear sessionStorage
  // ============================================================================
  try {
    const sessionStorageKeys = Object.keys(sessionStorage);
    console.log("📋 [Cache Clear] sessionStorage keys:", sessionStorageKeys);

    const firebaseKeys = sessionStorageKeys.filter(
      (key) =>
        key.includes("firebase") ||
        key.includes("FIREBASE") ||
        key.includes("the-kinetic")
    );

    for (const key of firebaseKeys) {
      sessionStorage.removeItem(key);
      console.log(`✅ [Cache Clear] Removed sessionStorage: ${key}`);
      clearedItems.push(`sessionStorage: ${key}`);
    }
  } catch (error) {
    console.error("❌ [Cache Clear] Error clearing sessionStorage:", error);
  }

  // ============================================================================
  // 4. Summary
  // ============================================================================
  console.log("🎉 [Cache Clear] Cache clear complete!");
  console.log("📊 [Cache Clear] Cleared items:", clearedItems);

  if (clearedItems.length === 0) {
    console.log("ℹ️ [Cache Clear] No Firebase cache found to clear");
  }

  return;
}

/**
 * Call this before redirecting to Google sign-in for maximum reliability
 */
export async function clearCacheAndReload(): Promise<void> {
  await clearAllFirebaseCache();
  console.log("🔄 [Cache Clear] Reloading page in 1 second...");
  setTimeout(() => {
    window.location.reload();
  }, 1000);
}
