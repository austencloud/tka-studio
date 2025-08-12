/**
 * Simple configuration state management for GeneratePanel
 *
 * Just extracts the configuration logic from GeneratePanel.svelte without over-engineering
 */

// ===== Types (same as original) =====
export type GenerationMode = 'FREEFORM' | 'CIRCULAR';
export type GridMode = 'DIAMOND' | 'BOX';
export type PropContinuity = 'RANDOM' | 'CONTINUOUS';
export type SliceSize = 'HALVED' | 'QUARTERED';
export type CAPType = 'STRICT_ROTATED';
export type LetterType = 'TYPE1' | 'TYPE2' | 'TYPE3' | 'TYPE4' | 'TYPE5' | 'TYPE6';

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
	mode: 'FREEFORM',
	length: 16,
	level: 2,
	turnIntensity: 1.0,
	gridMode: 'DIAMOND',
	propContinuity: 'CONTINUOUS',
	letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3', 'TYPE4', 'TYPE5', 'TYPE6']),
	sliceSize: 'HALVED',
	capType: 'STRICT_ROTATED',
};

// ===== Simple State Creator =====
/**
 * Creates simple reactive state for generation configuration
 */
export function createGenerationConfigState(initialConfig?: Partial<GenerationConfig>) {
	// Initialize config
	let config = $state<GenerationConfig>({
		...DEFAULT_CONFIG,
		...initialConfig,
	});

	// Derived values
	const isFreeformMode = $derived(config.mode === 'FREEFORM');

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
