/**
 * Visibility State Manager - Modern Web Implementation
 *
 * Replicates the sophisticated visibility system from the legacy desktop app.
 * Manages complex dependencies between motion visibility and dependent glyphs.
 */

import type { AppSettings } from "$domain";
import { MotionColor } from "$domain";

type VisibilityObserver = () => void;

type VisibilityCategory = "glyph" | "motion" | "non_radial" | "all" | "buttons";

interface VisibilitySettings {
  // Motion visibility (independent)
  red_motion: boolean;
  blue_motion: boolean;

  // Independent glyphs
  Reversals: boolean;

  // Dependent glyphs (only available when both motions are visible)
  TKA: boolean;
  VTG: boolean;
  Elemental: boolean;
  Positions: boolean;

  // Grid elements
  nonRadialPoints: boolean;
}

export class VisibilityStateManager {
  private settings: VisibilitySettings;
  private observers: Map<VisibilityCategory, Set<VisibilityObserver>> =
    new Map();

  // Dependent glyphs that require both motions to be visible
  private readonly DEPENDENT_GLYPHS = ["TKA", "VTG", "Elemental", "Positions"];

  constructor(initialSettings?: Partial<AppSettings>) {
    // Initialize with defaults matching desktop app
    this.settings = {
      // Motion defaults - both visible
      red_motion: true,
      blue_motion: true,

      // Independent glyph defaults
      Reversals: true,

      // Dependent glyph defaults
      TKA: true,
      VTG: false,
      Elemental: false,
      Positions: false,

      // Grid defaults
      nonRadialPoints: false,

      // Override with any provided settings
      ...this.convertAppSettingsToVisibility(initialSettings),
    };

    // Initialize observer categories
    this.observers.set("glyph", new Set());
    this.observers.set("motion", new Set());
    this.observers.set("non_radial", new Set());
    this.observers.set("all", new Set());
    this.observers.set("buttons", new Set());
  }

  /**
   * Convert AppSettings visibility format to internal format
   */
  private convertAppSettingsToVisibility(
    appSettings?: Partial<AppSettings>
  ): Partial<VisibilitySettings> {
    if (!appSettings?.visibility) return {};

    return {
      TKA: appSettings.visibility.TKA,
      Reversals: appSettings.visibility.Reversals,
      VTG: appSettings.visibility.VTG,
      Elemental: appSettings.visibility.Elemental,
      Positions: appSettings.visibility.Positions,
      nonRadialPoints: appSettings.visibility.nonRadialPoints,
    };
  }

  /**
   * Convert internal visibility format to AppSettings format
   */
  public toAppSettings(): AppSettings["visibility"] {
    return {
      TKA: this.settings.TKA,
      Reversals: this.settings.Reversals,
      VTG: this.settings.VTG,
      Elemental: this.settings.Elemental,
      Positions: this.settings.Positions,
      nonRadialPoints: this.settings.nonRadialPoints,
    };
  }

  /**
   * Register an observer for visibility changes
   */
  registerObserver(
    callback: VisibilityObserver,
    categories: VisibilityCategory[] = ["all"]
  ): void {
    categories.forEach((category) => {
      if (!this.observers.has(category)) {
        this.observers.set(category, new Set());
      }
      const categoryObservers = this.observers.get(category);
      if (categoryObservers) {
        categoryObservers.add(callback);
      }
    });
  }

  /**
   * Unregister an observer
   */
  unregisterObserver(callback: VisibilityObserver): void {
    this.observers.forEach((observerSet) => {
      observerSet.delete(callback);
    });
  }

  /**
   * Notify observers of changes
   */
  private notifyObservers(categories: VisibilityCategory[]): void {
    const callbacksToNotify = new Set<VisibilityObserver>();

    // Collect callbacks from specific categories
    categories.forEach((category) => {
      const observers = this.observers.get(category);
      if (observers) {
        observers.forEach((callback) => callbacksToNotify.add(callback));
      }
    });

    // Always notify "all" observers
    const allObservers = this.observers.get("all");
    if (allObservers) {
      allObservers.forEach((callback) => callbacksToNotify.add(callback));
    }

    // Execute callbacks
    callbacksToNotify.forEach((callback) => {
      try {
        callback();
      } catch (error) {
        console.error("Error in visibility observer:", error);
      }
    });
  }

  // ============================================================================
  // MOTION VISIBILITY
  // ============================================================================

  /**
   * Get motion visibility for a specific color
   */
  getMotionVisibility(color: MotionColor): boolean {
    return this.settings[
      `${color}_motion` as keyof VisibilitySettings
    ] as boolean;
  }

