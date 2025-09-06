// src/lib/components/Pictograph/utils/errorHandling.ts
import type { PictographData } from '$lib/types/PictographData';
import { get, type Writable } from 'svelte/store';
import { logger } from '$lib/core/logging';
import { errorService, ErrorSeverity } from '../../../services/ErrorHandlingService';
import type { PropData } from '../../objects/Prop/PropData';
import type { ArrowData } from '../../objects/Arrow/ArrowData';

/**
 * Interface for the error handler context
 * Contains all the necessary data and functions for error handling
 */
export interface ErrorHandlerContext {
  pictographDataStore: { subscribe: (callback: (value: PictographData) => void) => () => void };
  dispatch: (event: string, detail?: any) => void;
  state: Writable<string>;
  errorMessage: Writable<string | null>;
  componentsLoaded: number;
  totalComponentsToLoad: number;
}

/**
 * Handles errors that occur during pictograph component operations
 * Logs the error, updates component state, and dispatches events
 *
 * @param source The source of the error (e.g., 'initialization', 'grid loading')
 * @param error The error object or message
 * @param context The error handler context containing necessary data and functions
 */
export function handleError(
  source: string,
  error: any,
  context: ErrorHandlerContext
): void {
  try {
    // Create a safe error message that won't have circular references
    const errorMsg =
      error instanceof Error
        ? error.message
        : typeof error === 'string'
          ? error
          : 'Unknown error';

    // Get current pictograph data for context
    let pictographData: PictographData | undefined;
    const unsubscribe = context.pictographDataStore.subscribe(data => {
      pictographData = data;
    });
    unsubscribe();

    // Get current state value
    const currentState = get(context.state);

    // Log using the structured logging system
    logger.pictograph(`Error in ${source}`, {
      letter: pictographData?.letter
        ? String(pictographData?.letter)
        : undefined,
      gridMode: pictographData?.gridMode,
      componentState: currentState,
      renderMetrics: {
        componentsLoaded: context.componentsLoaded,
        totalComponents: context.totalComponentsToLoad,
        renderTime: performance.now()
      },
      error: error instanceof Error ? error : new Error(errorMsg),
      data: {
        source,
        errorSource: source,
        isCritical: source === 'initialization'
      }
    });

    // For backward compatibility, also log with the error service
    const errorObj = errorService.createError(
      `Pictograph:${source}`,
      { message: errorMsg },
      source === 'initialization' ? ErrorSeverity.CRITICAL : ErrorSeverity.ERROR
    );

    errorObj.context = {
      loadedCount: context.componentsLoaded,
      totalCount: context.totalComponentsToLoad
    };

    errorService.log(errorObj);

    // Set local error message and state
    context.errorMessage.set(errorMsg);
    context.state.set('error');

    // Dispatch events
    context.dispatch('error', { source, error: { message: errorMsg }, message: errorMsg });
    context.dispatch('loaded', { complete: false, error: true, message: errorMsg });
  } catch (errorHandlingError) {
    // If error handling itself fails, use a simpler approach
    logger.error('Error in Pictograph error handler', {
      error:
        errorHandlingError instanceof Error
          ? errorHandlingError
          : new Error(String(errorHandlingError)),
      data: { originalSource: source }
    });

    // Set minimal error state
    context.errorMessage.set('Error in Pictograph component');
    context.state.set('error');

    // Dispatch minimal error events
    context.dispatch('error', { source, error: null, message: 'Error in Pictograph component' });
    context.dispatch('loaded', {
      complete: false,
      error: true,
      message: 'Error in Pictograph component'
    });
  }
}

/**
 * Handles errors that occur in specific pictograph components (Prop, Arrow, etc.)
 * Applies fallback positioning and continues loading
 *
 * @param component The component that experienced the error (e.g., 'redProp', 'blueArrow')
 * @param error The error object or message
 * @param context Additional context for error handling
 * @param fallbackData Object containing the data that needs fallback positioning
 */
export function handleComponentError(
  component: string,
  error: any,
  context: {
    loadedComponents: Set<string>;
    componentsLoaded: number;
    totalComponentsToLoad: number;
    dispatch: (event: string, detail?: any) => void;
    checkLoadingComplete: () => void;
  },
  fallbackData: {
    redPropData: PropData | null;
    bluePropData: PropData | null;
    redArrowData: ArrowData | null;
    blueArrowData: ArrowData | null;
  }
): void {
  logger.warn(`Component error (${component})`, {
    error: error instanceof Error ? error : new Error(String(error)),
    data: {
      component,
      applyingFallback: true
    }
  });

  // Apply fallback positioning
  applyFallbackPositioning(component, fallbackData);

  // Mark component as loaded despite the error
  context.loadedComponents.add(component);
  context.componentsLoaded++;

  logger.debug(`Applied fallback positioning for ${component}`, {
    data: {
      component,
      loadedComponents: Array.from(context.loadedComponents),
      componentsLoaded: context.componentsLoaded,
      totalComponentsToLoad: context.totalComponentsToLoad
    }
  });

  // Continue with loading process
  context.checkLoadingComplete();
}

/**
 * Applies fallback positioning to components that failed to load properly
 * Ensures the pictograph still displays something meaningful despite errors
 *
 * @param component The component that needs fallback positioning
 * @param data Object containing the data that needs fallback positioning
 */
export function applyFallbackPositioning(
  component: string,
  data: {
    redPropData: PropData | null;
    bluePropData: PropData | null;
    redArrowData: ArrowData | null;
    blueArrowData: ArrowData | null;
  }
): void {
  const centerX = 475;
  const centerY = 475;
  const offset = 50;

  switch (component) {
    case 'redProp':
      if (data.redPropData) {
        data.redPropData.coords = { x: centerX - offset, y: centerY };
        data.redPropData.rotAngle = 0;
      }
      break;
    case 'blueProp':
      if (data.bluePropData) {
        data.bluePropData.coords = { x: centerX + offset, y: centerY };
        data.bluePropData.rotAngle = 0;
      }
      break;
    case 'redArrow':
      if (data.redArrowData) {
        data.redArrowData.coords = { x: centerX, y: centerY - offset };
        data.redArrowData.rotAngle = -90;
      }
      break;
    case 'blueArrow':
      if (data.blueArrowData) {
        data.blueArrowData.coords = { x: centerX, y: centerY + offset };
        data.blueArrowData.rotAngle = 90;
      }
      break;
    default:
      logger.warn(`Unknown component: ${component}, using center position`);
  }
}
