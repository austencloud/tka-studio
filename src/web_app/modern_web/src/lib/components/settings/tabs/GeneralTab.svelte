<!-- GeneralTab.svelte - Compact general settings with fade system controls -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import SettingCard from '../SettingCard.svelte';
	import TextInput from '../TextInput.svelte';
	import ToggleSetting from '../ToggleSetting.svelte';
	import SelectInput from '../SelectInput.svelte';
	
	// Import fade system for direct control
	import { 
		isFadeEnabled, 
		setFadeEnabled, 
		getFadeDebugInfo,
		updateFadeSettings 
	} from '$services/ui/animation';

	interface Props {
		settings: any;
	}

	let { settings }: Props = $props();
	const dispatch = createEventDispatcher();

	// Local state for form values
	let userName = $state(settings.userName || '');
	let autoSave = $state(settings.autoSave ?? true);
	let gridMode = $state(settings.gridMode || 'diamond');
	let workbenchColumns = $state(settings.workbenchColumns || 5);
	
	// Fade system state
	let fadeEnabled = $state(() => {
		try {
			return isFadeEnabled();
		} catch {
			return true; // Default to enabled
		}
	});
	let fadeMainTabDuration = $state(350);
	let fadeSubTabDuration = $state(250);

	// Options
	const gridModeOptions = [
		{ value: 'diamond', label: 'Diamond' },
		{ value: 'box', label: 'Box' }
	];

	// Fade system handlers
	function handleFadeEnabledChange(event: CustomEvent) {
		fadeEnabled = event.detail;
		try {
			setFadeEnabled(fadeEnabled);
			dispatch('update', { key: 'fadeEnabled', value: fadeEnabled });
			console.log(`🎭 Fade animations ${fadeEnabled ? 'enabled' : 'disabled'}`);
		} catch (error) {
			console.error('Failed to update fade enabled state:', error);
		}
	}

	function handleFadeMainTabDurationChange(event: CustomEvent) {
		fadeMainTabDuration = parseInt(event.detail);
		try {
			updateFadeSettings({ mainTabDuration: fadeMainTabDuration });
			dispatch('update', { key: 'fadeMainTabDuration', value: fadeMainTabDuration });
		} catch (error) {
			console.error('Failed to update main tab duration:', error);
		}
	}

	function handleFadeSubTabDurationChange(event: CustomEvent) {
		fadeSubTabDuration = parseInt(event.detail);
		try {
			updateFadeSettings({ subTabDuration: fadeSubTabDuration });
			dispatch('update', { key: 'fadeSubTabDuration', value: fadeSubTabDuration });
		} catch (error) {
			console.error('Failed to update sub-tab duration:', error);
		}
	}

	// Debug info for developers
	function logFadeDebugInfo() {
		try {
			const debugInfo = getFadeDebugInfo();
			console.log('🎭 Fade System Debug Info:', debugInfo);
		} catch (error) {
			console.error('Failed to get fade debug info:', error);
		}
	}
	function handleUserNameChange(event: CustomEvent) {
		userName = event.detail;
		dispatch('update', { key: 'userName', value: userName });
	}

	function handleAutoSaveChange(event: CustomEvent) {
		autoSave = event.detail;
		dispatch('update', { key: 'autoSave', value: autoSave });
	}

	function handleGridModeChange(event: CustomEvent) {
		gridMode = event.detail;
		dispatch('update', { key: 'gridMode', value: gridMode });
	}

	function handleWorkbenchColumnsChange(event: CustomEvent) {
		workbenchColumns = parseInt(event.detail);
		dispatch('update', { key: 'workbenchColumns', value: workbenchColumns });
	}
</script>

<div class="tab-content">
	<SettingCard title="User Profile">
		<TextInput
			label="User Name"
			value={userName}
			placeholder="Enter your name..."
			maxlength={50}
			helpText="Appears on exported sequences"
			on:change={handleUserNameChange}
		/>
	</SettingCard>

	<SettingCard title="Animation Settings">
		<ToggleSetting
			label="Enable Fade Transitions"
			checked={fadeEnabled}
			helpText="Smooth animations when switching between tabs"
			on:change={handleFadeEnabledChange}
		/>
		
		{#if fadeEnabled}
			<TextInput
				label="Main Tab Duration (ms)"
				value={fadeMainTabDuration.toString()}
				type="number"
				min={100}
				max={1000}
				helpText="Animation duration for main tab transitions (Construct, Browse, etc.)"
				on:change={handleFadeMainTabDurationChange}
			/>
			
			<TextInput
				label="Sub-tab Duration (ms)"
				value={fadeSubTabDuration.toString()}
				type="number"
				min={100}
				max={1000}
				helpText="Animation duration for sub-tab transitions (Build, Generate, etc.)"
				on:change={handleFadeSubTabDurationChange}
			/>
			
			<div class="fade-debug-section">
				<button 
					class="debug-button" 
					onclick={logFadeDebugInfo}
					title="Print fade system debug info to console"
				>
					🎭 Debug Fade System
				</button>
				<span class="debug-help">Check browser console for details</span>
			</div>
		{/if}
	</SettingCard>

	<SettingCard title="Application Settings">
		<ToggleSetting
			label="Auto-save Settings"
			checked={autoSave}
			helpText="Save changes automatically"
			on:change={handleAutoSaveChange}
		/>

		<SelectInput
			label="Grid Mode"
			value={gridMode}
			options={gridModeOptions}
			helpText="Pictograph grid layout style"
			on:change={handleGridModeChange}
		/>

		<TextInput
			label="Workbench Columns"
			value={workbenchColumns.toString()}
			type="number"
			min={1}
			max={12}
			helpText="Number of columns in sequence workbench"
			on:change={handleWorkbenchColumnsChange}
		/>
	</SettingCard>
</div>

<style>
	.tab-content {
		max-width: 500px;
	}

	.fade-debug-section {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
		margin-top: var(--spacing-md);
		padding: var(--spacing-sm);
		background: var(--muted) / 10;
		border-radius: var(--border-radius-sm);
		border: 1px solid var(--border);
	}

	.debug-button {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--primary);
		color: var(--primary-foreground);
		border: none;
		border-radius: var(--border-radius-sm);
		cursor: pointer;
		font-size: var(--font-size-xs);
		font-weight: 500;
		transition: all var(--transition-fast);
	}

	.debug-button:hover {
		background: var(--primary-hover);
		transform: translateY(-1px);
	}

	.debug-help {
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		font-style: italic;
	}
</style>
