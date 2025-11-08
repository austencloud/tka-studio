/**
 * Animate Module State
 *
 * Manages state for the Animate module including:
 * - Current animation mode (single, tunnel, mirror, grid)
 * - Selected sequences for each mode
 * - Mode-specific settings (colors, mirror axis, rotation offsets)
 * - Sequence browser panel state
 */

import type { SequenceData, GridMode } from "$shared";

export type AnimateMode = "single" | "tunnel" | "mirror" | "grid";

export type MirrorAxis = "vertical" | "horizontal";

export type TunnelColors = {
  primary: {
    blue: string;
    red: string;
  };
  secondary: {
    blue: string;
    red: string;
  };
};

export type AnimateModuleState = {
  // Current mode
  readonly currentMode: AnimateMode;

  // Sequence selection
  readonly primarySequence: SequenceData | null;
  readonly secondarySequence: SequenceData | null;
  readonly gridSequences: [
    SequenceData | null,
    SequenceData | null,
    SequenceData | null,
    SequenceData | null,
  ];

  // Sequence browser panel
  readonly isSequenceBrowserOpen: boolean;
  readonly browserMode:
    | "primary"
    | "secondary"
    | "grid-0"
    | "grid-1"
    | "grid-2"
    | "grid-3";

  // Tunnel mode settings
  readonly tunnelColors: TunnelColors;
  readonly tunnelOpacity: number;

  // Mirror mode settings
  readonly mirrorAxis: MirrorAxis;
  readonly mirrorShowOriginal: boolean;

  // Grid mode settings
  readonly gridRotationOffsets: [number, number, number, number];

  // Playback state
  readonly isPlaying: boolean;
  readonly speed: number;
  readonly shouldLoop: boolean;

  // State mutators
  setCurrentMode: (mode: AnimateMode) => void;

  // Sequence selection
  setPrimarySequence: (sequence: SequenceData | null) => void;
  setSecondarySequence: (sequence: SequenceData | null) => void;
  setGridSequence: (
    index: 0 | 1 | 2 | 3,
    sequence: SequenceData | null
  ) => void;

  // Browser panel
  openSequenceBrowser: (
    mode: "primary" | "secondary" | "grid-0" | "grid-1" | "grid-2" | "grid-3"
  ) => void;
  closeSequenceBrowser: () => void;

  // Tunnel settings
  setTunnelColors: (colors: TunnelColors) => void;
  setTunnelOpacity: (opacity: number) => void;

  // Mirror settings
  setMirrorAxis: (axis: MirrorAxis) => void;
  setMirrorShowOriginal: (show: boolean) => void;

  // Grid settings
  setGridRotationOffset: (index: 0 | 1 | 2 | 3, offset: number) => void;

  // Playback controls
  setIsPlaying: (playing: boolean) => void;
  setSpeed: (speed: number) => void;
  setShouldLoop: (loop: boolean) => void;

  // Reset
  reset: () => void;
};

// Default tunnel colors (red/blue for primary, green/purple for secondary)
const DEFAULT_TUNNEL_COLORS: TunnelColors = {
  primary: {
    blue: "#3b82f6",
    red: "#ef4444",
  },
  secondary: {
    blue: "#10b981",
    red: "#a855f7",
  },
};

