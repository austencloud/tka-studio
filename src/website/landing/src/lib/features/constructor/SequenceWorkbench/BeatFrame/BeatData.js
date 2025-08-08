// Beat data structure
export const BeatData = {
  createDefault: (id, number) => ({
    id: id || `beat_${number}`,
    number: number || 1,
    letter: 'A',
    position: 'alpha1',
    orientation: 'in',
    timing: 1,
    selected: false,
    motion: {
      type: 'static',
      direction: 'none'
    }
  })
};
