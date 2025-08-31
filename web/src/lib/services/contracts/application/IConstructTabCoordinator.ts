/**
 * Construct Tab Coordination Service Interface
 *
 * Interface for coordinating construct tab operations.
 * Handles communication between different construct tab components.
 */

import type { BeatData, SequenceData } from "$domain";

export interface IConstructTabCoordinator {
  setupComponentCoordination(components: Record<string, unknown>): void;
  handleSequenceModified(sequence: SequenceData): Promise<void>;
  handleStartPositionSet(startPosition: BeatData): Promise<void>;
  handleBeatAdded(beatData: BeatData): Promise<void>;
  handleGenerationRequest(config: Record<string, unknown>): Promise<void>;
  handleUITransitionRequest(targetPanel: string): Promise<void>;
}
