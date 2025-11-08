<!-- AccessibilityTab.svelte - Modern User Experience Settings -->
<script lang="ts">
  import { browser } from "$app/environment";
  import type {
    IHapticFeedbackService,
    IMobileFullscreenService,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { nuclearCacheClear } from "$shared/auth";
  import { onMount } from "svelte";
  import EnhancedPWAInstallGuide from "$lib/shared/mobile/components/EnhancedPWAInstallGuide.svelte";

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
  let clearing = $state(false);
  let showPWAGuide = $state(false);

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
      return undefined;
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

  async function clearCache() {
    if (
      !confirm(
        "⚠️ CLEAR ALL CACHE ⚠️\n\n" +
          "This will DELETE ALL cached data and reload the page.\n\n" +
          "Continue?"
      )
    ) {
      return;
    }

    clearing = true;
    try {
      await nuclearCacheClear();
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    } catch (error) {
      console.error("Failed to clear cache:", error);
      alert("Failed to clear cache. Check console.");
      clearing = false;
    }
  }
</script>

<div class="experience-tab">
  <!-- Settings List - Clean & Minimal -->
  <div class="settings-list">
    <!-- Haptic Feedback -->
    <div class="setting-row" class:disabled={!isHapticSupported}>
      <div class="setting-label">
        <span>Haptic Feedback</span>
        {#if !isHapticSupported}
          <span class="unavailable">(unavailable)</span>
        {/if}
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

    <!-- Reduced Motion -->
    <div class="setting-row">
      <div class="setting-label">
        <span>Reduce Motion</span>
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

    <!-- Fullscreen Mode -->
    {#if !isPWA}
      <div class="setting-row" class:disabled={!isFullscreenSupported}>
        <div class="setting-label">
          <span>Fullscreen Mode</span>
          {#if !isFullscreenSupported}
            <span class="unavailable">(unavailable)</span>
          {/if}
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

    <!-- Cache Clear -->
    <div class="setting-row cache-row">
      <div class="setting-label">
        <span>Clear Cache</span>
      </div>
      <button
        class="clear-cache-btn"
        onclick={clearCache}
        disabled={clearing}
        aria-label="Clear all cached data and reload the app"
      >
        {clearing ? "Clearing..." : "Clear"}
      </button>
    </div>
  </div>

  <!-- PWA Tip - Minimal -->
  <div class="pwa-tip">
    <span class="tip-text">
      💡 <strong>Tip:</strong> Install as PWA for best experience
    </span>
    <button class="learn-how-btn" onclick={() => (showPWAGuide = true)}>
      Learn How
    </button>
  </div>
</div>

<!-- PWA Installation Guide -->
<EnhancedPWAInstallGuide bind:showGuide={showPWAGuide} />

<style>
  .experience-tab {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 600px;
    margin: 0 auto;
    padding: 0 8px;
  }

  /* Settings List Container */
  .settings-list {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
  }

  /* Individual Setting Row */
  .setting-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    transition: background 0.2s;
  }

  .setting-row:last-child {
    border-bottom: none;
  }

  .setting-row:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.02);
  }

  .setting-row.disabled {
    opacity: 0.5;
  }

  .setting-row.cache-row {
    background: rgba(239, 68, 68, 0.05);
  }

  /* Setting Label */
  .setting-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 15px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.95);
  }

  .setting-label .unavailable {
    font-size: 12px;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.5);
  }

  /* Compact Toggle Switch */
  .toggle-switch {
    flex-shrink: 0;
    position: relative;
    display: inline-block;
    width: 48px;
    height: 28px;
    cursor: pointer;
  }

  .toggle-switch input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
    margin: 0;
    z-index: 2;
    top: 0;
    left: 0;
  }

  .toggle-slider {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    transition: all 0.3s;
  }

  .toggle-slider:before {
    content: "";
    position: absolute;
    height: 22px;
    width: 22px;
    left: 3px;
    bottom: 3px;
    background: white;
    border-radius: 50%;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  input:checked + .toggle-slider {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
  }

  input:checked + .toggle-slider:before {
    transform: translateX(20px);
  }

  input:disabled + .toggle-slider {
    opacity: 0.5;
  }

  /* Clear Cache Button */
  .clear-cache-btn {
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    min-height: 44px;
    transition: all 0.2s;
  }

  .clear-cache-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
  }

  .clear-cache-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* PWA Tip */
  .pwa-tip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 10px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.85);
  }

  .tip-text {
    flex: 1;
  }

  .pwa-tip strong {
    color: #a78bfa;
  }

  .learn-how-btn {
    flex-shrink: 0;
    padding: 8px 16px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .learn-how-btn:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
  }

  .learn-how-btn:active {
    transform: translateY(0);
  }

  /* Accessibility */
  @media (prefers-reduced-motion: reduce) {
    .setting-row,
    .toggle-slider,
    .toggle-slider:before,
    .clear-cache-btn,
    .learn-how-btn {
      transition: none;
    }

    .learn-how-btn:hover,
    .learn-how-btn:active {
      transform: none;
    }
  }

  @media (prefers-contrast: high) {
    .settings-list {
      border-width: 2px;
      border-color: rgba(255, 255, 255, 0.3);
    }
  }
</style>
