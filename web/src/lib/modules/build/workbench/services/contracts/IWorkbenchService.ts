/**
 * Workbench Service Interface
 *
 * Interface for managing workbench operations.
 */

import type { BeatData } from "$shared/domain";

export interface IWorkbenchService {
  initializeWorkbench(): Promise<void>;
  getCurrentBeat(): BeatData | null;
  updateBeat(beat: BeatData): Promise<void>;
  clearWorkbench(): void;
}
