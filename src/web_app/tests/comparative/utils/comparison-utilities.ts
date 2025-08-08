/**
 * Comparison Utilities for Start Position Picker Testing
 *
 * This module provides utilities for extracting, comparing, and analyzing
 * positioning data between legacy and modern start position picker implementations.
 */

import type { Page } from '@playwright/test';

export interface PropPositionData {
  x: number;
  y: number;
  rotation: number;
  color: 'blue' | 'red';
  location: string;
  transformMatrix?: string;
  cssTransform?: string;
}

export interface StartPositionData {
  positionKey: string;
  gridMode: 'diamond' | 'box';
  props: PropPositionData[];
  letter: string;
  metadata: {
    timestamp: number;
    source: 'legacy' | 'modern';
    componentVersion?: string;
  };
}

/**
 * Extracts positioning data from legacy start position picker components
 */
export class LegacyStartPositionExtractor {
  async extractPositionData(
    page: Page,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<StartPositionData> {
    // Wait for the specific start position to be visible
    const positionSelector = `[data-position-key="${positionKey}"]`;
    await page.waitForSelector(positionSelector, { state: 'visible', timeout: 10000 });

    // Extract prop data from the pictograph
    const props = await page.evaluate((selector) => {
      const positionElement = document.querySelector(selector);
      if (!positionElement) return [];

      const propElements = positionElement.querySelectorAll('.prop-element, [data-prop-color]');
      const extractedProps: PropPositionData[] = [];

      propElements.forEach((propEl) => {
        const element = propEl as HTMLElement;
        const color = element.getAttribute('data-prop-color') as 'blue' | 'red';
        const location = element.getAttribute('data-location') || '';

        // Extract coordinates from transform or direct positioning
        const transform = element.style.transform || element.getAttribute('transform');
        const computedStyle = window.getComputedStyle(element);

        let x = 0, y = 0, rotation = 0;

        // Parse transform matrix or translate values
        if (transform) {
          const matrixMatch = transform.match(/matrix\(([^)]+)\)/);
          const translateMatch = transform.match(/translate\(([^)]+)\)/);
          const rotateMatch = transform.match(/rotate\(([^)]+)\)/);

          if (matrixMatch) {
            const values = matrixMatch[1].split(',').map(v => parseFloat(v.trim()));
            x = values[4] || 0;
            y = values[5] || 0;
            // Extract rotation from matrix if needed
          } else if (translateMatch) {
            const values = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
            x = values[0] || 0;
            y = values[1] || 0;
          }

          if (rotateMatch) {
            rotation = parseFloat(rotateMatch[1]) || 0;
          }
        }

        // Fallback to direct positioning
        if (x === 0 && y === 0) {
          x = parseFloat(element.getAttribute('x') || '0');
          y = parseFloat(element.getAttribute('y') || '0');
        }

        extractedProps.push({
          x,
          y,
          rotation,
          color,
          location,
          transformMatrix: transform,
          cssTransform: computedStyle.transform
        });
      });

      return extractedProps;
    }, positionSelector);

    // Extract letter information
    const letter = await page.evaluate((selector) => {
      const positionElement = document.querySelector(selector);
      const letterElement = positionElement?.querySelector('.tka-letter, [data-letter]');
      return letterElement?.textContent || letterElement?.getAttribute('data-letter') || '';
    }, positionSelector);

    return {
      positionKey,
      gridMode,
      props,
      letter,
      metadata: {
        timestamp: Date.now(),
        source: 'legacy',
        componentVersion: await this.getComponentVersion(page)
      }
    };
  }

  private async getComponentVersion(page: Page): Promise<string> {
    return await page.evaluate(() => {
      // Try to extract version from various sources
      const versionMeta = document.querySelector('meta[name="version"]');
      if (versionMeta) return versionMeta.getAttribute('content') || 'unknown';

      // Check for version in global objects
      if ((window as any).APP_VERSION) return (window as any).APP_VERSION;

      return 'legacy-unknown';
    });
  }
}

/**
 * Extracts positioning data from modern start position picker components
 */
