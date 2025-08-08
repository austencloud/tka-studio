// Sequence machine actions and selectors
export const sequenceActions = {
  addBeat: (beat) => console.log('Add beat:', beat),
  removeBeat: (index) => console.log('Remove beat:', index),
  clearSequence: () => console.log('Clear sequence')
};

export const sequenceSelectors = {
  getBeats: () => [],
  getBeatCount: () => 0
};