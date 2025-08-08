/**
 * Comparative Start Position Picker Test
 *
 * This test validates the start position picker functionality between the legacy
 * and modern web applications by comparing 3-star position pictographs for:
 * - Individual prop positioning coordinates (x, y positions)
 * - Rotation values applied to each prop
 * - Transformation matrices or CSS transforms
 *
 * Uses legacy as reference baseline for pixel-perfect positioning and rotation consistency.
 */

import { test, expect } from '@playwright/test';
import {
  LegacyStartPositionExtractor,
  ModernStartPositionExtractor,
  CoordinateComparator,
  RotationComparator,
  DiscrepancyReporter,
  TestDataGenerator,
  TransformationAnalyzer
} from './utils/comparison-utilities';
import { ComparativeTestRunner } from './utils/test-runner';
import { DEFAULT_TEST_CONFIG, getConfigForEnvironment } from './config/test-config';

// Test configuration is now handled by the config system

// Interfaces are now imported from utilities

test.describe('Start Position Picker Comparative Analysis', () => {
  let testRunner: ComparativeTestRunner;
  const config = getConfigForEnvironment('development');

  test.beforeAll(async () => {
    // Initialize test runner with development environment
    testRunner = new ComparativeTestRunner('development');
  });

  test.describe('3-Star Position Pictograph Comparison', () => {
    for (const gridMode of config.gridModes) {
      test.describe(`${gridMode.toUpperCase()} Grid Mode`, () => {
        for (const positionKey of config.startPositions[gridMode]) {
          test(`should have pixel-perfect parity for ${positionKey}`, async ({ context }) => {
            // Create separate browser contexts for legacy and modern apps
            const legacyContext = await context.browser()?.newContext();
            const modernContext = await context.browser()?.newContext();

            if (!legacyContext || !modernContext) {
              throw new Error('Failed to create browser contexts');
            }

            try {
              // Execute test using test runner
              const result = await testRunner.executePositionTest(
                legacyContext,
                modernContext,
                positionKey,
                gridMode
              );

              // Log detailed findings
              console.log(`\n=== COMPARISON REPORT: ${positionKey} (${gridMode}) ===`);
              console.log(`Success: ${result.success}`);
              console.log(`Execution Time: ${result.executionTime}ms`);

              if (result.comparisonResult.coordinateDiscrepancies?.length > 0) {
                console.log(`Coordinate Issues: ${result.comparisonResult.coordinateDiscrepancies.length}`);
              }

              if (result.comparisonResult.rotationDiscrepancies?.length > 0) {
                console.log(`Rotation Issues: ${result.comparisonResult.rotationDiscrepancies.length}`);
              }

              // Assert overall match
              expect(result.success).toBe(true);

              // If there are discrepancies, fail with detailed information
              if (!result.success) {
                const errorMessage = [
                  `Position ${positionKey} in ${gridMode} mode has discrepancies:`,
                  `Coordinate issues: ${result.comparisonResult.coordinateDiscrepancies?.length || 0}`,
                  `Rotation issues: ${result.comparisonResult.rotationDiscrepancies?.length || 0}`,
                  `Transform issues: ${result.comparisonResult.transformDiscrepancies?.length || 0}`,
                  '',
                  'Recommendations:',
                  ...(result.comparisonResult.recommendations || []).map(r => `- ${r}`)
                ].join('\n');

                throw new Error(errorMessage);
              }

            } finally {
              await legacyContext.close();
              await modernContext.close();
            }
          });
        }
      });
    }
  });

  test.describe('Cross-Grid Mode Consistency', () => {
    test('should maintain consistent relative positioning between grid modes', async ({ context }) => {
      // Create separate browser contexts for legacy and modern apps
      const legacyContext = await context.browser()?.newContext();
      const modernContext = await context.browser()?.newContext();

      if (!legacyContext || !modernContext) {
        throw new Error('Failed to create browser contexts');
      }

      try {
        // Execute full test suite to get comprehensive results
        const suiteResult = await testRunner.executeFullTestSuite(
          legacyContext,
          modernContext
        );

        // Log comprehensive report
        console.log('\n=== FULL TEST SUITE RESULTS ===');
        console.log(`Total Tests: ${suiteResult.totalTests}`);
        console.log(`Passed: ${suiteResult.passedTests}`);
        console.log(`Failed: ${suiteResult.failedTests}`);
        console.log(`Success Rate: ${((suiteResult.passedTests / suiteResult.totalTests) * 100).toFixed(1)}%`);
        console.log(`Execution Time: ${suiteResult.executionTime}ms`);

        // Analyze cross-grid consistency
        const diamondResults = suiteResult.results.filter(r => r.gridMode === 'diamond');
        const boxResults = suiteResult.results.filter(r => r.gridMode === 'box');

        const diamondSuccessRate = diamondResults.filter(r => r.success).length / diamondResults.length;
        const boxSuccessRate = boxResults.filter(r => r.success).length / boxResults.length;

        console.log(`Diamond Grid Success Rate: ${(diamondSuccessRate * 100).toFixed(1)}%`);
        console.log(`Box Grid Success Rate: ${(boxSuccessRate * 100).toFixed(1)}%`);

        // All tests should pass for consistency
        expect(suiteResult.failedTests).toBe(0);

        // Both grid modes should have similar success rates
        const successRateDifference = Math.abs(diamondSuccessRate - boxSuccessRate);
        expect(successRateDifference).toBeLessThan(0.1); // Less than 10% difference

      } finally {
        await legacyContext.close();
        await modernContext.close();
      }
    });
  });

});
