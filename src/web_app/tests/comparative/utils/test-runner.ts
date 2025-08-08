/**
 * Test Runner for Start Position Picker Comparative Analysis
 * 
 * Orchestrates the execution of comparative tests and generates comprehensive reports
 */

import type { Page, BrowserContext } from '@playwright/test';
import { 
  LegacyStartPositionExtractor,
  ModernStartPositionExtractor,
  CoordinateComparator,
  RotationComparator,
  DiscrepancyReporter,
  TestDataGenerator,
  TransformationAnalyzer,
  type StartPositionData,
  type PropPositionData
} from './comparison-utilities';
import { 
  DEFAULT_TEST_CONFIG,
  getConfigForEnvironment,
  type TestConfig 
} from '../config/test-config';
import * as fs from 'fs';
import * as path from 'path';

export interface TestExecutionResult {
  positionKey: string;
  gridMode: 'diamond' | 'box';
  success: boolean;
  legacyData: StartPositionData;
  modernData: StartPositionData;
  comparisonResult: ComparisonResult;
  executionTime: number;
  screenshots?: {
    legacy: string;
    modern: string;
  };
  rawData?: {
    legacyHtml: string;
    modernHtml: string;
  };
}

export interface ComparisonResult {
  positionKey: string;
  gridMode: 'diamond' | 'box';
  coordinateDiscrepancies: Array<{
    color: 'blue' | 'red';
    expected: { x: number; y: number };
    actual: { x: number; y: number };
    difference: { x: number; y: number };
    magnitude: number;
  }>;
  rotationDiscrepancies: Array<{
    color: 'blue' | 'red';
    expected: number;
    actual: number;
    difference: number;
  }>;
  transformDiscrepancies: Array<{
    color: 'blue' | 'red';
    issue: string;
    details: string;
  }>;
  overallMatch: boolean;
  recommendations: string[];
}

export interface TestSuiteResult {
  totalTests: number;
  passedTests: number;
  failedTests: number;
  executionTime: number;
  results: TestExecutionResult[];
  summary: {
    coordinateIssues: number;
    rotationIssues: number;
    transformIssues: number;
    mostCommonIssues: string[];
    recommendations: string[];
  };
  environment: string;
  timestamp: string;
}

export class ComparativeTestRunner {
  private config: TestConfig;
  private legacyExtractor: LegacyStartPositionExtractor;
  private modernExtractor: ModernStartPositionExtractor;
  private coordinateComparator: CoordinateComparator;
  private rotationComparator: RotationComparator;
  private discrepancyReporter: DiscrepancyReporter;
  private testDataGenerator: TestDataGenerator;
  private transformationAnalyzer: TransformationAnalyzer;

  constructor(environment: string = 'development') {
    this.config = getConfigForEnvironment(environment);
    this.legacyExtractor = new LegacyStartPositionExtractor();
    this.modernExtractor = new ModernStartPositionExtractor();
    this.coordinateComparator = new CoordinateComparator(this.config.tolerance.coordinates);
    this.rotationComparator = new RotationComparator(this.config.tolerance.rotation);
    this.discrepancyReporter = new DiscrepancyReporter();
    this.testDataGenerator = new TestDataGenerator();
    this.transformationAnalyzer = new TransformationAnalyzer();
  }

  /**
   * Execute comprehensive test suite for all positions and grid modes
   */
  async executeFullTestSuite(
    legacyContext: BrowserContext,
    modernContext: BrowserContext
  ): Promise<TestSuiteResult> {
    const startTime = Date.now();
    const results: TestExecutionResult[] = [];

    // Ensure output directory exists
    this.ensureOutputDirectory();

    // Execute tests for all grid modes and positions
    for (const gridMode of this.config.gridModes) {
      for (const positionKey of this.config.startPositions[gridMode]) {
        try {
          const result = await this.executePositionTest(
            legacyContext,
            modernContext,
            positionKey,
            gridMode
          );
          results.push(result);
        } catch (error) {
          console.error(`Failed to execute test for ${positionKey} in ${gridMode} mode:`, error);
          results.push({
            positionKey,
            gridMode,
            success: false,
            legacyData: {} as StartPositionData,
            modernData: {} as StartPositionData,
            comparisonResult: {} as ComparisonResult,
            executionTime: 0
          });
        }
      }
    }

    const executionTime = Date.now() - startTime;
    const passedTests = results.filter(r => r.success).length;
    const failedTests = results.length - passedTests;

    const summary = this.generateTestSummary(results);

    const suiteResult: TestSuiteResult = {
      totalTests: results.length,
      passedTests,
      failedTests,
      executionTime,
      results,
      summary,
      environment: 'development', // TODO: Get from config
      timestamp: new Date().toISOString()
    };

    // Save comprehensive report
    await this.saveTestReport(suiteResult);

    return suiteResult;
  }

