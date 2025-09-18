/**
 * Application Settings Domain Model
 *
 * Defines the structure for application-wide settings and configuration.
 * This is a domain type that represents the user's preferences and app state.
 */

import type { BackgroundType, GridMode } from "$shared";

export interface AppSettings {
  gridMode: GridMode;
  userName?: string;
  propType?: string;
  backupFrequency?: string;
  enableFades?: boolean;
  growSequence?: boolean;
  numBeats?: number;
  beatLayout?: string;
  // Background settings
  backgroundType?: BackgroundType;
  backgroundQuality?: "high" | "medium" | "low" | "minimal";
  backgroundEnabled?: boolean;


  // Word Card Settings
  WordCard?: {
    defaultColumnCount?: number;
    defaultLayoutMode?: "grid" | "list" | "printable";
    enableTransparency?: boolean;
    cacheEnabled?: boolean;
    cacheSizeLimit?: number;
    exportQuality?: "low" | "medium" | "high";
    exportFormat?: "PNG" | "JPG" | "WebP";
    defaultPaperSize?: "A4" | "Letter" | "Legal" | "Tabloid";
  };

}
