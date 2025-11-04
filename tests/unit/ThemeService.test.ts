import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { ThemeService } from "../../src/lib/shared/theme/services/ThemeService";

describe("ThemeService", () => {
  let mockLocalStorage: Record<string, string> = {};
  let mockDocumentElement: any;
  let computedStyleValues: Record<string, string> = {};

  beforeEach(() => {
    // Mock localStorage
    mockLocalStorage = {};
    global.localStorage = {
      getItem: vi.fn((key: string) => mockLocalStorage[key] || null),
      setItem: vi.fn((key: string, value: string) => {
        mockLocalStorage[key] = value;
      }),
      removeItem: vi.fn((key: string) => {
        delete mockLocalStorage[key];
      }),
      clear: vi.fn(() => {
        mockLocalStorage = {};
      }),
      key: vi.fn(),
      length: 0,
    };

    // Mock document.documentElement with style property
    mockDocumentElement = {
      style: {
        setProperty: vi.fn(),
        getPropertyValue: vi.fn((prop: string) => computedStyleValues[prop] || ""),
      },
    };

    // Mock getComputedStyle
    global.getComputedStyle = vi.fn(() => ({
      getPropertyValue: (prop: string) => computedStyleValues[prop] || "",
    })) as any;

    Object.defineProperty(global, "document", {
      writable: true,
      value: {
        documentElement: mockDocumentElement,
      },
    });

    // Reset computed style values
    computedStyleValues = {};
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("getCurrentTheme", () => {
    it("should return default theme when no settings stored", () => {
      const theme = ThemeService.getCurrentTheme();
      expect(theme).toBe("nightSky");
    });

    it("should return stored theme from localStorage", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "aurora",
      });

      const theme = ThemeService.getCurrentTheme();
      expect(theme).toBe("aurora");
    });

    it("should return default theme when localStorage has invalid JSON", () => {
      mockLocalStorage["tka-modern-web-settings"] = "invalid json";

      const theme = ThemeService.getCurrentTheme();
      expect(theme).toBe("nightSky");
    });

    it("should return default theme when backgroundType is missing", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        someOtherSetting: "value",
      });

      const theme = ThemeService.getCurrentTheme();
      expect(theme).toBe("nightSky");
    });
  });

  describe("applyCurrentTheme", () => {
    beforeEach(() => {
      // Set up computed style values for all theme variables
      const backgrounds = ["nightSky", "aurora", "snowfall", "deepOcean"];
      const variables = [
        "dropdown-bg",
        "dropdown-text",
        "dropdown-description",
        "dropdown-hover",
        "dropdown-current",
        "header-bg",
        "header-border",
        "header-text",
        "panel-bg",
        "panel-border",
        "panel-hover",
        "card-bg",
        "card-border",
        "card-hover",
        "text-primary",
        "text-secondary",
        "input-bg",
        "input-border",
        "input-focus",
        "button-active",
      ];

      backgrounds.forEach((bg) => {
        variables.forEach((variable) => {
          const varName = `--${variable}-${bg}`;
          // Mock some distinct values for testing
          if (variable === "panel-bg" && bg === "aurora") {
            computedStyleValues[varName] = "rgba(20, 10, 40, 0.85)";
          } else if (variable === "card-bg" && bg === "aurora") {
            computedStyleValues[varName] = "rgba(25, 15, 45, 0.88)";
          } else {
            computedStyleValues[varName] = `test-value-${bg}-${variable}`;
          }
        });
      });
    });

    it("should apply nightSky theme by default", () => {
      ThemeService.applyCurrentTheme();

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--panel-bg-current",
        "test-value-nightSky-panel-bg"
      );
      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--card-bg-current",
        "test-value-nightSky-card-bg"
      );
    });

    it("should apply aurora theme when stored", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "aurora",
      });

      ThemeService.applyCurrentTheme();

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--panel-bg-current",
        "rgba(20, 10, 40, 0.85)"
      );
      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--card-bg-current",
        "rgba(25, 15, 45, 0.88)"
      );
    });

    it("should apply all 20 theme variables", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "aurora",
      });

      ThemeService.applyCurrentTheme();

      // Should have called setProperty for each of the 20 variables
      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledTimes(20);
    });

    it("should apply snowfall theme correctly", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "snowfall",
      });

      ThemeService.applyCurrentTheme();

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--panel-bg-current",
        "test-value-snowfall-panel-bg"
      );
    });

    it("should apply deepOcean theme correctly", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "deepOcean",
      });

      ThemeService.applyCurrentTheme();

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalledWith(
        "--panel-bg-current",
        "test-value-deepOcean-panel-bg"
      );
    });
  });

  describe("updateTheme", () => {
    beforeEach(() => {
      // Set up all computed styles needed for theme variables
      const backgrounds = ["nightSky", "aurora", "snowfall", "deepOcean"];
      const variables = [
        "dropdown-bg",
        "dropdown-text",
        "dropdown-description",
        "dropdown-hover",
        "dropdown-current",
        "header-bg",
        "header-border",
        "header-text",
        "panel-bg",
        "panel-border",
        "panel-hover",
        "card-bg",
        "card-border",
        "card-hover",
        "text-primary",
        "text-secondary",
        "input-bg",
        "input-border",
        "input-focus",
        "button-active",
      ];

      backgrounds.forEach((bg) => {
        variables.forEach((variable) => {
          computedStyleValues[`--${variable}-${bg}`] = `test-value-${bg}-${variable}`;
        });
      });
    });

    it("should trigger theme application", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "aurora",
      });

      ThemeService.updateTheme("aurora");

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalled();
    });

    it("should work regardless of parameter passed (uses localStorage)", () => {
      mockLocalStorage["tka-modern-web-settings"] = JSON.stringify({
        backgroundType: "snowfall",
      });

      // Even though we pass "aurora", it should use what's in localStorage
      ThemeService.updateTheme("aurora");

      expect(mockDocumentElement.style.setProperty).toHaveBeenCalled();
    });
  });

  describe("initialize", () => {
    beforeEach(() => {
      // Set up all computed styles needed for theme variables
      const backgrounds = ["nightSky", "aurora", "snowfall", "deepOcean"];
      const variables = [
        "dropdown-bg",
        "dropdown-text",
        "dropdown-description",
        "dropdown-hover",
        "dropdown-current",
        "header-bg",
        "header-border",
        "header-text",
        "panel-bg",
        "panel-border",
        "panel-hover",
        "card-bg",
        "card-border",
        "card-hover",
        "text-primary",
        "text-secondary",
        "input-bg",
        "input-border",
        "input-focus",
        "button-active",
      ];

      backgrounds.forEach((bg) => {
        variables.forEach((variable) => {
          computedStyleValues[`--${variable}-${bg}`] = `test-value-${bg}-${variable}`;
        });
      });
    });

    it("should apply theme on initialization", () => {
      const setPropertySpy = vi.spyOn(
        mockDocumentElement.style,
        "setProperty"
      );

      ThemeService.initialize();

      expect(setPropertySpy).toHaveBeenCalled();
    });

    it("should set up storage event listener", () => {
      const addEventListenerSpy = vi.spyOn(window, "addEventListener");

      ThemeService.initialize();

      expect(addEventListenerSpy).toHaveBeenCalledWith(
        "storage",
        expect.any(Function)
      );
    });
  });
});
