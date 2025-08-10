/**
 * Construct Tab Coordination Service - Implementation
 *
 * Coordinates between construct tab components (start position picker, option picker, workbench).
 * Based on desktop ConstructTabCoordinationService but simplified for web with runes.
 */

import { createSequence } from '$stores/sequenceActions';
import { setCurrentSequence } from '$stores/sequenceState.svelte';
import { resolve } from '../bootstrap';
import type {
	BeatData,
	IConstructTabCoordinationService,
	IOptionDataService,
	ISequenceService,
	IStartPositionService,
	SequenceData,
} from '../interfaces';
import { sequenceStateService } from '../SequenceStateService.svelte';

export class ConstructTabCoordinationService implements IConstructTabCoordinationService {
	private components: Record<string, any> = {};
	private isHandlingSequenceModification = false;

	constructor(
		private sequenceService: ISequenceService,
		private startPositionService: IStartPositionService,
		private optionDataService: IOptionDataService
	) {
		console.log('🎭 ConstructTabCoordinationService initialized');
	}

	setupComponentCoordination(components: Record<string, any>): void {
		console.log('🎭 Setting up component coordination:', Object.keys(components));
		this.components = components;

		// Set up any cross-component communication here
		this.connectComponentSignals();
	}

	async handleSequenceModified(sequence: SequenceData): Promise<void> {
		if (this.isHandlingSequenceModification) {
			return;
		}

		console.log('🎭 Handling sequence modification:', sequence.id);

		try {
			this.isHandlingSequenceModification = true;

			// Update UI based on sequence state
			await this.updateUIBasedOnSequence(sequence);

			// Notify components about sequence change
			this.notifyComponents('sequence_modified', { sequence });
		} catch (error) {
			console.error('❌ Error handling sequence modification:', error);
		} finally {
			this.isHandlingSequenceModification = false;
		}
	}

	async handleStartPositionSet(startPosition: BeatData): Promise<void> {
		console.log('🎭 Handling start position set:', startPosition.pictograph_data?.id);

		try {
			// Set the start position using the service
			await this.startPositionService.setStartPosition(startPosition);

			// **CRITICAL: Create a sequence with the start position stored separately**
			console.log('🎭 Creating sequence with start position stored separately from beats');
			const sequenceService = resolve('ISequenceService');

			// Create a new sequence with NO beats initially (progressive creation)
			const newSequence = await createSequence(sequenceService, {
				name: `Sequence ${new Date().toLocaleTimeString()}`,
				length: 0, // Start with 0 beats - beats will be added progressively
				gridMode: 'diamond', // Default grid mode
				propType: 'staff', // Default prop type
			});

			// **CRITICAL: Set the start position in the sequence's start_position field, NOT as beat 0**
			console.log('🎭 Setting start position in sequence.start_position field');
			await sequenceService.setSequenceStartPosition(newSequence.id, startPosition);

			// **CRITICAL: Reload the sequence to get the updated start position**
			const updatedSequence = await sequenceService.getSequence(newSequence.id);
			if (updatedSequence) {
				// Set the updated sequence as the current sequence in BOTH state systems
				setCurrentSequence(updatedSequence); // Old sequence state system
				sequenceStateService.setCurrentSequence(updatedSequence); // New sequence state service for beat frame
				console.log(
					'🎯 Set updated sequence as current sequence:',
					updatedSequence.id,
					'beats:',
					updatedSequence.beats.length,
					'start_position:',
					updatedSequence.start_position?.pictograph_data?.id
				);
				console.log(
					'🎯 Updated both sequence state systems for beat frame synchronization'
				);
			} else {
				console.error('❌ Failed to reload updated sequence');
			}

			console.log('✅ Sequence created with start position stored separately');

			// Notify components
			this.notifyComponents('start_position_set', { startPosition });

			// **CRITICAL: Update construct tab state to hide start position picker**
			const { constructTabState } = await import('$stores/constructTabState.svelte');
			constructTabState.updateShouldShowStartPositionPicker();
			console.log('🎭 Updated construct tab state to show option picker');

			// Transition to option picker
			await this.handleUITransitionRequest('option_picker');
		} catch (error) {
			console.error('❌ Error handling start position set:', error);
		}
	}

