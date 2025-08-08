import { createStore } from '../../core/index.js';

export const workbenchStore = createStore({
  currentTab: 'construct',
  isLoading: false
});