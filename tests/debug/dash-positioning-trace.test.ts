/**
 * Comprehensive Dash Arrow Positioning Trace Test
 *
 * Tests the complete arrow positioning pipeline for dash motions with 1 turn
 * to identify where transformations are failing or being bypassed.
 */

import { describe, it, expect, beforeAll } from 'vitest';
import { GridLocation, GridMode, MotionType, type PictographData, type MotionData } from '$shared';
import { DashLocationCalculator } from '$shared/pictograph/arrow/positioning/calculation/services/implementations/DashLocationCalculator';
import { DirectionalTupleCalculator } from '$shared/pictograph/arrow/positioning/calculation/services/implementations/DirectionalTupleProcessor';
import { ArrowQuadrantCalculator } from '$shared/pictograph/arrow/orchestration/services/implementations/ArrowQuadrantCalculator';

// Test data: 4 dash arrows from the sequence Σ-YΣ-YΣ-YΣ-Y
const dashMotions = [
  {
    name: "Beat 1: S→N Dash (CW, 1T)",
    motion: {
      motionType: MotionType.DASH,
      rotationDirection: "cw",
      startLocation: GridLocation.SOUTH,
      endLocation: GridLocation.NORTH,
      turns: 1,
      startOrientation: "in",
      endOrientation: "in",
      color: "blue",
      gridMode: GridMode.DIAMOND,
    } as MotionData,
    letter: "Σ-"
  },
  {
    name: "Beat 3: E→W Dash (CW, 1T)",
    motion: {
      motionType: MotionType.DASH,
      rotationDirection: "cw",
      startLocation: GridLocation.EAST,
      endLocation: GridLocation.WEST,
      turns: 1,
      startOrientation: "out",
      endOrientation: "out",
      color: "blue",
      gridMode: GridMode.DIAMOND,
    } as MotionData,
    letter: "Σ-"
  },
  {
    name: "Beat 5: N→S Dash (CW, 1T)",
    motion: {
      motionType: MotionType.DASH,
      rotationDirection: "cw",
      startLocation: GridLocation.NORTH,
      endLocation: GridLocation.SOUTH,
      turns: 1,
      startOrientation: "in",
      endOrientation: "in",
      color: "blue",
      gridMode: GridMode.DIAMOND,
    } as MotionData,
    letter: "Σ-"
  },
  {
    name: "Beat 7: W→E Dash (CW, 1T)",
    motion: {
      motionType: MotionType.DASH,
      rotationDirection: "cw",
      startLocation: GridLocation.WEST,
      endLocation: GridLocation.EAST,
      turns: 1,
      startOrientation: "out",
      endOrientation: "out",
      color: "blue",
      gridMode: GridMode.DIAMOND,
    } as MotionData,
    letter: "Σ-"
  }
];

interface PositioningTrace {
  motionName: string;
  step1_motionDetection: {
    motionType: string;
    isDash: boolean;
  };
  step2_rotationDetection: {
    rotationDirection: string;
    turns: number;
    isCW: boolean;
    isCCW: boolean;
    isNoRot: boolean;
  };
  step3_gridModeDetection: {
    startLocation: GridLocation;
    endLocation: GridLocation;
    inferredGridMode: GridMode;
  };
  step4_arrowLocationCalculation: {
    calculatedLocation: GridLocation;
  };
  step5_baseAdjustment: {
    x: number;
    y: number;
    source: string;
  };
  step6_directionalTuples: {
    baseX: number;
    baseY: number;
    tuples: Array<{ quadrant: string; x: number; y: number }>;
    allSameAsBase: boolean;
    transformationApplied: boolean;
  };
  step7_quadrantIndex: {
    location: GridLocation;
    gridMode: GridMode;
    quadrantIndex: number;
    quadrantName: string;
  };
  step8_finalAdjustment: {
    selectedTuple: { x: number; y: number };
    finalAdjustment: { x: number; y: number };
    transformationApplied: boolean;
  };
}

