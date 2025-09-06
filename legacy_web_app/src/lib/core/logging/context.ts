/**
 * Logging Context Management
 *
 * Provides utilities for managing and enriching log context.
 */

import { browser } from '$app/environment';
import { LogDomain, type LoggerContext } from './types';

/**
 * Global context that applies to all loggers
 */
let globalContext: Partial<LoggerContext> = {
  data: {}
};

/**
 * Set global context that will be included in all logs
 */
export function setGlobalContext(context: Partial<LoggerContext>): void {
  globalContext = {
    ...globalContext,
    ...context,
    // Merge data objects
    data: {
      ...(globalContext.data || {}),
      ...(context.data || {})
    }
  };
}

/**
 * Get the current global context
 */
export function getGlobalContext(): Partial<LoggerContext> {
  return { ...globalContext };
}

/**
 * Add data to the global context
 */
export function addGlobalContextData(data: Record<string, unknown>): void {
  globalContext = {
    ...globalContext,
    data: {
      ...(globalContext.data || {}),
      ...data
    }
  };
}

/**
 * Clear the global context
 */
export function clearGlobalContext(): void {
  globalContext = { data: {} };
}

/**
 * Create a context object for a specific domain
 */
export function createDomainContext(domain: LogDomain, data?: Record<string, unknown>): Partial<LoggerContext> {
  return {
    domain,
    data: {
      ...(globalContext.data || {}),
      ...(data || {})
    }
  };
}

/**
 * Create a context object for a pictograph
 */
export function createPictographContext(params: {
  letter?: string;
  gridMode?: string;
  componentState?: string;
}): Partial<LoggerContext> {
  return createDomainContext(LogDomain.PICTOGRAPH, params);
}

/**
 * Create a context object for a sequence
 */
export function createSequenceContext(params: {
  sequenceId?: string;
  motionType?: string;
  gridType?: string;
}): Partial<LoggerContext> {
  return createDomainContext(LogDomain.SEQUENCE, params);
}

/**
 * Create a context object for SVG operations
 */
export function createSvgContext(params: {
  path?: string;
  component?: string;
}): Partial<LoggerContext> {
  return createDomainContext(LogDomain.SVG, params);
}

/**
 * Create a context object for state machines
 */
export function createStateContext(params: {
  machine: string;
  state?: string;
}): Partial<LoggerContext> {
  return createDomainContext(LogDomain.STATE, params);
}

/**
 * Create a context object for components
 */
export function createComponentContext(params: {
  component: string;
  props?: Record<string, unknown>;
}): Partial<LoggerContext> {
  return createDomainContext(LogDomain.COMPONENT, params);
}

/**
 * Gather automatic context information from the environment
 */
export function gatherAutomaticContext(): Partial<LoggerContext> {
  if (!browser) {
    return {
      data: {
        environment: 'server'
      }
    };
  }

  return {
    data: {
      environment: 'browser',
      userAgent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      },
      devicePixelRatio: window.devicePixelRatio,
      url: window.location.href,
      referrer: document.referrer,
      language: navigator.language
    }
  };
}

/**
 * Initialize global context with automatic information
 */
export function initializeGlobalContext(): void {
  setGlobalContext(gatherAutomaticContext());
}

// Initialize global context when this module is loaded
if (browser) {
  initializeGlobalContext();
}
