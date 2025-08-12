<!-- VisibilityTab.svelte - Compact visibility settings with better contrast -->
<script lang="ts">
	import type { AppSettings } from '$services/interfaces';
	import SettingCard from '../SettingCard.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';

	interface Props {
		settings: AppSettings;
		onUpdate?: (event: { key: string; value: unknown }) => void;
	}

	let { settings, onUpdate }: Props = $props();

	// Visibility settings - matching desktop defaults
	let visibilitySettings = $state({
		TKA: settings.visibility?.TKA ?? true,
		Reversals: settings.visibility?.Reversals ?? true,
		Positions: settings.visibility?.Positions ?? false,
		Elemental: settings.visibility?.Elemental ?? false,
		VTG: settings.visibility?.VTG ?? false,
		nonRadialPoints: settings.visibility?.nonRadialPoints ?? false,
	});

	function updateVisibilitySetting(key: keyof typeof visibilitySettings, value: boolean) {
		visibilitySettings[key] = value;
		onUpdate?.({ key: 'visibility', value: { ...visibilitySettings } });
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
		width: 100%;
		max-width: var(--max-content-width, 100%);
		margin: 0 auto;
		container-type: inline-size;
	}

	.visibility-grid {
		display: grid;
		grid-template-columns: repeat(var(--responsive-columns, 1), 1fr);
		gap: clamp(12px, 1.5vw, 24px);
	}

	/* Container queries for visibility grid */
	@container (min-width: 400px) {
		.visibility-grid {
			grid-template-columns: repeat(1, 1fr);
		}
	}

	@container (min-width: 600px) {
		.visibility-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@container (min-width: 800px) {
		.visibility-grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
</style>
