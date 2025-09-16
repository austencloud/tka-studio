<script lang="ts">
  import { getDeviceInfo } from "$shared/device";
  import DesktopDropdown from "./DesktopDropdown.svelte";
  import MobileModal from "./MobileModal.svelte";
  
  export interface ModeOption {
    id: string;
    label: string;
    icon: string;
    description?: string;
  }
  
  let {
    contextLabel = "Mode",
    currentMode,
    modes = [],
    onModeChange,
    showBreadcrumb = true
  } = $props<{
    contextLabel?: string;
    currentMode: string;
    modes: ModeOption[];
    onModeChange: (mode: string) => void;
    showBreadcrumb?: boolean;
  }>();
  
  const deviceInfo = getDeviceInfo();
  
  const currentModeData = $derived(
    modes.find(m => m.id === currentMode) || modes[0]
  );
</script>

<div class="mode-switcher">
  {#if deviceInfo.isMobile || deviceInfo.isTablet}
    <MobileModal
      {contextLabel}
      {currentModeData}
      {modes}
      {onModeChange}
    />
  {:else}
    <DesktopDropdown
      {contextLabel}
      {currentModeData}
      {modes}
      {onModeChange}
      {showBreadcrumb}
    />
  {/if}
</div>

<style>
  .mode-switcher {
    position: relative;
    flex-shrink: 0;
    height: 40px; /* Consistent compact height */
    display: flex;
    align-items: center;
  }
</style>
