<!-- AccessibilityTab.svelte - Modern User Experience Settings -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type { IHapticFeedbackService, IMobileFullscreenService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  interface Props {
    currentSettings: {
      hapticFeedback?: boolean;
      reducedMotion?: boolean;
    };
    onSettingUpdate: (event: { key: string; value: unknown }) => void;
  }

  let { currentSettings, onSettingUpdate }: Props = $props();

  // Services
  let hapticService: IHapticFeedbackService;
  let fullscreenService: IMobileFullscreenService | null = null;

  // Local state for immediate UI feedback
  let hapticEnabled = $state(currentSettings.hapticFeedback ?? true);
  let reducedMotion = $state(currentSettings.reducedMotion ?? false);
  let isFullscreen = $state(false);
  let isPWA = $state(false);

  // Check if device supports haptic feedback
  const isHapticSupported =
    browser &&
    ("vibrate" in navigator ||
      "mozVibrate" in navigator ||
      "webkitVibrate" in navigator);

  // Check if fullscreen is supported
  const isFullscreenSupported =
    browser &&
    !!(
      document.fullscreenEnabled ||
      (document as any).webkitFullscreenEnabled ||
      (document as any).mozFullScreenEnabled ||
      (document as any).msFullscreenEnabled
    );

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    try {
      fullscreenService = resolve<IMobileFullscreenService>(
        TYPES.IMobileFullscreenService
      );
      isPWA = fullscreenService.isPWA();
      isFullscreen = fullscreenService.isFullscreen();

      // Listen for fullscreen changes
      const unsubscribe = fullscreenService.onFullscreenChange((fullscreen) => {
        isFullscreen = fullscreen;
      });

      return () => {
        unsubscribe?.();
      };
    } catch (error) {
      console.warn("Failed to resolve fullscreen service:", error);
      fullscreenService = null;
    }
  });

  // Watch for external changes to settings
  $effect(() => {
    hapticEnabled = currentSettings.hapticFeedback ?? true;
    reducedMotion = currentSettings.reducedMotion ?? false;
  });

  function triggerTestVibration() {
    if (browser && isHapticSupported) {
      try {
        navigator.vibrate([100, 30, 50]); // Success pattern
      } catch (error) {
        console.warn("Test vibration failed:", error);
      }
    }
  }

  function handleHapticToggle(event: Event) {
    const target = event.target as HTMLInputElement;
    const enabled = target.checked;
    hapticEnabled = enabled;

    // Trigger haptic feedback test if enabling
    if (enabled) {
      setTimeout(triggerTestVibration, 150);
    }

    // Update parent settings
    onSettingUpdate({ key: "hapticFeedback", value: enabled });
  }

  function handleReducedMotionToggle(event: Event) {
    const target = event.target as HTMLInputElement;
    const enabled = target.checked;
    reducedMotion = enabled;

    // If reduced motion is enabled, also disable haptic feedback
    if (enabled && hapticEnabled) {
      hapticEnabled = false;
      onSettingUpdate({ key: "hapticFeedback", value: false });
    }

    // Update parent settings
    onSettingUpdate({ key: "reducedMotion", value: enabled });
  }

  async function handleFullscreenToggle(event: Event) {
    const target = event.target as HTMLInputElement;
    const shouldBeFullscreen = target.checked;

    if (!fullscreenService) {
      // Fallback to direct DOM API
      try {
        if (shouldBeFullscreen) {
          const element = document.documentElement;
          if (element.requestFullscreen) {
            await element.requestFullscreen();
          } else if ((element as any).webkitRequestFullscreen) {
            await (element as any).webkitRequestFullscreen();
          } else if ((element as any).mozRequestFullScreen) {
            await (element as any).mozRequestFullScreen();
          } else if ((element as any).msRequestFullscreen) {
            await (element as any).msRequestFullscreen();
          }
        } else {
          if (document.exitFullscreen) {
            await document.exitFullscreen();
          } else if ((document as any).webkitExitFullscreen) {
            await (document as any).webkitExitFullscreen();
          } else if ((document as any).mozCancelFullScreen) {
            await (document as any).mozCancelFullScreen();
          } else if ((document as any).msExitFullscreen) {
            await (document as any).msExitFullscreen();
          }
        }
      } catch (error) {
        console.warn("Fullscreen toggle failed:", error);
      }
    } else {
      // Use fullscreen service
      try {
        if (shouldBeFullscreen) {
          await fullscreenService.requestFullscreen();
        } else {
          await fullscreenService.exitFullscreen();
        }
      } catch (error) {
        console.warn("Fullscreen toggle failed:", error);
      }
    }
  }
</script>

