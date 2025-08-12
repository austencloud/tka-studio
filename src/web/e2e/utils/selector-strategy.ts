/**
 * Selector Strategy for The Kinetic Constructor
 *
 * This file provides a consistent approach to selecting elements in the application
 * that won't break with design changes.
 */

/**
 * Component selectors that are resilient to design changes
 *
 * These selectors prioritize data-test attributes, then semantic roles,
 * then text content, and finally CSS classes as a last resort.
 */
export const selectors = {
  // Main application structure
  app: {
    mainLayout: '[data-test="main-layout"], .main-layout-wrapper',
    menuBar: '[data-test="menu-bar"], .menu-bar',
    tabButton: (tabName: string) =>
      `[data-test="tab-${tabName}"], button[data-tab="${tabName}"], button:has-text("${tabName}")`,
    activeTab: '[data-test="active-tab"], [aria-selected="true"], .active',
    loadingOverlay: '[data-test="loading-overlay"], .loading-overlay-wrapper',
    fullscreenToggle:
      '[data-test="fullscreen-toggle"], button.fullscreen-toggle',
  },

  // Pictograph components
  pictograph: {
    wrapper: '[data-test="pictograph"], .pictograph-wrapper',
    grid: '[data-test="grid"], .grid-component',
    gridPoint: (pointName: string) =>
      `[data-test="grid-point-${pointName}"], [data-point-name="${pointName}"]`,
    prop: '[data-test="prop"], .prop-component',
    arrow: '[data-test="arrow"], .arrow-component',
    svgElement: "svg",
  },

  // Generate Tab
  generateTab: {
    container: '[data-test="generate-tab"], .generate-tab',
    workbenchPanel: '[data-test="workbench-panel"], .workbench-panel',
    controlsPanel: '[data-test="controls-panel"], .controls-panel',
    generatorTypeSelector: '[data-test="generator-type-selector"]',
    generateButton:
      '[data-test="generate-button"], button:has-text("Generate")',
    sequenceOutput: '[data-test="sequence-output"], .sequence-output',
    progressBar: '[data-test="progress-bar"], .progress-bar',
    numBeatsInput: '[data-test="num-beats-input"], input[name="numBeats"]',
    turnIntensityInput:
      '[data-test="turn-intensity-input"], input[name="turnIntensity"]',
    propContinuitySelect:
      '[data-test="prop-continuity-select"], select[name="propContinuity"]',
    capTypeSelect: '[data-test="cap-type-select"], select[name="capType"]',
  },

  // Write Tab
  writeTab: {
    container: '[data-test="write-tab"], .write-tab',
    actSheet: '[data-test="act-sheet"], .act-sheet',
    sequenceRow: '[data-test="sequence-row"], .sequence-row',
    beatCell: '[data-test="beat-cell"], .beat-cell',
    actTitle: '[data-test="act-title"], .act-title',
    actTitleInput: '[data-test="act-title-input"], input.act-title-input',
    favoriteSequences: '[data-test="favorite-sequences"], .favorite-sequences',
    eraseActButton:
      '[data-test="erase-act-button"], button:has-text("Erase Act")',
    confirmButton: '[data-test="confirm-button"], button:has-text("Confirm")',
  },

  // XState UI elements
  stateMachine: {
    loadingState: '[data-state="loading"]',
    errorState: '[data-state="error"]',
    readyState: '[data-state="ready"]',
    generatingState: '[data-state="generating"]',
  },
};

/**
 * Best practices for adding test attributes to components
 *
 * This function returns the data-test attribute that should be added
 * to components for reliable testing.
 */
export function getTestAttribute(componentName: string, identifier?: string) {
  if (identifier) {
    return `data-test="${componentName}-${identifier}"`;
  }
  return `data-test="${componentName}"`;
}
