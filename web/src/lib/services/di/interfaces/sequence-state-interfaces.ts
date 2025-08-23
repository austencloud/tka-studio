/**
 * DI Container Interface Definitions for Sequence State Services
 */

import { createServiceInterface } from "../types";
import { SequenceStateService } from "$lib/services/implementations/sequence/SequenceStateService";
import type { ISequenceStateService } from "$lib/services/interfaces/sequence-state-interfaces";

// ============================================================================
// SERVICE INTERFACE DEFINITIONS
// ============================================================================

export const ISequenceStateServiceInterface =
  createServiceInterface<ISequenceStateService>(
    "ISequenceStateService",
    SequenceStateService
  );
