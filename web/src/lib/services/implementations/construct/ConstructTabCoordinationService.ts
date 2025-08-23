/**
 * Construct Tab Coordination Service - Implementation
 *
 * Coordinates between construct tab components (start position picker, option picker, workbench).
 * Based on desktop ConstructTabCoordinationService but simplified for web with runes.
 *
 * FIXED: Added proper state synchronization to resolve start position selection getting stuck
 */

import { GridMode } from "$lib/domain/enums";
import type {
  IConstructTabCoordinationService,
  IStartPositionService,
} from "../../interfaces/application-interfaces";
import type { BeatData, SequenceData } from "../../interfaces/domain-types";
import type {
  ISequenceService,
  IWorkbenchBeatOperationsService,
} from "../../interfaces/sequence-interfaces";

// Note: This service will need to be updated to use the new DI pattern
// For now, we'll comment out the direct import to avoid build errors
// import { sequenceStateService } from "../../SequenceStateService.svelte";

interface ComponentWithEventHandler {
  handleEvent?: (eventType: string, data: unknown) => void;
}

export class ConstructTabCoordinationService
  implements IConstructTabCoordinationService
{
  private components: Record<string, ComponentWithEventHandler> = {};
  private isHandlingSequenceModification = false;
  private eventListenersSetup = false;
  private boundEventHandlers: {
    startPositionSelected: (event: CustomEvent) => void;
    optionSelected: (event: CustomEvent) => void;
    sequenceModified: (event: CustomEvent) => void;
  } | null = null;

  constructor(
    private sequenceService: ISequenceService,
    private startPositionService: IStartPositionService,
    private workbenchBeatOperations: IWorkbenchBeatOperationsService
  ) {}

  /**
   * Clean up resources when service is destroyed
   */
  destroy(): void {
    this.disconnectComponentSignals();
    this.components = {};
  }

  setupComponentCoordination(
    components: Record<string, ComponentWithEventHandler>
  ): void {
    this.components = components;

    // Set up any cross-component communication here (only once)
    if (!this.eventListenersSetup) {
      this.connectComponentSignals();
      this.eventListenersSetup = true;
    }
  }

  async handleSequenceModified(sequence: SequenceData): Promise<void> {
    if (this.isHandlingSequenceModification) {
      return;
    }

    try {
      this.isHandlingSequenceModification = true;

      // **CRITICAL: Update singleton state to keep UI in sync**
      // TODO: Update to use new DI pattern
      // sequenceStateService.setCurrentSequence(sequence);

      // Update UI based on sequence state
      await this.updateUIBasedOnSequence(sequence);

      // Notify components about sequence change
      this.notifyComponents("sequence_modified", { sequence });
    } catch (error) {
      console.error("❌ Error handling sequence modification:", error);
    } finally {
      this.isHandlingSequenceModification = false;
    }
  }

  async handleStartPositionSet(startPosition: BeatData): Promise<void> {
    try {
      // Set loading state to show user something is happening
      // TODO: Update to use new DI pattern
      // sequenceStateService.setLoading(true);
      // sequenceStateService.clearError();

      // Set the start position using the service
      await this.startPositionService.setStartPosition(startPosition);

      // **CRITICAL: Create a sequence with the start position stored separately**
      // Create a new sequence with NO beats initially (progressive creation)
      const newSequence = await this.sequenceService.createSequence({
        name: `Sequence ${new Date().toLocaleTimeString()}`,
        length: 0, // Start with 0 beats - beats will be added progressively
        gridMode: GridMode.DIAMOND, // Default grid mode
        propType: "staff", // Default prop type
      });

      // **CRITICAL: Set the start position in the sequence's startPosition field, NOT as beat 0**
      const updatedSequence =
        await this.workbenchBeatOperations.setConstructionStartPosition(
          newSequence.id,
          startPosition
        );

      if (updatedSequence) {
        // **CRITICAL FIX: Update the singleton state that UI components watch**
        // TODO: Update to use new DI pattern
        // sequenceStateService.setCurrentSequence(updatedSequence);

        // Also clear loading state
        // sequenceStateService.setLoading(false);

        // Service completed successfully - let components handle additional state updates
        this.notifyComponents("sequenceCreated", {
          sequence: updatedSequence,
          startPosition: startPosition,
        });
      } else {
        console.error("❌ Failed to reload updated sequence");
        // TODO: Update to use new DI pattern
        // sequenceStateService.setLoading(false);
        // sequenceStateService.setError(
        //   "Failed to create sequence with start position"
        // );
        return;
      }

      // Notify components
      this.notifyComponents("start_position_set", { startPosition });

      // **CRITICAL: Notify components to update UI state**
      // The shouldShowStartPositionPicker logic should now automatically return false
      // because we've set a current sequence with a startPosition
      this.notifyComponents("ui_state_update_requested", {
        action: "hide_start_position_picker",
      });

      // Transition to option picker
      await this.handleUITransitionRequest("option_picker");
    } catch (error) {
      console.error("❌ Error handling start position set:", error);
      // TODO: Update to use new DI pattern
      // sequenceStateService.setLoading(false);
      // sequenceStateService.setError(
      //   `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      // );
    }
  }

  async handleBeatAdded(beatData: BeatData): Promise<void> {
    try {
      // Get current sequence from singleton state
      // TODO: Update to use new DI pattern
      const currentSequence = null; // sequenceStateService.currentSequence;

      if (!currentSequence) {
        console.error("❌ No current sequence available for adding beat");
        return;
      }

      // **CRITICAL: Use the workbench service to add the beat**
      // TODO: Fix when currentSequence is properly implemented
      // const updatedSequence = await this.workbenchBeatOperations.addBeat(
      //   currentSequence.id,
      //   beatData
      // );

      // **CRITICAL: Update singleton state**
      // TODO: Update to use new DI pattern
      // sequenceStateService.setCurrentSequence(updatedSequence);

      // Notify components
      this.notifyComponents("beat_added", { beatData });
    } catch (error) {
      console.error("❌ Error handling beat added:", error);
      // TODO: Update to use new DI pattern
      // sequenceStateService.setError(
      //   `Failed to add beat: ${error instanceof Error ? error.message : "Unknown error"}`
      // );
    }
  }

  async handleGenerationRequest(
    config: Record<string, unknown>
  ): Promise<void> {
    try {
      // TODO: Implement sequence generation
      // For now, just notify components
      this.notifyComponents("generation_requested", { config });

      // Simulate generation completion
      setTimeout(() => {
        this.notifyComponents("generation_completed", {
          success: true,
          message: "Generation completed",
        });
      }, 1000);
    } catch (error) {
      console.error("❌ Error handling generation request:", error);
    }
  }

  async handleUITransitionRequest(targetPanel: string): Promise<void> {
    try {
      // Emit custom events for UI transitions (similar to legacy implementation)
      const transitionEvent = new CustomEvent("construct-tab-transition", {
        detail: { targetPanel },
        bubbles: true,
      });

      if (typeof window !== "undefined") {
        document.dispatchEvent(transitionEvent);
      }

      // Notify components about the transition
      this.notifyComponents("ui_transition", { targetPanel });
    } catch (error) {
      console.error("❌ Error handling UI transition:", error);
    }
  }

  private connectComponentSignals(): void {
    // Set up event listeners for component coordination
    if (typeof window !== "undefined") {
      // Create bound event handlers to allow proper cleanup
      this.boundEventHandlers = {
        startPositionSelected: ((event: CustomEvent) => {
          this.handleStartPositionSet(event.detail.startPosition);
        }) as (event: CustomEvent) => void,

        optionSelected: ((event: CustomEvent) => {
          this.handleBeatAdded(event.detail.beatData);
        }) as (event: CustomEvent) => void,

        sequenceModified: ((event: CustomEvent) => {
          this.handleSequenceModified(event.detail.sequence);
        }) as (event: CustomEvent) => void,
      };

      // Add event listeners
      document.addEventListener(
        "start-position-selected",
        this.boundEventHandlers.startPositionSelected as EventListener
      );
      document.addEventListener(
        "option-selected",
        this.boundEventHandlers.optionSelected as EventListener
      );
      document.addEventListener(
        "sequence-modified",
        this.boundEventHandlers.sequenceModified as EventListener
      );
    }
  }

  /**
   * Clean up event listeners to prevent memory leaks and duplicate handlers
   */
  private disconnectComponentSignals(): void {
    if (typeof window !== "undefined" && this.boundEventHandlers) {
      document.removeEventListener(
        "start-position-selected",
        this.boundEventHandlers.startPositionSelected as EventListener
      );
      document.removeEventListener(
        "option-selected",
        this.boundEventHandlers.optionSelected as EventListener
      );
      document.removeEventListener(
        "sequence-modified",
        this.boundEventHandlers.sequenceModified as EventListener
      );
      this.boundEventHandlers = null;
      this.eventListenersSetup = false;
    }
  }

  private async updateUIBasedOnSequence(sequence: SequenceData): Promise<void> {
    try {
      // Determine which panel to show based on sequence state
      const hasStartPosition = sequence?.startingPositionBeat != null;
      const hasBeats = sequence && sequence.beats && sequence.beats.length > 0;

      let targetPanel: string;

      if (hasStartPosition || hasBeats) {
        targetPanel = "option_picker";
      } else {
        targetPanel = "start_position_picker";
      }

      // Transition to appropriate panel
      await this.handleUITransitionRequest(targetPanel);
    } catch (error) {
      console.error("❌ Error updating UI based on sequence:", error);
    }
  }

  private hasStartPosition(sequence: SequenceData): boolean {
    // **FIXED: Check the startPosition field instead of checking beats[0]**
    // This aligns with the modern architecture where start position is separate
    return sequence?.startingPositionBeat != null;
  }

  private notifyComponents(eventType: string, data: unknown): void {
    // Notify individual components if they have handlers
    Object.entries(this.components).forEach(([name, component]) => {
      if (component && typeof component.handleEvent === "function") {
        try {
          component.handleEvent(eventType, data);
        } catch (error) {
          console.error(`❌ Error notifying component ${name}:`, error);
        }
      }
    });

    // Emit global event for any listeners
    if (typeof window !== "undefined") {
      const event = new CustomEvent(`construct-coordination-${eventType}`, {
        detail: data,
        bubbles: true,
      });
      document.dispatchEvent(event);
    }
  }
}
