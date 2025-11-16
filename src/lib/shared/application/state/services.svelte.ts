import type { IPersistenceService, ISettingsService } from "$shared";
import { ensureContainerInitialized, resolve } from "../../inversify";
import { TYPES } from "../../inversify/types";

// Make isInitialized reactive so components using getSettings() will re-evaluate
let isInitialized = $state(false);
let settingsService: ISettingsService | null = null;
let persistenceService: IPersistenceService | null = null;

export async function initializeAppServices(): Promise<void> {
  if (isInitialized) return;

  await ensureContainerInitialized();
  settingsService = await resolve(TYPES.ISettingsService);
  isInitialized = true;
}

export function clearAppServicesCache(): void {
  isInitialized = false;
  settingsService = null;
  persistenceService = null;
}

export function getSettingsServiceSync(): ISettingsService {
  if (!settingsService) {
    throw new Error(
      "Settings service not initialized. Call initializeAppServices first."
    );
  }
  return settingsService;
}

export async function getSettingsService(): Promise<ISettingsService> {
  if (!settingsService) {
    settingsService = await resolve(TYPES.ISettingsService);
  }
  return settingsService!;
}

export function getPersistenceService(): IPersistenceService {
  if (!persistenceService) {
    persistenceService = resolve(TYPES.IPersistenceService);
  }
  return persistenceService!;
}

export function areServicesInitialized(): boolean {
  return isInitialized;
}
