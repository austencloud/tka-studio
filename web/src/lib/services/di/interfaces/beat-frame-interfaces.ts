/**
 * DI Container Interface Definitions for Beat Frame Services
 */

import { createServiceInterface } from "../types";
import { BeatFrameService } from "$lib/services/implementations/layout/BeatFrameService";
import type { IBeatFrameService } from "$lib/services/interfaces/beat-frame-interfaces";

// ============================================================================
// SERVICE INTERFACE DEFINITIONS
// ============================================================================

export const IBeatFrameServiceInterface =
  createServiceInterface<IBeatFrameService>(
    "IBeatFrameService",
    BeatFrameService
  );
