<!-- PropTypeTab.svelte - Prop type selection with actual desktop app files -->
<script lang="ts">
	import type { AppSettings } from '$services/interfaces';
	import SettingCard from '../SettingCard.svelte';

	interface Props {
		settings: AppSettings;
		onUpdate?: (event: { key: string; value: unknown }) => void;
	}

	let { settings, onUpdate }: Props = $props();

	// Exact prop types from desktop app prop_type_tab.py
	const propTypes = [
		{ id: 'Staff', label: 'Staff', image: '/images/props/staff.svg' },
		{ id: 'Simplestaff', label: 'Simple Staff', image: '/images/props/simple_staff.svg' },
		{ id: 'Club', label: 'Club', image: '/images/props/club.svg' },
		{ id: 'Fan', label: 'Fan', image: '/images/props/fan.svg' },
		{ id: 'Triad', label: 'Triad', image: '/images/props/triad.svg' },
		{ id: 'Minihoop', label: 'Mini Hoop', image: '/images/props/minihoop.svg' },
		{ id: 'Buugeng', label: 'Buugeng', image: '/images/props/buugeng.svg' },
		{ id: 'Triquetra', label: 'Triquetra', image: '/images/props/triquetra.svg' },
		{ id: 'Sword', label: 'Sword', image: '/images/props/sword.svg' },
		{ id: 'Chicken', label: 'Chicken', image: '/images/props/chicken.png' },
		{ id: 'Hand', label: 'Hand', image: '/images/props/hand.svg' },
		{ id: 'Guitar', label: 'Guitar', image: '/images/props/guitar.svg' },
		{ id: 'Ukulele', label: 'Ukulele', image: '/images/props/ukulele.svg' },
	];

	let selectedPropType = $state(settings.propType || 'Staff');

	function selectPropType(propType: string) {
		selectedPropType = propType;
		onUpdate?.({ key: 'propType', value: propType });
	}
</script>

<div class="tab-content">
	<SettingCard title="Select Prop Type" description="Choose your primary prop type for sequences">
		<div class="prop-grid">
			{#each propTypes as prop}
				<button
					class="prop-button"
					class:selected={selectedPropType === prop.id}
					onclick={() => selectPropType(prop.id)}
				>
					<div class="prop-image-container">
						<img src={prop.image} alt={prop.label} class="prop-image" loading="lazy" />
					</div>
					<span class="prop-label">{prop.label}</span>
				</button>
			{/each}
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

	.prop-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
		gap: clamp(12px, 1.5vw, 24px);
		margin-top: clamp(16px, 2vw, 32px);
	}

	/* Container queries for prop grid */
	@container (min-width: 300px) {
		.prop-grid {
			grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
		}
	}

	@container (min-width: 500px) {
		.prop-grid {
			grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		}
	}

	@container (min-width: 700px) {
		.prop-grid {
			grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
		}
	}

	@container (min-width: 900px) {
		.prop-grid {
			grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		}
	}

	.prop-button {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: clamp(6px, 0.8vw, 12px);
		padding: clamp(8px, 1vw, 16px);
		background: rgba(255, 255, 255, 0.05);
		border: 2px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		cursor: pointer;
		transition: all var(--transition-fast);
		color: rgba(255, 255, 255, 0.8);
		min-height: clamp(70px, 8vw, 100px);
		aspect-ratio: 1;
	}

	.prop-button:hover {
		background: rgba(255, 255, 255, 0.08);
		border-color: rgba(255, 255, 255, 0.3);
		color: #ffffff;
		transform: translateY(-1px);
	}

	.prop-button.selected {
		background: rgba(99, 102, 241, 0.2);
		border-color: #6366f1;
		color: #ffffff;
		box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);
	}

	.prop-image-container {
		width: clamp(28px, 4vw, 48px);
		height: clamp(28px, 4vw, 48px);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.prop-image {
		max-width: 100%;
		max-height: 100%;
		filter: invert(1) brightness(0.9);
		transition: filter var(--transition-fast);
	}

	.prop-button:hover .prop-image {
		filter: invert(1) brightness(1);
	}

	.prop-button.selected .prop-image {
		filter: invert(1) brightness(1);
	}

	.prop-label {
		font-size: clamp(10px, 1.2vw, 14px);
		font-weight: 500;
		text-align: center;
		line-height: 1.2;
		word-break: break-word;
	}

	/* Remove old responsive styles - replaced with container queries */
</style>
