#!/usr/bin/env node

/**
 * 🧪 COMPREHENSIVE TEST RUNNER
 *
 * Master test runner that executes all test suites with detailed reporting,
 * performance monitoring, and quality gates for enterprise CI/CD pipelines.
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

interface TestSuiteResult {
  name: string;
  passed: boolean;
  duration: number;
  coverage?: number;
  details: any;
}

interface TestRunResult {
  success: boolean;
  totalSuites: number;
  passedSuites: number;
  failedSuites: number;
  totalDuration: number;
  overallCoverage: number;
  suites: TestSuiteResult[];
  qualityGates: {
    coverage: boolean;
    performance: boolean;
    stability: boolean;
  };
}

class TKATestRunner {
  private results: TestSuiteResult[] = [];
  private startTime: number = 0;

  async runAllTests(): Promise<TestRunResult> {
    console.log('🚀 Starting TKA DI Comprehensive Test Suite\n');
    this.startTime = Date.now();

    // Ensure output directories exist
    this.ensureDirectories();

    try {
      // Run test suites in order
      await this.runCoreTests();
      await this.runPerformanceTests();
      await this.runIntegrationTests();
      await this.runCompatibilityTests();
      await this.runStabilityTests();
      await this.runCoverageAnalysis();

      // Generate final report
      const result = this.generateFinalReport();
      await this.saveResults(result);

      return result;

    } catch (error) {
      console.error('❌ Test suite execution failed:', error);
      throw error;
    }
  }

  private ensureDirectories(): void {
    const dirs = ['./test-results', './coverage', './reports'];
    dirs.forEach(dir => {
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    });
  }

  private async runCoreTests(): Promise<void> {
    console.log('🔧 Running Core DI System Tests...');

    const suites = [
      { name: 'ServiceContainer', pattern: 'core/ServiceContainer.test.ts' },
      { name: 'ServiceRegistry', pattern: 'core/ServiceRegistry.test.ts' },
      { name: 'ResolverChain', pattern: 'core/ResolverChain.test.ts' },
      { name: 'CircularDependency', pattern: 'core/CircularDependency.test.ts' }
    ];

    for (const suite of suites) {
      await this.runTestSuite(suite.name, suite.pattern, 'core');
    }
  }

  private async runPerformanceTests(): Promise<void> {
    console.log('⚡ Running Performance Tests...');

    await this.runTestSuite(
      'Performance & Stability',
      'performance/PerformanceStability.test.ts',
      'performance'
    );
  }

  private async runIntegrationTests(): Promise<void> {
    console.log('🔗 Running Integration Tests...');

    await this.runTestSuite(
      'Cross-Platform Compatibility',
      'integration/CrossPlatformCompatibility.test.ts',
      'integration'
    );
  }

  private async runCompatibilityTests(): Promise<void> {
    console.log('🌐 Running Compatibility Tests...');

    // Test with different environments
    const environments = ['jsdom', 'node'];

    for (const env of environments) {
      try {
        const result = await this.runWithEnvironment(env);
        this.results.push({
          name: `Compatibility-${env}`,
          passed: result.success,
          duration: result.duration,
          details: result
        });
      } catch (error) {
        this.results.push({
          name: `Compatibility-${env}`,
          passed: false,
          duration: 0,
          details: { error: error.message }
        });
      }
    }
  }

  private async runStabilityTests(): Promise<void> {
    console.log('🛡️ Running Stability Tests...');

    // Long-running stability test
    try {
      const command = 'vitest run performance/PerformanceStability.test.ts --reporter=json';
      const output = execSync(command, { encoding: 'utf8', timeout: 300000 }); // 5 min timeout
      const result = JSON.parse(output);

      this.results.push({
        name: 'Long-Running Stability',
        passed: result.success,
        duration: result.duration || 0,
        details: result
      });
    } catch (error) {
      this.results.push({
        name: 'Long-Running Stability',
        passed: false,
        duration: 0,
        details: { error: error.message }
      });
    }
  }

  private async runCoverageAnalysis(): Promise<void> {
    console.log('📊 Running Coverage Analysis...');

    try {
      const command = 'vitest run --coverage --reporter=json';
      const output = execSync(command, { encoding: 'utf8' });
      const result = JSON.parse(output);

      this.results.push({
        name: 'Coverage Analysis',
        passed: result.success,
        duration: result.duration || 0,
        coverage: result.coverage?.global?.lines || 0,
        details: result
      });
    } catch (error) {
      this.results.push({
        name: 'Coverage Analysis',
        passed: false,
        duration: 0,
        coverage: 0,
        details: { error: error.message }
      });
    }
  }

  private async runTestSuite(name: string, pattern: string, category: string): Promise<void> {
    const startTime = Date.now();

    try {
      console.log(`  📝 ${name}...`);

      const command = `vitest run ${pattern} --reporter=json`;
      const output = execSync(command, { encoding: 'utf8' });
      const result = JSON.parse(output);

      const duration = Date.now() - startTime;
      const passed = result.success || result.testResults?.every((t: any) => t.status === 'passed');

      this.results.push({
        name,
        passed,
        duration,
        details: result
      });

      console.log(`    ${passed ? '✅' : '❌'} ${name} (${duration}ms)`);

    } catch (error) {
      const duration = Date.now() - startTime;

      this.results.push({
        name,
        passed: false,
        duration,
        details: { error: error.message }
      });

      console.log(`    ❌ ${name} FAILED (${duration}ms)`);
      console.error(`       Error: ${error.message}`);
    }
  }

  private async runWithEnvironment(environment: string): Promise<any> {
    const startTime = Date.now();

    try {
      const command = `vitest run --environment=${environment} --reporter=json`;
      const output = execSync(command, { encoding: 'utf8' });
      const result = JSON.parse(output);

      return {
        success: result.success,
        duration: Date.now() - startTime,
        environment,
        details: result
      };
    } catch (error) {
      return {
        success: false,
        duration: Date.now() - startTime,
        environment,
        error: error.message
      };
    }
  }

  private generateFinalReport(): TestRunResult {
    const totalDuration = Date.now() - this.startTime;
    const passedSuites = this.results.filter(r => r.passed).length;
    const failedSuites = this.results.filter(r => !r.passed).length;

    // Calculate overall coverage
    const coverageResults = this.results.filter(r => r.coverage !== undefined);
    const overallCoverage = coverageResults.length > 0
      ? coverageResults.reduce((sum, r) => sum + (r.coverage || 0), 0) / coverageResults.length
      : 0;

    // Quality gates
    const qualityGates = {
      coverage: overallCoverage >= 90, // 90% coverage required
      performance: this.checkPerformanceGate(),
      stability: this.checkStabilityGate()
    };

    const success = failedSuites === 0 && Object.values(qualityGates).every(gate => gate);

    return {
      success,
      totalSuites: this.results.length,
      passedSuites,
      failedSuites,
      totalDuration,
      overallCoverage,
      suites: this.results,
      qualityGates
    };
  }

  private checkPerformanceGate(): boolean {
    const perfResults = this.results.filter(r => r.name.includes('Performance'));
    return perfResults.length > 0 && perfResults.every(r => r.passed);
  }

  private checkStabilityGate(): boolean {
    const stabilityResults = this.results.filter(r => r.name.includes('Stability'));
    return stabilityResults.length > 0 && stabilityResults.every(r => r.passed);
  }

  private async saveResults(result: TestRunResult): Promise<void> {
    // Save JSON results
    const jsonPath = join('./test-results', 'comprehensive-results.json');
    writeFileSync(jsonPath, JSON.stringify(result, null, 2));

    // Generate HTML report
    const htmlReport = this.generateHtmlReport(result);
    const htmlPath = join('./test-results', 'comprehensive-report.html');
    writeFileSync(htmlPath, htmlReport);

    // Generate CI summary
    const ciSummary = this.generateCISummary(result);
    const ciPath = join('./test-results', 'ci-summary.txt');
    writeFileSync(ciPath, ciSummary);

    console.log('\n📄 Reports generated:');
    console.log(`  📊 JSON: ${jsonPath}`);
    console.log(`  🌐 HTML: ${htmlPath}`);
    console.log(`  🤖 CI: ${ciPath}`);
  }

  private generateHtmlReport(result: TestRunResult): string {
    const statusIcon = result.success ? '✅' : '❌';
    const statusColor = result.success ? 'green' : 'red';

    return `
<!DOCTYPE html>
<html>
<head>
    <title>TKA DI Test Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        .status { font-size: 24px; color: ${statusColor}; }
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }
        .metric { background: #f9f9f9; padding: 15px; border-radius: 8px; text-align: center; }
        .suite { margin: 10px 0; padding: 10px; border-left: 4px solid #ddd; }
        .passed { border-left-color: green; }
        .failed { border-left-color: red; }
        .quality-gates { background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 TKA DI Comprehensive Test Results</h1>
        <div class="status">${statusIcon} ${result.success ? 'ALL TESTS PASSED' : 'TESTS FAILED'}</div>
        <p>Generated: ${new Date().toISOString()}</p>
    </div>

    <div class="metrics">
        <div class="metric">
            <h3>Total Suites</h3>
            <div style="font-size: 24px;">${result.totalSuites}</div>
        </div>
        <div class="metric">
            <h3>Passed</h3>
            <div style="font-size: 24px; color: green;">${result.passedSuites}</div>
        </div>
        <div class="metric">
            <h3>Failed</h3>
            <div style="font-size: 24px; color: red;">${result.failedSuites}</div>
        </div>
        <div class="metric">
            <h3>Coverage</h3>
            <div style="font-size: 24px;">${result.overallCoverage.toFixed(1)}%</div>
        </div>
    </div>

    <div class="quality-gates">
        <h3>🎯 Quality Gates</h3>
        <ul>
            <li>${result.qualityGates.coverage ? '✅' : '❌'} Coverage ≥ 90% (${result.overallCoverage.toFixed(1)}%)</li>
            <li>${result.qualityGates.performance ? '✅' : '❌'} Performance Tests</li>
            <li>${result.qualityGates.stability ? '✅' : '❌'} Stability Tests</li>
        </ul>
    </div>

    <h3>📋 Test Suites</h3>
    ${result.suites.map(suite => `
        <div class="suite ${suite.passed ? 'passed' : 'failed'}">
            <strong>${suite.passed ? '✅' : '❌'} ${suite.name}</strong>
            <span style="float: right;">${suite.duration}ms</span>
            ${suite.coverage ? `<br><small>Coverage: ${suite.coverage.toFixed(1)}%</small>` : ''}
        </div>
    `).join('')}

    <div style="margin-top: 40px; padding: 20px; background: #f5f5f5; border-radius: 8px;">
        <h3>🚀 TKA Enterprise DI System</h3>
        <p>Your web dependency injection system now has enterprise-grade testing coverage!</p>
        <p><strong>Total Duration:</strong> ${(result.totalDuration / 1000).toFixed(2)} seconds</p>
    </div>
</body>
</html>`;
  }

  private generateCISummary(result: TestRunResult): string {
    return `
TKA DI Test Suite Results
========================

Status: ${result.success ? 'PASSED' : 'FAILED'}
Total Suites: ${result.totalSuites}
Passed: ${result.passedSuites}
Failed: ${result.failedSuites}
Coverage: ${result.overallCoverage.toFixed(1)}%
Duration: ${(result.totalDuration / 1000).toFixed(2)}s

Quality Gates:
- Coverage ≥ 90%: ${result.qualityGates.coverage ? 'PASS' : 'FAIL'}
- Performance: ${result.qualityGates.performance ? 'PASS' : 'FAIL'}
- Stability: ${result.qualityGates.stability ? 'PASS' : 'FAIL'}

${result.failedSuites > 0 ? `
Failed Suites:
${result.suites.filter(s => !s.passed).map(s => `- ${s.name}`).join('\n')}
` : ''}

Generated: ${new Date().toISOString()}
`;
  }

  private printFinalSummary(result: TestRunResult): void {
    console.log('\n' + '='.repeat(60));
    console.log('🧪 TKA DI COMPREHENSIVE TEST RESULTS');
    console.log('='.repeat(60));

    console.log(`\n📊 Summary:`);
    console.log(`  Status: ${result.success ? '✅ PASSED' : '❌ FAILED'}`);
    console.log(`  Total Suites: ${result.totalSuites}`);
    console.log(`  Passed: ${result.passedSuites}`);
    console.log(`  Failed: ${result.failedSuites}`);
    console.log(`  Coverage: ${result.overallCoverage.toFixed(1)}%`);
    console.log(`  Duration: ${(result.totalDuration / 1000).toFixed(2)}s`);

    console.log(`\n🎯 Quality Gates:`);
    console.log(`  Coverage ≥ 90%: ${result.qualityGates.coverage ? '✅' : '❌'}`);
    console.log(`  Performance: ${result.qualityGates.performance ? '✅' : '❌'}`);
    console.log(`  Stability: ${result.qualityGates.stability ? '✅' : '❌'}`);

    if (result.failedSuites > 0) {
      console.log(`\n❌ Failed Suites:`);
      result.suites.filter(s => !s.passed).forEach(suite => {
        console.log(`  - ${suite.name}`);
      });
    }

    console.log('\n' + '='.repeat(60));
    console.log(result.success
      ? '🎉 ALL TESTS PASSED - Your DI system is enterprise-ready!'
      : '💥 TESTS FAILED - Please review and fix issues before deployment'
    );
    console.log('='.repeat(60));
  }
}

// Main execution
async function main() {
  const runner = new TKATestRunner();

  try {
    const result = await runner.runAllTests();
    runner.printFinalSummary(result);

    // Exit with appropriate code for CI/CD
    process.exit(result.success ? 0 : 1);

  } catch (error) {
    console.error('💥 Test runner failed:', error);
    process.exit(1);
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { TKATestRunner };
