<!--
ContentTypeSelector - Content Type Selection Buttons
Compact horizontal row of buttons for selecting content types (Video, Animation, Image)
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  type ContentType = "video" | "animation" | "image";

  let {
    selectedTypes = $bindable<ContentType[]>([]),
  }: {
    selectedTypes?: ContentType[];
  } = $props();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Content types configuration
  const contentTypes: {
    type: ContentType;
    icon: string;
    label: string;
    color: string;
    disabled: boolean;
  }[] = [
    {
      type: "video",
      icon: "fa-solid fa-video",
      label: "Video",
      color: "#ef4444",
      disabled: true,
    },
    {
      type: "animation",
      icon: "fa-solid fa-film",
      label: "Animation",
      color: "#8b5cf6",
      disabled: true,
    },
    {
      type: "image",
      icon: "fa-solid fa-image",
      label: "Image",
      color: "#3b82f6",
      disabled: false,
    },
  ];

  function toggleContentType(type: ContentType) {
    const disabled = contentTypes.find((ct) => ct.type === type)?.disabled;
    if (disabled) return;

    hapticService?.trigger("selection");

    selectedTypes = selectedTypes.includes(type)
      ? selectedTypes.filter((t) => t !== type)
      : [...selectedTypes, type];
  }
</script>

<section class="content-type-selector">
  <h3>Select Content Types</h3>
  <div class="type-grid">
    {#each contentTypes as contentType}
      <button
        class="type-button"
        class:selected={selectedTypes.includes(contentType.type)}
        class:disabled={contentType.disabled}
        onclick={() => toggleContentType(contentType.type)}
        style="--type-color: {contentType.color}"
        type="button"
      >
        <div class="type-icon">
          <i class={contentType.icon}></i>
        </div>
        <span class="type-label">{contentType.label}</span>
        <div class="selection-indicator">
          <i class="fas fa-check"></i>
        </div>
      </button>
    {/each}
  </div>
</section>

<style>
  .content-type-selector h3 {
    margin: 0 0 18px 0;
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-size: 13px;
  }

  .type-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .type-button {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.04);
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .type-button:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .type-button.selected {
    background: color-mix(in srgb, var(--type-color) 15%, transparent);
    border-color: var(--type-color);
  }

  .type-button.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .type-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--type-color);
    transition: all 0.2s ease;
  }

  .type-button.selected .type-icon {
    color: var(--type-color);
  }

  .type-label {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.2s ease;
  }

  .type-button.selected .type-label {
    color: rgba(255, 255, 255, 0.95);
  }

  .selection-indicator {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--type-color);
    color: white;
    font-size: 10px;
    opacity: 0;
    transform: scale(0.5);
    transition: all 0.2s ease;
  }

  .type-button.selected .selection-indicator {
    opacity: 1;
    transform: scale(1);
  }
</style>
