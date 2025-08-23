/**
 * DI Container Interface Definitions for Workbench Services
 */

import { WorkbenchCoordinationService } from "$lib/services/implementations/workbench/WorkbenchCoordinationService";
import { WorkbenchService } from "$lib/services/implementations/workbench/WorkbenchService";
import type {
  IWorkbenchCoordinationService,
  IWorkbenchService,
} from "$lib/services/interfaces/workbench-interfaces";
import { createServiceInterface } from "../types";

// ============================================================================
// SERVICE INTERFACE DEFINITIONS
// ============================================================================

export const IWorkbenchServiceInterface =
  createServiceInterface<IWorkbenchService>(
    "IWorkbenchService",
    WorkbenchService
  );

export const IWorkbenchCoordinationServiceInterface =
  createServiceInterface<IWorkbenchCoordinationService>(
    "IWorkbenchCoordinationService",
    class extends WorkbenchCoordinationService {
      constructor(...args: unknown[]) {
        super(args[0] as IWorkbenchService);
      }
    }
  );
