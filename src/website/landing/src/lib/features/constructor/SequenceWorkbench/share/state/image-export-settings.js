/**
 * Image Export Settings for TKA Constructor
 * Provides default settings for image export functionality
 */

// Default image export settings
const defaultSettings = {
  include_start_position: false,
  add_user_info: true,
  add_word: true,
  add_difficulty_level: true,
  add_beat_numbers: true,
  add_reversal_symbols: true,
  use_last_save_directory: false,
  combined_grids: false,
  format: 'PNG',
  quality: 95,
  width: 1920,
  height: 1080
};

// Export function to get current settings
export function getImageExportSettings() {
  return defaultSettings;
}

// Export function to update settings (stub for now)
export function updateImageExportSettings(newSettings) {
  // In a real implementation, this would update persistent storage
  console.log('Updating image export settings:', newSettings);
}

// Export function to reset to defaults
export function resetImageExportSettings() {
  // In a real implementation, this would reset persistent storage
  console.log('Resetting image export settings to defaults');
}
