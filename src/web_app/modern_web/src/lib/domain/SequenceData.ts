/**
 * Sequence Domain Model
 *
 * Immutable data structure for complete kinetic sequences.
 * Based on the modern desktop app's SequenceData but adapted for TypeScript.
 */

import type { BeatData } from './BeatData';

export interface SequenceData {
	readonly id: string;
	readonly name: string;
	readonly word: string;
	readonly beats: readonly BeatData[];
	readonly start_position?: BeatData;
	readonly thumbnails: readonly string[];
	readonly sequence_length?: number;
	readonly author?: string;
	readonly level?: number;
	readonly date_added?: Date;
	readonly grid_mode?: string;
	readonly prop_type?: string;
	readonly is_favorite: boolean;
	readonly is_circular: boolean;
	readonly starting_position?: string;
	readonly difficulty_level?: string;
	readonly tags: readonly string[];
	readonly metadata: Record<string, unknown>;
}

export function createSequenceData(data: Partial<SequenceData> = {}): SequenceData {
	const result: SequenceData = {
		id: data.id ?? crypto.randomUUID(),
		name: data.name ?? '',
		word: data.word ?? '',
		beats: data.beats ?? [],
		thumbnails: data.thumbnails ?? [],
		is_favorite: data.is_favorite ?? false,
		is_circular: data.is_circular ?? false,
		tags: data.tags ?? [],
		metadata: data.metadata ?? {},
		// Optional properties - only include if defined
		...(data.sequence_length !== undefined && { sequence_length: data.sequence_length }),
		...(data.author !== undefined && { author: data.author }),
		...(data.level !== undefined && { level: data.level }),
		...(data.date_added !== undefined && { date_added: data.date_added }),
		...(data.grid_mode !== undefined && { grid_mode: data.grid_mode }),
		...(data.prop_type !== undefined && { prop_type: data.prop_type }),
		...(data.starting_position !== undefined && { starting_position: data.starting_position }),
		...(data.difficulty_level !== undefined && { difficulty_level: data.difficulty_level }),
		...(data.start_position !== undefined && { start_position: data.start_position }),
	};
	return result;
}

export function updateSequenceData(
	sequence: SequenceData,
	updates: Partial<SequenceData>
): SequenceData {
	return {
		...sequence,
		...updates,
	};
}

export function addBeatToSequence(sequence: SequenceData, beat: BeatData): SequenceData {
	return updateSequenceData(sequence, {
		beats: [...sequence.beats, beat],
	});
}

export function removeBeatFromSequence(sequence: SequenceData, beatIndex: number): SequenceData {
	if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
		return sequence;
	}

	const newBeats = sequence.beats.filter((_, index) => index !== beatIndex);
	return updateSequenceData(sequence, {
		beats: newBeats,
	});
}

export function updateBeatInSequence(
	sequence: SequenceData,
	beatIndex: number,
	beat: BeatData
): SequenceData {
	if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
		return sequence;
	}

	const newBeats = [...sequence.beats];
	newBeats[beatIndex] = beat;

	return updateSequenceData(sequence, {
		beats: newBeats,
	});
}

export function getSequenceLength(sequence: SequenceData): number {
	return sequence.beats.length;
}

export function isEmptySequence(sequence: SequenceData): boolean {
	return sequence.beats.length === 0;
}

export function hasStartPosition(sequence: SequenceData): boolean {
	return sequence.start_position != null;
}
