/**
 * Animator module exports
 * Main entry point for the animation system
 */

// Core types (refactored into focused modules)
export * from "./types/index.js";

// Constants
export * from "./constants/index.js";

// Animation engine
export { SequenceAnimationEngine as StandalonePortedEngine } from "../../animator/core/engine/sequence-animation-engine.js";

// Math services (replaces standalone-math.js)
export * from "../../animator/utils/math/index.js";

// TODO: File utilities (PNG parser path issues)
// export { extractSequenceFromPNG } from "../../../animator/src/lib/animator/utils/file/png-parser.js";
// export type { PNGParseResult } from "../../../animator/src/lib/animator/utils/file/png-parser.js";

// Canvas utilities
export { CanvasRenderer } from "../../animator/utils/canvas/CanvasRenderer.js";
export { SVGGenerator } from "../../animator/utils/canvas/SVGGenerator.js";

// SVG utilities
export { svgStringToImage } from "./svgStringToImage.js";

// Components (based on standalone_animator.html reference implementation)
export { default as AnimatorCanvas } from "./AnimatorCanvas.svelte";
export { default as GridManager } from "./GridManager.svelte";
