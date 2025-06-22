/**
 * Shared API constants across desktop and web applications.
 */

// API Configuration
export const API_BASE_URL = "http://localhost:8000";
export const API_TIMEOUT = 30000; // milliseconds

// API Endpoints
export const ENDPOINTS = {
  health: "/api/health",
  sequences: "/api/sequences",
  settings: "/api/settings",
  backgrounds: "/api/settings/backgrounds/available",
  sequenceById: "/api/sequences/{id}",
  saveSequence: "/api/sequences",
  deleteSequence: "/api/sequences/{id}",
  exportSequence: "/api/sequences/{id}/export",
  importSequence: "/api/sequences/import",
} as const;

// Error messages
export const ERROR_MESSAGES = {
  apiUnavailable: "API server is not available",
  sequenceNotFound: "Sequence not found",
  invalidData: "Invalid data provided",
  saveFailed: "Failed to save sequence",
  loadFailed: "Failed to load sequence",
  deleteFailed: "Failed to delete sequence",
  exportFailed: "Failed to export sequence",
  importFailed: "Failed to import sequence",
  networkError: "Network connection error",
  timeoutError: "Request timeout",
  serverError: "Internal server error",
  validationError: "Data validation error",
} as const;

// Success messages
export const SUCCESS_MESSAGES = {
  sequenceSaved: "Sequence saved successfully",
  sequenceLoaded: "Sequence loaded successfully",
  sequenceDeleted: "Sequence deleted successfully",
  sequenceExported: "Sequence exported successfully",
  sequenceImported: "Sequence imported successfully",
  settingsSaved: "Settings saved successfully",
  settingsLoaded: "Settings loaded successfully",
} as const;

// Settings keys
export const SETTING_KEYS = {
  backgroundType: "ui.background_type",
  theme: "ui.theme",
  windowGeometry: "ui.window_geometry",
  lastSequence: "app.last_sequence_id",
  autoSave: "app.auto_save_enabled",
  autoSaveInterval: "app.auto_save_interval_minutes",
  defaultPropType: "app.default_prop_type",
  showGrid: "ui.show_grid",
  gridOpacity: "ui.grid_opacity",
  animationSpeed: "ui.animation_speed",
} as const;

// Default values
export const DEFAULT_VALUES = {
  backgroundType: "aurora_borealis",
  theme: "dark",
  autoSave: true,
  autoSaveInterval: 5,
  defaultPropType: "staff",
  showGrid: true,
  gridOpacity: 0.3,
  animationSpeed: 1.0,
  sequenceDuration: 4.0,
  beatDuration: 1.0,
} as const;

// HTTP Status codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const;

// File extensions
export const FILE_EXTENSIONS = {
  sequence: ".tka",
  settings: ".ini",
  exportJson: ".json",
  exportCsv: ".csv",
  image: ".png",
  video: ".mp4",
} as const;

// Validation limits
export const VALIDATION_LIMITS = {
  maxSequenceNameLength: 100,
  maxSequenceWordLength: 50,
  maxBeatsPerSequence: 100,
  minBeatDuration: 0.1,
  maxBeatDuration: 10.0,
  maxTurns: 10.0,
  minTurns: -10.0,
} as const;

// Type helpers for better TypeScript support
export type EndpointKey = keyof typeof ENDPOINTS;
export type ErrorMessageKey = keyof typeof ERROR_MESSAGES;
export type SuccessMessageKey = keyof typeof SUCCESS_MESSAGES;
export type SettingKey = keyof typeof SETTING_KEYS;
export type DefaultValueKey = keyof typeof DEFAULT_VALUES;
