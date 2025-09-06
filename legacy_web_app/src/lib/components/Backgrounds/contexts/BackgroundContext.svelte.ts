/**
 * Svelte 5 Runes Integration for Background Context
 *
 * This module provides utilities for integrating the background context
 * with Svelte 5 runes. This file has a .svelte.ts extension to enable runes support.
 */

import { getContext, setContext } from 'svelte';
import type {
  BackgroundType,
  Dimensions,
  PerformanceMetrics,
  QualityLevel,
  BackgroundSystem
} from '../types/types';
import { BackgroundFactory } from '../core/BackgroundFactory';
import { PerformanceTracker } from '../core/PerformanceTracker';
import { detectAppropriateQuality } from '../config';
import { browser } from '$app/environment';
import { getBackgroundContext } from './BackgroundContext';

// The context key
const BACKGROUND_CONTEXT_KEY = 'background-context-runes';

/**
 * Interface for the runes-based background context
 */
export interface RunesBackgroundContext {
  // State
  dimensions: Dimensions;
  performanceMetrics: PerformanceMetrics;
  isActive: boolean;
  qualityLevel: QualityLevel;
  isLoading: boolean;
  backgroundType: BackgroundType;
  isInitialized: boolean;
  shouldRender: boolean;
  backgroundSystem: BackgroundSystem | null;

  // Methods
  initializeCanvas: (canvas: HTMLCanvasElement, onReady?: () => void) => void;
  startAnimation: (
    renderFn: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void,
    reportFn?: (metrics: PerformanceMetrics) => void
  ) => void;
  stopAnimation: () => void;
  setQuality: (quality: QualityLevel) => void;
  setLoading: (isLoading: boolean) => void;
  setBackgroundType: (type: BackgroundType) => void;
  cleanup: () => void;

  // State persistence
  savePreferences: () => void;
  loadPreferences: () => void;
}

// Track created context instances to prevent duplicates
let contextInstances = new Set();

/**
 * Create a new background context using Svelte 5 runes
 *
 * This function creates a new background context using Svelte 5's runes system
 * for reactive state management. It provides the same API as the original context
 * but uses runes instead of stores.
 *
 * @returns A runes-based background context
 */
