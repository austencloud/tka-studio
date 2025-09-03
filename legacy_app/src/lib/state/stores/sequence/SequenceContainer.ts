import { createContainer } from '$lib/state/core/container';
import { createDerived } from '$lib/state/core/container';
import { browser } from '$app/environment';

export interface BeatData {
	id: string;
	number: number;
	letter?: string;
	position?: string;
	orientation?: string;
	turnsTuple?: string;
	redPropData?: any;
	bluePropData?: any;
	redArrowData?: any;
	blueArrowData?: any;
	redMotionData?: any;
	blueMotionData?: any;
	metadata?: Record<string, unknown>;
}

export interface SequenceState {
	beats: BeatData[];
	selectedBeatIds: string[];
	currentBeatIndex: number;
	isModified: boolean;
	metadata: {
		name: string;
		difficulty: number;
		tags: string[];
		createdAt: Date;
		lastModified: Date;
	};
}

const initialState: SequenceState = {
	beats: [],
	selectedBeatIds: [],
	currentBeatIndex: 0,
	isModified: false,
	metadata: {
		name: '',
		difficulty: 0,
		tags: [],
		createdAt: new Date(),
		lastModified: new Date()
	}
};

function createSequenceContainer() {
	return createContainer(initialState, (state, update) => ({
		addBeat: (beat: BeatData) => {
			update((state) => {
				state.beats.push(beat);
				state.isModified = true;
				state.metadata.lastModified = new Date();
			});
		},

		addBeats: (beats: BeatData[]) => {
			update((state) => {
				state.beats.push(...beats);
				state.isModified = true;
				state.metadata.lastModified = new Date();
			});
		},

		setSequence: (beats: BeatData[]) => {
			update((state) => {
				state.beats = beats;
				state.isModified = true;
				state.currentBeatIndex = 0;
				state.selectedBeatIds = [];
				state.metadata.lastModified = new Date();
			});
		},

		removeBeat: (beatId: string) => {
			update((state) => {
				state.beats = state.beats.filter((beat) => beat.id !== beatId);
				state.selectedBeatIds = state.selectedBeatIds.filter((id) => id !== beatId);
				state.isModified = true;
				state.metadata.lastModified = new Date();
			});
		},

		updateBeat: (beatId: string, updates: Partial<BeatData>) => {
			update((state) => {
				const beatIndex = state.beats.findIndex((beat) => beat.id === beatId);
				if (beatIndex >= 0) {
					state.beats[beatIndex] = { ...state.beats[beatIndex], ...updates };
					state.isModified = true;
					state.metadata.lastModified = new Date();
				}
			});
		},

		selectBeat: (beatId: string, multiSelect = false) => {
			update((state) => {
				// If multi-select is enabled, toggle the selection
				if (multiSelect) {
					// If already selected, deselect it
					if (state.selectedBeatIds.includes(beatId)) {
						state.selectedBeatIds = state.selectedBeatIds.filter((id) => id !== beatId);
					} else {
						// Otherwise add it to the selection
						state.selectedBeatIds.push(beatId);
					}
				} else {
					// If not multi-select, replace the selection with just this beat
					state.selectedBeatIds = [beatId];
				}

				// Log selection state for debugging
				if (typeof console !== 'undefined') {
					console.debug('Beat selection updated:', {
						beatId,
						multiSelect,
						selectedBeatIds: state.selectedBeatIds
					});
				}
			});
		},

		deselectBeat: (beatId: string) => {
			update((state) => {
				state.selectedBeatIds = state.selectedBeatIds.filter((id) => id !== beatId);
			});
		},

		clearSelection: () => {
			update((state) => {
				state.selectedBeatIds = [];
			});
		},

		setCurrentBeatIndex: (index: number) => {
			update((state) => {
				state.currentBeatIndex = index;
			});
		},

		updateMetadata: (metadata: Partial<SequenceState['metadata']>) => {
			update((state) => {
				state.metadata = {
					...state.metadata,
					...metadata,
					lastModified: new Date()
				};
				state.isModified = true;
			});
		},

		markAsSaved: () => {
			update((state) => {
				state.isModified = false;
			});
		},

		/**
		 * Save the sequence to localStorage.
		 * Handles edge cases, errors and ensures proper saving of sequence data.
		 */
		saveToLocalStorage: () => {
			if (!browser) return;

			try {
				import('$lib/utils/pictographUtils')
					.then(({ createSafeBeatCopy }) => {
						try {
							const beats = state.beats;

							const safeBeats = beats.map((beat) => {
								const safeBeat = createSafeBeatCopy(beat);

								if (!safeBeat.pictographData && beat.metadata) {
									safeBeat.pictographData = {
										letter: beat.letter || beat.metadata.letter || null,
										startPos: beat.position || beat.metadata.startPos || null,
										endPos: beat.metadata.endPos || null,
										gridMode: beat.metadata.gridMode || 'diamond',
										redPropData: beat.redPropData || null,
										bluePropData: beat.bluePropData || null,
										redMotionData: beat.redMotionData || null,
										blueMotionData: beat.blueMotionData || null,
										redArrowData: beat.redArrowData || null,
										blueArrowData: beat.blueArrowData || null,
										grid: beat.metadata.grid || '',
										timing: null,
										direction: null,
										gridData: null,
										motions: [],
										redMotion: null,
										blueMotion: null,
										props: []
									};
								}

								return safeBeat;
							});

							const letters = beats
								.map((beat) => {
									return (
										beat.letter ||
										(beat.metadata && typeof beat.metadata.letter === 'string'
											? beat.metadata.letter
											: null)
									);
								})
								.filter((letter): letter is string => letter !== null);

							const word = letters.join('');

							update((state) => {
								state.metadata.name = word;
							});

							const safeState = {
								...state,
								beats: safeBeats
							};

							localStorage.setItem('sequence', JSON.stringify(safeState));
						} catch (innerError) {
							console.error('Error in saveToLocalStorage inner function:', innerError);
						}
					})
					.catch((importError) => {
						console.error('Error importing pictographUtils:', importError);
					});
			} catch (outerError) {
				console.error('Failed to save sequence to localStorage:', outerError);
			}
		},

		/**
		 * Load the sequence from localStorage.
		 * Handles edge cases, errors and restores the start position when loading a sequence.
		 */
		loadFromLocalStorage: () => {
			if (!browser) return false;

			try {
				const savedSequence = localStorage.getItem('sequence');
				if (!savedSequence) {
					return false;
				}

				const parsed = JSON.parse(savedSequence);

				if (parsed.beats && Array.isArray(parsed.beats)) {
					parsed.beats = parsed.beats.map((beat: any) => {
						if (!beat.pictographData && beat.metadata) {
							beat.pictographData = {
								letter: beat.letter || beat.metadata.letter || null,
								startPos: beat.position || beat.metadata.startPos || null,
								endPos: beat.metadata.endPos || null,
								gridMode: beat.metadata.gridMode || 'diamond',
								redPropData: beat.redPropData || null,
								bluePropData: beat.bluePropData || null,
								redMotionData: beat.redMotionData || null,
								blueMotionData: beat.blueMotionData || null,
								redArrowData: beat.redArrowData || null,
								blueArrowData: beat.blueArrowData || null,
								grid: beat.metadata.grid || '',
								timing: null,
								direction: null,
								gridData: null,
								motions: [],
								redMotion: null,
								blueMotion: null,
								props: []
							};
						}

						return {
							id: beat.id || `beat-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`,
							number: beat.number || 0,
							letter: beat.letter || beat.metadata?.letter || null,
							position: beat.position || beat.metadata?.startPos || null,
							orientation: beat.orientation || '',
							turnsTuple: beat.turnsTuple || '',
							redPropData: beat.redPropData || beat.pictographData?.redPropData || null,
							bluePropData: beat.bluePropData || beat.pictographData?.bluePropData || null,
							redArrowData: beat.redArrowData || beat.pictographData?.redArrowData || null,
							blueArrowData: beat.blueArrowData || beat.pictographData?.blueArrowData || null,
							redMotionData: beat.redMotionData || beat.pictographData?.redMotionData || null,
							blueMotionData: beat.blueMotionData || beat.pictographData?.blueMotionData || null,
							metadata: beat.metadata || {},
							pictographData: beat.pictographData || null
						};
					});
				}

				update((state) => {
					Object.assign(state, parsed);
					state.metadata.createdAt = new Date(state.metadata.createdAt);
					state.metadata.lastModified = new Date(state.metadata.lastModified);

					if (state.beats && state.beats.length > 0) {
						const letters = state.beats
							.map((beat) => {
								return (
									beat.letter ||
									(beat.metadata && typeof beat.metadata.letter === 'string'
										? beat.metadata.letter
										: null)
								);
							})
							.filter((letter): letter is string => letter !== null);

						const word = letters.join('');

						state.metadata.name = word;
					} else {
						state.metadata.name = '';
					}
				});

				try {
					Promise.all([
						import('$lib/stores/sequence/selectionStore'),
						import('$lib/state/stores/pictograph/pictographContainer')
					]).then(([{ selectedStartPos }, { pictographContainer }]) => {
						const savedStartPos = localStorage.getItem('start_position');
						let startPosData = null;

						if (savedStartPos) {
							try {
								startPosData = JSON.parse(savedStartPos);
							} catch (parseError) {
								console.error('Failed to parse start position from localStorage:', parseError);
							}
						}

						if (startPosData) {
							if (startPosData.redMotionData) {
								startPosData.redMotionData.endLoc = startPosData.redMotionData.startLoc;
							}
							if (startPosData.blueMotionData) {
								startPosData.blueMotionData.endLoc = startPosData.blueMotionData.startLoc;
							}

							startPosData.isStartPosition = true;

							const startPosCopy = JSON.parse(JSON.stringify(startPosData));

							selectedStartPos.set(startPosCopy);

							pictographContainer.setData(startPosCopy);

							if (typeof document !== 'undefined') {
								const event = new CustomEvent('start-position-selected', {
									detail: { startPosition: startPosCopy },
									bubbles: true
								});
								document.dispatchEvent(event);
							}
						}
					});
				} catch (startPosError) {
					console.error('Failed to restore start position:', startPosError);
				}

				return true;
			} catch (e) {
				console.error('Failed to load sequence from localStorage:', e);
				return false;
			}
		}
	}));
}

