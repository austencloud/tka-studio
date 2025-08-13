<script lang="ts">
	import LocationSelector from './LocationSelector.svelte';
	import OrientationSelector from './OrientationSelector.svelte';
	import TurnsControl from './TurnsControl.svelte';
	import MotionTypeSelector from './MotionTypeSelector.svelte';
	import type { Orientation, MotionType } from '../utils/motion-helpers.js';

	interface Props {
		propName: string;
		propColor: string;
		startLocation: string;
		endLocation: string;
		startOrientation: Orientation;
		endOrientation: Orientation;
		turns: number;
		motionType: MotionType;
		onStartLocationChange: (location: string) => void;
		onEndLocationChange: (location: string) => void;
		onStartOrientationChange: (orientation: Orientation) => void;
		onEndOrientationChange: (orientation: Orientation) => void;
		onTurnsChange: (turns: number) => void;
		onMotionTypeChange: (motionType: MotionType) => void;
	}

	let {
		propName,
		propColor,
		startLocation,
		endLocation,
		startOrientation,
		endOrientation,
		turns,
		motionType,
		onStartLocationChange,
		onEndLocationChange,
		onStartOrientationChange,
		onEndOrientationChange,
		onTurnsChange,
		onMotionTypeChange
	}: Props = $props();
</script>

<div class="prop-panel">
	<div class="prop-header" style="color: {propColor}">
		{propName} Prop
	</div>
	
	<div class="prop-controls">
		<LocationSelector 
			{propColor}
			propLabel="Loc"
			{startLocation}
			{endLocation}
			{onStartLocationChange}
			{onEndLocationChange}
		/>
		
		<OrientationSelector 
			orientation={startOrientation}
			{propColor}
			label="Start"
			onOrientationChange={onStartOrientationChange}
		/>
		
		<OrientationSelector 
			orientation={endOrientation}
			{propColor}
			label="End"
			onOrientationChange={onEndOrientationChange}
		/>
		
		<TurnsControl 
			{turns}
			{propColor}
			{onTurnsChange}
		/>
		
		<MotionTypeSelector 
			{motionType}
			{propColor}
			{onMotionTypeChange}
		/>
	</div>
</div>

<style>
	.prop-panel {
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 8px;
		padding: 16px;
		background: rgba(0, 0, 0, 0.2);
	}

	.prop-header {
		font-size: 16px;
		font-weight: 700;
		margin-bottom: 16px;
		text-align: center;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.prop-controls {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
</style>
