/**
 * Sequence Service - Application Layer
 * 
 * Coordinates between domain logic and persistence for sequence operations.
 * This service orchestrates the business workflows for sequence management.
 */

import type { SequenceData, BeatData } from '@tka/schemas';
import type {
	ISequenceService,
	ISequenceDomainService,
	IPersistenceService,
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

			// Add timestamps
			const sequenceWithTimestamps = {
				...sequence,
				createdAt: new Date().toISOString(),
				updatedAt: new Date().toISOString(),
			};

			// Persist the sequence
			await this.persistenceService.saveSequence(sequenceWithTimestamps);

			console.log('Sequence created successfully:', sequenceWithTimestamps.id);
			return sequenceWithTimestamps;
		} catch (error) {
			console.error('Failed to create sequence:', error);
			throw new Error(`Failed to create sequence: ${error instanceof Error ? error.message : 'Unknown error'}`);
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

			// Update timestamps
			const sequenceWithTimestamp = {
				...updatedSequence,
				updatedAt: new Date().toISOString(),
			};

			// Persist the updated sequence
			await this.persistenceService.saveSequence(sequenceWithTimestamp);

			console.log('Beat updated successfully');
		} catch (error) {
			console.error('Failed to update beat:', error);
			throw new Error(`Failed to update beat: ${error instanceof Error ? error.message : 'Unknown error'}`);
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
			throw new Error(`Failed to delete sequence: ${error instanceof Error ? error.message : 'Unknown error'}`);
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
				beatNumber: nextBeatNumber,
				letter: null,
				duration: 1.0,
				blueMotion: null,
				redMotion: null,
				blueReversal: false,
				redReversal: false,
				filled: false,
				tags: [],
				metadata: null,
				...beatData, // Override with provided data
			};

			// Add the beat to the sequence
			const updatedSequence = {
				...sequence,
				beats: [...sequence.beats, newBeat],
				length: sequence.beats.length + 1,
				updatedAt: new Date().toISOString(),
			};

			await this.persistenceService.saveSequence(updatedSequence);
		} catch (error) {
			console.error('Failed to add beat:', error);
			throw new Error(`Failed to add beat: ${error instanceof Error ? error.message : 'Unknown error'}`);
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
				.map((beat, index) => ({ ...beat, beatNumber: index + 1 }));

			const updatedSequence = {
				...sequence,
				beats: newBeats,
				length: newBeats.length,
				updatedAt: new Date().toISOString(),
			};

			await this.persistenceService.saveSequence(updatedSequence);
		} catch (error) {
			console.error('Failed to remove beat:', error);
			throw new Error(`Failed to remove beat: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}
}