export function createRunesBackgroundContext(): RunesBackgroundContext {
  // Skip browser-specific initialization during SSR
  if (!browser) {
    return createMockRunesBackgroundContext();
  }

  // Debug counter to track context creation
  let contextId = Math.floor(Math.random() * 10000);

  // Ensure we don't create duplicate contexts
  if (contextInstances.size > 0) {
    // Return the existing context from getRunesBackgroundContext
    const existingContext = getRunesBackgroundContext();
    if (existingContext) {
      return existingContext;
    }
  }

  // Initialize state with runes - use explicit initial values to avoid undefined
  let dimensions = $state<Dimensions>({ width: 0, height: 0 });
  let performanceMetrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });
  let isActive = $state(true);
  let qualityLevel = $state<QualityLevel>(detectAppropriateQuality());
  let isLoading = $state(false);
  let backgroundType = $state<BackgroundType>('nightSky');
  let isInitialized = $state(false);

  // Derived values
  let shouldRender = $derived(isActive && performanceMetrics.fps > 30);

  // Create background system based on type and quality
  let backgroundSystem = $state<BackgroundSystem | null>(null);

  // Flag to prevent circular updates
  let isUpdatingSystem = $state(false);

  // Create and track a single background system during context initialization
  if (browser && !backgroundSystem) {
    try {
      backgroundSystem = BackgroundFactory.createBackgroundSystem({
        type: backgroundType,
        initialQuality: qualityLevel
      });
    } catch (error) {
      console.error('[SYSTEM] Error creating initial background system:', error);
      // Try fallback
      try {
        backgroundSystem = BackgroundFactory.createBackgroundSystem({
          type: 'snowfall',
          initialQuality: qualityLevel
        });
      } catch (fallbackError) {
        console.error('[SYSTEM] Error creating fallback background system:', fallbackError);
      }
    }
  }

  // Canvas references
  let canvas: HTMLCanvasElement | null = null;
  let ctx: CanvasRenderingContext2D | null = null;
  let animationFrameId: number | null = null;
  let reportCallback: ((metrics: PerformanceMetrics) => void) | null = null;

  // Load preferences from localStorage
  function loadPreferences() {
    if (!browser) return;

    try {
      const savedPrefs = localStorage.getItem('background-preferences');
      if (savedPrefs) {
        const prefs = JSON.parse(savedPrefs);

        // Only update if values are different to prevent triggering effects
        if (prefs.backgroundType && prefs.backgroundType !== backgroundType) {
          backgroundType = prefs.backgroundType;
        }

        if (prefs.qualityLevel && prefs.qualityLevel !== qualityLevel) {
          qualityLevel = prefs.qualityLevel;
        }
      }
    } catch (error) {
      console.error('Failed to load background preferences:', error);
    }
  }

  // Save preferences to localStorage
  function savePreferences() {
    if (!browser) return;

    try {
      const prefs = {
        backgroundType,
        qualityLevel
      };
      localStorage.setItem('background-preferences', JSON.stringify(prefs));
    } catch (error) {
      console.error('Failed to save background preferences:', error);
    }
  }

  // Function to create and initialize the background system
  function createAndInitializeBackgroundSystem(type: BackgroundType, quality: QualityLevel): void {

    if (backgroundSystem) {
      backgroundSystem.cleanup();
    }

    try {
      const newSystem = BackgroundFactory.createBackgroundSystem({
        type,
        initialQuality: quality
      });

      // Initialize if canvas is already set up
      if (isInitialized && canvas && ctx) {
        newSystem.initialize(dimensions, quality);
      }

      // Set the background system
      backgroundSystem = newSystem;

    } catch (error) {
      console.error('[SYSTEM] Error creating background system:', error);

      // Fallback to snowfall if there's an error with the requested background
      if (type !== 'snowfall') {
        try {
          const fallbackSystem = BackgroundFactory.createBackgroundSystem({
            type: 'snowfall',
            initialQuality: quality
          });

          if (isInitialized && canvas && ctx) {
            fallbackSystem.initialize(dimensions, quality);
          }

          backgroundSystem = fallbackSystem;
        } catch (fallbackError) {
          console.error('[SYSTEM] Error creating fallback background system:', fallbackError);
        }
      }
    }
  }

  // Initialize canvas
  function initializeCanvas(canvasElement: HTMLCanvasElement, onReady?: () => void): void {
    // Skip if already initialized with this canvas
    if (canvas === canvasElement && ctx) {
      if (onReady) onReady();
      return;
    }

    canvas = canvasElement;
    ctx = canvas.getContext('2d');

    if (!ctx) {
      console.error('Failed to get canvas context');
      return;
    }

    const initialWidth = window.innerWidth;
    const initialHeight = window.innerHeight;

    dimensions = { width: initialWidth, height: initialHeight };

    canvas.width = initialWidth;
    canvas.height = initialHeight;

    // Set up event listeners
    const handleResize = () => {
      if (!canvas) return;

      const newWidth = window.innerWidth;
      const newHeight = window.innerHeight;

      canvas.width = newWidth;
      canvas.height = newHeight;

      dimensions = { width: newWidth, height: newHeight };

      // Temporarily reduce quality during resize for better performance
      const currentQuality = qualityLevel;
      qualityLevel = 'low';

      setTimeout(() => {
        qualityLevel = currentQuality;
      }, 500);
    };

    const handleVisibilityChange = () => {
      isActive = document.visibilityState === 'visible';
    };

    window.addEventListener('resize', handleResize);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Set up cleanup when component is destroyed
    $effect(() => {
      // Return cleanup function
      return () => {
        window.removeEventListener('resize', handleResize);
        document.removeEventListener('visibilitychange', handleVisibilityChange);
        stopAnimation();
      };
    });

    isInitialized = true;

    // Initialize background system if it exists
    if (backgroundSystem) {
      backgroundSystem.initialize(dimensions, qualityLevel);
    }

    if (onReady) {
      onReady();
    }
  }

  // Performance tracker
  const performanceTracker = PerformanceTracker.getInstance();

  // Start animation
  function startAnimation(
    renderFn: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void,
    reportFn?: (metrics: PerformanceMetrics) => void
  ): void {
    if (!ctx || !canvas) {
      console.error('Canvas not initialized');
      return;
    }

    // Skip if animation is already running
    if (animationFrameId) {
      return;
    }

    if (reportFn) {
      reportCallback = reportFn;
    }

    performanceTracker.reset();

    const animate = () => {
      if (!ctx || !canvas) return;

      performanceTracker.update();

      const perfStatus = performanceTracker.getPerformanceStatus();
      performanceMetrics = {
        fps: perfStatus.fps,
        warnings: perfStatus.warnings
      };

      if (reportCallback) {
        reportCallback(performanceMetrics);
      }

      const shouldRenderNow = isActive && perfStatus.fps > 30;

      if (shouldRenderNow) {
        ctx.clearRect(0, 0, dimensions.width, dimensions.height);
        renderFn(ctx, dimensions);
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);
  }

  // Stop animation
  function stopAnimation(): void {
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
  }

  // Cleanup
  function cleanup(): void {
    stopAnimation();

    if (backgroundSystem) {
      backgroundSystem.cleanup();
      backgroundSystem = null;
    }

    canvas = null;
    ctx = null;

    // Remove from context instances
    contextInstances.delete(contextId);
  }

  // Flag to prevent circular updates from setters
  let isSettingState = false;

  // Set quality
  function setQuality(quality: QualityLevel): void {
    // Skip if we're already updating to prevent circular updates
    if (isSettingState) {
      return;
    }

    // Skip if the quality hasn't changed
    if (quality === qualityLevel) {
      return;
    }


    isSettingState = true;
    try {
      qualityLevel = quality;

      // Update background system directly rather than waiting for effect
      if (backgroundSystem) {
        backgroundSystem.setQuality(quality);
      }

      savePreferences();
    } finally {
      // Reset the flag immediately
      isSettingState = false;
    }
  }

  // Set loading state
  function setLoading(loading: boolean): void {
    // Skip if we're already updating to prevent circular updates
    if (isSettingState) {
      return;
    }

    // Skip if the loading state hasn't changed
    if (loading === isLoading) {
      return;
    }


    isSettingState = true;
    try {
      isLoading = loading;
    } finally {
      // Reset the flag immediately
      isSettingState = false;
    }
  }

  // Set background type
  function setBackgroundType(type: BackgroundType): void {
    // Skip if we're already updating to prevent circular updates
    if (isSettingState) {
      return;
    }

    // Skip if the background type hasn't changed
    if (type === backgroundType) {
      return;
    }


    isSettingState = true;
    try {
      backgroundType = type;

      // Update background system directly
      createAndInitializeBackgroundSystem(type, qualityLevel);

      savePreferences();
    } finally {
      // Reset the flag immediately
      isSettingState = false;
    }
  }

  // Load preferences on initialization
  if (browser) {
    loadPreferences();
  }

  const context = {
    // State
    get dimensions() { return dimensions; },
    get performanceMetrics() { return performanceMetrics; },
    get isActive() { return isActive; },
    get qualityLevel() { return qualityLevel; },
    get isLoading() { return isLoading; },
    get backgroundType() { return backgroundType; },
    get isInitialized() { return isInitialized; },
    get shouldRender() { return shouldRender; },
    get backgroundSystem() { return backgroundSystem; },

    // Methods
    initializeCanvas,
    startAnimation,
    stopAnimation,
    setQuality,
    setLoading,
    setBackgroundType,
    cleanup,

    // State persistence
    savePreferences,
    loadPreferences
  };

  // Add to context instances
  contextInstances.add(contextId);

  // Return the context
  return context;
}

