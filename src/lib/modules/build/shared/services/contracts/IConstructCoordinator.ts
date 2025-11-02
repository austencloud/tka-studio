import type { BeatData, SequenceData } from "$shared";

/**
 * Coordination service for the Construct section within the Build module
 * Restored minimal contract based on usages in BuildTabEventService.
 */
export interface IBuildConstructSectionCoordinator {
  setupComponentCoordination(components: Record<string, unknown>): void;
  handleSequenceModified(sequence: SequenceData): Promise<void>;
  handleStartPositionSet(startPosition: BeatData): Promise<void>;
  handleBeatAdded(beatData: BeatData): Promise<void>;
  handleGenerationRequest(config: Record<string, unknown>): Promise<void>;
  handleUITransitionRequest(targetPanel: string): Promise<void>;
}
