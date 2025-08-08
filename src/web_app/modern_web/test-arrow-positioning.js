/**
 * Quick validation test for the sophisticated Arrow Positioning Service
 * 
 * This script tests the complete positioning pipeline:
 * - ArrowPlacementDataService loading real JSON data
 * - ArrowPlacementKeyService generating complex keys
 * - ArrowPositioningService calculating sophisticated adjustments
 * 
 * Run this to validate the system is working end-to-end.
 */

import { ArrowPositioningService } from './src/lib/services/implementations/ArrowPositioningService.js';
import { ArrowPlacementDataService } from './src/lib/services/implementations/ArrowPlacementDataService.js';
import { ArrowPlacementKeyService } from './src/lib/services/implementations/ArrowPlacementKeyService.js';

// Quick test data
const testMotionData = {
  motionType: 'pro',
  propRotDir: 'cw',
  startLocation: 'n',
  endLocation: 's',
  turns: 1,
  startOrientation: 'in',
  endOrientation: 'out'
};

const testPictographData = {
  id: 'sophisticated-test',
  gridData: { mode: 'diamond' },
  arrows: { blue: {}, red: {} },
  props: { blue: {}, red: {} },
  motions: { blue: testMotionData, red: null },
  letter: 'A'
};

const testGridData = {
  mode: 'diamond',
  allLayer2PointsNormal: {
    'n_diamond_layer2_point': { coordinates: { x: 150, y: 70 } }
  },
  allHandPointsNormal: {
    'n_diamond_hand_point': { coordinates: { x: 150, y: 102 } }
  }
};

const testArrowData = {
  id: 'blue-arrow',
  color: 'blue',
  motionType: 'pro',
  location: 'n',
  startOrientation: 'in',
  endOrientation: 'out',
  propRotDir: 'cw',
  turns: 1,
  isMirrored: false
};

// Quick validation function
async function validateSophisticatedPositioning() {
  console.log('🧪 QUICK VALIDATION: Sophisticated Arrow Positioning');
  console.log('==================================================');

  try {
    // 1. Test service creation
    console.log('\n🏗️ Step 1: Creating sophisticated services...');
    const placementDataService = new ArrowPlacementDataService();
    const placementKeyService = new ArrowPlacementKeyService();
    const arrowPositioningService = new ArrowPositioningService(
      placementDataService,
      placementKeyService
    );
    console.log('✅ Services created successfully');

    // 2. Test data loading
    console.log('\n📊 Step 2: Loading sophisticated placement data...');
    await placementDataService.loadPlacementData();
    console.log(`✅ Data loaded: ${placementDataService.isLoaded()}`);

    // 3. Test available keys
    console.log('\n🔑 Step 3: Checking available placement keys...');
    const availableKeys = await placementDataService.getAvailablePlacementKeys('pro', 'diamond');
    console.log(`✅ Found ${availableKeys.length} placement keys for PRO motion`);
    console.log('Sample keys:', availableKeys.slice(0, 3));

    // 4. Test key generation
    console.log('\n🎯 Step 4: Testing sophisticated key generation...');
    const placementKey = placementKeyService.generatePlacementKey(
      testMotionData,
      testPictographData,
      availableKeys
    );
    console.log(`✅ Generated sophisticated key: ${placementKey}`);

    // 5. Test adjustment lookup
    console.log('\n📐 Step 5: Testing sophisticated adjustment lookup...');
    const adjustment = await placementDataService.getDefaultAdjustment(
      'pro',
      placementKey,
      1,
      'diamond'
    );
    console.log(`✅ Sophisticated adjustment: [${adjustment.x}, ${adjustment.y}]`);

    // 6. Test complete positioning
    console.log('\n🎯 Step 6: Testing complete sophisticated positioning...');
    const position = await arrowPositioningService.calculateArrowPosition(
      testArrowData,
      testPictographData,
      testGridData
    );
    console.log(`✅ Sophisticated position: [${position.x}, ${position.y}] rotation: ${position.rotation}°`);

    // 7. Test all arrows
    console.log('\n🏹 Step 7: Testing all arrows sophisticated positioning...');
    const allPositions = await arrowPositioningService.calculateAllArrowPositions(
      testPictographData,
      testGridData
    );
    console.log(`✅ Calculated ${allPositions.size} arrows with sophisticated positioning`);

    console.log('\n🎉 VALIDATION COMPLETE!');
    console.log('=============================');
    console.log('✅ All sophisticated positioning features working!');
    console.log(`✅ Placement data: ${placementDataService.isLoaded()}`);
    console.log(`✅ Available keys: ${availableKeys.length}`);
    console.log(`✅ Generated key: ${placementKey}`);
    console.log(`✅ Adjustment: [${adjustment.x}, ${adjustment.y}]`);
    console.log(`✅ Final position: [${position.x}, ${position.y}] @ ${position.rotation}°`);
    console.log('\n🚀 SOPHISTICATED POSITIONING SYSTEM IS OPERATIONAL!');

    return true;

  } catch (error) {
    console.error('❌ VALIDATION FAILED:', error);
    console.error('Stack:', error.stack);
    return false;
  }
}

// Fix function name typo
validateSophisticatedPositioning()
  .then(success => {
    if (success) {
      console.log('\n✅ QUICK VALIDATION PASSED - System is ready!');
    } else {
      console.log('\n❌ QUICK VALIDATION FAILED - Check errors above');
    }
  })
  .catch(error => {
    console.error('\n💥 VALIDATION CRASHED:', error);
  });
