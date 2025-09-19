<script lang="ts">
  let {
    isOpen,
    currentBackground,
    onClose,
    onBackgroundChange,
  } = $props<{
    isOpen: boolean;
    currentBackground: "deepOcean" | "snowfall" | "nightSky";
    onClose: () => void;
    onBackgroundChange: (background: string) => void;
  }>();

  const backgroundOptions = [
    {
      id: "nightSky",
      label: "Night Sky",
      icon: "🌌",
      description: "Starry night with constellations",
    },
    {
      id: "deepOcean",
      label: "Deep Ocean",
      icon: "🌊",
      description: "Underwater marine life",
    },
    {
      id: "snowfall",
      label: "Snowfall",
      icon: "❄️",
      description: "Gentle falling snow",
    },
  ];

  function handleBackgroundSelect(backgroundId: string) {
    onBackgroundChange(backgroundId);
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      onClose();
    }
  }
</script>

{#if isOpen}
  <!-- Modal backdrop -->
  <div
    class="modal-backdrop"
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="settings-title"
    tabindex="0"
  >
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <h2 id="settings-title">Background Settings</h2>
        <button
          class="close-button"
          onclick={onClose}
          aria-label="Close settings"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M18 6L6 18M6 6l12 12"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="modal-body">
        <div class="settings-section">
          <h3>Choose Background</h3>
          <div class="background-grid">
            {#each backgroundOptions as option}
              <button
                class="background-option"
                class:active={currentBackground === option.id}
                onclick={() => handleBackgroundSelect(option.id)}
                aria-pressed={currentBackground === option.id}
              >
                <div class="option-icon">{option.icon}</div>
                <div class="option-content">
                  <div class="option-label">{option.label}</div>
                  <div class="option-description">{option.description}</div>
                </div>
                {#if currentBackground === option.id}
                  <div class="active-indicator">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M20 6L9 17l-5-5"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  </div>
                {/if}
              </button>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: var(--spacing-lg);
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .modal-content {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 1.5rem;
    box-shadow:
      0 20px 40px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    max-width: 500px;
    width: 100%;
    max-height: 80vh;
    overflow: hidden;
    animation: slideIn 0.3s ease-out;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg) var(--spacing-xl);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .modal-header h2 {
    margin: 0;
    color: var(--text-color, white);
    font-size: 1.5rem;
    font-weight: 600;
  }

  .close-button {
    background: transparent;
    border: none;
    color: var(--text-color, white);
    cursor: pointer;
    padding: var(--spacing-sm);
    border-radius: var(--border-radius);
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ff6b6b;
  }

  .close-button:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  .modal-body {
    padding: var(--spacing-xl);
    overflow-y: auto;
  }

  .settings-section {
    margin-bottom: var(--spacing-lg);
  }

  .settings-section h3 {
    margin: 0 0 var(--spacing-lg) 0;
    color: var(--text-color, white);
    font-size: 1.125rem;
    font-weight: 600;
  }

  .background-grid {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .background-option {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    width: 100%;
    text-align: left;
  }

  .background-option:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .background-option.active {
    background: rgba(102, 126, 234, 0.2);
    border-color: rgba(102, 126, 234, 0.4);
    box-shadow:
      0 4px 16px rgba(102, 126, 234, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .background-option:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  .option-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .option-content {
    flex: 1;
  }

  .option-label {
    font-weight: 600;
    color: var(--text-color, white);
    margin-bottom: 2px;
  }

  .option-description {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
  }

  .active-indicator {
    color: #667eea;
    flex-shrink: 0;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .modal-backdrop {
      padding: var(--spacing-md);
    }

    .modal-content {
      max-height: 90vh;
    }

    .modal-header,
    .modal-body {
      padding: var(--spacing-lg);
    }

    .option-icon {
      font-size: 1.5rem;
    }

    .background-option {
      padding: var(--spacing-sm) var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .modal-backdrop,
    .modal-content,
    .background-option,
    .close-button {
      animation: none;
      transition: none;
    }

    .background-option:hover {
      transform: none;
    }
  }
</style>
