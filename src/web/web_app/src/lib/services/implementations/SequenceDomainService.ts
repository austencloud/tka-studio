/**
 * Sequence Domain Service - REAL Business Logic from Desktop
 *
 * Ported from desktop.modern.application.services.sequence.beat_sequence_service
 * and desktop.modern.domain.models for actual validation and business rules.
 */

import type { BeatData, SequenceData } from '$lib/domain';
import type {
	ISequenceDomainService,
	SequenceCreateRequest,
	ValidationResult,
} from '../interfaces';

export class SequenceDomainService implements ISequenceDomainService {
	/**
	 * Validate sequence creation request - REAL validation from desktop
	 */
	validateCreateRequest(request: SequenceCreateRequest): ValidationResult {
		const errors: string[] = [];

		// Validation from desktop SequenceData.__post_init__
		if (!request.name || request.name.trim().length === 0) {
			errors.push('Sequence name is required');
		}

		if (request.name && request.name.length > 100) {
			errors.push('Sequence name must be less than 100 characters');
		}

		// Length validation from desktop domain models
		// Allow 0 length for progressive creation (start position only)
		if (request.length !== undefined && (request.length < 0 || request.length > 64)) {
			errors.push('Sequence length must be between 0 and 64');
		}

		// Grid mode validation from desktop enums
		if (request.gridMode && !['diamond', 'box'].includes(request.gridMode)) {
			errors.push('Grid mode must be either "diamond" or "box"');
		}

		return {
			isValid: errors.length === 0,
			errors,
		};
	}

	/**
	 * Create sequence with proper beat numbering - from desktop SequenceData
	 */
	createSequence(request: SequenceCreateRequest): SequenceData {
		const validation = this.validateCreateRequest(request);
		if (!validation.isValid) {
			throw new Error(`Invalid sequence request: ${validation.errors.join(', ')}`);
		}

		// Create beats with proper numbering (desktop logic)
		const beats: BeatData[] = [];
		for (let i = 1; i <= request.length; i++) {
			beats.push(this.createEmptyBeat(i));
		}

		// Create sequence following desktop SequenceData structure
		const sequence: SequenceData = {
			id: this.generateId(),
			name: request.name.trim(),
			word: '',
			beats,
			thumbnails: [],
			is_favorite: false,
			is_circular: false,
			tags: [],
			metadata: { length: request.length },
		};

		return sequence;
	}

	/**
	 * Update beat with proper validation - from desktop BeatSequenceService
	 */
	updateBeat(sequence: SequenceData, beatIndex: number, beatData: BeatData): SequenceData {
		// Validation from desktop BeatSequenceService
		if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
			throw new Error(`Invalid beat index: ${beatIndex}`);
		}

		// Validate beat data
		if (beatData.duration && beatData.duration < 0) {
			throw new Error('Beat duration must be positive');
		}

		// Legacy field guard (beatNumber) for migrated data
		if (typeof (beatData as unknown as { beatNumber?: number }).beatNumber === 'number') {
			if ((beatData as unknown as { beatNumber: number }).beatNumber < 0) {
				throw new Error('Beat number must be non-negative');
			}
		}

		// Create new beats array with updated beat
		const newBeats = [...sequence.beats];
		newBeats[beatIndex] = { ...beatData };

		return { ...sequence, beats: newBeats } as SequenceData;
	}

	/**
	 * Calculate sequence word - from desktop SequenceWordCalculator
	 */
	calculateSequenceWord(sequence: SequenceData): string {
		if (!sequence.beats || sequence.beats.length === 0) {
			return '';
		}

		// Extract letters from beats (desktop logic)
		const word = sequence.beats
			.map((beat) => beat.pictograph_data?.letter || beat.metadata?.letter || '?')
			.join('');

		// Apply word simplification for circular sequences (desktop logic)
		return this.simplifyRepeatedWord(word);
	}

	/**
	 * Simplify repeated patterns - from desktop WordSimplifier
	 */
	private simplifyRepeatedWord(word: string): string {
		if (!word) return word;

		const canFormByRepeating = (s: string, pattern: string): boolean => {
			const patternLen = pattern.length;
			for (let i = 0; i < s.length; i += patternLen) {
				if (s.slice(i, i + patternLen) !== pattern) {
					return false;
				}
			}
			return true;
		};

		const n = word.length;

		// Try each possible pattern length from smallest to largest
		for (let i = 1; i <= Math.floor(n / 2); i++) {
			const pattern = word.slice(0, i);
			if (n % i === 0 && canFormByRepeating(word, pattern)) {
				return pattern;
			}
		}

		return word;
	}

	/**
	 * Create empty beat - from desktop BeatData structure
	 */
	private createEmptyBeat(beatNumber: number): BeatData {
		return {
			id: crypto.randomUUID(),
			beat_number: beatNumber,
			duration: 1.0,
			blue_reversal: false,
			red_reversal: false,
			is_blank: true,
			pictograph_data: null,
			metadata: {},
		};
	}

	/**
	 * Generate unique ID - following desktop pattern
	 */
	private generateId(): string {
		return `seq_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
	}
}
