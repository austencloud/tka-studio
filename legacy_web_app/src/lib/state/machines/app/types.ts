/**
 * Application State Machine Types
 *
 * This file contains shared types for the application state machine.
 */

import type { BackgroundType } from '$lib/components/MainWidget/state/appState';

/**
 * Context for the application state machine
 */
export interface AppMachineContext {
	currentTab: number;
	previousTab: number;
	background: BackgroundType;
	isFullScreen: boolean;
	isSettingsOpen: boolean;
	initializationError: string | null;
	loadingProgress: number;
	loadingMessage: string;
	contentVisible: boolean;
	backgroundIsReady: boolean;
}

/**
 * Events for the application state machine
 */
export type AppMachineEvents =
	| { type: 'BACKGROUND_READY' }
	| { type: 'INITIALIZATION_SUCCESS' }
	| { type: 'INITIALIZATION_FAILURE'; error: string }
	| { type: 'UPDATE_PROGRESS'; progress: number; message: string }
	| { type: 'RETRY_INITIALIZATION' }
	| { type: 'CHANGE_TAB'; tab: number }
	| { type: 'TOGGLE_FULLSCREEN' }
	| { type: 'SET_FULLSCREEN'; value: boolean }
	| { type: 'OPEN_SETTINGS' }
	| { type: 'CLOSE_SETTINGS' }
	| { type: 'UPDATE_BACKGROUND'; background: string };
