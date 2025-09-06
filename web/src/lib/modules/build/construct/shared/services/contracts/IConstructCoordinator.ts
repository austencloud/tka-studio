import type { BeatData, SequenceData } from "$shared/domain";

/**
 * Coordination service for Construct sub-tabs
 * Restored minimal contract based on usages in BuildTabEventService.
 */
export interface IConstructSubTabCoordinationService {
  setupComponentCoordination(components: Record<string, unknown>): void;
  handleSequenceModified(sequence: SequenceData): Promise<void>;
  handleStartPositionSet(startPosition: BeatData): Promise<void>;
  handleBeatAdded(beatData: BeatData): Promise<void>;
  handleGenerationRequest(config: Record<string, unknown>): Promise<void>;
  handleUITransitionRequest(targetPanel: string): Promise<void>;
}
