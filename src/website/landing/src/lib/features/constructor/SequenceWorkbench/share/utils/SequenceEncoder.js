import { logger } from "../../../core/logging/index.js";
import { compressString } from "../../../utils/lzstring.js";

export function encodeSequenceCompact(beats) {
  if (!beats || beats.length === 0) return "";

  try {
    const sequenceData = {
      version: "1.0",
      beats: beats.map((beat) => ({
        id: beat.id,
        letter: beat.letter,
        position: beat.position,
        orientation: beat.orientation,
        timing: beat.timing || 1,
      })),
    };

    const jsonString = JSON.stringify(sequenceData);
    const compressed = compressString(jsonString);

    logger.debug("Encoded sequence:", {
      beats: beats.length,
      compressed: compressed.length,
    });
    return compressed;
  } catch (error) {
    logger.error("Failed to encode sequence:", error);
    return "";
  }
}

/**
 * Extract start position data from a sequence
 * @param {Array} beats - Array of beat data
 * @returns {Object|null} Start position data or null if not found
 */
export function extractStartPositionData(beats) {
  if (!beats || beats.length === 0) return null;

  // Look for the start position (usually the first beat or beat with id 0)
  const startBeat =
    beats.find((beat) => beat.id === 0 || beat.isStartPosition) || beats[0];

  if (!startBeat) return null;

  return {
    position: startBeat.position,
    orientation: startBeat.orientation,
    letter: startBeat.letter || "A",
  };
}

/**
 * Encode start position data
 * @param {Object} startPosition - Start position data
 * @returns {string} Encoded start position
 */
export function encodeStartPosition(startPosition) {
  if (!startPosition) return "";

  try {
    return JSON.stringify({
      position: startPosition.position,
      orientation: startPosition.orientation,
      letter: startPosition.letter || "A",
    });
  } catch (error) {
    logger.error("Failed to encode start position:", error);
    return "";
  }
}

/**
 * Encode orientation data
 * @param {string} orientation - Orientation value
 * @returns {string} Encoded orientation
 */
export function encodeOrientation(orientation) {
  if (!orientation) return "";
  return orientation.toString();
}

/**
 * Encode position data
 * @param {string} position - Position value
 * @returns {string} Encoded position
 */
export function encodePosition(position) {
  if (!position) return "";
  return position.toString();
}

/**
 * Encode motion data
 * @param {Object} motion - Motion data
 * @returns {string} Encoded motion
 */
export function encodeMotion(motion) {
  if (!motion) return "";

  try {
    return JSON.stringify({
      type: motion.type,
      direction: motion.direction,
      timing: motion.timing || 1,
    });
  } catch (error) {
    logger.error("Failed to encode motion:", error);
    return "";
  }
}

// Re-export compressString for convenience
export { compressString } from "../../../utils/lzstring.js";
