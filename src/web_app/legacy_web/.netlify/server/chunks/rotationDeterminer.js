import { w as writable, j as derived } from "./vendor.js";
const initialState = {
  status: "idle",
  progress: 0,
  message: "Ready to generate",
  errorMessage: null,
  lastGeneratedAt: null
};
const { subscribe, set, update } = writable({ ...initialState });
derived(
  { subscribe },
  ($state) => $state.status === "generating"
);
derived(
  { subscribe },
  ($state) => $state.status === "error"
);
derived(
  { subscribe },
  ($state) => $state.progress
);
derived(
  { subscribe },
  ($state) => $state.message
);
function startGeneration() {
  update((state) => ({
    ...state,
    status: "generating",
    progress: 0,
    message: "Starting generation...",
    errorMessage: null
  }));
}
function updateProgress(progress2, message) {
  update((state) => ({
    ...state,
    progress: Math.min(100, Math.max(0, progress2)),
    message
  }));
}
function completeGeneration() {
  update((state) => ({
    ...state,
    status: "complete",
    progress: 100,
    message: "Generation complete",
    lastGeneratedAt: /* @__PURE__ */ new Date()
  }));
}
function setError(errorMessage) {
  update((state) => ({
    ...state,
    status: "error",
    errorMessage,
    message: "Generation failed"
  }));
}
function reset() {
  set({ ...initialState });
}
const generatorStore = {
  subscribe,
  startGeneration,
  updateProgress,
  completeGeneration,
  setError,
  reset
};
function determineRotationDirection(propContinuity) {
  if (propContinuity === "continuous") {
    const baseDirection = Math.random() < 0.5 ? "clockwise" : "counterclockwise";
    return {
      blue: baseDirection,
      red: baseDirection
    };
  }
  return {
    blue: Math.random() < 0.5 ? "clockwise" : "counterclockwise",
    red: Math.random() < 0.5 ? "clockwise" : "counterclockwise"
  };
}
export {
  determineRotationDirection as d,
  generatorStore as g
};
