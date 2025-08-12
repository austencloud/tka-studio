/**
 * Core exports for easy importing
 */

// Engine
export { AnimationEngine } from "./engine/animation-engine.js";

// Services
export { HybridDictionaryService } from "./services/hybrid-dictionary.js";

// State management
export {
  AnimationStateManager,
  createInitialState,
} from "./state/animation-state.js";
export type {
  AnimationState,
  AnimationStateActions,
} from "./state/animation-state.js";
