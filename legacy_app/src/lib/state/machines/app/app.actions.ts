/**
 * Application State Actions
 *
 * This file contains action creators for the app state machine.
 * Actions are functions that send events to the machine to trigger state changes.
 */

import { appService } from './app.machine';
import type { BackgroundType } from '$lib/components/MainWidget/state/appState';

/**
 * App actions object containing all available actions
 */
export const appActions = {
  /**
   * Change the active tab
   * @param tab The index of the tab to activate
   */
  changeTab: (tab: number): void => {
    appService.send({ type: 'CHANGE_TAB', tab });
  },

  /**
   * Toggle fullscreen mode
   */
  toggleFullScreen: (): void => {
    appService.send({ type: 'TOGGLE_FULLSCREEN' });
  },

  /**
   * Set fullscreen mode
   * @param isFullScreen Whether to enable fullscreen mode
   */
  setFullScreen: (isFullScreen: boolean): void => {
    const currentState = appService.getSnapshot().context.isFullScreen;
    if (currentState !== isFullScreen) {
      appService.send({ type: 'TOGGLE_FULLSCREEN' });
    }
  },

  /**
   * Open the settings panel
   */
  openSettings: (): void => {
    appService.send({ type: 'OPEN_SETTINGS' });
  },

  /**
   * Close the settings panel
   */
  closeSettings: (): void => {
    appService.send({ type: 'CLOSE_SETTINGS' });
  },

  /**
   * Update the background type
   * @param background The new background type
   */
  updateBackground: (background: BackgroundType): void => {
    appService.send({ type: 'UPDATE_BACKGROUND', background });
  },

  /**
   * Signal that the background is ready
   */
  backgroundReady: (): void => {
    appService.send({ type: 'BACKGROUND_READY' });
  },

  /**
   * Retry initialization after a failure
   */
  retryInitialization: (): void => {
    appService.send({ type: 'RETRY_INITIALIZATION' });
  }
};
