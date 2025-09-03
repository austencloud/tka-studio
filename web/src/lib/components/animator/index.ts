/**
 * Animator module exports
 * Main entry point for the animation system
 */


// Animation engine
export { SequenceAnimationEngine as StandalonePortedEngine } from "$implementations";

// Math services are now in services/implementations/animator/
// Import them from $utils for convenience

// TODO: File utilities (PNG parser path issues)
// export { extractSequenceFromPNG } from "../../../animator/src/lib/animator/utils/file/png-parser.js";
// export type { PNGParseResult } from "../../../animator/src/lib/animator/utils/file/png-parser.js";

// Canvas utilities
export { CanvasRenderer, SVGGenerator } from "$implementations";

// SVG utilities
export { svgStringToImage } from "../../utils/svgStringToImage.js";

// Components (based on standalone_animator.html reference implementation)
export { default as AnimatorCanvas } from "./AnimatorCanvas.svelte";
export { default as GridManager } from "./GridManager.svelte";
