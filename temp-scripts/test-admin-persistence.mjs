/**
 * Test Admin Module Persistence
 *
 * This script tests whether the admin module is properly restored after a page refresh.
 */

import { chromium } from "playwright";

async function testAdminPersistence() {
  console.log("🧪 Starting Admin Module Persistence Test...\n");

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Capture console logs
  const logs = [];
  page.on("console", (msg) => {
    const text = msg.text();
    logs.push(text);

    // Filter for relevant logs
    if (
      text.includes("[module-state]") ||
      text.includes("[authStore]") ||
      text.includes("Admin")
    ) {
      console.log("📋", text);
    }
  });

  try {
    console.log("1️⃣ Navigating to app...");
    await page.goto("http://localhost:5173", { waitUntil: "networkidle" });

    // Wait for auth to load
    console.log("\n2️⃣ Waiting for auth to initialize...");
    await page.waitForFunction(
      () => {
        return window.localStorage.getItem("tka-active-module-cache") !== null;
      },
      { timeout: 10000 }
    );

    await page.waitForTimeout(2000); // Wait for auth detection

    // Debug: List all visible buttons
    const visibleButtons = await page.evaluate(() => {
      const buttons = Array.from(
        document.querySelectorAll("button, .nav-button, .nav-item")
      );
      return buttons
        .filter((btn) => btn.offsetParent !== null) // Only visible elements
        .map((btn) => ({
          text: btn.textContent?.trim().substring(0, 50),
          ariaLabel: btn.getAttribute("aria-label"),
          className: btn.className,
          id: btn.id,
        }))
        .slice(0, 20); // First 20 buttons
    });
    console.log(
      "\n🔍 Visible buttons on page:",
      JSON.stringify(visibleButtons, null, 2)
    );

    // Check current module
    const currentModuleBefore = await page.evaluate(() => {
      return localStorage.getItem("tka-active-module-cache");
    });
    console.log("\n📊 Current module (before):", currentModuleBefore);

    // Check Firestore saved module
    const firestoreSaved = await page.evaluate(async () => {
      const db = window.indexedDB;
      return new Promise((resolve) => {
        const request = db.open("firebaseLocalStorageDb");
        request.onsuccess = (event) => {
          const database = event.target.result;
          const transaction = database.transaction(
            ["firebaseLocalStorage"],
            "readonly"
          );
          const store = transaction.objectStore("firebaseLocalStorage");
          const getRequest = store.get("tka-active-tab");

          getRequest.onsuccess = () => {
            resolve(getRequest.result ? getRequest.result.value : null);
          };
          getRequest.onerror = () => resolve(null);
        };
        request.onerror = () => resolve(null);
      });
    });
    console.log("📊 Firestore saved module:", firestoreSaved);

    // Navigate to admin module
    console.log("\n3️⃣ Opening module menu and clicking admin...");

    // First, click the "Menu" button to open the unified navigation menu
    try {
      await page.click('button[aria-label="Switch module"]', { timeout: 5000 });
      console.log("✅ Opened unified menu");
      await page.waitForTimeout(500); // Wait for menu animation
    } catch (e) {
      console.log(
        "⚠️ Could not find menu button, trying alternative selectors"
      );
      await page.click(".module-switcher", { timeout: 5000 });
    }

    // Now click the Admin module item in the menu
    try {
      // The admin module should be in the "Developer Tools" section
      await page.click('button.module-item:has-text("Admin")', {
        timeout: 5000,
      });
      console.log("✅ Clicked Admin module in menu");
    } catch (e) {
      console.log("⚠️ Could not find Admin in menu, trying direct click");
      await page.evaluate(() => {
        const moduleItems = Array.from(
          document.querySelectorAll(".module-item")
        );
        const adminItem = moduleItems.find(
          (item) =>
            item.textContent?.includes("Admin") ||
            item.querySelector('[class*="crown"]')
        );
        if (adminItem) {
          adminItem.click();
        }
      });
    }

    await page.waitForTimeout(1000);

    // Verify we're on admin
    const onAdminBefore = await page.evaluate(() => {
      return (
        window.location.href.includes("admin") ||
        document.querySelector('.admin-dashboard, [class*="admin"]') !== null
      );
    });
    console.log("✅ On admin module:", onAdminBefore);

    // Refresh the page
    console.log("\n4️⃣ Refreshing page...");
    await page.reload({ waitUntil: "domcontentloaded" }); // Don't wait for networkidle due to Firebase permission errors

    // Wait for auth and module restoration
    await page.waitForTimeout(3000);

    // Check final state
    console.log("\n5️⃣ Checking final state...");

    const currentModuleAfter = await page.evaluate(() => {
      return localStorage.getItem("tka-active-module-cache");
    });
    console.log("📊 Current module (after refresh):", currentModuleAfter);

    const onAdminAfter = await page.evaluate(() => {
      return (
        window.location.href.includes("admin") ||
        document.querySelector('.admin-dashboard, [class*="admin"]') !== null
      );
    });

    // Extract relevant logs
    console.log("\n📜 Relevant Console Logs:");
    console.log("=".repeat(80));
    const relevantLogs = logs.filter(
      (log) =>
        log.includes("module-state") ||
        log.includes("Admin user") ||
        log.includes("Revalidating")
    );
    relevantLogs.forEach((log) => console.log(log));
    console.log("=".repeat(80));

    // Final result
    console.log("\n🎯 TEST RESULT:");
    if (onAdminAfter) {
      console.log(
        "✅ SUCCESS: Admin module was properly restored after refresh!"
      );
    } else {
      console.log("❌ FAILURE: Admin module was NOT restored after refresh");
      console.log("   Expected: admin module");
      console.log("   Got:", currentModuleAfter);
    }

    await page.waitForTimeout(2000);
  } catch (error) {
    console.error("\n❌ Test Error:", error);
  } finally {
    await browser.close();
  }
}

testAdminPersistence().catch(console.error);