export function createAnimateModuleState(): AnimateModuleState {
  // Current mode
  let currentMode = $state<AnimateMode>("single");

  // Sequence selection
  let primarySequence = $state<SequenceData | null>(null);
  let secondarySequence = $state<SequenceData | null>(null);
  let gridSequences = $state<
    [
      SequenceData | null,
      SequenceData | null,
      SequenceData | null,
      SequenceData | null,
    ]
  >([null, null, null, null]);

  // Sequence browser panel
  let isSequenceBrowserOpen = $state<boolean>(false);
  let browserMode = $state<
    "primary" | "secondary" | "grid-0" | "grid-1" | "grid-2" | "grid-3"
  >("primary");

  // Tunnel mode settings
  let tunnelColors = $state<TunnelColors>({ ...DEFAULT_TUNNEL_COLORS });
  let tunnelOpacity = $state<number>(0.7);

  // Mirror mode settings
  let mirrorAxis = $state<MirrorAxis>("vertical");
  let mirrorShowOriginal = $state<boolean>(true);

  // Grid mode settings
  let gridRotationOffsets = $state<[number, number, number, number]>([
    0, 90, 180, 270,
  ]);

  // Playback state
  let isPlaying = $state<boolean>(false);
  let speed = $state<number>(1.0);
  let shouldLoop = $state<boolean>(true);

  return {
    // Getters
    get currentMode() {
      return currentMode;
    },
    get primarySequence() {
      return primarySequence;
    },
    get secondarySequence() {
      return secondarySequence;
    },
    get gridSequences() {
      return gridSequences;
    },
    get isSequenceBrowserOpen() {
      return isSequenceBrowserOpen;
    },
    get browserMode() {
      return browserMode;
    },
    get tunnelColors() {
      return tunnelColors;
    },
    get tunnelOpacity() {
      return tunnelOpacity;
    },
    get mirrorAxis() {
      return mirrorAxis;
    },
    get mirrorShowOriginal() {
      return mirrorShowOriginal;
    },
    get gridRotationOffsets() {
      return gridRotationOffsets;
    },
    get isPlaying() {
      return isPlaying;
    },
    get speed() {
      return speed;
    },
    get shouldLoop() {
      return shouldLoop;
    },

    // Mode switching
    setCurrentMode(mode: AnimateMode) {
      currentMode = mode;
      console.log("🎬 AnimateModuleState: Mode changed to", mode);
    },

    // Sequence selection
    setPrimarySequence(sequence: SequenceData | null) {
      primarySequence = sequence;
      console.log("🎬 AnimateModuleState: Primary sequence set", sequence?.id);
    },

    setSecondarySequence(sequence: SequenceData | null) {
      secondarySequence = sequence;
      console.log(
        "🎬 AnimateModuleState: Secondary sequence set",
        sequence?.id
      );
    },

    setGridSequence(index: 0 | 1 | 2 | 3, sequence: SequenceData | null) {
      const newGridSequences = [...gridSequences] as [
        SequenceData | null,
        SequenceData | null,
        SequenceData | null,
        SequenceData | null,
      ];
      newGridSequences[index] = sequence;
      gridSequences = newGridSequences;
      console.log(
        `🎬 AnimateModuleState: Grid sequence ${index} set`,
        sequence?.id
      );
    },

    // Browser panel
    openSequenceBrowser(
      mode: "primary" | "secondary" | "grid-0" | "grid-1" | "grid-2" | "grid-3"
    ) {
      browserMode = mode;
      isSequenceBrowserOpen = true;
      console.log("🎬 AnimateModuleState: Browser opened for", mode);
    },

    closeSequenceBrowser() {
      isSequenceBrowserOpen = false;
      console.log("🎬 AnimateModuleState: Browser closed");
    },

    // Tunnel settings
    setTunnelColors(colors: TunnelColors) {
      tunnelColors = { ...colors };
    },

    setTunnelOpacity(opacity: number) {
      tunnelOpacity = Math.max(0, Math.min(1, opacity));
    },

    // Mirror settings
    setMirrorAxis(axis: MirrorAxis) {
      mirrorAxis = axis;
    },

    setMirrorShowOriginal(show: boolean) {
      mirrorShowOriginal = show;
    },

    // Grid settings
    setGridRotationOffset(index: 0 | 1 | 2 | 3, offset: number) {
      const newOffsets = [...gridRotationOffsets] as [
        number,
        number,
        number,
        number,
      ];
      newOffsets[index] = offset % 360;
      gridRotationOffsets = newOffsets;
    },

    // Playback controls
    setIsPlaying(playing: boolean) {
      isPlaying = playing;
    },

    setSpeed(newSpeed: number) {
      speed = Math.max(0.1, Math.min(3.0, newSpeed));
    },

    setShouldLoop(loop: boolean) {
      shouldLoop = loop;
    },

    // Reset
    reset() {
      currentMode = "single";
      primarySequence = null;
      secondarySequence = null;
      gridSequences = [null, null, null, null];
      isSequenceBrowserOpen = false;
      browserMode = "primary";
      tunnelColors = { ...DEFAULT_TUNNEL_COLORS };
      tunnelOpacity = 0.7;
      mirrorAxis = "vertical";
      mirrorShowOriginal = true;
      gridRotationOffsets = [0, 90, 180, 270];
      isPlaying = false;
      speed = 1.0;
      shouldLoop = true;
      console.log("🎬 AnimateModuleState: Reset");
    },
  };
}
