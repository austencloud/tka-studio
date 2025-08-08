import { createStore } from '../../core/index.js';

export const sequenceStore = createStore({
  beats: [],
  metadata: { name: '', difficulty: 1 }
});