<!-- VisibilityTab.svelte - Compact visibility settings with better contrast -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import SettingCard from '../SettingCard.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';

	interface Props {
		settings: any;
	}

	let { settings }: Props = $props();
	const dispatch = createEventDispatcher();

	// Visibility settings - matching desktop defaults
	let visibilitySettings = $state({
		TKA: settings.visibility?.TKA ?? true,
		Reversals: settings.visibility?.Reversals ?? true,
		Positions: settings.visibility?.Positions ?? false,
		Elemental: settings.visibility?.Elemental ?? false,
		VTG: settings.visibility?.VTG ?? false,
		nonRadialPoints: settings.visibility?.nonRadialPoints ?? false,
	});

	function updateVisibilitySetting(key: string, value: boolean) {
		visibilitySettings[key] = value;
		dispatch('update', { key: 'visibility', value: { ...visibilitySettings } });
	}
</script>

<div class="tab-content">
	<SettingCard
		title="Visibility Settings"
		description="Control which elements are shown in pictographs"
	>
		<div class="visibility-grid">
			<ToggleSetting
				label="TKA Notation"
				checked={visibilitySettings.TKA}
				helpText="Movement notation letters"
				on:change={(e) => updateVisibilitySetting('TKA', e.detail)}
			/>

			<ToggleSetting
				label="Reversals"
				checked={visibilitySettings.Reversals}
				helpText="Reversal direction indicators"
				on:change={(e) => updateVisibilitySetting('Reversals', e.detail)}
			/>

			<ToggleSetting
				label="Positions"
				checked={visibilitySettings.Positions}
				helpText="Position markers and dots"
				on:change={(e) => updateVisibilitySetting('Positions', e.detail)}
			/>

			<ToggleSetting
				label="Elemental"
				checked={visibilitySettings.Elemental}
				helpText="Elemental movement notation"
				on:change={(e) => updateVisibilitySetting('Elemental', e.detail)}
			/>

			<ToggleSetting
				label="VTG"
				checked={visibilitySettings.VTG}
				helpText="Vulcan Tech Guild notation"
				on:change={(e) => updateVisibilitySetting('VTG', e.detail)}
			/>

			<ToggleSetting
				label="Non-Radial Points"
				checked={visibilitySettings.nonRadialPoints}
				helpText="Additional position points"
				on:change={(e) => updateVisibilitySetting('nonRadialPoints', e.detail)}
			/>
		</div>
	</SettingCard>
</div>

<style>
	.tab-content {
		max-width: 500px;
	}

	.visibility-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: var(--spacing-sm);
	}
</style>
