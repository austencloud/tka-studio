import { w as writable, j as derived, k as get, a as attr_class, i as slot, p as pop, c as push, s as stringify, r as readable, l as attr_style, e as escape_html, b as bind_props, f as fallback, m as element, n as spread_attributes, q as attr, g as store_get, d as ensure_array_like, u as unsubscribe_stores, t as setContext, v as getContext, o as onDestroy, x as copy_payload, y as assign_payload } from "../../chunks/vendor.js";
import "clsx";
import { s as sequenceContainer, c as createContainer, a as createDerived } from "../../chunks/SequenceContainer.js";
import { a as appService, c as createStore, s as stateRegistry, L as LetterType, p as pictographDataStore, u as uiStore } from "../../chunks/uiStore.js";
import { fromCallback, createActor, setup } from "xstate";
import { u as useContainer } from "../../chunks/svelte5-integration.svelte.js";
/* empty css                                                      */
import { u as useSelector } from "../../chunks/xstate-vendor.js";
class HapticFeedbackService {
  isSupported;
  isEnabled = true;
  constructor() {
    this.isSupported = typeof navigator !== "undefined" && "vibrate" in navigator;
  }
  /**
   * Trigger haptic feedback based on the interaction type
   */
  trigger(type) {
    if (!this.isEnabled || !this.isSupported) {
      return;
    }
    try {
      switch (type) {
        case "navigation":
          this.vibrate(10);
          break;
        case "success":
          this.vibrate([50, 50, 100]);
          break;
        case "selection":
          this.vibrate(25);
          break;
        case "warning":
          this.vibrate([100, 50, 100]);
          break;
        case "error":
          this.vibrate([200, 100, 200]);
          break;
        default:
          this.vibrate(25);
      }
    } catch (error) {
      console.debug("Haptic feedback not available:", error);
    }
  }
  /**
   * Vibrate the device with the specified pattern
   */
  vibrate(pattern) {
    if (typeof navigator !== "undefined" && "vibrate" in navigator) {
      navigator.vibrate(pattern);
    }
  }
  /**
   * Enable haptic feedback
   */
  enable() {
    this.isEnabled = true;
  }
  /**
   * Disable haptic feedback
   */
  disable() {
    this.isEnabled = false;
  }
  /**
   * Check if haptic feedback is currently enabled
   */
  isHapticEnabled() {
    return this.isEnabled;
  }
  /**
   * Check if the device supports haptic feedback
   */
  isHapticSupported() {
    return this.isSupported;
  }
  /**
   * Check if haptic feedback is available (alias for isHapticSupported)
   */
  isAvailable() {
    return this.isSupported && this.isEnabled;
  }
  /**
   * Check if haptic feedback is supported (alias for isHapticSupported)
   */
  isHapticFeedbackSupported() {
    return this.isSupported;
  }
}
const hapticFeedbackService = new HapticFeedbackService();
const appActions = {
  /**
   * Change the active tab
   * @param tab The index of the tab to activate
   */
  changeTab: (tab) => {
    appService.send({ type: "CHANGE_TAB", tab });
  },
  /**
   * Toggle fullscreen mode
   */
  toggleFullScreen: () => {
    appService.send({ type: "TOGGLE_FULLSCREEN" });
  },
  /**
   * Set fullscreen mode
   * @param isFullScreen Whether to enable fullscreen mode
   */
  setFullScreen: (isFullScreen) => {
    const currentState = appService.getSnapshot().context.isFullScreen;
    if (currentState !== isFullScreen) {
      appService.send({ type: "TOGGLE_FULLSCREEN" });
    }
  },
  /**
   * Open the settings panel
   */
  openSettings: () => {
    appService.send({ type: "OPEN_SETTINGS" });
  },
  /**
   * Close the settings panel
   */
  closeSettings: () => {
    appService.send({ type: "CLOSE_SETTINGS" });
  },
  /**
   * Update the background type
   * @param background The new background type
   */
  updateBackground: (background) => {
    appService.send({ type: "UPDATE_BACKGROUND", background });
  },
  /**
   * Signal that the background is ready
   */
  backgroundReady: () => {
    appService.send({ type: "BACKGROUND_READY" });
  },
  /**
   * Retry initialization after a failure
   */
  retryInitialization: () => {
    appService.send({ type: "RETRY_INITIALIZATION" });
  }
};
function createSequenceStoreAdapter() {
  const { subscribe, set } = writable(sequenceContainer.state);
  let cleanup = null;
  if ("subscribe" in sequenceContainer && typeof sequenceContainer.subscribe === "function") {
    const unsubscribe = sequenceContainer.subscribe((state) => {
      set(state);
    });
    cleanup = () => {
      if (typeof unsubscribe === "function") {
        unsubscribe();
      }
    };
  } else {
    const intervalId = setInterval(() => {
      set(sequenceContainer.state);
    }, 16);
    cleanup = () => {
      clearInterval(intervalId);
    };
  }
  if (typeof window !== "undefined") {
    window.addEventListener("beforeunload", () => {
      if (cleanup) cleanup();
    });
  }
  return {
    subscribe,
    set: (value) => {
      sequenceContainer.setSequence(value.beats);
      sequenceContainer.updateMetadata(value.metadata);
      if (value.selectedBeatIds.length > 0) {
        sequenceContainer.clearSelection();
        value.selectedBeatIds.forEach((id) => sequenceContainer.selectBeat(id, true));
      }
      sequenceContainer.setCurrentBeatIndex(value.currentBeatIndex);
      if (!value.isModified) {
        sequenceContainer.markAsSaved();
      }
      set(value);
    },
    update: (updater) => {
      const newValue = updater(sequenceContainer.state);
      sequenceContainer.setSequence(newValue.beats);
      sequenceContainer.updateMetadata(newValue.metadata);
      if (newValue.selectedBeatIds.length > 0) {
        sequenceContainer.clearSelection();
        newValue.selectedBeatIds.forEach((id) => sequenceContainer.selectBeat(id, true));
      }
      sequenceContainer.setCurrentBeatIndex(newValue.currentBeatIndex);
      if (!newValue.isModified) {
        sequenceContainer.markAsSaved();
      }
      set(newValue);
    },
    // Forward action methods to the container
    addBeat: sequenceContainer.addBeat,
    addBeats: sequenceContainer.addBeats,
    setSequence: sequenceContainer.setSequence,
    removeBeat: sequenceContainer.removeBeat,
    updateBeat: sequenceContainer.updateBeat,
    selectBeat: sequenceContainer.selectBeat,
    deselectBeat: sequenceContainer.deselectBeat,
    clearSelection: sequenceContainer.clearSelection,
    setCurrentBeatIndex: sequenceContainer.setCurrentBeatIndex,
    updateMetadata: sequenceContainer.updateMetadata,
    markAsSaved: sequenceContainer.markAsSaved
  };
}
const sequenceStore$1 = createSequenceStoreAdapter();
derived(
  sequenceStore$1,
  ($store) => $store.beats.filter((beat) => $store.selectedBeatIds.includes(beat.id))
);
derived(
  sequenceStore$1,
  ($store) => $store.beats[$store.currentBeatIndex] || null
);
derived(
  sequenceStore$1,
  ($store) => $store.beats.length
);
derived(
  sequenceStore$1,
  ($store) => $store.metadata.difficulty
);
function convertToModernBeat(legacyBeat) {
  return {
    id: legacyBeat.id || `beat-${Date.now()}-${Math.random().toString(36).slice(2, 11)}`,
    number: legacyBeat.beatNumber,
    // Copy all other properties from the legacy beat
    ...legacyBeat
  };
}
function convertToLegacyBeat(modernBeat) {
  return {
    id: modernBeat.id,
    beatNumber: modernBeat.number,
    filled: modernBeat.filled || true,
    pictographData: modernBeat.pictographData || {}
  };
}
const beatsStore = {
  subscribe: derived(sequenceStore$1, ($store) => $store.beats.map(convertToLegacyBeat)).subscribe,
  set: (beats) => {
    sequenceStore$1.setSequence(beats.map(convertToModernBeat));
  },
  update: (updater) => {
    const currentBeats = get(sequenceStore$1).beats.map(convertToLegacyBeat);
    const newBeats = updater(currentBeats);
    sequenceStore$1.setSequence(newBeats.map(convertToModernBeat));
  }
};
function createSelectedStartPosStore() {
  let initialValue = null;
  const { subscribe, set: originalSet, update } = writable(initialValue);
  function set(value) {
    originalSet(value);
  }
  return {
    subscribe,
    set,
    update: (updater) => {
      update((current) => {
        const newValue = updater(current);
        return newValue;
      });
    }
  };
}
const selectedBeatIndexStore = writable(null);
const selectedStartPosStore = createSelectedStartPosStore();
derived(
  [beatsStore, selectedBeatIndexStore],
  ([$beats, $selectedIndex]) => {
    if ($selectedIndex === null || $selectedIndex < 0 || $selectedIndex >= $beats.length) {
      return null;
    }
    return $beats[$selectedIndex];
  }
);
derived(
  [selectedBeatIndexStore, selectedStartPosStore],
  ([$selectedBeatIndex, $selectedStartPos]) => {
    return $selectedBeatIndex === null && $selectedStartPos !== null;
  }
);
derived(
  selectedBeatIndexStore,
  ($selectedBeatIndex) => $selectedBeatIndex !== null
);
derived(
  [selectedBeatIndexStore, selectedStartPosStore],
  ([$selectedBeatIndex, $selectedStartPos]) => $selectedBeatIndex !== null || $selectedStartPos !== null
);
const selectedStartPos = selectedStartPosStore;
const initialState$6 = {
  status: "idle",
  data: null,
  error: null,
  loadProgress: 0,
  components: {
    grid: false,
    redProp: false,
    blueProp: false,
    redArrow: false,
    blueArrow: false
  },
  stateHistory: []
};
function calculateProgress$1(components) {
  const total = Object.keys(components).length;
  const loaded = Object.values(components).filter(Boolean).length;
  return Math.floor(loaded / Math.max(total, 1) * 100);
}
const pictographStore = createStore(
  "pictograph",
  initialState$6,
  (set, update, get2) => {
    function transitionTo(newState, reason) {
      update((state) => {
        if (state.status === newState) return state;
        const newTransition = {
          from: state.status,
          to: newState,
          reason,
          timestamp: Date.now()
        };
        const updatedHistory = [...state.stateHistory, newTransition].slice(-10);
        return {
          ...state,
          status: newState,
          stateHistory: updatedHistory
        };
      });
    }
    return {
      setData: (data) => {
        transitionTo("initializing", "Starting to load pictograph");
        update((state) => ({ ...state, data, status: "grid_loading" }));
      },
      updateComponentLoaded: (component) => {
        update((state) => {
          const updatedComponents = {
            ...state.components,
            [component]: true
          };
          const newProgress = calculateProgress$1(updatedComponents);
          const allLoaded = Object.values(updatedComponents).every(Boolean);
          const newState = allLoaded ? "complete" : state.status;
          if (allLoaded && newState !== "complete") transitionTo("complete", "All components loaded");
          return {
            ...state,
            components: updatedComponents,
            loadProgress: newProgress,
            status: newState
          };
        });
      },
      setError: (message, component) => {
        update((state) => ({
          ...state,
          status: "error",
          error: {
            message,
            component,
            timestamp: Date.now()
          }
        }));
      },
      updatePropData: (color, propData) => {
        update((state) => {
          if (!state.data) return state;
          const key = color === "red" ? "redPropData" : "bluePropData";
          const componentKey = color === "red" ? "redProp" : "blueProp";
          return {
            ...state,
            data: { ...state.data, [key]: propData },
            components: { ...state.components, [componentKey]: true }
          };
        });
      },
      updateArrowData: (color, arrowData) => {
        update((state) => {
          if (!state.data) return state;
          const key = color === "red" ? "redArrowData" : "blueArrowData";
          const componentKey = color === "red" ? "redArrow" : "blueArrow";
          return {
            ...state,
            data: { ...state.data, [key]: arrowData },
            components: { ...state.components, [componentKey]: true }
          };
        });
      },
      transitionTo
    };
  },
  {
    persist: false,
    description: "Manages the state of pictographs in the application"
  }
);
const isSequenceEmpty = writable(true);
if (typeof window !== "undefined") {
  sequenceStore$1.subscribe((state) => {
    isSequenceEmpty.set(state.beats.length === 0);
  });
}
function initializePersistence(sequenceActor2) {
  if (typeof window === "undefined") return;
  import("../../chunks/SequenceContainer.js").then((n) => n.S).then(({ sequenceContainer: sequenceContainer2 }) => {
    let sequenceLoaded = false;
    try {
      sequenceLoaded = sequenceContainer2.loadFromLocalStorage();
      if (sequenceLoaded) {
        const hasBeats = sequenceContainer2.state.beats.length > 0;
        isSequenceEmpty.set(!hasBeats);
        const firstBeat = sequenceContainer2.state.beats[0];
        if (hasBeats) {
          let pictographData = null;
          if (firstBeat.pictographData) {
            pictographData = firstBeat.pictographData;
          } else if (firstBeat.metadata?.pictographData) {
            pictographData = firstBeat.metadata.pictographData;
          } else {
            pictographData = {
              letter: firstBeat.letter || firstBeat.metadata?.letter || null,
              startPos: firstBeat.position || firstBeat.metadata?.startPos || null,
              endPos: firstBeat.metadata?.endPos || null,
              gridMode: firstBeat.metadata?.gridMode || "diamond",
              redPropData: firstBeat.redPropData || null,
              bluePropData: firstBeat.bluePropData || null,
              redMotionData: firstBeat.redMotionData || null,
              blueMotionData: firstBeat.blueMotionData || null,
              redArrowData: firstBeat.redArrowData || null,
              blueArrowData: firstBeat.blueArrowData || null,
              grid: firstBeat.metadata?.grid || "",
              timing: null,
              direction: null,
              gridData: null,
              motions: [],
              redMotion: null,
              blueMotion: null,
              props: []
            };
          }
          if (pictographData) {
            restoreStartPosition(pictographData);
          }
        }
      }
    } catch (error) {
      console.error("Error loading sequence from modern storage:", error);
    }
    if (!sequenceLoaded) {
      try {
        const backupData = localStorage.getItem("sequence_backup");
        if (backupData) {
          const backup = JSON.parse(backupData);
          if (backup.beats && Array.isArray(backup.beats) && backup.beats.length > 0) {
            const processedBeats = backup.beats.map((beat) => {
              const processedBeat = { ...beat };
              if (!processedBeat.pictographData && processedBeat.metadata) {
                processedBeat.pictographData = {
                  letter: processedBeat.letter || processedBeat.metadata.letter || null,
                  startPos: processedBeat.position || processedBeat.metadata.startPos || null,
                  endPos: processedBeat.metadata.endPos || null,
                  gridMode: processedBeat.metadata.gridMode || "diamond",
                  redPropData: processedBeat.redPropData || null,
                  bluePropData: processedBeat.bluePropData || null,
                  redMotionData: processedBeat.redMotionData || null,
                  blueMotionData: processedBeat.blueMotionData || null,
                  redArrowData: processedBeat.redArrowData || null,
                  blueArrowData: processedBeat.blueArrowData || null,
                  grid: processedBeat.metadata.grid || "",
                  timing: null,
                  direction: null,
                  gridData: null,
                  motions: [],
                  redMotion: null,
                  blueMotion: null,
                  props: []
                };
              }
              return processedBeat;
            });
            sequenceStore$1.setSequence(processedBeats);
            sequenceContainer2.setSequence(processedBeats);
            if (backup.word) {
              sequenceContainer2.updateMetadata({
                name: backup.word
              });
            } else {
              const letters = processedBeats.map((beat) => {
                return beat.letter || (beat.metadata && typeof beat.metadata.letter === "string" ? beat.metadata.letter : null);
              }).filter((letter) => letter !== null);
              const word = letters.join("");
              sequenceContainer2.updateMetadata({
                name: word
              });
            }
            isSequenceEmpty.set(false);
            const firstBeat = processedBeats[0];
            if (firstBeat) {
              let pictographData = null;
              if (firstBeat.pictographData) {
                pictographData = firstBeat.pictographData;
              } else if (firstBeat.metadata?.pictographData) {
                pictographData = firstBeat.metadata.pictographData;
              } else {
                pictographData = {
                  letter: firstBeat.letter || firstBeat.metadata?.letter || null,
                  startPos: firstBeat.position || firstBeat.metadata?.startPos || null,
                  endPos: firstBeat.metadata?.endPos || null,
                  gridMode: firstBeat.metadata?.gridMode || "diamond",
                  redPropData: firstBeat.redPropData || null,
                  bluePropData: firstBeat.bluePropData || null,
                  redMotionData: firstBeat.redMotionData || null,
                  blueMotionData: firstBeat.blueMotionData || null,
                  redArrowData: firstBeat.redArrowData || null,
                  blueArrowData: firstBeat.blueArrowData || null,
                  grid: firstBeat.metadata?.grid || "",
                  timing: null,
                  direction: null,
                  gridData: null,
                  motions: [],
                  redMotion: null,
                  blueMotion: null,
                  props: []
                };
              }
              if (pictographData) {
                restoreStartPosition(pictographData);
              }
            }
            sequenceContainer2.saveToLocalStorage();
          }
        }
      } catch (error) {
        console.error("Error loading sequence backup:", error);
      }
    }
  });
  function restoreStartPosition(pictographData) {
    const startPosCopy = JSON.parse(JSON.stringify(pictographData));
    selectedStartPos.set(startPosCopy);
    pictographStore.setData(startPosCopy);
    if (typeof document !== "undefined") {
      const event = new CustomEvent("start-position-selected", {
        detail: { startPosition: startPosCopy },
        bubbles: true
      });
      document.dispatchEvent(event);
    }
  }
  sequenceActor2.subscribe((state) => {
    Promise.all([
      import("../../chunks/SequenceContainer.js").then((n) => n.S),
      import("../../chunks/pictographUtils.js")
    ]).then(([{ sequenceContainer: sequenceContainer2 }, { createSafeBeatCopy }]) => {
      try {
        let beats = [];
        sequenceStore$1.subscribe((state2) => {
          beats = state2.beats;
        })();
        const safeBeats = beats.map((beat) => {
          const safeBeat = createSafeBeatCopy(beat);
          if (!safeBeat.pictographData && beat.metadata) {
            safeBeat.pictographData = {
              letter: beat.letter || beat.metadata.letter || null,
              startPos: beat.position || beat.metadata.startPos || null,
              endPos: beat.metadata.endPos || null,
              gridMode: beat.metadata.gridMode || "diamond",
              redPropData: beat.redPropData || null,
              bluePropData: beat.bluePropData || null,
              redMotionData: beat.redMotionData || null,
              blueMotionData: beat.blueMotionData || null,
              redArrowData: beat.redArrowData || null,
              blueArrowData: beat.blueArrowData || null,
              grid: beat.metadata.grid || "",
              timing: null,
              direction: null,
              gridData: null,
              motions: [],
              redMotion: null,
              blueMotion: null,
              props: []
            };
          }
          return safeBeat;
        });
        const letters = beats.map((beat) => {
          return beat.letter || (beat.metadata && typeof beat.metadata.letter === "string" ? beat.metadata.letter : null);
        }).filter((letter) => letter !== null);
        const word = letters.join("");
        localStorage.setItem(
          "sequence_backup",
          JSON.stringify({
            beats: safeBeats,
            options: state.context.generationOptions,
            word
            // Add the word to the backup
          })
        );
        sequenceContainer2.saveToLocalStorage();
        console.log("Saved sequence to both storage mechanisms with beats:", safeBeats.length);
      } catch (error) {
        console.error("Error saving sequence:", error);
      }
    });
  });
}
const generateSequenceActor = fromCallback(
  ({ sendBack, input }) => {
    console.log(
      `Generating ${input.generationType} sequence with options:`,
      input.generationOptions
    );
    (async () => {
      try {
        sendBack({
          type: "UPDATE_PROGRESS",
          progress: 10,
          message: `Initializing ${input.generationType} sequence generation...`
        });
        await new Promise((resolve) => setTimeout(resolve, 10));
        let generatedSequence = [];
        if (input.generationType === "circular") {
          const { createCircularSequence } = await import("../../chunks/createCircularSequence.js");
          sendBack({
            type: "UPDATE_PROGRESS",
            progress: 30,
            message: "Creating circular sequence pattern..."
          });
          const circularOptions = input.generationOptions;
          generatedSequence = await createCircularSequence(circularOptions);
        } else {
          const { createFreeformSequence } = await import("../../chunks/createFreeformSequence.js");
          sendBack({
            type: "UPDATE_PROGRESS",
            progress: 30,
            message: "Creating freeform sequence pattern..."
          });
          const freeformOptions = input.generationOptions;
          generatedSequence = await createFreeformSequence(freeformOptions);
        }
        sendBack({
          type: "UPDATE_PROGRESS",
          progress: 90,
          message: "Finalizing sequence..."
        });
        sendBack({
          type: "GENERATION_COMPLETE",
          output: generatedSequence
        });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Unknown error during sequence generation";
        console.error("Sequence generation error:", error);
        sendBack({
          type: "GENERATION_ERROR",
          error: errorMessage
        });
      }
    })();
    return () => {
    };
  }
);
function convertToStoreBeatData(componentBeats) {
  return componentBeats.map((beat, index) => ({
    id: beat.id || `beat-${index}`,
    number: beat.number || index + 1,
    letter: beat.letterType || beat.letter || "",
    position: beat.position || "",
    orientation: typeof beat.orientation === "object" ? `${beat.orientation.blue || "in"}_${beat.orientation.red || "in"}` : beat.orientation || "",
    turnsTuple: beat.turnIntensity ? String(beat.turnIntensity) : "",
    redPropData: beat.redPropData || null,
    bluePropData: beat.bluePropData || null,
    redArrowData: beat.redArrowData || null,
    blueArrowData: beat.blueArrowData || null,
    pictographData: beat.pictographData || null,
    metadata: beat.metadata || {}
  }));
}
function createModernMachine(options) {
  return setup({
    types: {},
    actions: options.actions || {},
    actors: options.services || {},
    guards: options.guards || {}
  }).createMachine({
    id: options.id,
    initial: options.initial,
    context: options.context,
    states: options.states
  });
}
function createMachineContainer(machine, options = {}) {
  const actor = createActor(machine, options);
  actor.start();
  const initialSnapshot = actor.getSnapshot();
  const initialState2 = {
    value: void 0,
    context: void 0,
    status: void 0,
    nextEvents: void 0
  };
  if (initialSnapshot) {
    try {
      const snapshot = initialSnapshot;
      if (snapshot && typeof snapshot === "object") {
        if ("value" in snapshot) initialState2.value = snapshot.value;
        if ("context" in snapshot) initialState2.context = snapshot.context;
        if ("status" in snapshot) initialState2.status = snapshot.status;
        if ("nextEvents" in snapshot) initialState2.nextEvents = snapshot.nextEvents;
      }
    } catch (error) {
      console.error("Error copying properties from snapshot:", error);
    }
  }
  return createContainer(initialState2, (state, update) => {
    const subscription = actor.subscribe((snapshotInput) => {
      update(() => {
        try {
          const snapshot = snapshotInput;
          if (snapshot && typeof snapshot === "object") {
            if ("value" in snapshot) state.value = snapshot.value;
            if ("context" in snapshot) state.context = snapshot.context;
            if ("status" in snapshot) state.status = snapshot.status;
            if ("nextEvents" in snapshot) state.nextEvents = snapshot.nextEvents;
          }
        } catch (error) {
          console.error("Error updating state from snapshot:", error);
        }
      });
    });
    const unsubscribe = () => {
      if (subscription && typeof subscription.unsubscribe === "function") {
        subscription.unsubscribe();
      }
    };
    return {
      send: (event) => actor.send(event),
      getSnapshot: () => actor.getSnapshot(),
      stop: () => {
        unsubscribe();
        actor.stop();
      },
      // Add helper methods for better ergonomics
      can: (eventType) => actor.getSnapshot().can({ type: eventType }),
      matches: (stateValue) => actor.getSnapshot().matches(stateValue),
      hasTag: (tag) => actor.getSnapshot().hasTag(tag),
      getActor: () => actor
    };
  });
}
const DIAMOND = "diamond";
const defaultPictographData = {
  letter: null,
  startPos: null,
  endPos: null,
  timing: null,
  direction: null,
  gridMode: DIAMOND,
  blueMotionData: null,
  redMotionData: null,
  motions: [],
  redMotion: null,
  blueMotion: null,
  props: [],
  redPropData: null,
  bluePropData: null,
  gridData: null,
  redArrowData: null,
  blueArrowData: null,
  grid: "",
  isStartPosition: false
};
const initialState$5 = {
  status: "idle",
  data: defaultPictographData,
  // Initialize with default data instead of null
  error: null,
  loadProgress: 0,
  components: {
    grid: false,
    redProp: false,
    blueProp: false,
    redArrow: false,
    blueArrow: false
  },
  stateHistory: []
};
function calculateProgress(components) {
  const total = Object.keys(components).length;
  const loaded = Object.values(components).filter(Boolean).length;
  return Math.floor(loaded / Math.max(total, 1) * 100);
}
function createPictographContainer() {
  return createContainer(initialState$5, (state, update) => {
    function transitionTo(newState, reason) {
      update((state2) => {
        if (state2.status === newState) return;
        const newTransition = {
          from: state2.status,
          to: newState,
          reason,
          timestamp: Date.now()
        };
        state2.status = newState;
        state2.stateHistory = [...state2.stateHistory, newTransition].slice(-10);
      });
    }
    return {
      setData: (data) => {
        transitionTo("initializing", "Starting to load pictograph");
        update((state2) => {
          state2.data = data;
          state2.status = "grid_loading";
        });
      },
      updateComponentLoaded: (component) => {
        update((state2) => {
          state2.components[component] = true;
          state2.loadProgress = calculateProgress(state2.components);
          const allLoaded = Object.values(state2.components).every(Boolean);
          if (allLoaded && state2.status !== "complete") {
            transitionTo("complete", "All components loaded");
          }
        });
      },
      setError: (message, component) => {
        update((state2) => {
          state2.status = "error";
          state2.error = {
            message,
            component,
            timestamp: Date.now()
          };
          state2.loadProgress = 0;
        });
      },
      updateGridData: (gridData) => {
        update((state2) => {
          if (!state2.data) return;
          state2.data = { ...state2.data, gridData };
          state2.components.grid = true;
          transitionTo("props_loading", "Grid data loaded");
        });
      },
      updatePropData: (color, propData) => {
        update((state2) => {
          if (!state2.data) return;
          const key = color === "red" ? "redPropData" : "bluePropData";
          const componentKey = color === "red" ? "redProp" : "blueProp";
          state2.data = { ...state2.data, [key]: propData };
          state2.components[componentKey] = true;
          transitionTo("arrows_loading", `${color} prop loaded`);
        });
      },
      updateArrowData: (color, arrowData) => {
        update((state2) => {
          if (!state2.data) return;
          const key = color === "red" ? "redArrowData" : "blueArrowData";
          const componentKey = color === "red" ? "redArrow" : "blueArrow";
          state2.data = { ...state2.data, [key]: arrowData };
          state2.components[componentKey] = true;
        });
      },
      reset: () => {
        update((state2) => {
          state2.status = "idle";
          state2.data = defaultPictographData;
          state2.error = null;
          state2.loadProgress = 0;
          state2.components = {
            grid: false,
            redProp: false,
            blueProp: false,
            redArrow: false,
            blueArrow: false
          };
          state2.stateHistory = [];
        });
      },
      transitionTo
    };
  });
}
const pictographContainer = createPictographContainer();
createDerived(() => pictographContainer.state.data);
createDerived(() => pictographContainer.state.status);
createDerived(() => pictographContainer.state.error);
createDerived(() => pictographContainer.state.loadProgress);
createDerived(
  () => ["initializing", "grid_loading", "props_loading", "arrows_loading"].includes(
    pictographContainer.state.status
  )
);
createDerived(() => pictographContainer.state.status === "complete");
createDerived(() => pictographContainer.state.status === "error");
function getStoreValue(store) {
  let value;
  const unsubscribe = store.subscribe((currentValue) => {
    value = currentValue;
  });
  unsubscribe();
  return value;
}
function updateSequenceWord() {
  const state = sequenceContainer.state;
  const beats = state.beats;
  const difficulty = beats.length > 0 ? 1 : 0;
  const letters = beats.map((beat) => {
    return beat.letter || (beat.metadata && typeof beat.metadata.letter === "string" ? beat.metadata.letter : null);
  }).filter((letter) => letter !== null);
  const word = letters.join("");
  sequenceContainer.updateMetadata({
    name: word,
    difficulty
  });
}
function updateSequence({ event }) {
  const doneEvent = event;
  if (doneEvent.output && Array.isArray(doneEvent.output)) {
    const storeBeats = convertToStoreBeatData(doneEvent.output);
    sequenceContainer.setSequence(storeBeats);
    console.log("Sequence updated with new data:", storeBeats);
    updateSequenceWord();
  }
}
function selectBeat({ event }) {
  const selectEvent = event;
  sequenceContainer.selectBeat(selectEvent.beatId);
  if (typeof document !== "undefined") {
    const selectionEvent = new CustomEvent("beat-selected", {
      detail: { beatId: selectEvent.beatId },
      bubbles: true
    });
    document.dispatchEvent(selectionEvent);
  }
}
function deselectBeat({ event }) {
  const deselectEvent = event;
  sequenceContainer.deselectBeat(deselectEvent.beatId);
  if (typeof document !== "undefined") {
    const selectionEvent = new CustomEvent("beat-deselected", {
      detail: { beatId: deselectEvent.beatId },
      bubbles: true
    });
    document.dispatchEvent(selectionEvent);
  }
}
function addBeat({ event }) {
  const addEvent = event;
  const beatId = addEvent.beat.id || crypto.randomUUID();
  const newBeat = {
    id: beatId,
    number: addEvent.beat.number || 0,
    ...addEvent.beat
  };
  sequenceContainer.addBeat(newBeat);
  updateSequenceWord();
  if (typeof document !== "undefined") {
    const beatEvent = new CustomEvent("beat-added", {
      detail: { beat: newBeat },
      bubbles: true
    });
    document.dispatchEvent(beatEvent);
  }
}
function removeBeat({ event }) {
  const removeEvent = event;
  let currentStartPos = null;
  try {
    currentStartPos = getStoreValue(selectedStartPos);
    if (currentStartPos) {
      currentStartPos.isStartPosition = true;
      if (currentStartPos.redMotionData) {
        currentStartPos.redMotionData.motionType = "static";
        currentStartPos.redMotionData.endLoc = currentStartPos.redMotionData.startLoc;
        currentStartPos.redMotionData.endOri = currentStartPos.redMotionData.startOri;
        currentStartPos.redMotionData.turns = 0;
      }
      if (currentStartPos.blueMotionData) {
        currentStartPos.blueMotionData.motionType = "static";
        currentStartPos.blueMotionData.endLoc = currentStartPos.blueMotionData.startLoc;
        currentStartPos.blueMotionData.endOri = currentStartPos.blueMotionData.startOri;
        currentStartPos.blueMotionData.turns = 0;
      }
      currentStartPos = JSON.parse(JSON.stringify(currentStartPos));
    }
  } catch (error) {
    console.error("Failed to get current start position:", error);
  }
  sequenceContainer.removeBeat(removeEvent.beatId);
  updateSequenceWord();
  if (typeof document !== "undefined") {
    const beatEvent = new CustomEvent("beat-removed", {
      detail: { beatId: removeEvent.beatId },
      bubbles: true
    });
    document.dispatchEvent(beatEvent);
    if (currentStartPos) {
      const startPosEvent = new CustomEvent("start-position-selected", {
        detail: { startPosition: currentStartPos },
        bubbles: true
      });
      document.dispatchEvent(startPosEvent);
      const refreshOptionsEvent = new CustomEvent("refresh-options", {
        detail: { startPosition: currentStartPos },
        bubbles: true
      });
      document.dispatchEvent(refreshOptionsEvent);
      try {
        localStorage.setItem("start_position", JSON.stringify(currentStartPos));
        console.log("Saved start position to localStorage after beat removal");
      } catch (error) {
        console.error("Failed to save start position to localStorage:", error);
      }
      console.log("Preserved start position after beat removal");
    }
  }
}
function removeBeatAndFollowing({ event }) {
  const removeEvent = event;
  const beatIndex = sequenceContainer.state.beats.findIndex(
    (beat) => beat.id === removeEvent.beatId
  );
  if (beatIndex >= 0) {
    const beatsToRemove = sequenceContainer.state.beats.slice(beatIndex).map((beat) => beat.id);
    let currentStartPos = null;
    try {
      currentStartPos = getStoreValue(selectedStartPos);
      if (currentStartPos) {
        currentStartPos.isStartPosition = true;
      }
    } catch (error) {
      console.error("Failed to get current start position:", error);
    }
    beatsToRemove.forEach((id) => {
      sequenceContainer.removeBeat(id);
    });
    updateSequenceWord();
    if (typeof document !== "undefined") {
      const sequenceUpdatedEvent = new CustomEvent("sequence-updated", {
        detail: { type: "beats-removed", fromIndex: beatIndex },
        bubbles: true
      });
      document.dispatchEvent(sequenceUpdatedEvent);
      if (currentStartPos) {
        const startPosEvent = new CustomEvent("start-position-selected", {
          detail: { startPosition: currentStartPos },
          bubbles: true
        });
        document.dispatchEvent(startPosEvent);
        const refreshOptionsEvent = new CustomEvent("refresh-options", {
          detail: { startPosition: currentStartPos },
          bubbles: true
        });
        document.dispatchEvent(refreshOptionsEvent);
        try {
          localStorage.setItem("start_position", JSON.stringify(currentStartPos));
          console.log("Saved start position to localStorage after beat removal");
        } catch (error) {
          console.error("Failed to save start position to localStorage:", error);
        }
        console.log("Preserved start position after beat removal");
      }
    }
  }
}
function updateBeat({ event }) {
  const updateEvent = event;
  sequenceContainer.updateBeat(updateEvent.beatId, updateEvent.updates);
  updateSequenceWord();
  if (typeof document !== "undefined") {
    const beatEvent = new CustomEvent("beat-updated", {
      detail: { beatId: updateEvent.beatId, updates: updateEvent.updates },
      bubbles: true
    });
    document.dispatchEvent(beatEvent);
  }
}
function clearSequence() {
  console.log("Clearing sequence and start position");
  sequenceContainer.setSequence([]);
  updateSequenceWord();
  sequenceContainer.updateMetadata({
    name: "",
    difficulty: 0,
    tags: []
  });
  isSequenceEmpty.set(true);
  selectedStartPos.set(null);
  pictographContainer.setData(defaultPictographData);
  if (typeof window !== "undefined") {
    try {
      sequenceContainer.saveToLocalStorage();
      localStorage.setItem("start_position", JSON.stringify(null));
      localStorage.setItem(
        "sequence_backup",
        JSON.stringify({
          beats: [],
          options: null,
          word: ""
        })
      );
      console.log("Saved empty sequence state to localStorage");
    } catch (error) {
      console.error("Error saving empty sequence state:", error);
    }
  }
  sequenceContainer.markAsSaved();
  if (typeof document !== "undefined") {
    const sequenceUpdatedEvent = new CustomEvent("sequence-updated", {
      detail: { type: "sequence-cleared" },
      bubbles: true
    });
    document.dispatchEvent(sequenceUpdatedEvent);
    const startPosEvent = new CustomEvent("start-position-selected", {
      detail: { startPosition: null },
      bubbles: true
    });
    document.dispatchEvent(startPosEvent);
    const resetOptionPickerEvent = new CustomEvent("reset-option-picker", {
      bubbles: true
    });
    document.dispatchEvent(resetOptionPickerEvent);
  }
}
const modernSequenceMachine = createModernMachine({
  id: "sequence",
  initial: "idle",
  context: {
    generationType: null,
    generationOptions: null,
    generationProgress: 0,
    generationMessage: "",
    error: null
  },
  states: {
    idle: {
      on: {
        GENERATE: {
          target: "generating",
          actions: (context, event) => {
            context.generationType = event.generationType;
            context.generationOptions = event.options;
            context.generationProgress = 0;
            context.generationMessage = "Initializing sequence generation...";
            context.error = null;
          }
        },
        SELECT_BEAT: {
          actions: "selectBeat"
        },
        DESELECT_BEAT: {
          actions: "deselectBeat"
        },
        ADD_BEAT: {
          actions: "addBeat"
        },
        REMOVE_BEAT: {
          actions: "removeBeat"
        },
        REMOVE_BEAT_AND_FOLLOWING: {
          actions: "removeBeatAndFollowing"
        },
        UPDATE_BEAT: {
          actions: "updateBeat"
        },
        CLEAR_SEQUENCE: {
          actions: "clearSequence"
        }
      }
    },
    generating: {
      invoke: {
        src: "generateSequenceActor",
        input: ({ context }) => ({
          type: context.generationType,
          options: context.generationOptions
        }),
        onDone: {
          target: "idle",
          actions: "updateSequence"
        },
        onError: {
          target: "error",
          actions: (context, event) => {
            context.error = event.error?.message || "Unknown error during sequence generation";
            context.generationProgress = 0;
          }
        }
      },
      on: {
        GENERATION_PROGRESS: {
          actions: (context, event) => {
            context.generationProgress = event.progress;
            context.generationMessage = event.message;
          }
        }
      }
    },
    error: {
      on: {
        RETRY: { target: "generating" },
        RESET: {
          target: "idle",
          actions: (context) => {
            context.error = null;
            context.generationProgress = 0;
            context.generationMessage = "";
          }
        }
      }
    }
  },
  actions: {
    updateSequence,
    selectBeat,
    deselectBeat,
    addBeat,
    removeBeat,
    removeBeatAndFollowing,
    updateBeat,
    clearSequence
  },
  services: {
    generateSequenceActor
  }
});
const modernSequenceContainer = createMachineContainer(modernSequenceMachine, {
  inspect: void 0
});
const sequenceSelectors$1 = {
  // Machine state selectors
  isGenerating: () => modernSequenceContainer.state.value === "generating",
  hasError: () => modernSequenceContainer.state.value === "error",
  error: () => modernSequenceContainer.state.context.error,
  progress: () => modernSequenceContainer.state.context.generationProgress,
  message: () => modernSequenceContainer.state.context.generationMessage,
  generationType: () => modernSequenceContainer.state.context.generationType,
  generationOptions: () => modernSequenceContainer.state.context.generationOptions,
  // Sequence data selectors
  beats: () => {
    const state = sequenceContainer.state;
    return state.beats || [];
  },
  selectedBeatIds: () => {
    const state = sequenceContainer.state;
    return state.selectedBeatIds || [];
  },
  selectedBeats: () => {
    const state = sequenceContainer.state;
    return state.beats.filter((beat) => state.selectedBeatIds.includes(beat.id)) || [];
  },
  currentBeatIndex: () => {
    const state = sequenceContainer.state;
    return state.currentBeatIndex || 0;
  },
  currentBeat: () => {
    const state = sequenceContainer.state;
    return state.beats[state.currentBeatIndex] || null;
  },
  beatCount: () => {
    const state = sequenceContainer.state;
    return state.beats.length || 0;
  }
};
const sequenceActions$1 = {
  generate: (generatorType, options) => {
    modernSequenceContainer.send({
      type: "GENERATE",
      generationType: generatorType,
      options
    });
  },
  retry: () => {
    modernSequenceContainer.send({ type: "RETRY" });
  },
  reset: () => {
    modernSequenceContainer.send({ type: "RESET" });
  },
  selectBeat: (beatId) => {
    modernSequenceContainer.send({ type: "SELECT_BEAT", beatId });
  },
  deselectBeat: (beatId) => {
    modernSequenceContainer.send({ type: "DESELECT_BEAT", beatId });
  },
  addBeat: (beat) => {
    modernSequenceContainer.send({ type: "ADD_BEAT", beat });
  },
  removeBeat: (beatId) => {
    modernSequenceContainer.send({ type: "REMOVE_BEAT", beatId });
  },
  removeBeatAndFollowing: (beatId) => {
    modernSequenceContainer.send({ type: "REMOVE_BEAT_AND_FOLLOWING", beatId });
  },
  updateBeat: (beatId, updates) => {
    modernSequenceContainer.send({ type: "UPDATE_BEAT", beatId, updates });
  },
  clearSequence: () => {
    modernSequenceContainer.send({ type: "CLEAR_SEQUENCE" });
  }
};
const sequenceActor = stateRegistry.registerMachine("sequence", modernSequenceMachine, {
  persist: true,
  description: "Manages sequence generation and related operations"
});
if (typeof window !== "undefined") {
  initializePersistence(sequenceActor);
}
const sequenceSelectors = sequenceSelectors$1;
const sequenceActions = sequenceActions$1;
function AppFullScreen($$payload, $$props) {
  push();
  let isFull = false;
  $$payload.out += `<div${attr_class(`fullscreen-container ${stringify("")}`, "svelte-qjrj5f")}><!---->`;
  slot($$payload, $$props, "default", { isFull });
  $$payload.out += `<!----> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
const initialState$4 = {
  toolsPanelOpen: false,
  activeTab: "generate"
};
const workbenchStore = writable(initialState$4);
function useResponsiveLayout$1() {
  const dimensions = readable({ width: 0, height: 0 }, (set) => {
    return;
  });
  const isPortrait = derived(dimensions, ($d) => $d.height > $d.width);
  const layout = derived(isPortrait, ($p) => $p ? "horizontal" : "vertical");
  return {
    dimensions,
    isPortrait,
    layout
  };
}
function useResizeObserver(defaultSize = {}) {
  const initialSize = {
    width: defaultSize.width || 0,
    height: defaultSize.height || 0,
    x: defaultSize.x || 0,
    y: defaultSize.y || 0
  };
  const size = writable(initialSize);
  function resizeObserver(node) {
    const rect = node.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      size.set({
        width: rect.width,
        height: rect.height,
        x: rect.x,
        y: rect.y
      });
    }
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect) {
          size.set({
            width: entry.contentRect.width,
            height: entry.contentRect.height,
            x: entry.contentRect.x,
            y: entry.contentRect.y
          });
        }
      }
    });
    observer.observe(node);
    return {
      destroy() {
        observer.disconnect();
      }
    };
  }
  return {
    size,
    resizeObserver
  };
}
const BEAT_FRAME_CONTEXT_KEY = Symbol("beat-frame-element");
function calculateWorkbenchIsPortrait(width, height) {
  return width < height && width < 768;
}
function calculateButtonSizeFactor(width, height) {
  const smallerDimension = Math.min(width, height);
  if (smallerDimension < 400) {
    return 0.7;
  } else if (smallerDimension < 600) {
    return 0.8;
  } else {
    return 1;
  }
}
const sequenceOverlayStore = writable({
  isOpen: false
});
function DifficultyCircle($$payload, $$props) {
  push();
  const DIFFICULTY_GRADIENTS = {
    1: [
      { position: 0, color: "#F5F5F5" }
      // Light gray/white
    ],
    2: [
      { position: 0, color: "#AAAAAA" },
      { position: 0.15, color: "#D2D2D2" },
      { position: 0.3, color: "#787878" },
      { position: 0.4, color: "#B4B4B4" },
      { position: 0.55, color: "#BEBEBE" },
      { position: 0.75, color: "#828282" },
      { position: 1, color: "#6E6E6E" }
    ],
    3: [
      { position: 0, color: "#FFD700" },
      // Gold
      { position: 0.2, color: "#EEC900" },
      // Goldenrod
      { position: 0.4, color: "#DAA520" },
      // Goldenrod darker
      { position: 0.6, color: "#B8860B" },
      // Dark goldenrod
      { position: 0.8, color: "#8B4513" },
      // Saddle brown
      { position: 1, color: "#556B2F" }
      // Dark olive green
    ],
    4: [
      { position: 0, color: "#C8A2C8" },
      { position: 0.3, color: "#AA84AA" },
      { position: 0.6, color: "#9400D3" },
      { position: 1, color: "#640096" }
    ],
    5: [
      { position: 0, color: "#FF4500" },
      { position: 0.4, color: "#FF0000" },
      { position: 0.8, color: "#8B0000" },
      { position: 1, color: "#640000" }
    ]
  };
  const { difficultyLevel = 1, size = 30, showBorder = true } = $$props;
  const level = Math.max(1, Math.min(5, Math.round(difficultyLevel)));
  const fontSize = Math.round(size * 0.65 / 2);
  const textColor = level >= 4 ? "white" : "black";
  const gradientCSS = () => {
    const stops = DIFFICULTY_GRADIENTS[level] || DIFFICULTY_GRADIENTS[1];
    return stops.map((stop) => `${stop.color} ${stop.position * 100}%`).join(", ");
  };
  $$payload.out += `<div class="difficulty-circle svelte-15w3uro"${attr_style(` --size: ${stringify(size)}px; --font-size: ${stringify(fontSize)}px; --text-color: ${stringify(textColor)}; --gradient: linear-gradient(135deg, ${stringify(gradientCSS)}); --border: ${stringify(showBorder ? "1px solid black" : "none")}; `)}>${escape_html(level)}</div>`;
  pop();
}
function CurrentWordLabel($$payload, $$props) {
  push();
  const { currentWord = "Word" } = $$props;
  const sequence = useContainer(sequenceContainer);
  const difficultyLevel = sequence.metadata?.difficulty || 1;
  const MAX_CHARS = 8;
  const displayWord = currentWord.length > MAX_CHARS ? currentWord.substring(0, MAX_CHARS) + "..." : currentWord;
  $$payload.out += `<div class="current-word-label svelte-rq9mus"><div class="difficulty-container svelte-rq9mus">`;
  DifficultyCircle($$payload, { difficultyLevel, size: 30 });
  $$payload.out += `<!----></div> <span class="word-display svelte-rq9mus">${escape_html(displayWord)}</span></div>`;
  pop();
}
const createLayoutStore = () => {
  const initialLayout = {
    rows: 1,
    cols: 1,
    beatCount: 0,
    lastChanged: Date.now()
  };
  const { subscribe, set, update } = writable(initialLayout);
  return {
    subscribe,
    // Update the layout information
    updateLayout: (rows, cols, beatCount) => {
      update((layout) => {
        const layoutChanged = layout.rows !== rows || layout.cols !== cols;
        return {
          rows,
          cols,
          beatCount,
          lastChanged: layoutChanged ? Date.now() : layout.lastChanged
        };
      });
    },
    // Reset the layout to initial values
    reset: () => set(initialLayout)
  };
};
createLayoutStore();
const initialState$3 = {
  theme: "system",
  background: "snowfall",
  backgroundQuality: "medium",
  defaultGridMode: "diamond",
  showGridDebug: false,
  enableAnimations: true,
  enableTransitions: true,
  autoSave: true,
  showTutorials: true,
  highContrast: false,
  reducedMotion: false,
  // Enable haptic feedback by default on mobile devices
  hapticFeedback: true,
  lastUpdated: Date.now()
};
const settingsStore = createStore(
  "settings",
  initialState$3,
  (set, update) => {
    return {
      setTheme: (theme) => {
        update((state) => ({
          ...state,
          theme,
          lastUpdated: Date.now()
        }));
      },
      setBackground: (background) => {
        update((state) => ({
          ...state,
          background,
          lastUpdated: Date.now()
        }));
      },
      setBackgroundQuality: (quality) => {
        update((state) => ({
          ...state,
          backgroundQuality: quality,
          lastUpdated: Date.now()
        }));
      },
      setDefaultGridMode: (mode) => {
        update((state) => ({
          ...state,
          defaultGridMode: mode,
          lastUpdated: Date.now()
        }));
      },
      setShowGridDebug: (show) => {
        update((state) => ({
          ...state,
          showGridDebug: show,
          lastUpdated: Date.now()
        }));
      },
      setEnableAnimations: (enable) => {
        update((state) => ({
          ...state,
          enableAnimations: enable,
          lastUpdated: Date.now()
        }));
      },
      setEnableTransitions: (enable) => {
        update((state) => ({
          ...state,
          enableTransitions: enable,
          lastUpdated: Date.now()
        }));
      },
      setAutoSave: (enable) => {
        update((state) => ({
          ...state,
          autoSave: enable,
          lastUpdated: Date.now()
        }));
      },
      setShowTutorials: (show) => {
        update((state) => ({
          ...state,
          showTutorials: show,
          lastUpdated: Date.now()
        }));
      },
      setHighContrast: (enable) => {
        update((state) => ({
          ...state,
          highContrast: enable,
          lastUpdated: Date.now()
        }));
      },
      setReducedMotion: (enable) => {
        update((state) => ({
          ...state,
          reducedMotion: enable,
          lastUpdated: Date.now()
        }));
      },
      setHapticFeedback: (enable) => {
        update((state) => ({
          ...state,
          hapticFeedback: enable,
          lastUpdated: Date.now()
        }));
      },
      updateSettings: (settings) => {
        update((state) => ({
          ...state,
          ...settings,
          lastUpdated: Date.now()
        }));
      }
    };
  },
  {
    persist: true,
    description: "Manages application settings"
  }
);
function PictographDebug($$payload, $$props) {
  let state = $$props["state"];
  let componentsLoaded = $$props["componentsLoaded"];
  let totalComponents = $$props["totalComponents"];
  let renderCount = $$props["renderCount"];
  $$payload.out += `<g class="debug-overlay svelte-kq3ojk"><rect x="10" y="10" width="200" height="80" fill="rgba(0,0,0,0.7)" rx="5"></rect><text x="20" y="30" font-size="12" fill="white">State: ${escape_html(state)}</text><text x="20" y="50" font-size="12" fill="white">Loaded: ${escape_html(componentsLoaded)}/${escape_html(totalComponents)}</text><text x="20" y="70" font-size="12" fill="white">Renders: ${escape_html(renderCount)}</text></g>`;
  bind_props($$props, { state, componentsLoaded, totalComponents, renderCount });
}
function InitializingSpinner($$payload, $$props) {
  let animationDuration = fallback($$props["animationDuration"], 200);
  $$payload.out += `<g><rect x="425" y="425" width="100" height="100" fill="transparent"></rect><circle cx="475" cy="475" r="40" fill="none" stroke="#ccc" stroke-width="8"></circle><path d="M475 435 A40 40 0 0 1 515 475" fill="none" stroke="#4299e1" stroke-width="8" stroke-linecap="round"><animate attributeName="stroke-dasharray" from="0 1000" to="1000 1000" dur="1s" repeatCount="indefinite"></animate></path><text x="50%" y="550" dominant-baseline="middle" text-anchor="middle" font-size="16" fill="#666">Initializing...</text></g>`;
  bind_props($$props, { animationDuration });
}
function shouldShowLoadingIndicator(state, showLoadingIndicator) {
  return showLoadingIndicator;
}
function shouldShowDebugInfo(debug) {
  return debug;
}
function getPictographRole(onClick) {
  return onClick ? "button" : "img";
}
function getPictographElement(onClick) {
  return onClick ? "button" : "div";
}
function PictographWrapper($$payload, $$props) {
  push();
  let pictographDataStore2 = $$props["pictographDataStore"];
  let onClick = fallback($$props["onClick"], () => void 0, true);
  let state = $$props["state"];
  element(
    $$payload,
    getPictographElement(onClick),
    () => {
      $$payload.out += `${spread_attributes(
        {
          class: "pictograph-wrapper",
          "aria-label": onClick ? `Pictograph for letter ${get(pictographDataStore2)?.letter || "unknown"}` : void 0,
          role: getPictographRole(onClick),
          "data-state": state,
          "data-letter": get(pictographDataStore2)?.letter || "none",
          ...onClick ? { type: "button" } : {}
        },
        "svelte-1ft9xv0"
      )}`;
    },
    () => {
      $$payload.out += `<!---->`;
      slot($$payload, $$props, "default", {});
      $$payload.out += `<!---->`;
    }
  );
  bind_props($$props, { pictographDataStore: pictographDataStore2, onClick, state });
  pop();
}
function getPictographAriaLabel(state, errorMessage, pictographData) {
  if (state === "error") return `Pictograph error: ${errorMessage}`;
  const letterPart = pictographData?.letter ? `for letter ${pictographData.letter}` : "";
  const statePart = state === "complete" ? "complete" : "loading";
  return `Pictograph visualization ${letterPart} - ${statePart}`;
}
function PictographSVG($$payload, $$props) {
  push();
  let pictographDataStore2 = $$props["pictographDataStore"];
  let state = $$props["state"];
  let errorMessage = $$props["errorMessage"];
  $$payload.out += `<svg class="pictograph svelte-jwn9gw" viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg" role="img"${attr("aria-label", getPictographAriaLabel(state, errorMessage, get(pictographDataStore2)))}><!---->`;
  slot($$payload, $$props, "default", {});
  $$payload.out += `<!----></svg>`;
  bind_props($$props, { pictographDataStore: pictographDataStore2, state, errorMessage });
  pop();
}
function createPictographDataStore(initialData) {
  return writable(initialData || defaultPictographData);
}
function Pictograph($$payload, $$props) {
  push();
  let pictographData = fallback($$props["pictographData"], () => void 0, true);
  let onClick = fallback($$props["onClick"], () => void 0, true);
  let debug = fallback($$props["debug"], false);
  let animationDuration = fallback($$props["animationDuration"], 200);
  let showLoadingIndicator = fallback($$props["showLoadingIndicator"], true);
  let beatNumber = fallback($$props["beatNumber"], null);
  let isStartPosition = fallback($$props["isStartPosition"], false);
  const pictographDataStore2 = createPictographDataStore(pictographData);
  let state = "initializing";
  let errorMessage = null;
  let totalComponentsToLoad = 1;
  let componentsLoaded = 0;
  let renderCount = 0;
  if (pictographData) {
    pictographDataStore2.set(pictographData);
  }
  PictographWrapper($$payload, {
    pictographDataStore: pictographDataStore2,
    onClick,
    state,
    children: ($$payload2) => {
      PictographSVG($$payload2, {
        pictographDataStore: pictographDataStore2,
        state,
        errorMessage,
        children: ($$payload3) => {
          {
            $$payload3.out += "<!--[-->";
            if (shouldShowLoadingIndicator(state, showLoadingIndicator)) {
              $$payload3.out += "<!--[-->";
              InitializingSpinner($$payload3, { animationDuration });
            } else {
              $$payload3.out += "<!--[!-->";
            }
            $$payload3.out += `<!--]-->`;
          }
          $$payload3.out += `<!--]-->`;
        },
        $$slots: { default: true }
      });
      $$payload2.out += `<!----> `;
      {
        $$payload2.out += "<!--[!-->";
      }
      $$payload2.out += `<!--]--> `;
      if (shouldShowDebugInfo(debug)) {
        $$payload2.out += "<!--[-->";
        PictographDebug($$payload2, {
          state,
          componentsLoaded,
          totalComponents: totalComponentsToLoad,
          renderCount
        });
      } else {
        $$payload2.out += "<!--[!-->";
      }
      $$payload2.out += `<!--]-->`;
    },
    $$slots: { default: true }
  });
  bind_props($$props, {
    pictographData,
    onClick,
    debug,
    animationDuration,
    showLoadingIndicator,
    beatNumber,
    isStartPosition
  });
  pop();
}
function StyledBorderOverlay($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const GOLD = "#FFD700";
  const OUTER_BORDER_WIDTH = 2;
  const INNER_BORDER_WIDTH = 2;
  const BORDER_COLORS = {
    [LetterType.Type1.folderName]: ["#36c3ff", "#6F2DA8"],
    // Cyan, Purple
    [LetterType.Type2.folderName]: ["#6F2DA8", "#6F2DA8"],
    // Purple, Purple
    [LetterType.Type3.folderName]: ["#26e600", "#6F2DA8"],
    // Green, Purple
    [LetterType.Type4.folderName]: ["#26e600", "#26e600"],
    // Green, Green
    [LetterType.Type5.folderName]: ["#00b3ff", "#26e600"],
    // Cyan, Green
    [LetterType.Type6.folderName]: ["#eb7d00", "#eb7d00"],
    // Orange, Orange
    [LetterType.Type7.folderName]: ["#6F2DA8", "#36c3ff"],
    // Purple, Cyan
    [LetterType.Type8.folderName]: ["#26e600", "#36c3ff"],
    // Green, Cyan
    [LetterType.Type9.folderName]: ["#eb7d00", "#36c3ff"]
    // Orange, Cyan
  };
  function getBorderColors() {
    if (!props.isEnabled) {
      return { primary: null, secondary: null };
    }
    if (props.isGold) {
      return { primary: GOLD, secondary: GOLD };
    }
    const letter = props.pictographData?.letter;
    if (!letter) {
      return { primary: null, secondary: null };
    }
    const letterType = LetterType.getLetterType(letter);
    if (!letterType) {
      return { primary: null, secondary: null };
    }
    const [primary2, secondary2] = BORDER_COLORS[letterType.folderName] || ["#000000", "#000000"];
    return {
      primary: primary2,
      secondary: primary2 !== secondary2 ? secondary2 : null
    };
  }
  const { primary, secondary } = getBorderColors();
  const showBorder = !!primary;
  const outerWidth = OUTER_BORDER_WIDTH;
  const innerWidth = INNER_BORDER_WIDTH;
  if (showBorder) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="border-overlay svelte-16veu2q"><div class="outer-border svelte-16veu2q"${attr_style(`border-color: ${stringify(primary)}; border-width: ${stringify(outerWidth)}px;`)}>`;
    if (secondary) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="inner-border svelte-16veu2q"${attr_style(`border-color: ${stringify(secondary)}; border-width: ${stringify(innerWidth)}px;`)}></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function Beat($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const isStartPosition = props.isStartPosition ?? false;
  const pictographData = props.beat?.pictographData || defaultPictographData;
  const isFilled = props.beat?.filled ?? false;
  const beatNumber = props.beat?.beatNumber ?? 0;
  let showBorder = false;
  $$payload.out += `<button${attr_class("beat svelte-d1xqkd", void 0, { "filled": isFilled })}${attr("aria-label", `Beat ${beatNumber}`)}><div class="pictograph-wrapper svelte-d1xqkd">`;
  Pictograph($$payload, {
    pictographData,
    beatNumber,
    isStartPosition,
    showLoadingIndicator: false
  });
  $$payload.out += `<!----> `;
  StyledBorderOverlay($$payload, { pictographData, isEnabled: showBorder });
  $$payload.out += `<!----></div></button>`;
  pop();
}
function SelectionBorderOverlay($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const BORDER_WIDTH = 3;
  const GLOW_RADIUS = 4;
  const BORDER_COLORS = {
    [LetterType.Type1.folderName]: "#36c3ff",
    // Cyan
    [LetterType.Type2.folderName]: "#6F2DA8",
    // Purple
    [LetterType.Type3.folderName]: "#26e600",
    // Green
    [LetterType.Type4.folderName]: "#26e600",
    // Green
    [LetterType.Type5.folderName]: "#00b3ff",
    // Cyan
    [LetterType.Type6.folderName]: "#eb7d00",
    // Orange
    [LetterType.Type7.folderName]: "#6F2DA8",
    // Purple
    [LetterType.Type8.folderName]: "#26e600",
    // Green
    [LetterType.Type9.folderName]: "#eb7d00"
    // Orange
  };
  const DEFAULT_COLOR = "#ffcc00";
  function getBorderColor() {
    if (!props.isSelected) {
      return "transparent";
    }
    const letter = props.pictographData?.letter;
    if (!letter) {
      return DEFAULT_COLOR;
    }
    const letterType = LetterType.getLetterType(letter);
    if (!letterType) {
      return DEFAULT_COLOR;
    }
    return BORDER_COLORS[letterType.folderName] || DEFAULT_COLOR;
  }
  const borderColor = getBorderColor();
  const showBorder = props.isSelected;
  const borderWidth = BORDER_WIDTH;
  const glowRadius = GLOW_RADIUS;
  if (showBorder) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="selection-border svelte-iucv9i"${attr_style(` --border-color: ${stringify(borderColor)}; --border-width: ${stringify(borderWidth)}px; --glow-radius: ${stringify(glowRadius)}px; `)}></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function AnimatedBeat($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const isSelected = props.isSelected ?? false;
  let isVisible = false;
  $$payload.out += `<div${attr_class("animated-beat-container svelte-1noymsb", void 0, {
    "animate": isVisible,
    "visible": isVisible
  })}>`;
  Beat($$payload, { beat: props.beat, onClick: props.onClick });
  $$payload.out += `<!----> `;
  if (isSelected) {
    $$payload.out += "<!--[-->";
    SelectionBorderOverlay($$payload, { pictographData: props.beat.pictographData, isSelected });
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function ReversalGlyph($$payload, $$props) {
  const { blueReversal = false, redReversal = false } = $$props;
  const blueStyle = "background-color: blue; border-radius: 50%; width: 20px; height: 20px;";
  const redStyle = "background-color: red; border-radius: 50%; width: 20px; height: 20px;";
  $$payload.out += `<div class="reversal-glyphs svelte-1ojqoel">`;
  if (blueReversal) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="reversal"${attr_style(blueStyle)} title="Blue Reversal"></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> `;
  if (redReversal) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="reversal"${attr_style(redStyle)} title="Red Reversal"></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
}
function EmptyStartPosLabel($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let isVisible = false;
  let isHovered = false;
  let isSelected = false;
  let uniqueId = `start-pos-label-${Math.random().toString(36).substring(2, 9)}`;
  $$payload.out += `<div${attr_class("empty-start-pos-label svelte-1ej10gm", void 0, {
    "visible": isVisible,
    "hovered": isHovered,
    "selected": isSelected
  })} role="button" tabindex="0" aria-label="Choose your start position"${attr("id", uniqueId)}><div class="label-content svelte-1ej10gm"><div class="glow-container svelte-1ej10gm"><div class="glow-effect svelte-1ej10gm"></div></div> <div class="instruction-container svelte-1ej10gm"><span class="instruction svelte-1ej10gm">Choose your start position</span></div></div></div>`;
  pop();
}
function BeatFrame($$payload, $$props) {
  push();
  var $$store_subs;
  function safeLog(message, data) {
  }
  const { size: sizeStore } = useResizeObserver({
    width: 800,
    height: 600
  });
  ({
    width: store_get($$store_subs ??= {}, "$sizeStore", sizeStore)?.width || 0,
    height: store_get($$store_subs ??= {}, "$sizeStore", sizeStore)?.height || 0
  });
  const sequence = useContainer(sequenceContainer);
  const {
    isScrollable = false,
    layoutOverride = null,
    elementReceiver = () => {
    },
    // Define with $bindable and default
    fullScreenMode = false
    // Add fullScreenMode prop
  } = $$props;
  let beatRows = 1;
  let beatCols = 1;
  let cellSize = 100;
  const beats = convertContainerBeatsToLegacyFormat(sequence.beats);
  const selectedBeatIds = sequence.selectedBeatIds;
  const selectedBeatIndex = selectedBeatIds.length > 0 ? beats.findIndex((beat) => beat.id === selectedBeatIds[0]) : -1;
  const beatCount = beats.length;
  function convertContainerBeatsToLegacyFormat(containerBeats) {
    return containerBeats.map((beat) => {
      const pictographData = {
        letter: beat.metadata?.letter || null,
        startPos: beat.metadata?.startPos || null,
        endPos: beat.metadata?.endPos || null,
        gridMode: beat.metadata?.gridMode || "diamond",
        redPropData: beat.redPropData || null,
        bluePropData: beat.bluePropData || null,
        redMotionData: beat.redMotionData || null,
        blueMotionData: beat.blueMotionData || null,
        redArrowData: beat.redArrowData || null,
        blueArrowData: beat.blueArrowData || null,
        grid: beat.metadata?.grid || ""
      };
      return {
        id: beat.id,
        beatNumber: beat.number,
        filled: true,
        // Assume filled if it exists in the container
        pictographData,
        duration: 1,
        // Default duration
        metadata: beat.metadata
      };
    });
  }
  function handleStartPosBeatClick() {
    const startPosCopy = null;
    const event = new CustomEvent("select-start-pos", { bubbles: true, detail: { currentStartPos: startPosCopy } });
    document.dispatchEvent(event);
  }
  function handleBeatClick(beatIndex) {
    if (beatIndex >= 0 && beatIndex < beats.length) {
      const beat = beats[beatIndex];
      const beatId = beat.id;
      safeLog("Selecting beat", {
        beatNumber: beat.beatNumber,
        motionTypes: {
          red: beat.pictographData?.redMotionData?.motionType || "none",
          blue: beat.pictographData?.blueMotionData?.motionType || "none"
        }
      });
      if (beatId) {
        sequenceContainer.selectBeat(beatId);
        const event = new CustomEvent("beat-selected", { bubbles: true, detail: { beatId } });
        document.dispatchEvent(event);
      }
    }
  }
  function addBeat2(beatData) {
    const beatWithId = beatData.id ? beatData : { ...beatData, id: crypto.randomUUID() };
    const containerBeat = {
      id: beatWithId.id || crypto.randomUUID(),
      // Ensure ID is never undefined
      number: beatWithId.beatNumber,
      redPropData: beatWithId.pictographData.redPropData,
      bluePropData: beatWithId.pictographData.bluePropData,
      redMotionData: beatWithId.pictographData.redMotionData,
      blueMotionData: beatWithId.pictographData.blueMotionData,
      redArrowData: beatWithId.pictographData.redArrowData,
      blueArrowData: beatWithId.pictographData.blueArrowData,
      metadata: {
        ...beatWithId.metadata,
        letter: beatWithId.pictographData.letter,
        startPos: beatWithId.pictographData.startPos,
        endPos: beatWithId.pictographData.endPos,
        gridMode: beatWithId.pictographData.gridMode
      }
    };
    sequenceContainer.addBeat(containerBeat);
  }
  function clearBeats() {
    sequenceContainer.setSequence([]);
  }
  function testPersistence() {
    console.log("Current sequence state:", {
      beats: sequence.beats.length,
      startPosition: "not set"
    });
    sequenceContainer.saveToLocalStorage();
    console.log("Forced save to localStorage");
    return {
      success: true,
      message: "Persistence test complete. Check console for details."
    };
  }
  const each_array = ensure_array_like(Array(beatRows));
  $$payload.out += `<div${attr_class("beat-frame-container svelte-136pd4r", void 0, {
    "scrollable-active": isScrollable,
    "fullscreen-mode": fullScreenMode
  })}><div class="beat-frame svelte-136pd4r"${attr_style(`--total-rows: ${stringify(beatRows)}; --total-cols: ${stringify(beatCount === 0 ? 1 : beatCols + 1)}; --cell-size: ${stringify(cellSize)}px;`)}><!--[-->`;
  for (let rowIndex = 0, $$length = each_array.length; rowIndex < $$length; rowIndex++) {
    each_array[rowIndex];
    const each_array_1 = ensure_array_like(Array(beatCols));
    if (rowIndex === 0) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="beat-container start-position svelte-136pd4r" style="grid-row: 1; grid-column: 1;">`;
      {
        $$payload.out += "<!--[-->";
        EmptyStartPosLabel($$payload, { onClick: handleStartPosBeatClick });
      }
      $$payload.out += `<!--]--></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--> <!--[-->`;
    for (let colIndex = 0, $$length2 = each_array_1.length; colIndex < $$length2; colIndex++) {
      each_array_1[colIndex];
      if (rowIndex * beatCols + colIndex < beats.length) {
        $$payload.out += "<!--[-->";
        const beatIndex = rowIndex * beatCols + colIndex;
        const beat = beats[beatIndex];
        $$payload.out += `<!---->`;
        {
          $$payload.out += `<div${attr_class("beat-container svelte-136pd4r", void 0, { "selected": selectedBeatIndex === beatIndex })}${attr_style(`grid-row: ${stringify(rowIndex + 1)}; grid-column: ${stringify(colIndex + (beatCount === 0 ? 1 : 2))};`)}>`;
          AnimatedBeat($$payload, {
            beat,
            onClick: () => handleBeatClick(beatIndex),
            isSelected: selectedBeatIndex === beatIndex
          });
          $$payload.out += `<!----> `;
          if (beat.metadata?.blueReversal || beat.metadata?.redReversal) {
            $$payload.out += "<!--[-->";
            $$payload.out += `<div class="reversal-indicator svelte-136pd4r">`;
            ReversalGlyph($$payload, {
              blueReversal: beat.metadata?.blueReversal || false,
              redReversal: beat.metadata?.redReversal || false
            });
            $$payload.out += `<!----></div>`;
          } else {
            $$payload.out += "<!--[!-->";
          }
          $$payload.out += `<!--]--></div>`;
        }
        $$payload.out += `<!---->`;
      } else {
        $$payload.out += "<!--[!-->";
      }
      $$payload.out += `<!--]-->`;
    }
    $$payload.out += `<!--]-->`;
  }
  $$payload.out += `<!--]--></div></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  bind_props($$props, {
    isScrollable,
    layoutOverride,
    elementReceiver,
    fullScreenMode,
    addBeat: addBeat2,
    clearBeats,
    testPersistence
  });
  pop();
}
function SequenceContent($$payload, $$props) {
  push();
  const {
    containerHeight = 0,
    containerWidth = 0,
    onBeatSelected = (beatId) => {
    }
  } = $$props;
  let beatFrameShouldScroll = false;
  let sequenceName = "";
  let beatFrameElement = null;
  setContext(BEAT_FRAME_CONTEXT_KEY, {
    getElement: () => beatFrameElement,
    setElement: (el) => {
      if (el) {
        beatFrameElement = el;
        const event = new CustomEvent("beatframe-element-available", { bubbles: true, detail: { element: el } });
        document.dispatchEvent(event);
        return true;
      }
      return false;
    }
  });
  $$payload.out += `<div class="sequence-container svelte-1pyes1o"${attr_style("", {
    "justify-content": "center",
    "align-items": "center"
  })}><div${attr_class("content-wrapper svelte-1pyes1o", void 0, { "scroll-mode-active": beatFrameShouldScroll })}><div${attr_class("label-and-beatframe-unit svelte-1pyes1o", void 0, { "scroll-mode-active": beatFrameShouldScroll })}><div class="sequence-widget-labels svelte-1pyes1o">`;
  CurrentWordLabel($$payload, { currentWord: sequenceName });
  $$payload.out += `<!----></div> <div${attr_class("beat-frame-wrapper svelte-1pyes1o", void 0, { "scroll-mode-active": beatFrameShouldScroll })}>`;
  BeatFrame($$payload, {
    isScrollable: beatFrameShouldScroll,
    elementReceiver(el) {
      if (el) {
        beatFrameElement = el;
        const event = new CustomEvent("beatframe-element-available", { bubbles: true, detail: { element: el } });
        document.dispatchEvent(event);
      }
    }
  });
  $$payload.out += `<!----></div></div></div></div>`;
  bind_props($$props, { containerHeight, containerWidth });
  pop();
}
function SequenceOverlay($$payload, $$props) {
  push();
  var $$store_subs;
  const { title = null, children = void 0 } = $$props;
  const isOpen = store_get($$store_subs ??= {}, "$sequenceOverlayStore", sequenceOverlayStore).isOpen;
  const MAX_CHARS = 8;
  const displayTitle = title && title.length > MAX_CHARS ? title.substring(0, MAX_CHARS) + "..." : title;
  if (isOpen) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="sequence-overlay-wrapper svelte-1eavlwx"><button class="background-button svelte-1eavlwx" aria-label="Close sequence overlay"></button> <div class="sequence-content svelte-1eavlwx" role="dialog" aria-modal="true"${attr("aria-labelledby", title ? "sequence-title" : void 0)} tabindex="-1">`;
    if (title) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="sequence-header svelte-1eavlwx"><h2 id="sequence-title" class="svelte-1eavlwx">${escape_html(displayTitle)}</h2></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--> <button class="close-button svelte-1eavlwx" aria-label="Close sequence overlay" title="Close sequence overlay"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button> <div class="sequence-body svelte-1eavlwx"><div class="content-wrapper">`;
    children?.($$payload);
    $$payload.out += `<!----></div></div></div></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  bind_props($$props, { children });
  pop();
}
function SequenceOverlayContent($$payload, $$props) {
  push();
  const { title = "" } = $$props;
  let cols = 1;
  const beats = sequenceContainer.state.beats;
  const beatCount = beats.length;
  function getBeatPosition(index) {
    {
      const row = Math.floor(index / cols);
      const col = index % cols + 1;
      return { row, col };
    }
  }
  const each_array = ensure_array_like(beats);
  $$payload.out += `<div class="fullscreen-overlay-container fullscreen-beat-container svelte-1qvp2ql"${attr("data-beat-count", beatCount)}>`;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> <div class="sequence-grid svelte-1qvp2ql">`;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> <!--[-->`;
  for (let index = 0, $$length = each_array.length; index < $$length; index++) {
    let beat = each_array[index];
    const position = getBeatPosition(index);
    $$payload.out += `<div class="grid-item svelte-1qvp2ql"${attr_style(`grid-column: ${stringify(position.col)}; grid-row: ${stringify(position.row + 1)};`)}><div class="pictograph-container svelte-1qvp2ql">`;
    Pictograph($$payload, {
      pictographData: {
        letter: beat.metadata?.letter || null,
        startPos: beat.metadata?.startPos || null,
        endPos: beat.metadata?.endPos || null,
        gridMode: beat.metadata?.gridMode || "diamond",
        redPropData: beat.redPropData || null,
        bluePropData: beat.bluePropData || null,
        redMotionData: beat.redMotionData || null,
        blueMotionData: beat.blueMotionData || null,
        redArrowData: beat.redArrowData || null,
        blueArrowData: beat.blueArrowData || null,
        grid: beat.metadata?.grid || ""
      },
      beatNumber: index + 1
    });
    $$payload.out += `<!----></div></div>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  bind_props($$props, { title });
  pop();
}
function DeleteButton($$payload, $$props) {
  push();
  const { $$slots, $$events, ...dispatch } = $$props;
  $$payload.out += `<button class="delete-button ripple svelte-18nhvlj" aria-label="Delete options" data-mdb-ripple="true" data-mdb-ripple-color="light"><div class="icon-wrapper svelte-18nhvlj"><i class="fa-solid fa-trash svelte-18nhvlj"></i></div></button>`;
  pop();
}
function DeleteModal($$payload, $$props) {
  push();
  const { isOpen = false, hasSelectedBeat = false, buttonRect = null } = $$props;
  let popupPosition = { left: 0, position: "", arrowOffset: 0 };
  const popupStyle = buttonRect ? `left: ${popupPosition.left}px; ${popupPosition.position} --arrow-offset: ${popupPosition.arrowOffset}px; --position-above: ${"1"};` : "";
  if (isOpen) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="popup-backdrop svelte-7gixpi" role="dialog" aria-modal="true" aria-labelledby="delete-popup-title" tabindex="-1"><div class="popup-container svelte-7gixpi"${attr_style(popupStyle, {
      transform: "translateX(-50%)",
      "transform-origin": `calc(50% + var(--arrow-offset)) ${"100%"}`
    })} data-testid="delete-popup-container"><div class="popup-content svelte-7gixpi"><div class="option-buttons svelte-7gixpi"><button class="option-button remove-beat svelte-7gixpi"><div class="option-icon svelte-7gixpi"><i class="fa-solid fa-trash"></i></div> <div class="option-text svelte-7gixpi"><span class="option-title svelte-7gixpi">Remove Selected Beat</span> <span class="option-description svelte-7gixpi">${escape_html(hasSelectedBeat ? "Delete the currently selected beat" : "Click a beat to delete it")}</span></div></button> <button class="option-button clear-sequence svelte-7gixpi"><div class="option-icon svelte-7gixpi"><i class="fa-solid fa-eraser"></i></div> <div class="option-text svelte-7gixpi"><span class="option-title svelte-7gixpi">Clear Entire Sequence</span> <span class="option-description svelte-7gixpi">Remove all beats and reset start position</span></div></button></div> <div class="popup-footer svelte-7gixpi"><button class="cancel-button svelte-7gixpi">Cancel</button></div></div></div></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function SequenceOverlayButton($$payload, $$props) {
  push();
  $$payload.out += `<button class="sequence-overlay-button ripple svelte-cefdb" aria-label="View sequence in overlay" data-mdb-ripple="true" data-mdb-ripple-color="light"><div class="icon-wrapper svelte-cefdb"><i class="fa-solid fa-up-right-and-down-left-from-center svelte-cefdb"></i></div></button>`;
  pop();
}
function ClearSequenceButton($$payload, $$props) {
  push();
  $$payload.out += `<button class="clear-button ripple svelte-1ck6x27" aria-label="Clear sequence" data-mdb-ripple="true" data-mdb-ripple-color="light"><div class="icon-wrapper svelte-1ck6x27"><i class="fa-solid fa-eraser svelte-1ck6x27"></i></div></button> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function ShareButton($$payload, $$props) {
  push();
  let isRendering = false;
  let showSuccessIndicator = false;
  const { beatFrameElement = null } = $$props;
  const sequence = useContainer(sequenceContainer);
  const sequenceBeats = sequence.beats || [];
  generateSequenceName(sequenceBeats);
  getContext(BEAT_FRAME_CONTEXT_KEY);
  function generateSequenceName(beats) {
    if (!beats || beats.length === 0) return "Sequence";
    const letters = beats.map((beat) => beat.letter || beat.metadata?.letter || "").filter((letter) => letter.trim() !== "").join("");
    return letters || "Sequence";
  }
  $$payload.out += `<button${attr_class("share-button svelte-yzq2eo", void 0, { "loading": isRendering, "success": showSuccessIndicator })} aria-label="Share sequence"><div class="icon-wrapper svelte-yzq2eo">`;
  {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<i class="fa-solid fa-share-alt svelte-yzq2eo"></i>`;
  }
  $$payload.out += `<!--]--></div> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></button> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function SettingsButton($$payload, $$props) {
  push();
  $$payload.out += `<button class="settings-button ripple svelte-oep5e0" aria-label="Settings" data-mdb-ripple="true" data-mdb-ripple-color="light"><div class="icon-wrapper svelte-oep5e0"><i class="fa-solid fa-gear settings-icon svelte-oep5e0" aria-hidden="true"></i></div></button>`;
  pop();
}
function SequenceWidget($$payload, $$props) {
  push();
  var $$store_subs;
  console.log("SequenceWidget: ShareButton imported:", ShareButton);
  const { size } = useResizeObserver();
  const { dimensions } = useResponsiveLayout$1();
  getContext(BEAT_FRAME_CONTEXT_KEY);
  let isDeleteModalOpen = false;
  let isInDeletionMode = false;
  let deleteButtonRect = null;
  const workbenchIsPortrait = calculateWorkbenchIsPortrait(store_get($$store_subs ??= {}, "$dimensions", dimensions).width, store_get($$store_subs ??= {}, "$size", size).height);
  const buttonSizeFactor = calculateButtonSizeFactor(store_get($$store_subs ??= {}, "$dimensions", dimensions).width, store_get($$store_subs ??= {}, "$dimensions", dimensions).height);
  let sequenceName = "";
  let hasSelectedBeat = false;
  function handleDeleteButtonClick(buttonRect) {
    deleteButtonRect = buttonRect;
    isDeleteModalOpen = true;
  }
  function exitDeletionMode() {
    isInDeletionMode = false;
    document.removeEventListener("click", handleDocumentClick);
    document.removeEventListener("keydown", handleEscapeKey);
  }
  function updateTooltipPosition() {
  }
  function handleDocumentClick(event) {
  }
  function handleEscapeKey(event) {
    if (event.key === "Escape") {
      exitDeletionMode();
    }
  }
  function handleBeatSelected(event) {
    if (isInDeletionMode) {
      const beatId = event.detail.beatId;
      if (beatId) {
        sequenceActions.removeBeatAndFollowing(beatId);
        exitDeletionMode();
      }
    }
  }
  onDestroy(() => {
    document.removeEventListener("beat-selected", handleBeatSelected);
    document.removeEventListener("click", handleDocumentClick);
    document.removeEventListener("keydown", handleEscapeKey);
    window.removeEventListener("resize", updateTooltipPosition);
  });
  $$payload.out += `<!---->`;
  {
    $$payload.out += `<div class="sequence-widget svelte-1jrztl9"><div${attr_class("main-layout svelte-1jrztl9", void 0, { "portrait": workbenchIsPortrait })}${attr_style(`--container-width: ${stringify(store_get($$store_subs ??= {}, "$dimensions", dimensions).width)}px; --container-height: ${stringify(store_get($$store_subs ??= {}, "$dimensions", dimensions).height)}px; --button-size-factor: ${stringify(buttonSizeFactor)};`)}><div class="left-vbox svelte-1jrztl9">`;
    SequenceContent($$payload, {
      containerHeight: store_get($$store_subs ??= {}, "$size", size).height,
      containerWidth: store_get($$store_subs ??= {}, "$dimensions", dimensions).width,
      onBeatSelected: (beatId) => {
        const customEvent = new CustomEvent("beatselected", { detail: { beatId } });
        handleBeatSelected(customEvent);
      }
    });
    $$payload.out += `<!----></div> `;
    SettingsButton($$payload);
    $$payload.out += `<!----> `;
    DeleteButton($$payload, { onClick: handleDeleteButtonClick });
    $$payload.out += `<!----> `;
    ClearSequenceButton($$payload);
    $$payload.out += `<!----> `;
    SequenceOverlayButton($$payload);
    $$payload.out += `<!----> `;
    ShareButton($$payload, {});
    $$payload.out += `<!----> `;
    {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div> `;
    SequenceOverlay($$payload, {
      title: sequenceName,
      children: ($$payload2) => {
        SequenceOverlayContent($$payload2, { title: sequenceName });
      },
      $$slots: { default: true }
    });
    $$payload.out += `<!----> `;
    DeleteModal($$payload, {
      isOpen: isDeleteModalOpen,
      hasSelectedBeat,
      buttonRect: deleteButtonRect
    });
    $$payload.out += `<!----> `;
    if (isInDeletionMode) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="deletion-mode-overlay svelte-1jrztl9" aria-hidden="true"></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div>`;
  }
  $$payload.out += `<!---->`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
const DEFAULT_SETTINGS = {
  generatorType: "circular",
  numBeats: 8,
  turnIntensity: 2,
  propContinuity: "continuous",
  capType: "mirrored",
  level: 1,
  theme: "system",
  animationsEnabled: true,
  lastUsedGeneratorType: "circular",
  favoriteCapTypes: ["mirrored", "rotated"]
};
createStore(
  "settings",
  DEFAULT_SETTINGS,
  (set, update) => ({
    setGeneratorType: (type) => {
      update((state) => ({
        ...state,
        generatorType: type,
        lastUsedGeneratorType: type
      }));
    },
    setNumBeats: (beats) => {
      update((state) => ({
        ...state,
        numBeats: Math.max(1, Math.min(32, beats))
        // Clamp between 1-32
      }));
    },
    setTurnIntensity: (intensity) => {
      update((state) => ({
        ...state,
        turnIntensity: Math.max(1, Math.min(5, intensity))
        // Clamp between 1-5
      }));
    },
    setPropContinuity: (continuity) => {
      update((state) => ({
        ...state,
        propContinuity: continuity
      }));
    },
    setCAPType: (type) => {
      update((state) => ({
        ...state,
        capType: type
      }));
    },
    setLevel: (level) => {
      update((state) => ({
        ...state,
        level: Math.max(1, Math.min(5, level))
        // Clamp between 1-5
      }));
    },
    setTheme: (theme) => {
      update((state) => ({
        ...state,
        theme
      }));
    },
    toggleAnimations: () => {
      update((state) => ({
        ...state,
        animationsEnabled: !state.animationsEnabled
      }));
    },
    addFavoriteCapType: (type) => {
      update((state) => {
        if (state.favoriteCapTypes.includes(type)) {
          return state;
        }
        return {
          ...state,
          favoriteCapTypes: [...state.favoriteCapTypes, type]
        };
      });
    },
    removeFavoriteCapType: (type) => {
      update((state) => ({
        ...state,
        favoriteCapTypes: state.favoriteCapTypes.filter((t) => t !== type)
      }));
    },
    resetSettings: () => {
      set(DEFAULT_SETTINGS);
    }
  }),
  {
    persist: true,
    description: "Application settings including sequence generation parameters"
  }
);
function GenerateButton($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const isLoading = props.isLoading ?? false;
  const hasError = props.hasError ?? false;
  const statusMessage = props.statusMessage ?? "";
  const text = props.text ?? "Generate Sequence";
  $$payload.out += `<div class="button-container svelte-ne2t2n"><button${attr_class("generate-button svelte-ne2t2n", void 0, { "loading": isLoading, "error": hasError })}${attr("disabled", isLoading, true)}><div class="button-content svelte-ne2t2n">`;
  if (isLoading) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="spinner-container svelte-ne2t2n"><div class="spinner svelte-ne2t2n"></div></div> <span class="button-text svelte-ne2t2n">${escape_html(statusMessage || "Generating...")}</span>`;
  } else if (hasError) {
    $$payload.out += "<!--[1-->";
    $$payload.out += `<div class="icon-container error-icon svelte-ne2t2n"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svelte-ne2t2n"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" class="svelte-ne2t2n"></path><line x1="12" y1="9" x2="12" y2="13" class="svelte-ne2t2n"></line><line x1="12" y1="17" x2="12.01" y2="17" class="svelte-ne2t2n"></line></svg></div> <span class="button-text svelte-ne2t2n">Try Again</span>`;
  } else {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<div class="icon-container svelte-ne2t2n"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svelte-ne2t2n"><polygon points="5 3 19 12 5 21 5 3" class="svelte-ne2t2n"></polygon></svg></div> <span class="button-text svelte-ne2t2n">${escape_html(text)}</span>`;
  }
  $$payload.out += `<!--]--></div> <div class="button-background svelte-ne2t2n"></div></button> `;
  if (hasError) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="error-message svelte-ne2t2n">${escape_html(statusMessage)}</div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function CAPButton($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  const selected = props.selected ?? false;
  $$payload.out += `<button${attr_class("cap-button svelte-1k24p3o", void 0, { "selected": selected })}${attr("title", props.capType.description)}><div class="cap-button-content svelte-1k24p3o"><span class="cap-label svelte-1k24p3o">${escape_html(props.capType.label)}</span> `;
  if (selected) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<span class="selected-indicator svelte-1k24p3o">✓</span>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div></button>`;
  pop();
}
function CAPPicker($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  function handleSelect(capId) {
    if (props.onSelect) {
      props.onSelect(capId);
    }
  }
  const groupedCapTypes = {
    mirror: props.capTypes.filter((cap) => cap.id.toLowerCase().includes("mirrored")),
    rotate: props.capTypes.filter((cap) => cap.id.toLowerCase().includes("rotated")),
    other: props.capTypes.filter((cap) => !cap.id.toLowerCase().includes("mirrored") && !cap.id.toLowerCase().includes("rotated"))
  };
  const each_array = ensure_array_like(Object.entries(groupedCapTypes));
  $$payload.out += `<div class="cap-picker svelte-lkt4o0"><!--[-->`;
  for (let $$index_1 = 0, $$length = each_array.length; $$index_1 < $$length; $$index_1++) {
    let [groupName, typesInGroup] = each_array[$$index_1];
    if (typesInGroup.length > 0) {
      $$payload.out += "<!--[-->";
      const each_array_1 = ensure_array_like(typesInGroup);
      $$payload.out += `<div class="cap-group svelte-lkt4o0"><h5 class="group-title svelte-lkt4o0">${escape_html(groupName.charAt(0).toUpperCase() + groupName.slice(1))} Types</h5> <div class="cap-buttons-list svelte-lkt4o0"><!--[-->`;
      for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
        let capType = each_array_1[$$index];
        CAPButton($$payload, {
          capType,
          selected: props.selectedCapId === capType.id,
          onClick: () => handleSelect(capType.id)
        });
      }
      $$payload.out += `<!--]--></div></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]-->`;
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function CircularSequencer($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let selectedCapType = props.selectedCapType ?? "mirrored";
  const capTypesData = [
    {
      id: "mirrored",
      label: "Mirrored",
      description: "Second half mirrors the first."
    },
    {
      id: "rotated",
      label: "Rotated",
      description: "Second half rotates the first."
    },
    {
      id: "mirrored_complementary",
      label: "Mirrored Complementary",
      description: "Mirrored with complementary motion."
    },
    // Add all your CAP types here
    {
      id: "rotated_complementary",
      label: "Rotated Complementary",
      description: "Rotated with complementary motion."
    },
    {
      id: "mirrored_swapped",
      label: "Mirrored Swapped",
      description: "Mirrored with swapped prop colors."
    },
    {
      id: "rotated_swapped",
      label: "Rotated Swapped",
      description: "Rotated with swapped prop colors."
    },
    {
      id: "strict_mirrored",
      label: "Strict Mirrored",
      description: "Strictly mirrored sequence."
    },
    {
      id: "strict_rotated",
      label: "Strict Rotated",
      description: "Strictly rotated sequence."
    }
  ];
  function handleCapTypeSelect(capId) {
    const isValidCapType = capTypesData.some((capType) => capType.id === capId);
    if (isValidCapType) {
      const newCapType = capId;
      selectedCapType = newCapType;
      if (props.onCapTypeChange) {
        props.onCapTypeChange(newCapType);
      }
    }
  }
  $$payload.out += `<div class="circular-sequencer-controls svelte-ayh42k"><h4 class="sequencer-title svelte-ayh42k">Circular Options</h4> <div class="options-content svelte-ayh42k">`;
  CAPPicker($$payload, {
    capTypes: capTypesData,
    selectedCapId: selectedCapType,
    onSelect: handleCapTypeSelect
  });
  $$payload.out += `<!----></div></div>`;
  pop();
}
function LetterTypePicker($$payload, $$props) {
  push();
  let options = $$props["options"];
  let selectedTypes = fallback($$props["selectedTypes"], () => [], true);
  const each_array = ensure_array_like(options);
  $$payload.out += `<div class="letter-type-picker svelte-ga4tbq"><h4 class="svelte-ga4tbq">Letter Type Selection</h4> <div class="letter-types-grid svelte-ga4tbq"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let option = each_array[$$index];
    $$payload.out += `<button${attr_class("letter-type-button svelte-ga4tbq", void 0, { "selected": selectedTypes.includes(option.id) })}><div class="letter-type-content svelte-ga4tbq"><span class="letter-type-label svelte-ga4tbq">${escape_html(option.label)}</span> <span class="letter-type-description svelte-ga4tbq">${escape_html(option.description)}</span></div></button>`;
  }
  $$payload.out += `<!--]--></div> <div class="selection-info svelte-ga4tbq">`;
  if (selectedTypes.length === 0) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<p class="info-text svelte-ga4tbq">No letter types selected. All types will be used.</p>`;
  } else {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<p class="info-text svelte-ga4tbq">Selected types: ${escape_html(selectedTypes.length)}</p>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  bind_props($$props, { options, selectedTypes });
  pop();
}
function FreeformSequencer($$payload, $$props) {
  push();
  const letterTypeOptionsData = [
    {
      id: "type1",
      label: "Type 1",
      description: "Basic motions, simple transitions."
    },
    {
      id: "type2",
      label: "Type 2",
      description: "Intermediate flow, common patterns."
    },
    {
      id: "type3",
      label: "Type 3",
      description: "Advanced patterns, complex movements."
    },
    {
      id: "type4",
      label: "Type 4",
      description: "Expert sequences, intricate combinations."
    },
    {
      id: "alpha",
      label: "Alpha Series",
      description: "Focus on Alpha-based movements."
    },
    {
      id: "beta",
      label: "Beta Series",
      description: "Focus on Beta-based movements."
    },
    {
      id: "gamma",
      label: "Gamma Series",
      description: "Focus on Gamma-based movements."
    }
  ];
  let selectedLetterTypes = [];
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
    $$payload2.out += `<div class="freeform-sequencer-controls svelte-c6anqd"><h4 class="sequencer-title svelte-c6anqd">Freeform Options</h4> <div class="options-content svelte-c6anqd">`;
    LetterTypePicker($$payload2, {
      options: letterTypeOptionsData,
      get selectedTypes() {
        return selectedLetterTypes;
      },
      set selectedTypes($$value) {
        selectedLetterTypes = $$value;
        $$settled = false;
      }
    });
    $$payload2.out += `<!----> <div class="info-panel svelte-c6anqd">Selected Types: ${escape_html(selectedLetterTypes.length > 0 ? selectedLetterTypes.map((id) => letterTypeOptionsData.find((opt) => opt.id === id)?.label || id).join(", ") : "All (Default)")}</div></div></div>`;
  }
  do {
    $$settled = true;
    $$inner_payload = copy_payload($$payload);
    $$render_inner($$inner_payload);
  } while (!$$settled);
  assign_payload($$payload, $$inner_payload);
  pop();
}
function ModernGenerationControls($$payload, $$props) {
  push();
  const MAX_INTENSITY = 5;
  const MIN_BEATS = 1;
  const MAX_BEATS = 32;
  const intensityLabels = ["Minimal", "Light", "Moderate", "Heavy", "Extreme"];
  const continuityOptions = [
    { id: "continuous", label: "Continuous" },
    { id: "random", label: "Random" }
  ];
  const generatorType = sequenceSelectors.generationType();
  const isGenerating = sequenceSelectors.isGenerating();
  const hasError = sequenceSelectors.hasError();
  const statusMessage = sequenceSelectors.message();
  let numBeats = 8;
  let turnIntensity = 3;
  let propContinuity = "continuous";
  let capType = "mirrored";
  let level = 3;
  const currentIntensityLabel = intensityLabels[turnIntensity - 1];
  let inputValue = "8";
  function handleGenerate() {
    const settings = { numBeats, turnIntensity, propContinuity, capType, level };
    sequenceActions.generate(generatorType, settings);
  }
  const each_array = ensure_array_like(Array(MAX_INTENSITY));
  const each_array_1 = ensure_array_like(continuityOptions);
  $$payload.out += `<div class="modern-generation-controls svelte-17x3mmb"><div class="generator-type-container svelte-17x3mmb"><div class="generator-toggle-wrapper svelte-17x3mmb"><button${attr_class("generator-type-button svelte-17x3mmb", void 0, { "active": generatorType === "circular" })}><span class="generator-icon svelte-17x3mmb">⭕</span> <span>Circular</span></button> <button${attr_class("generator-type-button svelte-17x3mmb", void 0, { "active": generatorType === "freeform" })}><span class="generator-icon svelte-17x3mmb">🔀</span> <span>Freeform</span></button></div></div> <div class="controls-grid svelte-17x3mmb"><div class="control-card svelte-17x3mmb"><label for="beat-length" class="svelte-17x3mmb">Sequence Length</label> <div class="control-group svelte-17x3mmb"><button class="control-button decrement svelte-17x3mmb"${attr("disabled", numBeats <= MIN_BEATS, true)} aria-label="Decrease beats">-</button> <input id="beat-length" type="text" class="beat-input svelte-17x3mmb"${attr("value", inputValue)}${attr("min", MIN_BEATS)}${attr("max", MAX_BEATS)} aria-label="Number of beats"/> <button class="control-button increment svelte-17x3mmb"${attr("disabled", numBeats >= MAX_BEATS, true)} aria-label="Increase beats">+</button></div></div> <div class="control-card svelte-17x3mmb"><div class="control-header svelte-17x3mmb"><label for="turn-intensity" class="svelte-17x3mmb">Turn Intensity</label> <span class="current-level svelte-17x3mmb">${escape_html(currentIntensityLabel)}</span></div> <div id="turn-intensity" class="intensity-buttons svelte-17x3mmb"><!--[-->`;
  for (let i = 0, $$length = each_array.length; i < $$length; i++) {
    each_array[i];
    const level2 = i + 1;
    $$payload.out += `<button${attr_class("intensity-button svelte-17x3mmb", void 0, { "active": turnIntensity === level2 })}${attr("aria-label", `Set turn intensity to ${stringify(intensityLabels[i])}`)}${attr("aria-pressed", turnIntensity === level2)}>${escape_html(level2)}</button>`;
  }
  $$payload.out += `<!--]--></div></div> <div class="control-card svelte-17x3mmb"><label for="prop-continuity-toggle" class="svelte-17x3mmb">Prop Continuity</label> <div class="toggle-control svelte-17x3mmb"><button id="prop-continuity-toggle" type="button" class="toggle-track svelte-17x3mmb" aria-label="Toggle Prop Continuity"><div class="toggle-labels svelte-17x3mmb"><!--[-->`;
  for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
    let option = each_array_1[$$index_1];
    $$payload.out += `<span${attr_class("toggle-label svelte-17x3mmb", void 0, { "selected": option.id === propContinuity })}>${escape_html(option.label)}</span>`;
  }
  $$payload.out += `<!--]--></div> <div${attr_class("toggle-thumb svelte-17x3mmb", void 0, { "right": propContinuity === "random" })}></div></button></div> <div class="description svelte-17x3mmb">`;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<p class="svelte-17x3mmb">Props maintain rotation direction</p>`;
  }
  $$payload.out += `<!--]--></div></div> <div class="control-card svelte-17x3mmb"><label for="complexity-level" class="svelte-17x3mmb">Complexity Level</label> <div id="complexity-level" class="level-buttons svelte-17x3mmb" role="radiogroup"><button${attr_class("level-button svelte-17x3mmb", void 0, { "active": level === 1 })}>Beginner</button> <button${attr_class("level-button svelte-17x3mmb", void 0, { "active": level === 3 })}>Intermediate</button> <button${attr_class("level-button svelte-17x3mmb", void 0, { "active": level === 5 })}>Advanced</button></div></div></div> <div class="generator-options svelte-17x3mmb">`;
  if (generatorType === "circular") {
    $$payload.out += "<!--[-->";
    CircularSequencer($$payload, {});
  } else {
    $$payload.out += "<!--[!-->";
    FreeformSequencer($$payload);
  }
  $$payload.out += `<!--]--></div> <div class="generate-button-container svelte-17x3mmb">`;
  GenerateButton($$payload, {
    isLoading: isGenerating,
    hasError,
    statusMessage,
    onClick: handleGenerate
  });
  $$payload.out += `<!----></div></div>`;
  pop();
}
function getNextOptions(sequence) {
  if (!sequence || sequence.length === 0) {
    return generateStartingOptions();
  }
  return generateNextOptionsFromSequence(sequence);
}
function generateStartingOptions() {
  return [
    createBasicOption("A", "alpha", "alpha"),
    createBasicOption("B", "alpha", "beta"),
    createBasicOption("C", "alpha", "gamma")
  ];
}
function generateNextOptionsFromSequence(sequence) {
  const lastBeat = sequence[sequence.length - 1];
  if (!lastBeat) return generateStartingOptions();
  const options = [];
  const letters = ["A", "B", "C", "D", "E", "F"];
  const positions = ["alpha", "beta", "gamma"];
  for (const letter of letters) {
    for (const startPos of positions) {
      for (const endPos of positions) {
        options.push(createBasicOption(letter, startPos, endPos));
      }
    }
  }
  return options.slice(0, 20);
}
function createBasicOption(letter, startPos, endPos) {
  return {
    letter,
    startPos,
    endPos,
    timing: null,
    direction: null,
    gridMode: "diamond",
    gridData: null,
    blueMotionData: {
      id: crypto.randomUUID(),
      color: "blue",
      motionType: "pro",
      startLoc: "n",
      endLoc: "s",
      startOri: "in",
      endOri: "out",
      turns: 1,
      propRotDir: "clockwise"
    },
    redMotionData: {
      id: crypto.randomUUID(),
      color: "red",
      motionType: "anti",
      startLoc: "s",
      endLoc: "n",
      startOri: "out",
      endOri: "in",
      turns: 1,
      propRotDir: "counter_clockwise"
    },
    redPropData: null,
    bluePropData: null,
    redArrowData: null,
    blueArrowData: null,
    grid: "diamond"
  };
}
function determineReversalCategory(sequence, option) {
  if (!sequence || sequence.length === 0) {
    return "continuous";
  }
  const lastBeat = sequence[sequence.length - 1];
  if (!lastBeat || !lastBeat.redMotionData || !lastBeat.blueMotionData) {
    return "continuous";
  }
  if (!option.redMotionData || !option.blueMotionData) {
    return "continuous";
  }
  const redContinuous = lastBeat.redMotionData.propRotDir === option.redMotionData.propRotDir;
  const blueContinuous = lastBeat.blueMotionData.propRotDir === option.blueMotionData.propRotDir;
  if (redContinuous && blueContinuous) {
    return "continuous";
  } else if (redContinuous || blueContinuous) {
    return "one_reversal";
  } else {
    return "two_reversals";
  }
}
function determineGroupKey(option, sortMethod, sequence) {
  switch (sortMethod) {
    case "type":
      return getLetterType(option.letter);
    case "letter":
      return option.letter || "Unknown";
    case "reversal":
      return determineReversalCategory(sequence, option);
    case "grid":
      return option.gridMode || "diamond";
    default:
      return "all";
  }
}
function getLetterType(letter) {
  if (!letter) return "Unknown";
  const type1Letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"];
  const type2Letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"];
  const type3Letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"];
  const type4Letters = ["Φ", "Ψ", "Λ"];
  const type5Letters = ["Φ-", "Ψ-", "Λ-"];
  const type6Letters = ["α", "β", "Γ"];
  if (type1Letters.includes(letter)) return "Type 1";
  if (type2Letters.includes(letter)) return "Type 2";
  if (type3Letters.includes(letter)) return "Type 3";
  if (type4Letters.includes(letter)) return "Type 4";
  if (type5Letters.includes(letter)) return "Type 5";
  if (type6Letters.includes(letter)) return "Type 6";
  return "Unknown";
}
function getSortedGroupKeys(keys, sortMethod) {
  switch (sortMethod) {
    case "type":
      return keys.sort((a, b) => {
        const order = ["Type 1", "Type 2", "Type 3", "Type 4", "Type 5", "Type 6", "Unknown"];
        return order.indexOf(a) - order.indexOf(b);
      });
    case "letter":
      return keys.sort();
    case "reversal":
      return keys.sort((a, b) => {
        const order = ["continuous", "one_reversal", "two_reversals"];
        return order.indexOf(a) - order.indexOf(b);
      });
    case "grid":
      return keys.sort();
    default:
      return keys.sort();
  }
}
function getSorter(sortMethod, sequence) {
  switch (sortMethod) {
    case "type":
      return (a, b) => {
        const typeA = getLetterType(a.letter);
        const typeB = getLetterType(b.letter);
        return typeA.localeCompare(typeB);
      };
    case "letter":
      return (a, b) => {
        const letterA = a.letter || "";
        const letterB = b.letter || "";
        return letterA.localeCompare(letterB);
      };
    case "reversal":
      return (a, b) => {
        const reversalA = determineReversalCategory(sequence, a);
        const reversalB = determineReversalCategory(sequence, b);
        return reversalA.localeCompare(reversalB);
      };
    case "grid":
      return (a, b) => {
        const gridA = a.gridMode || "";
        const gridB = b.gridMode || "";
        return gridA.localeCompare(gridB);
      };
    default:
      return () => 0;
  }
}
const sequenceStore = writable([]);
const optionsStore = writable([]);
function getStoredState() {
  return { sortMethod: "type", lastSelectedTab: {} };
}
const storedState = getStoredState();
const uiState = writable({
  sortMethod: storedState.sortMethod,
  isLoading: false,
  error: null,
  lastSelectedTab: storedState.lastSelectedTab
});
const filteredOptionsStore = derived(
  [optionsStore, sequenceStore, uiState],
  ([$options, $sequence, $ui]) => {
    let options = [...$options];
    options.sort(getSorter($ui.sortMethod, $sequence));
    return options;
  }
);
const groupedOptionsStore = derived(
  [filteredOptionsStore, sequenceStore, uiState],
  ([$filteredOptions, $sequence, $ui]) => {
    const groups = {};
    $filteredOptions.forEach((option) => {
      const groupKey = determineGroupKey(option, $ui.sortMethod, $sequence);
      if (!groups[groupKey]) groups[groupKey] = [];
      groups[groupKey].push(option);
    });
    const sortedKeys = getSortedGroupKeys(Object.keys(groups), $ui.sortMethod);
    const sortedGroups = {};
    sortedKeys.forEach((key) => {
      if (groups[key]) {
        sortedGroups[key] = groups[key];
      }
    });
    return sortedGroups;
  }
);
({
  subscribe: derived([optionsStore, sequenceStore, uiState], ([$options, $sequence, $ui]) => ({
    allOptions: $options,
    currentSequence: $sequence,
    sortMethod: $ui.sortMethod,
    isLoading: $ui.isLoading,
    error: $ui.error
    // components interact via actions or specific selectors if needed.
  })).subscribe
});
function memoizeLRU(fn, maxSize = 100, keyFn) {
  const cache = /* @__PURE__ */ new Map();
  const keyOrder = [];
  const memoized = (...args) => {
    const key = keyFn ? keyFn(...args) : JSON.stringify(args);
    if (cache.has(key)) {
      const keyIndex = keyOrder.indexOf(key);
      if (keyIndex > -1) {
        keyOrder.splice(keyIndex, 1);
      }
      keyOrder.push(key);
      return cache.get(key);
    }
    if (cache.size >= maxSize && keyOrder.length > 0) {
      const oldestKey = keyOrder.shift();
      if (oldestKey) cache.delete(oldestKey);
    }
    const result = fn(...args);
    cache.set(key, result);
    keyOrder.push(key);
    return result;
  };
  memoized.clearCache = () => {
    cache.clear();
    keyOrder.length = 0;
  };
  return memoized;
}
const BREAKPOINTS = {
  smallMobile: 375,
  mobile: 480,
  tablet: 768,
  laptop: 1024,
  desktop: 1280
};
const ASPECT_RATIO = {
  tall: 0.8,
  square: 1.3
};
const DEVICE_CONFIG = {
  smallMobile: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 150,
    scaleFactor: 1
  },
  mobile: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 175,
    scaleFactor: 1
  },
  tablet: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 175,
    scaleFactor: 1
  },
  desktop: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 90,
    maxItemSize: 180,
    scaleFactor: 1
  },
  largeDesktop: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 100,
    maxItemSize: 200,
    scaleFactor: 1
  }
};
const LAYOUT_TEMPLATES = {
  singleItem: {
    cols: 1,
    class: "single-item-grid"
  },
  twoItems: {
    horizontal: { cols: 2, class: "two-item-grid horizontal-layout" },
    vertical: { cols: 1, class: "two-item-grid vertical-layout" }
  },
  fewItems: {
    portraitDevice: { cols: 4, class: "few-items-grid" },
    landscapeDevice: { cols: 4, class: "few-items-grid" }
  },
  mediumItems: {
    portraitDevice: { cols: 4, class: "medium-items-grid" },
    landscapeDevice: { cols: 4, class: "medium-items-grid" }
  },
  manyItems: {
    portraitDevice: { cols: 4, class: "many-items-grid" },
    landscapeDevice: { cols: 4, class: "many-items-grid" }
  }
};
const GAP_ADJUSTMENTS = {
  singleItem: 0,
  twoItems: 3,
  fewItems: 3,
  mediumItems: 3,
  manyItems: 3
};
function getContainerAspect(width, height) {
  if (!width || !height) return "square";
  const ratio = width / height;
  if (ratio < ASPECT_RATIO.tall) return "tall";
  if (ratio > ASPECT_RATIO.square) return "wide";
  return "square";
}
function getDeviceType(width, isMobileUserAgent) {
  if (width < BREAKPOINTS.mobile) {
    return width < BREAKPOINTS.smallMobile ? "smallMobile" : "mobile";
  }
  if (width < BREAKPOINTS.tablet) return "mobile";
  if (width < BREAKPOINTS.laptop) return "tablet";
  if (width < BREAKPOINTS.desktop) return "desktop";
  return "largeDesktop";
}
function getLayoutCategory(count) {
  if (count === 1) return "singleItem";
  if (count === 2) return "twoItems";
  if (count <= 8) return "fewItems";
  if (count <= 16) return "mediumItems";
  if (count > 16) return "manyItems";
  return "manyItems";
}
const DEFAULT_COLUMNS = {
  singleItem: 1,
  twoItems: { vertical: 1, horizontal: 2 },
  fewItems: 4,
  mediumItems: 4,
  manyItems: 4
};
const LAYOUT_RULES = [
  // --- Rules for Unfolded Foldable Devices ---
  // (Keep the workaround for foldableType)
  {
    description: "Unfolded Foldable - Landscape, Few Items (<=8)",
    columns: 2,
    when: {
      maxCount: 8,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === false
    }
  },
  {
    description: "Two items on foldable in portrait mode = 1 column",
    columns: 1,
    when: {
      count: 2,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === true
    }
  },
  {
    description: "Unfolded Foldable - Portrait, Few Items (<=8)",
    columns: 2,
    when: {
      minCount: 3,
      maxCount: 8,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === true
    }
  },
  {
    description: "Unfolded Foldable - Landscape, Medium Items (9-16)",
    columns: 4,
    when: {
      minCount: 9,
      maxCount: 16,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === false
    }
  },
  {
    description: "Unfolded Foldable - Portrait, Medium Items (9-16)",
    columns: 4,
    when: {
      minCount: 9,
      maxCount: 16,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === true
    }
  },
  {
    description: "Unfolded Foldable - Landscape, Many Items (17+)",
    columns: 4,
    when: {
      minCount: 17,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === false
    }
  },
  {
    description: "Unfolded Foldable - Portrait, Many Items (17+)",
    columns: 4,
    when: {
      minCount: 17,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true && params.isPortraitMode === true
    }
  },
  {
    description: "Folded Foldable - Use Standard Mobile Layout",
    columns: 4,
    when: {
      minCount: 3,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === false
    }
  },
  // --- Standard Layout Rules (Simplified Aspects) ---
  { description: "1 item = 1 column", columns: 1, when: { count: 1 } },
  {
    description: "Two items, wide/square landscape = 2 columns",
    columns: 2,
    when: { count: 2, aspects: ["wide", "square"], orientation: "landscape" }
    // Removed 'widish'
  },
  {
    description: "Two items, tall/square portrait = 1 column",
    columns: 1,
    when: { count: 2, aspects: ["tall", "square"], orientation: "portrait" }
  },
  {
    description: "Few items (3-8) on mobile = 4 columns",
    columns: 4,
    when: { minCount: 3, maxCount: 8, device: "mobile" }
  },
  {
    description: "Medium items (9-16) on mobile = 4 columns",
    columns: 4,
    when: { minCount: 9, maxCount: 16, device: "mobile" }
  },
  {
    description: "Small window width forces 4 columns",
    columns: 4,
    when: {
      minCount: 17,
      device: "desktop",
      aspect: "square",
      extraCheck: (w) => w <= 700
      // Enforce 4 columns for small window widths
    }
  },
  {
    description: "Many items (17+) on mobile, tall = 4 columns",
    columns: 4,
    when: { minCount: 17, device: "mobile", aspect: "tall" }
  },
  {
    description: "Many items (17+) on mobile, square = 4 columns",
    columns: 4,
    when: { minCount: 17, device: "mobile", aspect: "square" }
  },
  {
    description: "Many items (17+) on mobile, wide = 6 columns",
    columns: 4,
    when: { minCount: 17, device: "mobile", aspect: "wide" }
  },
  {
    description: "Few/Medium items (3-16) on desktop, tall = 2 columns",
    columns: 4,
    when: { minCount: 3, maxCount: 16, device: "desktop", aspect: "tall" }
  },
  {
    description: "Few/Medium items (3-16) on desktop, square = 4 columns",
    columns: 4,
    when: { minCount: 3, maxCount: 16, device: "desktop", aspect: "square" }
  },
  {
    description: "Few/Medium items (3-16) on desktop, wide = 4 columns",
    columns: 4,
    when: { minCount: 3, maxCount: 16, device: "desktop", aspect: "wide" }
  },
  {
    description: "Many items (17+) on desktop, tall = 4 columns",
    columns: 4,
    when: { minCount: 17, device: "desktop", aspect: "tall" }
  },
  {
    description: "Many items (17+) on desktop, square = 6 columns",
    columns: 8,
    when: { minCount: 17, device: "desktop", aspect: "square" }
  },
  {
    description: "Many items (17+) on desktop, wide = 8 columns",
    columns: 8,
    when: { minCount: 17, device: "desktop", aspect: "wide" }
  },
  {
    description: "Very wide desktop gets +1 column",
    columns: "+1",
    maxColumns: 8,
    when: {
      device: "desktop",
      orientation: "landscape",
      extraCheck: (w) => w > 1600
    }
  }
];
const GRID_GAP_OVERRIDES = [
  {
    description: "Unfolded Foldable with many items = smaller 6px gap",
    gap: "6px",
    when: {
      minCount: 12,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true
    }
  },
  {
    description: "Unfolded Foldable with few items = 8px gap",
    gap: "8px",
    when: {
      maxCount: 11,
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true
    }
  },
  {
    description: "Wide desktop screens = 12px minimum gap",
    gap: "12px",
    when: {
      aspect: "wide",
      extraCheck: (w, h, params) => w > 1400 && params?.device === "desktop"
    }
  },
  {
    description: "Example: 16 items in wide landscape = 10px gap",
    gap: "10px",
    when: { count: 16, aspect: "wide", orientation: "landscape" }
  },
  {
    description: "Few/Medium items (3-16) on desktop, square aspect = 16px gap",
    gap: "16px",
    when: {
      minCount: 3,
      maxCount: 16,
      aspect: "square",
      extraCheck: (w, h, params) => params?.foldableInfo?.isFoldable !== true && // Not a foldable device
      params?.device === "desktop"
      // Desktop only
    }
  }
];
const DEBUG_MODE = typeof window !== "undefined" && window.location.search.includes("debug=foldable");
const FOLDABLE_DEVICE_SPECS = {
  zfold3: {
    models: ["SM-F926"],
    foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
    unfoldedDimensions: { width: { min: 700, max: 800 }, height: { min: 800, max: 900 } }
  },
  zfold4: {
    models: ["SM-F936"],
    foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
    unfoldedDimensions: { width: { min: 700, max: 800 }, height: { min: 800, max: 900 } }
  },
  zfold5: {
    models: ["SM-F946"],
    foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
    unfoldedDimensions: { width: { min: 700, max: 820 }, height: { min: 800, max: 920 } }
  },
  zfold6: {
    models: ["SM-F956"],
    // Example model, update if needed
    foldedDimensions: { width: { min: 350, max: 410 }, height: { min: 800, max: 950 } },
    // Estimated
    unfoldedDimensions: { width: { min: 800, max: 850 }, height: { min: 680, max: 750 } }
    // Based on previous user log
  }
  // Add other known foldable specs here (e.g., Pixel Fold)
};
function detectFoldableDevice() {
  const manualOverride = checkManualOverride();
  if (manualOverride) {
    if (DEBUG_MODE) console.log("Foldable Detect: Using Manual Override", manualOverride);
    return manualOverride;
  }
  let finalResult = {
    isFoldable: false,
    isUnfolded: false,
    foldableType: "unknown",
    confidence: 0,
    detectionMethod: "none"
  };
  if (typeof window === "undefined" || typeof navigator === "undefined") {
    console.warn("Foldable Detect: Cannot run outside browser environment.");
    return finalResult;
  }
  const ua = navigator.userAgent;
  const windowW = window.innerWidth;
  const windowH = window.innerHeight;
  const pixelRatio = window.devicePixelRatio;
  const aspectRatio = windowW / windowH;
  if (DEBUG_MODE) {
    console.log("Foldable Detect: UA:", ua);
    console.log("Foldable Detect: Window WxH:", windowW, "x", windowH);
    console.log("Foldable Detect: DPR:", pixelRatio);
    console.log("Foldable Detect: Aspect Ratio:", aspectRatio.toFixed(3));
  }
  let specMatchFound = checkAgainstDeviceSpecs(ua, windowW, windowH, finalResult);
  if (specMatchFound) {
    if (DEBUG_MODE) console.log("Foldable Detect: Result from Spec Match", finalResult);
    saveDetectionResult(finalResult);
    return finalResult;
  }
  const isScreenSpanning = window.matchMedia("(screen-spanning: single-fold-vertical)").matches || window.matchMedia("(screen-spanning: single-fold-horizontal)").matches;
  let segmentCount = 0;
  try {
    if ("getWindowSegments" in navigator && typeof navigator.getWindowSegments === "function") {
      segmentCount = navigator.getWindowSegments().length;
    }
  } catch (e) {
    if (DEBUG_MODE) console.warn("Error accessing getWindowSegments", e);
  }
  let viewportSegments;
  try {
    if (window.visualViewport && "segments" in window.visualViewport) {
      viewportSegments = window.visualViewport.segments;
    }
  } catch (e) {
    if (DEBUG_MODE) console.warn("Error accessing visualViewport.segments", e);
  }
  const hasSegments = segmentCount > 1 || viewportSegments && viewportSegments.length > 1;
  if (isScreenSpanning || hasSegments) {
    if (DEBUG_MODE) console.log("Foldable Detect: Detected via Spanning/Segments API");
    finalResult.isFoldable = true;
    finalResult.confidence = 0.8;
    finalResult.detectionMethod = isScreenSpanning ? "mediaQuery" : segmentCount > 1 ? "getWindowSegments" : "visualViewport";
    finalResult.isUnfolded = aspectRatio > 0.8 && aspectRatio < 1.3;
    finalResult.foldableType = /galaxy z/i.test(ua) ? "zfold" : "other";
    if (DEBUG_MODE) console.log("Foldable Detect: Result from API Match", finalResult);
    saveDetectionResult(finalResult);
    return finalResult;
  }
  const isLikelyDesktopUA = /Windows NT|Macintosh|Linux x86_64/i.test(ua) && !/Android|iPhone|iPad|iPod|Mobile/i.test(ua);
  if (isLikelyDesktopUA) {
    if (DEBUG_MODE) console.log("Foldable Detect: Detected standard desktop platform via UA. Not foldable.");
    return finalResult;
  }
  if (DEBUG_MODE) console.log("Foldable Detect: No API/Desktop match, trying generic dimension heuristic...");
  if (windowW > 600 && aspectRatio > 0.8 && aspectRatio < 1.3 && pixelRatio > 1.5) {
    if (DEBUG_MODE) console.log("Foldable Detect: Generic dimension heuristic PASSED (with pixelRatio check).");
    finalResult.isFoldable = true;
    finalResult.isUnfolded = true;
    finalResult.confidence = 0.5;
    finalResult.detectionMethod = "GenericDimensionsPixelRatio";
    finalResult.foldableType = /galaxy z/i.test(ua) ? "zfold" : "other";
  } else {
    if (DEBUG_MODE) console.log("Foldable Detect: Generic dimension heuristic FAILED.");
  }
  if (DEBUG_MODE && finalResult.isFoldable) {
    console.log("Foldable Detect: Result from Dimension Heuristic", finalResult);
  } else if (DEBUG_MODE && !finalResult.isFoldable) {
    console.log("Foldable Detect: Final Result - Not Foldable");
  }
  saveDetectionResult(finalResult);
  return finalResult;
}
function checkManualOverride() {
  if (typeof window === "undefined" || typeof localStorage === "undefined") return null;
  try {
    const override = localStorage.getItem("foldableDeviceOverride");
    if (override) {
      const settings = JSON.parse(override);
      if (typeof settings.isFoldable === "boolean" && typeof settings.isUnfolded === "boolean") {
        return {
          isFoldable: settings.isFoldable,
          foldableType: settings.foldableType || "unknown",
          isUnfolded: settings.isUnfolded,
          confidence: 1,
          // Max confidence for manual override
          detectionMethod: "ManualOverride"
        };
      }
    }
  } catch (e) {
    if (DEBUG_MODE) console.error("Error checking for manual override:", e);
  }
  return null;
}
function saveDetectionResult(result) {
  if (typeof window === "undefined" || typeof localStorage === "undefined") return;
  if (!result.isFoldable || result.confidence < 0.6) return;
  try {
    const dataToSave = {
      ...result,
      timestamp: Date.now(),
      width: window.innerWidth,
      // Save dimensions at time of detection
      height: window.innerHeight
    };
    localStorage.setItem("foldableDeviceState", JSON.stringify(dataToSave));
    if (DEBUG_MODE) console.log("Foldable Detect: Saved state to localStorage", dataToSave);
  } catch (e) {
    if (DEBUG_MODE) console.error("Error saving detection state:", e);
  }
}
function checkAgainstDeviceSpecs(ua, width, height, result) {
  for (const [deviceKey, specs] of Object.entries(FOLDABLE_DEVICE_SPECS)) {
    const isMatchingModel = specs.models.some((model) => ua.includes(model));
    if (isMatchingModel) {
      if (DEBUG_MODE) console.log(`Foldable Detect: Spec Match - Found model match for ${deviceKey}`);
      result.isFoldable = true;
      result.foldableType = deviceKey.startsWith("zfold") ? "zfold" : "other";
      result.confidence = 0.9;
      result.detectionMethod = "DeviceSpecMatch";
      const { min: minWUnfolded, max: maxWUnfolded } = specs.unfoldedDimensions.width;
      const { min: minHUnfolded, max: maxHUnfolded } = specs.unfoldedDimensions.height;
      const isUnfoldedMatch = width >= minWUnfolded && width <= maxWUnfolded && height >= minHUnfolded && height <= maxHUnfolded || height >= minWUnfolded && height <= maxWUnfolded && width >= minHUnfolded && width <= maxHUnfolded;
      result.isUnfolded = isUnfoldedMatch;
      if (DEBUG_MODE) console.log(`Foldable Detect: Spec Match - Unfolded state: ${result.isUnfolded}`);
      return true;
    }
  }
  if (DEBUG_MODE) console.log("Foldable Detect: Spec Match - No matching model found.");
  return false;
}
const activeLayoutRule = writable(null);
function getEnhancedDeviceType(width, isMobileUserAgent) {
  const foldableInfo = detectFoldableDevice();
  const baseDeviceType = getDeviceType(width);
  if (foldableInfo.isFoldable && foldableInfo.isUnfolded && foldableInfo.foldableType === "zfold") {
    return {
      deviceType: "tablet",
      isFoldable: true,
      foldableInfo
    };
  }
  return {
    deviceType: baseDeviceType,
    isFoldable: foldableInfo.isFoldable,
    foldableInfo
  };
}
const getResponsiveLayout = memoizeLRU(
  (count, containerHeight = 0, containerWidth = 0, isMobileDevice = false, isPortraitMode = false, foldableInfoParam) => {
    if (containerHeight <= 0 || containerWidth <= 0) {
      return {
        gridColumns: "repeat(auto-fit, minmax(100px, 1fr))",
        optionSize: isMobileDevice ? "80px" : "100px",
        gridGap: "8px",
        gridClass: "",
        aspectClass: "",
        scaleFactor: isMobileDevice ? 0.95 : 1
      };
    }
    const foldableInfo = foldableInfoParam || detectFoldableDevice();
    const { deviceType: enhancedDeviceType } = getEnhancedDeviceType(
      containerWidth
    );
    const gridConfig = calculateGridConfiguration({
      count,
      containerWidth,
      containerHeight,
      isMobileDevice,
      isPortraitMode,
      foldableInfo
    });
    const optionSize = calculateOptionSize({
      count,
      containerWidth,
      containerHeight,
      gridConfig,
      isMobileDevice,
      isPortraitMode,
      foldableInfo
    });
    let gridGap = getGridGap({
      count,
      containerWidth,
      containerHeight,
      isMobileDevice,
      isPortraitMode,
      foldableInfo
    });
    const { gridClass, aspectClass } = getGridClasses(
      count,
      containerWidth,
      containerHeight,
      isPortraitMode,
      foldableInfo
    );
    const deviceConfig = DEVICE_CONFIG[enhancedDeviceType];
    let scaleFactor = deviceConfig?.scaleFactor ?? (isMobileDevice ? 0.95 : 1);
    if (foldableInfo.isFoldable && foldableInfo.isUnfolded) {
      scaleFactor = Math.max(0.9, scaleFactor * 0.95);
    }
    return {
      gridColumns: gridConfig.template,
      optionSize,
      gridGap,
      gridClass,
      aspectClass,
      scaleFactor
    };
  },
  100,
  (count, containerHeight = 0, containerWidth = 0, isMobileDevice, isPortraitMode, foldableInfo) => {
    const roundedWidth = Math.round(containerWidth / 10) * 10;
    const roundedHeight = Math.round(containerHeight / 10) * 10;
    const foldableKey = foldableInfo?.isFoldable ? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? "unfolded" : "folded"}` : "none";
    return `${count}:${roundedHeight}:${roundedWidth}:${isMobileDevice}:${isPortraitMode}:${foldableKey}`;
  }
);
function doesRuleMatch(rule, params) {
  if (rule.when.count !== void 0 && rule.when.count !== params.count) return false;
  if (rule.when.minCount !== void 0 && params.count < rule.when.minCount) return false;
  if (rule.when.maxCount !== void 0 && params.count > rule.when.maxCount) return false;
  if (rule.when.device === "desktop" && params.isMobileDevice) return false;
  if (rule.when.device === "mobile" && !params.isMobileDevice) return false;
  if (rule.when.aspect && rule.when.aspect !== params.containerAspect) return false;
  if (rule.when.aspects && !rule.when.aspects.includes(params.containerAspect)) return false;
  if (rule.when.orientation === "portrait" && !params.isPortraitMode) return false;
  if (rule.when.orientation === "landscape" && params.isPortraitMode) return false;
  if (rule.when.extraCheck && !rule.when.extraCheck(params.containerWidth, params.containerHeight, params))
    return false;
  return true;
}
const calculateGridConfiguration = memoizeLRU(
  (params) => {
    const layoutCategory = getLayoutCategory(params.count);
    const containerAspect = getContainerAspect(params.containerWidth, params.containerHeight);
    let columns = getBaseColumnCount(layoutCategory, containerAspect, params.isPortraitMode);
    const fullParams = {
      ...params,
      containerAspect,
      layoutCategory
    };
    activeLayoutRule.set(null);
    for (const rule of LAYOUT_RULES) {
      if (doesRuleMatch(rule, fullParams)) {
        activeLayoutRule.set(rule);
        if (rule.columns === "+1") {
          columns = Math.min(rule.maxColumns || 8, columns + 1);
        } else {
          columns = parseInt(rule.columns.toString(), 10);
        }
        break;
      }
    }
    columns = Math.max(1, columns);
    if (params.foldableInfo?.isFoldable && params.foldableInfo.isUnfolded) {
      if (params.foldableInfo.foldableType === "zfold" && !params.isPortraitMode && columns > 2) {
        columns = Math.min(columns, 5);
      }
    }
    const template = `repeat(${columns}, minmax(0, 1fr))`;
    return { columns, template };
  },
  100,
  (params) => {
    const { count, containerWidth, containerHeight, isMobileDevice, isPortraitMode, foldableInfo } = params;
    const roundedWidth = Math.round(containerWidth / 10) * 10;
    const roundedHeight = Math.round(containerHeight / 10) * 10;
    const foldableKey = foldableInfo?.isFoldable ? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? "unfolded" : "folded"}` : "none";
    return `${count}:${roundedHeight}:${roundedWidth}:${isMobileDevice}:${isPortraitMode}:${foldableKey}`;
  }
);
function getGridGap(params) {
  const layoutCategory = getLayoutCategory(params.count);
  const deviceType = getDeviceType(params.containerWidth, params.isMobileDevice);
  const containerAspect = getContainerAspect(params.containerWidth, params.containerHeight);
  for (const override of GRID_GAP_OVERRIDES) {
    const fullParams = {
      ...params,
      containerAspect,
      layoutCategory
    };
    if (doesRuleMatch(override, fullParams)) {
      return override.gap;
    }
  }
  const deviceConfig = DEVICE_CONFIG[deviceType] || DEVICE_CONFIG.desktop;
  let gapSize = deviceConfig.gap + (GAP_ADJUSTMENTS[layoutCategory] || 0);
  if (params.foldableInfo?.isFoldable && params.foldableInfo.isUnfolded) {
    gapSize = Math.max(2, gapSize - 2);
  }
  return `${Math.max(6, gapSize)}px`;
}
function getGridClasses(count, containerWidth, containerHeight, isPortraitMode, foldableInfo) {
  const layoutCategory = getLayoutCategory(count);
  const containerAspect = getContainerAspect(containerWidth, containerHeight);
  let gridClass = "";
  if (layoutCategory === "singleItem") {
    gridClass = LAYOUT_TEMPLATES.singleItem.class;
  } else if (layoutCategory === "twoItems") {
    const useVerticalLayout = containerAspect === "tall" || containerAspect === "square" && isPortraitMode;
    gridClass = useVerticalLayout ? LAYOUT_TEMPLATES.twoItems.vertical.class : LAYOUT_TEMPLATES.twoItems.horizontal.class;
  } else {
    const deviceOrientation = isPortraitMode ? "portraitDevice" : "landscapeDevice";
    gridClass = LAYOUT_TEMPLATES[layoutCategory][deviceOrientation].class;
  }
  if (foldableInfo?.isFoldable) {
    gridClass += ` foldable-${foldableInfo.foldableType}`;
    gridClass += foldableInfo.isUnfolded ? " unfolded" : " folded";
  }
  const aspectClass = `${containerAspect}-aspect-container`;
  return { gridClass, aspectClass };
}
const calculateOptionSize = memoizeLRU(
  (config) => {
    const { count, containerWidth, containerHeight, gridConfig, isMobileDevice, foldableInfo } = config;
    const { columns } = gridConfig;
    if (containerWidth <= 0 || containerHeight <= 0 || columns <= 0) {
      return isMobileDevice ? "80px" : "100px";
    }
    const { deviceType } = getEnhancedDeviceType(containerWidth);
    const deviceConfig = DEVICE_CONFIG[deviceType] || DEVICE_CONFIG.desktop;
    const horizontalPadding = deviceConfig.padding.horizontal * 2;
    const verticalPadding = deviceConfig.padding.vertical * 2;
    const gapSize = deviceConfig.gap;
    const totalHorizontalGap = Math.max(0, columns - 1) * gapSize;
    const totalVerticalGap = Math.max(0, Math.ceil(count / columns) - 1) * gapSize;
    const availableWidth = containerWidth - horizontalPadding - totalHorizontalGap;
    const availableHeight = containerHeight - verticalPadding - totalVerticalGap;
    const widthPerItem = availableWidth / columns;
    const heightPerItem = availableHeight / Math.ceil(count / columns);
    let calculatedSize = Math.min(widthPerItem, heightPerItem);
    let scaleFactor = deviceConfig.scaleFactor;
    if (foldableInfo?.isFoldable && foldableInfo.isUnfolded) {
      if (foldableInfo.foldableType === "zfold") {
        scaleFactor *= 0.95;
      }
    }
    calculatedSize *= scaleFactor;
    calculatedSize = Math.max(deviceConfig.minItemSize, calculatedSize);
    calculatedSize = Math.min(deviceConfig.maxItemSize, calculatedSize);
    return `${Math.floor(calculatedSize)}px`;
  },
  100,
  (config) => {
    const { count, containerWidth, containerHeight, gridConfig, isMobileDevice, foldableInfo } = config;
    const roundedWidth = Math.round(containerWidth / 10) * 10;
    const roundedHeight = Math.round(containerHeight / 10) * 10;
    const foldableKey = foldableInfo?.isFoldable ? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? "unfolded" : "folded"}` : "none";
    return `${count}:${roundedHeight}:${roundedWidth}:${gridConfig.columns}:${isMobileDevice}:${foldableKey}`;
  }
);
function getBaseColumnCount(layoutCategory, aspect, isPortrait) {
  if (layoutCategory === "singleItem") {
    return DEFAULT_COLUMNS.singleItem;
  }
  if (layoutCategory === "twoItems") {
    const useVerticalLayout = aspect === "tall" || aspect === "square" && isPortrait;
    return useVerticalLayout ? DEFAULT_COLUMNS.twoItems.vertical : DEFAULT_COLUMNS.twoItems.horizontal;
  }
  return DEFAULT_COLUMNS[layoutCategory] || 4;
}
const LAYOUT_CONTEXT_KEY = Symbol("layout-context");
function LoadingSpinner($$payload, $$props) {
  let size = fallback($$props["size"], "medium");
  $$payload.out += `<div${attr_class("lds-ring svelte-1b53b9l", void 0, { "small": size === "small", "large": size === "large" })}><div class="svelte-1b53b9l"></div> <div class="svelte-1b53b9l"></div> <div class="svelte-1b53b9l"></div> <div class="svelte-1b53b9l"></div></div>`;
  bind_props($$props, { size });
}
function LoadingMessage($$payload) {
  $$payload.out += `<div class="message-container loading svelte-lq53w9"><div class="pulse-container svelte-lq53w9">`;
  LoadingSpinner($$payload, {});
  $$payload.out += `<!----></div> <p class="svelte-lq53w9">Loading options...</p></div>`;
}
function createPersistentObjectState(key, initialValue, options = {}) {
  options.debounceMs || 100;
  options.persistFields;
  options.validateData || (() => true);
  let loadedValue = { ...initialValue };
  let stateObj = { ...loadedValue };
  const proxy = new Proxy(stateObj, {
    get(target, prop) {
      return target[prop];
    },
    set(target, prop, value) {
      target[prop] = value;
      return true;
    }
  });
  return proxy;
}
const initialState$2 = {
  sequence: [],
  options: [],
  selectedPictograph: null,
  sortMethod: "type",
  isLoading: false,
  error: null,
  lastSelectedTab: { type: "all" },
  selectedTab: "all"
};
function createOptionPickerContainer() {
  const persistentUIState = createPersistentObjectState("optionPickerUIState", {
    sortMethod: initialState$2.sortMethod,
    lastSelectedTab: initialState$2.lastSelectedTab
  });
  return createContainer(
    // Initialize with both initial state and persisted UI state
    {
      ...initialState$2,
      sortMethod: persistentUIState.sortMethod,
      lastSelectedTab: persistentUIState.lastSelectedTab
    },
    (state, update) => {
      const persistUIState = () => {
        persistentUIState.sortMethod = state.sortMethod;
        persistentUIState.lastSelectedTab = state.lastSelectedTab;
      };
      return {
        loadOptions: (sequence) => {
          if (!sequence || sequence.length === 0) {
            console.warn("Attempted to load options with empty sequence");
            update((state2) => {
              state2.options = [];
              state2.isLoading = false;
              state2.error = null;
            });
            return;
          }
          update((state2) => {
            state2.sequence = sequence;
            state2.isLoading = true;
            state2.error = null;
          });
          try {
            const nextOptions = getNextOptions(sequence);
            if (!nextOptions || nextOptions.length === 0) {
              console.warn("No options available for the current sequence");
            }
            update((state2) => {
              state2.options = nextOptions || [];
              state2.isLoading = false;
            });
          } catch (error) {
            console.error("Error loading options:", error);
            update((state2) => {
              state2.isLoading = false;
              state2.error = error instanceof Error ? error.message : "Unknown error loading options";
              state2.options = [];
            });
          }
        },
        setSortMethod: (method) => {
          update((state2) => {
            state2.sortMethod = method;
          });
          persistUIState();
        },
        setReversalFilter: (filter) => {
          update((state2) => {
            state2.reversalFilter = filter;
          });
          persistUIState();
        },
        setLastSelectedTabForSort: (sortMethod, tabKey) => {
          if (state.lastSelectedTab[sortMethod] === tabKey) {
            return;
          }
          update((state2) => {
            state2.lastSelectedTab = { ...state2.lastSelectedTab, [sortMethod]: tabKey };
          });
          persistUIState();
        },
        setSelectedTab: (tab) => {
          update((state2) => {
            state2.selectedTab = tab;
          });
        },
        selectOption: (option) => {
          update((state2) => {
            state2.selectedPictograph = option;
          });
          const beatData = {
            id: crypto.randomUUID(),
            number: sequenceSelectors.beatCount() + 1,
            redPropData: option.redPropData,
            bluePropData: option.bluePropData,
            redMotionData: option.redMotionData,
            blueMotionData: option.blueMotionData,
            metadata: {
              letter: option.letter,
              startPos: option.startPos,
              endPos: option.endPos
            }
          };
          sequenceActions.addBeat(beatData);
        },
        reset: () => {
          update((state2) => {
            state2.options = [];
            state2.sequence = [];
            state2.selectedPictograph = null;
            state2.isLoading = false;
            state2.error = null;
          });
        }
      };
    }
  );
}
const optionPickerContainer = createOptionPickerContainer();
const filteredOptions = createDerived(() => {
  const options = [...optionPickerContainer.state.options];
  options.sort(getSorter(optionPickerContainer.state.sortMethod, optionPickerContainer.state.sequence));
  return options;
});
const groupedOptions = createDerived(() => {
  const groups = {};
  const options = filteredOptions.value;
  options.forEach((option) => {
    const groupKey = determineGroupKey(option, optionPickerContainer.state.sortMethod, optionPickerContainer.state.sequence);
    if (!groups[groupKey]) groups[groupKey] = [];
    groups[groupKey].push(option);
  });
  const sortedKeys = getSortedGroupKeys(Object.keys(groups), optionPickerContainer.state.sortMethod);
  const sortedGroups = {};
  sortedKeys.forEach((key) => {
    if (groups[key]) {
      sortedGroups[key] = groups[key];
    }
  });
  return sortedGroups;
});
createDerived(() => {
  const selectedTab = optionPickerContainer.state.selectedTab;
  if (selectedTab === "all") {
    return filteredOptions.value;
  }
  return selectedTab && groupedOptions.value[selectedTab] || [];
});
createDerived(() => {
  return Object.keys(groupedOptions.value);
});
function OptionDisplayArea($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  $$payload.out += `<div class="display-wrapper svelte-1cy4f5i"><!---->`;
  {
    {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="absolute-content svelte-1cy4f5i">`;
      LoadingMessage($$payload);
      $$payload.out += `<!----></div>`;
    }
    $$payload.out += `<!--]-->`;
  }
  $$payload.out += `<!----></div>`;
  pop();
}
class SequenceDataService {
  sequences = /* @__PURE__ */ new Map();
  currentSequence = null;
  idCounter = 0;
  /**
   * Create a new empty sequence
   */
  createNewSequence(name) {
    const sequence = {
      id: `seq_${this.idCounter++}`,
      name,
      beats: [],
      length: 16,
      createdAt: /* @__PURE__ */ new Date(),
      lastModified: /* @__PURE__ */ new Date(),
      metadata: {
        author: "user",
        level: 1,
        propType: "staff",
        gridMode: "diamond",
        tags: []
      }
    };
    this.sequences.set(sequence.id, sequence);
    return sequence;
  }
  /**
   * Get all sequences
   */
  getAllSequences() {
    return Array.from(this.sequences.values());
  }
  /**
   * Get sequence by ID
   */
  getSequenceById(id) {
    return this.sequences.get(id) || null;
  }
  /**
   * Save sequence
   */
  saveSequence(sequence) {
    try {
      sequence.lastModified = /* @__PURE__ */ new Date();
      this.sequences.set(sequence.id, sequence);
      return true;
    } catch (error) {
      console.error("Error saving sequence:", error);
      return false;
    }
  }
  /**
   * Delete sequence
   */
  deleteSequence(id) {
    return this.sequences.delete(id);
  }
  /**
   * Get current sequence
   */
  getCurrentSequence() {
    return this.currentSequence;
  }
  /**
   * Set current sequence
   */
  setCurrentSequence(sequence) {
    this.currentSequence = sequence;
  }
  /**
   * Add beat to sequence
   */
  addBeatToSequence(sequenceId, pictographData) {
    const sequence = this.sequences.get(sequenceId);
    if (!sequence) return null;
    const beat = {
      id: `beat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      number: sequence.beats.length + 1,
      pictographData,
      metadata: {
        letter: pictographData.letter || void 0,
        startPos: pictographData.startPos?.toString() || void 0,
        endPos: pictographData.endPos?.toString() || void 0,
        timing: pictographData.timing || void 0,
        direction: pictographData.direction || void 0
      }
    };
    sequence.beats.push(beat);
    sequence.lastModified = /* @__PURE__ */ new Date();
    return beat;
  }
  /**
   * Remove beat from sequence
   */
  removeBeatFromSequence(sequenceId, beatId) {
    const sequence = this.sequences.get(sequenceId);
    if (!sequence) return false;
    const beatIndex = sequence.beats.findIndex((beat) => beat.id === beatId);
    if (beatIndex === -1) return false;
    sequence.beats.splice(beatIndex, 1);
    sequence.beats.forEach((beat, index) => {
      beat.number = index + 1;
    });
    sequence.lastModified = /* @__PURE__ */ new Date();
    return true;
  }
  /**
   * Update beat in sequence
   */
  updateBeatInSequence(sequenceId, beatId, pictographData) {
    const sequence = this.sequences.get(sequenceId);
    if (!sequence) return false;
    const beat = sequence.beats.find((b) => b.id === beatId);
    if (!beat) return false;
    beat.pictographData = pictographData;
    beat.metadata = {
      letter: pictographData.letter || void 0,
      startPos: pictographData.startPos?.toString() || void 0,
      endPos: pictographData.endPos?.toString() || void 0,
      timing: pictographData.timing || void 0,
      direction: pictographData.direction || void 0
    };
    sequence.lastModified = /* @__PURE__ */ new Date();
    return true;
  }
  /**
   * Get beats from sequence
   */
  getBeatsFromSequence(sequenceId) {
    const sequence = this.sequences.get(sequenceId);
    return sequence ? sequence.beats : [];
  }
  /**
   * Clear all sequences (for testing)
   */
  clearAllSequences() {
    this.sequences.clear();
    this.currentSequence = null;
    this.idCounter = 0;
  }
  /**
   * Load sequences from storage (placeholder for future implementation)
   */
  async loadSequencesFromStorage() {
    try {
      const stored = localStorage.getItem("tka_sequences");
      if (stored) {
        const sequences = JSON.parse(stored);
        sequences.forEach((seq) => {
          seq.createdAt = new Date(seq.createdAt);
          seq.lastModified = new Date(seq.lastModified);
          this.sequences.set(seq.id, seq);
        });
        return sequences;
      }
    } catch (error) {
      console.error("Error loading sequences from storage:", error);
    }
    return [];
  }
  /**
   * Save sequences to storage (placeholder for future implementation)
   */
  async saveSequencesToStorage() {
    try {
      const sequences = Array.from(this.sequences.values());
      localStorage.setItem("tka_sequences", JSON.stringify(sequences));
      return true;
    } catch (error) {
      console.error("Error saving sequences to storage:", error);
      return false;
    }
  }
  /**
   * Convert sequence to legacy format (for compatibility)
   */
  convertToLegacyFormat(sequence) {
    return sequence.beats.map((beat) => ({
      letter: beat.metadata?.letter || beat.pictographData.letter,
      start_pos: beat.metadata?.startPos || beat.pictographData.startPos,
      end_pos: beat.metadata?.endPos || beat.pictographData.endPos,
      timing: beat.metadata?.timing || beat.pictographData.timing,
      direction: beat.metadata?.direction || beat.pictographData.direction,
      red_attributes: beat.pictographData.redMotionData,
      blue_attributes: beat.pictographData.blueMotionData,
      grid_mode: beat.pictographData.gridMode
    }));
  }
}
const sequenceDataService = new SequenceDataService();
const transitionLoadingStore = writable(false);
const transitionLoading = {
  /**
   * Start the loading state
   */
  start: () => {
    transitionLoadingStore.set(true);
  },
  /**
   * End the loading state
   */
  end: () => {
    transitionLoadingStore.set(false);
  },
  /**
   * Toggle the loading state
   */
  toggle: () => {
    transitionLoadingStore.update((state) => !state);
  }
};
const viewOptions = [
  {
    value: "all",
    label: "All",
    icon: "✨",
    isSortMethod: false,
    description: "Show all valid options"
  },
  {
    value: "type",
    label: "Type",
    icon: "📁",
    isSortMethod: true,
    description: "Group options by type"
  },
  {
    value: "endPosition",
    label: "End",
    icon: "🏁",
    isSortMethod: true,
    description: "Group by ending position"
  },
  {
    value: "reversals",
    label: "Reversals",
    icon: "🔄",
    isSortMethod: true,
    description: "Group by reversals"
  }
];
function ViewButton($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let isCompact = false;
  $$payload.out += `<button${attr_class("view-button svelte-1xtv5wi", void 0, { "compact": isCompact })} aria-label="Change view mode"${attr("aria-expanded", props.isOpen)} aria-haspopup="listbox"${attr("title", props.selectedViewOption.description)}><span class="view-icon svelte-1xtv5wi" aria-hidden="true">${escape_html(props.selectedViewOption.icon)}</span> `;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<span class="view-label svelte-1xtv5wi">${escape_html(props.selectedViewOption.label)}</span> <span class="dropdown-arrow svelte-1xtv5wi" aria-hidden="true">${escape_html(props.isOpen ? "▲" : "▼")}</span>`;
  }
  $$payload.out += `<!--]--></button>`;
  pop();
}
function ViewDropdown($$payload, $$props) {
  push();
  let isOpen = $$props["isOpen"];
  let selectedViewOption = $$props["selectedViewOption"];
  let viewOptions2 = $$props["viewOptions"];
  let onSelect = $$props["onSelect"];
  let onKeydown = $$props["onKeydown"];
  if (isOpen) {
    $$payload.out += "<!--[-->";
    const each_array = ensure_array_like(viewOptions2);
    $$payload.out += `<div class="dropdown svelte-1x8dbl3" role="listbox" aria-label="View options" tabindex="-1"><!--[-->`;
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let option = each_array[$$index];
      $$payload.out += `<button${attr_class("dropdown-item svelte-1x8dbl3", void 0, { "selected": selectedViewOption.value === option.value })} role="option"${attr("aria-selected", selectedViewOption.value === option.value)}${attr("title", option.description)}><span class="option-icon svelte-1x8dbl3" aria-hidden="true">${escape_html(option.icon)}</span> <span class="option-text svelte-1x8dbl3">${escape_html(option.label)}</span> `;
      if (option.description) {
        $$payload.out += "<!--[-->";
        $$payload.out += `<span class="option-description svelte-1x8dbl3">${escape_html(option.description)}</span>`;
      } else {
        $$payload.out += "<!--[!-->";
      }
      $$payload.out += `<!--]--></button>`;
    }
    $$payload.out += `<!--]--></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { isOpen, selectedViewOption, viewOptions: viewOptions2, onSelect, onKeydown });
  pop();
}
function ViewControl($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let isOpen = false;
  let selectedViewOption = viewOptions.find((opt) => opt.value === optionPickerContainer.state.sortMethod) || viewOptions.find((opt) => opt.value === "all") || viewOptions[0];
  let buttonElement = null;
  let isCompact = false;
  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
    document.removeEventListener("update-view-control", () => {
    });
  });
  function toggleDropdown() {
    isOpen = !isOpen;
    if (isOpen && "vibrate" in window.navigator) {
      try {
        window.navigator.vibrate(50);
      } catch (e) {
      }
    }
  }
  function closeDropdown() {
    isOpen = false;
  }
  function handleClickOutside(event) {
    if (isOpen && buttonElement && !buttonElement.contains(event.target)) {
      closeDropdown();
    }
  }
  function handleViewSelect(option) {
    selectedViewOption = option;
    console.log("Selected view option:", option.label, option.value);
    if ("vibrate" in window.navigator) {
      try {
        window.navigator.vibrate(50);
      } catch (e) {
      }
    }
    const detail = option.value === "all" ? { mode: "all" } : { mode: "group", method: option.value };
    if (option.value === "all") {
      optionPickerContainer.setSelectedTab("all");
      optionPickerContainer.setLastSelectedTabForSort(optionPickerContainer.state.sortMethod, "all");
      const allOption = viewOptions.find((opt) => opt.value === "all");
      if (allOption) {
        selectedViewOption = allOption;
      }
    } else {
      optionPickerContainer.setSortMethod(option.value);
      const matchingOption = viewOptions.find((opt) => opt.value === option.value);
      if (matchingOption) {
        selectedViewOption = matchingOption;
      }
    }
    const customEvent = new CustomEvent("viewChange", { detail, bubbles: true, composed: true });
    if (buttonElement) {
      console.log("Dispatching viewChange event with detail:", detail);
      buttonElement.dispatchEvent(customEvent);
    } else {
      console.warn("Button element not available, using document for event dispatch");
      document.dispatchEvent(customEvent);
    }
    closeDropdown();
  }
  function handleKeydown(event) {
    if (!isOpen) return;
    const currentIndex = viewOptions.findIndex((opt) => opt.value === selectedViewOption.value);
    let newIndex = currentIndex;
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        newIndex = (currentIndex + 1) % viewOptions.length;
        break;
      case "ArrowUp":
        event.preventDefault();
        newIndex = (currentIndex - 1 + viewOptions.length) % viewOptions.length;
        break;
      case "Home":
        event.preventDefault();
        newIndex = 0;
        break;
      case "End":
        event.preventDefault();
        newIndex = viewOptions.length - 1;
        break;
      case "Enter":
      case " ":
        event.preventDefault();
        handleViewSelect(selectedViewOption);
        return;
      case "Escape":
        event.preventDefault();
        closeDropdown();
        return;
      case "Tab":
        closeDropdown();
        return;
      default:
        const key = event.key.toLowerCase();
        const matchingOption = viewOptions.find((opt) => opt.label.toLowerCase().startsWith(key));
        if (matchingOption) {
          event.preventDefault();
          newIndex = viewOptions.findIndex((opt) => opt.value === matchingOption.value);
        }
        break;
    }
    if (newIndex !== currentIndex) {
      selectedViewOption = viewOptions[newIndex];
    }
  }
  $$payload.out += `<div${attr_class("view-control svelte-gnzt19", void 0, { "compact": isCompact })}>`;
  ViewButton($$payload, {
    selectedViewOption,
    isOpen,
    onClick: toggleDropdown,
    compact: isCompact,
    onButtonRef: (element2) => buttonElement = element2
  });
  $$payload.out += `<!----> `;
  ViewDropdown($$payload, {
    isOpen,
    selectedViewOption,
    viewOptions,
    onSelect: handleViewSelect,
    onKeydown: handleKeydown
  });
  $$payload.out += `<!----></div>`;
  pop();
}
const tabLabelMappings = {
  long: {
    Type1: "Type 1",
    Type2: "Type 2",
    Type3: "Type 3",
    Type4: "Type 4",
    Type5: "Type 5",
    Type6: "Type 6",
    "Unknown Type": "Unknown",
    alpha: "Alpha",
    beta: "Beta",
    gamma: "Gamma",
    Continuous: "Continuous",
    "One Reversal": "One Reversal",
    "Two Reversals": "Two Reversals"
  },
  short: {
    Type1: "1",
    Type2: "2",
    Type3: "3",
    Type4: "4",
    Type5: "5",
    Type6: "6",
    "Unknown Type": "?",
    alpha: "α",
    beta: "β",
    gamma: "Γ",
    Continuous: "Cont.",
    "One Reversal": "1 Rev.",
    "Two Reversals": "2 Rev."
  }
};
function formatTabName(key) {
  if (!key) return "";
  return tabLabelMappings.long[key] || key.replace(/([A-Z])/g, " $1").trim().replace(/^\w/, (c) => c.toUpperCase());
}
function formatShortTabName(key) {
  if (!key) return "";
  return tabLabelMappings.short[key] || formatTabName(key);
}
function TabButton($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let isHovered = false;
  $$payload.out += `<button${attr_class("tab svelte-14n1y52", void 0, {
    "active": props.isActive,
    "first-tab": props.isFirstTab,
    "last-tab": props.isLastTab,
    "hovered": isHovered
  })} role="tab"${attr("aria-selected", props.isActive)}${attr("aria-controls", `options-panel-${props.categoryKey}`)}${attr("id", `tab-${stringify(props.categoryKey)}`)}${attr("title", formatTabName(props.categoryKey))}${attr_style(`--tab-flex-basis: ${stringify(props.tabFlexBasis)}`)}><div class="tab-content svelte-14n1y52"><span class="tab-text svelte-14n1y52">${escape_html(props.useShortLabels ? formatShortTabName(props.categoryKey) : formatTabName(props.categoryKey))}</span> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div></button>`;
  pop();
}
function ScrollIndicator($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  if (props.show) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="scroll-indicator svelte-1o2jnpw"></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function TabsContainer($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let scrollPosition = 0;
  let maxScroll = 0;
  let showTooltip = false;
  setTimeout(
    () => {
      showTooltip = true;
      setTimeout(
        () => {
          showTooltip = false;
        },
        5e3
      );
    },
    1e3
  );
  if (props.categoryKeys && props.categoryKeys.length > 0) {
    $$payload.out += "<!--[-->";
    const each_array = ensure_array_like(props.categoryKeys);
    $$payload.out += `<div class="tabs-wrapper svelte-1rym7x5">`;
    if (props.isScrollable && scrollPosition > 20) ;
    else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--> <div${attr_class("tabs svelte-1rym7x5", void 0, { "scrollable": props.isScrollable })} role="tablist"><div class="tabs-inner-container svelte-1rym7x5"><!--[-->`;
    for (let index = 0, $$length = each_array.length; index < $$length; index++) {
      let categoryKey = each_array[index];
      TabButton($$payload, {
        categoryKey,
        isActive: props.selectedTab === categoryKey,
        isFirstTab: index === 0,
        isLastTab: index === props.categoryKeys.length - 1,
        useShortLabels: props.useShortLabels,
        tabFlexBasis: `${100 / props.categoryKeys.length}%`,
        index,
        totalTabs: props.categoryKeys.length
      });
    }
    $$payload.out += `<!--]--></div> `;
    if (showTooltip && props.categoryKeys.length > 1) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="tabs-tooltip svelte-1rym7x5"><div class="tooltip-content svelte-1rym7x5">Explore ${escape_html(props.categoryKeys.length)} categories</div></div>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div> `;
    if (props.isScrollable && scrollPosition < maxScroll - 20) ;
    else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div> `;
    if (props.showScrollIndicator) {
      $$payload.out += "<!--[-->";
      ScrollIndicator($$payload, { show: props.isScrollable });
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]-->`;
  } else {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<div class="tabs-placeholder svelte-1rym7x5"><span class="no-categories-message svelte-1rym7x5">No sub-categories</span></div>`;
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function useResponsiveLayout(layoutContext) {
  const isMobileDevice = writable(false);
  const useShortLabels = writable(false);
  const tabsContainerRef = writable(null);
  const isScrollable = writable(false);
  const compactMode = writable(false);
  const showScrollIndicator = writable(false);
  let currentTabsContainerRef = null;
  tabsContainerRef.subscribe((value) => {
    currentTabsContainerRef = value;
  });
  function checkTabsOverflow() {
    if (!currentTabsContainerRef) return;
    const { scrollWidth, clientWidth } = currentTabsContainerRef;
    const newIsScrollable = scrollWidth > clientWidth;
    isScrollable.set(newIsScrollable);
    const isNearlyOverflowing = scrollWidth > clientWidth - 20;
    if ((newIsScrollable || isNearlyOverflowing) && !get(compactMode)) {
      compactMode.set(true);
      setTimeout(() => {
        if (currentTabsContainerRef) {
          const { scrollWidth: scrollWidth2, clientWidth: clientWidth2 } = currentTabsContainerRef;
          isScrollable.set(scrollWidth2 > clientWidth2);
          showScrollIndicator.set(get(isScrollable));
        }
      }, 50);
    }
    showScrollIndicator.set(newIsScrollable);
  }
  function handleScroll() {
    if (!currentTabsContainerRef) return;
    const { scrollLeft, scrollWidth, clientWidth } = currentTabsContainerRef;
    showScrollIndicator.set(scrollLeft + clientWidth < scrollWidth - 10);
  }
  return {
    isMobileDevice,
    useShortLabels,
    tabsContainerRef,
    isScrollable,
    compactMode,
    showScrollIndicator,
    handleScroll,
    checkTabsOverflow
  };
}
function OptionPickerHeader($$payload, $$props) {
  push();
  var $$store_subs;
  const { $$slots, $$events, ...props } = $$props;
  getContext(LAYOUT_CONTEXT_KEY);
  const {
    isMobileDevice,
    useShortLabels,
    tabsContainerRef,
    isScrollable,
    compactMode,
    showScrollIndicator,
    handleScroll
  } = useResponsiveLayout();
  $$payload.out += `<div${attr_class("option-picker-header", void 0, {
    "mobile": store_get($$store_subs ??= {}, "$isMobileDevice", isMobileDevice)
  })} data-testid="option-picker-header"><div class="header-content">`;
  if (props.showTabs) {
    $$payload.out += "<!--[-->";
    TabsContainer($$payload, {
      selectedTab: props.selectedTab,
      categoryKeys: props.categoryKeys || [],
      isScrollable: store_get($$store_subs ??= {}, "$isScrollable", isScrollable),
      showScrollIndicator: store_get($$store_subs ??= {}, "$showScrollIndicator", showScrollIndicator),
      useShortLabels: store_get($$store_subs ??= {}, "$useShortLabels", useShortLabels),
      isMobileDevice: store_get($$store_subs ??= {}, "$isMobileDevice", isMobileDevice),
      compactMode: store_get($$store_subs ??= {}, "$compactMode", compactMode),
      tabsContainerRefStore: tabsContainerRef,
      onScroll: handleScroll
    });
  } else {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<div class="helper-message">Showing all - filter to see sections</div>`;
  }
  $$payload.out += `<!--]--> <div${attr_class("view-controls", void 0, {
    "compact": store_get($$store_subs ??= {}, "$compactMode", compactMode)
  })}>`;
  ViewControl($$payload, {
    compact: store_get($$store_subs ??= {}, "$compactMode", compactMode)
  });
  $$payload.out += `<!----></div></div></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
function OptionPicker($$payload, $$props) {
  push();
  var $$store_subs;
  let isLoading, groupedOptions2, filteredOptions2, actualCategoryKeys, optionsToDisplay, showTabs, context;
  const windowWidth = writable(typeof window !== "undefined" ? window.innerWidth : BREAKPOINTS.desktop);
  const windowHeight = writable(typeof window !== "undefined" ? window.innerHeight : 768);
  const containerWidth = writable(typeof window !== "undefined" ? Math.max(300, window.innerWidth * 0.8) : BREAKPOINTS.desktop);
  const containerHeight = writable(typeof window !== "undefined" ? Math.max(200, window.innerHeight * 0.6) : 768);
  const selectedTab = writable(null);
  const layoutContextValue = derived(
    [
      windowWidth,
      windowHeight,
      containerWidth,
      containerHeight,
      uiState,
      filteredOptionsStore,
      // Need filtered options count for layout
      groupedOptionsStore,
      // Need grouped options for layout when tab is selected
      selectedTab
    ],
    ([
      $windowWidth,
      $windowHeight,
      $containerWidth,
      $containerHeight,
      $ui,
      $filteredOptions,
      $groupedOptions,
      $selectedTab2
    ]) => {
      const { deviceType: enhancedDeviceType, foldableInfo } = getEnhancedDeviceType($containerWidth > 0 ? $containerWidth : $windowWidth);
      const isMobile = enhancedDeviceType === "smallMobile" || enhancedDeviceType === "mobile";
      const isTablet = enhancedDeviceType === "tablet";
      const isPortrait = $containerHeight > $containerWidth;
      const currentContainerAspect = getContainerAspect($containerWidth, $containerHeight);
      const optionsCount = $selectedTab2 && $selectedTab2 !== "all" && $groupedOptions && $groupedOptions[$selectedTab2] ? $groupedOptions[$selectedTab2].length : $filteredOptions.length;
      const currentLayoutConfig = getResponsiveLayout(optionsCount, $containerHeight, $containerWidth, isMobile, isPortrait, foldableInfo);
      return {
        deviceType: enhancedDeviceType,
        isMobile,
        isTablet,
        isPortrait,
        containerWidth: $containerWidth,
        containerHeight: $containerHeight,
        ht: $containerHeight,
        // Add missing 'ht' property
        containerAspect: currentContainerAspect,
        layoutConfig: currentLayoutConfig,
        foldableInfo
        // IMPORTANT: Pass the full foldable info object
      };
    }
  );
  setContext(LAYOUT_CONTEXT_KEY, layoutContextValue);
  isLoading = store_get($$store_subs ??= {}, "$uiState", uiState).isLoading;
  groupedOptions2 = store_get($$store_subs ??= {}, "$groupedOptionsStore", groupedOptionsStore);
  filteredOptions2 = store_get($$store_subs ??= {}, "$filteredOptionsStore", filteredOptionsStore);
  actualCategoryKeys = groupedOptions2 ? Object.keys(groupedOptions2) : [];
  if (!isLoading && filteredOptions2.length > 0) {
    transitionLoading.end();
  }
  optionsToDisplay = store_get($$store_subs ??= {}, "$selectedTab", selectedTab) === "all" ? filteredOptions2 : store_get($$store_subs ??= {}, "$selectedTab", selectedTab) && groupedOptions2 && groupedOptions2[store_get($$store_subs ??= {}, "$selectedTab", selectedTab)] || [];
  showTabs = store_get($$store_subs ??= {}, "$selectedTab", selectedTab) !== "all";
  context = store_get($$store_subs ??= {}, "$layoutContextValue", layoutContextValue);
  $$payload.out += `<div${attr_class("option-picker svelte-zwtppc", void 0, {
    "mobile": (
      // Force update only when explicitly showing all
      // Convert motion data from the store format
      context.isMobile
    ),
    "portrait": context.isPortrait
  })}>`;
  OptionPickerHeader($$payload, {
    selectedTab: store_get($$store_subs ??= {}, "$selectedTab", selectedTab),
    categoryKeys: actualCategoryKeys,
    showTabs
  });
  $$payload.out += `<!----> <div class="options-container svelte-zwtppc">`;
  OptionDisplayArea($$payload, {
    isLoading,
    selectedTab: store_get($$store_subs ??= {}, "$selectedTab", selectedTab),
    optionsToDisplay,
    hasCategories: actualCategoryKeys.length > 0
  });
  $$payload.out += `<!----></div></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
function OptionPickerWithDebug($$payload) {
  $$payload.out += `<div class="option-picker-container svelte-1azx46a">`;
  OptionPicker($$payload);
  $$payload.out += `<!----></div>`;
}
class StartPositionService {
  DEFAULT_START_POSITIONS = {
    diamond: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    box: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
  };
  constructor() {
    console.log("🎯 StartPositionService initialized");
  }
  async getAvailableStartPositions(propType, gridMode) {
    console.log(`📍 Getting available start positions for ${propType} in ${gridMode} mode`);
    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
      const beatData = startPositionKeys.map((key, index) => {
        const [startPos, endPos] = key.split("_");
        return {
          beat: 0,
          pictograph_data: this.createStartPositionPictograph(key, index, gridMode)
        };
      });
      console.log(`✅ Generated ${beatData.length} start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting start positions:", error);
      return [];
    }
  }
  async setStartPosition(startPosition) {
    console.log("🎯 Setting start position:", startPosition.pictograph_data?.letter);
    try {
      if (typeof window !== "undefined") {
        const serializableData = this.createSerializableStartPosition(startPosition);
        localStorage.setItem("start_position", JSON.stringify(serializableData));
      }
      console.log("✅ Start position set successfully");
    } catch (error) {
      console.error("❌ Error setting start position:", error);
      throw new Error(`Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }
  async addStartPosition(pictographData) {
    console.log("🎯 Adding start position:", pictographData?.letter);
    try {
      const beatData = {
        beat: 0,
        pictograph_data: pictographData
      };
      await this.setStartPosition(beatData);
      await this.initializeSequenceWithStartPosition(pictographData);
      console.log("✅ Start position added and sequence initialized successfully");
    } catch (error) {
      console.error("❌ Error adding start position:", error);
      throw new Error(`Failed to add start position: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }
  validateStartPosition(position) {
    const errors = [];
    if (!position.pictograph_data) {
      errors.push("Start position must have pictograph data");
    }
    if (!position.pictograph_data?.redMotionData && !position.pictograph_data?.blueMotionData) {
      errors.push("Start position must have at least one motion");
    }
    if (position.pictograph_data?.blueMotionData?.motionType !== "static") {
      errors.push("Blue motion must be static for start positions");
    }
    if (position.pictograph_data?.redMotionData?.motionType !== "static") {
      errors.push("Red motion must be static for start positions");
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }
  /**
   * Create a serializable version of start position data without circular references
   */
  createSerializableStartPosition(startPosition) {
    if (!startPosition.pictograph_data) {
      return startPosition;
    }
    const pictographData = startPosition.pictograph_data;
    const serializableData = {
      beat: startPosition.beat,
      pictograph_data: {
        letter: pictographData.letter,
        startPos: pictographData.startPos,
        endPos: pictographData.endPos,
        isStartPosition: pictographData.isStartPosition,
        // Extract only essential motion data without circular references
        redMotionData: this.extractMotionData(pictographData.redMotionData),
        blueMotionData: this.extractMotionData(pictographData.blueMotionData)
      }
    };
    return serializableData;
  }
  /**
   * Extract essential motion data without circular references
   */
  extractMotionData(motionData) {
    if (!motionData) return null;
    return {
      motionType: motionData.motionType,
      startOrientation: motionData.startOrientation,
      endOrientation: motionData.endOrientation,
      turns: motionData.turns,
      color: motionData.color
    };
  }
  async getDefaultStartPositions(gridMode) {
    console.log(`📍 Getting default start positions for ${gridMode} mode`);
    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
      const pictographData = startPositionKeys.map(
        (key, index) => this.createStartPositionPictograph(key, index, gridMode)
      );
      console.log(`✅ Generated ${pictographData.length} default start positions`);
      return pictographData;
    } catch (error) {
      console.error("❌ Error getting default start positions:", error);
      return [];
    }
  }
  createStartPositionPictograph(key, index, gridMode) {
    const [startPos, endPos] = key.split("_");
    let letter;
    if (key.includes("alpha")) letter = "α";
    else if (key.includes("beta")) letter = "β";
    else if (key.includes("gamma")) letter = "γ";
    else letter = key;
    const locations = ["n", "s", "e", "w", "ne", "se", "sw", "nw"];
    const blueLocation = locations[index % locations.length];
    const redLocation = locations[(index + 4) % locations.length];
    return {
      letter,
      startPos,
      endPos,
      timing: null,
      direction: null,
      gridMode,
      gridData: null,
      blueMotionData: {
        id: crypto.randomUUID(),
        color: "blue",
        motionType: "static",
        startLoc: blueLocation,
        endLoc: blueLocation,
        startOri: "in",
        endOri: "in",
        turns: 0,
        propRotDir: "no_rot"
      },
      redMotionData: {
        id: crypto.randomUUID(),
        color: "red",
        motionType: "static",
        startLoc: redLocation,
        endLoc: redLocation,
        startOri: "out",
        endOri: "out",
        turns: 0,
        propRotDir: "no_rot"
      },
      redPropData: null,
      bluePropData: null,
      redArrowData: null,
      blueArrowData: null,
      grid: gridMode
    };
  }
  /**
   * Initialize sequence with start position as beat 0
   */
  async initializeSequenceWithStartPosition(pictographData) {
    try {
      const sequence = sequenceDataService.createNewSequence("New Sequence");
      const startBeat = {
        id: `beat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        number: 0,
        // Start position should be beat 0
        pictographData,
        metadata: {
          letter: pictographData.letter || void 0,
          startPos: pictographData.startPos?.toString() || void 0,
          endPos: pictographData.endPos?.toString() || void 0,
          timing: pictographData.timing || void 0,
          direction: pictographData.direction || void 0
        }
      };
      sequence.beats.push(startBeat);
      sequence.lastModified = /* @__PURE__ */ new Date();
      sequenceDataService.setCurrentSequence(sequence);
      console.log("✅ Sequence initialized with start position as beat 0");
    } catch (error) {
      console.error("❌ Error initializing sequence:", error);
      throw error;
    }
  }
}
new StartPositionService();
function LoadingOverlay$1($$payload, $$props) {
  let visible = fallback($$props["visible"], false);
  let message = fallback($$props["message"], "Loading options...");
  let transitionDuration = fallback($$props["transitionDuration"], 200);
  if (visible) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="loading-overlay svelte-ovjgv1"><div class="loading-content svelte-ovjgv1">`;
    LoadingSpinner($$payload, { size: "medium" });
    $$payload.out += `<!----> <p class="loading-message svelte-ovjgv1">${escape_html(message)}</p></div></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { visible, message, transitionDuration });
}
function StartPosPicker($$payload, $$props) {
  push();
  let isTransitioning = false;
  pictographDataStore.subscribe((data) => {
    return;
  });
  $$payload.out += `<div class="start-pos-picker svelte-1dnn0rp">`;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="loading-container svelte-1dnn0rp">`;
    LoadingSpinner($$payload, { size: "large" });
    $$payload.out += `<!----> <p class="loading-text svelte-1dnn0rp">Loading Start Positions...</p></div>`;
  }
  $$payload.out += `<!--]--> `;
  LoadingOverlay$1($$payload, {
    visible: isTransitioning,
    message: "Loading options...",
    transitionDuration: 200
  });
  $$payload.out += `<!----></div>`;
  pop();
}
function TransitionWrapper($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  props.isSequenceEmpty;
  let showStartPosPicker = props.isSequenceEmpty;
  let showOptionPicker = !props.isSequenceEmpty;
  ({
    duration: props.transitionDuration
  });
  ({
    duration: props.transitionDuration * 0.8
  });
  $$payload.out += `<div class="transition-container svelte-4mxova">`;
  if (showStartPosPicker) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div${attr_class("component-wrapper start-pos-wrapper svelte-4mxova", void 0, { "active": props.isSequenceEmpty })}><!---->`;
    slot($$payload, $$props, "startPosPicker", {});
    $$payload.out += `<!----></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> `;
  if (showOptionPicker) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div${attr_class("component-wrapper option-picker-wrapper svelte-4mxova", void 0, { "active": !props.isSequenceEmpty })}><!---->`;
    slot($$payload, $$props, "optionPicker", {});
    $$payload.out += `<!----></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function RightPanel($$payload, $$props) {
  push();
  var $$store_subs;
  const transitionDuration = 400;
  $$payload.out += `<div class="right-panel svelte-16m74dh">`;
  if (store_get($$store_subs ??= {}, "$workbenchStore", workbenchStore).activeTab === "generate") {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div>`;
    ModernGenerationControls($$payload);
    $$payload.out += `<!----></div>`;
  } else {
    $$payload.out += "<!--[!-->";
    TransitionWrapper($$payload, {
      isSequenceEmpty: store_get($$store_subs ??= {}, "$isSequenceEmpty", isSequenceEmpty),
      transitionDuration,
      $$slots: {
        startPosPicker: ($$payload2) => {
          $$payload2.out += `<div slot="startPosPicker" class="full-height-wrapper svelte-16m74dh">`;
          StartPosPicker($$payload2);
          $$payload2.out += `<!----></div>`;
        },
        optionPicker: ($$payload2) => {
          $$payload2.out += `<div slot="optionPicker" class="full-height-wrapper svelte-16m74dh">`;
          OptionPickerWithDebug($$payload2);
          $$payload2.out += `<!----></div>`;
        }
      }
    });
  }
  $$payload.out += `<!--]--></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
function ToolsPanel($$payload, $$props) {
  push();
  let buttons = fallback($$props["buttons"], () => [], true);
  let activeMode = fallback($$props["activeMode"], null);
  const modeButtons = buttons.filter((b) => ["constructMode", "generateMode"].includes(b.id));
  const sharingButtons = buttons.filter((b) => ["viewFullScreen", "saveImage"].includes(b.id));
  const manipulationButtons = buttons.filter((b) => ["mirrorSequence", "swapColors", "rotateSequence"].includes(b.id));
  const dictionaryButtons = buttons.filter((b) => ["addToDictionary"].includes(b.id));
  const destructiveButtons = buttons.filter((b) => ["deleteBeat", "clearSequence"].includes(b.id));
  const orderedButtons = [
    ...modeButtons,
    ...sharingButtons,
    ...manipulationButtons,
    ...dictionaryButtons,
    ...destructiveButtons
  ];
  const each_array = ensure_array_like(orderedButtons);
  $$payload.out += `<div class="tools-panel svelte-jt32zg"><div class="tools-header svelte-jt32zg"><h2 class="svelte-jt32zg">Tools</h2> <button class="close-button svelte-jt32zg" aria-label="Close tools panel">✕</button></div> <div class="tools-content svelte-jt32zg"><div class="tools-grid svelte-jt32zg"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let button = each_array[$$index];
    $$payload.out += `<button${attr_class(`tool-button ${stringify(button.id.includes("delete") || button.id.includes("clear") ? "destructive" : "")} ${stringify(button.id === "constructMode" && activeMode === "construct" || button.id === "generateMode" && activeMode === "generate" ? "active-mode" : "")}`, "svelte-jt32zg")}${attr_style(`--button-color: ${stringify(button.color)}`)}${attr("title", button.title)}${attr("aria-label", button.title)}><i${attr_class(`fa-solid ${stringify(button.id === "saveImage" ? "fa-share-nodes" : button.icon)}`, "svelte-jt32zg")}></i> <span class="button-title svelte-jt32zg">${escape_html(button.title)}</span></button>`;
  }
  $$payload.out += `<!--]--></div></div></div>`;
  bind_props($$props, { buttons, activeMode });
  pop();
}
function SharedWorkbench($$payload, $$props) {
  push();
  var $$store_subs;
  let toolsPanelButtons = $$props["toolsPanelButtons"];
  let onToolsPanelAction = $$props["onToolsPanelAction"];
  onDestroy(() => {
  });
  $$payload.out += `<div class="shared-workbench svelte-i2el1u"><div class="sequenceWorkbenchContainer svelte-i2el1u">`;
  SequenceWidget($$payload);
  $$payload.out += `<!----></div> <div${attr_class("optionPickerContainer svelte-i2el1u", void 0, {
    "tools-panel-active": store_get($$store_subs ??= {}, "$workbenchStore", workbenchStore).toolsPanelOpen
  })}>`;
  if (store_get($$store_subs ??= {}, "$workbenchStore", workbenchStore).toolsPanelOpen) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="tools-panel-overlay svelte-i2el1u">`;
    ToolsPanel($$payload, {
      buttons: toolsPanelButtons,
      activeMode: store_get($$store_subs ??= {}, "$workbenchStore", workbenchStore).activeTab
    });
    $$payload.out += `<!----></div>`;
  } else {
    $$payload.out += "<!--[!-->";
    RightPanel($$payload);
  }
  $$payload.out += `<!--]--></div></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  bind_props($$props, { toolsPanelButtons, onToolsPanelAction });
  pop();
}
const isSequenceFullScreen = writable(false);
function openSequenceFullScreen() {
  console.log("Setting sequence overlay to open");
  isSequenceFullScreen.set(true);
}
function ConstructTab($$payload, $$props) {
  push();
  let isGenerateMode = fallback($$props["isGenerateMode"], false);
  const buttonPanelButtons = [
    {
      icon: "fa-book-medical",
      title: "Add to Dictionary",
      id: "addToDictionary",
      color: "#4361ee"
    },
    {
      icon: "fa-save",
      title: "Save Image",
      id: "saveImage",
      color: "#3a86ff"
    },
    {
      icon: "fa-expand",
      title: "View Sequence Full Screen",
      id: "viewFullScreen",
      color: "#4cc9f0"
    },
    {
      icon: "fa-arrows-left-right",
      title: "Mirror Sequence",
      id: "mirrorSequence",
      color: "#4895ef"
    },
    {
      icon: "fa-paintbrush",
      title: "Swap Colors",
      id: "swapColors",
      color: "#ff6b6b"
    },
    {
      icon: "fa-rotate",
      title: "Rotate Sequence",
      id: "rotateSequence",
      color: "#f72585"
    },
    {
      icon: "fa-trash",
      title: "Delete Beat",
      id: "deleteBeat",
      color: "#ff9e00"
    },
    {
      icon: "fa-eraser",
      title: "Clear Sequence",
      id: "clearSequence",
      color: "#ff7b00"
    }
  ];
  function handleButtonAction(id) {
    console.log(`Handling button action: ${id}`);
    switch (id) {
      case "viewFullScreen":
        openSequenceFullScreen();
        break;
      case "constructMode":
        workbenchStore.update((state) => ({ ...state, activeTab: "construct" }));
        break;
      case "generateMode":
        workbenchStore.update((state) => ({ ...state, activeTab: "generate" }));
        break;
      case "saveImage":
        console.log("Save image action triggered");
        break;
      case "addToDictionary":
        console.log("Add to dictionary action triggered");
        break;
      case "mirrorSequence":
        console.log("Mirror sequence action triggered");
        break;
      case "swapColors":
        console.log("Swap colors action triggered");
        break;
      case "rotateSequence":
        console.log("Rotate sequence action triggered");
        break;
      case "deleteBeat":
        console.log("Delete beat action triggered");
        break;
      case "clearSequence":
        console.log("Clear sequence action triggered");
        break;
      default:
        console.log(`Unhandled action: ${id}`);
        break;
    }
  }
  workbenchStore.update((state) => ({
    ...state,
    activeTab: isGenerateMode ? "generate" : "construct"
  }));
  $$payload.out += `<div class="construct-tab svelte-bj48nv">`;
  SharedWorkbench($$payload, {
    toolsPanelButtons: buttonPanelButtons,
    onToolsPanelAction: handleButtonAction
  });
  $$payload.out += `<!----></div>`;
  bind_props($$props, { isGenerateMode });
  pop();
}
function TabContent($$payload, $$props) {
  push();
  const isGenerateTab = false;
  $$payload.out += `<div class="tab-content-container svelte-16hapdj"><div class="split-view-container svelte-16hapdj">`;
  ConstructTab($$payload, { isGenerateMode: isGenerateTab });
  $$payload.out += `<!----></div></div>`;
  pop();
}
function SettingsTabs($$payload, $$props) {
  push();
  const { tabs, activeTab = "" } = $$props;
  const each_array = ensure_array_like(tabs);
  $$payload.out += `<div class="settings-tabs svelte-10bj44p"><div class="tabs-container svelte-10bj44p"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let tab = each_array[$$index];
    $$payload.out += `<button${attr_class("tab-button svelte-10bj44p", void 0, { "active": activeTab === tab.id })}${attr("aria-selected", activeTab === tab.id)} role="tab"${attr("id", `tab-${tab.id}`)}${attr("aria-controls", `panel-${tab.id}`)}><i${attr_class(`fa-solid ${tab.icon}`, "svelte-10bj44p")} aria-hidden="true"></i> <span class="tab-label svelte-10bj44p">${escape_html(tab.label)}</span></button>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  pop();
}
const initialState$1 = {
  currentUser: "User",
  // Default username
  hasCompletedSetup: false,
  lastUpdated: Date.now()
};
function createUserContainer() {
  let savedState = { ...initialState$1 };
  return createContainer(savedState, (state, update) => ({
    /**
     * Set the current username
     */
    setUsername: (username) => {
      if (!username || typeof username !== "string") {
        console.warn("Invalid username provided, using default");
        username = "User";
      }
      username = username.trim().substring(0, 50);
      if (username === "") {
        username = "User";
      }
      update((state2) => {
        state2.currentUser = username;
        state2.lastUpdated = Date.now();
      });
    },
    /**
     * Mark the first-time setup as completed
     */
    completeSetup: (username) => {
      if (username) {
        userContainer.setUsername(username);
      }
      update((state2) => {
        state2.hasCompletedSetup = true;
        state2.lastUpdated = Date.now();
      });
    },
    /**
     * Reset the user data to defaults
     */
    resetUser: () => {
      update((state2) => {
        state2.currentUser = initialState$1.currentUser;
        state2.lastUpdated = Date.now();
      });
    },
    /**
     * Check if this is the first visit
     */
    isFirstVisit: () => {
      return !state.hasCompletedSetup;
    }
  }));
}
const userContainer = createUserContainer();
const initialState = {
  isBrowserPanelOpen: true,
  browserPanelWidth: 300,
  // Default browser panel width in pixels
  scrollPosition: {
    beatGrid: 0,
    cueScroll: 0
  },
  gridSettings: {
    cellSize: 80
    // Default cell size in pixels
  },
  preferences: {
    confirmDeletions: true
    // Default to showing confirmation dialogs
  }
};
function createUIStore() {
  let savedState = initialState;
  const { subscribe, set, update } = writable(savedState);
  return {
    subscribe,
    /**
     * Toggle the browser panel open/closed state
     */
    toggleBrowserPanel: () => {
      update((state) => ({
        ...state,
        isBrowserPanelOpen: !state.isBrowserPanelOpen
      }));
    },
    /**
     * Set the browser panel open/closed state
     */
    setBrowserPanelOpen: (isOpen) => {
      update((state) => ({
        ...state,
        isBrowserPanelOpen: isOpen
      }));
    },
    /**
     * Update the scroll position for the beat grid
     */
    updateBeatGridScroll: (position) => {
      update((state) => ({
        ...state,
        scrollPosition: {
          ...state.scrollPosition,
          beatGrid: position
        }
      }));
    },
    /**
     * Update the scroll position for the cue scroll
     */
    updateCueScrollPosition: (position) => {
      update((state) => ({
        ...state,
        scrollPosition: {
          ...state.scrollPosition,
          cueScroll: position
        }
      }));
    },
    /**
     * Sync the scroll positions between beat grid and cue scroll
     */
    syncScrollPositions: (position) => {
      update((state) => ({
        ...state,
        scrollPosition: {
          beatGrid: position,
          cueScroll: position
        }
      }));
    },
    /**
     * Update the grid cell size
     */
    updateCellSize: (size) => {
      update((state) => ({
        ...state,
        gridSettings: {
          ...state.gridSettings,
          cellSize: size
        }
      }));
    },
    /**
     * Zoom in by increasing the cell size
     */
    zoomIn: () => {
      update((state) => {
        const newSize = Math.min(state.gridSettings.cellSize + 20, 200);
        return {
          ...state,
          gridSettings: {
            ...state.gridSettings,
            cellSize: newSize
          }
        };
      });
    },
    /**
     * Zoom out by decreasing the cell size
     */
    zoomOut: () => {
      update((state) => {
        const newSize = Math.max(state.gridSettings.cellSize - 20, 40);
        return {
          ...state,
          gridSettings: {
            ...state.gridSettings,
            cellSize: newSize
          }
        };
      });
    },
    /**
     * Update the browser panel width
     */
    updateBrowserPanelWidth: (width) => {
      const constrainedWidth = Math.max(200, Math.min(1200, width));
      update((state) => ({
        ...state,
        browserPanelWidth: constrainedWidth
      }));
    },
    /**
     * Toggle whether to show confirmation dialogs for deletions
     */
    toggleConfirmDeletions: (value) => {
      update((state) => ({
        ...state,
        preferences: {
          ...state.preferences,
          confirmDeletions: value !== void 0 ? value : !state.preferences.confirmDeletions
        }
      }));
    },
    /**
     * Reset the UI state to defaults
     */
    reset: () => {
      set(initialState);
    }
  };
}
createUIStore();
function GeneralTab($$payload, $$props) {
  push();
  const settings = settingsStore.getSnapshot();
  const user = useContainer(userContainer);
  let username = user.currentUser || "User";
  let confirmDeletions = true;
  let rememberLastSaveDirectory = true;
  $$payload.out += `<div class="general-tab svelte-1i72se2"><div class="settings-section svelte-1i72se2"><h3 class="svelte-1i72se2">User Settings</h3> <div class="setting-item svelte-1i72se2"><div class="setting-info svelte-1i72se2"><span class="setting-label svelte-1i72se2">Username</span> <span class="setting-description svelte-1i72se2">Your name for exported sequences</span></div> <div class="setting-control username-control svelte-1i72se2"><input type="text"${attr("value", username)} placeholder="Enter your name" aria-label="Username" class="username-input svelte-1i72se2" maxlength="50"/></div></div></div> <div class="settings-section svelte-1i72se2"><h3 class="svelte-1i72se2">Preferences</h3> <div class="setting-item svelte-1i72se2"><div class="setting-info svelte-1i72se2"><span class="setting-label svelte-1i72se2">Haptic Feedback</span> <span class="setting-description svelte-1i72se2">Vibration feedback for touch interactions</span></div> <div class="setting-control svelte-1i72se2"><label class="switch svelte-1i72se2"><input type="checkbox"${attr("checked", settings.hapticFeedback, true)} aria-label="Toggle haptic feedback"${attr("disabled", !hapticFeedbackService.isHapticFeedbackSupported(), true)} class="svelte-1i72se2"/> <span class="slider round svelte-1i72se2"></span></label></div></div> <div class="setting-item svelte-1i72se2"><div class="setting-info svelte-1i72se2"><span class="setting-label svelte-1i72se2">Confirmation Dialogs</span> <span class="setting-description svelte-1i72se2">Show confirmation when clearing sequences or deleting beats</span></div> <div class="setting-control svelte-1i72se2"><label class="switch svelte-1i72se2"><input type="checkbox"${attr("checked", confirmDeletions, true)} aria-label="Toggle confirmation dialogs" class="svelte-1i72se2"/> <span class="slider round svelte-1i72se2"></span></label></div></div> <div class="setting-item svelte-1i72se2"><div class="setting-info svelte-1i72se2"><span class="setting-label svelte-1i72se2">Remember Save Location</span> <span class="setting-description svelte-1i72se2">Remember last directory used for image exports</span></div> <div class="setting-control svelte-1i72se2"><label class="switch svelte-1i72se2"><input type="checkbox"${attr("checked", rememberLastSaveDirectory, true)} aria-label="Toggle remember save location" class="svelte-1i72se2"/> <span class="slider round svelte-1i72se2"></span></label></div></div></div></div>`;
  pop();
}
function SettingsDialog($$payload, $$props) {
  push();
  const tabs = [
    { id: "general", label: "General", icon: "fa-sliders" }
    // Image Export tab temporarily removed
  ];
  function getLastActiveTab() {
    return "general";
  }
  let activeTab = getLastActiveTab();
  let isSaving = false;
  $$payload.out += `<div class="settings-container svelte-v1o7b6" role="dialog" aria-modal="true" aria-labelledby="settings-title"><div class="settings-header svelte-v1o7b6"><div class="settings-title svelte-v1o7b6"><i class="fa-solid fa-gear svelte-v1o7b6"></i> <h2 id="settings-title" class="svelte-v1o7b6">Settings</h2></div> <button class="close-button svelte-v1o7b6" aria-label="Close settings"${attr("disabled", isSaving, true)}><i class="fa-solid fa-xmark svelte-v1o7b6"></i></button></div> `;
  SettingsTabs($$payload, { tabs, activeTab });
  $$payload.out += `<!----> <div class="settings-content svelte-v1o7b6">`;
  if (activeTab === "general") {
    $$payload.out += "<!--[-->";
    GeneralTab($$payload);
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div> <div class="settings-footer svelte-v1o7b6"><button class="reset-button svelte-v1o7b6" aria-label="Reset settings to defaults"${attr("disabled", isSaving, true)}><i class="fa-solid fa-arrows-rotate svelte-v1o7b6"></i> Reset to Defaults</button> <button class="save-button svelte-v1o7b6" aria-label="Save settings"${attr("disabled", isSaving, true)}><i${attr_class(`fa-solid ${stringify("fa-save")}`, "svelte-v1o7b6")}></i> ${escape_html("Save Settings")}</button></div></div>`;
  pop();
}
function MainLayout($$payload, $$props) {
  push();
  var $$store_subs;
  let isSettingsDialogOpen;
  const isSettingsOpenStore = useSelector(appService, (state) => state.context.isSettingsOpen);
  isSettingsDialogOpen = store_get($$store_subs ??= {}, "$isSettingsOpenStore", isSettingsOpenStore);
  if (store_get($$store_subs ??= {}, "$uiStore", uiStore) && store_get($$store_subs ??= {}, "$uiStore", uiStore).windowWidth) {
    Math.max(30, Math.min(50, store_get($$store_subs ??= {}, "$uiStore", uiStore).windowWidth / 12));
  }
  $$payload.out += `<div class="content svelte-1pslyz0"><div class="mainContent svelte-1pslyz0">`;
  TabContent($$payload);
  $$payload.out += `<!----></div> `;
  if (isSettingsDialogOpen) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="settingsBackdrop svelte-1pslyz0" role="button" tabindex="0" aria-label="Close settings"></div> <div class="settingsContent svelte-1pslyz0">`;
    SettingsDialog($$payload);
    $$payload.out += `<!----></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
function LoadingOverlay($$payload, $$props) {
  let onRetry = $$props["onRetry"];
  let showInitializationError = fallback($$props["showInitializationError"], false);
  let progress = fallback($$props["progress"], 0);
  let message = fallback($$props["message"], "Loading...");
  let errorMessage = fallback($$props["errorMessage"], null);
  $$payload.out += `<div class="loading-overlay svelte-1ynnii3"><div class="loading-container svelte-1ynnii3">`;
  LoadingSpinner($$payload, {});
  $$payload.out += `<!----> <div class="loading-progress-container svelte-1ynnii3"><div class="loading-progress-bar svelte-1ynnii3"><div class="loading-progress-fill svelte-1ynnii3"${attr_style(`width: ${stringify(progress)}%`)}></div></div> <p class="loading-text svelte-1ynnii3">${escape_html(message)}</p> `;
  if (showInitializationError) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<p class="error-text svelte-1ynnii3">${escape_html(errorMessage ?? "An error occurred during initialization.")} <button class="retry-button svelte-1ynnii3">Retry</button></p>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div></div></div>`;
  bind_props($$props, {
    onRetry,
    showInitializationError,
    progress,
    message,
    errorMessage
  });
}
function BackgroundCanvas($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  props.backgroundType || "snowfall";
  props.appIsLoading !== void 0 ? props.appIsLoading : true;
  onDestroy(() => {
    return;
  });
  function setQuality(quality) {
    return;
  }
  $$payload.out += `<div class="background-canvas-container svelte-1bdsp4v"><canvas class="background-canvas svelte-1bdsp4v" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; width: 100%; height: 100%; z-index: -1;"></canvas></div>`;
  bind_props($$props, { setQuality });
  pop();
}
function BackgroundProvider($$payload, $$props) {
  push();
  const { $$slots, $$events, ...props } = $$props;
  let backgroundType = props.backgroundType || "snowfall";
  props.initialQuality;
  let isLoading = props.isLoading || false;
  onDestroy(() => {
    return;
  });
  const derivedType = backgroundType;
  const derivedIsLoading = isLoading;
  const background = {
    get type() {
      return derivedType;
    },
    get isLoading() {
      return derivedIsLoading;
    },
    setType: (type) => {
      return;
    },
    setLoading: (loading) => {
      return;
    },
    setQuality: (quality) => {
      return;
    }
  };
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { background });
  pop();
}
function FirstTimeSetupDialog($$payload, $$props) {
  push();
  const user = useContainer(userContainer);
  let username = user.currentUser || "";
  let isVisible = userContainer.isFirstVisit();
  function showDialog() {
    isVisible = true;
  }
  if (isVisible) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="overlay svelte-1p1sxyv"><div class="dialog svelte-1p1sxyv"><div class="dialog-header svelte-1p1sxyv"><h2 class="svelte-1p1sxyv">The Kinetic Constructor</h2> <button class="close-button svelte-1p1sxyv" aria-label="Close dialog">×</button></div> <div class="dialog-content svelte-1p1sxyv"><p class="welcome svelte-1p1sxyv">Kinetic Fire 2025 software pre-release!</p> <div class="compact-info svelte-1p1sxyv"><p class="svelte-1p1sxyv"><strong><br/>Note:</strong> This is an alpha version.<br/> For bugs or feature requests, email<br/> <a href="mailto:austencloud@gmail.com" class="email-link svelte-1p1sxyv">austencloud@gmail.com</a></p> <div class="donation-section svelte-1p1sxyv"><p class="svelte-1p1sxyv"><strong>Support:</strong> If you find this tool useful, consider a donation:</p> <div class="donation-links svelte-1p1sxyv"><a href="https://paypal.me/austencloud" target="_blank" rel="noopener noreferrer" class="donation-link paypal svelte-1p1sxyv">PayPal</a> <a href="https://venmo.com/austencloud" target="_blank" rel="noopener noreferrer" class="donation-link venmo svelte-1p1sxyv">Venmo</a></div></div></div> <div class="input-group svelte-1p1sxyv"><label for="username-input" class="svelte-1p1sxyv">Your Name (Optional)</label> <input type="text" id="username-input"${attr("value", username)} placeholder="Enter your name (or leave blank)" maxlength="50" autocomplete="name" class="svelte-1p1sxyv"/> <p class="input-help svelte-1p1sxyv">Used only when exporting sequences.</p></div></div> <div class="dialog-footer svelte-1p1sxyv"><button class="close-button-large svelte-1p1sxyv">Close</button></div></div></div>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { showDialog });
  pop();
}
function FirstTimeSetupButton($$payload, $$props) {
  push();
  let isDesktopLandscape = false;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<button${attr_class("setup-button svelte-1xmmtlj", void 0, { "desktop-landscape": isDesktopLandscape })} title="Show First-Time Setup Dialog" aria-label="Show First-Time Setup Dialog"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg></button>`;
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function _page($$payload, $$props) {
  push();
  var $$store_subs;
  const windowHeight = store_get($$store_subs ??= {}, "$uiStore", uiStore) ? store_get($$store_subs ??= {}, "$uiStore", uiStore).windowHeight + "px" : "100vh";
  const isInitializingAppStore = useSelector(appService, (state) => state.matches("initializingApp"));
  const isInitializingApp = store_get($$store_subs ??= {}, "$isInitializingAppStore", isInitializingAppStore);
  const hasFailedStore = useSelector(appService, (state) => state.matches("initializationFailed"));
  const hasFailed = store_get($$store_subs ??= {}, "$hasFailedStore", hasFailedStore);
  const isReadyStore = useSelector(appService, (state) => state.matches("ready"));
  const isReady = store_get($$store_subs ??= {}, "$isReadyStore", isReadyStore);
  const currentBackgroundStore = useSelector(appService, (state) => state.context.background);
  const currentBackground = store_get($$store_subs ??= {}, "$currentBackgroundStore", currentBackgroundStore);
  const initializationErrorMsgStore = useSelector(appService, (state) => state.context.initializationError);
  const initializationErrorMsg = store_get($$store_subs ??= {}, "$initializationErrorMsgStore", initializationErrorMsgStore);
  const loadingProgressStore = useSelector(appService, (state) => state.context.loadingProgress);
  const loadingProgress = store_get($$store_subs ??= {}, "$loadingProgressStore", loadingProgressStore);
  const loadingMessageStore = useSelector(appService, (state) => state.context.loadingMessage);
  const loadingMessage = store_get($$store_subs ??= {}, "$loadingMessageStore", loadingMessageStore);
  function handleBackgroundReady() {
    appActions.backgroundReady();
  }
  function handlePerformanceReport(_metrics) {
  }
  function handleRetry() {
    appActions.retryInitialization();
  }
  $$payload.out += `<div id="main-widget"${attr_style(`height: ${stringify(windowHeight)}`)} class="main-widget svelte-tmhtvi">`;
  AppFullScreen($$payload, {
    children: ($$payload2) => {
      $$payload2.out += `<div${attr_class("background svelte-tmhtvi", void 0, { "blur-background": isInitializingApp || hasFailed })}>`;
      BackgroundProvider($$payload2, {
        backgroundType: currentBackground || "snowfall",
        isLoading: isInitializingApp || hasFailed,
        initialQuality: isInitializingApp || hasFailed ? "medium" : "high",
        children: ($$payload3) => {
          BackgroundCanvas($$payload3, {
            appIsLoading: isInitializingApp || hasFailed,
            onReady: handleBackgroundReady,
            onPerformanceReport: handlePerformanceReport
          });
        },
        $$slots: { default: true }
      });
      $$payload2.out += `<!----></div> `;
      if (isInitializingApp || hasFailed) {
        $$payload2.out += "<!--[-->";
        $$payload2.out += `<div class="loading-overlay-wrapper svelte-tmhtvi">`;
        LoadingOverlay($$payload2, {
          message: loadingMessage,
          progress: loadingProgress,
          onRetry: handleRetry,
          showInitializationError: hasFailed,
          errorMessage: initializationErrorMsg
        });
        $$payload2.out += `<!----></div>`;
      } else {
        $$payload2.out += "<!--[!-->";
      }
      $$payload2.out += `<!--]--> `;
      if (isReady) {
        $$payload2.out += "<!--[-->";
        $$payload2.out += `<div class="main-layout-wrapper svelte-tmhtvi">`;
        MainLayout($$payload2);
        $$payload2.out += `<!----></div> `;
        FirstTimeSetupDialog($$payload2, {});
        $$payload2.out += `<!----> `;
        FirstTimeSetupButton($$payload2);
        $$payload2.out += `<!---->`;
      } else {
        $$payload2.out += "<!--[!-->";
      }
      $$payload2.out += `<!--]-->`;
    },
    $$slots: { default: true }
  });
  $$payload.out += `<!----></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
export {
  _page as default
};
