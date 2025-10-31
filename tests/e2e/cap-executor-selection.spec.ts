import { expect, test } from "@playwright/test";

test.describe("CAP Executor Selection - All 9 Variations", () => {
  // Increase timeout for these tests as they involve complex generation
  test.setTimeout(60000);

  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Use domcontentloaded instead of networkidle for faster/more reliable loading
    await page.waitForLoadState("domcontentloaded");

    // Wait for the Build button to be visible and ready
    await page
      .getByRole("button", { name: "Build" })
      .waitFor({ state: "visible" });
    await page.waitForTimeout(1000);

    // Navigate to Build tab and Generate sub-tab
    await page.getByRole("button", { name: "Build" }).click();
    await page.getByRole("button", { name: "Generate" }).click();
    await page.waitForTimeout(500);
  });

  // ===== STRICT TYPES (4 tests) =====

  test("should generate sequence with Strict Rotated CAP", async ({ page }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    // Click circular option
    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Click CAP Type card to open modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Verify only Rotated is selected (default)
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await expect(rotatedButton).toHaveClass(/selected/);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener to check for success
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Click generate button
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();

    // Wait for generation to complete
    await page.waitForTimeout(3000);

    // Check console logs for successful generation
    const successLog = consoleMessages.find(
      (msg) => msg.includes("Circular sequence complete") || msg.includes("🎉")
    );

    expect(successLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Strict Mirrored CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated, Select Mirrored
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    const mirroredButton = page.locator('button:has-text("Mirrored")').first();
    await mirroredButton.click();
    await page.waitForTimeout(200);

    // Verify Mirrored is selected
    await expect(mirroredButton).toHaveClass(/selected/);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];

    page.on("console", (msg) => {
      const text = msg.text();
      consoleMessages.push(text);
      if (msg.type() === "error") {
        errorMessages.push(text);
      }
    });

    // Click generate button
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();

    // Wait for generation
    await page.waitForTimeout(5000);

    // Check for successful generation
    const successLog = consoleMessages.find(
      (msg) => msg.includes("Circular sequence complete") || msg.includes("🎉")
    );

    const mirroredExecutorLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: strict_mirrored")
    );

    expect(mirroredExecutorLog).toBeTruthy();
    expect(successLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Strict Swapped CAP", async ({ page }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated, Select Swapped
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    const swappedButton = page.locator('button:has-text("Swapped")').first();
    await swappedButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    expect(successLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Strict Complementary CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated, Select Complementary
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    const complementaryButton = page
      .locator('button:has-text("Complementary")')
      .first();
    await complementaryButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    expect(successLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  // ===== COMBINATION TYPES (5 tests) =====

  test("should generate sequence with Mirrored + Swapped CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    // Select Mirrored
    const mirroredButton = page.locator('button:has-text("Mirrored")').first();
    await mirroredButton.click();
    await page.waitForTimeout(200);

    // Select Swapped
    const swappedButton = page.locator('button:has-text("Swapped")').first();
    await swappedButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    const mirroredSwappedLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: mirrored_swapped")
    );

    expect(successLog).toBeTruthy();
    expect(mirroredSwappedLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Swapped + Complementary CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    // Select Swapped
    const swappedButton = page.locator('button:has-text("Swapped")').first();
    await swappedButton.click();
    await page.waitForTimeout(200);

    // Select Complementary
    const complementaryButton = page
      .locator('button:has-text("Complementary")')
      .first();
    await complementaryButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    const swappedComplementaryLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: swapped_complementary")
    );

    expect(successLog).toBeTruthy();
    expect(swappedComplementaryLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Mirrored + Complementary CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Deselect Rotated
    const rotatedButton = page.locator('button:has-text("Rotated")').first();
    await rotatedButton.click();
    await page.waitForTimeout(200);

    // Select Mirrored
    const mirroredButton = page.locator('button:has-text("Mirrored")').first();
    await mirroredButton.click();
    await page.waitForTimeout(200);

    // Select Complementary
    const complementaryButton = page
      .locator('button:has-text("Complementary")')
      .first();
    await complementaryButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    const mirroredComplementaryLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: mirrored_complementary")
    );

    expect(successLog).toBeTruthy();
    expect(mirroredComplementaryLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Rotated + Swapped CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Rotated is already selected by default, just add Swapped
    const swappedButton = page.locator('button:has-text("Swapped")').first();
    await swappedButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    const rotatedSwappedLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: rotated_swapped")
    );

    expect(successLog).toBeTruthy();
    expect(rotatedSwappedLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });

  test("should generate sequence with Rotated + Complementary CAP", async ({
    page,
  }) => {
    // Set mode to circular
    const modeCard = page
      .locator(".card-settings-container")
      .locator("text=Mode")
      .first();
    await modeCard.click();
    await page.waitForTimeout(200);

    const circularButton = page.locator('button:has-text("Circular")');
    await circularButton.click();

    // Wait for CAP Type card to appear (it only shows in circular mode)
    const capCard = page.locator("text=CAP Type").first();
    await capCard.waitFor({ state: "visible", timeout: 10000 });
    await page.waitForTimeout(1000); // Extra wait for animations to settle

    // Open CAP Type modal (force: true to handle background animations)
    await capCard.click({ force: true });
    await page.waitForTimeout(300);

    // Rotated is already selected by default, just add Complementary
    const complementaryButton = page
      .locator('button:has-text("Complementary")')
      .first();
    await complementaryButton.click();
    await page.waitForTimeout(200);

    // Close modal
    await page.locator(".close-button").first().click();
    await page.waitForTimeout(200);

    // Set up console listener
    const consoleMessages: string[] = [];
    const errorMessages: string[] = [];
    page.on("console", (msg) => {
      consoleMessages.push(msg.text());
      if (msg.type() === "error") errorMessages.push(msg.text());
    });

    // Generate
    const generateButton = page
      .getByRole("button", { name: /Generate/i })
      .last();
    await generateButton.click();
    await page.waitForTimeout(5000);

    const successLog = consoleMessages.find((msg) =>
      msg.includes("Circular sequence complete")
    );

    const rotatedComplementaryLog = consoleMessages.find((msg) =>
      msg.includes("Using CAP executor: rotated_complementary")
    );

    expect(successLog).toBeTruthy();
    expect(rotatedComplementaryLog).toBeTruthy();
    expect(errorMessages.length).toBe(0);
  });
});
