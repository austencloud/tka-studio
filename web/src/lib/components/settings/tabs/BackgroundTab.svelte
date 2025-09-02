<!-- BackgroundTab.svelte - Refactored using modular components -->
<script lang="ts">
  import { BackgroundType } from "$domain";
    import { updateBodyBackground } from "$utils";
  import SettingCard from "../SettingCard.svelte";
  import BackgroundSelector from "./background/BackgroundSelector.svelte";

  interface Props {
    settings: {
      backgroundType?: BackgroundType;
    };
    onupdate?: (update: { key: string; value: any }) => void;
  }

  let { settings, onupdate }: Props = $props();

  // Current selection state
  let selectedBackground = $state<BackgroundType>(
    settings.backgroundType || BackgroundType.NIGHT_SKY
  );

  // Handle background selection
  function handleBackgroundSelect(backgroundType: BackgroundType) {
    selectedBackground = backgroundType;

    // Update the body background immediately for smooth transition
    updateBodyBackground(backgroundType);

    // Update settings - backgrounds are always enabled, quality is auto-managed
    if (onupdate) {
      onupdate({ key: "backgroundType", value: backgroundType });
    }

    console.log(`🌌 Background changed to: ${backgroundType}`);
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Background Selection"
    description="Choose your preferred animated background"
  >
    <BackgroundSelector
      {selectedBackground}
      onBackgroundSelect={handleBackgroundSelect}
    />
  </SettingCard>
</div>

<style>
  .tab-content {
    width: 100%;
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: clamp(20px, 3vw, 32px);
    container-type: inline-size;
  }
</style>
