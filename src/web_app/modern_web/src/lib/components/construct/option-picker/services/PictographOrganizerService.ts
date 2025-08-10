/**
 * PictographOrganizerService - Handles organization and filtering of pictographs
 *
 * Extracted from OptionPickerScroll.svelte to provide reusable pictograph organization logic.
 * Maintains compatibility with legacy letter type detection while providing clean separation.
 */

import type { PictographData } from '$lib/domain/PictographData';

// ===== Types =====
export interface OrganizedPictographs {
	individual: Record<string, PictographData[]>;
	grouped: Record<string, PictographData[]>;
	totalCount: number;
	hasIndividual: boolean;
	hasGrouped: boolean;
}

export interface PictographOrganizationConfig {
	individualSections: string[];
	groupedSections: string[];
}

// ===== Constants =====
const DEFAULT_CONFIG: PictographOrganizationConfig = {
	individualSections: ['Type1', 'Type2', 'Type3'],
	groupedSections: ['Type4', 'Type5', 'Type6'],
};

// ===== Main Service Class =====
export class PictographOrganizerService {
	private config: PictographOrganizationConfig;

	constructor(config: PictographOrganizationConfig = DEFAULT_CONFIG) {
		this.config = config;
	}

	/**
	 * Organizes pictographs by type with comprehensive error handling
	 * Maintains compatibility with legacy letter type detection
	 */
	organizePictographs(pictographs: PictographData[]): OrganizedPictographs {
		const organized: OrganizedPictographs = {
			individual: {},
			grouped: {},
			totalCount: pictographs.length,
			hasIndividual: false,
			hasGrouped: false,
		};

		// Initialize sections
		this.config.individualSections.forEach((section) => {
			organized.individual[section] = [];
		});
		this.config.groupedSections.forEach((section) => {
			organized.grouped[section] = [];
		});

		// Organize pictographs by type with error handling
		pictographs.forEach((pictograph) => {
			try {
				const pictographType = this.determinePictographType(pictograph);

				if (this.config.individualSections.includes(pictographType)) {
					organized.individual[pictographType]?.push(pictograph);
					organized.hasIndividual = true;
				} else if (this.config.groupedSections.includes(pictographType)) {
					organized.grouped[pictographType]?.push(pictograph);
					organized.hasGrouped = true;
				}
			} catch (error) {
				console.warn(
					'Letter type detection error for pictograph:',
					pictograph.letter,
					error
				);
				// Fallback: put all problematic options in Type1 section
				organized.individual['Type1']?.push(pictograph);
				organized.hasIndividual = true;
			}
		});

		return organized;
	}

	/**
	 * Determines pictograph type based on letter with sophisticated pattern matching
	 * Maintains backward compatibility with legacy letter type detection
	 */
	private determinePictographType(pictograph: PictographData): string {
		const letter = pictograph.letter || '';

		// Check longer patterns first to avoid partial matches
		// Complex patterns with dash suffix
		if (letter.match(/^[WXYZ]-$|^[ΣΔθΩ]-$/)) {
			return 'Type3';
		}
		if (letter.match(/^[ΦΨΛ]-$/)) {
			return 'Type5';
		}

		// Simple letter patterns
		if (letter.match(/^[A-V]$/)) {
			return 'Type1';
		}
		if (letter.match(/^[WXYZ]$|^[ΣΔθΩ]$/)) {
			return 'Type2';
		}
		if (letter.match(/^[ΦΨΛ]$/)) {
			return 'Type4';
		}
		if (letter.match(/^[αβΓ]$/)) {
			return 'Type6';
		}

		// Default fallback
		return 'Type1';
	}

	/**
	 * Gets sections that have pictographs
	 */
	getPopulatedSections(organized: OrganizedPictographs): {
		individual: string[];
		grouped: string[];
	} {
		return {
			individual: Object.keys(organized.individual).filter(
				(key) => organized.individual[key] && organized.individual[key].length > 0
			),
			grouped: Object.keys(organized.grouped).filter(
				(key) => organized.grouped[key] && organized.grouped[key].length > 0
			),
		};
	}

	/**
	 * Gets total count of pictographs in a specific category
	 */
	getCategoryCount(organized: OrganizedPictographs, category: 'individual' | 'grouped'): number {
		const sections = organized[category];
		return Object.values(sections).reduce((total, section) => total + section.length, 0);
	}

	/**
	 * Updates configuration
	 */
	updateConfig(newConfig: Partial<PictographOrganizationConfig>): void {
		this.config = { ...this.config, ...newConfig };
	}

	/**
	 * Gets current configuration
	 */
	getConfig(): PictographOrganizationConfig {
		return { ...this.config };
	}
}

// ===== Factory Function =====
/**
 * Creates a new PictographOrganizerService instance
 * Provides a convenient factory function following your service patterns
 */
export function createPictographOrganizer(
	config?: Partial<PictographOrganizationConfig>
): PictographOrganizerService {
	const finalConfig = config ? { ...DEFAULT_CONFIG, ...config } : DEFAULT_CONFIG;
	return new PictographOrganizerService(finalConfig);
}

// ===== Utility Functions =====
/**
 * Quick organization function for simple use cases
 */
export function organizePictographsQuick(pictographs: PictographData[]): OrganizedPictographs {
	const organizer = createPictographOrganizer();
	return organizer.organizePictographs(pictographs);
}
