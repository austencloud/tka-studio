/**
 * DEBUG TEST: Systematic investigation of white screen on DevTools refresh
 *
 * This test systematically captures everything that happens when:
 * 1. Opening the app normally (baseline)
 * 2. Opening the app with DevTools already open
 * 3. Refreshing with DevTools open (the failing scenario)
 */

import { test, expect } from "@playwright/test";

test.describe("DevTools Refresh White Screen Investigation", () => {
  test("Scenario 1: Normal load (baseline)", async ({ page }) => {
    const consoleMessages: string[] = [];
    const errors: string[] = [];
    const warnings: string[] = [];

    // Capture all console output
    page.on("console", (msg) => {
      const text = `[${msg.type()}] ${msg.text()}`;
      consoleMessages.push(text);
      if (msg.type() === "error") errors.push(text);
      if (msg.type() === "warning") warnings.push(text);
    });

    // Capture page errors
    page.on("pageerror", (error) => {
      errors.push(`[PAGE ERROR] ${error.message}\n${error.stack}`);
    });

    console.log("\n========== SCENARIO 1: NORMAL LOAD ==========");
    console.log("Starting normal load without DevTools...");

    await page.goto("http://localhost:5173");

    // Wait for app to initialize
    await page.waitForTimeout(3000);

    console.log("\n--- Console Messages ---");
    consoleMessages.forEach((msg) => console.log(msg));

    console.log("\n--- Errors ---");
    if (errors.length === 0) {
      console.log("✅ No errors");
    } else {
      errors.forEach((err) => console.log(err));
    }

    console.log("\n--- Warnings ---");
    if (warnings.length === 0) {
      console.log("✅ No warnings");
    } else {
      warnings.forEach((warn) => console.log(warn));
    }

    // Check if app loaded
    const hasContent = (await page.locator(".tka-app").count()) > 0;
    console.log(`\nApp loaded: ${hasContent ? "✅" : "❌"}`);

    await page.screenshot({
      path: "debug-scenario-1-normal-load.png",
      fullPage: true,
    });
    console.log("Screenshot saved: debug-scenario-1-normal-load.png");
  });

  test("Scenario 2: Load with DevTools open from start", async ({
    page,
    context,
  }) => {
    const consoleMessages: string[] = [];
    const errors: string[] = [];
    const warnings: string[] = [];

    page.on("console", (msg) => {
      const text = `[${msg.type()}] ${msg.text()}`;
      consoleMessages.push(text);
      if (msg.type() === "error") errors.push(text);
      if (msg.type() === "warning") warnings.push(text);
    });

    page.on("pageerror", (error) => {
      errors.push(`[PAGE ERROR] ${error.message}\n${error.stack}`);
    });

    console.log("\n========== SCENARIO 2: LOAD WITH DEVTOOLS OPEN ==========");

    // Create a new page with DevTools-like properties
    const cdpSession = await context.newCDPSession(page);

    console.log("Navigating with DevTools session active...");
    await page.goto("http://localhost:5173");

    // Wait for app to initialize
    await page.waitForTimeout(3000);

    console.log("\n--- Console Messages ---");
    consoleMessages.forEach((msg) => console.log(msg));

    console.log("\n--- Errors ---");
    if (errors.length === 0) {
      console.log("✅ No errors");
    } else {
      errors.forEach((err) => console.log(err));
    }

    console.log("\n--- Warnings ---");
    if (warnings.length === 0) {
      console.log("✅ No warnings");
    } else {
      warnings.forEach((warn) => console.log(warn));
    }

    const hasContent = (await page.locator(".tka-app").count()) > 0;
    console.log(`\nApp loaded: ${hasContent ? "✅" : "❌"}`);

    await page.screenshot({
      path: "debug-scenario-2-devtools-open.png",
      fullPage: true,
    });
    console.log("Screenshot saved: debug-scenario-2-devtools-open.png");
  });

  test("Scenario 3: Refresh with DevTools open (FAILING CASE)", async ({
    page,
    context,
  }) => {
    const consoleMessages: string[] = [];
    const errors: string[] = [];
    const warnings: string[] = [];
    const networkRequests: string[] = [];

    page.on("console", (msg) => {
      const text = `[${msg.type()}] ${msg.text()}`;
      consoleMessages.push(text);
      if (msg.type() === "error") errors.push(text);
      if (msg.type() === "warning") warnings.push(text);
    });

    page.on("pageerror", (error) => {
      errors.push(`[PAGE ERROR] ${error.message}\n${error.stack}`);
    });

    page.on("request", (request) => {
      networkRequests.push(`${request.method()} ${request.url()}`);
    });

    console.log(
      "\n========== SCENARIO 3: REFRESH WITH DEVTOOLS OPEN (FAILING) =========="
    );

    // Create CDP session to simulate DevTools being open
    const cdpSession = await context.newCDPSession(page);

    console.log("Initial load...");
    await page.goto("http://localhost:5173");
    await page.waitForTimeout(2000);

    console.log("Clearing captured data for refresh...");
    consoleMessages.length = 0;
    errors.length = 0;
    warnings.length = 0;
    networkRequests.length = 0;

    console.log("REFRESHING PAGE (with DevTools session active)...");
    await page.reload({ waitUntil: "domcontentloaded" });

    // Wait to see what happens
    await page.waitForTimeout(5000);

    console.log("\n--- Console Messages After Refresh ---");
    if (consoleMessages.length === 0) {
      console.log("⚠️ NO CONSOLE OUTPUT - This might be the issue!");
    } else {
      consoleMessages.forEach((msg) => console.log(msg));
    }

    console.log("\n--- Errors After Refresh ---");
    if (errors.length === 0) {
      console.log("No errors logged (but app might be stuck)");
    } else {
      errors.forEach((err) => console.log(err));
    }

    console.log("\n--- Network Requests After Refresh ---");
    networkRequests.forEach((req) => console.log(req));

    // Check various page states
    const hasContent = (await page.locator(".tka-app").count()) > 0;
    const hasLoadingScreen = (await page.locator(".error-screen").count()) > 0;
    const bodyText = await page.textContent("body");

    console.log("\n--- Page State ---");
    console.log(`Has .tka-app element: ${hasContent ? "✅" : "❌"}`);
    console.log(`Has loading/error screen: ${hasLoadingScreen ? "✅" : "❌"}`);
    console.log(`Body text content: "${bodyText?.trim() || "(empty)"}"`);
    console.log(`Body text length: ${bodyText?.length || 0} characters`);

    // Check if page is completely white
    if (!bodyText || bodyText.trim().length === 0) {
      console.log("🚨 CONFIRMED: Page is completely white/empty");
    }

    await page.screenshot({
      path: "debug-scenario-3-refresh-failing.png",
      fullPage: true,
    });
    console.log("Screenshot saved: debug-scenario-3-refresh-failing.png");

    // Try to evaluate some JavaScript to see if modules loaded
    try {
      const windowInfo = await page.evaluate(() => {
        return {
          hasVite: typeof window !== "undefined" && "__vite__" in window,
          hasSvelte: typeof window !== "undefined" && "__svelte" in window,
          documentReadyState: document.readyState,
          scriptsLoaded: document.scripts.length,
          stylesheetsLoaded: document.styleSheets.length,
        };
      });
      console.log("\n--- Window State ---");
      console.log(JSON.stringify(windowInfo, null, 2));
    } catch (err) {
      console.log("❌ Could not evaluate window state:", err);
    }
  });
});
