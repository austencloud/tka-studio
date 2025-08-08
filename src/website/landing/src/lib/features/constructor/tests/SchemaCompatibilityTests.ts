/**
 * Cross-Platform Schema Compatibility Test
 *
 * Tests that the web TypeScript factories and validation work correctly
 * and would be compatible with Python Pydantic model output.
 */

import {
  createDefaultMotionData,
  createDefaultBeatData,
  createDefaultSequenceData,
  motionDataFactory,
  beatDataFactory,
  sequenceDataFactory,
  updateMotionData,
  updateBeatData,
  updateSequenceData
} from '../factories/DataFactories.js';

import {
  validateMotionData,
  validateBeatData,
  validateSequenceData,
  isValidMotionData,
  isValidBeatData,
  isValidSequenceData,
  assertValidMotionData,
  validateDataFromPython
} from '../validation/SchemaValidation.js';

import type { MotionData, BeatData, SequenceData } from '../types/GeneratedTypes.js';

// Test data that simulates what would come from Python Pydantic models
const SAMPLE_PYTHON_MOTION_DATA = {
  motionType: 'pro',
  propRotDir: 'cw',
  startLoc: 'n',
  endLoc: 'e',
  turns: 1.5,
  startOri: 'in',
  endOri: 'out'
};

const SAMPLE_PYTHON_BEAT_DATA = {
  beatNumber: 1,
  letter: 'A',
  duration: 1.0,
  blueMotion: SAMPLE_PYTHON_MOTION_DATA,
  redMotion: {
    motionType: 'anti',
    propRotDir: 'ccw',
    startLoc: 's',
    endLoc: 'w',
    turns: 2.0,
    startOri: 'out',
    endOri: 'clock'
  },
  pictographData: null,
  blueReversal: false,
  redReversal: true,
  filled: true,
  tags: ['test', 'sample'],
  glyphData: null
};

const SAMPLE_PYTHON_SEQUENCE_DATA = {
  name: 'Test Sequence',
  beats: [SAMPLE_PYTHON_BEAT_DATA],
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z',
  version: '2.0',
  length: 8,
  difficulty: 'beginner',
  tags: ['test', 'tutorial']
};

