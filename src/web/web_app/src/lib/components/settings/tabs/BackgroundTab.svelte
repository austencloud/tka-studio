<!-- BackgroundTab.svelte - Background settings tab for the settings dialog -->
<script lang="ts">
	import type { BackgroundType, QualityLevel } from '$lib/components/backgrounds/types/types';
	import { createEventDispatcher } from 'svelte';
	import SelectInput from '../SelectInput.svelte';
	import SettingCard from '../SettingCard.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';

	interface Props {
		settings: {
			backgroundType?: BackgroundType;
			backgroundQuality?: QualityLevel;
			backgroundEnabled?: boolean;
		};
	}

	let { settings }: Props = $props();
	const dispatch = createEventDispatcher();

	// Local state for form values - FIXED: Use app's default ('aurora') not component default
	let backgroundType = $state<BackgroundType>(settings.backgroundType || 'aurora');
	let backgroundQuality = $state<QualityLevel>(settings.backgroundQuality || 'medium');
	let backgroundEnabled = $state(settings.backgroundEnabled ?? true);

	// Background type options (removed starfield and auroraBorealis as requested)
	const backgroundOptions = [
		{ value: 'snowfall', label: 'Snowfall' },
		{ value: 'nightSky', label: 'Night Sky' },
		{ value: 'aurora', label: 'Aurora' },
		{ value: 'bubbles', label: 'Bubbles' },
	];

	// Quality options
	const qualityOptions = [
		{ value: 'minimal', label: 'Minimal' },
		{ value: 'low', label: 'Low' },
		{ value: 'medium', label: 'Medium' },
		{ value: 'high', label: 'High' },
	];

	// Update handlers removed - now using inline functions

	function handleEnabledChange(event: CustomEvent) {
		backgroundEnabled = event.detail;
		dispatch('update', { key: 'backgroundEnabled', value: backgroundEnabled });
	}

	// Background descriptions for user guidance
	const backgroundDescriptions: Record<BackgroundType, string> = {
		snowfall: 'Gentle falling snowflakes with shooting stars',
		nightSky: 'Starry night with celestial bodies and shooting stars',
		aurora: 'Colorful aurora with animated blobs and sparkles',
		bubbles: 'Underwater scene with floating bubbles and light rays',
	};

	// Get current background description
	let currentDescription = $derived(
		backgroundDescriptions[backgroundType] || 'Beautiful animated background'
	);
</script>

<div class="tab-content">
	<SettingCard title="Background Settings">
		<ToggleSetting
			label="Enable Background"
			checked={backgroundEnabled}
			helpText="Show animated background behind the interface"
			on:change={handleEnabledChange}
		/>

		{#if backgroundEnabled}
			<SelectInput
				label="Background Type"
				value={backgroundType}
				options={backgroundOptions}
				helpText={currentDescription}
				onchange={(value) => {
					backgroundType = value as BackgroundType;
					dispatch('update', { key: 'backgroundType', value: backgroundType });
				}}
			/>

			<SelectInput
				label="Quality Level"
				value={backgroundQuality}
				options={qualityOptions}
				helpText="Higher quality shows more particles and effects"
				onchange={(value) => {
					backgroundQuality = value as QualityLevel;
					dispatch('update', { key: 'backgroundQuality', value: backgroundQuality });
				}}
			/>
		{/if}
	</SettingCard>

	{#if backgroundEnabled}
		<SettingCard title="Background Preview">
			<div class="preview-container">
				<div class="preview-box" data-background={backgroundType}>
					<div class="preview-content">
						<h4>
							{backgroundOptions.find((opt) => opt.value === backgroundType)?.label}
						</h4>
						<p class="preview-description">{currentDescription}</p>
						<div class="quality-indicator">
							Quality: <span class="quality-badge" data-quality={backgroundQuality}>
								{qualityOptions.find((opt) => opt.value === backgroundQuality)
									?.label}
							</span>
						</div>
					</div>
				</div>
			</div>
		</SettingCard>
	{/if}
</div>

<style>
	.tab-content {
		width: 100%;
		max-width: var(--max-content-width, 100%);
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: clamp(16px, 2vw, 32px);
		container-type: inline-size;
	}

	.preview-container {
		margin-top: clamp(12px, 1.5vw, 24px);
	}

	.preview-box {
		position: relative;
		height: clamp(100px, 15vw, 180px);
		border-radius: 12px;
		overflow: hidden;
		border: 2px solid rgba(255, 255, 255, 0.1);
		background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
		transition: all 0.3s ease;
	}

	/* Container queries for background tab layout */
	@container (min-width: 400px) {
		.tab-content {
			gap: clamp(20px, 2.5vw, 40px);
		}
	}

	@container (min-width: 600px) {
		.tab-content {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: clamp(24px, 3vw, 48px);
			align-items: start;
		}
	}

	.preview-box[data-background='snowfall'] {
		background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
	}

	.preview-box[data-background='nightSky'] {
		background: linear-gradient(135deg, #0a0e2c 0%, #1a2040 50%, #2a3060 100%);
	}

	.preview-box[data-background='aurora'] {
		background: linear-gradient(135deg, #ff00ff 0%, #00ffff 50%, #ffff00 100%);
		opacity: 0.8;
	}

	.preview-box[data-background='auroraBorealis'] {
		background: linear-gradient(135deg, #051932 0%, #0a2850 50%, #0f3c78 100%);
	}

	.preview-box[data-background='starfield'] {
		background: radial-gradient(circle, #050f15 0%, #020208 50%, #000003 100%);
	}

	.preview-box[data-background='bubbles'] {
		background: linear-gradient(135deg, #143250 0%, #0a1e3c 50%, #050f28 100%);
	}

	.preview-content {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		text-align: center;
		color: white;
		z-index: 2;
	}

	.preview-content h4 {
		margin: 0 0 0.5rem 0;
		font-size: 1.1rem;
		font-weight: 600;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
	}

	.preview-description {
		margin: 0 0 0.75rem 0;
		font-size: 0.85rem;
		opacity: 0.9;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
		max-width: 200px;
	}

	.quality-indicator {
		font-size: 0.8rem;
		opacity: 0.8;
	}

	.quality-badge {
		display: inline-block;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-weight: 500;
		text-transform: uppercase;
		font-size: 0.7rem;
		letter-spacing: 0.5px;
	}

	.quality-badge[data-quality='minimal'] {
		background: rgba(255, 100, 100, 0.3);
		color: #ffaaaa;
	}

	.quality-badge[data-quality='low'] {
		background: rgba(255, 200, 100, 0.3);
		color: #ffddaa;
	}

	.quality-badge[data-quality='medium'] {
		background: rgba(100, 200, 255, 0.3);
		color: #aaddff;
	}

	.quality-badge[data-quality='high'] {
		background: rgba(100, 255, 100, 0.3);
		color: #aaffaa;
	}

	/* Add subtle animation to preview */
	.preview-box::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
		animation: shimmer 3s infinite;
		z-index: 1;
	}

	@keyframes shimmer {
		0% {
			left: -100%;
		}
		100% {
			left: 100%;
		}
	}

	.preview-box:hover {
		border-color: rgba(255, 255, 255, 0.3);
		transform: translateY(-2px);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
	}
</style>