describe('Dash Arrow Positioning Pipeline Trace', () => {
  let dashLocationCalculator: DashLocationCalculator;
  let tupleCalculator: DirectionalTupleCalculator;
  let quadrantCalculator: ArrowQuadrantCalculator;

  beforeAll(() => {
    dashLocationCalculator = new DashLocationCalculator();
    tupleCalculator = new DirectionalTupleCalculator();
    quadrantCalculator = new ArrowQuadrantCalculator();
  });

  it('should trace positioning pipeline for all 4 dash motions', () => {
    console.log('\n' + '='.repeat(100));
    console.log('DASH ARROW POSITIONING PIPELINE TRACE');
    console.log('='.repeat(100) + '\n');

    const traces: PositioningTrace[] = [];

    for (const { name, motion, letter } of dashMotions) {
      console.log('\n' + '-'.repeat(100));
      console.log(`Testing: ${name}`);
      console.log('-'.repeat(100));

      const trace = tracePipeline(motion, letter);
      traces.push(trace);

      // Print trace
      printTrace(trace);
    }

    // Analysis
    console.log('\n' + '='.repeat(100));
    console.log('ANALYSIS');
    console.log('='.repeat(100) + '\n');

    analyzeTraces(traces);
  });

  function tracePipeline(motion: MotionData, letter: string): PositioningTrace {
    const trace: PositioningTrace = {
      motionName: `${motion.startLocation}→${motion.endLocation} (${motion.rotationDirection}, ${motion.turns}T)`,
      step1_motionDetection: {
        motionType: motion.motionType as string,
        isDash: motion.motionType === MotionType.DASH || motion.motionType?.toLowerCase() === 'dash'
      },
      step2_rotationDetection: {
        rotationDirection: motion.rotationDirection || 'unknown',
        turns: motion.turns || 0,
        isCW: motion.rotationDirection?.toLowerCase() === 'clockwise' || motion.rotationDirection?.toLowerCase() === 'cw',
        isCCW: motion.rotationDirection?.toLowerCase() === 'counter_clockwise' || motion.rotationDirection?.toLowerCase() === 'ccw',
        isNoRot: motion.rotationDirection?.toLowerCase() === 'norotation' || (motion.turns || 0) === 0
      },
      step3_gridModeDetection: {
        startLocation: motion.startLocation,
        endLocation: motion.endLocation,
        inferredGridMode: inferGridMode(motion)
      },
      step4_arrowLocationCalculation: {
        calculatedLocation: GridLocation.NORTH // Will be calculated
      },
      step5_baseAdjustment: {
        x: 0,
        y: 0,
        source: 'mock'
      },
      step6_directionalTuples: {
        baseX: 0,
        baseY: 0,
        tuples: [],
        allSameAsBase: false,
        transformationApplied: false
      },
      step7_quadrantIndex: {
        location: GridLocation.NORTH,
        gridMode: GridMode.DIAMOND,
        quadrantIndex: 0,
        quadrantName: 'NE'
      },
      step8_finalAdjustment: {
        selectedTuple: { x: 0, y: 0 },
        finalAdjustment: { x: 0, y: 0 },
        transformationApplied: false
      }
    };

    // STEP 4: Calculate arrow location
    try {
      const pictographData: PictographData = {
        letter,
        motions: {
          blue: motion,
          red: motion // Simplified for testing
        }
      };
      trace.step4_arrowLocationCalculation.calculatedLocation =
        dashLocationCalculator.calculateDashLocationFromPictographData(pictographData, true);
    } catch (error) {
      console.error('Error calculating arrow location:', error);
      trace.step4_arrowLocationCalculation.calculatedLocation = motion.startLocation;
    }

    // STEP 5: Mock base adjustment (in real scenario, this comes from JSON)
    // Using typical values for a dash arrow
    const baseX = 10;
    const baseY = 15;
    trace.step5_baseAdjustment = {
      x: baseX,
      y: baseY,
      source: 'mock (10, 15)'
    };

    // STEP 6: Generate directional tuples
    const tuples = tupleCalculator.generateDirectionalTuples(motion, baseX, baseY);
    trace.step6_directionalTuples = {
      baseX,
      baseY,
      tuples: tuples.map((t, i) => ({
        quadrant: ['NE (0)', 'SE (1)', 'SW (2)', 'NW (3)'][i],
        x: t[0],
        y: t[1]
      })),
      allSameAsBase: tuples.every(t => t[0] === baseX && t[1] === baseY),
      transformationApplied: !tuples.every(t => t[0] === baseX && t[1] === baseY)
    };

    // STEP 7: Calculate quadrant index
    const location = trace.step4_arrowLocationCalculation.calculatedLocation;
    const gridMode = trace.step3_gridModeDetection.inferredGridMode;
    const quadrantIndex = quadrantCalculator.calculateQuadrantIndex(motion, location);
    trace.step7_quadrantIndex = {
      location,
      gridMode,
      quadrantIndex,
      quadrantName: ['NE (0)', 'SE (1)', 'SW (2)', 'NW (3)'][quadrantIndex]
    };

    // STEP 8: Select final adjustment
    const selectedTuple = tuples[quadrantIndex] || [0, 0];
    trace.step8_finalAdjustment = {
      selectedTuple: { x: selectedTuple[0], y: selectedTuple[1] },
      finalAdjustment: { x: selectedTuple[0], y: selectedTuple[1] },
      transformationApplied: selectedTuple[0] !== baseX || selectedTuple[1] !== baseY
    };

    return trace;
  }

  function inferGridMode(motion: MotionData): GridMode {
    const cardinalSet = new Set([
      GridLocation.NORTH,
      GridLocation.EAST,
      GridLocation.SOUTH,
      GridLocation.WEST
    ]);
    return (cardinalSet.has(motion.startLocation) || cardinalSet.has(motion.endLocation))
      ? GridMode.DIAMOND
      : GridMode.BOX;
  }

  function printTrace(trace: PositioningTrace): void {
    console.log('\n📋 STEP 1: Motion Type Detection');
    console.log(`   Motion type: ${trace.step1_motionDetection.motionType}`);
    console.log(`   Is Dash: ${trace.step1_motionDetection.isDash ? '✅ YES' : '❌ NO'}`);

    console.log('\n🔄 STEP 2: Rotation Direction Detection');
    console.log(`   Rotation: ${trace.step2_rotationDetection.rotationDirection}`);
    console.log(`   Turns: ${trace.step2_rotationDetection.turns}`);
    console.log(`   Is CW: ${trace.step2_rotationDetection.isCW ? '✅ YES' : '❌ NO'}`);
    console.log(`   Is CCW: ${trace.step2_rotationDetection.isCCW ? '✅ YES' : '❌ NO'}`);
    console.log(`   Is NoRot: ${trace.step2_rotationDetection.isNoRot ? '✅ YES' : '❌ NO'}`);

    console.log('\n📐 STEP 3: Grid Mode Detection');
    console.log(`   Start: ${trace.step3_gridModeDetection.startLocation}`);
    console.log(`   End: ${trace.step3_gridModeDetection.endLocation}`);
    console.log(`   Inferred Grid Mode: ${trace.step3_gridModeDetection.inferredGridMode}`);

    console.log('\n📍 STEP 4: Arrow Location Calculation');
    console.log(`   Calculated Location: ${trace.step4_arrowLocationCalculation.calculatedLocation}`);

    console.log('\n📦 STEP 5: Base Adjustment');
    console.log(`   Base: (${trace.step5_baseAdjustment.x}, ${trace.step5_baseAdjustment.y})`);
    console.log(`   Source: ${trace.step5_baseAdjustment.source}`);

    console.log('\n🔢 STEP 6: Directional Tuple Generation');
    console.log(`   Base values: (${trace.step6_directionalTuples.baseX}, ${trace.step6_directionalTuples.baseY})`);
    console.log('   Generated tuples:');
    trace.step6_directionalTuples.tuples.forEach(t => {
      console.log(`      ${t.quadrant}: (${t.x}, ${t.y})`);
    });
    if (trace.step6_directionalTuples.allSameAsBase) {
      console.log('   ⚠️ WARNING: All tuples are identical to base - NO TRANSFORMATION!');
    } else {
      console.log('   ✅ Transformation applied');
    }

    console.log('\n🎯 STEP 7: Quadrant Index Calculation');
    console.log(`   Location: ${trace.step7_quadrantIndex.location}`);
    console.log(`   Grid Mode: ${trace.step7_quadrantIndex.gridMode}`);
    console.log(`   Quadrant Index: ${trace.step7_quadrantIndex.quadrantIndex}`);
    console.log(`   Quadrant Name: ${trace.step7_quadrantIndex.quadrantName}`);

    console.log('\n✨ STEP 8: Final Adjustment');
    console.log(`   Selected Tuple: (${trace.step8_finalAdjustment.selectedTuple.x}, ${trace.step8_finalAdjustment.selectedTuple.y})`);
    console.log(`   Final Adjustment: (${trace.step8_finalAdjustment.finalAdjustment.x}, ${trace.step8_finalAdjustment.finalAdjustment.y})`);
    if (!trace.step8_finalAdjustment.transformationApplied) {
      console.log('   ⚠️ WARNING: Final equals base - NO TRANSFORMATION!');
    } else {
      console.log('   ✅ Transformation applied');
    }
  }

  function analyzeTraces(traces: PositioningTrace[]): void {
    console.log('🔍 Checking for consistency issues:\n');

    // Check if all are detected as dash
    const allDash = traces.every(t => t.step1_motionDetection.isDash);
    console.log(`1. Motion Type Detection: ${allDash ? '✅ All detected as DASH' : '❌ Some NOT detected as DASH'}`);

    // Check if all are detected as CW
    const allCW = traces.every(t => t.step2_rotationDetection.isCW);
    console.log(`2. Rotation Detection: ${allCW ? '✅ All detected as CW' : '❌ Some NOT detected as CW'}`);

    // Check if all use Diamond mode
    const allDiamond = traces.every(t => t.step3_gridModeDetection.inferredGridMode === GridMode.DIAMOND);
    console.log(`3. Grid Mode Detection: ${allDiamond ? '✅ All using DIAMOND mode' : '❌ Mixed grid modes'}`);

    // Check arrow locations
    console.log('\n4. Arrow Location Calculation:');
    traces.forEach(t => {
      console.log(`   ${t.motionName} → Arrow at: ${t.step4_arrowLocationCalculation.calculatedLocation}`);
    });

    // Check if transformations were applied
    const allTransformed = traces.every(t => t.step6_directionalTuples.transformationApplied);
    console.log(`\n5. Tuple Transformation: ${allTransformed ? '✅ All tuples transformed' : '❌ Some tuples NOT transformed'}`);

    // Check if final adjustments differ
    const allFinalTransformed = traces.every(t => t.step8_finalAdjustment.transformationApplied);
    console.log(`6. Final Adjustment: ${allFinalTransformed ? '✅ All finals transformed' : '❌ Some finals NOT transformed'}`);

    // Check for inconsistencies
    console.log('\n7. Inconsistency Check:');
    const uniqueFinalAdjustments = new Set(
      traces.map(t => `(${t.step8_finalAdjustment.finalAdjustment.x}, ${t.step8_finalAdjustment.finalAdjustment.y})`)
    );
    if (uniqueFinalAdjustments.size === 1) {
      console.log('   ⚠️ WARNING: All dash arrows have IDENTICAL final adjustments!');
      console.log('   This suggests the quadrant-specific transformation is NOT working.');
    } else {
      console.log(`   ✅ Found ${uniqueFinalAdjustments.size} different final adjustments (expected: 4)`);
    }

    // Print all unique adjustments
    console.log('\n   Final adjustments by motion:');
    traces.forEach(t => {
      const final = t.step8_finalAdjustment.finalAdjustment;
      console.log(`      ${t.motionName}: (${final.x}, ${final.y})`);
    });
  }
});
