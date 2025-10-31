import { expect, test } from "@playwright/test";

test.describe("Generate Panel Card Layout", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Wait for the app to load
    await page.waitForSelector(".app-navigation-bar");

    // Navigate to Generate mode
    const buildTabContainer = page
      .locator(".nav-tab-container")
      .filter({ hasText: "Build" });
    await expect(buildTabContainer).toBeVisible();

    const dropdownTrigger = buildTabContainer.locator(".dropdown-trigger");
    await expect(dropdownTrigger).toBeVisible();
    await dropdownTrigger.click();

    const generateItem = page
      .locator(".dropdown-item")
      .filter({ hasText: "Generate" });
    await expect(generateItem).toBeVisible();
    await generateItem.click();

    // Wait for the Generate panel to be visible
    await page.waitForSelector(".generate-panel");
    await page.waitForSelector(".card-settings-container");
  });

  test("8-card scenario: SliceSize and CAP cards should span 3 columns each (Circular + Intermediate)", async ({
    page,
  }) => {
    // Set up the 8-card scenario: Circular mode + Intermediate level (or Advanced)
    // This should show all 8 cards:
    // 1. Level, 2. Length, 3. TurnIntensity, 4. GenerationMode,
    // 5. GridMode, 6. PropContinuity, 7. SliceSize, 8. CAP

    // First, ensure we're on Circular mode (Generation Mode card)
    const generationModeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Generation')"),
    });
    await generationModeCard.waitFor({ state: "visible" });

    // Click to ensure Circular mode is active (if not already)
    const circularOption = generationModeCard.locator(".toggle-option").filter({
      hasText: "Circular",
    });

    // Check if Circular is already active
    const isCircularActive = await circularOption.evaluate((el) =>
      el.classList.contains("active")
    );

    if (!isCircularActive) {
      await generationModeCard.click();
      await page.waitForTimeout(500); // Wait for animation
    }

    // Set level to Intermediate (level 2) or Advanced (level 3) to show Turn Intensity
    const levelCard = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Level')"),
    });
    await levelCard.waitFor({ state: "visible" });

    // Get current level value
    const levelValue = await levelCard.locator(".card-value").textContent();

    // If level is Beginner (1), click to increment to Intermediate (2)
    if (levelValue?.includes("Beginner")) {
      const incrementZone = levelCard.locator(".increment-zone");
      await incrementZone.click();
      await page.waitForTimeout(500); // Wait for Turn Intensity card to appear
    }

    // Verify all 8 cards are visible
    const levelCardVisible = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Level')"),
    });
    await expect(levelCardVisible).toBeVisible();

    const lengthCard = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Length')"),
    });
    await expect(lengthCard).toBeVisible();

    const turnIntensityCard = page.locator(".turn-intensity-card");
    await expect(turnIntensityCard).toBeVisible();

    await expect(generationModeCard).toBeVisible();

    const gridModeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Grid')"),
    });
    await expect(gridModeCard).toBeVisible();

    const propContinuityCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Continuity')"),
    });
    await expect(propContinuityCard).toBeVisible();

    const sliceSizeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Slice')"),
    });
    await expect(sliceSizeCard).toBeVisible();

    const capCard = page.locator(".base-card").filter({
      has: page.locator(".card-title:has-text('CAP')"),
    });
    await expect(capCard).toBeVisible();

    // CRITICAL TEST: Verify SliceSize and CAP cards span 3 columns
    const sliceSpan = await sliceSizeCard.evaluate((el) => {
      const style = window.getComputedStyle(el);
      const gridColumn = style.gridColumn;
      // Should be "span 3" or "auto / span 3"
      return gridColumn;
    });
    expect(sliceSpan).toContain("span 3");

    const capSpan = await capCard.evaluate((el) => {
      const style = window.getComputedStyle(el);
      const gridColumn = style.gridColumn;
      return gridColumn;
    });
    expect(capSpan).toContain("span 3");

    // Verify that Level, Length, and TurnIntensity span 2 columns (default)
    const levelSpan = await levelCardVisible.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.gridColumn;
    });
    expect(levelSpan).toContain("span 2");
  });

  test("7-card scenario: CAP should span full width (6 columns) when alone in row (Circular + Beginner)", async ({
    page,
  }) => {
    // This scenario has 7 cards (no Turn Intensity because level is Beginner)
    // CAP card is alone in row 3 and should span full width (6 columns)

    // Ensure Circular mode
    const generationModeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Generation')"),
    });
    const circularOption = generationModeCard.locator(".toggle-option").filter({
      hasText: "Circular",
    });
    const isCircularActive = await circularOption.evaluate((el) =>
      el.classList.contains("active")
    );
    if (!isCircularActive) {
      await generationModeCard.click();
      await page.waitForTimeout(500);
    }

    // Set level to Beginner (level 1)
    const levelCard = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Level')"),
    });
    const levelValue = await levelCard.locator(".card-value").textContent();

    // Click decrement until we reach Beginner
    while (!levelValue?.includes("Beginner")) {
      const decrementZone = levelCard.locator(".decrement-zone");
      await decrementZone.click();
      await page.waitForTimeout(300);

      const newValue = await levelCard.locator(".card-value").textContent();
      if (newValue?.includes("Beginner")) break;
    }

    // Verify Turn Intensity is NOT visible
    const turnIntensityCard = page.locator(".turn-intensity-card");
    await expect(turnIntensityCard).not.toBeVisible();

    // Verify 7 cards total are visible
    const allCards = page.locator(".card-settings-container > *");
    const cardCount = await allCards.count();
    expect(cardCount).toBe(7);

    // Verify SliceSize uses default 2-column span
    const sliceSizeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Slice')"),
    });
    await expect(sliceSizeCard).toBeVisible();

    const sliceSpan = await sliceSizeCard.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.gridColumn;
    });
    expect(sliceSpan).toContain("span 2");

    // CRITICAL TEST: Verify CAP spans full width (6 columns)
    const capCard = page.locator(".base-card").filter({
      has: page.locator(".card-title:has-text('CAP')"),
    });
    await expect(capCard).toBeVisible();

    const capSpan = await capCard.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.gridColumn;
    });
    expect(capSpan).toContain("span 6");
  });

  test("5-card scenario: Freeform + Beginner (no SliceSize, CAP, or TurnIntensity)", async ({
    page,
  }) => {
    // This scenario has only 5 base cards

    // Set to Freeform mode
    const generationModeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Generation')"),
    });
    const freeformOption = generationModeCard
      .locator(".toggle-option")
      .filter({ hasText: "Freeform" });
    const isFreeformActive = await freeformOption.evaluate((el) =>
      el.classList.contains("active")
    );
    if (!isFreeformActive) {
      await generationModeCard.click();
      await page.waitForTimeout(500);
    }

    // Set level to Beginner
    const levelCard = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Level')"),
    });
    const levelValue = await levelCard.locator(".card-value").textContent();
    while (!levelValue?.includes("Beginner")) {
      const decrementZone = levelCard.locator(".decrement-zone");
      await decrementZone.click();
      await page.waitForTimeout(300);
      const newValue = await levelCard.locator(".card-value").textContent();
      if (newValue?.includes("Beginner")) break;
    }

    // Verify only 5 cards are visible
    const allCards = page.locator(".card-settings-container > *");
    const cardCount = await allCards.count();
    expect(cardCount).toBe(5);

    // Verify SliceSize, CAP, and TurnIntensity are NOT visible
    const sliceSizeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Slice')"),
    });
    await expect(sliceSizeCard).not.toBeVisible();

    const capCard = page.locator(".base-card").filter({
      has: page.locator(".card-title:has-text('CAP')"),
    });
    await expect(capCard).not.toBeVisible();

    const turnIntensityCard = page.locator(".turn-intensity-card");
    await expect(turnIntensityCard).not.toBeVisible();
  });

  test("6-card scenario: Freeform + Advanced (shows TurnIntensity, no SliceSize/CAP)", async ({
    page,
  }) => {
    // Set to Freeform mode
    const generationModeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Generation')"),
    });
    const freeformOption = generationModeCard
      .locator(".toggle-option")
      .filter({ hasText: "Freeform" });
    const isFreeformActive = await freeformOption.evaluate((el) =>
      el.classList.contains("active")
    );
    if (!isFreeformActive) {
      await generationModeCard.click();
      await page.waitForTimeout(500);
    }

    // Set level to Advanced (level 3)
    const levelCard = page.locator(".stepper-card").filter({
      has: page.locator(".card-title:has-text('Level')"),
    });
    const levelValue = await levelCard.locator(".card-value").textContent();

    // Click increment until we reach Advanced
    while (!levelValue?.includes("Advanced")) {
      const incrementZone = levelCard.locator(".increment-zone");
      await incrementZone.click();
      await page.waitForTimeout(300);
      const newValue = await levelCard.locator(".card-value").textContent();
      if (newValue?.includes("Advanced")) break;
    }

    // Verify Turn Intensity IS visible
    const turnIntensityCard = page.locator(".turn-intensity-card");
    await expect(turnIntensityCard).toBeVisible();

    // Verify SliceSize and CAP are NOT visible
    const sliceSizeCard = page.locator(".toggle-card").filter({
      has: page.locator(".card-title:has-text('Slice')"),
    });
    await expect(sliceSizeCard).not.toBeVisible();

    const capCard = page.locator(".base-card").filter({
      has: page.locator(".card-title:has-text('CAP')"),
    });
    await expect(capCard).not.toBeVisible();

    // Verify total card count is 6 (accounting for TurnIntensity appearance)
    // Base 5 + TurnIntensity = 6 cards total
    const allCards = page.locator(".card-settings-container > *");
    const cardCount = await allCards.count();
    expect(cardCount).toBe(6);
  });
});
