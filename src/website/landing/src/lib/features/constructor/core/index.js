// Core state management
export function createStore(initialState) {
  let state = initialState;
  const subscribers = [];

  return {
    subscribe: (callback) => {
      subscribers.push(callback);
      callback(state);
      return () => {
        const index = subscribers.indexOf(callback);
        if (index > -1) subscribers.splice(index, 1);
      };
    },
    set: (newState) => {
      state = newState;
      subscribers.forEach(callback => callback(state));
    },
    update: (updater) => {
      state = updater(state);
      subscribers.forEach(callback => callback(state));
    }
  };
}
