<!--
FullscreenPrompt.svelte - Intelligent fullscreen prompt

Shows when:
- Device is mobile (not desktop)
- Fullscreen API is supported
- NOT currently in fullscreen mode

This creates a better UX than height-based thresholds by directly detecting
the actual fullscreen state rather than inferring from viewport size.
-->
<script lang="ts">
  import type { IDeviceDetector } from "$lib/shared/device/services/contracts/IDeviceDetector";
  import type { IMobileFullscreenService } from "$lib/shared/mobile/services/contracts/IMobileFullscreenService";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let showPrompt = $state(false);
  let isEmergencyMode = $state(false); // Track if we're in emergency mode
  let message = $state("");

  let deviceDetector: IDeviceDetector | null = null;
  let fullscreenService: IMobileFullscreenService | null = null;

  // Session-based dismissal (resets on page reload)
  const DISMISSAL_KEY = "tka-fullscreen-prompt-dismissed-session";
  let hasBeenDismissed = $state(false);

  // Fun, inviting messages that make users want to tap
  const messages = [
    "Tap to Build Movement ✨",
    "Enter the Constructor 🎯",
    "Let's Create Sequences 🌟",
    "Tap to Choreograph ⚡",
    "Begin Your Sequence 🎨",
    "Create Something Beautiful ✨",
    "Build Your Vision 🎭",
    "Tap to Start Creating 🚀",
  ];

  onMount(() => {
    try {
      // Check if user dismissed this session
      if (typeof sessionStorage !== "undefined") {
        hasBeenDismissed = sessionStorage.getItem(DISMISSAL_KEY) === "true";
      }

      // Resolve services
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      fullscreenService = resolve<IMobileFullscreenService>(
        TYPES.IMobileFullscreenService
      );

      // Pick a random message
      message = messages[Math.floor(Math.random() * messages.length)];

      // Initial check
      checkShouldPrompt();

      // Listen for fullscreen state changes
      const unsubscribe = fullscreenService?.onFullscreenChange(() => {
        checkShouldPrompt();
      });

      // Re-check on resize (device orientation change)
      const handleResize = () => checkShouldPrompt();
      window.addEventListener("resize", handleResize);

      return () => {
        unsubscribe?.();
        window.removeEventListener("resize", handleResize);
      };
    } catch (error) {
      console.error("Failed to initialize FullscreenPrompt:", error);
    }
  });

  function checkShouldPrompt() {
    if (!deviceDetector || !fullscreenService) {
      showPrompt = false;
      return;
    }

    // 📱 Only show on mobile devices (not desktop)
    const isMobile = deviceDetector.isMobile();

    // 🔲 Check if fullscreen API is supported
    const fullscreenSupported = fullscreenService.isFullscreenSupported();

    // ✅ Check if currently in fullscreen mode
    const isCurrentlyFullscreen = fullscreenService.isFullscreen();

    // 📐 Skip if already installed as PWA (has native fullscreen)
    const isPWA = fullscreenService.isPWA();

    // 🔧 Skip in development mode (localhost) to avoid interrupting debugging
    const isDevelopment =
      typeof window !== "undefined" &&
      (window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1" ||
        window.location.hostname.includes("192.168"));

    // 📱 Check orientation
    const isLandscape =
      typeof window !== "undefined" && window.innerWidth > window.innerHeight;

    // 🚨 EMERGENCY MODE: Extremely constrained vertical space
    // When height is critically low, ALWAYS show (even in portrait, even in dev)
    const isExtremelyConstrained =
      typeof window !== "undefined" && window.innerHeight < 300;

    // 🎯 SMART LOGIC: Show prompt in two scenarios:

    // SCENARIO 1: Emergency mode (extremely constrained)
    // - Always show when height < 300px (takes priority over all other checks)
    // - Can't dismiss in emergency mode (need fullscreen to use app)
    const emergencyMode =
      fullscreenSupported && !isCurrentlyFullscreen && isExtremelyConstrained;

    // SCENARIO 2: Normal landscape mode (smart detection)
    // - On mobile device
    // - Fullscreen is supported
    // - NOT currently in fullscreen
    // - NOT running as PWA
    // - NOT in development mode (allow debugging)
    // - In landscape mode (portrait works fine without fullscreen)
    // - NOT been dismissed this session
    const normalMode =
      isMobile &&
      fullscreenSupported &&
      !isCurrentlyFullscreen &&
      !isPWA &&
      !isDevelopment &&
      isLandscape &&
      !hasBeenDismissed &&
      !isExtremelyConstrained; // Don't use normal mode when in emergency

    showPrompt = emergencyMode || normalMode;
    isEmergencyMode = emergencyMode;

    if (emergencyMode) {
      console.log(
        "🚨 EMERGENCY: Showing fullscreen prompt (height < 300px - can't dismiss)"
      );
    } else if (normalMode) {
      console.log(
        "🎯 Showing fullscreen prompt (landscape mobile, not in fullscreen)"
      );
    } else if (isDevelopment && isMobile && !isExtremelyConstrained) {
      console.log("🔧 Skipping fullscreen prompt (development mode)");
    }
  }

  async function requestFullscreen() {
    if (!fullscreenService) return;

    try {
      const success = await fullscreenService.requestFullscreen();
      if (success) {
        console.log("✅ Entered fullscreen mode");
        // Prompt will hide automatically via fullscreen change listener
      }
    } catch (error) {
      console.warn("Fullscreen request failed:", error);
      // User can try again by tapping
    }
  }

  function dismissPrompt() {
    hasBeenDismissed = true;
    showPrompt = false;
    if (typeof sessionStorage !== "undefined") {
      sessionStorage.setItem(DISMISSAL_KEY, "true");
    }
    console.log("⏸️ Fullscreen prompt dismissed for this session");
  }
