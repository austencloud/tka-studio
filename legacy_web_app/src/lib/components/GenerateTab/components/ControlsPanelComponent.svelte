<!-- src/lib/components/GenerateTab/layout/ControlsPanelComponent.svelte -->
<script lang="ts">
	import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';
	import { settingsStore as newSettingsStore } from '$lib/state/stores/settingsStore';
	import {
		settingsStore,
		numBeats,
		turnIntensity,
		propContinuity,
		capType,
		level
	} from '../store/settings';

	import GeneratorTypeSection from '../controls/GeneratorTypeSection.svelte';
	import ParametersSection from '../controls/ParametersSection.svelte';
	import GeneratorOptionsSection from '../controls/GeneratorOptionsSection.svelte';
	import GenerateButtonSection from '../controls/GenerateButtonSection.svelte';

	// Use both old and new state management during migration
	export let useNewStateManagement = true;

	// Generator types for the toggle
	const generatorTypes = [
		{ id: 'circular', label: 'Circular' },
		{ id: 'freeform', label: 'Freeform' }
	];

	// Handle generate click
	function handleGenerate() {
		if (useNewStateManagement) {
			// New implementation using sequence machine
			// Get current settings from the store values
			const settings = {
				numBeats: $numBeats,
				turnIntensity: $turnIntensity,
				propContinuity: $propContinuity,
				capType: $capType,
				level: $level
			};

			// Use the sequence machine to generate the sequence - pass generatorType first, then settings
			sequenceActions.generate($settingsStore.generatorType, settings);
		} else {
			// Current implementation using event dispatch
			const event = new CustomEvent('generate-sequence', {
				detail: {
					// We could pass additional options here if needed
				}
			});

			document.dispatchEvent(event);
		}
	}
</script>

<div class="controls-panel">
	<GeneratorTypeSection {generatorTypes} {useNewStateManagement} />
	<ParametersSection />
	<GeneratorOptionsSection {useNewStateManagement} />
	<GenerateButtonSection {useNewStateManagement} onGenerateClick={handleGenerate} />
</div>

<style>
	.controls-panel {
		display: flex;
		flex-direction: column;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.5));
		border-radius: 0.75rem;
		box-shadow:
			0 4px 12px rgba(0, 0, 0, 0.2),
			0 0 0 1px rgba(255, 255, 255, 0.05);
		overflow: hidden;
		transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		flex: 1;
		max-width: 400px;
		overflow-y: auto;
		animation: fadeIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		animation-delay: 0.2s;
	}

	.controls-panel:hover {
		box-shadow:
			0 8px 24px rgba(0, 0, 0, 0.3),
			0 0 0 1px rgba(255, 255, 255, 0.1);
		transform: translateY(-2px);
	}

	/* Animation for panel transitions */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
			filter: blur(5px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
			filter: blur(0);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.controls-panel {
			max-width: none;
			transition:
				transform 0.3s ease,
				box-shadow 0.3s ease;
		}

		.controls-panel:hover {
			transform: translateY(-4px);
		}
	}
</style>