  /**
   * Set motion visibility with constraint enforcement
   */
  setMotionVisibility(color: MotionColor, visible: boolean): void {
    const otherColor =
      color === MotionColor.RED ? MotionColor.BLUE : MotionColor.RED;

    const colorMotionKey = `${color}_motion` as keyof VisibilitySettings;
    const otherColorMotionKey =
      `${otherColor}_motion` as keyof VisibilitySettings;

    // Enforce constraint: at least one motion must remain visible
    if (!visible && !this.settings[otherColorMotionKey]) {
      // If trying to turn off the last visible motion, turn on the other one
      this.settings[colorMotionKey] = false;
      this.settings[otherColorMotionKey] = true;
      this.notifyObservers(["motion", "glyph", "buttons"]);
      return;
    }

    // Normal case
    this.settings[colorMotionKey] = visible;
    this.notifyObservers(["motion", "glyph", "buttons"]);
  }

  /**
   * Check if all motions are visible
   */
  areAllMotionsVisible(): boolean {
    return this.settings.red_motion && this.settings.blue_motion;
  }

  /**
   * Check if any motion is visible
   */
  isAnyMotionVisible(): boolean {
    return this.settings.red_motion || this.settings.blue_motion;
  }

  // ============================================================================
  // GLYPH VISIBILITY
  // ============================================================================

  /**
   * Get glyph visibility considering dependencies
   */
  getGlyphVisibility(glyphType: string): boolean {
    const baseVisibility =
      (this.settings[glyphType as keyof VisibilitySettings] as boolean) ??
      false;

    // For dependent glyphs, also check if both motions are visible
    if (this.DEPENDENT_GLYPHS.includes(glyphType)) {
      return baseVisibility && this.areAllMotionsVisible();
    }

    // For independent glyphs, return direct visibility
    return baseVisibility;
  }

  /**
   * Set glyph visibility
   */
  setGlyphVisibility(glyphType: string, visible: boolean): void {
    if (glyphType in this.settings) {
      (this.settings as unknown as Record<string, boolean>)[glyphType] =
        visible;
      this.notifyObservers(["glyph"]);
    }
  }

  /**
   * Get raw glyph visibility (user preference, ignoring dependencies)
   */
  getRawGlyphVisibility(glyphType: string): boolean {
    return (
      (this.settings[glyphType as keyof VisibilitySettings] as boolean) ?? false
    );
  }

  /**
   * Check if glyph is dependent on motion visibility
   */
  isGlyphDependent(glyphType: string): boolean {
    return this.DEPENDENT_GLYPHS.includes(glyphType);
  }

  // ============================================================================
  // NON-RADIAL POINTS
  // ============================================================================

  /**
   * Get non-radial points visibility
   */
  getNonRadialVisibility(): boolean {
    return this.settings.nonRadialPoints;
  }

  /**
   * Set non-radial points visibility
   */
  setNonRadialVisibility(visible: boolean): void {
    this.settings.nonRadialPoints = visible;
    this.notifyObservers(["non_radial"]);
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  /**
   * Get all visible glyph types
   */
  getVisibleGlyphs(): string[] {
    return ["TKA", "Reversals", "VTG", "Elemental", "Positions"].filter(
      (glyph) => this.getGlyphVisibility(glyph)
    );
  }

  /**
   * Get all enabled dependent glyphs (considering motion constraints)
   */
  getAvailableDependentGlyphs(): string[] {
    if (!this.areAllMotionsVisible()) {
      return [];
    }
    return this.DEPENDENT_GLYPHS.filter((glyph) =>
      this.getRawGlyphVisibility(glyph)
    );
  }

  /**
   * Update from external AppSettings
   */
  updateFromAppSettings(appSettings: AppSettings): void {
    const visibilityUpdate = this.convertAppSettingsToVisibility(appSettings);
    Object.assign(this.settings, visibilityUpdate);
    this.notifyObservers(["all"]);
  }

  /**
   * Get complete visibility state for debugging
   */
  getState(): VisibilitySettings {
    return { ...this.settings };
  }
}

// Global instance for the application
let globalVisibilityStateManager: VisibilityStateManager | null = null;

/**
 * Get or create the global visibility state manager
 */
export function getVisibilityStateManager(
  initialSettings?: Partial<AppSettings>
): VisibilityStateManager {
  if (!globalVisibilityStateManager) {
    globalVisibilityStateManager = new VisibilityStateManager(initialSettings);
  }
  return globalVisibilityStateManager;
}

/**
 * Reset the global visibility state manager (useful for testing)
 */
export function resetVisibilityStateManager(): void {
  globalVisibilityStateManager = null;
}
