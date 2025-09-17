/**
 * Navigation State - Global Navigation State Management
 * 
 * Manages global navigation state including current modes for tabs with sub-modes.
 * This provides a centralized way to track and update navigation state across the app.
 */

import type { ModeOption } from "../domain/types";

// Build modes configuration
export const BUILD_MODES: ModeOption[] = [
  { 
    id: "construct", 
    label: "Construct", 
    icon: "🔨", 
    description: "Build sequences step by step",
    color: "#3b82f6"
  },
  { 
    id: "generate", 
    label: "Generate", 
    icon: "⚡", 
    description: "Auto-create sequences",
    color: "#10b981"
  },
  { 
    id: "edit", 
    label: "Edit", 
    icon: "🔧", 
    description: "Modify existing sequences",
    color: "#f59e0b"
  },
  { 
    id: "export", 
    label: "Export", 
    icon: "🔤", 
    description: "Share and save sequences",
    color: "#8b5cf6"
  }
];

// Learn modes configuration
export const LEARN_MODES: ModeOption[] = [
  { 
    id: "codex", 
    label: "Codex", 
    icon: "📖", 
    description: "Browse and reference all TKA letters",
    color: "#3b82f6"
  },
  { 
    id: "quiz", 
    label: "Quiz", 
    icon: "🧠", 
    description: "Interactive learning and testing",
    color: "#10b981"
  },
  { 
    id: "read", 
    label: "Read", 
    icon: "📚", 
    description: "Beautiful PDF flipbook reader",
    color: "#f59e0b"
  }
];

/**
 * Creates navigation state for managing current modes
 */
export function createNavigationState() {
  // State
  let currentBuildMode = $state<string>("construct");
  let currentLearnMode = $state<string>("codex");

  // Load persisted state
  if (typeof localStorage !== "undefined") {
    const savedBuildMode = localStorage.getItem("tka-current-build-mode");
    if (savedBuildMode && BUILD_MODES.some(m => m.id === savedBuildMode)) {
      currentBuildMode = savedBuildMode;
    }

    const savedLearnMode = localStorage.getItem("tka-current-learn-mode");
    if (savedLearnMode && LEARN_MODES.some(m => m.id === savedLearnMode)) {
      currentLearnMode = savedLearnMode;
    }
  }

  // Actions
  function setBuildMode(mode: string) {
    if (BUILD_MODES.some(m => m.id === mode)) {
      currentBuildMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-build-mode", mode);
      }
    }
  }

  function setLearnMode(mode: string) {
    if (LEARN_MODES.some(m => m.id === mode)) {
      currentLearnMode = mode;
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("tka-current-learn-mode", mode);
      }
    }
  }

  return {
    // Readonly state
    get currentBuildMode() { return currentBuildMode; },
    get currentLearnMode() { return currentLearnMode; },
    
    // Mode configurations
    get buildModes() { return BUILD_MODES; },
    get learnModes() { return LEARN_MODES; },
    
    // Actions
    setBuildMode,
    setLearnMode
  };
}

// Global navigation state instance
export const navigationState = createNavigationState();
