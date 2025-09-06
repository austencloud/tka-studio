/**
 * Application State Selectors
 *
 * This file contains selectors for the app state machine.
 * Selectors are functions that extract specific pieces of state from the machine.
 */

import { derived } from 'svelte/store';
import { useSelector } from '@xstate/svelte';
import { appService } from './app.machine';
import { createSelector } from '$lib/state/core';

// Basic selectors
export const selectAppContext = () => useSelector(appService, (snapshot) => snapshot.context);

export const selectIsSettingsOpen = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.isSettingsOpen),
  { id: 'app.isSettingsOpen', description: 'Whether the settings panel is open' }
);

export const selectBackground = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.background),
  { id: 'app.background', description: 'Current background type' }
);

export const selectCurrentTab = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.currentTab),
  { id: 'app.currentTab', description: 'Current active tab index' }
);

export const selectPreviousTab = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.previousTab),
  { id: 'app.previousTab', description: 'Previous active tab index' }
);

export const selectContentVisible = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.contentVisible),
  { id: 'app.contentVisible', description: 'Whether the main content is visible' }
);

export const selectInitializationError = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.initializationError),
  { id: 'app.initializationError', description: 'Error message from initialization' }
);

export const selectLoadingProgress = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.loadingProgress),
  { id: 'app.loadingProgress', description: 'Current loading progress (0-100)' }
);

export const selectLoadingMessage = createSelector(
  useSelector(appService, (snapshot) => snapshot.context.loadingMessage),
  { id: 'app.loadingMessage', description: 'Current loading message' }
);

// Derived selectors
export const selectIsLoading = createSelector(
  useSelector(
    appService,
    (snapshot) => snapshot.matches('initializingBackground') || snapshot.matches('initializingApp')
  ),
  { id: 'app.isLoading', description: 'Whether the app is in a loading state' }
);

export const selectIsInitializingApp = createSelector(
  useSelector(appService, (snapshot) => snapshot.matches('initializingApp')),
  { id: 'app.isInitializingApp', description: 'Whether the app is initializing' }
);

export const selectIsReady = createSelector(
  useSelector(appService, (snapshot) => snapshot.matches('ready')),
  { id: 'app.isReady', description: 'Whether the app is ready' }
);

export const selectHasInitializationFailed = createSelector(
  useSelector(appService, (snapshot) => snapshot.matches('initializationFailed')),
  { id: 'app.hasInitializationFailed', description: 'Whether initialization has failed' }
);

export const selectSlideDirection = createSelector(
  useSelector(
    appService,
    (snapshot) => snapshot.context.currentTab > snapshot.context.previousTab
  ),
  { id: 'app.slideDirection', description: 'Direction of tab slide animation' }
);
