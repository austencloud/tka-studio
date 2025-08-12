/**
 * Section Service - Manages sequence section organization
 *
 * Handles grouping sequences into sections with headers and counts,
 * following the microservices architecture pattern.
 */

import type { BrowseSequenceMetadata, SortMethod } from '../interfaces';

export interface SequenceSection {
	id: string;
	title: string;
	count: number;
	sequences: BrowseSequenceMetadata[];
	isExpanded: boolean;
	sortOrder: number;
}

export interface SectionConfiguration {
	groupBy: 'letter' | 'length' | 'difficulty' | 'author' | 'date' | 'none';
	sortMethod: SortMethod;
	showEmptySections: boolean;
	expandedSections: Set<string>;
}

export interface ISectionService {
	/** Organize sequences into sections based on configuration */
	organizeSections(
		sequences: BrowseSequenceMetadata[],
		config: SectionConfiguration
	): Promise<SequenceSection[]>;

	/** Toggle section expansion state */
	toggleSectionExpansion(sectionId: string, sections: SequenceSection[]): SequenceSection[];

	/** Get default section configuration */
	getDefaultSectionConfiguration(): SectionConfiguration;

	/** Update section configuration */
	updateSectionConfiguration(
		config: SectionConfiguration,
		updates: Partial<SectionConfiguration>
	): SectionConfiguration;

	/** Get section statistics */
	getSectionStatistics(sections: SequenceSection[]): {
		totalSections: number;
		totalSequences: number;
		expandedSections: number;
		averageSequencesPerSection: number;
	};
}

export class SectionService implements ISectionService {
	async organizeSections(
		sequences: BrowseSequenceMetadata[],
		config: SectionConfiguration
	): Promise<SequenceSection[]> {
		if (config.groupBy === 'none') {
			return [
				{
					id: 'all',
					title: 'All Sequences',
					count: sequences.length,
					sequences,
					isExpanded: true,
					sortOrder: 0,
				},
			];
		}

		const grouped = this.groupSequences(sequences, config.groupBy);
		const sections = this.createSections(grouped, config);

		return this.sortSections(sections, config.groupBy);
	}

	toggleSectionExpansion(sectionId: string, sections: SequenceSection[]): SequenceSection[] {
		return sections.map((section) => ({
			...section,
			isExpanded: section.id === sectionId ? !section.isExpanded : section.isExpanded,
		}));
	}

	getDefaultSectionConfiguration(): SectionConfiguration {
		return {
			groupBy: 'letter',
			sortMethod: 'alphabetical' as SortMethod,
			showEmptySections: false,
			expandedSections: new Set(['A', 'B', 'C']), // Default expand first few sections
		};
	}

	updateSectionConfiguration(
		config: SectionConfiguration,
		updates: Partial<SectionConfiguration>
	): SectionConfiguration {
		return {
			...config,
			...updates,
		};
	}

	getSectionStatistics(sections: SequenceSection[]) {
		const totalSections = sections.length;
		const totalSequences = sections.reduce((sum, section) => sum + section.count, 0);
		const expandedSections = sections.filter((section) => section.isExpanded).length;
		const averageSequencesPerSection = totalSections > 0 ? totalSequences / totalSections : 0;

		return {
			totalSections,
			totalSequences,
			expandedSections,
			averageSequencesPerSection: Math.round(averageSequencesPerSection * 10) / 10,
		};
	}

	// Private helper methods
	private groupSequences(
		sequences: BrowseSequenceMetadata[],
		groupBy: SectionConfiguration['groupBy']
	): Map<string, BrowseSequenceMetadata[]> {
		const groups = new Map<string, BrowseSequenceMetadata[]>();

		sequences.forEach((sequence) => {
			const key = this.getGroupKey(sequence, groupBy);
			if (!groups.has(key)) {
				groups.set(key, []);
			}
			groups.get(key)!.push(sequence);
		});

		return groups;
	}

	private getGroupKey(
		sequence: BrowseSequenceMetadata,
		groupBy: SectionConfiguration['groupBy']
	): string {
		switch (groupBy) {
			case 'letter':
				return sequence.word.charAt(0).toUpperCase();

			case 'length': {
				const length = sequence.sequenceLength || sequence.word.length;
				return `${length} beats`;
			}

			case 'difficulty':
				return sequence.difficultyLevel || 'Unknown';

			case 'author':
				return sequence.author || 'Unknown Author';

			case 'date': {
				if (!sequence.dateAdded) return 'Unknown Date';
				const date = new Date(sequence.dateAdded);
				return date.toDateString();
			}

			default:
				return 'All';
		}
	}

