/**
 * GenerationConfigurationService - Manages sequence generation configuration
 * 
 * Extracted from GeneratePanel.svelte to provide reusable configuration management.
 * Handles validation, default values, and configuration updates with type safety.
 */

// ===== Types =====
export type GenerationMode = 'FREEFORM' | 'CIRCULAR';
export type GridMode = 'DIAMOND' | 'BOX';
export type PropContinuity = 'RANDOM' | 'CONTINUOUS';
export type SliceSize = 'HALVED' | 'QUARTERED';
export type CAPType = 'STRICT_ROTATED';
export type LetterType = 'TYPE1' | 'TYPE2' | 'TYPE3' | 'TYPE4' | 'TYPE5' | 'TYPE6';

export interface GenerationConfiguration {
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

export interface ConfigurationConstraints {
	length: { min: number; max: number; step: number };
	level: { min: number; max: number; step: number };
	turnIntensity: { min: number; max: number; step: number };
	letterTypes: { minSelection: number; maxSelection: number };
}

export interface ConfigurationValidationResult {
	isValid: boolean;
	errors: string[];
	warnings: string[];
	normalizedConfig?: GenerationConfiguration;
}

// ===== Constants =====
const DEFAULT_CONFIGURATION: GenerationConfiguration = {
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

const DEFAULT_CONSTRAINTS: ConfigurationConstraints = {
	length: { min: 4, max: 64, step: 1 },
	level: { min: 1, max: 6, step: 1 },
	turnIntensity: { min: 0.1, max: 2.0, step: 0.1 },
	letterTypes: { minSelection: 1, maxSelection: 6 },
};

// ===== Main Service Class =====
export class GenerationConfigurationService {
	private config: GenerationConfiguration;
	private constraints: ConfigurationConstraints;
	private changeListeners: Array<(config: GenerationConfiguration) => void> = [];

	constructor(
		initialConfig?: Partial<GenerationConfiguration>,
		constraints: ConfigurationConstraints = DEFAULT_CONSTRAINTS
	) {
		this.constraints = constraints;
		this.config = this.createValidConfiguration(initialConfig);
	}

	/**
	 * Gets the current configuration
	 */
	getConfiguration(): GenerationConfiguration {
		return { ...this.config, letterTypes: new Set(this.config.letterTypes) };
	}

	/**
	 * Updates configuration with validation
	 */
	updateConfiguration(updates: Partial<GenerationConfiguration>): ConfigurationValidationResult {
		const proposedConfig = { ...this.config, ...updates };
		const validation = this.validateConfiguration(proposedConfig);

		if (validation.isValid && validation.normalizedConfig) {
			const previousConfig = this.getConfiguration();
			this.config = validation.normalizedConfig;
			
			// Notify listeners if configuration actually changed
			if (!this.configurationEquals(previousConfig, this.config)) {
				this.notifyChangeListeners();
			}
		}

		return validation;
	}

	/**
	 * Updates a single configuration property
	 */
	updateProperty<K extends keyof GenerationConfiguration>(
		property: K,
		value: GenerationConfiguration[K]
	): ConfigurationValidationResult {
		return this.updateConfiguration({ [property]: value } as Partial<GenerationConfiguration>);
	}

	/**
	 * Resets configuration to defaults
	 */
	resetToDefaults(): void {
		const previousConfig = this.getConfiguration();
		this.config = { ...DEFAULT_CONFIGURATION, letterTypes: new Set(DEFAULT_CONFIGURATION.letterTypes) };
		
		if (!this.configurationEquals(previousConfig, this.config)) {
			this.notifyChangeListeners();
		}
	}

	/**
	 * Validates a configuration against constraints
	 */
	validateConfiguration(config: Partial<GenerationConfiguration>): ConfigurationValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		// Validate length
		if (config.length !== undefined) {
			if (config.length < this.constraints.length.min || config.length > this.constraints.length.max) {
				errors.push(`Length must be between ${this.constraints.length.min} and ${this.constraints.length.max}`);
			}
		}

		// Validate level
		if (config.level !== undefined) {
			if (config.level < this.constraints.level.min || config.level > this.constraints.level.max) {
				errors.push(`Level must be between ${this.constraints.level.min} and ${this.constraints.level.max}`);
			}
		}

		// Validate turn intensity
		if (config.turnIntensity !== undefined) {
			if (config.turnIntensity < this.constraints.turnIntensity.min || config.turnIntensity > this.constraints.turnIntensity.max) {
				errors.push(`Turn intensity must be between ${this.constraints.turnIntensity.min} and ${this.constraints.turnIntensity.max}`);
			}
		}

		// Validate letter types
		if (config.letterTypes !== undefined) {
			const typeCount = config.letterTypes.size;
			if (typeCount < this.constraints.letterTypes.minSelection) {
				errors.push(`At least ${this.constraints.letterTypes.minSelection} letter type must be selected`);
			}
			if (typeCount > this.constraints.letterTypes.maxSelection) {
				errors.push(`At most ${this.constraints.letterTypes.maxSelection} letter types can be selected`);
			}
		}

		// Check for mode-specific issues
		if (config.mode === 'CIRCULAR') {
			if (config.length !== undefined && config.length % 4 !== 0) {
				warnings.push('Circular mode works best with lengths that are multiples of 4');
			}
		}

		// Create normalized configuration if no errors
		let normalizedConfig: GenerationConfiguration | undefined;
		if (errors.length === 0) {
			normalizedConfig = this.normalizeConfiguration(config);
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings,
			normalizedConfig,
		};
	}

	/**
	 * Gets constraints for the configuration
	 */
	getConstraints(): ConfigurationConstraints {
		return { ...this.constraints };
	}

	/**
	 * Updates constraints
	 */
	updateConstraints(newConstraints: Partial<ConfigurationConstraints>): void {
		this.constraints = { ...this.constraints, ...newConstraints };
		
		// Re-validate current configuration against new constraints
		const validation = this.validateConfiguration(this.config);
		if (!validation.isValid) {
			console.warn('Current configuration violates new constraints:', validation.errors);
		}
	}

	/**
	 * Adds a listener for configuration changes
	 */
	addChangeListener(listener: (config: GenerationConfiguration) => void): () => void {
		this.changeListeners.push(listener);
		
		// Return cleanup function
		return () => {
			const index = this.changeListeners.indexOf(listener);
			if (index > -1) {
				this.changeListeners.splice(index, 1);
			}
		};
	}

	/**
	 * Gets configuration summary for debugging
	 */
	getConfigurationSummary(): {
		mode: GenerationMode;
		settingsCount: number;
		isValid: boolean;
		letterTypeCount: number;
	} {
		const validation = this.validateConfiguration(this.config);
		return {
			mode: this.config.mode,
			settingsCount: Object.keys(this.config).length,
			isValid: validation.isValid,
			letterTypeCount: this.config.letterTypes.size,
		};
	}

	/**
	 * Creates a preset configuration for common use cases
	 */
	applyPreset(preset: 'beginner' | 'intermediate' | 'advanced' | 'expert'): void {
		const presets: Record<string, Partial<GenerationConfiguration>> = {
			beginner: {
				mode: 'FREEFORM',
				length: 8,
				level: 1,
				turnIntensity: 0.5,
				propContinuity: 'CONTINUOUS',
				letterTypes: new Set(['TYPE1', 'TYPE2']),
			},
			intermediate: {
				mode: 'FREEFORM',
				length: 16,
				level: 2,
				turnIntensity: 1.0,
				propContinuity: 'CONTINUOUS',
				letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3']),
			},
			advanced: {
				mode: 'FREEFORM',
				length: 24,
				level: 3,
				turnIntensity: 1.5,
				propContinuity: 'RANDOM',
				letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3', 'TYPE4']),
			},
			expert: {
				mode: 'CIRCULAR',
				length: 32,
				level: 4,
				turnIntensity: 2.0,
				propContinuity: 'RANDOM',
				letterTypes: new Set(['TYPE1', 'TYPE2', 'TYPE3', 'TYPE4', 'TYPE5', 'TYPE6']),
			},
		};

		this.updateConfiguration(presets[preset]);
	}

	// ===== Private Methods =====

	private createValidConfiguration(partial?: Partial<GenerationConfiguration>): GenerationConfiguration {
		const proposed = { ...DEFAULT_CONFIGURATION, ...partial };
		const validation = this.validateConfiguration(proposed);
		
		if (validation.isValid && validation.normalizedConfig) {
			return validation.normalizedConfig;
		} else {
			console.warn('Invalid initial configuration, using defaults:', validation.errors);
			return { ...DEFAULT_CONFIGURATION, letterTypes: new Set(DEFAULT_CONFIGURATION.letterTypes) };
		}
	}

	private normalizeConfiguration(config: Partial<GenerationConfiguration>): GenerationConfiguration {
		const base = { ...this.config, ...config };
		
		// Normalize values to constraints
		if (base.length !== undefined) {
			base.length = Math.round(base.length / this.constraints.length.step) * this.constraints.length.step;
			base.length = Math.max(this.constraints.length.min, Math.min(this.constraints.length.max, base.length));
		}

		if (base.level !== undefined) {
			base.level = Math.max(this.constraints.level.min, Math.min(this.constraints.level.max, Math.round(base.level)));
		}

		if (base.turnIntensity !== undefined) {
			base.turnIntensity = Math.round(base.turnIntensity / this.constraints.turnIntensity.step) * this.constraints.turnIntensity.step;
			base.turnIntensity = Math.max(this.constraints.turnIntensity.min, Math.min(this.constraints.turnIntensity.max, base.turnIntensity));
		}

		return base as GenerationConfiguration;
	}

	private configurationEquals(a: GenerationConfiguration, b: GenerationConfiguration): boolean {
		if (a.mode !== b.mode || a.length !== b.length || a.level !== b.level || 
			a.turnIntensity !== b.turnIntensity || a.gridMode !== b.gridMode || 
			a.propContinuity !== b.propContinuity || a.sliceSize !== b.sliceSize || 
			a.capType !== b.capType) {
			return false;
		}

		// Compare letter types sets
		if (a.letterTypes.size !== b.letterTypes.size) {
			return false;
		}
		for (const type of a.letterTypes) {
			if (!b.letterTypes.has(type)) {
				return false;
			}
		}

		return true;
	}

	private notifyChangeListeners(): void {
		const currentConfig = this.getConfiguration();
		this.changeListeners.forEach(listener => {
			try {
				listener(currentConfig);
			} catch (error) {
				console.error('Error in configuration change listener:', error);
			}
		});
	}
}

// ===== Factory Functions =====

/**
 * Creates a new GenerationConfigurationService instance
 */
export function createGenerationConfigurationService(
	initialConfig?: Partial<GenerationConfiguration>,
	constraints?: Partial<ConfigurationConstraints>
): GenerationConfigurationService {
	const finalConstraints = constraints ? { ...DEFAULT_CONSTRAINTS, ...constraints } : DEFAULT_CONSTRAINTS;
	return new GenerationConfigurationService(initialConfig, finalConstraints);
}

/**
 * Creates a configuration service with preset constraints for different difficulty levels
 */
export function createConfigurationServiceForLevel(
	level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
): GenerationConfigurationService {
	const constraintsByLevel: Record<string, Partial<ConfigurationConstraints>> = {
		beginner: {
			length: { min: 4, max: 16, step: 1 },
			level: { min: 1, max: 2, step: 1 },
			turnIntensity: { min: 0.1, max: 1.0, step: 0.1 },
			letterTypes: { minSelection: 1, maxSelection: 3 },
		},
		intermediate: {
			length: { min: 8, max: 32, step: 1 },
			level: { min: 1, max: 4, step: 1 },
			turnIntensity: { min: 0.1, max: 1.5, step: 0.1 },
			letterTypes: { minSelection: 1, maxSelection: 4 },
		},
		advanced: {
			length: { min: 12, max: 48, step: 1 },
			level: { min: 2, max: 5, step: 1 },
			turnIntensity: { min: 0.5, max: 2.0, step: 0.1 },
			letterTypes: { minSelection: 1, maxSelection: 6 },
		},
		expert: DEFAULT_CONSTRAINTS,
	};

	const service = createGenerationConfigurationService(undefined, constraintsByLevel[level]);
	service.applyPreset(level);
	return service;
}

// ===== Utility Functions =====

/**
 * Validates if a mode change is compatible with current configuration
 */
export function validateModeChange(
	currentConfig: GenerationConfiguration,
	newMode: GenerationMode
): { isCompatible: boolean; issues: string[]; suggestions: string[] } {
	const issues: string[] = [];
	const suggestions: string[] = [];

	if (newMode === 'CIRCULAR') {
		if (currentConfig.length % 4 !== 0) {
			issues.push('Circular mode requires length to be a multiple of 4');
			suggestions.push(`Consider changing length to ${Math.round(currentConfig.length / 4) * 4}`);
		}
		
		if (currentConfig.level > 4) {
			issues.push('Circular mode works best with levels 1-4');
			suggestions.push('Consider reducing level to 4 or lower');
		}
	}

	return {
		isCompatible: issues.length === 0,
		issues,
		suggestions,
	};
}

/**
 * Gets recommended configuration based on user experience level
 */
export function getRecommendedConfiguration(
	experienceLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert',
	preferences?: Partial<GenerationConfiguration>
): GenerationConfiguration {
	const service = createConfigurationServiceForLevel(experienceLevel);
	
	if (preferences) {
		const validation = service.updateConfiguration(preferences);
		if (validation.isValid) {
			return service.getConfiguration();
		}
	}
	
	return service.getConfiguration();
}
