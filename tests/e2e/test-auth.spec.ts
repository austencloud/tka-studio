import { test, expect } from "@playwright/test";

// Only run on chromium to avoid timeouts
test.use({ browserName: "chromium" });

// Increase test timeout
test.setTimeout(60000);

test("Google Sign-In Flow Test", async ({ page }) => {
  console.log("🧪 Starting Google sign-in test...");

  // Capture console logs from the start
  const logs: string[] = [];
  page.on("console", (msg) => {
    const text = msg.text();
    logs.push(text);
    if (
      text.includes("[google]") ||
      text.includes("[authStore]") ||
      text.includes("Clearing")
    ) {
      console.log("📋 BROWSER:", text);
    }
  });

  // Navigate to the app
  await page.goto("http://localhost:5173", { waitUntil: "domcontentloaded" });
  console.log("✅ Navigated to app");

  // Wait for app to load - look for main content
  await page.waitForTimeout(5000); // Give app time to initialize
  console.log("✅ Waited for initial load");

  // Take screenshot of initial state
  await page.screenshot({
    path: "test-screenshots/01-initial.png",
    fullPage: true,
  });
  console.log("📸 Screenshot: initial state");

  // Click the profile icon in the top right to reveal the user menu
  console.log("🔍 Clicking profile icon at top-right coordinates...");
  await page.mouse.click(1240, 27);
  console.log("✅ Clicked profile icon");

  // Wait for user menu to appear
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: "test-screenshots/02-user-menu.png",
    fullPage: true,
  });
  console.log("📸 Screenshot: user menu opened");

  // Click the "Sign In" button in the user menu to open the AuthSheet
  console.log('🔍 Looking for "Sign In" button in user menu...');
  const signInButton = page.getByRole("button", { name: "Sign In" }).last(); // Get the one in the menu (not the profile icon)
  await signInButton.click();
  console.log('✅ Clicked "Sign In" button');

  // Wait for AuthSheet to open
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: "test-screenshots/03-auth-sheet.png",
    fullPage: true,
  });
  console.log("📸 Screenshot: auth sheet opened");

  // Click the Google sign-in button
  console.log("🔍 Looking for Google button...");
  const googleButton = page.getByRole("button", { name: /google/i });
  await googleButton.click();
  console.log("✅ Clicked Google button");

  // Wait a moment for the redirect to start
  await page.waitForTimeout(3000);

  // Check current URL
  const currentUrl = page.url();
  console.log("🔍 Current URL after Google click:", currentUrl);

  // Check if we were redirected to Google
  if (currentUrl.includes("accounts.google.com")) {
    console.log("✅ Successfully redirected to Google!");
    await page.screenshot({
      path: "test-screenshots/03-google-auth.png",
      fullPage: true,
    });
    console.log("📸 Screenshot: Google auth page");
  } else if (currentUrl === "http://localhost:5173/") {
    console.log("❌ Still on localhost - redirect did not happen");
    await page.screenshot({
      path: "test-screenshots/03-redirect-failed.png",
      fullPage: true,
    });
    console.log("📸 Screenshot: redirect failed");
  } else {
    console.log("⚠️ Unexpected URL:", currentUrl);
    await page.screenshot({
      path: "test-screenshots/03-unexpected-url.png",
      fullPage: true,
    });
  }

  // Print summary
  console.log("\n=== TEST SUMMARY ===");
  console.log("Final URL:", page.url());
  console.log("Screenshots saved to test-screenshots/");
  console.log("\n=== ALL RELEVANT LOGS ===");
  logs
    .filter(
      (log) =>
        log.includes("[google]") ||
        log.includes("[authStore]") ||
        log.includes("Clearing") ||
        log.includes("Cache")
    )
    .forEach((log) => {
      console.log(log);
    });
});
