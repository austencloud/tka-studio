/**
 * @deprecated This file is deprecated and will be removed in a future version.
 * Use sequenceActions from '../state/machines/sequenceMachine.js' instead.
 */

import { sequenceStore } from '../state/stores/sequence/sequenceAdapter.js';
import { sequenceActions as modernSequenceActions } from '../state/machines/sequenceMachine.js';
import type { BeatData as LegacyBeatData } from '../components/SequenceWorkbench/BeatFrame/BeatData.js';
import type { BeatData as ModernBeatData } from '../state/stores/sequence/SequenceContainer.js';

// Type adapter functions to convert between legacy and modern BeatData types
function convertToModernBeat(legacyBeat: LegacyBeatData): ModernBeatData {
	return {
		id: legacyBeat.id || `beat-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`,
		number: legacyBeat.beatNumber,
		// Copy all other properties from the legacy beat
		...legacyBeat
	} as unknown as ModernBeatData;
}

// Forward all actions to the modern implementation
export const sequenceActions = {
	addBeat: (beat: LegacyBeatData) => sequenceStore.addBeat(convertToModernBeat(beat)),
	removeBeat: (beatId: string) => sequenceStore.removeBeat(beatId),
	updateBeat: (beatId: string, updates: Partial<LegacyBeatData>) =>
		sequenceStore.updateBeat(beatId, updates as any),
	clearSequence: () => sequenceStore.setSequence([]),
	generate: (options: any, type: string) => modernSequenceActions.generate(type as any, options)
};
