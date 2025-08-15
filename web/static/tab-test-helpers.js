// Tab State Testing Helper Script
// Run this in the browser console to help test and debug tab state restoration

// 1. Enable developer mode
function enableDeveloperMode() {
  const settings = JSON.parse(
    localStorage.getItem("tka-modern-web-settings") || "{}"
  );
  settings.developerMode = true;
  localStorage.setItem("tka-modern-web-settings", JSON.stringify(settings));
  console.log("✅ Developer mode enabled. Refresh the page to see all tabs.");
  return settings;
}

// 2. Check current tab state
function checkTabState() {
  const appTabState = localStorage.getItem("tka-app-tab-state");
  const settings = localStorage.getItem("tka-modern-web-settings");

  console.log("=== TAB STATE DEBUG ===");
  console.log("App Tab State:", appTabState ? JSON.parse(appTabState) : "none");
  console.log("Settings:", settings ? JSON.parse(settings) : "none");
  console.log(
    "Developer Mode:",
    settings ? JSON.parse(settings).developerMode : "default"
  );
}

// 3. Manually set tab state for testing
function setTabState(tabName) {
  const tabState = {
    activeTab: tabName,
    lastActiveTab: null,
    tabStates: {},
    lastUpdated: new Date().toISOString(),
  };
  localStorage.setItem("tka-app-tab-state", JSON.stringify(tabState));
  console.log(`✅ Tab state set to: ${tabName}. Refresh to test restoration.`);
}

// 4. Clear all state for fresh start
function clearAllState() {
  localStorage.removeItem("tka-app-tab-state");
  localStorage.removeItem("tka-modern-web-settings");
  console.log("🗑️ All state cleared. Refresh for fresh start.");
}

// Export functions to window for easy access
window.tabTestHelpers = {
  enableDeveloperMode,
  checkTabState,
  setTabState,
  clearAllState,
};

console.log("🔧 Tab testing helpers loaded! Use:");
console.log("- tabTestHelpers.enableDeveloperMode() - Enable dev mode");
console.log("- tabTestHelpers.checkTabState() - Check current state");
console.log(
  '- tabTestHelpers.setTabState("motion-tester") - Set tab to restore'
);
console.log("- tabTestHelpers.clearAllState() - Clear all state");
