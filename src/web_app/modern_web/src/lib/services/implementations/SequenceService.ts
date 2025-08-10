/**
 * Sequence Service - Application Layer
 *
 * Coordinates between domain logic and persistence for sequence operations.
 * This service orchestrates the business workflows for sequence management.
 */

import type { BeatData, SequenceData } from '$lib/domain';
import type {
	IPersistenceService,
	ISequenceDomainService,
	ISequenceService,
	SequenceCreateRequest,
} from '../interfaces';

export class SequenceService implements ISequenceService {
	constructor(
		private sequenceDomainService: ISequenceDomainService,
		private persistenceService: IPersistenceService
	) {}

	/**
	 * Create a new sequence
	 */
	async createSequence(request: SequenceCreateRequest): Promise<SequenceData> {
		try {
			console.log('Creating sequence:', request);

			// Use domain service to create the sequence
			const sequence = this.sequenceDomainService.createSequence(request);
			await this.persistenceService.saveSequence(sequence);
			console.log('Sequence created successfully:', sequence.id);
			return sequence;
		} catch (error) {
			console.error('Failed to create sequence:', error);
			throw new Error(
				`Failed to create sequence: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Update a beat in a sequence
	 */
	async updateBeat(sequenceId: string, beatIndex: number, beatData: BeatData): Promise<void> {
		try {
			console.log(`Updating beat ${beatIndex} in sequence ${sequenceId}`);

			// Load the current sequence
			const currentSequence = await this.persistenceService.loadSequence(sequenceId);
			if (!currentSequence) {
				throw new Error(`Sequence ${sequenceId} not found`);
			}

			// Use domain service to update the beat
			const updatedSequence = this.sequenceDomainService.updateBeat(
				currentSequence,
				beatIndex,
				beatData
			);

			await this.persistenceService.saveSequence(updatedSequence);

			console.log('Beat updated successfully');
		} catch (error) {
			console.error('Failed to update beat:', error);
			throw new Error(
				`Failed to update beat: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Set the start position for a sequence
	 */
	async setSequenceStartPosition(sequenceId: string, startPosition: BeatData): Promise<void> {
		try {
			console.log(`Setting start position for sequence ${sequenceId}`);

			// Load the current sequence
			const currentSequence = await this.persistenceService.loadSequence(sequenceId);
			if (!currentSequence) {
				throw new Error(`Sequence ${sequenceId} not found`);
			}

			// Update the sequence with the start position
			const updatedSequence = {
				...currentSequence,
				start_position: startPosition,
			} as SequenceData;

			await this.persistenceService.saveSequence(updatedSequence);

			console.log('Start position set successfully');
		} catch (error) {
			console.error('Failed to set start position:', error);
			throw new Error(
				`Failed to set start position: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Delete a sequence
	 */
	async deleteSequence(id: string): Promise<void> {
		try {
			console.log(`Deleting sequence ${id}`);
			await this.persistenceService.deleteSequence(id);
			console.log('Sequence deleted successfully');
		} catch (error) {
			console.error('Failed to delete sequence:', error);
			throw new Error(
				`Failed to delete sequence: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Get a sequence by ID
	 */
	async getSequence(id: string): Promise<SequenceData | null> {
		try {
			return await this.persistenceService.loadSequence(id);
		} catch (error) {
			console.error(`Failed to get sequence ${id}:`, error);
			return null;
		}
	}

	/**
	 * Get all sequences
	 */
	async getAllSequences(): Promise<SequenceData[]> {
		try {
			return await this.persistenceService.loadAllSequences();
		} catch (error) {
			console.error('Failed to get all sequences:', error);
			return [];
		}
	}

	/**
	 * Add a beat to a sequence
	 */
	async addBeat(sequenceId: string, beatData?: Partial<BeatData>): Promise<void> {
		try {
			const sequence = await this.getSequence(sequenceId);
			if (!sequence) {
				throw new Error(`Sequence ${sequenceId} not found`);
			}

			// Create new beat with next beat number
			const nextBeatNumber = sequence.beats.length + 1;
			const newBeat: BeatData = {
				id: crypto.randomUUID(),
				beat_number: nextBeatNumber,
				duration: 1.0,
				blue_reversal: false,
				red_reversal: false,
				is_blank: true,
				pictograph_data: null,
				metadata: {},
				...beatData,
			};
			const updatedSequence = {
				...sequence,
				beats: [...sequence.beats, newBeat],
			} as SequenceData;
			await this.persistenceService.saveSequence(updatedSequence);
		} catch (error) {
			console.error('Failed to add beat:', error);
			throw new Error(
				`Failed to add beat: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Remove a beat from a sequence
	 */
	async removeBeat(sequenceId: string, beatIndex: number): Promise<void> {
		try {
			const sequence = await this.getSequence(sequenceId);
			if (!sequence) {
				throw new Error(`Sequence ${sequenceId} not found`);
			}

			if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
				throw new Error(`Beat index ${beatIndex} is out of range`);
			}

			// Remove the beat and renumber remaining beats
			const newBeats = sequence.beats
				.filter((_, index) => index !== beatIndex)
				.map((beat, index) => ({ ...beat, beat_number: index + 1 }));
			const updatedSequence = { ...sequence, beats: newBeats } as SequenceData;
			await this.persistenceService.saveSequence(updatedSequence);
		} catch (error) {
			console.error('Failed to remove beat:', error);
			throw new Error(
				`Failed to remove beat: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}
}
