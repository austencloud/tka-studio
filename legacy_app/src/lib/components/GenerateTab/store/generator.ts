// src/lib/components/GenerateTab/store/generator.ts
import { writable, derived } from 'svelte/store';

// Generator states
export type GeneratorStatus =
  | 'idle'           // Ready to generate
  | 'generating'     // Currently generating
  | 'complete'       // Generation complete
  | 'error';         // Error occurred

// Generator state interface
interface GeneratorState {
  status: GeneratorStatus;
  progress: number;       // 0-100 progress percentage
  message: string;        // Status message
  errorMessage: string | null;
  lastGeneratedAt: Date | null;
}

// Initial state
const initialState: GeneratorState = {
  status: 'idle',
  progress: 0,
  message: 'Ready to generate',
  errorMessage: null,
  lastGeneratedAt: null
};

// Create the store
const { subscribe, set, update } = writable<GeneratorState>({ ...initialState });

// Derived stores
export const isGenerating = derived(
  { subscribe },
  $state => $state.status === 'generating'
);

export const hasError = derived(
  { subscribe },
  $state => $state.status === 'error'
);

export const progress = derived(
  { subscribe },
  $state => $state.progress
);

export const statusMessage = derived(
  { subscribe },
  $state => $state.message
);

// Actions
function startGeneration() {
  update(state => ({
    ...state,
    status: 'generating',
    progress: 0,
    message: 'Starting generation...',
    errorMessage: null
  }));
}

function updateProgress(progress: number, message: string) {
  update(state => ({
    ...state,
    progress: Math.min(100, Math.max(0, progress)),
    message
  }));
}

function completeGeneration() {
  update(state => ({
    ...state,
    status: 'complete',
    progress: 100,
    message: 'Generation complete',
    lastGeneratedAt: new Date()
  }));
}

function setError(errorMessage: string) {
  update(state => ({
    ...state,
    status: 'error',
    errorMessage,
    message: 'Generation failed'
  }));
}

function reset() {
  set({ ...initialState });
}

// Export the store and its actions
export const generatorStore = {
  subscribe,
  startGeneration,
  updateProgress,
  completeGeneration,
  setError,
  reset
};
