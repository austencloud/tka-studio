import { createActor } from 'xstate';
import { appMachine as appStateMachine } from '$lib/state/machines/app/app.machine';
import { tabs } from './appState';
import { useSelector as useXStateSelector } from '@xstate/svelte';

export const appService = createActor(appStateMachine, {
	inspect: import.meta.env.DEV ? undefined : undefined
}).start();

export const useSelector = useXStateSelector;

export const selectAppContext = () => useXStateSelector(appService, (snapshot) => snapshot.context);
export const selectIsSettingsOpen = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.isSettingsOpen);
export const selectBackground = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.background);
export const selectCurrentTab = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.currentTab);
export const selectPreviousTab = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.previousTab);
export const selectContentVisible = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.contentVisible);
export const selectInitializationError = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.initializationError);
export const selectLoadingProgress = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.loadingProgress);
export const selectLoadingMessage = () =>
	useXStateSelector(appService, (snapshot) => snapshot.context.loadingMessage);
export const selectIsLoading = () =>
	useXStateSelector(
		appService,
		(snapshot) => snapshot.matches('initializingBackground') || snapshot.matches('initializingApp')
	);
export const selectIsInitializingApp = () =>
	useXStateSelector(appService, (snapshot) => snapshot.matches('initializingApp'));
export const selectIsReady = () =>
	useXStateSelector(appService, (snapshot) => snapshot.matches('ready'));
export const selectHasInitializationFailed = () =>
	useXStateSelector(appService, (snapshot) => snapshot.matches('initializationFailed'));
export const selectSlideDirection = () =>
	useXStateSelector(
		appService,
		(snapshot) => snapshot.context.currentTab > snapshot.context.previousTab
	);

export const selectActiveTabData = () =>
	useXStateSelector(appService, (snapshot) => {
		const currentTabIndex = snapshot.context.currentTab;

		if (currentTabIndex >= 0 && currentTabIndex < tabs.length) {
			const activeTab = tabs[currentTabIndex];
			return activeTab;
		} else {
			return null;
		}
	});

if (typeof window !== 'undefined') {
	window.addEventListener('beforeunload', () => {
		appService.stop();
	});
}
