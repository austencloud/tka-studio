<!--
ViewportTester.svelte

Development tool for testing different device viewport sizes.
Provides quick access to common device dimensions for responsive testing.
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";

  // Services
  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  // State
  let isOpen = $state(false);
  let currentDevice = $state("Custom");

  // Device presets
  const devicePresets = [
    // Mobile Phones
    { name: "iPhone 15 Pro", width: 393, height: 852, category: "iPhone" },
    { name: "iPhone 15 Pro Max", width: 430, height: 932, category: "iPhone" },
    { name: "iPhone SE", width: 375, height: 667, category: "iPhone" },
    {
      name: "Samsung Galaxy S24",
      width: 384,
      height: 854,
      category: "Android",
    },
    {
      name: "Samsung Galaxy S24 Ultra",
      width: 412,
      height: 915,
      category: "Android",
    },
    { name: "Google Pixel 8", width: 412, height: 915, category: "Android" },

    // Foldables
    {
      name: "Galaxy Z Fold 6 (Folded)",
      width: 344,
      height: 882,
      category: "Foldable",
    },
    {
      name: "Galaxy Z Fold 6 (Unfolded)",
      width: 673,
      height: 841,
      category: "Foldable",
    },
    {
      name: "Galaxy Z Flip 6 (Folded)",
      width: 344,
      height: 748,
      category: "Foldable",
    },
    {
      name: "Galaxy Z Flip 6 (Unfolded)",
      width: 344,
      height: 1516,
      category: "Foldable",
    },

    // Tablets
    { name: "iPad", width: 768, height: 1024, category: "Tablet" },
    { name: 'iPad Pro 11"', width: 834, height: 1194, category: "Tablet" },
    { name: 'iPad Pro 12.9"', width: 1024, height: 1366, category: "Tablet" },

    // Desktop
    { name: "Desktop 1080p", width: 1920, height: 1080, category: "Desktop" },
    { name: "Desktop 1440p", width: 2560, height: 1440, category: "Desktop" },
    { name: "Desktop 4K", width: 3840, height: 2160, category: "Desktop" },

    // Ultra-narrow (for testing edge cases)
    { name: "Ultra Narrow", width: 280, height: 800, category: "Edge Case" },
    { name: "Z Fold Cover", width: 316, height: 684, category: "Edge Case" },
  ];

  // Group devices by category
  const groupedDevices = devicePresets.reduce(
    (acc, device) => {
      if (!acc[device.category]) {
        acc[device.category] = [];
      }
      acc[device.category]?.push(device);
      return acc;
    },
    {} as Record<string, typeof devicePresets>
  );

  function togglePanel() {
    hapticService?.trigger("selection");
    isOpen = !isOpen;
  }

  function selectDevice(device: (typeof devicePresets)[0]) {
    hapticService?.trigger("selection");
    currentDevice = device.name;

    // Resize the viewport
    if (typeof window !== "undefined") {
      // For development, we'll resize the browser window if possible
      try {
        window.resizeTo(device.width + 16, device.height + 100); // Add some padding for browser chrome
      } catch (error) {
        // Fallback: Set viewport meta tag or use CSS transform
        console.log(
          `📱 Viewport set to: ${device.width}x${device.height} (${device.name})`
        );

        // Dispatch custom event for other components to listen to
        window.dispatchEvent(
          new CustomEvent("viewport-change", {
            detail: {
              width: device.width,
              height: device.height,
              device: device.name,
            },
          })
        );
      }
    }

    // Close panel after selection
    isOpen = false;
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      togglePanel();
    }
  }

  function handleBackdropKeydown(event: KeyboardEvent) {
    if (
      (event.key === "Enter" || event.key === " ") &&
      event.target === event.currentTarget
    ) {
      event.preventDefault();
      togglePanel();
    }
  }
</script>

<!-- Floating toggle button -->
<button class="viewport-toggle" onclick={togglePanel} title="Viewport Tester">
  <span class="toggle-icon">📱</span>
  <span class="current-device">{currentDevice}</span>
</button>