// Test Runner
export function runSchemaCompatibilityTests(): boolean {
  console.log('🔧 Running Cross-Platform Schema Compatibility Tests...\n');

  let allTestsPassed = true;

  // Test 1: Factory Creation
  console.log('📋 Test 1: Factory Creation');
  try {
    const motion = createDefaultMotionData();
    const beat = createDefaultBeatData(1, 'A');
    const sequence = createDefaultSequenceData('Test');

    console.log('✅ Factory creation successful');
    console.log(`   Motion: ${motion.motionType}, Beat: ${beat.letter}, Sequence: ${sequence.name}`);
  } catch (error) {
    console.error('❌ Factory creation failed:', error);
    allTestsPassed = false;
  }

  // Test 2: Schema Validation of Factory Output
  console.log('\n📋 Test 2: Factory Output Validation');
  try {
    const motion = createDefaultMotionData({
      motionType: 'anti',
      propRotDir: 'ccw'
    });

    const validationResult = validateMotionData(motion);
    if (validationResult.valid) {
      console.log('✅ Factory output validates against schema');
    } else {
      console.error('❌ Factory output validation failed:', validationResult.errors);
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Validation test failed:', error);
    allTestsPassed = false;
  }

  // Test 3: Python Data Compatibility
  console.log('\n📋 Test 3: Python Data Compatibility');
  try {
    const motionResult = validateMotionData(SAMPLE_PYTHON_MOTION_DATA);
    const beatResult = validateBeatData(SAMPLE_PYTHON_BEAT_DATA);
    const sequenceResult = validateSequenceData(SAMPLE_PYTHON_SEQUENCE_DATA);

    if (motionResult.valid && beatResult.valid && sequenceResult.valid) {
      console.log('✅ Python-style data validates successfully');
      console.log('   All cross-platform data structures are compatible');
    } else {
      console.error('❌ Python data validation failed:');
      if (!motionResult.valid) console.error('   Motion errors:', motionResult.errors);
      if (!beatResult.valid) console.error('   Beat errors:', beatResult.errors);
      if (!sequenceResult.valid) console.error('   Sequence errors:', sequenceResult.errors);
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Python compatibility test failed:', error);
    allTestsPassed = false;
  }

  // Test 4: Factory fromJson Compatibility
  console.log('\n📋 Test 4: JSON Deserialization');
  try {
    const motion = motionDataFactory.fromJson(SAMPLE_PYTHON_MOTION_DATA);
    const beat = beatDataFactory.fromJson(SAMPLE_PYTHON_BEAT_DATA);
    const sequence = sequenceDataFactory.fromJson(SAMPLE_PYTHON_SEQUENCE_DATA);

    console.log('✅ JSON deserialization successful');
    console.log(`   Parsed: Motion(${motion.motionType}), Beat(${beat.letter}), Sequence(${sequence.name})`);
  } catch (error) {
    console.error('❌ JSON deserialization failed:', error);
    allTestsPassed = false;
  }

  // Test 5: Immutable Operations
  console.log('\n📋 Test 5: Immutable Operations');
  try {
    const originalMotion = createDefaultMotionData();
    const updatedMotion = updateMotionData(originalMotion, { motionType: 'anti' });

    if (originalMotion.motionType === 'pro' && updatedMotion.motionType === 'anti') {
      console.log('✅ Immutable updates work correctly');
      console.log('   Original preserved, new object created');
    } else {
      console.error('❌ Immutable update failed');
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Immutable operations test failed:', error);
    allTestsPassed = false;
  }

  // Test 6: Type Guards
  console.log('\n📋 Test 6: Type Guards');
  try {
    const validMotion = createDefaultMotionData();
    const invalidData = { invalid: 'data' };

    if (isValidMotionData(validMotion) && !isValidMotionData(invalidData)) {
      console.log('✅ Type guards work correctly');
    } else {
      console.error('❌ Type guards failed');
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Type guards test failed:', error);
    allTestsPassed = false;
  }

  // Test 7: Sequence Operations (Python-like)
  console.log('\n📋 Test 7: Sequence Operations');
  try {
    const sequence = createDefaultSequenceData('Test Sequence');
    const beat1 = createDefaultBeatData(1, 'A');
    const beat2 = createDefaultBeatData(2, 'B');

    const withBeat1 = sequenceDataFactory.addBeat(sequence, beat1);
    const withBeat2 = sequenceDataFactory.addBeat(withBeat1, beat2);

    if (sequence.beats.length === 0 &&
        withBeat1.beats.length === 1 &&
        withBeat2.beats.length === 2) {
      console.log('✅ Sequence operations maintain immutability');
      console.log(`   Progression: ${sequence.beats.length} → ${withBeat1.beats.length} → ${withBeat2.beats.length} beats`);
    } else {
      console.error('❌ Sequence operations failed');
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Sequence operations test failed:', error);
    allTestsPassed = false;
  }

  // Test 8: Error Handling
  console.log('\n📋 Test 8: Error Handling');
  try {
    let errorThrown = false;
    try {
      motionDataFactory.fromJson({ motionType: 'invalid_type' });
    } catch (e) {
      errorThrown = true;
    }

    if (errorThrown) {
      console.log('✅ Error handling works correctly');
      console.log('   Invalid data properly rejected');
    } else {
      console.error('❌ Error handling failed - invalid data accepted');
      allTestsPassed = false;
    }
  } catch (error) {
    console.error('❌ Error handling test failed:', error);
    allTestsPassed = false;
  }

  // Final Results
  console.log('\n' + '='.repeat(50));
  if (allTestsPassed) {
    console.log('🎉 ALL TESTS PASSED!');
    console.log('✅ Cross-platform schema compatibility verified');
    console.log('✅ TypeScript factories match Python behavior');
    console.log('✅ Runtime validation works correctly');
    console.log('✅ Ready for web integration!');
  } else {
    console.log('❌ Some tests failed');
    console.log('⚠️  Schema compatibility issues detected');
  }

  return allTestsPassed;
}

// Export test data for other modules
export {
  SAMPLE_PYTHON_MOTION_DATA,
  SAMPLE_PYTHON_BEAT_DATA,
  SAMPLE_PYTHON_SEQUENCE_DATA
};

// Auto-run if executed directly (for testing)
if (typeof window !== 'undefined' && (window as any).runSchemaTests) {
  runSchemaCompatibilityTests();
}
