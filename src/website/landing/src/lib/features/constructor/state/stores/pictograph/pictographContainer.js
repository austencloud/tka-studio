import { createContainer } from '../../../core/container.js';

export const pictographContainer = createContainer(
  {
    currentPictograph: null,
    isLoading: false,
    error: null,
    renderSettings: {
      showArrows: true,
      showGrid: false,
      size: 100
    }
  },
  (state, update) => ({
    setPictograph: (pictograph) => {
      update((state) => {
        state.currentPictograph = pictograph;
        state.isLoading = false;
        state.error = null;
      });
    },
    setLoading: (loading) => {
      update((state) => {
        state.isLoading = loading;
      });
    },
    setError: (error) => {
      update((state) => {
        state.error = error;
        state.isLoading = false;
      });
    },
    updateRenderSettings: (settings) => {
      update((state) => {
        state.renderSettings = { ...state.renderSettings, ...settings };
      });
    }
  })
);
