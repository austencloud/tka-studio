// src/lib/components/Backgrounds/core/BackgroundFactory.ts
import { SnowfallBackgroundSystem } from '../snowfall/SnowfallBackgroundSystem';
import { NightSkyBackgroundSystem } from '../nightSky/NightSkyBackgroundSystem';
import type {
	BackgroundSystem,
	BackgroundType,
	QualityLevel,
	AccessibilitySettings,
	BackgroundFactoryParams
} from '../types/types';
import { detectAppropriateQuality } from '../config';

export class BackgroundFactory {
	private static defaultAccessibility: AccessibilitySettings = {
		reducedMotion: false,
		highContrast: false,
		visibleParticleSize: 2
	};

	public static createBackgroundSystem(
		params: BackgroundFactoryParams | BackgroundType
	): BackgroundSystem {
		const options: BackgroundFactoryParams = typeof params === 'string' ? { type: params } : params;

		const quality: QualityLevel =
			options.initialQuality ||
			(typeof window !== 'undefined' ? detectAppropriateQuality() : 'medium');

		const accessibility: AccessibilitySettings = {
			...this.defaultAccessibility,
			...(options.accessibility || {})
		};

		// Detect accessibility preferences from browser if not overridden
		if (typeof window !== 'undefined' && window.matchMedia) {
			if (options.accessibility?.reducedMotion === undefined) {
				// Check if not explicitly set
				const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
				if (reducedMotionQuery.matches) {
					accessibility.reducedMotion = true;
				}
			}
			if (options.accessibility?.highContrast === undefined) {
				// Check if not explicitly set
				const highContrastQuery = window.matchMedia('(prefers-contrast: more)');
				if (highContrastQuery.matches) {
					accessibility.highContrast = true;
				}
			}
		}

		let backgroundSystem: BackgroundSystem;

		// Switch statement for background types
		switch (options.type) {
			case 'snowfall':
				backgroundSystem = new SnowfallBackgroundSystem();
				break;
			case 'nightSky':
				backgroundSystem = new NightSkyBackgroundSystem();
				break;
			default:
				console.warn(`Unknown background type "${options.type}". Defaulting to snowfall.`);
				backgroundSystem = new SnowfallBackgroundSystem(); // Default to snowfall
		}

		// Apply accessibility settings to the created system
		if (backgroundSystem.setAccessibility) {
			backgroundSystem.setAccessibility(accessibility);
		}

		// Apply initial quality (important to do after instantiation)
		// The system's constructor might set a default, this overrides it.
		backgroundSystem.setQuality(quality);

		return backgroundSystem;
	}

	// --- createOptimalBackgroundSystem and isBackgroundSupported remain the same ---
	// (Though you might update isBackgroundSupported for 'nightSky')

	public static createOptimalBackgroundSystem(): BackgroundSystem {
		const quality = detectAppropriateQuality();

		// You could add logic here to choose the best default based on time/prefs
		// For now, defaulting to nightSky as it's newly added
		return this.createBackgroundSystem({
			type: 'nightSky', // Changed default maybe? Or keep snowfall?
			initialQuality: quality
		});
	}

	public static isBackgroundSupported(type: BackgroundType): boolean {
		const quality = detectAppropriateQuality();

		switch (type) {
			case 'snowfall':
			case 'nightSky':
				return quality !== 'minimal'; // Disable on minimal quality
			default:
				return false;
		}
	}
}
