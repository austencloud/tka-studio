import { test, expect } from "@playwright/test";

test("debug Generate tab", async ({ page }) => {
  // Navigate to the application
  await page.goto("/");

  // Wait for the application to load
  await page.waitForSelector(".main-layout-wrapper", {
    state: "visible",
    timeout: 30000,
  });

  // Take a screenshot of the initial page
  await page.screenshot({
    path: "test-results/initial-page.png",
    fullPage: true,
  });

  // Click on the Generate tab
  console.log("Clicking on Generate tab...");
  await page.click('button:has-text("Generate")');

  // Wait for the Generate tab to load
  await page.waitForTimeout(2000);

  // Take a screenshot of the Generate tab
  await page.screenshot({
    path: "test-results/generate-tab-debug.png",
    fullPage: true,
  });

  // Log all buttons on the page
  const buttons = await page.$$eval("button", (btns) => {
    return btns.map((btn) => ({
      text: btn.textContent?.trim(),
      classes: btn.className,
      isVisible: btn.offsetWidth > 0 && btn.offsetHeight > 0,
      rect: btn.getBoundingClientRect(),
    }));
  });

  console.log("Buttons on the page:", JSON.stringify(buttons, null, 2));

  // Look specifically for the generate button
  const generateButtons = await page.$$eval(".generate-button", (btns) => {
    return btns.map((btn) => ({
      text: btn.textContent?.trim(),
      classes: btn.className,
      isVisible: btn.offsetWidth > 0 && btn.offsetHeight > 0,
      rect: btn.getBoundingClientRect(),
    }));
  });

  console.log("Generate buttons:", JSON.stringify(generateButtons, null, 2));

  // Success if we've made it this far
  expect(true).toBeTruthy();
});