export const sequenceContainer = createSequenceContainer();

export const selectedBeats = createDerived(() =>
	sequenceContainer.state.beats.filter((beat) =>
		sequenceContainer.state.selectedBeatIds.includes(beat.id)
	)
);

export const currentBeat = createDerived(
	() => sequenceContainer.state.beats[sequenceContainer.state.currentBeatIndex] || null
);

export const beatCount = createDerived(() => sequenceContainer.state.beats.length);

export const sequenceDifficulty = createDerived(() => sequenceContainer.state.metadata.difficulty);

if (browser) {
	let saveTimeoutId: ReturnType<typeof setTimeout> | null = null;
	let lastSavedState = JSON.stringify({
		beats: sequenceContainer.state.beats.length,
		metadata: sequenceContainer.state.metadata.name
	});

	const debouncedSave = () => {
		if (saveTimeoutId) {
			clearTimeout(saveTimeoutId);
		}
		saveTimeoutId = setTimeout(() => {
			const currentState = JSON.stringify({
				beats: sequenceContainer.state.beats.length,
				metadata: sequenceContainer.state.metadata.name
			});

			if (currentState !== lastSavedState) {
				sequenceContainer.saveToLocalStorage();
				lastSavedState = currentState;
			}

			saveTimeoutId = null;
		}, 0);
	};

	sequenceContainer.subscribe((state) => {
		if (state.isModified) {
			debouncedSave();
		}
	});

	window.addEventListener('beforeunload', () => {
		if (saveTimeoutId) {
			clearTimeout(saveTimeoutId);
			saveTimeoutId = null;

			const currentState = JSON.stringify({
				beats: sequenceContainer.state.beats.length,
				metadata: sequenceContainer.state.metadata.name
			});

			if (currentState !== lastSavedState && sequenceContainer.state.isModified) {
				sequenceContainer.saveToLocalStorage();
			}
		}
	});
}
