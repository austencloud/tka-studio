/**
 * Application Settings Domain Model
 *
 * Defines the structure for application-wide settings and configuration.
 * This is a domain type that represents the user's preferences and app state.
 */

import type { GridMode, BackgroundType } from "$domain";

export interface AppSettings {
  theme: "light" | "dark";
  gridMode: GridMode;
  showBeatNumbers: boolean;
  autoSave: boolean;
  exportQuality: "low" | "medium" | "high";
  workbenchColumns: number;
  userName?: string;
  propType?: string;
  backupFrequency?: string;
  enableFades?: boolean;
  animationsEnabled?: boolean; // Simple animation control
  growSequence?: boolean;
  numBeats?: number;
  beatLayout?: string;
  // Background settings
  backgroundType?: BackgroundType;
  backgroundQuality?: "high" | "medium" | "low" | "minimal";
  backgroundEnabled?: boolean;
  visibility?: {
    TKA?: boolean;
    Reversals?: boolean;
    Positions?: boolean;
    Elemental?: boolean;
    VTG?: boolean;
    nonRadialPoints?: boolean;
  };
  imageExport?: {
    includeStartPosition?: boolean;
    addReversalSymbols?: boolean;
    addBeatNumbers?: boolean;
    addDifficultyLevel?: boolean;
    addWord?: boolean;
    addInfo?: boolean;
    addUserInfo?: boolean;
  };
  // Sequence Card Settings
  sequenceCard?: {
    defaultColumnCount?: number;
    defaultLayoutMode?: "grid" | "list" | "printable";
    enableTransparency?: boolean;
    cacheEnabled?: boolean;
    cacheSizeLimit?: number;
    exportQuality?: "low" | "medium" | "high";
    exportFormat?: "PNG" | "JPG" | "WebP";
    defaultPaperSize?: "A4" | "Letter" | "Legal" | "Tabloid";
  };
  // Developer Settings
  developerMode?: boolean;
}
