import { test, expect } from "@playwright/test";

/**
 * This test is designed to explore the DOM structure of the application
 * to help us create more accurate selectors for our tests.
 */
test("explore DOM structure", async ({ page }) => {
  // Navigate to the application
  await page.goto("/");

  // Wait for the application to load
  await page.waitForSelector(".main-layout-wrapper", {
    state: "visible",
    timeout: 30000,
  });

  // Take a screenshot of the entire page
  await page.screenshot({ path: "test-results/full-page.png", fullPage: true });

  // Log the tab buttons that are available
  const tabButtons = await page.$$eval("button", (buttons) => {
    return buttons.map((button) => ({
      text: button.textContent?.trim(),
      classes: button.className,
      attributes: {
        "data-tab": button.getAttribute("data-tab"),
        "aria-label": button.getAttribute("aria-label"),
        title: button.getAttribute("title"),
        id: button.getAttribute("id"),
      },
    }));
  });

  console.log("Available buttons:", JSON.stringify(tabButtons, null, 2));

  // Try to find the menu bar
  const menuBar = await page.$(".menu-bar");
  if (menuBar) {
    console.log("Menu bar found");

    // Get all elements in the menu bar
    const menuItems = await menuBar.$$eval("*", (elements) => {
      return elements.map((el) => ({
        tag: el.tagName,
        classes: el.className,
        text: el.textContent?.trim(),
        attributes: {
          "data-tab": el.getAttribute("data-tab"),
          "aria-label": el.getAttribute("aria-label"),
          title: el.getAttribute("title"),
          id: el.getAttribute("id"),
        },
      }));
    });

    console.log("Menu bar items:", JSON.stringify(menuItems, null, 2));
  } else {
    console.log("Menu bar not found");
  }

  // Try to find any tab content
  const tabContents = await page.$$eval('[class*="-tab"]', (elements) => {
    return elements.map((el) => {
      // Check if the element is an HTMLElement before accessing offsetWidth and offsetHeight
      const isHtmlElement = el instanceof HTMLElement;
      return {
        classes: el.className,
        isVisible: isHtmlElement
          ? el.offsetWidth > 0 && el.offsetHeight > 0
          : true,
      };
    });
  });

  console.log("Tab contents:", JSON.stringify(tabContents, null, 2));

  // Click on the Generate tab
  console.log("Clicking on Generate tab...");
  await page.click('button:has-text("Generate")');

  // Wait for the Generate tab to load
  await page.waitForTimeout(2000);

  // Take a screenshot of the Generate tab
  await page.screenshot({
    path: "test-results/generate-tab.png",
    fullPage: true,
  });

  // Explore the Generate tab structure
  console.log("Exploring Generate tab structure...");
  const generateTabElements = await page.$$eval(
    '.generate-tab, [class*="generate-tab"] *',
    (elements) => {
      return elements.map((el) => ({
        tag: el.tagName,
        classes: el.className,
        text: el.textContent?.trim(),
        attributes: {
          "data-test": el.getAttribute("data-test"),
          "data-value": el.getAttribute("data-value"),
          "aria-label": el.getAttribute("aria-label"),
          id: el.getAttribute("id"),
        },
      }));
    },
  );

  console.log(
    "Generate tab elements:",
    JSON.stringify(generateTabElements, null, 2),
  );

  // Look specifically for the generator type selector
  console.log("Looking for generator type selector...");
  const generatorTypeElements = await page.$$eval(
    '.toggle-container, .toggle-track, .toggle-option, [data-test="generator-type-selector"]',
    (elements) => {
      return elements.map((el) => ({
        tag: el.tagName,
        classes: el.className,
        text: el.textContent?.trim(),
        attributes: {
          "data-test": el.getAttribute("data-test"),
          "data-value": el.getAttribute("data-value"),
          "aria-pressed": el.getAttribute("aria-pressed"),
          id: el.getAttribute("id"),
        },
      }));
    },
  );

  console.log(
    "Generator type elements:",
    JSON.stringify(generatorTypeElements, null, 2),
  );

  // Success if we've made it this far
  expect(true).toBeTruthy();
});
