/**
 * Local Storage Persistence Service
 * 
 * Handles data persistence using browser localStorage.
 * This provides a simple persistence layer for sequences and settings.
 */

import type { SequenceData } from '@tka/schemas';
import type { IPersistenceService } from '../interfaces';

export class LocalStoragePersistenceService implements IPersistenceService {
	private readonly SEQUENCES_KEY = 'tka-v2-sequences';
	private readonly SEQUENCE_PREFIX = 'tka-v2-sequence-';

	/**
	 * Save a sequence to localStorage
	 */
	async saveSequence(sequence: SequenceData): Promise<void> {
		try {
			// Save individual sequence
			const sequenceKey = `${this.SEQUENCE_PREFIX}${sequence.id}`;
			localStorage.setItem(sequenceKey, JSON.stringify(sequence));

			// Update sequence index
			await this.updateSequenceIndex(sequence);

			console.log(`Sequence "${sequence.name}" saved successfully`);
		} catch (error) {
			console.error('Failed to save sequence:', error);
			throw new Error(`Failed to save sequence: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Load a sequence by ID
	 */
	async loadSequence(id: string): Promise<SequenceData | null> {
		try {
			const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
			const data = localStorage.getItem(sequenceKey);

			if (!data) {
				return null;
			}

			const sequence = JSON.parse(data) as SequenceData;
			return this.validateSequenceData(sequence);
		} catch (error) {
			console.error(`Failed to load sequence ${id}:`, error);
			return null;
		}
	}

	/**
	 * Load all sequences
	 */
	async loadAllSequences(): Promise<SequenceData[]> {
		try {
			const indexData = localStorage.getItem(this.SEQUENCES_KEY);
			if (!indexData) {
				return [];
			}

			const sequenceIds = JSON.parse(indexData) as string[];
			const sequences: SequenceData[] = [];

			for (const id of sequenceIds) {
				const sequence = await this.loadSequence(id);
				if (sequence) {
					sequences.push(sequence);
				}
			}

			return sequences.sort((a, b) => {
				// Sort by creation date, newest first
				const aDate = new Date(a.createdAt || 0).getTime();
				const bDate = new Date(b.createdAt || 0).getTime();
				return bDate - aDate;
			});
		} catch (error) {
			console.error('Failed to load sequences:', error);
			return [];
		}
	}

	/**
	 * Delete a sequence
	 */
	async deleteSequence(id: string): Promise<void> {
		try {
			// Remove individual sequence
			const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
			localStorage.removeItem(sequenceKey);

			// Update sequence index
			await this.removeFromSequenceIndex(id);

			console.log(`Sequence ${id} deleted successfully`);
		} catch (error) {
			console.error(`Failed to delete sequence ${id}:`, error);
			throw new Error(`Failed to delete sequence: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Update the sequence index with a new or updated sequence
	 */
	private async updateSequenceIndex(sequence: SequenceData): Promise<void> {
		try {
			const indexData = localStorage.getItem(this.SEQUENCES_KEY);
			const sequenceIds = indexData ? JSON.parse(indexData) as string[] : [];

			// Add sequence ID if not already present
			if (!sequenceIds.includes(sequence.id)) {
				sequenceIds.push(sequence.id);
				localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(sequenceIds));
			}
		} catch (error) {
			console.error('Failed to update sequence index:', error);
		}
	}

	/**
	 * Remove a sequence ID from the index
	 */
	private async removeFromSequenceIndex(id: string): Promise<void> {
		try {
			const indexData = localStorage.getItem(this.SEQUENCES_KEY);
			if (!indexData) return;

			const sequenceIds = JSON.parse(indexData) as string[];
			const filteredIds = sequenceIds.filter(existingId => existingId !== id);

			localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(filteredIds));
		} catch (error) {
			console.error('Failed to remove from sequence index:', error);
		}
	}

	/**
	 * Validate sequence data structure
	 */
	private validateSequenceData(data: any): SequenceData {
		// Basic validation - ensure required fields exist
		if (!data.id || !data.name || !Array.isArray(data.beats)) {
			throw new Error('Invalid sequence data structure');
		}

		// Ensure all required fields have defaults
		return {
			id: data.id,
			name: data.name,
			beats: data.beats || [],
			createdAt: data.createdAt || new Date().toISOString(),
			updatedAt: data.updatedAt || new Date().toISOString(),
			version: data.version || '2.0',
			length: data.length || data.beats.length,
			tags: data.tags || [],
			...data, // Preserve any additional fields
		};
	}

	/**
	 * Get storage usage statistics
	 */
	getStorageInfo(): { used: number; available: number; sequences: number } {
		try {
			// Calculate used storage (rough estimate)
			let used = 0;
			for (let i = 0; i < localStorage.length; i++) {
				const key = localStorage.key(i);
				if (key?.startsWith('tka-v2-')) {
					const value = localStorage.getItem(key);
					used += (key.length + (value?.length || 0)) * 2; // UTF-16 encoding
				}
			}

			// Get sequence count
			const indexData = localStorage.getItem(this.SEQUENCES_KEY);
			const sequenceCount = indexData ? JSON.parse(indexData).length : 0;

			return {
				used: Math.round(used / 1024), // KB
				available: 5120, // Rough estimate of 5MB localStorage limit
				sequences: sequenceCount,
			};
		} catch (error) {
			return { used: 0, available: 5120, sequences: 0 };
		}
	}
}
