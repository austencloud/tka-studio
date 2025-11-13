<!-- ShareOptionsForm.svelte - Share options configuration -->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { FontAwesomeIcon, resolve, TYPES } from "$shared";
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
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Toggle options with Font Awesome icons and colors (matching your CAP card style)
  const toggleOptions = [
    {
      key: "addWord" as const,
      icon: "fa-solid fa-heading",
      label: "Word/Title",
      color: "#3b82f6", // blue
    },
    {
      key: "addBeatNumbers" as const,
      icon: "fa-solid fa-list-ol",
      label: "Beat #s",
      color: "#8b5cf6", // purple
    },
    {
      key: "addUserInfo" as const,
      icon: "fa-solid fa-user",
      label: "User Info",
      color: "#ec4899", // pink
    },
    {
      key: "addDifficultyLevel" as const,
      icon: "fa-solid fa-star",
      label: "Difficulty",
      color: "#f59e0b", // amber
    },
    {
      key: "includeStartPosition" as const,
      icon: "fa-solid fa-bullseye",
      label: "Start Pos",
      color: "#10b981", // green
    },
  ];

  // Handle toggle with haptic feedback
  function handleToggle(key: keyof ShareOptions) {
    hapticService?.trigger("selection");
    if (!options) return;
    onOptionsChange?.({ [key]: !options[key] });
  }

  // Handle text input
  function handleInputChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;
      onOptionsChange?.({ [key]: target.value });
    };
  }

  // Set optimal defaults - PNG format for better Android share preview compatibility
  $effect(() => {
    if (options && (options.format !== "PNG" || options.quality !== 1.0)) {
      onOptionsChange?.({
        format: "PNG",
        quality: 1.0,
      });
    }
  });
</script>

<div class="share-options">
  {#if options}
    <!-- Toggle Buttons Grid (matching CAP card style) -->
    <div class="toggles-grid">
      {#each toggleOptions as option}
        <button
          type="button"
          class="toggle-btn"
          class:active={options[option.key]}
          style:--toggle-color={option.color}
          onclick={() => handleToggle(option.key)}
          aria-label="Toggle {option.label}"
        >
          <span class="toggle-icon">
            <FontAwesomeIcon icon={option.icon} size="1.4em" />
          </span>
          <span class="toggle-label">{option.label}</span>
        </button>
      {/each}
    </div>

    <!-- User Info Inputs (if enabled) -->
    {#if options.addUserInfo}
      <div class="user-info-section">
        <input
          type="text"
          class="info-input"
          value={options.userName}
          oninput={handleInputChange("userName")}
          placeholder="Your name"
        />

        <input
          type="text"
          class="info-input"
          value={options.notes}
          oninput={handleInputChange("notes")}
          placeholder="Optional notes"
        />
      </div>
    {/if}
  {/if}
</div>

<style>
  /* Simple vertical stack - no grid needed */
  .share-options {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* Toggle Buttons Stack - clean vertical list */
  .toggles-grid {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  /* Toggle Button - horizontal list item style */
  .toggle-btn {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;

    /* Solid background - no glassmorphism */
    background: rgba(0, 0, 0, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
  }

  .toggle-btn:hover {
    background: rgba(0, 0, 0, 0.4);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-1px);
  }

  .toggle-btn:active {
    transform: translateY(0);
  }

  /* Active state - colorful gradient with glow */
  .toggle-btn.active {
    background: linear-gradient(
      135deg,
      var(--toggle-color),
      color-mix(in srgb, var(--toggle-color) 80%, black)
    );
    border-color: white;
    border-width: 3px;
    box-shadow: 0 0 16px
      color-mix(in srgb, var(--toggle-color) 50%, transparent);
  }

  .toggle-btn:focus-visible {
    outline: 3px solid rgba(59, 130, 246, 0.4);
    outline-offset: 2px;
  }

  .toggle-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    line-height: 1;
    color: white;
    flex-shrink: 0;
  }

  .toggle-label {
    flex: 1;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.3px;
    line-height: 1.2;
    text-align: left;
  }

  /* User Info Section */
  .user-info-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-top: 4px;
  }

  .info-input {
    padding: 12px 14px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.3);
    color: rgba(255, 255, 255, 0.95);
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .info-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  .info-input:hover {
    background: rgba(0, 0, 0, 0.4);
    border-color: rgba(255, 255, 255, 0.35);
  }

  .info-input:focus {
    outline: none;
    background: rgba(0, 0, 0, 0.5);
    border-color: rgba(59, 130, 246, 0.7);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .toggle-btn,
    .info-input {
      transition: none;
    }

    .toggle-btn:hover,
    .toggle-btn:active {
      transform: none;
    }
  }
</style>