	private createSections(
		grouped: Map<string, BrowseSequenceMetadata[]>,
		config: SectionConfiguration
	): SequenceSection[] {
		const sections: SequenceSection[] = [];

		grouped.forEach((sequences, key) => {
			if (!config.showEmptySections && sequences.length === 0) {
				return;
			}

			const section: SequenceSection = {
				id: this.createSectionId(key, config.groupBy),
				title: this.createSectionTitle(key, config.groupBy, sequences.length),
				count: sequences.length,
				sequences: this.sortSequencesInSection(sequences, config.sortMethod),
				isExpanded: config.expandedSections.has(key),
				sortOrder: this.getSectionSortOrder(key, config.groupBy),
			};

			sections.push(section);
		});

		return sections;
	}

	private createSectionId(key: string, groupBy: SectionConfiguration['groupBy']): string {
		return `${groupBy}-${key.toLowerCase().replace(/\s+/g, '-')}`;
	}

	private createSectionTitle(
		key: string,
		groupBy: SectionConfiguration['groupBy'],
		count: number
	): string {
		const countText = count === 1 ? '1 sequence' : `${count} sequences`;

		switch (groupBy) {
			case 'letter':
				return `${key} (${countText})`;

			case 'length':
				return `${key} (${countText})`;

			case 'difficulty': {
				const difficultyEmoji =
					{
						beginner: '🟢',
						intermediate: '🟡',
						advanced: '🔴',
						Unknown: '⚪',
					}[key] || '⚪';
				return `${difficultyEmoji} ${key} (${countText})`;
			}

			case 'author':
				return `👤 ${key} (${countText})`;

			case 'date':
				return `📅 ${this.formatDateForSection(key)} (${countText})`;

			default:
				return `${key} (${countText})`;
		}
	}

	private sortSequencesInSection(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): BrowseSequenceMetadata[] {
		const sorted = [...sequences];

		switch (sortMethod) {
			case 'alphabetical':
				return sorted.sort((a, b) => a.word.localeCompare(b.word));

			case 'difficulty_level':
				return sorted.sort((a, b) => {
					const getDifficultyOrder = (level?: string) => {
						switch (level) {
							case 'beginner':
								return 1;
							case 'intermediate':
								return 2;
							case 'advanced':
								return 3;
							default:
								return 0;
						}
					};
					return (
						getDifficultyOrder(a.difficultyLevel) -
						getDifficultyOrder(b.difficultyLevel)
					);
				});

			case 'sequence_length':
				return sorted.sort((a, b) => {
					const lengthA = a.sequenceLength || a.word.length;
					const lengthB = b.sequenceLength || b.word.length;
					return lengthA - lengthB;
				});

			case 'date_added':
				return sorted.sort((a, b) => {
					const dateA = a.dateAdded ? new Date(a.dateAdded).getTime() : 0;
					const dateB = b.dateAdded ? new Date(b.dateAdded).getTime() : 0;
					return dateB - dateA; // Most recent first
				});

			case 'author':
				return sorted.sort((a, b) => (a.author || '').localeCompare(b.author || ''));

			default:
				return sorted;
		}
	}

	private sortSections(
		sections: SequenceSection[],
		_groupBy: SectionConfiguration['groupBy']
	): SequenceSection[] {
		return sections.sort((a, b) => {
			// Primary sort by sortOrder
			if (a.sortOrder !== b.sortOrder) {
				return a.sortOrder - b.sortOrder;
			}

			// Secondary sort by title for consistent ordering
			return a.title.localeCompare(b.title);
		});
	}

	private getSectionSortOrder(key: string, groupBy: SectionConfiguration['groupBy']): number {
		switch (groupBy) {
			case 'letter':
				// A-Z order
				return key.charCodeAt(0);

			case 'length': {
				// Extract number from "X beats"
				const match = key.match(/^(\d+)/);
				return match && match[1] ? parseInt(match[1]) : 999;
			}

			case 'difficulty': {
				// Difficulty order
				const difficultyOrder = { beginner: 1, intermediate: 2, advanced: 3, Unknown: 4 };
				return difficultyOrder[key as keyof typeof difficultyOrder] || 999;
			}

			case 'author':
				// Alphabetical by author
				return 0; // Will be sorted by title comparison

			case 'date': {
				// Most recent first
				const date = new Date(key);
				return -date.getTime(); // Negative for reverse chronological
			}

			default:
				return 0;
		}
	}

	private formatDateForSection(dateString: string): string {
		const date = new Date(dateString);
		const now = new Date();
		const diffTime = now.getTime() - date.getTime();
		const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

		if (diffDays === 0) return 'Today';
		if (diffDays === 1) return 'Yesterday';
		if (diffDays < 7) return `${diffDays} days ago`;
		if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

		return date.toLocaleDateString();
	}
}
