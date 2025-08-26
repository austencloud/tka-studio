/**
 * Background Animation Service Interfaces
 * Defines service interfaces for background animation system
 */

import type { ServiceInterface } from "../types";
import { BackgroundService } from "../../implementations/background/BackgroundService";

export const IBackgroundServiceInterface: ServiceInterface<BackgroundService> = {
  token: "IBackgroundService",
  implementation: BackgroundService,
};
