<!-- src/lib/constructor/ConstructTab.svelte -->
<script lang="ts">
	import SharedWorkbench from './SequenceWorkbench/SharedWorkbench.svelte';
	import { workbenchStore } from './state/stores/workbenchStore.js';
	import type { ButtonDefinition } from './SequenceWorkbench/ButtonPanel/types.js';
	import { openSequenceFullScreen } from './stores/sequence/fullScreenStore.js';
	import { sequenceActions } from './state/machines/sequenceMachine/index.js';
	import { sequenceContainer } from './state/stores/sequence/SequenceContainer.js';
	import { renderSequence, downloadSequenceImage } from './SequenceWorkbench/share/utils/ShareUtils.js';
	import { BEAT_FRAME_CONTEXT_KEY, type ElementContext } from './SequenceWorkbench/context/ElementContext.js';
	import { showSuccess, showError, showInfo } from './components/shared/ToastManager.svelte.js';
	import hapticFeedbackService from './services/HapticFeedbackService.js';
	import { getContext } from 'svelte';
	import { browser } from '$app/environment';

	// Props
	export let isGenerateMode = false;

	// Get beat frame context for image operations
	const beatFrameContext = getContext<ElementContext>(BEAT_FRAME_CONTEXT_KEY);

	// Define Button Panel Data
	const buttonPanelButtons: ButtonDefinition[] = [
		{
			icon: 'fa-book-medical',
			title: 'Add to Dictionary',
			id: 'addToDictionary',
			color: '#4361ee'
		},
		{ icon: 'fa-save', title: 'Save Image', id: 'saveImage', color: '#3a86ff' },
		{
			icon: 'fa-expand',
			title: 'View Sequence Full Screen',
			id: 'viewFullScreen',
			color: '#4cc9f0'
		},
		{
			icon: 'fa-arrows-left-right',
			title: 'Mirror Sequence',
			id: 'mirrorSequence',
			color: '#4895ef'
		},
		{ icon: 'fa-paintbrush', title: 'Swap Colors', id: 'swapColors', color: '#ff6b6b' },
		{ icon: 'fa-rotate', title: 'Rotate Sequence', id: 'rotateSequence', color: '#f72585' },
		{ icon: 'fa-trash', title: 'Delete Beat', id: 'deleteBeat', color: '#ff9e00' },
		{ icon: 'fa-eraser', title: 'Clear Sequence', id: 'clearSequence', color: '#ff7b00' }
	];

	// Helper function to generate sequence name from beats
	function generateSequenceName(beats: any[]): string {
		if (!beats || beats.length === 0) return 'Sequence';

		// Extract letters from beats
		const letters = beats
			.map((beat) => ((beat.letter || beat.metadata?.letter) as string) || '')
			.filter((letter) => letter.trim() !== '')
			.join('');

		return letters || 'Sequence';
	}

	// Helper function to transform sequence for mirroring
	function mirrorSequenceData(beats: any[]): any[] {
		return beats.map((beat) => {
			const mirrored = { ...beat };

			// Mirror red prop location (swap left/right)
			if (mirrored.redMotionData?.startLoc?.side) {
				mirrored.redMotionData.startLoc.side =
					mirrored.redMotionData.startLoc.side === 'L' ? 'R' : 'L';
			}
			if (mirrored.redMotionData?.endLoc?.side) {
				mirrored.redMotionData.endLoc.side =
					mirrored.redMotionData.endLoc.side === 'L' ? 'R' : 'L';
			}

			// Mirror blue prop location (swap left/right)
			if (mirrored.blueMotionData?.startLoc?.side) {
				mirrored.blueMotionData.startLoc.side =
					mirrored.blueMotionData.startLoc.side === 'L' ? 'R' : 'L';
			}
			if (mirrored.blueMotionData?.endLoc?.side) {
				mirrored.blueMotionData.endLoc.side =
					mirrored.blueMotionData.endLoc.side === 'L' ? 'R' : 'L';
			}

			return mirrored;
		});
	}

	// Helper function to transform sequence for rotation
	function rotateSequenceData(beats: any[]): any[] {
		return beats.map((beat) => {
			const rotated = { ...beat };

			// Rotate orientations by 90 degrees
			if (rotated.redMotionData?.startOri !== undefined) {
				rotated.redMotionData.startOri = (rotated.redMotionData.startOri + 90) % 360;
			}
			if (rotated.redMotionData?.endOri !== undefined) {
				rotated.redMotionData.endOri = (rotated.redMotionData.endOri + 90) % 360;
			}
			if (rotated.blueMotionData?.startOri !== undefined) {
				rotated.blueMotionData.startOri = (rotated.blueMotionData.startOri + 90) % 360;
			}
			if (rotated.blueMotionData?.endOri !== undefined) {
				rotated.blueMotionData.endOri = (rotated.blueMotionData.endOri + 90) % 360;
			}

			return rotated;
		});
	}

	// Helper function to swap red and blue colors in sequence
	function swapSequenceColors(beats: any[]): any[] {
		return beats.map((beat) => {
			const swapped = { ...beat };

			// Swap red and blue motion data
			const tempRed = swapped.redMotionData;
			swapped.redMotionData = swapped.blueMotionData;
			swapped.blueMotionData = tempRed;

			return swapped;
		});
	}

	// Handler for button panel actions
	async function handleButtonAction(id: string) {
		// Provide haptic feedback for all actions
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		console.log(`Handling button action: ${id}`);

		// Handle specific actions based on the button ID
		switch (id) {
			case 'viewFullScreen':
				// Use the fullScreenStore to open the fullscreen overlay
				openSequenceFullScreen();
				if (browser && hapticFeedbackService.isAvailable()) {
					hapticFeedbackService.trigger('navigation');
				}
				break;

			case 'constructMode':
				workbenchStore.update((state) => ({ ...state, activeTab: 'construct' }));
				if (browser && hapticFeedbackService.isAvailable()) {
					hapticFeedbackService.trigger('navigation');
				}
				break;

			case 'generateMode':
				workbenchStore.update((state) => ({ ...state, activeTab: 'generate' }));
				if (browser && hapticFeedbackService.isAvailable()) {
					hapticFeedbackService.trigger('navigation');
				}
				break;

			case 'saveImage':
				try {
					const sequence = sequenceContainer.state;
					const beats = sequence.beats || [];

					if (beats.length === 0) {
						showError('No sequence to save');
						return;
					}

					const sequenceName = generateSequenceName(beats);
					const beatFrameElement = beatFrameContext?.getElement();

					// Render the sequence to an image
					const result = await renderSequence({
						sequenceName,
						sequenceBeats: beats,
						difficultyLevel: sequence.metadata?.difficulty || 1,
						beatFrameElement
					});

					if (!result) {
						showError('Failed to generate image');
						return;
					}

					// Download the image
					const downloadResult = await downloadSequenceImage({
						sequenceName,
						imageResult: result
					});

					if (downloadResult && browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('success');
					}
				} catch (error) {
					console.error('Error saving image:', error);
					showError('Failed to save image');
				}
				break;

			case 'addToDictionary':
				try {
					const sequence = sequenceContainer.state;
					const beats = sequence.beats || [];

					if (beats.length === 0) {
						showError('No sequence to add to dictionary');
						return;
					}

					const sequenceName = generateSequenceName(beats);

					// Save to localStorage dictionary
					const existingDictionary = JSON.parse(localStorage.getItem('sequence_dictionary') || '[]');
					const newEntry = {
						id: crypto.randomUUID(),
						name: sequenceName,
						beats: beats,
						difficulty: sequence.metadata?.difficulty || 1,
						dateAdded: new Date().toISOString(),
						tags: sequence.metadata?.tags || []
					};

					existingDictionary.push(newEntry);
					localStorage.setItem('sequence_dictionary', JSON.stringify(existingDictionary));

					showSuccess(`"${sequenceName}" added to dictionary`);
					if (browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('success');
					}
				} catch (error) {
					console.error('Error adding to dictionary:', error);
					showError('Failed to add to dictionary');
				}
				break;

			case 'mirrorSequence':
				try {
					const sequence = sequenceContainer.state;
					const beats = sequence.beats || [];

					if (beats.length === 0) {
						showError('No sequence to mirror');
						return;
					}

					const mirroredBeats = mirrorSequenceData(beats);
					sequenceContainer.setSequence(mirroredBeats);

					showSuccess('Sequence mirrored');
					if (browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('success');
					}
				} catch (error) {
					console.error('Error mirroring sequence:', error);
					showError('Failed to mirror sequence');
				}
				break;

			case 'swapColors':
				try {
					const sequence = sequenceContainer.state;
					const beats = sequence.beats || [];

					if (beats.length === 0) {
						showError('No sequence to swap colors');
						return;
					}

					const swappedBeats = swapSequenceColors(beats);
					sequenceContainer.setSequence(swappedBeats);

					showSuccess('Colors swapped');
					if (browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('success');
					}
				} catch (error) {
					console.error('Error swapping colors:', error);
					showError('Failed to swap colors');
				}
				break;

			case 'rotateSequence':
				try {
					const sequence = sequenceContainer.state;
					const beats = sequence.beats || [];

					if (beats.length === 0) {
						showError('No sequence to rotate');
						return;
					}

					const rotatedBeats = rotateSequenceData(beats);
					sequenceContainer.setSequence(rotatedBeats);

					showSuccess('Sequence rotated');
					if (browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('success');
					}
				} catch (error) {
					console.error('Error rotating sequence:', error);
					showError('Failed to rotate sequence');
				}
				break;

			case 'deleteBeat':
				try {
					const selectedBeatIds = sequenceContainer.state.selectedBeatIds;
					if (selectedBeatIds.length > 0) {
						sequenceActions.removeBeatAndFollowing({
							event: { type: 'REMOVE_BEAT_AND_FOLLOWING', beatId: selectedBeatIds[0] }
						});
						showSuccess('Beat deleted');
						if (browser && hapticFeedbackService.isAvailable()) {
							hapticFeedbackService.trigger('warning');
						}
					} else {
						showError('No beat selected to delete');
					}
				} catch (error) {
					console.error('Error deleting beat:', error);
					showError('Failed to delete beat');
				}
				break;

			case 'clearSequence':
				try {
					sequenceActions.clearSequence();
					showSuccess('Sequence cleared');
					if (browser && hapticFeedbackService.isAvailable()) {
						hapticFeedbackService.trigger('error');
					}
				} catch (error) {
					console.error('Error clearing sequence:', error);
					showError('Failed to clear sequence');
				}
				break;

			default:
				console.log(`Unhandled action: ${id}`);
				break;
		}
	}

	// Set active tab when component mounts
	$: workbenchStore.update((state) => ({
		...state,
		activeTab: isGenerateMode ? 'generate' : 'construct'
	}));
</script>

<div class="construct-tab">
	<SharedWorkbench toolsPanelButtons={buttonPanelButtons} onToolsPanelAction={handleButtonAction} />
</div>

<style>
	.construct-tab {
		display: flex;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	@media (max-width: 768px) {
		.construct-tab {
			flex-direction: column;
		}
	}
</style>
