// Container utilities
import { createStore } from "./index.js";

export function createContainer(initialState, actions) {
  const store = createStore(initialState);

  // If no actions provided, just return the store
  if (!actions) {
    return store;
  }

  // Create actions with update function
  const boundActions = actions(initialState, (updater) => {
    store.update(updater);
  });

  // Return store with actions
  return {
    ...store,
    ...boundActions,
    reset: () => store.set(initialState),
  };
}

export function createDerived(stores, fn) {
  // Simple derived store implementation
  return {
    subscribe: (callback) => {
      return stores.subscribe((value) => callback(fn(value)));
    },
  };
}
