/**
 * ConstructTab Event Service
 *
 * Centralized event handling for the ConstructTab component.
 * This service handles all the event coordination between different child components
 * that was previously scattered throughout the massive ConstructTab component.
 */

import type { BeatData } from '$domain/BeatData';
import { createBeatData } from '$domain/BeatData';
import type { PictographData } from '$domain/PictographData';
import { getCurrentSequence } from '../../state/sequenceState.svelte';
import {
	clearError,
	// constructTabState,
	setError,
	setTransitioning,
} from '../../stores/constructTabState.svelte';
import { resolve } from '../bootstrap';
import type { IConstructTabCoordinationService } from '../interfaces';

export class ConstructTabEventService {
	private constructCoordinator: IConstructTabCoordinationService | null = null;

	constructor() {
		this.initializeServices();
	}

	private initializeServices() {
		try {
			this.constructCoordinator = resolve('IConstructTabCoordinationService');
		} catch {
			// This is expected during SSR - services will be resolved once client-side DI container is ready
			console.warn(
				'ConstructTabEventService: Services not yet available (expected during SSR)'
			);
			// Services will remain null and methods will handle gracefully
		}
	}

	/**
	 * Handle start position selection in the Build tab
	 */
	async handleStartPositionSelected(startPosition: BeatData): Promise<void> {
		try {
			console.log(
				'🎭 Start position selected in ConstructTabEventService:',
				startPosition.pictograph_data?.id
			);
			// DON'T set transitioning immediately - let the fade transitions handle the UI
			// setTransitioning(true); // ← REMOVED to prevent flash

			// Ensure coordination service is available - retry resolution if needed
			if (!this.constructCoordinator) {
				console.log('🎭 Coordination service not available, attempting to resolve...');
				try {
					this.constructCoordinator = resolve('IConstructTabCoordinationService');
					console.log('✅ Coordination service resolved successfully');
				} catch (resolveError) {
					console.error('❌ Failed to resolve coordination service:', resolveError);
					throw new Error('Coordination service not available');
				}
			}

			// Use coordination service to handle the selection
			if (this.constructCoordinator) {
				console.log('🎭 Calling coordination service handleStartPositionSet...');
				await this.constructCoordinator.handleStartPositionSet(startPosition);
				console.log('✅ Coordination service handleStartPositionSet completed');
			} else {
				throw new Error('Coordination service is null after resolution attempt');
			}

			// Clear any previous errors
			clearError();

			console.log('✅ Transitioned to option picker');
		} catch (error) {
			console.error('❌ Error handling start position selection:', error);
			setError(error instanceof Error ? error.message : 'Failed to set start position');
		} finally {
			// No need to set transitioning to false since we don't set it to true
			// setTransitioning(false); // ← REMOVED to match the removal above
		}
	}

	/**
	 * Handle option selection in the Build tab
	 */
	async handleOptionSelected(option: PictographData): Promise<void> {
		try {
			console.log('🎭 Option selected in ConstructTabEventService:', option.id);
			setTransitioning(true);

			// Create beat data from option
			const beatData = createBeatData({
				beat_number: (getCurrentSequence()?.beats.length || 0) + 1,
				pictograph_data: option,
			});

			// Use coordination service to handle beat addition
			if (this.constructCoordinator) {
				await this.constructCoordinator.handleBeatAdded(beatData);
			}

			// Clear any previous errors
			clearError();

			console.log('✅ Beat added to sequence');
		} catch (error) {
			console.error('❌ Error handling option selection:', error);
			setError(error instanceof Error ? error.message : 'Failed to add option to sequence');
		} finally {
			setTransitioning(false);
		}
	}

	/**
	 * Handle beat modification from the Graph Editor
	 */
	handleBeatModified(beatIndex: number, beatData: BeatData): void {
		console.log('ConstructTabEventService: Beat modified in graph editor', beatIndex, beatData);

		// Handle beat modifications from graph editor
		// Note: The coordination service doesn't have handleBeatModified,
		// so we'll handle this locally or extend the interface if needed
		console.log('Beat modification handled locally for beat index:', beatIndex);
	}

	/**
	 * Handle arrow selection from the Graph Editor
	 */
	handleArrowSelected(arrowData: unknown): void {
		console.log('ConstructTabEventService: Arrow selected in graph editor', arrowData);
		// Handle arrow selection events from graph editor
		// This could be used for highlighting or additional UI feedback
	}

	/**
	 * Handle graph editor visibility changes
	 */
	handleGraphEditorVisibilityChanged(isVisible: boolean): void {
		console.log('ConstructTabEventService: Graph editor visibility changed', isVisible);
		// Handle graph editor visibility changes if needed
	}

	/**
	 * Handle export setting changes from the Export Panel
	 */
	handleExportSettingChanged(event: CustomEvent): void {
		const { setting, value } = event.detail;
		console.log('ConstructTabEventService: Export setting changed', setting, value);
		// Handle export setting changes - could save to settings service
	}

	/**
	 * Handle preview update requests from the Export Panel
	 */
	handlePreviewUpdateRequested(event: CustomEvent): void {
		const settings = event.detail;
		console.log('ConstructTabEventService: Preview update requested', settings);
		// Handle preview update requests
	}

	/**
	 * Handle export requests from the Export Panel
	 */
	handleExportRequested(event: CustomEvent): void {
		const { type, config } = event.detail;
		console.log('ConstructTabEventService: Export requested', type, config);

		// Handle export requests
		if (type === 'current') {
			console.log('Exporting current sequence:', config.sequence?.name);
			// TODO: Implement actual export service call
			alert(
				`Exporting sequence "${config.sequence?.name || 'Untitled'}" with ${config.sequence?.beats?.length || 0} beats`
			);
		} else if (type === 'all') {
			console.log('Exporting all sequences');
			// TODO: Implement actual export all service call
			alert('Exporting all sequences in library');
		}
	}

	/**
	 * Setup component coordination
	 */
	setupComponentCoordination(): void {
		console.log('🎭 ConstructTabEventService setting up coordination');

		// Register this service with the coordination service
		if (this.constructCoordinator) {
			this.constructCoordinator.setupComponentCoordination({
				constructTab: {
					handleEvent: (eventType: string, data: unknown) => {
						switch (eventType) {
							case 'ui_transition':
								// Handle legacy transition events if needed
								break;
							default:
								console.log(
									`ConstructTabEventService received event: ${eventType}`,
									data
								);
						}
					},
				},
			});
		}
	}
}

// Create and export singleton instance
export const constructTabEventService = new ConstructTabEventService();
