/**
 * Pictograph Machine Actions
 *
 * This module provides actions for the pictograph state machine.
 */

import type { PictographMachineContext } from './pictographMachine.js';
import type { PictographData } from '../types/PictographData.js';
import type { ArrowData } from '../components/objects/Arrow/ArrowData.js';
import type { GridData } from '../components/objects/Grid/GridData.js';
import type { PropData } from '../components/objects/Prop/PropData.js';

/**
 * Helper function to calculate progress
 */
function calculateProgress(components: PictographMachineContext['components']): number {
  const total = Object.keys(components).length;
  const loaded = Object.values(components).filter(Boolean).length;
  return Math.floor((loaded / Math.max(total, 1)) * 100);
}

/**
 * Sets the pictograph data and transitions to grid_loading
 */
export function setData(
  context: PictographMachineContext,
  event: { type: 'SET_DATA'; data: PictographData }
) {
  context.data = event.data;
  addStateTransition(context, 'initializing', 'grid_loading', 'Starting to load pictograph');
}

/**
 * Updates a component's loaded status
 */
export function updateComponentLoaded(
  context: PictographMachineContext,
  event: { type: 'UPDATE_COMPONENT_LOADED'; component: keyof PictographMachineContext['components'] }
) {
  context.components[event.component] = true;
  context.loadProgress = calculateProgress(context.components);
}

/**
 * Sets an error state
 */
export function setError(
  context: PictographMachineContext,
  event: { type: 'SET_ERROR'; message: string; component?: string }
) {
  context.error = {
    message: event.message,
    component: event.component,
    timestamp: Date.now()
  };
  context.loadProgress = 0;
  addStateTransition(context, context.status, 'error', event.message);
}

/**
 * Updates the grid data
 */
export function updateGridData(
  context: PictographMachineContext,
  event: { type: 'UPDATE_GRID_DATA'; gridData: GridData }
) {
  if (!context.data) return;

  context.data = { ...context.data, gridData: event.gridData };
  context.components.grid = true;
  addStateTransition(context, context.status, 'props_loading', 'Grid data loaded');
}

/**
 * Updates prop data for a specific color
 */
export function updatePropData(
  context: PictographMachineContext,
  event: { type: 'UPDATE_PROP_DATA'; color: 'red' | 'blue'; propData: PropData }
) {
  if (!context.data) return;

  const key = event.color === 'red' ? 'redPropData' : 'bluePropData';
  const componentKey = event.color === 'red' ? 'redProp' : 'blueProp';

  context.data = { ...context.data, [key]: event.propData };
  context.components[componentKey] = true;
  addStateTransition(context, context.status, 'arrows_loading', `${event.color} prop loaded`);
}

/**
 * Updates arrow data for a specific color
 */
export function updateArrowData(
  context: PictographMachineContext,
  event: { type: 'UPDATE_ARROW_DATA'; color: 'red' | 'blue'; arrowData: ArrowData }
) {
  if (!context.data) return;

  const key = event.color === 'red' ? 'redArrowData' : 'blueArrowData';
  const componentKey = event.color === 'red' ? 'redArrow' : 'blueArrow';

  context.data = { ...context.data, [key]: event.arrowData };
  context.components[componentKey] = true;
}

/**
 * Resets the pictograph state
 */
export function reset(context: PictographMachineContext) {
  context.status = 'idle';
  context.data = null;
  context.error = null;
  context.loadProgress = 0;
  context.components = {
    grid: false,
    redProp: false,
    blueProp: false,
    redArrow: false,
    blueArrow: false
  };
  context.stateHistory = [];
}

/**
 * Adds a state transition to the history
 */
export function addStateTransition(
  context: PictographMachineContext,
  from: PictographMachineContext['status'],
  to: PictographMachineContext['status'],
  reason?: string
) {
  context.status = to;
  context.stateHistory = [
    ...context.stateHistory,
    {
      from,
      to,
      reason,
      timestamp: Date.now()
    }
  ].slice(-10); // Keep only the last 10 transitions
}

/**
 * Checks if all components are loaded
 */
export function checkAllComponentsLoaded(context: PictographMachineContext) {
  const allLoaded = Object.values(context.components).every(Boolean);
  if (allLoaded && context.status !== 'complete') {
    addStateTransition(context, context.status, 'complete', 'All components loaded');
  }
}
