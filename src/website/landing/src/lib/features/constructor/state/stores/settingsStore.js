import { createStore } from '../../core/index.js';

export const settingsStore = createStore({
  theme: 'system',
  hapticFeedback: true
});