export class ModernStartPositionExtractor {
  async extractPositionData(
    page: Page,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<StartPositionData> {
    // Wait for the specific start position to be visible
    const positionSelector = `[data-position-key="${positionKey}"], .pictograph-container[data-letter="${this.getLetterFromKey(positionKey)}"]`;
    await page.waitForSelector(positionSelector, { state: 'visible', timeout: 10000 });

    // Extract prop data from the modern pictograph
    const props = await page.evaluate((selector, gridMode) => {
      const positionElement = document.querySelector(selector);
      if (!positionElement) return [];

      // Look for modern prop elements
      const propElements = positionElement.querySelectorAll('svg g[data-component="prop"], svg circle[data-prop-color], svg g.prop');
      const extractedProps: PropPositionData[] = [];

      propElements.forEach((propEl) => {
        const element = propEl as SVGElement;
        const color = element.getAttribute('data-prop-color') ||
                     element.getAttribute('data-color') as 'blue' | 'red';
        const location = element.getAttribute('data-location') || '';

        // Extract coordinates from SVG positioning
        let x = 0, y = 0, rotation = 0;

        // Check for transform attribute
        const transform = element.getAttribute('transform');
        if (transform) {
          const translateMatch = transform.match(/translate\(([^)]+)\)/);
          const rotateMatch = transform.match(/rotate\(([^)]+)\)/);

          if (translateMatch) {
            const values = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
            x = values[0] || 0;
            y = values[1] || 0;
          }

          if (rotateMatch) {
            const rotateValues = rotateMatch[1].split(',').map(v => parseFloat(v.trim()));
            rotation = rotateValues[0] || 0;
          }
        }

        // Check for direct positioning attributes
        if (x === 0 && y === 0) {
          x = parseFloat(element.getAttribute('cx') || element.getAttribute('x') || '0');
          y = parseFloat(element.getAttribute('cy') || element.getAttribute('y') || '0');
        }

        // Get computed transform for comparison
        const computedStyle = window.getComputedStyle(element);

        if (color) {
          extractedProps.push({
            x,
            y,
            rotation,
            color,
            location,
            transformMatrix: transform || '',
            cssTransform: computedStyle.transform
          });
        }
      });

      return extractedProps;
    }, positionSelector, gridMode);

    // Extract letter information
    const letter = await page.evaluate((selector) => {
      const positionElement = document.querySelector(selector);
      const letterElement = positionElement?.querySelector('svg text, .position-label, [data-letter]');
      return letterElement?.textContent || letterElement?.getAttribute('data-letter') || '';
    }, positionSelector);

    return {
      positionKey,
      gridMode,
      props,
      letter,
      metadata: {
        timestamp: Date.now(),
        source: 'modern',
        componentVersion: await this.getComponentVersion(page)
      }
    };
  }

  private getLetterFromKey(positionKey: string): string {
    // Map position keys to letters
    const keyToLetter: Record<string, string> = {
      'alpha1_alpha1': 'A',
      'beta5_beta5': 'E',
      'gamma11_gamma11': 'K',
      'alpha2_alpha2': 'B',
      'beta4_beta4': 'D',
      'gamma12_gamma12': 'L'
    };
    return keyToLetter[positionKey] || '';
  }

  private async getComponentVersion(page: Page): Promise<string> {
    return await page.evaluate(() => {
      // Try to extract version from various sources
      const versionMeta = document.querySelector('meta[name="version"]');
      if (versionMeta) return versionMeta.getAttribute('content') || 'unknown';

      // Check for version in global objects
      if ((window as any).APP_VERSION) return (window as any).APP_VERSION;

      return 'modern-unknown';
    });
  }
}

/**
 * Compares coordinate positioning between legacy and modern implementations
 */
export class CoordinateComparator {
  constructor(private tolerance: number = 1.0) {}

  compare(legacyProps: PropPositionData[], modernProps: PropPositionData[]) {
    const discrepancies: Array<{
      color: 'blue' | 'red';
      expected: { x: number; y: number };
      actual: { x: number; y: number };
      difference: { x: number; y: number };
      magnitude: number;
    }> = [];

    for (const legacyProp of legacyProps) {
      const modernProp = modernProps.find(p => p.color === legacyProp.color);
      if (!modernProp) continue;

      const diffX = modernProp.x - legacyProp.x;
      const diffY = modernProp.y - legacyProp.y;
      const magnitude = Math.sqrt(diffX * diffX + diffY * diffY);

      if (magnitude > this.tolerance) {
        discrepancies.push({
          color: legacyProp.color,
          expected: { x: legacyProp.x, y: legacyProp.y },
          actual: { x: modernProp.x, y: modernProp.y },
          difference: { x: diffX, y: diffY },
          magnitude
        });
      }
    }

    return discrepancies;
  }
}

/**
 * Compares rotation values between legacy and modern implementations
 */
export class RotationComparator {
  constructor(private tolerance: number = 0.5) {}

