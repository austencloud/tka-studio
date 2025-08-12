/**
 * Browse Service Implementation
 *
 * Handles loading, filtering, and sorting of sequence metadata for the browse tab.
 * Ported and adapted from desktop app's BrowseService.
 */

import { FilterType as FilterTypeEnum, SortMethod as SortMethodEnum } from '$lib/domain/browse';
import type {
	BrowseSequenceMetadata,
	FilterType,
	FilterValue,
	IBrowseService,
	SortMethod,
} from '$lib/services/interfaces';

export class BrowseService implements IBrowseService {
	private cachedSequences: BrowseSequenceMetadata[] | null = null;

	async loadSequenceMetadata(): Promise<BrowseSequenceMetadata[]> {
		console.log('🔍 BrowseService.loadSequenceMetadata() called');

		if (this.cachedSequences !== null) {
			console.log('📦 Returning cached sequences:', this.cachedSequences.length, 'items');
			return this.cachedSequences;
		}

		try {
			// Try to load from sequence index first
			console.log('🔄 Loading from sequence index...');
			const sequences = await this.loadFromSequenceIndex();
			console.log(
				'✅ Successfully loaded from sequence index:',
				sequences.length,
				'sequences'
			);
			console.log(
				'📋 Sequence IDs:',
				sequences.map((s) => s.id)
			);
			this.cachedSequences = sequences;
			return sequences;
		} catch (error) {
			console.warn('❌ Failed to load sequence index, generating from dictionary:', error);
			// Fallback to scanning dictionary folders
			const sequences = await this.generateSequenceIndex();
			console.log('🔧 Generated sequences as fallback:', sequences.length, 'sequences');
			this.cachedSequences = sequences;
			return sequences;
		}
	}

	async applyFilter(
		sequences: BrowseSequenceMetadata[],
		filterType: FilterType,
		filterValue: FilterValue
	): Promise<BrowseSequenceMetadata[]> {
		console.log('🔍 BrowseService.applyFilter() called with:');
		console.log('  - filterType:', filterType);
		console.log('  - filterValue:', filterValue);
		console.log('  - input sequences:', sequences.length, 'items');

		if (filterType === FilterTypeEnum.ALL_SEQUENCES) {
			console.log(
				'✅ ALL_SEQUENCES filter detected - returning all sequences:',
				sequences.length
			);
			return sequences;
		}

		console.log('🔄 Applying specific filter...');
		let filtered: BrowseSequenceMetadata[];

		switch (filterType) {
			case FilterTypeEnum.STARTING_LETTER:
				filtered = this.filterByStartingLetter(sequences, filterValue);
				break;
			case FilterTypeEnum.CONTAINS_LETTERS:
				filtered = this.filterByContainsLetters(sequences, filterValue);
				break;
			case FilterTypeEnum.LENGTH:
				filtered = this.filterByLength(sequences, filterValue);
				break;
			case FilterTypeEnum.DIFFICULTY:
				filtered = this.filterByDifficulty(sequences, filterValue);
				break;
			case FilterTypeEnum.STARTING_POSITION:
				filtered = this.filterByStartingPosition(sequences, filterValue);
				break;
			case FilterTypeEnum.AUTHOR:
				filtered = this.filterByAuthor(sequences, filterValue);
				break;
			case FilterTypeEnum.GRID_MODE:
				filtered = this.filterByGridMode(sequences, filterValue);
				break;
			case FilterTypeEnum.FAVORITES:
				filtered = sequences.filter((s) => s.isFavorite);
				break;
			case FilterTypeEnum.RECENT:
				filtered = this.filterByRecent(sequences);
				break;
			default:
				console.log('⚠️ Unknown filter type, returning all sequences');
				filtered = sequences;
		}

		console.log('📊 Filter result:', filtered.length, 'sequences after filtering');
		return filtered;
	}

