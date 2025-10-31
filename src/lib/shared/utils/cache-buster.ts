/**
 * Cache Buster - Nuclear option to clear all caches
 * Use this when the app gets stuck on white screen
 */

export async function clearAllCaches(): Promise<void> {
  if (typeof window === "undefined") return;

  console.log("🧹 Starting nuclear cache clear...");

  try {
    // 1. Clear Service Worker caches
    if ("caches" in window) {
      const cacheNames = await caches.keys();
      console.log(`Found ${cacheNames.length} caches to clear`);
      await Promise.all(cacheNames.map((name) => caches.delete(name)));
      console.log("✅ Service Worker caches cleared");
    }

    // 2. Unregister all service workers
    if ("serviceWorker" in navigator) {
      const registrations = await navigator.serviceWorker.getRegistrations();
      console.log(`Found ${registrations.length} service workers to unregister`);
      await Promise.all(registrations.map((reg) => reg.unregister()));
      console.log("✅ Service workers unregistered");
    }

    // 3. Clear IndexedDB (Dexie databases)
    if ("indexedDB" in window) {
      try {
        const databases = await indexedDB.databases();
        console.log(`Found ${databases.length} IndexedDB databases`);
        for (const db of databases) {
          if (db.name) {
            indexedDB.deleteDatabase(db.name);
            console.log(`Deleted database: ${db.name}`);
          }
        }
        console.log("✅ IndexedDB cleared");
      } catch (e) {
        console.warn("Could not enumerate IndexedDB databases:", e);
      }
    }

    // 4. Clear localStorage
    localStorage.clear();
    console.log("✅ localStorage cleared");

    // 5. Clear sessionStorage
    sessionStorage.clear();
    console.log("✅ sessionStorage cleared");

    console.log("🎉 All caches cleared! Reloading page...");

    // Wait a moment for operations to complete
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Force hard reload
    window.location.reload();
  } catch (error) {
    console.error("❌ Error clearing caches:", error);
  }
}

/**
 * Check if we should auto-clear cache on white screen
 */
export function checkAndClearIfBroken(): void {
  if (typeof window === "undefined") return;

  // Wait for page to load
  window.addEventListener("load", () => {
    setTimeout(() => {
      // Check if the page is still white (no meaningful content)
      const root = document.getElementById("app") || document.body;
      const hasContent =
        root.children.length > 0 &&
        root.querySelector("svg, img, button, input, canvas");

      if (!hasContent) {
        console.warn("⚠️ Page appears to be stuck on white screen!");
        console.warn("Auto-clearing caches in 2 seconds...");

        setTimeout(() => {
          clearAllCaches();
        }, 2000);
      }
    }, 1000);
  });
}

/**
 * Add keyboard shortcut to clear caches: Ctrl+Shift+Delete or Cmd+Shift+Delete
 */
export function registerCacheClearShortcut(): void {
  if (typeof window === "undefined") return;

  // Check for URL parameter to force cache clear
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("clear-cache")) {
    console.log("🔗 URL parameter detected: ?clear-cache");
    console.log("Auto-clearing caches...");
    clearAllCaches();
    return;
  }

  window.addEventListener("keydown", (e) => {
    // Ctrl+Shift+Delete (Windows/Linux) or Cmd+Shift+Delete (Mac)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "Delete") {
      e.preventDefault();
      console.log("🔑 Cache clear shortcut triggered!");

      const confirm = window.confirm(
        "Clear all caches and reload?\n\nThis will:\n- Clear service worker caches\n- Clear IndexedDB\n- Clear localStorage\n- Clear sessionStorage\n- Reload the page"
      );

      if (confirm) {
        clearAllCaches();
      }
    }
  });

  console.log("✨ Cache clear shortcut registered: Ctrl+Shift+Delete");
  console.log("💡 Or visit: http://localhost:5173/?clear-cache");
}
