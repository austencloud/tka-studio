/**
 * Sequence Preview Rendering Performance Test
 *
 * This test measures rendering performance for the share panel preview
 * and identifies optimization opportunities for phone screens.
 *
 * Test goals:
 * 1. Measure baseline rendering time with current settings
 * 2. Test various optimization strategies
 * 3. Identify bottlenecks in the rendering pipeline
 * 4. Compare pre-rendering vs on-demand rendering
 */

import { describe, it, expect, beforeAll } from "vitest";
import { container } from "$shared/inversify/container";
import { TYPES } from "$shared/inversify/types";
import type { ISequenceRenderService } from "$render";
import type { SequenceData } from "$shared";

// Test sequence data (16-beat circular sequence)
const TEST_SEQUENCE: SequenceData = {
  id: "fd609c39-163f-49ec-b504-7cd42103e399",
  name: "Circular XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  word: "XΔX-ΔXΔX-ΔXΔX-ΔXΔX-Δ",
  beats: [
    {
      id: "e7bf366d-ba05-46f2-abf1-c71546f90ed2",
      letter: "X",
      startPosition: "gamma11",
      endPosition: "alpha3",
      motions: {
        blue: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "w",
          turns: 0,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "e",
          turns: 1,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 1,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "0ced6c2e-6eda-4fca-9ecc-50b0f2ec880b",
      letter: "Δ",
      startPosition: "alpha3",
      endPosition: "gamma13",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "noRotation",
          startLocation: "w",
          endLocation: "w",
          turns: 0,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "s",
          turns: 0,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 2,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "8328b537-34b3-4f40-98c9-94bb32d16a3d",
      letter: "X-",
      startPosition: "gamma13",
      endPosition: "alpha7",
      motions: {
        blue: {
          motionType: "dash",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "e",
          turns: 1,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "w",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 3,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "e424386c-ee91-4004-b041-0c4919fe6bb6",
      letter: "Δ",
      startPosition: "alpha7",
      endPosition: "gamma9",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "e",
          turns: 1,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "n",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 4,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-5",
      letter: "X",
      startPosition: "gamma9",
      endPosition: "alpha1",
      motions: {
        blue: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "s",
          turns: 0,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "n",
          turns: 1,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 5,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-6",
      letter: "Δ",
      startPosition: "alpha1",
      endPosition: "gamma11",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "noRotation",
          startLocation: "s",
          endLocation: "s",
          turns: 0,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "e",
          turns: 0,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 6,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-7",
      letter: "X-",
      startPosition: "gamma11",
      endPosition: "alpha5",
      motions: {
        blue: {
          motionType: "dash",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "n",
          turns: 1,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "s",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 7,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-8",
      letter: "Δ",
      startPosition: "alpha5",
      endPosition: "gamma15",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "n",
          turns: 1,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "w",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 8,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-9",
      letter: "X",
      startPosition: "gamma15",
      endPosition: "alpha7",
      motions: {
        blue: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "e",
          turns: 0,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "w",
          turns: 1,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 9,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-10",
      letter: "Δ",
      startPosition: "alpha7",
      endPosition: "gamma9",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "noRotation",
          startLocation: "e",
          endLocation: "e",
          turns: 0,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "n",
          turns: 0,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 10,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-11",
      letter: "X-",
      startPosition: "gamma9",
      endPosition: "alpha3",
      motions: {
        blue: {
          motionType: "dash",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "w",
          turns: 1,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "e",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 11,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-12",
      letter: "Δ",
      startPosition: "alpha3",
      endPosition: "gamma13",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "w",
          turns: 1,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "e",
          endLocation: "s",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 12,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-13",
      letter: "X",
      startPosition: "gamma13",
      endPosition: "alpha5",
      motions: {
        blue: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "n",
          turns: 0,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "s",
          turns: 1,
          startOrientation: "in",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 13,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-14",
      letter: "Δ",
      startPosition: "alpha5",
      endPosition: "gamma15",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "noRotation",
          startLocation: "n",
          endLocation: "n",
          turns: 0,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "w",
          turns: 0,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 14,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-15",
      letter: "X-",
      startPosition: "gamma15",
      endPosition: "alpha1",
      motions: {
        blue: {
          motionType: "dash",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "s",
          turns: 1,
          startOrientation: "out",
          endOrientation: "out",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "w",
          endLocation: "n",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 15,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
    {
      id: "beat-16",
      letter: "Δ",
      startPosition: "alpha1",
      endPosition: "gamma11",
      motions: {
        blue: {
          motionType: "static",
          rotationDirection: "ccw",
          startLocation: "s",
          endLocation: "s",
          turns: 1,
          startOrientation: "out",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "blue",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
        red: {
          motionType: "anti",
          rotationDirection: "ccw",
          startLocation: "n",
          endLocation: "e",
          turns: 1,
          startOrientation: "in",
          endOrientation: "in",
          isVisible: true,
          propType: "staff",
          arrowLocation: "n",
          color: "red",
          gridMode: "diamond",
          arrowPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
            svgMirrored: false,
          },
          propPlacementData: {
            positionX: 0,
            positionY: 0,
            rotationAngle: 0,
            coordinates: null,
            svgCenter: null,
          },
          prefloatMotionType: null,
          prefloatRotationDirection: null,
        },
      },
      beatNumber: 16,
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    },
  ],
  thumbnails: [],
  isFavorite: false,
  isCircular: true,
  tags: ["circular", "cap", "strict-rotated"],
  metadata: {
    generated: true,
    generatedAt: "2025-10-29T23:11:43.464Z",
    algorithm: "freeform",
    beatsGenerated: 16,
    propContinuity: "continuous",
    blueRotationDirection: "",
    redRotationDirection: "",
    turnIntensity: 1,
    level: 2,
  },
  gridMode: "diamond",
  propType: "fan",
  startingPositionBeat: {
    id: "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    motions: {
      blue: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "s",
        endLocation: "s",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "s",
        color: "blue",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
      red: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "e",
        endLocation: "e",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "e",
        color: "red",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
    },
    letter: "Γ",
    startPosition: "gamma11",
    endPosition: "gamma11",
    beatNumber: 0,
    duration: 1,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
  },
  startPosition: {
    id: "4146b97b-0849-46fd-a971-2c73e0a7a4e6",
    motions: {
      blue: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "s",
        endLocation: "s",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "s",
        color: "blue",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
      red: {
        motionType: "static",
        rotationDirection: "noRotation",
        startLocation: "e",
        endLocation: "e",
        turns: 0,
        startOrientation: "in",
        endOrientation: "in",
        isVisible: true,
        propType: "staff",
        arrowLocation: "e",
        color: "red",
        gridMode: "diamond",
        arrowPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
          svgMirrored: false,
        },
        propPlacementData: {
          positionX: 0,
          positionY: 0,
          rotationAngle: 0,
          coordinates: null,
          svgCenter: null,
        },
        prefloatMotionType: null,
        prefloatRotationDirection: null,
      },
    },
    letter: "Γ",
    startPosition: "gamma11",
    endPosition: "gamma11",
    beatNumber: 0,
    duration: 1,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
  },
  difficultyLevel: "intermediate",
} as SequenceData;

// Phone screen sizes to test against
const PHONE_SCREENS = {
  iPhoneSE: { width: 375, height: 667, name: "iPhone SE" },
  iPhone14: { width: 390, height: 844, name: "iPhone 14" },
  iPhone14Pro: { width: 393, height: 852, name: "iPhone 14 Pro" },
  Pixel7: { width: 412, height: 915, name: "Pixel 7" },
  GalaxyS23: { width: 360, height: 780, name: "Galaxy S23" },
};

describe("Sequence Preview Rendering Performance", () => {
  let renderService: ISequenceRenderService;

  beforeAll(() => {
    renderService = container.get<ISequenceRenderService>(
      TYPES.ISequenceRenderService
    );
  });

  describe("Baseline Performance Tests", () => {
    it("should measure current preview generation time (beatScale: 0.15, quality: 0.4, JPEG)", async () => {
      const runs = 5;
      const times: number[] = [];

      for (let i = 0; i < runs; i++) {
        const start = performance.now();

        await renderService.generatePreview(TEST_SEQUENCE, {
          beatScale: 0.15,
          quality: 0.4,
          format: "JPEG",
          includeStartPosition: true,
          addBeatNumbers: true,
          addWord: true,
          addDifficultyLevel: true,
        });

        const end = performance.now();
        times.push(end - start);
      }

      const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
      const minTime = Math.min(...times);
      const maxTime = Math.max(...times);

      console.log("\n📊 BASELINE PERFORMANCE (Current Settings):");
      console.log(`   Average: ${avgTime.toFixed(2)}ms`);
      console.log(`   Min: ${minTime.toFixed(2)}ms`);
      console.log(`   Max: ${maxTime.toFixed(2)}ms`);
      console.log(`   Settings: beatScale=0.15, quality=0.4, format=JPEG`);

      expect(avgTime).toBeLessThan(5000); // Should complete in under 5 seconds
    }, 30000);

    it("should measure full-quality preview generation time (beatScale: 0.5, quality: 0.8)", async () => {
      const runs = 3;
      const times: number[] = [];

      for (let i = 0; i < runs; i++) {
        const start = performance.now();

        await renderService.generatePreview(TEST_SEQUENCE, {
          beatScale: 0.5,
          quality: 0.8,
          format: "PNG",
          includeStartPosition: true,
          addBeatNumbers: true,
          addWord: true,
          addDifficultyLevel: true,
        });

        const end = performance.now();
        times.push(end - start);
      }

      const avgTime = times.reduce((a, b) => a + b, 0) / times.length;

      console.log("\n📊 FULL QUALITY PREVIEW:");
      console.log(`   Average: ${avgTime.toFixed(2)}ms`);
      console.log(`   Settings: beatScale=0.5, quality=0.8, format=PNG`);
    }, 30000);
  });

  describe("Scale Optimization Tests", () => {
    const scales = [0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3];

    scales.forEach((scale) => {
      it(`should measure performance at beatScale: ${scale}`, async () => {
        const runs = 3;
        const times: number[] = [];

        for (let i = 0; i < runs; i++) {
          const start = performance.now();

          const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
            beatScale: scale,
            quality: 0.4,
            format: "JPEG",
            includeStartPosition: true,
            addBeatNumbers: true,
            addWord: true,
            addDifficultyLevel: true,
          });

          const end = performance.now();
          times.push(end - start);

          // Measure data URL size
          if (i === 0) {
            const sizeKB = (dataUrl.length * 0.75) / 1024; // Base64 to bytes
            console.log(
              `   beatScale=${scale}: ${times[0]!.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
            );
          }
        }

        const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
        expect(avgTime).toBeLessThan(10000);
      }, 30000);
    });
  });

  describe("Quality Optimization Tests", () => {
    const qualities = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8];

    qualities.forEach((quality) => {
      it(`should measure performance at quality: ${quality}`, async () => {
        const start = performance.now();

        const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
          beatScale: 0.15,
          quality,
          format: "JPEG",
          includeStartPosition: true,
          addBeatNumbers: true,
          addWord: true,
          addDifficultyLevel: true,
        });

        const end = performance.now();
        const time = end - start;
        const sizeKB = (dataUrl.length * 0.75) / 1024;

        console.log(
          `   quality=${quality}: ${time.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
        );
        expect(time).toBeLessThan(10000);
      }, 15000);
    });
  });

  describe("Format Comparison Tests", () => {
    const formats: Array<"PNG" | "JPEG" | "WebP"> = ["JPEG", "PNG", "WebP"];

    formats.forEach((format) => {
      it(`should measure performance with format: ${format}`, async () => {
        const runs = 3;
        const times: number[] = [];

        for (let i = 0; i < runs; i++) {
          const start = performance.now();

          const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
            beatScale: 0.15,
            quality: 0.4,
            format,
            includeStartPosition: true,
            addBeatNumbers: true,
            addWord: true,
            addDifficultyLevel: true,
          });

          const end = performance.now();
          times.push(end - start);

          if (i === 0) {
            const sizeKB = (dataUrl.length * 0.75) / 1024;
            console.log(
              `   ${format}: ${times[0]!.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
            );
          }
        }

        const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
        expect(avgTime).toBeLessThan(10000);
      }, 30000);
    });
  });

  describe("Content Optimization Tests", () => {
    it("should measure performance with minimal content (no extras)", async () => {
      const start = performance.now();

      await renderService.generatePreview(TEST_SEQUENCE, {
        beatScale: 0.15,
        quality: 0.4,
        format: "JPEG",
        includeStartPosition: false,
        addBeatNumbers: false,
        addWord: false,
        addDifficultyLevel: false,
      });

      const end = performance.now();
      console.log(`\n   Minimal content: ${(end - start).toFixed(2)}ms`);
    }, 15000);

    it("should measure performance with full content (all extras)", async () => {
      const start = performance.now();

      await renderService.generatePreview(TEST_SEQUENCE, {
        beatScale: 0.15,
        quality: 0.4,
        format: "JPEG",
        includeStartPosition: true,
        addBeatNumbers: true,
        addWord: true,
        addDifficultyLevel: true,
      });

      const end = performance.now();
      console.log(`   Full content: ${(end - start).toFixed(2)}ms`);
    }, 15000);
  });

  describe("Phone Screen Suitability Tests", () => {
    Object.entries(PHONE_SCREENS).forEach(([key, screen]) => {
      it(`should generate preview suitable for ${screen.name} (${screen.width}x${screen.height})`, async () => {
        const start = performance.now();

        const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
          beatScale: 0.15,
          quality: 0.4,
          format: "JPEG",
          includeStartPosition: true,
          addBeatNumbers: true,
          addWord: true,
          addDifficultyLevel: true,
        });

        const end = performance.now();
        const time = end - start;
        const sizeKB = (dataUrl.length * 0.75) / 1024;

        console.log(
          `\n   ${screen.name}: ${time.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
        );
        console.log(`   Target viewport: ${screen.width}x${screen.height}px`);

        // Should be fast enough for good UX
        expect(time).toBeLessThan(3000);
        // Should be small enough for quick transfer
        expect(sizeKB).toBeLessThan(500);
      }, 15000);
    });
  });

  describe("Extreme Optimization Tests", () => {
    it("should test ultra-low quality (quality: 0.1, beatScale: 0.08)", async () => {
      const start = performance.now();

      const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
        beatScale: 0.08,
        quality: 0.1,
        format: "JPEG",
        includeStartPosition: true,
        addBeatNumbers: false,
        addWord: false,
        addDifficultyLevel: false,
      });

      const end = performance.now();
      const time = end - start;
      const sizeKB = (dataUrl.length * 0.75) / 1024;

      console.log(
        `\n   Ultra-low quality: ${time.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
      );
      expect(time).toBeLessThan(5000);
    }, 15000);

    it("should test aggressive optimization (quality: 0.2, beatScale: 0.10)", async () => {
      const start = performance.now();

      const dataUrl = await renderService.generatePreview(TEST_SEQUENCE, {
        beatScale: 0.1,
        quality: 0.2,
        format: "JPEG",
        includeStartPosition: true,
        addBeatNumbers: true,
        addWord: true,
        addDifficultyLevel: false,
      });

      const end = performance.now();
      const time = end - start;
      const sizeKB = (dataUrl.length * 0.75) / 1024;

      console.log(
        `   Aggressive optimization: ${time.toFixed(2)}ms, Size: ${sizeKB.toFixed(2)}KB`
      );
      expect(time).toBeLessThan(5000);
    }, 15000);
  });

  describe("Batch Rendering Tests (Pre-generation Simulation)", () => {
    it("should measure time to pre-generate 10 sequences", async () => {
      const start = performance.now();

      const promises = Array(10)
        .fill(null)
        .map(() =>
          renderService.generatePreview(TEST_SEQUENCE, {
            beatScale: 0.15,
            quality: 0.4,
            format: "JPEG",
            includeStartPosition: true,
            addBeatNumbers: true,
            addWord: true,
            addDifficultyLevel: true,
          })
        );

      await Promise.all(promises);

      const end = performance.now();
      const totalTime = end - start;
      const avgTime = totalTime / 10;

      console.log(
        `\n   Batch of 10 sequences: ${totalTime.toFixed(2)}ms total`
      );
      console.log(`   Average per sequence: ${avgTime.toFixed(2)}ms`);
      console.log(
        `   Parallelization benefit: ${avgTime < totalTime / 10 ? "Yes" : "No"}`
      );
    }, 60000);
  });
});
