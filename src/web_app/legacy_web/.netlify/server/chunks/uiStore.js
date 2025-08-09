import { w as writable, k as get, z as browser } from "./vendor.js";
import "clsx";
import { createActor, createMachine, assign, fromPromise } from "xstate";
import { s as sequenceContainer } from "./SequenceContainer.js";
/* empty css                                           */
var Letter = /* @__PURE__ */ ((Letter2) => {
  Letter2["A"] = "A";
  Letter2["B"] = "B";
  Letter2["C"] = "C";
  Letter2["D"] = "D";
  Letter2["E"] = "E";
  Letter2["F"] = "F";
  Letter2["G"] = "G";
  Letter2["H"] = "H";
  Letter2["I"] = "I";
  Letter2["J"] = "J";
  Letter2["K"] = "K";
  Letter2["L"] = "L";
  Letter2["M"] = "M";
  Letter2["N"] = "N";
  Letter2["O"] = "O";
  Letter2["P"] = "P";
  Letter2["Q"] = "Q";
  Letter2["R"] = "R";
  Letter2["S"] = "S";
  Letter2["T"] = "T";
  Letter2["U"] = "U";
  Letter2["V"] = "V";
  Letter2["W"] = "W";
  Letter2["X"] = "X";
  Letter2["Y"] = "Y";
  Letter2["Z"] = "Z";
  Letter2["Σ"] = "Σ";
  Letter2["Δ"] = "Δ";
  Letter2["θ"] = "θ";
  Letter2["Ω"] = "Ω";
  Letter2["W_DASH"] = "W-";
  Letter2["X_DASH"] = "X-";
  Letter2["Y_DASH"] = "Y-";
  Letter2["Z_DASH"] = "Z-";
  Letter2["Σ_DASH"] = "Σ-";
  Letter2["Δ_DASH"] = "Δ-";
  Letter2["θ_DASH"] = "θ-";
  Letter2["Ω_DASH"] = "Ω-";
  Letter2["Φ"] = "Φ";
  Letter2["Ψ"] = "Ψ";
  Letter2["Λ"] = "Λ";
  Letter2["Φ_DASH"] = "Φ-";
  Letter2["Ψ_DASH"] = "Ψ-";
  Letter2["Λ_DASH"] = "Λ-";
  Letter2["α"] = "α";
  Letter2["β"] = "β";
  Letter2["Γ"] = "Γ";
  return Letter2;
})(Letter || {});
class LetterType {
  constructor(letters, description, folderName) {
    this.letters = letters;
    this.description = description;
    this.folderName = folderName;
  }
  static Type1 = new LetterType(
    [
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
      "G",
      "H",
      "I",
      "J",
      "K",
      "L",
      "M",
      "N",
      "O",
      "P",
      "Q",
      "R",
      "S",
      "T",
      "U",
      "V"
    ],
    "Dual-Shift",
    "Type1"
  );
  static Type2 = new LetterType(["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"], "Shift", "Type2");
  static Type3 = new LetterType(
    ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
    "Cross-Shift",
    "Type3"
  );
  static Type4 = new LetterType(["Φ", "Ψ", "Λ"], "Dash", "Type4");
  static Type5 = new LetterType(["Φ-", "Ψ-", "Λ-"], "Dual-Dash", "Type5");
  static Type6 = new LetterType(["α", "β", "Γ"], "Static", "Type6");
  static Type7 = new LetterType(["ζ", "η"], "Skewed", "Type7");
  static Type8 = new LetterType(["μ", "ν"], "TauShift", "Type8");
  static Type9 = new LetterType(["τ", "⊕"], "Centric", "Type9");
  static AllTypes = [
    LetterType.Type1,
    LetterType.Type2,
    LetterType.Type3,
    LetterType.Type4,
    LetterType.Type5,
    LetterType.Type6,
    LetterType.Type7,
    LetterType.Type8,
    LetterType.Type9
  ];
  static getLetterType(letter) {
    const letterStr = letter.toString();
    for (const type of LetterType.AllTypes) {
      if (type.letters.includes(letterStr)) {
        return type;
      }
    }
    return null;
  }
}
var LetterConditions = /* @__PURE__ */ ((LetterConditions2) => {
  LetterConditions2["ALPHA_ENDING"] = "alpha_ending";
  LetterConditions2["BETA_ENDING"] = "beta_ending";
  LetterConditions2["GAMMA_ENDING"] = "gamma_ending";
  LetterConditions2["HYBRID"] = "hybrid";
  LetterConditions2["NON_HYBRID"] = "non_hybrid";
  return LetterConditions2;
})(LetterConditions || {});
class LetterUtils {
  static conditionMappings = {
    [LetterConditions.ALPHA_ENDING]: [
      Letter.A,
      Letter.B,
      Letter.C,
      Letter.D,
      Letter.E,
      Letter.F,
      Letter.W,
      Letter.X,
      Letter.W_DASH,
      Letter.X_DASH,
      Letter.Φ,
      Letter.Φ_DASH,
      Letter.α
    ],
    [LetterConditions.BETA_ENDING]: [
      Letter.G,
      Letter.H,
      Letter.I,
      Letter.J,
      Letter.K,
      Letter.L,
      Letter.Y,
      Letter.Z,
      Letter.Y_DASH,
      Letter.Z_DASH,
      Letter.Ψ,
      Letter.Ψ_DASH,
      Letter.β
    ],
    [LetterConditions.GAMMA_ENDING]: [
      Letter.M,
      Letter.N,
      Letter.O,
      Letter.P,
      Letter.Q,
      Letter.R,
      Letter.S,
      Letter.T,
      Letter.U,
      Letter.V,
      Letter.Σ,
      Letter.Δ,
      Letter.θ,
      Letter.Ω,
      Letter.Σ_DASH,
      Letter.Δ_DASH,
      Letter.θ_DASH,
      Letter.Ω_DASH,
      Letter.Λ,
      Letter.Λ_DASH,
      Letter.Γ
    ],
    [LetterConditions.HYBRID]: [
      Letter.C,
      Letter.F,
      Letter.I,
      Letter.L,
      Letter.O,
      Letter.R,
      Letter.U,
      Letter.V,
      Letter.W,
      Letter.X,
      Letter.Y,
      Letter.Z,
      Letter.W_DASH,
      Letter.X_DASH,
      Letter.Y_DASH,
      Letter.Z_DASH,
      Letter.Σ,
      Letter.Δ,
      Letter.θ,
      Letter.Ω,
      Letter.Σ_DASH,
      Letter.Δ_DASH,
      Letter.θ_DASH,
      Letter.Ω_DASH,
      Letter.Φ,
      Letter.Ψ,
      Letter.Λ
    ],
    [LetterConditions.NON_HYBRID]: [
      Letter.A,
      Letter.B,
      Letter.D,
      Letter.E,
      Letter.G,
      Letter.H,
      Letter.J,
      Letter.K,
      Letter.M,
      Letter.N,
      Letter.P,
      Letter.Q,
      Letter.S,
      Letter.T,
      Letter.Φ_DASH,
      Letter.Ψ_DASH,
      Letter.Λ_DASH,
      Letter.α,
      Letter.β,
      Letter.Γ
    ]
  };
  static getLettersByCondition(condition) {
    return this.conditionMappings[condition] || [];
  }
  static letterMappings = {
    α: Letter.α,
    beta: Letter.β,
    β: Letter.β,
    alpha: Letter.α,
    gamma: Letter.Γ,
    Γ: Letter.Γ,
    γ: Letter.Γ,
    theta: Letter.θ,
    theta_dash: Letter.θ_DASH,
    omega: Letter.Ω,
    omega_dash: Letter.Ω_DASH,
    phi: Letter.Φ,
    phi_dash: Letter.Φ_DASH,
    psi: Letter.Ψ,
    psi_dash: Letter.Ψ_DASH,
    lambda: Letter.Λ,
    lambda_dash: Letter.Λ_DASH,
    sigma: Letter.Σ,
    sigma_dash: Letter.Σ_DASH,
    delta: Letter.Δ,
    delta_dash: Letter.Δ_DASH
  };
  static fromString(letterStr) {
    if (!letterStr) {
      throw new Error("Cannot convert empty input to Letter");
    }
    let normalizedStr = letterStr.trim().replace(/θ/g, "theta").replace(/Θ/g, "Theta").replace(/ω/g, "omega").replace(/Ω/g, "Omega").replace(/φ/g, "phi").replace(/Φ/g, "Phi").replace(/ψ/g, "psi").replace(/Ψ/g, "Psi").replace(/λ/g, "lambda").replace(/Λ/g, "Lambda").replace(/σ/g, "sigma").replace(/Σ/g, "Sigma").replace(/δ/g, "delta").replace(/Δ/g, "Delta").toLowerCase().replace(/-/g, "_dash");
    if (this.letterMappings[normalizedStr]) {
      return this.letterMappings[normalizedStr];
    }
    const enumKey = Object.keys(Letter).find((key) => key.toLowerCase() === normalizedStr);
    if (enumKey) {
      return Letter[enumKey];
    }
    console.warn(`Could not convert letter: "${letterStr}"`, {
      normalizedStr,
      availableLetters: Object.keys(Letter)
    });
    throw new Error(`No matching enum member for string: ${letterStr}`);
  }
  // More forgiving version that returns null instead of throwing
  static tryFromString(letterStr) {
    try {
      return this.fromString(letterStr);
    } catch {
      return null;
    }
  }
  static getLetter(letterStr) {
    return this.fromString(letterStr);
  }
}
const pictographDataStore = writable([]);
function createPictographStore() {
  const { subscribe, set, update } = writable({
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
  });
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
  function calculateProgress(components) {
    const loadedCount = Object.values(components).filter(Boolean).length;
    const totalComponents = Object.keys(components).length;
    return Math.floor(loadedCount / totalComponents * 100);
  }
  return {
    subscribe,
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
        const newProgress = calculateProgress(updatedComponents);
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
      const timestamp = Date.now();
      transitionTo("error", message);
      update((state) => ({
        ...state,
        error: { message, component, timestamp },
        loadProgress: 0
      }));
    },
    updateGridData: (gridData) => {
      update((state) => {
        if (!state.data) return state;
        transitionTo("props_loading", "Grid data loaded");
        return {
          ...state,
          data: { ...state.data, gridData },
          components: { ...state.components, grid: true }
        };
      });
    },
    updatePropData: (color, propData) => {
      update((state) => {
        if (!state.data) return state;
        const key = color === "red" ? "redPropData" : "bluePropData";
        const componentKey = color === "red" ? "redProp" : "blueProp";
        transitionTo("arrows_loading", `${color} prop loaded`);
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
    reset: () => {
      set({
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
      });
    },
    transitionTo
  };
}
createPictographStore();
class PersistenceError extends Error {
  constructor(message) {
    super(message);
    this.name = "PersistenceError";
  }
}
class DataCorruptionError extends PersistenceError {
  constructor(id, originalError) {
    super(`Corrupted data detected for ${id}${originalError ? `: ${originalError.message}` : ""}`);
    this.name = "DataCorruptionError";
  }
}
class StorageError extends PersistenceError {
  constructor(operation, originalError) {
    super(
      `Storage operation failed during ${operation}${originalError ? `: ${originalError.message}` : ""}`
    );
    this.name = "StorageError";
  }
}
function validateMachineSnapshot(snapshot) {
  return snapshot && typeof snapshot === "object" && "status" in snapshot && typeof snapshot.status === "string" && ["active", "done", "error", "stopped"].includes(snapshot.status) && "context" in snapshot && typeof snapshot.context === "object";
}
function validateStoreData(data) {
  return data !== void 0 && data !== null;
}
function addDependency(dependencies, containerExists, dependentId, dependencyId) {
  if (!containerExists(dependentId)) {
    console.debug(`Cannot add dependency: dependent ID "${dependentId}" is not registered`);
    return false;
  }
  if (!containerExists(dependencyId)) {
    console.debug(`Cannot add dependency: dependency ID "${dependencyId}" is not registered`);
    return false;
  }
  if (!dependencies.has(dependentId)) {
    dependencies.set(dependentId, /* @__PURE__ */ new Set());
  }
  dependencies.get(dependentId).add(dependencyId);
  return true;
}
function getDependencies(dependencies, id) {
  return Array.from(dependencies.get(id) || []);
}
function getDependents(dependencies, id) {
  const dependents = [];
  dependencies.forEach((deps, depId) => {
    if (deps.has(id)) {
      dependents.push(depId);
    }
  });
  return dependents;
}
function topologicalSort(dependencies, containerIds) {
  const result = [];
  const visited = /* @__PURE__ */ new Set();
  const temporaryMark = /* @__PURE__ */ new Set();
  const visit = (id) => {
    if (temporaryMark.has(id)) {
      console.error(`Circular dependency detected including ${id}`);
      return;
    }
    if (visited.has(id)) return;
    temporaryMark.add(id);
    const deps = dependencies.get(id);
    if (deps) {
      for (const depId of deps) {
        visit(depId);
      }
    }
    temporaryMark.delete(id);
    visited.add(id);
    result.push(id);
  };
  for (const id of containerIds) {
    if (!visited.has(id)) {
      visit(id);
    }
  }
  return result;
}
function loadPersistedState(persistenceKey) {
  const persistedState = {};
  const lastPersistedState = {};
  try {
    const persistedStateJson = localStorage.getItem(persistenceKey);
    if (!persistedStateJson) {
      return { persistedState, lastPersistedState };
    }
    const parsedData = JSON.parse(persistedStateJson);
    if (typeof parsedData !== "object" || parsedData === null) {
      throw new DataCorruptionError("root");
    }
    Object.entries(parsedData).forEach(([id, data]) => {
      try {
        if (!data || typeof data !== "object" || !("type" in data)) {
          throw new DataCorruptionError(id);
        }
        if (data.type === "machine" && (!("snapshot" in data) || !validateMachineSnapshot(data.snapshot))) {
          throw new DataCorruptionError(id);
        } else if (data.type === "store" && !("value" in data)) {
          throw new DataCorruptionError(id);
        }
        persistedState[id] = data;
        if (!lastPersistedState[id]) {
          lastPersistedState[id] = {};
        }
        if (data.type === "machine") {
          lastPersistedState[id].value = data.snapshot;
        } else if (data.type === "store") {
          lastPersistedState[id].value = data.value;
        }
      } catch (error) {
        console.warn(`Skipping corrupted state for "${id}":`, error);
      }
    });
  } catch (error) {
    console.error("Failed to load or parse persisted state from localStorage:", error);
    if (typeof localStorage !== "undefined") {
      try {
        const corruptedData = localStorage.getItem(persistenceKey);
        if (corruptedData) {
          localStorage.setItem(`${persistenceKey}_corrupted_backup`, corruptedData);
          localStorage.removeItem(persistenceKey);
        }
      } catch {
      }
    }
  }
  return { persistedState, lastPersistedState };
}
function performPersist(containers, lastPersistedState, persistenceKey) {
  const stateToPersist = {};
  let hasChanges = false;
  const updatedLastPersistedState = { ...lastPersistedState };
  Array.from(containers.values()).forEach((container) => {
    if (!container.persist) return;
    try {
      const instance = container.instance;
      let currentStateValue;
      let lastPersistedValue = lastPersistedState[container.id]?.value;
      if (container.type === "machine" && instance && typeof instance.send === "function") {
        const actorInstance = instance;
        if (actorInstance.getSnapshot().status !== "stopped") {
          const persistedSnapshot = actorInstance.getPersistedSnapshot();
          if (persistedSnapshot !== void 0) {
            currentStateValue = persistedSnapshot;
            if (!lastPersistedValue || JSON.stringify(lastPersistedValue) !== JSON.stringify(currentStateValue)) {
              stateToPersist[container.id] = {
                type: "machine",
                snapshot: currentStateValue
              };
              hasChanges = true;
            }
          }
        }
      } else if (container.type === "store") {
        const store = instance;
        currentStateValue = get(store);
        if (!lastPersistedValue || JSON.stringify(lastPersistedValue) !== JSON.stringify(currentStateValue)) {
          stateToPersist[container.id] = {
            type: "store",
            value: currentStateValue
          };
          hasChanges = true;
        }
      }
      if (stateToPersist[container.id]) {
        if (!updatedLastPersistedState[container.id]) {
          updatedLastPersistedState[container.id] = {};
        }
        updatedLastPersistedState[container.id].value = currentStateValue;
      }
    } catch (error) {
      console.error(`Failed to get state for persistence for ${container.id}:`, error);
    }
  });
  if (hasChanges) {
    try {
      localStorage.setItem(persistenceKey, JSON.stringify(stateToPersist));
    } catch (error) {
      const storageError = new StorageError("write", error instanceof Error ? error : void 0);
      console.error(storageError.message);
      if (error instanceof DOMException && error.name === "QuotaExceededError") {
        handleStorageQuotaError(persistenceKey);
      }
    }
  }
  return updatedLastPersistedState;
}
function handleStorageQuotaError(persistenceKey) {
  try {
    const allPersistedState = JSON.parse(localStorage.getItem(persistenceKey) || "{}");
    const criticalStateKeys = Object.keys(allPersistedState).filter(
      (key) => (
        // Define your criteria for critical states here
        key.includes("user") || key.includes("auth") || key.includes("app")
      )
    );
    const reducedState = {};
    criticalStateKeys.forEach((key) => {
      reducedState[key] = allPersistedState[key];
    });
    localStorage.setItem(persistenceKey, JSON.stringify(reducedState));
    console.warn("Storage quota exceeded - reduced persisted state to critical data only");
  } catch (error) {
    console.error("Failed to handle storage quota error:", error);
  }
}
function debugRegistry(containers, getDependencies2, getDependents2) {
  console.group("State Registry");
  containers.forEach((container) => {
    console.group(`${container.id} (${container.type})`);
    if (container.description) {
      console.log(`Description: ${container.description}`);
    }
    try {
      const instance = container.instance;
      if (container.type === "machine" && instance && typeof instance.send === "function") {
        const actor = instance;
        console.log("State:", actor.getSnapshot());
      } else if (container.type === "store") {
        const store = instance;
        console.log("Value:", get(store));
      }
    } catch (error) {
      console.error(`Error getting state for ${container.id}:`, error);
    }
    const dependencies = getDependencies2(container.id);
    if (dependencies.length > 0) {
      console.log("Dependencies:", dependencies);
    }
    const dependents = getDependents2(container.id);
    if (dependents.length > 0) {
      console.log("Dependents:", dependents);
    }
    console.groupEnd();
  });
  console.groupEnd();
}
class StateRegistry {
  containers = /* @__PURE__ */ new Map();
  persistenceEnabled = browser;
  persistenceKey = "app_state";
  persistedState = {};
  lastPersistedState = {};
  // Cache for selective persistence
  persistenceDebounceTimer = null;
  persistenceDebounceDelay = 300;
  // ms
  dependencies = /* @__PURE__ */ new Map();
  // Track dependencies between state containers
  constructor() {
    if (this.persistenceEnabled) {
      const { persistedState, lastPersistedState } = loadPersistedState(this.persistenceKey);
      this.persistedState = persistedState;
      this.lastPersistedState = lastPersistedState;
      if (typeof window !== "undefined") {
        window.addEventListener("beforeunload", () => {
          this.persistState();
        });
      }
    }
  }
  /**
   * Register a state container (machine or store)
   */
  register(id, instance, options) {
    if (this.containers.has(id)) {
      console.warn(`State container with ID "${id}" is already registered. Overwriting.`);
      this.unregister(id);
    }
    this.containers.set(id, {
      id,
      instance,
      subscriptions: /* @__PURE__ */ new Set(),
      ...options
    });
    return instance;
  }
  /**
   * Add a dependency relationship between state containers
   */
  addDependency(dependentId, dependencyId) {
    return addDependency(
      this.dependencies,
      (id) => this.containers.has(id),
      dependentId,
      dependencyId
    );
  }
  /**
   * Get all dependencies for a state container
   */
  getDependencies(id) {
    return getDependencies(this.dependencies, id);
  }
  /**
   * Get all dependents of a state container
   */
  getDependents(id) {
    return getDependents(this.dependencies, id);
  }
  /**
   * Get initialization order based on dependency graph
   */
  getInitializationOrder() {
    return topologicalSort(this.dependencies, Array.from(this.containers.keys()));
  }
  /**
   * Register a state machine
   */
  registerMachine(id, machine, options = {}) {
    let snapshotToRestore = void 0;
    const persistedData = this.persistedState[id];
    if (persistedData?.type === "machine") {
      try {
        if (validateMachineSnapshot(persistedData.snapshot)) {
          snapshotToRestore = persistedData.snapshot;
        } else {
          throw new DataCorruptionError(id);
        }
      } catch (error) {
        console.error(`Invalid persisted snapshot for machine "${id}". Using fallback.`, error);
        snapshotToRestore = options.snapshot;
      }
    } else {
      snapshotToRestore = options.snapshot;
    }
    const actorOptions = {};
    if (snapshotToRestore) {
      actorOptions.snapshot = snapshotToRestore;
    }
    let actor;
    actor = createActor(machine, actorOptions);
    actor.start();
    this.containers.set(id, {
      id,
      type: "machine",
      instance: actor,
      persist: options.persist,
      description: options.description,
      subscriptions: /* @__PURE__ */ new Set()
    });
    return actor;
  }
  /**
   * Register a Svelte store
   */
  registerStore(id, store, options = {}) {
    const persistedData = this.persistedState[id];
    if (persistedData?.type === "store" && "set" in store) {
      const writableStore = store;
      try {
        if (validateStoreData(persistedData.value)) {
          writableStore.set(persistedData.value);
        } else {
          throw new DataCorruptionError(id);
        }
      } catch (error) {
        console.error(`Failed to restore persisted state for store "${id}":`, error);
      }
    }
    const container = {
      id,
      type: "store",
      instance: store,
      persist: options.persist,
      description: options.description,
      subscriptions: /* @__PURE__ */ new Set()
    };
    this.containers.set(id, container);
    return store;
  }
  /**
   * Get a state container by ID
   */
  get(id) {
    const container = this.containers.get(id);
    return container ? container.instance : void 0;
  }
  /**
   * Remove a state container from the registry and clean up all subscriptions
   */
  unregister(id) {
    const container = this.containers.get(id);
    if (!container) return false;
    if (container.type === "machine") {
      const actor = container.instance;
      if (actor && actor.getSnapshot().status !== "stopped") {
        try {
          actor.stop();
        } catch (error) {
          console.error(`Error stopping actor ${id}:`, error);
        }
      }
    }
    if (container.subscriptions) {
      container.subscriptions.forEach((unsubscribe) => {
        try {
          unsubscribe();
        } catch (error) {
          console.error(`Error unsubscribing from ${id}:`, error);
        }
      });
    }
    this.dependencies.delete(id);
    for (const [depId, deps] of this.dependencies.entries()) {
      deps.delete(id);
    }
    return this.containers.delete(id);
  }
  /**
   * Track a subscription for automatic cleanup
   */
  trackSubscription(id, unsubscribe) {
    const container = this.containers.get(id);
    if (container && container.subscriptions) {
      container.subscriptions.add(unsubscribe);
    }
  }
  /**
   * Get all registered state containers
   */
  getAll() {
    return Array.from(this.containers.values());
  }
  /**
   * Get all state containers of a specific type
   */
  getAllByType(type) {
    return this.getAll().filter((container) => container.type === type);
  }
  /**
   * Clear the registry (useful for testing)
   */
  clear() {
    this.getAllByType("machine").forEach((container) => {
      const actor = container.instance;
      if (actor && actor.getSnapshot().status !== "stopped") {
        try {
          actor.stop();
        } catch (error) {
          console.error(`Error stopping actor ${container.id}:`, error);
        }
      }
    });
    this.containers.forEach((container) => {
      if (container.subscriptions) {
        container.subscriptions.forEach((unsubscribe) => {
          try {
            unsubscribe();
          } catch (error) {
            console.error(`Error during unsubscribe in clear():`, error);
          }
        });
      }
    });
    this.containers.clear();
    this.dependencies.clear();
    this.persistedState = {};
    this.lastPersistedState = {};
  }
  /**
   * Persist state to localStorage with debouncing and selective updating
   */
  persistState() {
    if (!this.persistenceEnabled) return;
    if (this.persistenceDebounceTimer) {
      clearTimeout(this.persistenceDebounceTimer);
    }
    this.persistenceDebounceTimer = setTimeout(() => {
      this.lastPersistedState = performPersist(
        this.containers,
        this.lastPersistedState,
        this.persistenceKey
      );
    }, this.persistenceDebounceDelay);
  }
  /**
   * Debug helper to log the current state of all containers
   */
  debug() {
    debugRegistry(
      this.getAll(),
      (id) => this.getDependencies(id),
      (id) => this.getDependents(id)
    );
  }
  /**
   * Get persisted state for a specific ID (loaded at startup)
   */
  getPersistedState(id) {
    return this.persistedState[id];
  }
}
const stateRegistry = new StateRegistry();
function createStore(id, initialState2, actions, options = {}) {
  const { subscribe, set, update } = writable(initialState2);
  const wrappedSubscribe = (run, invalidate) => {
    const unsubscribe = subscribe(run, invalidate);
    stateRegistry.trackSubscription(id, unsubscribe);
    return unsubscribe;
  };
  const getState = () => get({ subscribe });
  const storeActions = actions(set, update, getState);
  const resetAction = {
    reset: () => set(initialState2)
  };
  const store = {
    subscribe: wrappedSubscribe,
    getSnapshot: getState,
    // Add getSnapshot method for compatibility
    ...storeActions,
    ...resetAction
  };
  stateRegistry.registerStore(id, store, {
    persist: options.persist,
    description: options.description
  });
  return store;
}
function createAppMachine(id, machine, options = {}) {
  return stateRegistry.registerMachine(id, machine, {
    persist: options.persist,
    description: options.description
  });
}
async function checkForSequenceInUrl(sequenceContainer2) {
  return false;
}
const defaultImageExportSettings = {
  addUserInfo: true,
  addWord: true,
  addDifficultyLevel: true,
  addBeatNumbers: true,
  addReversalSymbols: true,
  userName: "User",
  customNote: "Created with The Kinetic Constructor",
  rememberLastSaveDirectory: true,
  lastSaveDirectory: "",
  useCategories: true,
  defaultCategory: "Sequences"
};
structuredClone(defaultImageExportSettings);
async function initializeApplication(progressCallback) {
  const reportProgress = (progress, message) => {
    progressCallback?.(progress, message);
  };
  reportProgress(0, "Starting initialization...");
  try {
    const isBrowser = typeof window !== "undefined";
    let preloadingPromise = Promise.resolve();
    if (isBrowser) {
      reportProgress(10, "Preloading SVG resources...");
      const { initSvgPreloading } = await import("./SvgPreloader.js").then((n) => n.S);
      preloadingPromise = initSvgPreloading();
    } else {
      reportProgress(10, "Server-side rendering (skipping SVG preload)...");
    }
    if (isBrowser) {
      reportProgress(30, "Checking for shared sequence...");
      const foundSequenceInUrl = checkForSequenceInUrl(sequenceContainer);
      if (!foundSequenceInUrl) {
        reportProgress(40, "Loading saved sequence...");
        sequenceContainer.loadFromLocalStorage();
      }
    }
    const preloadProgress = 70;
    if (isBrowser) {
      reportProgress(preloadProgress, "Finalizing resource loading...");
      await preloadingPromise;
    } else {
      reportProgress(preloadProgress, "Skipping SVG finalize...");
    }
    reportProgress(90, "Preparing user interface...");
    if (isBrowser) {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    reportProgress(100, "Ready!");
    return true;
  } catch (error) {
    console.error("Initialization failed:", error);
    throw error;
  }
}
function loadBackgroundPreference() {
  return "snowfall";
}
function loadActiveTabPreference() {
  return 0;
}
const appMachine = createMachine(
  {
    id: "appMachine",
    types: {},
    context: {
      currentTab: loadActiveTabPreference(),
      previousTab: 0,
      background: loadBackgroundPreference(),
      isFullScreen: false,
      isSettingsOpen: false,
      // Always initialize as closed
      initializationError: null,
      loadingProgress: 0,
      loadingMessage: "Initializing...",
      contentVisible: false,
      backgroundIsReady: false
    },
    initial: "initializingBackground",
    states: {
      initializingBackground: {
        entry: assign({
          backgroundIsReady: false,
          initializationError: null,
          loadingProgress: 0,
          loadingMessage: "Loading background...",
          contentVisible: false
        }),
        on: {
          BACKGROUND_READY: {
            target: "initializingApp",
            actions: assign({ backgroundIsReady: true })
          }
        }
      },
      initializingApp: {
        entry: assign({
          initializationError: null,
          loadingProgress: 0,
          loadingMessage: "Initializing application...",
          contentVisible: false
        }),
        invoke: {
          src: "initializeApplication",
          onDone: {
            target: "ready",
            actions: assign({
              loadingProgress: 100,
              loadingMessage: "Ready!",
              initializationError: null
            })
          },
          onError: {
            target: "initializationFailed",
            actions: assign({
              initializationError: (_, event) => {
                return typeof event?.data === "object" ? event.data?.message || "Unknown error" : "Initialization failed";
              },
              loadingProgress: 0
            })
          }
        },
        on: {
          UPDATE_PROGRESS: {
            actions: assign({
              loadingProgress: ({ event }) => event.progress,
              loadingMessage: ({ event }) => event.message
            })
          }
        }
      },
      initializationFailed: {
        on: {
          RETRY_INITIALIZATION: {
            target: "initializingApp",
            guard: ({ context }) => context.backgroundIsReady
          }
        }
      },
      ready: {
        entry: [
          assign({
            contentVisible: true,
            loadingProgress: 0,
            loadingMessage: ""
          }),
          // Enforce the background selection from localStorage
          ({ self, context }) => {
          },
          // Add this new action to enforce the tab selection from localStorage
          ({ self, context }) => {
          }
        ],
        on: {
          CHANGE_TAB: {
            target: "ready",
            actions: [
              assign({
                previousTab: ({ context }) => context.currentTab,
                currentTab: ({ event }) => event.tab
              }),
              ({ event }) => {
              }
            ],
            guard: ({ context, event }) => context.currentTab !== event.tab
          },
          TOGGLE_FULLSCREEN: {
            actions: assign({
              isFullScreen: ({ context }) => !context.isFullScreen
            })
          },
          OPEN_SETTINGS: {
            actions: assign({ isSettingsOpen: true })
          },
          CLOSE_SETTINGS: {
            actions: assign({ isSettingsOpen: false })
          },
          UPDATE_BACKGROUND: {
            actions: [
              assign({
                background: ({ event, context }) => {
                  const validBackgrounds = ["snowfall", "nightSky"];
                  return validBackgrounds.includes(event.background) ? event.background : context.background;
                }
              }),
              ({ event }) => {
              }
            ]
          }
        }
      }
    }
  },
  {
    actors: {
      initializeApplication: fromPromise(async ({ self }) => {
        const progressCallback = (progress, message) => {
          self.send({ type: "UPDATE_PROGRESS", progress, message });
        };
        try {
          const success = await initializeApplication(progressCallback);
          if (!success) {
            throw new Error("Initialization returned false.");
          }
          return success;
        } catch (error) {
          throw error;
        }
      })
    }
  }
);
const appService = createAppMachine("app", appMachine, {
  persist: true,
  description: "Core application state machine"
});
const initialState = {
  isLoading: true,
  activeTabIndex: 0,
  isSettingsOpen: false,
  isFullScreen: false,
  windowWidth: typeof window !== "undefined" ? window.innerWidth : 1024,
  windowHeight: typeof window !== "undefined" ? window.innerHeight : 768,
  isMobile: typeof window !== "undefined" ? window.innerWidth < 768 : false,
  isTablet: typeof window !== "undefined" ? window.innerWidth >= 768 && window.innerWidth < 1024 : false,
  isDesktop: typeof window !== "undefined" ? window.innerWidth >= 1024 : true,
  theme: "system",
  sidebarOpen: true
};
const uiStore = createStore("ui", initialState, (_set, update) => ({
  /**
   * Update window dimensions and responsive breakpoints
   */
  updateWindowDimensions: (width, height) => {
    update((state) => ({
      ...state,
      windowWidth: width,
      windowHeight: height,
      isMobile: width < 768,
      isTablet: width >= 768 && width < 1024,
      isDesktop: width >= 1024
    }));
  },
  /**
   * Set the active tab
   */
  setActiveTab: (index) => {
    update((state) => ({ ...state, activeTabIndex: index }));
  },
  /**
   * Toggle settings dialog
   */
  toggleSettings: () => {
    update((state) => ({ ...state, isSettingsOpen: !state.isSettingsOpen }));
  },
  /**
   * Set settings dialog state
   */
  setSettingsOpen: (isOpen) => {
    update((state) => ({ ...state, isSettingsOpen: isOpen }));
  },
  /**
   * Toggle fullscreen mode
   */
  toggleFullScreen: () => {
    update((state) => ({ ...state, isFullScreen: !state.isFullScreen }));
  },
  /**
   * Set fullscreen mode
   */
  setFullScreen: (isFullScreen) => {
    update((state) => ({ ...state, isFullScreen }));
  },
  /**
   * Set theme
   */
  setTheme: (theme) => {
    update((state) => ({ ...state, theme }));
    if (typeof document !== "undefined") {
      if (theme === "system") {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        document.documentElement.classList.toggle("dark", prefersDark);
      } else {
        document.documentElement.classList.toggle("dark", theme === "dark");
      }
    }
  },
  /**
   * Toggle sidebar
   */
  toggleSidebar: () => {
    update((state) => ({ ...state, sidebarOpen: !state.sidebarOpen }));
  },
  /**
   * Set sidebar state
   */
  setSidebarOpen: (isOpen) => {
    update((state) => ({ ...state, sidebarOpen: isOpen }));
  }
}));
if (typeof window !== "undefined") {
  window.addEventListener("resize", () => {
    uiStore.updateWindowDimensions(window.innerWidth, window.innerHeight);
  });
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", () => {
    let currentState;
    const unsubscribe = uiStore.subscribe((state) => {
      currentState = state;
    });
    unsubscribe();
    if (currentState && currentState.theme === "system") {
      document.documentElement.classList.toggle("dark", mediaQuery.matches);
    }
  });
}
export {
  LetterType as L,
  appService as a,
  createStore as c,
  pictographDataStore as p,
  stateRegistry as s,
  uiStore as u
};