  compare(legacyProps: PropPositionData[], modernProps: PropPositionData[]) {
    const discrepancies: Array<{
      color: 'blue' | 'red';
      expected: number;
      actual: number;
      difference: number;
    }> = [];

    for (const legacyProp of legacyProps) {
      const modernProp = modernProps.find(p => p.color === legacyProp.color);
      if (!modernProp) continue;

      // Normalize angles to 0-360 range
      const normalizedLegacy = this.normalizeAngle(legacyProp.rotation);
      const normalizedModern = this.normalizeAngle(modernProp.rotation);

      const difference = this.angleDifference(normalizedLegacy, normalizedModern);

      if (Math.abs(difference) > this.tolerance) {
        discrepancies.push({
          color: legacyProp.color,
          expected: normalizedLegacy,
          actual: normalizedModern,
          difference
        });
      }
    }

    return discrepancies;
  }

  private normalizeAngle(angle: number): number {
    return ((angle % 360) + 360) % 360;
  }

  private angleDifference(angle1: number, angle2: number): number {
    const diff = angle2 - angle1;
    return ((diff + 180) % 360) - 180;
  }
}

/**
 * Generates detailed discrepancy reports
 */
export class DiscrepancyReporter {
  generateReport(comparisonResult: any): string {
    const lines: string[] = [];

    lines.push(`Position: ${comparisonResult.positionKey} (${comparisonResult.gridMode})`);
    lines.push(`Overall Match: ${comparisonResult.overallMatch ? 'PASS' : 'FAIL'}`);
    lines.push('');

    if (comparisonResult.coordinateDiscrepancies.length > 0) {
      lines.push('COORDINATE DISCREPANCIES:');
      comparisonResult.coordinateDiscrepancies.forEach((disc: any) => {
        lines.push(`  ${disc.color.toUpperCase()} prop:`);
        lines.push(`    Expected: (${disc.expected.x}, ${disc.expected.y})`);
        lines.push(`    Actual:   (${disc.actual.x}, ${disc.actual.y})`);
        lines.push(`    Diff:     (${disc.difference.x.toFixed(2)}, ${disc.difference.y.toFixed(2)})`);
        lines.push(`    Magnitude: ${disc.magnitude.toFixed(2)} pixels`);
        lines.push('');
      });
    }

    if (comparisonResult.rotationDiscrepancies.length > 0) {
      lines.push('ROTATION DISCREPANCIES:');
      comparisonResult.rotationDiscrepancies.forEach((disc: any) => {
        lines.push(`  ${disc.color.toUpperCase()} prop:`);
        lines.push(`    Expected: ${disc.expected.toFixed(2)}°`);
        lines.push(`    Actual:   ${disc.actual.toFixed(2)}°`);
        lines.push(`    Diff:     ${disc.difference.toFixed(2)}°`);
        lines.push('');
      });
    }

    if (comparisonResult.transformDiscrepancies.length > 0) {
      lines.push('TRANSFORM DISCREPANCIES:');
      comparisonResult.transformDiscrepancies.forEach((disc: any) => {
        lines.push(`  ${disc.color.toUpperCase()} prop: ${disc.issue}`);
        lines.push(`    Details: ${disc.details}`);
        lines.push('');
      });
    }

    if (comparisonResult.recommendations.length > 0) {
      lines.push('RECOMMENDATIONS:');
      comparisonResult.recommendations.forEach((rec: string) => {
        lines.push(`  - ${rec}`);
      });
    }

    return lines.join('\n');
  }
}

/**
 * Generates test data for various scenarios
 */
export class TestDataGenerator {
  generateStartPositionTestData() {
    return {
      diamond: {
        alpha1_alpha1: {
          letter: 'A',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 467, y: 323.9, rotation: 0 },
            red: { x: 483, y: 339.9, rotation: 0 }
          }
        },
        beta5_beta5: {
          letter: 'E',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 610.1, y: 467, rotation: 90 },
            red: { x: 626.1, y: 483, rotation: 90 }
          }
        },
        gamma11_gamma11: {
          letter: 'K',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 467, y: 610.1, rotation: 180 },
            red: { x: 483, y: 626.1, rotation: 180 }
          }
        }
      },
      box: {
        alpha2_alpha2: {
          letter: 'B',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 467, y: 317, rotation: 0 },
            red: { x: 483, y: 333, rotation: 0 }
          }
        },
        beta4_beta4: {
          letter: 'D',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 617, y: 467, rotation: 90 },
            red: { x: 633, y: 483, rotation: 90 }
          }
        },
        gamma12_gamma12: {
          letter: 'L',
          expectedProps: 2,
          expectedCoordinates: {
            blue: { x: 467, y: 617, rotation: 180 },
            red: { x: 483, y: 633, rotation: 180 }
          }
        }
      }
    };
  }

  generateValidationScenarios() {
    return [
      {
        name: 'Basic Positioning',
        description: 'Validate basic prop positioning without complex transforms',
        testCases: ['alpha1_alpha1', 'alpha2_alpha2']
      },
      {
        name: 'Rotation Validation',
        description: 'Validate prop rotation calculations',
        testCases: ['beta5_beta5', 'beta4_beta4']
      },
      {
        name: 'Complex Positioning',
        description: 'Validate complex positioning with multiple transforms',
        testCases: ['gamma11_gamma11', 'gamma12_gamma12']
      },
      {
        name: 'Cross-Grid Consistency',
        description: 'Validate consistency between diamond and box grid modes',
        testCases: ['alpha1_alpha1', 'alpha2_alpha2', 'beta5_beta5', 'beta4_beta4']
      }
    ];
  }
}

