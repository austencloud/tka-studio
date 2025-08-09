import { w as writable, k as get } from "./vendor.js";
function safeClone(obj) {
  if (obj === null || obj === void 0 || typeof obj !== "object") {
    return obj;
  }
  const seen = /* @__PURE__ */ new WeakMap();
  const isBrowser = typeof window !== "undefined" && typeof document !== "undefined";
  const isInstanceOf = (obj2, className) => {
    if (!isBrowser) return false;
    try {
      const constructor = window[className];
      return constructor && obj2 instanceof constructor;
    } catch (e) {
      return false;
    }
  };
  const isDomNode = (obj2) => {
    if (!isBrowser) return false;
    return obj2 && typeof obj2 === "object" && // Has nodeType property (all DOM nodes have this)
    (typeof obj2.nodeType === "number" || // Has common DOM element methods
    typeof obj2.appendChild === "function" && typeof obj2.getAttribute === "function" || // Check constructor name for common DOM types
    obj2.constructor && /^HTML.*Element$/.test(obj2.constructor.name));
  };
  function isCloneable(value) {
    if (value === null || value === void 0 || typeof value !== "object") {
      return true;
    }
    if (typeof value === "function" || isDomNode(value) || isInstanceOf(value, "Window") || value instanceof Promise || value instanceof Error || value instanceof WeakMap || value instanceof WeakSet || // Check for custom class instances (not plain objects or arrays)
    value.constructor && value.constructor.name !== "Object" && value.constructor.name !== "Array" && value.constructor.name !== "Date" && value.constructor.name !== "RegExp" && value.constructor.name !== "Map" && value.constructor.name !== "Set") {
      return false;
    }
    return true;
  }
  function deepClone(value, path = []) {
    if (value === null || value === void 0 || typeof value !== "object") {
      return value;
    }
    if (seen.has(value)) {
      return seen.get(value);
    }
    if (!isCloneable(value)) {
      if (isDomNode(value) || isInstanceOf(value, "Window")) {
        return null;
      }
      if (typeof value === "function") {
        return function noopReplacement() {
          return null;
        };
      }
      return {};
    }
    if (value instanceof Date) {
      return new Date(value.getTime());
    }
    if (value instanceof RegExp) {
      return new RegExp(value.source, value.flags);
    }
    if (value instanceof Map) {
      const clonedMap = /* @__PURE__ */ new Map();
      seen.set(value, clonedMap);
      value.forEach((val, key) => {
        clonedMap.set(deepClone(key, [...path, "map-key"]), deepClone(val, [...path, "map-value"]));
      });
      return clonedMap;
    }
    if (value instanceof Set) {
      const clonedSet = /* @__PURE__ */ new Set();
      seen.set(value, clonedSet);
      value.forEach((val) => {
        clonedSet.add(deepClone(val, [...path, "set-value"]));
      });
      return clonedSet;
    }
    if (Array.isArray(value)) {
      const clonedArray = [];
      seen.set(value, clonedArray);
      for (let i = 0; i < value.length; i++) {
        clonedArray[i] = deepClone(value[i], [...path, i.toString()]);
      }
      return clonedArray;
    }
    const clonedObj = {};
    seen.set(value, clonedObj);
    for (const key in value) {
      if (Object.prototype.hasOwnProperty.call(value, key)) {
        try {
          clonedObj[key] = deepClone(value[key], [...path, key]);
        } catch (err) {
          clonedObj[key] = null;
        }
      }
    }
    return clonedObj;
  }
  try {
    let canUseStructuredClone = true;
    if (typeof obj === "object" && obj !== null) {
      for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
          const value = obj[key];
          if (!isCloneable(value)) {
            canUseStructuredClone = false;
            break;
          }
        }
      }
    }
    if (canUseStructuredClone) {
      return structuredClone(obj);
    }
  } catch (error) {
  }
  return deepClone(obj);
}
function createContainer(initialState2, actions) {
  const store = writable(safeClone(initialState2));
  const update = (fn) => {
    store.update((currentState) => {
      const copy = safeClone(currentState);
      fn(copy);
      return copy;
    });
  };
  const boundActions = actions(
    // Proxy that forwards property access to the store value
    new Proxy({}, {
      get: (_, prop) => {
        const value = get(store);
        return value[prop];
      },
      set: (_, prop, value) => {
        store.update((state) => {
          const newState = { ...state };
          newState[prop] = value;
          return newState;
        });
        return true;
      }
    }),
    update
  );
  const reset = () => {
    store.set(safeClone(initialState2));
  };
  const container = {
    get state() {
      return get(store);
    },
    ...boundActions,
    reset,
    // Add subscribe method for compatibility with Svelte stores
    subscribe: store.subscribe
  };
  return container;
}
function createDerived(fn) {
  const store = writable(fn());
  return {
    get value() {
      return get(store);
    },
    _update: () => {
      store.set(fn());
    }
  };
}
const initialState = {
  beats: [],
  selectedBeatIds: [],
  currentBeatIndex: 0,
  isModified: false,
  metadata: {
    name: "",
    difficulty: 0,
    tags: [],
    createdAt: /* @__PURE__ */ new Date(),
    lastModified: /* @__PURE__ */ new Date()
  }
};
function createSequenceContainer() {
  return createContainer(initialState, (state, update) => ({
    addBeat: (beat) => {
      update((state2) => {
        state2.beats.push(beat);
        state2.isModified = true;
        state2.metadata.lastModified = /* @__PURE__ */ new Date();
      });
    },
    addBeats: (beats) => {
      update((state2) => {
        state2.beats.push(...beats);
        state2.isModified = true;
        state2.metadata.lastModified = /* @__PURE__ */ new Date();
      });
    },
    setSequence: (beats) => {
      update((state2) => {
        state2.beats = beats;
        state2.isModified = true;
        state2.currentBeatIndex = 0;
        state2.selectedBeatIds = [];
        state2.metadata.lastModified = /* @__PURE__ */ new Date();
      });
    },
    removeBeat: (beatId) => {
      update((state2) => {
        state2.beats = state2.beats.filter((beat) => beat.id !== beatId);
        state2.selectedBeatIds = state2.selectedBeatIds.filter((id) => id !== beatId);
        state2.isModified = true;
        state2.metadata.lastModified = /* @__PURE__ */ new Date();
      });
    },
    updateBeat: (beatId, updates) => {
      update((state2) => {
        const beatIndex = state2.beats.findIndex((beat) => beat.id === beatId);
        if (beatIndex >= 0) {
          state2.beats[beatIndex] = { ...state2.beats[beatIndex], ...updates };
          state2.isModified = true;
          state2.metadata.lastModified = /* @__PURE__ */ new Date();
        }
      });
    },
    selectBeat: (beatId, multiSelect = false) => {
      update((state2) => {
        if (multiSelect) {
          if (state2.selectedBeatIds.includes(beatId)) {
            state2.selectedBeatIds = state2.selectedBeatIds.filter((id) => id !== beatId);
          } else {
            state2.selectedBeatIds.push(beatId);
          }
        } else {
          state2.selectedBeatIds = [beatId];
        }
        if (typeof console !== "undefined") {
          console.debug("Beat selection updated:", {
            beatId,
            multiSelect,
            selectedBeatIds: state2.selectedBeatIds
          });
        }
      });
    },
    deselectBeat: (beatId) => {
      update((state2) => {
        state2.selectedBeatIds = state2.selectedBeatIds.filter((id) => id !== beatId);
      });
    },
    clearSelection: () => {
      update((state2) => {
        state2.selectedBeatIds = [];
      });
    },
    setCurrentBeatIndex: (index) => {
      update((state2) => {
        state2.currentBeatIndex = index;
      });
    },
    updateMetadata: (metadata) => {
      update((state2) => {
        state2.metadata = {
          ...state2.metadata,
          ...metadata,
          lastModified: /* @__PURE__ */ new Date()
        };
        state2.isModified = true;
      });
    },
    markAsSaved: () => {
      update((state2) => {
        state2.isModified = false;
      });
    },
    /**
     * Save the sequence to localStorage.
     * Handles edge cases, errors and ensures proper saving of sequence data.
     */
    saveToLocalStorage: () => {
      return;
    },
    /**
     * Load the sequence from localStorage.
     * Handles edge cases, errors and restores the start position when loading a sequence.
     */
    loadFromLocalStorage: () => {
      return false;
    }
  }));
}
const sequenceContainer = createSequenceContainer();
const selectedBeats = createDerived(
  () => sequenceContainer.state.beats.filter(
    (beat) => sequenceContainer.state.selectedBeatIds.includes(beat.id)
  )
);
const currentBeat = createDerived(
  () => sequenceContainer.state.beats[sequenceContainer.state.currentBeatIndex] || null
);
const beatCount = createDerived(() => sequenceContainer.state.beats.length);
const sequenceDifficulty = createDerived(() => sequenceContainer.state.metadata.difficulty);
const SequenceContainer = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  beatCount,
  currentBeat,
  selectedBeats,
  sequenceContainer,
  sequenceDifficulty
}, Symbol.toStringTag, { value: "Module" }));
export {
  SequenceContainer as S,
  createDerived as a,
  createContainer as c,
  sequenceContainer as s
};
