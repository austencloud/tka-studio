// src/lib/components/MainWidget/state/actions.ts
import { appService } from './store';
import { tabs } from './appState'; // Keep for tab id

// Define event types more explicitly (if needed, often inferred)
export type TabChangeEventDetail = {
	index: number;
	id: string;
};
export type BackgroundChangeEventDetail = string;

// No longer needs callbacks passed in, but you might keep them if the *caller* needs them
// For simplicity, let's assume side effects are handled elsewhere or triggered by state changes
export const actions = {
	changeTab: (newTabIndex: number): void => {
		// The machine handles the logic (guards, context updates, transitions)
		appService.send({ type: 'CHANGE_TAB', tab: newTabIndex });

		// If the caller still needs this info immediately (less common with state machines)
		// You could return info or the caller could select it from the state
		// onTabChange({ index: newTabIndex, id: tabs[newTabIndex].id });
	},

	updateBackground: (newBackground: string): void => {
		appService.send({ type: 'UPDATE_BACKGROUND', background: newBackground });
		// onBackgroundChange(newBackground);
	},

	setFullScreen: (isFullScreen: boolean): void => {
		// If you only toggle, a single event is better:
		appService.send({ type: 'TOGGLE_FULLSCREEN' });
		// If you need to set explicitly:
		// This would require adding SET_FULLSCREEN event/logic to the machine
		// appService.send({ type: 'SET_FULLSCREEN', fullscreen: isFullScreen });
	},

	openSettings: (): void => {
		appService.send({ type: 'OPEN_SETTINGS' });
	},

	closeSettings: (): void => {
		appService.send({ type: 'CLOSE_SETTINGS' });
	},

	retryInitialization: (): void => {
		appService.send({ type: 'RETRY_INITIALIZATION' });
	},

    backgroundReady: (): void => {
        appService.send({ type: 'BACKGROUND_READY' });
    }
};
