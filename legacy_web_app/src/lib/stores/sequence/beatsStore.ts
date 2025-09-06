/**
 * @deprecated This file is deprecated and will be removed in a future version.
 * Use sequenceStore from '$lib/state/stores/sequence/sequenceAdapter' instead.
 */

import { sequenceStore } from '$lib/state/stores/sequence/sequenceAdapter';
import type { BeatData as LegacyBeatData } from '$lib/components/SequenceWorkbench/BeatFrame/BeatData';
import type { BeatData as ModernBeatData } from '$lib/state/stores/sequence/SequenceContainer';
import { derived, get, type Writable } from 'svelte/store';

// Type adapter functions to convert between legacy and modern BeatData types
function convertToModernBeat(legacyBeat: LegacyBeatData): ModernBeatData {
	return {
		id: legacyBeat.id || `beat-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`,
		number: legacyBeat.beatNumber,
		// Copy all other properties from the legacy beat
		...legacyBeat
	} as unknown as ModernBeatData;
}

function convertToLegacyBeat(modernBeat: ModernBeatData): LegacyBeatData {
	return {
		id: modernBeat.id,
		beatNumber: modernBeat.number,
		filled: (modernBeat as any).filled || true,
		pictographData: (modernBeat as any).pictographData || {}
	} as unknown as LegacyBeatData;
}

// Create a compatibility layer for the old beatsStore
export const beatsStore: Writable<LegacyBeatData[]> = {
	subscribe: derived(sequenceStore, ($store) => $store.beats.map(convertToLegacyBeat)).subscribe,

	set: (beats: LegacyBeatData[]) => {
		sequenceStore.setSequence(beats.map(convertToModernBeat));
	},

	update: (updater: (beats: LegacyBeatData[]) => LegacyBeatData[]) => {
		const currentBeats = get(sequenceStore).beats.map(convertToLegacyBeat);
		const newBeats = updater(currentBeats);
		sequenceStore.setSequence(newBeats.map(convertToModernBeat));
	}
};

// Compatibility function for getBeats
export function getBeats(): LegacyBeatData[] {
	return get(sequenceStore).beats.map(convertToLegacyBeat);
}
