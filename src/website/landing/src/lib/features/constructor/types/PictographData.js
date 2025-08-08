// Pictograph data type definitions
export const PictographData = {
  // Default pictograph structure
  createDefault: () => ({
    letter: 'A',
    start_position: 'alpha1',
    end_position: 'alpha1',
    timing: 1,
    motion: {
      type: 'static',
      direction: 'none'
    },
    arrows: [],
    grid: {
      visible: false,
      size: 8
    }
  })
};