/**
 * Create a mock background context for SSR
 *
 * @returns A mock background context for SSR
 */
function createMockRunesBackgroundContext(): RunesBackgroundContext {
  // Default values for SSR
  const dimensions = $state<Dimensions>({ width: 0, height: 0 });
  const performanceMetrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });
  const isActive = $state(true);
  const qualityLevel = $state<QualityLevel>('medium');
  const isLoading = $state(false);
  const backgroundType = $state<BackgroundType>('snowfall');
  const isInitialized = $state(false);
  const shouldRender = $derived(isActive && performanceMetrics.fps > 30);

  // Create a mock background system
  const mockSystem = {
    initialize: () => {},
    update: () => {},
    draw: () => {},
    setQuality: () => {},
    cleanup: () => {}
  } as BackgroundSystem;

  // Return a mock context with no-op functions
  return {
    // State
    get dimensions() { return dimensions; },
    get performanceMetrics() { return performanceMetrics; },
    get isActive() { return isActive; },
    get qualityLevel() { return qualityLevel; },
    get isLoading() { return isLoading; },
    get backgroundType() { return backgroundType; },
    get isInitialized() { return isInitialized; },
    get shouldRender() { return shouldRender; },
    get backgroundSystem() { return mockSystem; },

    // No-op methods for SSR
    initializeCanvas: () => {},
    startAnimation: () => {},
    stopAnimation: () => {},
    setQuality: () => {},
    setLoading: () => {},
    setBackgroundType: () => {},
    cleanup: () => {},
    savePreferences: () => {},
    loadPreferences: () => {}
  };
}