	async sortSequences(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): Promise<BrowseSequenceMetadata[]> {
		const sorted = [...sequences];

		switch (sortMethod) {
			case SortMethodEnum.ALPHABETICAL:
				return sorted.sort((a, b) => a.word.localeCompare(b.word));
			case SortMethodEnum.DATE_ADDED:
				return sorted.sort((a, b) => {
					const dateA = a.dateAdded || new Date(0);
					const dateB = b.dateAdded || new Date(0);
					return dateB.getTime() - dateA.getTime();
				});
			case SortMethodEnum.DIFFICULTY_LEVEL:
				return sorted.sort((a, b) => {
					const levelA = this.getDifficultyOrder(a.difficultyLevel);
					const levelB = this.getDifficultyOrder(b.difficultyLevel);
					return levelA - levelB;
				});
			case SortMethodEnum.SEQUENCE_LENGTH:
				return sorted.sort((a, b) => (a.sequenceLength || 0) - (b.sequenceLength || 0));
			case SortMethodEnum.AUTHOR:
				return sorted.sort((a, b) => (a.author || '').localeCompare(b.author || ''));
			case SortMethodEnum.POPULARITY:
				return sorted.sort((a, b) => Number(b.isFavorite) - Number(a.isFavorite));
			default:
				return sorted;
		}
	}

	async groupSequencesIntoSections(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): Promise<Record<string, BrowseSequenceMetadata[]>> {
		const sections: Record<string, BrowseSequenceMetadata[]> = {};

		for (const sequence of sequences) {
			const sectionKey = this.getSectionKey(sequence, sortMethod);
			if (!sections[sectionKey]) {
				sections[sectionKey] = [];
			}
			sections[sectionKey].push(sequence);
		}

		return sections;
	}

	async getUniqueValues(field: keyof BrowseSequenceMetadata): Promise<string[]> {
		const sequences = await this.loadSequenceMetadata();
		const values = new Set<string>();

		for (const sequence of sequences) {
			const value = sequence[field];
			if (value != null) {
				values.add(String(value));
			}
		}

		return Array.from(values).sort();
	}

	async getFilterOptions(filterType: FilterType): Promise<string[]> {
		switch (filterType) {
			case FilterTypeEnum.STARTING_LETTER:
				return ['A-D', 'E-H', 'I-L', 'M-P', 'Q-T', 'U-Z'];
			case FilterTypeEnum.LENGTH:
				return ['3', '4', '5', '6', '7', '8+'];
			case FilterTypeEnum.DIFFICULTY:
				return ['beginner', 'intermediate', 'advanced'];
			case FilterTypeEnum.AUTHOR:
				return this.getUniqueValues('author');
			case FilterTypeEnum.GRID_MODE:
				return ['diamond', 'box'];
			default:
				return [];
		}
	}

	// Private helper methods
	private async loadFromSequenceIndex(): Promise<BrowseSequenceMetadata[]> {
		console.log('🌐 Fetching sequence-index.json...');
		const response = await fetch('/sequence-index.json');
		console.log('🌐 Response status:', response.status, response.statusText);

		if (!response.ok) {
			throw new Error(`Failed to load sequence index: ${response.status}`);
		}

		const data = await response.json();
		console.log('📄 Loaded sequence index data:', data);
		console.log('📄 Total sequences in index:', data.totalSequences);
		console.log('📄 Sequences array length:', data.sequences?.length || 0);

		const sequences = data.sequences || [];
		console.log('📦 Returning sequences:', sequences.length, 'items');
		return sequences;
	}

	private async generateSequenceIndex(): Promise<BrowseSequenceMetadata[]> {
		// This would scan the dictionary folder to build the index
		// For now, return sample data - in production, you'd implement folder scanning
		return this.createSampleSequences();
	}