<!-- Viewport tester panel -->
{#if isOpen}
  <div
    class="viewport-backdrop"
    role="button"
    tabindex="0"
    onclick={handleBackdropClick}
    onkeydown={handleBackdropKeydown}
  >
    <div class="viewport-panel">
      <div class="panel-header">
        <h3>Viewport Tester</h3>
        <button class="close-btn" onclick={togglePanel}>✕</button>
      </div>

      <div class="panel-content">
        {#each Object.entries(groupedDevices) as [category, devices]}
          <div class="device-category">
            <h4 class="category-title">{category}</h4>
            <div class="device-grid">
              {#each devices as device}
                <button
                  class="device-button"
                  class:active={currentDevice === device.name}
                  onclick={() => selectDevice(device)}
                >
                  <div class="device-name">{device.name}</div>
                  <div class="device-dimensions">
                    {device.width} × {device.height}
                  </div>
                </button>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{/if}

<style>
  .viewport-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 9999;
    background: var(--surface-glass, rgba(0, 0, 0, 0.8));
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.2));
    border-radius: var(--border-radius-lg, 12px);
    padding: var(--spacing-sm, 8px) var(--spacing-md, 16px);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm, 8px);
    transition: all 0.2s ease;
    color: var(--foreground, #ffffff);
    font-size: var(--font-size-sm, 14px);
  }

  .viewport-toggle:hover {
    background: var(--surface-glass-hover, rgba(0, 0, 0, 0.9));
    border-color: var(--primary, #3b82f6);
    transform: translateY(-2px);
  }

  .toggle-icon {
    font-size: 16px;
  }

  .current-device {
    font-weight: 500;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .viewport-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg, 24px);
  }

  .viewport-panel {
    background: var(--surface-glass, rgba(20, 20, 20, 0.95));
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    border-radius: var(--border-radius-lg, 12px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 800px;
    max-height: 80vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-lg, 24px);
    border-bottom: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
  }

  .panel-header h3 {
    margin: 0;
    font-size: var(--font-size-lg, 18px);
    font-weight: 600;
    color: var(--foreground, #ffffff);
  }

  .close-btn {
    width: 32px;
    height: 32px;
    background: transparent;
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.2));
    border-radius: var(--border-radius-md, 8px);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--foreground, #ffffff);
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: var(--surface-light, rgba(255, 255, 255, 0.1));
    border-color: var(--primary, #3b82f6);
  }

  .panel-content {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-lg, 24px);
  }

  .device-category {
    margin-bottom: var(--spacing-xl, 32px);
  }

  .device-category:last-child {
    margin-bottom: 0;
  }

  .category-title {
    margin: 0 0 var(--spacing-md, 16px) 0;
    font-size: var(--font-size-base, 16px);
    font-weight: 600;
    color: var(--primary, #3b82f6);
  }

  .device-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: var(--spacing-sm, 8px);
  }

  .device-button {
    background: var(--surface-light, rgba(255, 255, 255, 0.05));
    border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
    border-radius: var(--border-radius-md, 8px);
    padding: var(--spacing-md, 16px);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
  }

  .device-button:hover {
    background: var(--surface-lighter, rgba(255, 255, 255, 0.1));
    border-color: var(--primary, #3b82f6);
    transform: translateY(-2px);
  }

  .device-button.active {
    background: var(--primary-glass, rgba(59, 130, 246, 0.2));
    border-color: var(--primary, #3b82f6);
  }

  .device-name {
    font-size: var(--font-size-sm, 14px);
    font-weight: 500;
    color: var(--foreground, #ffffff);
    margin-bottom: var(--spacing-xs, 4px);
  }

  .device-dimensions {
    font-size: var(--font-size-xs, 12px);
    color: var(--foreground-muted, #cccccc);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .viewport-toggle {
      top: 10px;
      left: 10px;
      padding: var(--spacing-xs, 4px) var(--spacing-sm, 8px);
    }

    .current-device {
      max-width: 80px;
    }

    .viewport-backdrop {
      padding: var(--spacing-md, 16px);
    }

    .device-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