</script>

{#if showPrompt}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="fullscreen-prompt-overlay"
    onclick={requestFullscreen}
    role="button"
    tabindex="0"
    aria-label="Enter fullscreen to start building"
  >
    <div class="fullscreen-prompt-content">
      <h2 class="prompt-title">{message}</h2>
      <p class="prompt-subtitle">
        {#if isEmergencyMode}
          Limited space detected - tap anywhere for fullscreen
        {:else}
          Tap anywhere to enter fullscreen
        {/if}
      </p>

      <!-- Only show dismiss button in normal mode, not emergency -->
      {#if !isEmergencyMode}
        <button
          class="dismiss-button"
          onclick={dismissPrompt}
          aria-label="Skip fullscreen for now"
          title="Skip fullscreen (this session)"
        >
          Skip
        </button>
      {/if}
    </div>
  </div>
{/if}

<style>
  .fullscreen-prompt-overlay {
    /* Full screen overlay */
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10000;

    /* Remove button styling */
    border: none;
    padding: 0;
    margin: 0;
    font: inherit;
    color: inherit;
    background: none;

    /* Semi-transparent dark background */
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(12px);

    /* Center content */
    display: flex;
    align-items: center;
    justify-content: center;

    /* Clickable */
    cursor: pointer;

    /* Smooth fade-in */
    animation: fadeIn 0.3s ease-out;
  }

  .fullscreen-prompt-overlay:hover {
    background: rgba(0, 0, 0, 0.95);
  }

  .fullscreen-prompt-overlay:active {
    background: rgba(0, 0, 0, 0.98);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .fullscreen-prompt-content {
    /* Prevent click events from bubbling (parent handles click) */
    pointer-events: none;

    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(12px, 3vh, 20px);

    /* Scale-in animation */
    animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  @keyframes scaleIn {
    from {
      transform: scale(0.9);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  .prompt-title {
    font-size: clamp(20px, 5vw, 32px);
    font-weight: 700;
    color: white;
    margin: 0;
    text-align: center;
    line-height: 1.3;
    letter-spacing: 0.5px;
    animation: glow 2s ease-in-out infinite;
  }

  @keyframes glow {
    0%,
    100% {
      opacity: 0.9;
      transform: scale(1);
    }
    50% {
      opacity: 1;
      transform: scale(1.02);
    }
  }
</style>
