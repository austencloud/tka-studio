<script lang="ts">
  import type { IDeviceDetector } from "$shared/device/services/contracts";
  import { resolve, TYPES } from "$shared/inversify";
  import type { ModeOption } from "../domain";
  import DesktopDropdown from "./DesktopDropdown.svelte";
  import MobileModal from "./MobileModal.svelte";
  
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
  
  const deviceDetector = resolve(TYPES.IDeviceDetector) as IDeviceDetector;
  const deviceInfo = {
    isMobile: deviceDetector.isMobile(),
    isTablet: deviceDetector.isTablet(),
    isDesktop: deviceDetector.isDesktop()
  };
  
  const currentModeData = $derived(
    modes.find((m: ModeOption) => m.id === currentMode) || modes[0]
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
