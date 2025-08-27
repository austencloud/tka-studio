<!-- ActHeader.svelte - Act header with name, description, and music controls -->
<script lang="ts">
  import type { ActData } from "$lib/types/write";

  // Props
  interface Props {
    act?: ActData | null;
    disabled?: boolean;
    onActInfoChanged?: (name: string, description: string) => void;
    onMusicLoadRequested?: () => void;
  }

  let {
    act = null,
    disabled = false,
    onActInfoChanged,
    onMusicLoadRequested,
  }: Props = $props();

  // Local state for form inputs
  let nameValue = $state("");
  let descriptionValue = $state("");

  // Update local state when act changes
  $effect(() => {
    if (act) {
      nameValue = act.name;
      descriptionValue = act.description;
    } else {
      nameValue = "";
      descriptionValue = "";
    }
  });

  // Handle name change
  function handleNameChange(event: Event) {
    const target = event.target;
    if (target instanceof HTMLInputElement) {
      nameValue = target.value;
      onActInfoChanged?.(nameValue, descriptionValue);
    }
  }

  // Handle description change
  function handleDescriptionChange(event: Event) {
    const target = event.target;
    if (target instanceof HTMLTextAreaElement) {
      descriptionValue = target.value;
      onActInfoChanged?.(nameValue, descriptionValue);
    }
  }

  // Handle music load button
  function handleMusicLoad() {
    onMusicLoadRequested?.();
  }

  // Computed values
  const sequenceCount = $derived(act?.sequences.length || 0);
  const musicStatus = $derived(() => {
    if (!act?.musicFile) return "No music loaded";
    return `♪ ${act.musicFile.name}`;
  });
  const musicStatusColor = $derived(
    act?.musicFile ? "rgba(100, 200, 100, 0.9)" : "rgba(255, 255, 255, 0.6)"
  );
</script>

<div class="act-header" class:disabled>
  <!-- Title row -->
  <div class="title-row">
    <!-- Act name editor -->
    <input
      class="name-input"
      type="text"
      placeholder="Act Name"
      value={nameValue}
      {disabled}
      oninput={handleNameChange}
    />

    <!-- Music button -->
    <button class="music-button btn-glass" {disabled} onclick={handleMusicLoad}>
      🎵 Load Music
    </button>
  </div>

  <!-- Description editor -->
  <textarea
    class="description-input"
    placeholder="Act description..."
    value={descriptionValue}
    {disabled}
    oninput={handleDescriptionChange}
    rows="3"
  ></textarea>

  <!-- Info bar -->
  <div class="info-bar">
    <span class="sequence-count">
      {sequenceCount} sequence{sequenceCount !== 1 ? "s" : ""}
    </span>

    <span class="music-status" style="color: {musicStatusColor}">
      {musicStatus()}
    </span>
  </div>
</div>

<style>
  .act-header {
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    padding: var(--spacing-md);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    transition: all var(--transition-normal);
  }

  .act-header.disabled {
    opacity: 0.6;
    pointer-events: none;
  }

  .title-row {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .name-input {
    flex: 1;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-sm) var(--spacing-md);
    color: var(--text-color);
    font-size: var(--font-size-lg);
    font-weight: bold;
    font-family: "Segoe UI", sans-serif;
    transition: all var(--transition-normal);
    backdrop-filter: blur(8px);
  }

  .name-input:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .name-input::placeholder {
    color: var(--text-secondary);
  }

  .music-button {
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
    font-weight: 500;
    white-space: nowrap;
    min-height: 32px;
  }

  .description-input {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-sm) var(--spacing-md);
    color: var(--text-color);
    font-size: var(--font-size-sm);
    font-family: "Segoe UI", sans-serif;
    resize: vertical;
    min-height: 60px;
    max-height: 120px;
    transition: all var(--transition-normal);
    backdrop-filter: blur(8px);
  }

  .description-input:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }

  .description-input::placeholder {
    color: var(--text-secondary);
  }

  .info-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-md);
    padding-top: var(--spacing-xs);
    border-top: var(--glass-border);
  }

  .sequence-count {
    color: var(--text-color);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .music-status {
    font-size: var(--font-size-sm);
    font-weight: 500;
    transition: color var(--transition-normal);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .act-header {
      padding: var(--spacing-sm);
      gap: var(--spacing-xs);
    }

    .title-row {
      flex-direction: column;
      align-items: stretch;
      gap: var(--spacing-sm);
    }

    .name-input {
      font-size: var(--font-size-base);
    }

    .music-button {
      align-self: flex-end;
      min-width: 120px;
    }

    .description-input {
      min-height: 50px;
    }

    .info-bar {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-xs);
    }
  }

  @media (max-width: 480px) {
    .act-header {
      padding: var(--spacing-xs);
    }

    .name-input {
      font-size: var(--font-size-sm);
      padding: var(--spacing-xs) var(--spacing-sm);
    }

    .description-input {
      font-size: var(--font-size-xs);
      padding: var(--spacing-xs) var(--spacing-sm);
    }

    .music-button {
      font-size: var(--font-size-xs);
      padding: var(--spacing-xs) var(--spacing-sm);
    }

    .sequence-count,
    .music-status {
      font-size: var(--font-size-xs);
    }
  }

  /* Custom scrollbar for textarea */
  .description-input::-webkit-scrollbar {
    width: 6px;
  }

  .description-input::-webkit-scrollbar-track {
    background: transparent;
    border-radius: var(--border-radius-sm);
  }

  .description-input::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-sm);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .description-input::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }
</style>
