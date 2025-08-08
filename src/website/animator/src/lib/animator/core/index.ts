/**
 * Core exports for easy importing
 */

// Engine
export { AnimationEngine } from './engine/animation-engine.js';

// Services
export { FileService } from './services/file-service.js';
export type { FileImportResult, FileExportResult } from './services/file-service.js';

// State management
export { AnimationStateManager, createInitialState } from './state/animation-state.js';
export type { AnimationState, AnimationStateActions } from './state/animation-state.js';