// Store a single instance of the context
let singletonContext: RunesBackgroundContext | undefined;

/**
 * Set the runes-based background context
 *
 * @returns The runes-based background context
 */
export function setRunesBackgroundContext(): RunesBackgroundContext {
  // Reuse context if it exists
  if (singletonContext) {
    setContext(BACKGROUND_CONTEXT_KEY, singletonContext);
    return singletonContext;
  }

  singletonContext = createRunesBackgroundContext();
  setContext(BACKGROUND_CONTEXT_KEY, singletonContext);
  return singletonContext;
}

/**
 * Get the runes-based background context
 *
 * @returns The runes-based background context
 */
export function getRunesBackgroundContext(): RunesBackgroundContext | undefined {
  // Return singleton if it exists
  if (singletonContext) {
    return singletonContext;
  }
  return getContext<RunesBackgroundContext>(BACKGROUND_CONTEXT_KEY);
}

/**
 * Hook to use the background context with Svelte 5 runes
 *
 * This hook provides a way to use the background context with Svelte 5 runes.
 * It first tries to get the runes-based context, and if that's not available,
 * it falls back to the store-based context.
 *
 * @returns A reactive state object with background state and methods
 */
export function useBackgroundContext() {
  // If singleton exists, return it
  if (singletonContext) {
    return singletonContext;
  }

  // Try to get the runes-based context first
  const runesContext = getRunesBackgroundContext();

  // If we have a runes-based context, return it directly
  if (runesContext) {
    singletonContext = runesContext;
    return runesContext;
  }

  // Skip context usage during SSR
  if (!browser) {
    // Default values for SSR
    const dimensions = $state<Dimensions>({ width: 0, height: 0 });
    const performanceMetrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });
    const isActive = $state(true);
    const qualityLevel = $state<QualityLevel>('medium');
    const isLoading = $state(false);
    const backgroundType = $state<BackgroundType>('snowfall');
    const isInitialized = $state(false);
    const shouldRender = $derived(isActive && performanceMetrics.fps > 30);

    return {
      // State
      dimensions,
      performanceMetrics,
      isActive,
      qualityLevel,
      isLoading,
      backgroundType,
      isInitialized,
      shouldRender,

      // No-op methods for SSR
      setQuality: () => {},
      setLoading: () => {},
      setBackgroundType: () => {},
      initializeCanvas: () => {},
      startAnimation: () => {},
      stopAnimation: () => {},
      cleanup: () => {}
    };
  }

  // Create and set a new context
  singletonContext = setRunesBackgroundContext();
  return singletonContext;
}