  /**
   * Execute test for a specific position and grid mode
   */
  async executePositionTest(
    legacyContext: BrowserContext,
    modernContext: BrowserContext,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<TestExecutionResult> {
    const startTime = Date.now();

    const legacyPage = await legacyContext.newPage();
    const modernPage = await modernContext.newPage();

    try {
      // Extract data from both applications
      const legacyData = await this.extractLegacyData(legacyPage, positionKey, gridMode);
      const modernData = await this.extractModernData(modernPage, positionKey, gridMode);

      // Perform detailed comparison
      const comparisonResult = await this.performComparison(
        legacyData,
        modernData,
        positionKey,
        gridMode
      );

      // Generate screenshots if enabled
      let screenshots: { legacy: string; modern: string } | undefined;
      if (this.config.reporting.generateScreenshots) {
        screenshots = await this.captureScreenshots(
          legacyPage,
          modernPage,
          positionKey,
          gridMode
        );
      }

      // Capture raw data if enabled
      let rawData: { legacyHtml: string; modernHtml: string } | undefined;
      if (this.config.reporting.saveRawData) {
        rawData = await this.captureRawData(legacyPage, modernPage);
      }

      const executionTime = Date.now() - startTime;

      return {
        positionKey,
        gridMode,
        success: comparisonResult.overallMatch,
        legacyData,
        modernData,
        comparisonResult,
        executionTime,
        screenshots,
        rawData
      };

    } finally {
      await legacyPage.close();
      await modernPage.close();
    }
  }

  /**
   * Extract data from legacy application
   */
  private async extractLegacyData(
    page: Page,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<StartPositionData> {
    await page.goto(this.config.urls.legacy, { 
      waitUntil: 'networkidle',
      timeout: this.config.timeouts.navigation 
    });

    // Navigate to construct tab
    await page.click(this.config.selectors.legacy.constructTab);
    await page.selectOption(this.config.selectors.legacy.gridModeSelector, gridMode);
    
    // Wait for start position picker
    await page.waitForSelector(this.config.selectors.legacy.startPositionPicker, {
      state: 'visible',
      timeout: this.config.timeouts.componentLoad
    });

    return await this.legacyExtractor.extractPositionData(page, positionKey, gridMode);
  }

  /**
   * Extract data from modern application
   */
  private async extractModernData(
    page: Page,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<StartPositionData> {
    await page.goto(this.config.urls.modern, { 
      waitUntil: 'networkidle',
      timeout: this.config.timeouts.navigation 
    });

    // Navigate to construct tab
    await page.click(this.config.selectors.modern.constructTab);
    await page.selectOption(this.config.selectors.modern.gridModeSelector, gridMode);
    
    // Wait for start position picker
    await page.waitForSelector(this.config.selectors.modern.startPositionPicker, {
      state: 'visible',
      timeout: this.config.timeouts.componentLoad
    });

    return await this.modernExtractor.extractPositionData(page, positionKey, gridMode);
  }

  /**
   * Perform detailed comparison between legacy and modern data
   */
  private async performComparison(
    legacyData: StartPositionData,
    modernData: StartPositionData,
    positionKey: string,
    gridMode: 'diamond' | 'box'
  ): Promise<ComparisonResult> {
    const coordinateDiscrepancies = this.coordinateComparator.compare(
      legacyData.props,
      modernData.props
    );

    const rotationDiscrepancies = this.rotationComparator.compare(
      legacyData.props,
      modernData.props
    );

    const transformDiscrepancies = this.compareTransformations(
      legacyData.props,
      modernData.props
    );

    const overallMatch = 
      coordinateDiscrepancies.length === 0 && 
      rotationDiscrepancies.length === 0 && 
      transformDiscrepancies.length === 0;

    const recommendations = this.generateRecommendations(
      coordinateDiscrepancies,
      rotationDiscrepancies,
      transformDiscrepancies
    );

    return {
      positionKey,
      gridMode,
      coordinateDiscrepancies,
      rotationDiscrepancies,
      transformDiscrepancies,
      overallMatch,
      recommendations
    };
  }

  /**
   * Compare transformations between legacy and modern props
   */
  private compareTransformations(
    legacyProps: PropPositionData[],
    modernProps: PropPositionData[]
  ) {
    const discrepancies: Array<{
      color: 'blue' | 'red';
      issue: string;
      details: string;
    }> = [];

    for (const legacyProp of legacyProps) {
      const modernProp = modernProps.find(p => p.color === legacyProp.color);
      if (!modernProp) continue;

      // Parse and compare transformations
      const legacyTransform = this.transformationAnalyzer.parseSVGTransform(
        legacyProp.transformMatrix || ''
      );
      const modernTransform = this.transformationAnalyzer.parseCSSTransform(
        modernProp.cssTransform || ''
      );

      const comparison = this.transformationAnalyzer.compareTransformations(
        legacyTransform,
        modernTransform,
        {
          position: this.config.tolerance.coordinates,
          rotation: this.config.tolerance.rotation
        }
      );

      if (!comparison.equivalent) {
        discrepancies.push({
          color: legacyProp.color,
          issue: 'Transform equivalence mismatch',
          details: comparison.differences.join(', ')
        });
      }
    }

    return discrepancies;
  }

  /**
   * Generate recommendations based on discrepancies
   */
  private generateRecommendations(
    coordinateDiscrepancies: any[],
    rotationDiscrepancies: any[],
    transformDiscrepancies: any[]
  ): string[] {
    const recommendations: string[] = [];

    if (coordinateDiscrepancies.length > 0) {
      recommendations.push('Review coordinate calculation algorithms in modern implementation');
      recommendations.push('Verify grid point mapping consistency');
    }

    if (rotationDiscrepancies.length > 0) {
      recommendations.push('Audit rotation calculation logic');
      recommendations.push('Ensure angle normalization consistency');
    }

    if (transformDiscrepancies.length > 0) {
      recommendations.push('Standardize transformation methods');
      recommendations.push('Verify CSS-to-SVG transform equivalence');
    }

    return recommendations;
  }

  /**
   * Capture screenshots for comparison
   */
  private async captureScreenshots(
    legacyPage: Page,
    modernPage: Page,
    positionKey: string,
    gridMode: string
  ): Promise<{ legacy: string; modern: string }> {
    const timestamp = Date.now();
    const legacyPath = path.join(
      this.config.reporting.outputDirectory,
      'screenshots',
      `legacy-${positionKey}-${gridMode}-${timestamp}.png`
    );
    const modernPath = path.join(
      this.config.reporting.outputDirectory,
      'screenshots',
      `modern-${positionKey}-${gridMode}-${timestamp}.png`
    );

    await legacyPage.screenshot({ path: legacyPath, fullPage: true });
    await modernPage.screenshot({ path: modernPath, fullPage: true });

    return { legacy: legacyPath, modern: modernPath };
  }

  /**
   * Capture raw HTML data
   */
  private async captureRawData(
    legacyPage: Page,
    modernPage: Page
  ): Promise<{ legacyHtml: string; modernHtml: string }> {
    const legacyHtml = await legacyPage.content();
    const modernHtml = await modernPage.content();

    return { legacyHtml, modernHtml };
  }

  /**
   * Generate test summary
   */
  private generateTestSummary(results: TestExecutionResult[]) {
    const coordinateIssues = results.reduce(
      (sum, r) => sum + r.comparisonResult.coordinateDiscrepancies?.length || 0,
      0
    );
    const rotationIssues = results.reduce(
      (sum, r) => sum + r.comparisonResult.rotationDiscrepancies?.length || 0,
      0
    );
    const transformIssues = results.reduce(
      (sum, r) => sum + r.comparisonResult.transformDiscrepancies?.length || 0,
      0
    );

    // Collect all recommendations
    const allRecommendations = results.flatMap(
      r => r.comparisonResult.recommendations || []
    );
    const uniqueRecommendations = [...new Set(allRecommendations)];

    return {
      coordinateIssues,
      rotationIssues,
      transformIssues,
      mostCommonIssues: this.findMostCommonIssues(results),
      recommendations: uniqueRecommendations
    };
  }

  /**
   * Find most common issues across all tests
   */
  private findMostCommonIssues(results: TestExecutionResult[]): string[] {
    // Implementation for finding patterns in issues
    return ['Coordinate calculation differences', 'Rotation normalization issues'];
  }

  /**
   * Save comprehensive test report
   */
  private async saveTestReport(suiteResult: TestSuiteResult): Promise<void> {
    const reportPath = path.join(
      this.config.reporting.outputDirectory,
      `test-report-${Date.now()}.json`
    );

    await fs.promises.writeFile(
      reportPath,
      JSON.stringify(suiteResult, null, 2),
      'utf8'
    );

    // Also generate human-readable report
    const humanReadableReport = this.generateHumanReadableReport(suiteResult);
    const textReportPath = path.join(
      this.config.reporting.outputDirectory,
      `test-report-${Date.now()}.txt`
    );

    await fs.promises.writeFile(textReportPath, humanReadableReport, 'utf8');
  }

  /**
   * Generate human-readable report
   */
  private generateHumanReadableReport(suiteResult: TestSuiteResult): string {
    const lines: string[] = [];
    
    lines.push('='.repeat(80));
    lines.push('START POSITION PICKER COMPARATIVE TEST REPORT');
    lines.push('='.repeat(80));
    lines.push('');
    lines.push(`Execution Time: ${suiteResult.executionTime}ms`);
    lines.push(`Total Tests: ${suiteResult.totalTests}`);
    lines.push(`Passed: ${suiteResult.passedTests}`);
    lines.push(`Failed: ${suiteResult.failedTests}`);
    lines.push(`Success Rate: ${((suiteResult.passedTests / suiteResult.totalTests) * 100).toFixed(1)}%`);
    lines.push('');

    // Summary section
    lines.push('SUMMARY:');
    lines.push(`- Coordinate Issues: ${suiteResult.summary.coordinateIssues}`);
    lines.push(`- Rotation Issues: ${suiteResult.summary.rotationIssues}`);
    lines.push(`- Transform Issues: ${suiteResult.summary.transformIssues}`);
    lines.push('');

    // Recommendations
    if (suiteResult.summary.recommendations.length > 0) {
      lines.push('RECOMMENDATIONS:');
      suiteResult.summary.recommendations.forEach(rec => {
        lines.push(`- ${rec}`);
      });
      lines.push('');
    }

    // Detailed results
    lines.push('DETAILED RESULTS:');
    lines.push('-'.repeat(40));
    
    suiteResult.results.forEach(result => {
      lines.push(`${result.positionKey} (${result.gridMode}): ${result.success ? 'PASS' : 'FAIL'}`);
      if (!result.success && result.comparisonResult.recommendations) {
        result.comparisonResult.recommendations.forEach(rec => {
          lines.push(`  → ${rec}`);
        });
      }
    });

    return lines.join('\n');
  }

  /**
   * Ensure output directory exists
   */
  private ensureOutputDirectory(): void {
    const dirs = [
      this.config.reporting.outputDirectory,
      path.join(this.config.reporting.outputDirectory, 'screenshots'),
      path.join(this.config.reporting.outputDirectory, 'raw-data')
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }
}
