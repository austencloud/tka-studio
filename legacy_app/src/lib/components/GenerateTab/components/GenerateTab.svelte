<!-- src/lib/components/GenerateTab/GenerateTab.svelte -->
<script lang="ts">
	// Import state management
	import { onMount } from 'svelte';
	import { settingsStore as newSettingsStore } from '$lib/state/stores/settingsStore';

	// Import existing stores for backward compatibility during migration
	import {
		generatorType as activeGeneratorType,
		numBeats,
		turnIntensity,
		propContinuity,
		capType,
		level
	} from '../store/settings';

	// Import layout components
	import GenerateTabHeader from './GenerateTabHeader.svelte';
	import GenerateTabContent from './GenerateTabContent.svelte';

	// Initialization logic
	onMount(() => {
		// Initialize the sequence machine with the current settings
		console.log('Initializing sequence machine with current settings');

		// Sync the old settings to the new settings store
		newSettingsStore.setGeneratorType($activeGeneratorType);
		newSettingsStore.setNumBeats($numBeats);
		newSettingsStore.setTurnIntensity($turnIntensity);
		newSettingsStore.setPropContinuity($propContinuity);
		newSettingsStore.setCAPType($capType);
		newSettingsStore.setLevel($level);
	});
</script>

<div class="generate-tab">
	<GenerateTabContent />
</div>

<style>
	.generate-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		padding: 1.5rem;
		gap: 1.5rem;
		color: var(--color-text-primary, white);
		position: relative;
		overflow: hidden;
	}

	/* Add subtle background pattern */
	.generate-tab::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-image:
			radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
			radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
		background-size: 40px 40px;
		background-position:
			0 0,
			20px 20px;
		pointer-events: none;
		z-index: 0;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.generate-tab {
			padding: 1rem;
		}
	}
</style>
