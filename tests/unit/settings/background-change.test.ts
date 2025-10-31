/**
 * Tests to demonstrate background change functionality issues
 *
 * This test suite verifies that selecting a background and clicking Apply
 * actually changes the background in the application.
 */

import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import { render, fireEvent, waitFor } from "@testing-library/svelte";
import "@testing-library/jest-dom";
import { BackgroundType } from "$lib/shared/background";

describe("Background Change Functionality", () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();

    // Clear any existing background classes/styles
    document.body.className = "";
    document.body.style.background = "";
    document.body.setAttribute("data-background", "");
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("should have starfield as the initial default background", () => {
    // Check localStorage for initial settings
    const storedSettings = localStorage.getItem("tka-modern-web-settings");

    if (storedSettings) {
      const parsed = JSON.parse(storedSettings);
      console.log("📦 Initial stored settings:", parsed);
      expect(parsed.backgroundType).toBeDefined();
    } else {
      console.log(
        "📦 No stored settings, using default: NIGHT_SKY (starfield)"
      );
    }

    // Check body element for background indicators
    const bodyBackground = document.body.getAttribute("data-background");
    const bodyClass = document.body.className;
    const bodyStyle = document.body.style.background;

    console.log("🎨 Body state:", {
      dataBackground: bodyBackground,
      className: bodyClass,
      style: bodyStyle,
    });
  });

  it("should demonstrate that selecting Aurora and clicking Apply does not change the background", async () => {
    // Import the necessary components
    const { updateBodyBackground } = await import("$lib/shared/background");
    const { updateSettings } = await import(
      "$lib/shared/application/state/app-state.svelte"
    );

    // Spy on the updateBodyBackground function
    const updateBodyBackgroundSpy = vi.fn(updateBodyBackground);

    console.log(
      "\n🔬 TEST: Simulating user selecting Aurora background and clicking Apply\n"
    );

    // Step 1: Get initial background
    const initialBackground = document.body.getAttribute("data-background");
    console.log("1️⃣ Initial background:", initialBackground || "none");

    // Step 2: Simulate user selecting Aurora in settings
    console.log("2️⃣ User selects Aurora (AURORA) background");
    const newSettings = {
      backgroundType: BackgroundType.AURORA,
      backgroundEnabled: true,
      backgroundQuality: "medium" as const,
    };

    // Step 3: Simulate clicking Apply button
    console.log("3️⃣ User clicks Apply button");
    await updateSettings(newSettings);

    // Step 4: Check if background actually changed
    await waitFor(() => {
      const currentBackground = document.body.getAttribute("data-background");
      console.log(
        "4️⃣ Current background after Apply:",
        currentBackground || "none"
      );

      // This assertion should fail if the background didn't change
      try {
        expect(currentBackground).toBe(BackgroundType.AURORA);
        console.log("✅ TEST PASSED: Background changed to Aurora");
      } catch (error) {
        console.log("❌ TEST FAILED: Background did NOT change to Aurora");
        console.log("   Expected:", BackgroundType.AURORA);
        console.log("   Actual:", currentBackground);
        throw error;
      }
    });
  });

  it("should demonstrate that updateBodyBackground function is called but body is not updated", async () => {
    const { updateBodyBackground } = await import("$lib/shared/background");

    console.log("\n🔬 TEST: Calling updateBodyBackground directly\n");

    // Step 1: Get initial state
    const initialBackground = document.body.getAttribute("data-background");
    const initialClass = document.body.className;
    console.log("1️⃣ Initial state:", {
      dataBackground: initialBackground,
      className: initialClass,
    });

    // Step 2: Call updateBodyBackground directly
    console.log("2️⃣ Calling updateBodyBackground(BackgroundType.AURORA)");
    updateBodyBackground(BackgroundType.AURORA);

    // Step 3: Check if body was updated
    await waitFor(() => {
      const newBackground = document.body.getAttribute("data-background");
      const newClass = document.body.className;

      console.log("3️⃣ After updateBodyBackground:", {
        dataBackground: newBackground,
        className: newClass,
      });

      // Check if background was updated
      try {
        expect(newBackground).toBe(BackgroundType.AURORA);
        console.log("✅ TEST PASSED: Body data-background attribute updated");
      } catch (error) {
        console.log(
          "❌ TEST FAILED: Body data-background attribute NOT updated"
        );
        console.log("   Expected:", BackgroundType.AURORA);
        console.log("   Actual:", newBackground);
        throw error;
      }
    });
  });

  it("should trace the complete flow from settings change to background update", async () => {
    const { updateSettings, getSettings } = await import(
      "$lib/shared/application/state/app-state.svelte"
    );
    const { updateBodyBackground } = await import("$lib/shared/background");

    console.log("\n🔬 TEST: Complete flow trace\n");

    // Step 1: Initial settings
    const initialSettings = getSettings();
    console.log("1️⃣ Initial settings:", initialSettings);

    // Step 2: Update settings to Deep Ocean
    console.log("2️⃣ Updating settings to DEEP_OCEAN background");
    await updateSettings({
      backgroundType: BackgroundType.DEEP_OCEAN,
      backgroundEnabled: true,
      backgroundQuality: "medium" as const,
    });

    // Step 3: Check if settings were updated
    const updatedSettings = getSettings();
    console.log("3️⃣ Updated settings:", updatedSettings);

    try {
      expect(updatedSettings.backgroundType).toBe(BackgroundType.DEEP_OCEAN);
      console.log("✅ Settings updated in state");
    } catch (error) {
      console.log("❌ Settings NOT updated in state");
      throw error;
    }

    // Step 4: Check localStorage
    const storedSettings = localStorage.getItem("tka-modern-web-settings");
    if (storedSettings) {
      const parsed = JSON.parse(storedSettings);
      console.log("4️⃣ Stored settings in localStorage:", parsed);

      try {
        expect(parsed.backgroundType).toBe(BackgroundType.DEEP_OCEAN);
        console.log("✅ Settings saved to localStorage");
      } catch (error) {
        console.log("❌ Settings NOT saved correctly to localStorage");
        throw error;
      }
    }

    // Step 5: Check body element
    await waitFor(() => {
      const bodyBackground = document.body.getAttribute("data-background");
      console.log("5️⃣ Body data-background:", bodyBackground);

      try {
        expect(bodyBackground).toBe(BackgroundType.DEEP_OCEAN);
        console.log("✅ TEST PASSED: Body background updated");
      } catch (error) {
        console.log("❌ TEST FAILED: Body background NOT updated");
        console.log(
          "   This is the root issue - updateBodyBackground is not being called or not working"
        );
        throw error;
      }
    });
  });

  it("should show that the MainApplication effect is not triggering on settings change", async () => {
    console.log("\n🔬 TEST: MainApplication reactive effect\n");

    const { updateSettings, getSettings } = await import(
      "$lib/shared/application/state/app-state.svelte"
    );

    // This test simulates what should happen in MainApplication.svelte
    // The $effect should watch settings.backgroundType and call updateBodyBackground

    console.log("1️⃣ Simulating MainApplication mounting...");

    // Initial background
    const initialSettings = getSettings();
    console.log("2️⃣ Initial backgroundType:", initialSettings.backgroundType);

    // Change background
    console.log("3️⃣ Changing background to AURORA...");
    await updateSettings({
      backgroundType: BackgroundType.AURORA,
    });

    const newSettings = getSettings();
    console.log(
      "4️⃣ New backgroundType in settings:",
      newSettings.backgroundType
    );

    // The issue: Even though settings changed, the $effect in MainApplication
    // might not be running, or updateBodyBackground might not be working
    const bodyBackground = document.body.getAttribute("data-background");
    console.log("5️⃣ Body background after change:", bodyBackground);

    console.log("\n❌ DIAGNOSIS:");
    console.log(
      "   - Settings state changed:",
      newSettings.backgroundType === BackgroundType.AURORA
    );
    console.log("   - Body updated:", bodyBackground === BackgroundType.AURORA);
    console.log(
      "   - Problem: The reactive effect or updateBodyBackground is not working"
    );
  });
});
