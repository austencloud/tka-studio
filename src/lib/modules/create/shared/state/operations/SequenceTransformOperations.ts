/**
 * Sequence Transform Operations
 *
 * Handles sequence-level transformations:
 * - Mirror sequence
 * - Swap colors
 * - Rotate sequence
 * - Duplicate sequence
 * - Set start position
 * - Validation
 *
 * RESPONSIBILITY: Transform operations coordinator, orchestrates state + services
 */

import type { BeatData, SequenceData, ValidationResult } from "$shared";
import { updateSequenceData } from "$shared";
import type { ISequenceStatisticsService } from "../../services/contracts/ISequenceStatisticsService";
import type { ISequenceTransformationService } from "../../services/contracts/ISequenceTransformationService";
import type { ISequenceValidationService } from "../../services/contracts/ISequenceValidationService";
import type { SequenceCoreState } from "../core/SequenceCoreState.svelte";
import type { SequenceSelectionState } from "../selection/SequenceSelectionState.svelte";

export interface TransformOperationsConfig {
  coreState: SequenceCoreState;
  selectionState: SequenceSelectionState;
  sequenceStatisticsService?: ISequenceStatisticsService | null;
  sequenceTransformationService?: ISequenceTransformationService | null;
  sequenceValidationService?: ISequenceValidationService | null;
  onError?: (error: string) => void;
  onSave?: () => Promise<void>;
}

export function createSequenceTransformOperations(
  config: TransformOperationsConfig
) {
  const {
    coreState,
    selectionState,
    sequenceStatisticsService,
    sequenceTransformationService,
    sequenceValidationService,
    onError,
    onSave,
  } = config;

  function handleError(message: string, error?: unknown) {
    const errorMsg = error instanceof Error ? error.message : message;
    coreState.setError(errorMsg);
    onError?.(errorMsg);
    console.error(message, error);
  }

  return {
    setStartPosition(startPosition: BeatData) {
      if (!coreState.currentSequence) return;

      try {
        // Update sequence with start position - set both fields for compatibility
        const updatedSequence = updateSequenceData(coreState.currentSequence, {
          startPosition: startPosition,
          startingPositionBeat: startPosition, // CRITICAL: Set both fields for compatibility
        });

        coreState.setCurrentSequence(updatedSequence);
        selectionState.setStartPosition(startPosition);
        console.log(
          "✅ Transform: Updated hasStartPosition to true (setStartPosition called)"
        );
        coreState.clearError();
      } catch (error) {
        handleError("Failed to set start position", error);
      }
    },

    async mirrorSequence() {
      if (!coreState.currentSequence || !sequenceTransformationService) return;

      try {
        const updatedSequence = sequenceTransformationService.mirrorSequence(
          coreState.currentSequence
        );
        coreState.setCurrentSequence(updatedSequence);

        // Update selection state with transformed start position so UI re-renders
        if (updatedSequence.startPosition) {
          selectionState.setStartPosition(updatedSequence.startPosition);
        }

        coreState.clearError();

        // Persist the transformed sequence
        await onSave?.();
      } catch (error) {
        handleError("Failed to mirror sequence", error);
      }
    },

    async swapColors() {
      if (!coreState.currentSequence || !sequenceTransformationService) return;

      try {
        const updatedSequence = sequenceTransformationService.swapColors(
          coreState.currentSequence
        );
        coreState.setCurrentSequence(updatedSequence);

        // Update selection state with transformed start position so UI re-renders
        if (updatedSequence.startPosition) {
          selectionState.setStartPosition(updatedSequence.startPosition);
        }

        coreState.clearError();

        // Persist the transformed sequence
        await onSave?.();
      } catch (error) {
        handleError("Failed to swap colors", error);
      }
    },

    async rotateSequence(direction: "clockwise" | "counterclockwise") {
      if (!coreState.currentSequence || !sequenceTransformationService) return;

      try {
        const rotationAmount = direction === "clockwise" ? 1 : -1;
        const updatedSequence = sequenceTransformationService.rotateSequence(
          coreState.currentSequence,
          rotationAmount
        );
        coreState.setCurrentSequence(updatedSequence);

        // Update selection state with transformed start position so UI re-renders
        if (updatedSequence.startPosition) {
          selectionState.setStartPosition(updatedSequence.startPosition);
        }

        coreState.clearError();

        // Persist the transformed sequence
        await onSave?.();
      } catch (error) {
        handleError("Failed to rotate sequence", error);
      }
    },

    duplicateSequence(newName?: string): SequenceData | null {
      if (!coreState.currentSequence || !sequenceTransformationService)
        return null;

      try {
        const duplicated = sequenceTransformationService.duplicateSequence(
          coreState.currentSequence,
          newName
        );
        coreState.clearError();
        return duplicated;
      } catch (error) {
        handleError("Failed to duplicate sequence", error);
        return null;
      }
    },

    async reverseSequence() {
      if (!coreState.currentSequence || !sequenceTransformationService) return;

      try {
        const reversedSequence = await sequenceTransformationService.reverseSequence(
          coreState.currentSequence
        );
        coreState.setCurrentSequence(reversedSequence);

        // Update selection state with new start position so UI re-renders
        if (reversedSequence.startPosition) {
          selectionState.setStartPosition(reversedSequence.startPosition);
        }

        coreState.clearError();

        // Persist the transformed sequence
        await onSave?.();
      } catch (error) {
        handleError("Failed to reverse sequence", error);
      }
    },

    validateSequence(): ValidationResult | null {
      if (!coreState.currentSequence || !sequenceValidationService) return null;
      return sequenceValidationService.validateSequence(
        coreState.currentSequence
      );
    },

    getSequenceStatistics() {
      if (!coreState.currentSequence || !sequenceStatisticsService) return null;
      return sequenceStatisticsService.getSequenceStatistics(
        coreState.currentSequence
      );
    },

    generateSequenceWord(): string {
      if (!coreState.currentSequence || !sequenceStatisticsService) {
        return "";
      }
      return sequenceStatisticsService.generateSequenceWord(
        coreState.currentSequence
      );
    },

    calculateSequenceDuration(): number {
      if (!coreState.currentSequence || !sequenceStatisticsService) return 0;
      return sequenceStatisticsService.calculateSequenceDuration(
        coreState.currentSequence
      );
    },
  };
}

export type SequenceTransformOperations = ReturnType<
  typeof createSequenceTransformOperations
>;
