<!-- ShareOptionsPanel.svelte - Share options configuration -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ShareOptions } from "../domain";

  let {
    options,
    onOptionsChange,
  }: {
    options?: ShareOptions;
    onOptionsChange?: (newOptions: Partial<ShareOptions>) => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });



  // Handle individual option changes
  function handleOptionChange(key: keyof ShareOptions, value: any) {
    if (!options) return;
    onOptionsChange?.({ [key]: value });
  }

  // Type-safe event handlers
  function handleSelectChange(key: keyof ShareOptions, transform?: (value: string) => any) {
    return (event: Event) => {
      const target = event.target as HTMLSelectElement;
      const value = transform ? transform(target.value) : target.value;

      // Trigger selection haptic feedback for option changes
      hapticService?.trigger("selection");

      handleOptionChange(key, value);
    };
  }

  function handleInputChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;
      handleOptionChange(key, target.value);
    };
  }

  function handleCheckboxChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;

      // Trigger selection haptic feedback for checkbox toggles
      hapticService?.trigger("selection");

      handleOptionChange(key, target.checked);
    };
  }

  // Set optimal defaults - PNG format for better Android share preview compatibility
  $effect(() => {
    if (options && (options.format !== 'PNG' || options.quality !== 1.0)) {
      onOptionsChange?.({
        format: 'PNG',
        quality: 1.0
      });
    }
  });


</script>

<div class="share-options">
  {#if options}



    <!-- Content Options -->
    <div class="option-group">
      <h4 class="group-title">What to include in your image</h4>

      <label class="option-checkbox">
        <input
          type="checkbox"
          checked={options.addWord}
          onchange={handleCheckboxChange('addWord')}
        />
        Include word/title
      </label>

      <label class="option-checkbox">
        <input
          type="checkbox"
          checked={options.addBeatNumbers}
          onchange={handleCheckboxChange('addBeatNumbers')}
        />
        Show beat numbers
      </label>

      <label class="option-checkbox">
        <input
          type="checkbox"
          checked={options.addUserInfo}
          onchange={handleCheckboxChange('addUserInfo')}
        />
        Include user info
      </label>

      <label class="option-checkbox">
        <input
          type="checkbox"
          checked={options.addDifficultyLevel}
          onchange={handleCheckboxChange('addDifficultyLevel')}
        />
        Show difficulty level
      </label>

      <label class="option-checkbox">
        <input
          type="checkbox"
          checked={options.includeStartPosition}
          onchange={handleCheckboxChange('includeStartPosition')}
        />
        Include start position
      </label>
    </div>

    <!-- User Info (if enabled) -->
    {#if options.addUserInfo}
      <div class="option-group">
        <h4 class="group-title">User Information</h4>

        <label class="option-label">
          Name
          <input
            type="text"
            class="option-input"
            value={options.userName}
            oninput={handleInputChange('userName')}
            placeholder="Your name"
          />
        </label>

        <label class="option-label">
          Notes
          <input
            type="text"
            class="option-input"
            value={options.notes}
            oninput={handleInputChange('notes')}
            placeholder="Optional notes"
          />
        </label>
      </div>
    {/if}
  {/if}
</div>

<style>
  .share-options {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
    max-height: 500px;
    overflow-y: auto;
  }

  .option-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .group-title {
    margin: 0 0 0.25rem 0;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.25rem;
  }

  .option-label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .option-input {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.9rem;
  }

  .option-input:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  .option-checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-primary);
    cursor: pointer;
  }

  .option-checkbox input[type="checkbox"] {
    margin: 0;
  }
</style>
