<script lang="ts">
  /**
   * Animation Coordinator Component
   *
   * Orchestrates all animation business logic, service resolution, and state management.
   * AnimationPanel is a pure presentation component that receives everything as props.
   *
   * Domain: Create module - Animation Panel Coordination
   */

  import AnimationPanel from "../../../animate/components/AnimationPanel.svelte";
  import type {
    AnimationExportFormat,
    GifExportProgress,
    IAnimationPlaybackController,
    IGifExportOrchestrator,
  } from "$create/animate/services/contracts";
  import { createAnimationPanelState } from "$create/animate/state/animation-panel-state.svelte";
  import { loadSequenceForAnimation } from "$create/animate/utils/sequence-loader";
  import type { ISequenceService } from "$create/shared";
  import { resolve, TYPES } from "$shared";
  import type { IHapticFeedbackService } from "$shared/application/services/contracts";
  import { onMount } from "svelte";
  import {
    ANIMATION_LOAD_DELAY_MS,
    ANIMATION_AUTO_START_DELAY_MS,
    GIF_EXPORT_SUCCESS_DELAY_MS,
  } from "$create/animate/constants/timing";
  import { getCreateModuleContext } from "../../context";

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState, panelState } = ctx;

  // Props (only bindable props remain)
  let {
    animatingBeatNumber = $bindable(),
  }: {
    animatingBeatNumber?: number | null;
  } = $props();

  // Services
  let sequenceService: ISequenceService | null = null;
  let playbackController: IAnimationPlaybackController | null = null;
  let hapticService: IHapticFeedbackService | null = null;
  let gifExportOrchestrator: IGifExportOrchestrator | null = null;
  let animationCanvas: HTMLCanvasElement | null = null;

  // Animation state
  const animationPanelState = createAnimationPanelState();

  // GIF Export state
  let showExportSheet = $state(false);
  let isExporting = $state(false);
  let exportProgress = $state<GifExportProgress | null>(null);

  // Toast notification state
  let showExportToast = $state(false);
  let exportToastType = $state<"success" | "error">("success");
  let exportToastMessage = $state("");

  // Derived: Current letter from sequence data
  let currentLetter = $derived.by(() => {
    if (!animationPanelState.sequenceData) return null;

    const currentBeat = animationPanelState.currentBeat;

    // Before animation starts (beat 0 and not playing) = start position
    if (
      currentBeat === 0 &&
      !animationPanelState.isPlaying &&
      animationPanelState.sequenceData.startPosition
    ) {
      return animationPanelState.sequenceData.startPosition.letter || null;
    }

    // During animation: show beat letters
    if (
      animationPanelState.sequenceData.beats &&
      animationPanelState.sequenceData.beats.length > 0
    ) {
      const beatIndex = Math.floor(currentBeat);
      const clampedIndex = Math.max(
        0,
        Math.min(beatIndex, animationPanelState.sequenceData.beats.length - 1)
      );
      return (
        animationPanelState.sequenceData.beats[clampedIndex]?.letter || null
      );
    }

    return null;
  });

  // Derived: Current beat data (including motions for turn calculations)
  let currentBeatData = $derived.by(() => {
    if (!animationPanelState.sequenceData) return null;

    const currentBeat = animationPanelState.currentBeat;

    // Before animation starts (beat 0 and not playing) = start position
    if (
      currentBeat === 0 &&
      !animationPanelState.isPlaying &&
      animationPanelState.sequenceData.startPosition
    ) {
      return animationPanelState.sequenceData.startPosition;
    }

    // During animation: show beat data
    if (
      animationPanelState.sequenceData.beats &&
      animationPanelState.sequenceData.beats.length > 0
    ) {
      const beatIndex = Math.floor(currentBeat);
      const clampedIndex = Math.max(
        0,
        Math.min(beatIndex, animationPanelState.sequenceData.beats.length - 1)
      );
      return animationPanelState.sequenceData.beats[clampedIndex] || null;
    }

    return null;
  });

  // Resolve services on mount
  onMount(() => {
    try {
      sequenceService = resolve<ISequenceService>(TYPES.ISequenceService);
      playbackController = resolve<IAnimationPlaybackController>(
        TYPES.IAnimationPlaybackController
      );
      hapticService = resolve<IHapticFeedbackService>(
        TYPES.IHapticFeedbackService
      );
      gifExportOrchestrator = resolve<IGifExportOrchestrator>(
        TYPES.IGifExportOrchestrator
      );
    } catch (error) {
      console.error("Failed to resolve animation services:", error);
      animationPanelState.setError("Failed to initialize animation services");
    }

    return undefined;
  });

  // Load and auto-start animation when panel becomes visible
  $effect(() => {
    const sequence = CreateModuleState.sequenceState.currentSequence;
    const isOpen = panelState.isAnimationPanelOpen;

    if (isOpen && sequence && sequenceService && playbackController) {
      animationPanelState.setLoading(true);
      animationPanelState.setError(null);

      const loadTimeout = setTimeout(() => {
        loadAndStartAnimation(sequence);
      }, ANIMATION_LOAD_DELAY_MS);

      return () => clearTimeout(loadTimeout);
    }
    return undefined;
  });

  async function loadAndStartAnimation(sequence: any) {
    if (!sequenceService || !playbackController) return;

    animationPanelState.setLoading(true);
    animationPanelState.setError(null);

    try {
      // Load sequence
      const result = await loadSequenceForAnimation(sequence, sequenceService);

      if (!result.success || !result.sequence) {
        throw new Error(result.error || "Failed to load sequence");
      }

      // Initialize playback controller
      animationPanelState.setShouldLoop(true);
      const success = playbackController.initialize(
        result.sequence,
        animationPanelState
      );

      if (!success) {
        throw new Error("Failed to initialize animation playback");
      }

      animationPanelState.setSequenceData(result.sequence);

      // Auto-start animation
      setTimeout(() => {
        playbackController?.togglePlayback();
      }, ANIMATION_AUTO_START_DELAY_MS);
    } catch (err) {
      console.error("❌ Failed to load sequence:", err);
      animationPanelState.setError(
        err instanceof Error ? err.message : "Failed to load sequence"
      );
    } finally {
      animationPanelState.setLoading(false);
    }
  }

  // Notify parent when current beat changes
  $effect(() => {
    const currentBeat = animationPanelState.currentBeat;
    if (animationPanelState.isPlaying || currentBeat > 0) {
      animatingBeatNumber = Math.floor(currentBeat) + 1;
    }
  });

  // Cleanup on component destroy
  $effect(() => {
    return () => {
      if (playbackController) {
        playbackController.dispose();
      }
    };
  });

  // Event handlers
  function handleClose() {
    hapticService?.trigger("selection");

    if (playbackController) {
      playbackController.dispose();
    }

    panelState.closeAnimationPanel();
    animatingBeatNumber = null;
  }

  function handleSpeedChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newSpeed = parseFloat(target.value);
    hapticService?.trigger("selection");
    playbackController?.setSpeed(newSpeed);
  }

  function handleOpenExport() {
    console.log("🎬 handleOpenExport called");
    hapticService?.trigger("selection");
    showExportSheet = true;
    console.log("🎬 showExportSheet set to:", showExportSheet);
  }

  function handleCloseExport() {
    if (!isExporting) {
      showExportSheet = false;
      exportProgress = null;
    }
  }

  async function handleExport(format: AnimationExportFormat) {
    if (!gifExportOrchestrator || !playbackController) {
      console.error("Export services not ready");
      hapticService?.trigger("error");
      return;
    }

    if (!animationCanvas) {
      console.error("Canvas not found");
      hapticService?.trigger("error");
      return;
    }

    try {
      isExporting = true;

      // Execute export using orchestrator service
      await gifExportOrchestrator.executeExport(
        animationCanvas,
        playbackController,
        animationPanelState,
        (progress) => {
          exportProgress = progress;
        },
        { format }
      );

      // Trigger success haptic feedback
      hapticService?.trigger("success");

      // Show success toast
      exportToastType = "success";
      exportToastMessage = `Your ${format.toUpperCase()} animation has been downloaded successfully!`;
      showExportToast = true;

      // Close sheet and reset state
      showExportSheet = false;
      isExporting = false;
      exportProgress = null;
    } catch (error) {
      console.error("GIF export failed:", error);
      // Trigger error haptic feedback
      hapticService?.trigger("error");

      // Show error toast
      exportToastType = "error";
      exportToastMessage =
        error instanceof Error ? error.message : "Failed to export animation";
      showExportToast = true;

      // Reset export state
      isExporting = false;
      exportProgress = null;
    }
  }

  function handleCancelExport() {
    // Trigger selection haptic feedback for cancel action
    hapticService?.trigger("selection");

    if (gifExportOrchestrator) {
      gifExportOrchestrator.cancelExport();
    }
    isExporting = false;
    exportProgress = null;
    handleCloseExport();
  }

  function handleDismissToast() {
    showExportToast = false;
  }
  function handleCanvasReady(canvas: HTMLCanvasElement | null) {
    animationCanvas = canvas;
  }
</script>

<AnimationPanel
  show={panelState.isAnimationPanelOpen}
  combinedPanelHeight={panelState.combinedPanelHeight}
  isSideBySideLayout={ctx.layout.shouldUseSideBySideLayout}
  loading={animationPanelState.loading}
  error={animationPanelState.error}
  speed={animationPanelState.speed}
  blueProp={animationPanelState.bluePropState}
  redProp={animationPanelState.redPropState}
  gridVisible={true}
  gridMode={animationPanelState.sequenceData?.gridMode}
  letter={currentLetter}
  beatData={currentBeatData}
  {showExportSheet}
  {isExporting}
  {exportProgress}
  {showExportToast}
  {exportToastType}
  {exportToastMessage}
  onClose={handleClose}
  onSpeedChange={handleSpeedChange}
  onOpenExport={handleOpenExport}
  onCloseExport={handleCloseExport}
  onExport={handleExport}
  onCancelExport={handleCancelExport}
  onCanvasReady={handleCanvasReady}
  onDismissToast={handleDismissToast}
/>
