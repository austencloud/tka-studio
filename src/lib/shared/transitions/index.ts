/**
 * Modern View Transitions Module
 * Exports for smooth, coordinated transitions between modules/tabs
 */

export {
  viewTransitionManager,
  createViewTransitionManager,
  type TransitionPhase,
  type TransitionDirection,
} from './view-transition-state.svelte';

export { default as ViewTransitionCoordinator } from './ViewTransitionCoordinator.svelte';
