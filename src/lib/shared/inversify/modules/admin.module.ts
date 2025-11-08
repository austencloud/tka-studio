/**
 * Admin Module - InversifyJS DI Container Configuration
 *
 * Registers all admin services with the dependency injection container.
 */

import { ContainerModule, type ContainerModuleLoadOptions } from "inversify";
import { TYPES } from "../types";
import type { IAdminChallengeService } from "../../../modules/admin/services/contracts";
import { AdminChallengeService } from "../../../modules/admin/services/implementations";

export const adminModule = new ContainerModule(
  (options: ContainerModuleLoadOptions) => {
    // Admin Challenge Service
    options
      .bind<IAdminChallengeService>(TYPES.IAdminChallengeService)
      .to(AdminChallengeService)
      .inSingletonScope();
  }
);