/**
 * Advanced transformation analysis utilities
 */
export class TransformationAnalyzer {
  /**
   * Parse CSS transform string into component values
   */
  parseCSSTransform(transform: string): {
    translateX: number;
    translateY: number;
    rotation: number;
    scaleX: number;
    scaleY: number;
  } {
    const result = {
      translateX: 0,
      translateY: 0,
      rotation: 0,
      scaleX: 1,
      scaleY: 1
    };

    if (!transform || transform === 'none') return result;

    // Parse translate
    const translateMatch = transform.match(/translate\(([^)]+)\)/);
    if (translateMatch) {
      const values = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
      result.translateX = values[0] || 0;
      result.translateY = values[1] || 0;
    }

    // Parse rotate
    const rotateMatch = transform.match(/rotate\(([^)]+)\)/);
    if (rotateMatch) {
      result.rotation = parseFloat(rotateMatch[1]) || 0;
    }

    // Parse scale
    const scaleMatch = transform.match(/scale\(([^)]+)\)/);
    if (scaleMatch) {
      const values = scaleMatch[1].split(',').map(v => parseFloat(v.trim()));
      result.scaleX = values[0] || 1;
      result.scaleY = values[1] || result.scaleX;
    }

    return result;
  }

  /**
   * Parse SVG transform attribute into component values
   */
  parseSVGTransform(transform: string): {
    translateX: number;
    translateY: number;
    rotation: number;
    rotationCenterX?: number;
    rotationCenterY?: number;
  } {
    const result = {
      translateX: 0,
      translateY: 0,
      rotation: 0,
      rotationCenterX: undefined as number | undefined,
      rotationCenterY: undefined as number | undefined
    };

    if (!transform) return result;

    // Parse translate
    const translateMatch = transform.match(/translate\(([^)]+)\)/);
    if (translateMatch) {
      const values = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
      result.translateX = values[0] || 0;
      result.translateY = values[1] || 0;
    }

    // Parse rotate with optional center
    const rotateMatch = transform.match(/rotate\(([^)]+)\)/);
    if (rotateMatch) {
      const values = rotateMatch[1].split(',').map(v => parseFloat(v.trim()));
      result.rotation = values[0] || 0;
      if (values.length >= 3) {
        result.rotationCenterX = values[1];
        result.rotationCenterY = values[2];
      }
    }

    return result;
  }

  /**
   * Compare two transformation objects for equivalence
   */
  compareTransformations(
    transform1: any,
    transform2: any,
    tolerance: { position: number; rotation: number }
  ): {
    equivalent: boolean;
    differences: string[];
  } {
    const differences: string[] = [];

    // Compare translations
    const positionDiff = Math.sqrt(
      Math.pow(transform1.translateX - transform2.translateX, 2) +
      Math.pow(transform1.translateY - transform2.translateY, 2)
    );

    if (positionDiff > tolerance.position) {
      differences.push(`Position difference: ${positionDiff.toFixed(2)} pixels`);
    }

    // Compare rotations
    const rotationDiff = Math.abs(this.normalizeAngle(transform1.rotation) - this.normalizeAngle(transform2.rotation));
    const normalizedRotationDiff = Math.min(rotationDiff, 360 - rotationDiff);

    if (normalizedRotationDiff > tolerance.rotation) {
      differences.push(`Rotation difference: ${normalizedRotationDiff.toFixed(2)} degrees`);
    }

    return {
      equivalent: differences.length === 0,
      differences
    };
  }

  private normalizeAngle(angle: number): number {
    return ((angle % 360) + 360) % 360;
  }
}