	private createSampleSequences(): BrowseSequenceMetadata[] {
		const sampleWords = [
			'ALPHA',
			'BETA',
			'GAMMA',
			'DELTA',
			'EPSILON',
			'ZETA',
			'ETA',
			'THETA',
			'IOTA',
			'KAPPA',
			'LAMBDA',
			'MU',
			'NU',
			'XI',
			'OMICRON',
			'PI',
			'RHO',
			'SIGMA',
		];

		const authors = ['TKA User', 'Demo Author', 'Expert User'];
		const difficulties = ['beginner', 'intermediate', 'advanced'];
		const gridModes = ['diamond', 'box'];

		return sampleWords.map((word, index): BrowseSequenceMetadata => {
			const authorValue = authors[index % authors.length];
			const gridModeValue = gridModes[index % gridModes.length];
			const difficultyValue = difficulties[index % difficulties.length];

			const result: BrowseSequenceMetadata = {
				id: word.toLowerCase(),
				name: `${word} Sequence`,
				word,
				thumbnails: [`${word}_ver1.png`],
				isFavorite: Math.random() > 0.7,
				isCircular: false,
				tags: ['flow', 'practice'],
				metadata: { generated: true },
			};

			// Add optional properties only if they have values
			if (authorValue) result.author = authorValue;
			if (gridModeValue) result.gridMode = gridModeValue;
			if (difficultyValue) result.difficultyLevel = difficultyValue;

			result.sequenceLength = Math.floor(Math.random() * 8) + 3;
			result.level = Math.floor(Math.random() * 4) + 1;
			result.dateAdded = new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000);
			result.propType = 'fans';
			result.startingPosition = 'center';

			return result;
		});
	}

	private filterByStartingLetter(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue || typeof filterValue !== 'string') return sequences;

		if (filterValue.includes('-')) {
			const [start, end] = filterValue.split('-');
			return sequences.filter((s) => {
				const firstLetter = s.word[0]?.toUpperCase();
				return firstLetter && start && end && firstLetter >= start && firstLetter <= end;
			});
		}

		return sequences.filter((s) => s.word[0]?.toUpperCase() === filterValue.toUpperCase());
	}

	private filterByContainsLetters(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue || typeof filterValue !== 'string') return sequences;
		return sequences.filter((s) => s.word.toLowerCase().includes(filterValue.toLowerCase()));
	}

	private filterByLength(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue) return sequences;

		if (filterValue === '8+') {
			return sequences.filter((s) => (s.sequenceLength || 0) >= 8);
		}

		const length = parseInt(String(filterValue));
		if (isNaN(length)) return sequences;

		return sequences.filter((s) => s.sequenceLength === length);
	}

	private filterByDifficulty(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue) return sequences;
		return sequences.filter((s) => s.difficultyLevel === filterValue);
	}

	private filterByStartingPosition(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue) return sequences;
		return sequences.filter((s) => s.startingPosition === filterValue);
	}

	private filterByAuthor(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue) return sequences;
		return sequences.filter((s) => s.author === filterValue);
	}

	private filterByGridMode(
		sequences: BrowseSequenceMetadata[],
		filterValue: FilterValue
	): BrowseSequenceMetadata[] {
		if (!filterValue) return sequences;
		return sequences.filter((s) => s.gridMode === filterValue);
	}

	private filterByRecent(sequences: BrowseSequenceMetadata[]): BrowseSequenceMetadata[] {
		const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
		return sequences.filter((s) => {
			const dateAdded = s.dateAdded || new Date(0);
			return dateAdded >= thirtyDaysAgo;
		});
	}

	private getDifficultyOrder(difficulty?: string): number {
		switch (difficulty) {
			case 'beginner':
				return 1;
			case 'intermediate':
				return 2;
			case 'advanced':
				return 3;
			default:
				return 0;
		}
	}

	private getSectionKey(sequence: BrowseSequenceMetadata, sortMethod: SortMethod): string {
		switch (sortMethod) {
			case SortMethodEnum.ALPHABETICAL:
				return sequence.word[0]?.toUpperCase() || '#';
			case SortMethodEnum.DIFFICULTY_LEVEL:
				return sequence.difficultyLevel || 'Unknown';
			case SortMethodEnum.AUTHOR:
				return sequence.author || 'Unknown';
			case SortMethodEnum.SEQUENCE_LENGTH: {
				const length = sequence.sequenceLength || 0;
				if (length <= 4) return '3-4 beats';
				if (length <= 6) return '5-6 beats';
				if (length <= 8) return '7-8 beats';
				return '9+ beats';
			}
			default:
				return 'All';
		}
	}

	clearCache(): void {
		this.cachedSequences = null;
	}
}