<div class="experience-tab">
  <!-- Haptic Feedback Card -->
  <div class="setting-card" class:disabled={!isHapticSupported}>
    <div class="card-icon haptic-icon">
      <i class="fas fa-hand-paper"></i>
    </div>
    <div class="card-content">
      <div class="card-header">
        <h3>Haptic Feedback</h3>
        {#if !isHapticSupported}
          <span class="badge">Not Available</span>
        {/if}
      </div>
    </div>
    <label class="toggle-switch">
      <input
        type="checkbox"
        checked={hapticEnabled && isHapticSupported}
        disabled={!isHapticSupported}
        onchange={handleHapticToggle}
        aria-label="Toggle haptic feedback"
      />
      <span class="toggle-slider"></span>
    </label>
  </div>

  <!-- Reduced Motion Card -->
  <div class="setting-card">
    <div class="card-icon motion-icon">
      <i class="fas fa-running"></i>
    </div>
    <div class="card-content">
      <div class="card-header">
        <h3>Reduce Motion</h3>
      </div>
    </div>
    <label class="toggle-switch">
      <input
        type="checkbox"
        checked={reducedMotion}
        onchange={handleReducedMotionToggle}
        aria-label="Toggle reduced motion"
      />
      <span class="toggle-slider"></span>
    </label>
  </div>

  <!-- Fullscreen Mode Card -->
  {#if !isPWA}
    <div class="setting-card" class:disabled={!isFullscreenSupported}>
      <div class="card-icon fullscreen-icon">
        <i class="fas fa-expand"></i>
      </div>
      <div class="card-content">
        <div class="card-header">
          <h3>Fullscreen Mode</h3>
          {#if !isFullscreenSupported}
            <span class="badge">Not Available</span>
          {/if}
        </div>
        <p class="card-description">Enter fullscreen mode for distraction-free experience</p>
      </div>
      <label class="toggle-switch">
        <input
          type="checkbox"
          checked={isFullscreen && isFullscreenSupported}
          disabled={!isFullscreenSupported}
          onchange={handleFullscreenToggle}
          aria-label="Toggle fullscreen mode"
        />
        <span class="toggle-slider"></span>
      </label>
    </div>
  {/if}

  <!-- PWA Install Recommendation -->
  <div class="info-banner pwa-recommendation">
    <i class="fas fa-lightbulb"></i>
    <span
      ><strong>Tip:</strong> Install TKA as a Progressive Web App for a distraction-free,
      fullscreen-like experience!</span
    >
  </div>

  <!-- Info Note (only if haptic not supported) -->
  {#if !isHapticSupported}
    <div class="info-banner">
      <i class="fas fa-info-circle"></i>
      <span>Haptic feedback requires a device with vibration support</span>
    </div>
  {/if}
</div>

<style>
  .experience-tab {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 600px;
    margin: 0 auto;
    padding: 8px;
  }

  /* Setting Card - Modern iOS/Material Design style */
  .setting-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.06);
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 80px;
  }

  .setting-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .setting-card.disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  /* Card Icon - Large colorful icons */
  .card-icon {
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.2),
      rgba(99, 102, 241, 0.1)
    );
    color: #8b8ff8;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .haptic-icon {
    background: linear-gradient(
      135deg,
      rgba(236, 72, 153, 0.2),
      rgba(236, 72, 153, 0.1)
    );
    color: #f472b6;
  }

  .motion-icon {
    background: linear-gradient(
      135deg,
      rgba(34, 197, 94, 0.2),
      rgba(34, 197, 94, 0.1)
    );
    color: #4ade80;
  }

  .fullscreen-icon {
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.2),
      rgba(59, 130, 246, 0.1)
    );
    color: #60a5fa;
  }

  .setting-card:hover .card-icon {
    transform: scale(1.1) rotate(-5deg);
  }

  /* Card Content */
  .card-content {
    flex: 1;
    min-width: 0;
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .card-header h3 {
    font-size: 17px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    letter-spacing: -0.01em;
  }

  .card-description {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
  }

  /* Badge for unavailable features */
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    color: #f87171;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* Modern Toggle Switch */
  .toggle-switch {
    flex-shrink: 0;
    position: relative;
    display: inline-block;
    width: 52px;
    height: 32px;
    cursor: pointer;
  }

  .toggle-switch input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    margin: 0;
    z-index: 1; /* Ensure it's above the slider */
  }

  .toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 16px;
  }

  .toggle-slider:before {
    position: absolute;
    content: "";
    height: 24px;
    width: 24px;
    left: 2px;
    bottom: 2px;
    background: white;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  input:checked + .toggle-slider {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-color: #6366f1;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
  }

  input:checked + .toggle-slider:before {
    transform: translateX(20px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  input:focus-visible + .toggle-slider {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
  }

  input:disabled + .toggle-slider {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Hover effect on toggle */
  .toggle-switch:hover .toggle-slider {
    background: rgba(255, 255, 255, 0.2);
  }

  .toggle-switch:hover input:checked + .toggle-slider {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.5);
  }

  /* Info Banner */
  .info-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background: rgba(59, 130, 246, 0.1);
    border: 1.5px solid rgba(59, 130, 246, 0.25);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.85);
    font-size: 13px;
    line-height: 1.4;
  }

  .info-banner i {
    font-size: 16px;
    color: #60a5fa;
    flex-shrink: 0;
  }

  .info-banner.pwa-recommendation {
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.15),
      rgba(99, 102, 241, 0.1)
    );
    border-color: rgba(139, 92, 246, 0.3);
  }

  .info-banner.pwa-recommendation i {
    color: #a78bfa;
  }

  /* Responsive adjustments */
  @media (max-width: 480px) {
    .experience-tab {
      padding: 4px;
      gap: 12px;
    }

    .setting-card {
      padding: 16px;
      min-height: 72px;
      gap: 12px;
    }

    .card-icon {
      width: 44px;
      height: 44px;
      font-size: 20px;
    }

    .card-header h3 {
      font-size: 16px;
    }

    .toggle-switch {
      width: 48px;
      height: 28px;
    }

    .toggle-slider:before {
      height: 22px;
      width: 22px;
    }

    input:checked + .toggle-slider:before {
      transform: translateX(18px);
    }

    .badge {
      font-size: 10px;
      padding: 3px 8px;
    }

    .info-banner {
      padding: 12px 14px;
      font-size: 12px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .setting-card,
    .card-icon,
    .toggle-slider,
    .toggle-slider:before {
      transition: none;
    }

    .setting-card:hover {
      transform: none;
    }

    .setting-card:hover .card-icon {
      transform: none;
    }
  }

  /* High contrast */
  @media (prefers-contrast: high) {
    .setting-card {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.3);
    }

    .setting-card:hover {
      border-color: #6366f1;
    }

    .toggle-slider {
      border-width: 2px;
    }
  }
</style>
