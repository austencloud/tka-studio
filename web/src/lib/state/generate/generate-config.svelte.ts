/**
 * Simple configuration state management for GeneratePanel
 *
 * Just extracts the configuration logic from GeneratePanel.svelte without over-engineering
 */

import {
  CAPType,
  GenerationMode,
  GridMode,
  LetterType,
  PropContinuity,
  SliceSize,
} from "$domain";

export interface GenerationConfig {
  mode: GenerationMode;
  length: number;
  level: number;
  turnIntensity: number;
  gridMode: GridMode;
  propContinuity: PropContinuity;
  letterTypes: Set<LetterType>;
  sliceSize: SliceSize;
  capType: CAPType;
}

// ===== Default Configuration =====
const DEFAULT_CONFIG: GenerationConfig = {
  mode: GenerationMode.FREEFORM,
  length: 16,
  level: 2,
  turnIntensity: 1.0,
  gridMode: GridMode.DIAMOND,
  propContinuity: PropContinuity.CONTINUOUS,
  letterTypes: new Set([
    LetterType.TYPE1,
    LetterType.TYPE2,
    LetterType.TYPE3,
    LetterType.TYPE4,
    LetterType.TYPE5,
    LetterType.TYPE6,
  ]),
  sliceSize: SliceSize.HALVED,
  capType: CAPType.STRICT_ROTATED,
};

// ===== Simple State Creator =====
/**
 * Creates simple reactive state for generation configuration
 */
export function createGenerationConfigState(
  initialConfig?: Partial<GenerationConfig>
) {
  // Initialize config
  let config = $state<GenerationConfig>({
    ...DEFAULT_CONFIG,
    ...initialConfig,
  });

  // Derived values
  const isFreeformMode = $derived(config.mode === GenerationMode.FREEFORM);

  // Simple update function
  function updateConfig(updates: Partial<GenerationConfig>) {
    config = { ...config, ...updates };
  }

  // Event handlers (matching your updated signatures)
  function onLevelChanged(event: CustomEvent) {
    updateConfig({ level: event.detail.value });
  }

  function onLengthChanged(event: CustomEvent) {
    updateConfig({ length: event.detail.value });
  }

  function onTurnIntensityChanged(event: CustomEvent) {
    updateConfig({ turnIntensity: event.detail.value });
  }

  function onGridModeChanged(value: GridMode) {
    updateConfig({ gridMode: value });
  }

  function onGenerationModeChanged(mode: GenerationMode) {
    updateConfig({ mode });
  }

  function onPropContinuityChanged(value: PropContinuity) {
    updateConfig({ propContinuity: value });
  }

  function onLetterTypesChanged(event: CustomEvent) {
    updateConfig({ letterTypes: event.detail.value });
  }

  function onSliceSizeChanged(value: SliceSize) {
    updateConfig({ sliceSize: value });
  }

  function onCAPTypeChanged(event: CustomEvent) {
    updateConfig({ capType: event.detail.value });
  }

  return {
    // State
    get config() {
      return config;
    },
    get isFreeformMode() {
      return isFreeformMode;
    },

    // Actions
    updateConfig,

    // Event handlers
    onLevelChanged,
    onLengthChanged,
    onTurnIntensityChanged,
    onGridModeChanged,
    onGenerationModeChanged,
    onPropContinuityChanged,
    onLetterTypesChanged,
    onSliceSizeChanged,
    onCAPTypeChanged,
  };
}