	async handleBeatAdded(beatData: BeatData): Promise<void> {
		console.log('🎭 Handling beat added:', beatData.beat_number);

		try {
			const sequenceService = resolve('ISequenceService');
			const sequenceStateService = resolve('SequenceStateService');

			// Get current sequence from state
			const currentSequence = sequenceStateService.currentSequence;
			if (!currentSequence) {
				console.error('❌ No current sequence available for beat addition');
				return;
			}

			console.log('🎭 Adding beat to sequence:', currentSequence.id);

			// Add beat to sequence using service
			await sequenceService.addBeat(currentSequence.id, beatData);

			// Reload the sequence to get the updated version
			const updatedSequence = await sequenceService.getSequence(currentSequence.id);
			if (updatedSequence) {
				// Update both state systems
				setCurrentSequence(updatedSequence); // Old sequence state system
				sequenceStateService.setCurrentSequence(updatedSequence); // New sequence state service
				console.log(
					'🎯 Updated sequence with new beat:',
					updatedSequence.id,
					'beats:',
					updatedSequence.beats.length
				);
			}

			// Notify components
			this.notifyComponents('beat_added', { beatData });

			console.log('✅ Beat added successfully');
		} catch (error) {
			console.error('❌ Error handling beat added:', error);
		}
	}

	async handleGenerationRequest(config: any): Promise<void> {
		console.log('🎭 Handling generation request:', config);

		try {
			// TODO: Implement sequence generation
			// For now, just notify components
			this.notifyComponents('generation_requested', { config });

			// Simulate generation completion
			setTimeout(() => {
				this.notifyComponents('generation_completed', {
					success: true,
					message: 'Generation completed',
				});
			}, 1000);
		} catch (error) {
			console.error('❌ Error handling generation request:', error);
		}
	}

	async handleUITransitionRequest(targetPanel: string): Promise<void> {
		console.log('🎭 Handling UI transition request to:', targetPanel);

		try {
			// Emit custom events for UI transitions (similar to legacy implementation)
			const transitionEvent = new CustomEvent('construct-tab-transition', {
				detail: { targetPanel },
				bubbles: true,
			});

			if (typeof window !== 'undefined') {
				document.dispatchEvent(transitionEvent);
			}

			// Notify components about the transition
			this.notifyComponents('ui_transition', { targetPanel });
		} catch (error) {
			console.error('❌ Error handling UI transition:', error);
		}
	}

	private connectComponentSignals(): void {
		// Set up event listeners for component coordination
		if (typeof window !== 'undefined') {
			// Listen for start position selection
			document.addEventListener('start-position-selected', ((event: CustomEvent) => {
				this.handleStartPositionSet(event.detail.startPosition);
			}) as EventListener);

			// Listen for option selection
			document.addEventListener('option-selected', ((event: CustomEvent) => {
				this.handleBeatAdded(event.detail.beatData);
			}) as EventListener);

			// Listen for sequence modifications
			document.addEventListener('sequence-modified', ((event: CustomEvent) => {
				this.handleSequenceModified(event.detail.sequence);
			}) as EventListener);
		}
	}

	private async updateUIBasedOnSequence(sequence: SequenceData): Promise<void> {
		console.log('🎭 Updating UI based on sequence state');

		try {
			// Determine which panel to show based on sequence state
			const hasStartPosition = this.hasStartPosition(sequence);
			const hasBeats = sequence && sequence.beats && sequence.beats.length > 0;

			let targetPanel: string;

			if (hasStartPosition || hasBeats) {
				targetPanel = 'option_picker';
			} else {
				targetPanel = 'start_position_picker';
			}

			// Transition to appropriate panel
			await this.handleUITransitionRequest(targetPanel);
		} catch (error) {
			console.error('❌ Error updating UI based on sequence:', error);
		}
	}

	private hasStartPosition(sequence: SequenceData): boolean {
		// Check if sequence has a start position
		if (!sequence?.beats || sequence.beats.length === 0) {
			return false;
		}

		const firstBeat = sequence.beats[0];
		return firstBeat?.beat === 0 && !!firstBeat.pictograph_data;
	}

	private notifyComponents(eventType: string, data: any): void {
		console.log(`🎭 Notifying components of ${eventType}:`, data);

		// Notify individual components if they have handlers
		Object.entries(this.components).forEach(([name, component]) => {
			if (component && typeof component.handleEvent === 'function') {
				try {
					component.handleEvent(eventType, data);
				} catch (error) {
					console.error(`❌ Error notifying component ${name}:`, error);
				}
			}
		});

		// Emit global event for any listeners
		if (typeof window !== 'undefined') {
			const event = new CustomEvent(`construct-coordination-${eventType}`, {
				detail: data,
				bubbles: true,
			});
			document.dispatchEvent(event);
		}
	}

	private async getCurrentSequence(): Promise<SequenceData | null> {
		try {
			// TODO: Get current sequence from sequence service
			// For now, return null - this would be implemented based on app state
			return null;
		} catch (error) {
			console.error('❌ Error getting current sequence:', error);
			return null;
		}
	}
}
