/**
 * Application State Machine
 *
 * This machine manages the core application state, including:
 * - Initialization
 * - Tab navigation
 * - Settings
 * - Background management
 */

import { createMachine, assign, fromPromise } from 'xstate';
import { createAppMachine } from '$lib/state/core';
import { initializeApplication } from '$lib/utils/appInitializer';
import type { BackgroundType } from '$lib/components/MainWidget/state/appState';
import { browser } from '$app/environment';
import { type AppMachineContext, type AppMachineEvents } from './types';
import {
	loadBackgroundPreference,
	loadActiveTabPreference,
	saveBackgroundPreference,
	saveActiveTabPreference
} from '$lib/utils/preferences';

// --- State Machine Definition ---
export const appMachine = createMachine(
	{
		id: 'appMachine',
		types: {} as {
			context: AppMachineContext;
			events: AppMachineEvents;
		},
		context: {
			currentTab: loadActiveTabPreference(),
			previousTab: 0,
			background: loadBackgroundPreference(),
			isFullScreen: false,
			isSettingsOpen: false, // Always initialize as closed
			initializationError: null,
			loadingProgress: 0,
			loadingMessage: 'Initializing...',
			contentVisible: false,
			backgroundIsReady: false
		},
		initial: 'initializingBackground',
		states: {
			initializingBackground: {
				entry: assign({
					backgroundIsReady: false,
					initializationError: null,
					loadingProgress: 0,
					loadingMessage: 'Loading background...',
					contentVisible: false
				}),
				on: {
					BACKGROUND_READY: {
						target: 'initializingApp',
						actions: assign({ backgroundIsReady: true })
					}
				}
			},
			initializingApp: {
				entry: assign({
					initializationError: null,
					loadingProgress: 0,
					loadingMessage: 'Initializing application...',
					contentVisible: false
				}),
				invoke: {
					src: 'initializeApplication',
					onDone: {
						target: 'ready',
						actions: assign({
							loadingProgress: 100,
							loadingMessage: 'Ready!',
							initializationError: null
						})
					},
					onError: {
						target: 'initializationFailed',
						actions: assign({
							initializationError: (_, event: any) => {
								// Safely extract error message from the event
								return typeof event?.data === 'object'
									? event.data?.message || 'Unknown error'
									: 'Initialization failed';
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
						target: 'initializingApp',
						guard: ({ context }) => context.backgroundIsReady
					}
				}
			},
			ready: {
				entry: [
					assign({
						contentVisible: true,
						loadingProgress: 0,
						loadingMessage: ''
					}),
					// Enforce the background selection from localStorage
					({ self, context }) => {
						if (browser) {
							try {
								const savedBackground = loadBackgroundPreference();
								console.log('Checking saved background in ready state:', savedBackground);

								if (savedBackground && savedBackground !== context.background) {
									console.log(
										'Enforcing background from localStorage in ready state:',
										savedBackground
									);
									// Use a small timeout to ensure this happens after other initialization
									setTimeout(() => {
										self.send({ type: 'UPDATE_BACKGROUND', background: savedBackground });
									}, 100);
								}
							} catch (error) {
								console.error('Error enforcing background on ready state:', error);
							}
						}
					},
					// Add this new action to enforce the tab selection from localStorage
					({ self, context }) => {
						if (browser) {
							try {
								const savedTab = loadActiveTabPreference();
								if (savedTab !== context.currentTab) {
									console.log('Enforcing tab from localStorage in ready state:', savedTab);
									// Use a small timeout to ensure this happens after other initialization
									setTimeout(() => {
										self.send({ type: 'CHANGE_TAB', tab: savedTab });
									}, 150);
								}
							} catch (error) {
								console.error('Error enforcing tab on ready state:', error);
							}
						}
					}
				],
				on: {
					CHANGE_TAB: {
						target: 'ready',
						actions: [
							assign({
								previousTab: ({ context }) => context.currentTab,
								currentTab: ({ event }) => event.tab
							}),
							({ event }) => {
								// Save the current tab to localStorage immediately
								if (browser) {
									try {
										console.log('Saving tab to localStorage immediately:', event.tab);
										saveActiveTabPreference(event.tab);
										console.log('Tab saved successfully');
									} catch (error) {
										console.error('Error saving last active tab:', error);
									}
								}
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
									const validBackgrounds: BackgroundType[] = ['snowfall', 'nightSky'];
									return validBackgrounds.includes(event.background as BackgroundType)
										? (event.background as BackgroundType)
										: context.background;
								}
							}),
							({ event }) => {
								// Save the background preference to localStorage immediately
								if (browser) {
									try {
										const validBackgrounds: BackgroundType[] = ['snowfall', 'nightSky'];
										const background = event.background as BackgroundType;

										if (validBackgrounds.includes(background)) {
											console.log(
												'Saving background preference to localStorage immediately:',
												background
											);
											saveBackgroundPreference(background);
											console.log('Background preference saved successfully');
										}
									} catch (error) {
										console.error('Error saving background preference:', error);
									}
								}
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
				const progressCallback = (progress: number, message: string) => {
					self.send({ type: 'UPDATE_PROGRESS', progress, message });
				};

				try {
					const success = await initializeApplication(progressCallback);
					if (!success) {
						throw new Error('Initialization returned false.');
					}
					return success;
				} catch (error) {
					throw error;
				}
			})
		}
	}
);

// Create and register the app machine
export const appService = createAppMachine('app', appMachine, {
	persist: true,
	description: 'Core application state machine'
});

// Subscribe to state changes to ensure persistence
if (browser) {
	// Subscribe to state changes to ensure direct persistence
	appService.subscribe((state) => {
		// Only save when in the ready state to avoid saving during initialization
		if (state.matches('ready')) {
			try {
				// Save background preference directly
				const background = state.context.background;
				if (background) {
					saveBackgroundPreference(background);
				}

				// Save tab preference directly
				const currentTab = state.context.currentTab;
				saveActiveTabPreference(currentTab);

				// Explicitly reset isSettingsOpen in localStorage to prevent auto-opening on reload
				try {
					const storageKey = 'xstate-app';
					const storedData = localStorage.getItem(storageKey);

					if (storedData) {
						const parsedData = JSON.parse(storedData);

						// If the stored data includes isSettingsOpen, ensure it's set to false
						if (parsedData && parsedData.context && 'isSettingsOpen' in parsedData.context) {
							console.log('Ensuring settings dialog is closed in persisted state');
							parsedData.context.isSettingsOpen = false;
							localStorage.setItem(storageKey, JSON.stringify(parsedData));
						}
					}
				} catch (storageError) {
					console.error('Error modifying persisted settings state:', storageError);
				}
			} catch (error) {
				console.error('Error saving preferences to localStorage:', error);
			}
		}
	});
}
