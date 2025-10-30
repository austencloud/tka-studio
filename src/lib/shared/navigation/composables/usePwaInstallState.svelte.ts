/**
 * PWA Installation State Composable
 *
 * Manages PWA installation state including:
 * - Detecting if app is already installed
 * - Tracking native install prompt availability
 * - Listening for installation events
 * - Cleaning up event listeners
 *
 * Returns reactive state that can be used in any Svelte component.
 */

import type { IMobileFullscreenService } from "$shared";
import { resolve, TYPES } from "$shared";

export interface PwaInstallState {
  showInstallOption: boolean;
  canUseNativeInstall: boolean;
}

/**
 * Creates and manages PWA installation state
 * Returns reactive state and cleanup function
 */
export function usePwaInstallState(): {
  state: PwaInstallState;
  cleanup: () => void;
} {
  const state = $state<PwaInstallState>({
    showInstallOption: false,
    canUseNativeInstall: false,
  });

  let fullscreenService: IMobileFullscreenService | undefined;
  let unsubscribePrompt: (() => void) | undefined;
  let handleAppInstalled: (() => void) | undefined;

  try {
    fullscreenService = resolve<IMobileFullscreenService>(
      TYPES.IMobileFullscreenService
    );

    const isPWA = fullscreenService?.isPWA?.() ?? false;

    // Only show install option if not already installed as PWA
    if (!isPWA) {
      state.showInstallOption = true;
      state.canUseNativeInstall = fullscreenService?.canInstallPWA?.() ?? false;

      // Listen for install prompt availability changes
      unsubscribePrompt = fullscreenService?.onInstallPromptAvailable?.(
        (available: boolean) => {
          state.canUseNativeInstall = available;
        }
      );

      // Listen for app installation
      handleAppInstalled = () => {
        state.showInstallOption = false;
      };
      window.addEventListener("appinstalled", handleAppInstalled);
    }
  } catch (error) {
    console.warn("Failed to initialize PWA install state:", error);
  }

  const cleanup = () => {
    unsubscribePrompt?.();
    if (handleAppInstalled) {
      window.removeEventListener("appinstalled", handleAppInstalled);
    }
  };

  return { state, cleanup };
}
