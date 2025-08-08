/**
 * Global Teardown for Comparative Tests
 * 
 * Cleans up after test execution and generates final summary reports.
 */

import { FullConfig } from '@playwright/test';
import { getConfigForEnvironment } from '../config/test-config';

async function globalTeardown(config: FullConfig) {
  console.log('🧹 Starting comparative test teardown...');
  
  const testEnv = process.env.TEST_ENV || 'development';
  const testConfig = getConfigForEnvironment(testEnv);
  
  try {
    // Import required modules
    const fs = await import('fs');
    const path = await import('path');
    
    // Generate summary report if results exist
    const resultsPath = './test-results/results.json';
    if (fs.existsSync(resultsPath)) {
      console.log('📊 Generating test summary...');
      
      const resultsData = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
      const summary = generateTestSummary(resultsData);
      
      // Save summary report
      const summaryPath = path.join(testConfig.reporting.outputDirectory, 'test-summary.json');
      fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
      
      // Generate human-readable summary
      const textSummary = generateTextSummary(summary);
      const textSummaryPath = path.join(testConfig.reporting.outputDirectory, 'test-summary.txt');
      fs.writeFileSync(textSummaryPath, textSummary);
      
      console.log('📄 Summary reports generated:');
      console.log(`   JSON: ${summaryPath}`);
      console.log(`   Text: ${textSummaryPath}`);
      
      // Log key metrics
      console.log('\n📈 Test Execution Summary:');
      console.log(`   Total Tests: ${summary.totalTests}`);
      console.log(`   Passed: ${summary.passedTests}`);
      console.log(`   Failed: ${summary.failedTests}`);
      console.log(`   Success Rate: ${summary.successRate}%`);
      console.log(`   Total Duration: ${summary.totalDuration}ms`);
      
      if (summary.failedTests > 0) {
        console.log('\n❌ Failed Tests:');
        summary.failedTestDetails.forEach((test: any) => {
          console.log(`   - ${test.title}: ${test.error}`);
        });
      }
    }
    
    // Clean up temporary files if in CI environment
    if (process.env.CI && testConfig.reporting.saveRawData === false) {
      console.log('🗑️ Cleaning up temporary files...');
      
      const tempDirs = [
        './test-results/artifacts',
        path.join(testConfig.reporting.outputDirectory, 'raw-data')
      ];
      
      for (const dir of tempDirs) {
        if (fs.existsSync(dir)) {
          fs.rmSync(dir, { recursive: true, force: true });
          console.log(`🗑️ Cleaned up: ${dir}`);
        }
      }
    }
    
    // Archive results if configured
    if (process.env.ARCHIVE_RESULTS === 'true') {
      console.log('📦 Archiving test results...');
      await archiveResults(testConfig);
    }
    
    console.log('✅ Global teardown completed successfully');
    
  } catch (error) {
    console.error('❌ Global teardown failed:', error);
    // Don't throw error in teardown to avoid masking test failures
  }
}

function generateTestSummary(resultsData: any) {
  const totalTests = resultsData.suites?.reduce((total: number, suite: any) => {
    return total + (suite.specs?.length || 0);
  }, 0) || 0;
  
  const passedTests = resultsData.suites?.reduce((passed: number, suite: any) => {
    return passed + (suite.specs?.filter((spec: any) => 
      spec.tests?.every((test: any) => test.results?.every((result: any) => result.status === 'passed'))
    ).length || 0);
  }, 0) || 0;
  
  const failedTests = totalTests - passedTests;
  const successRate = totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0;
  
  const failedTestDetails = resultsData.suites?.flatMap((suite: any) => 
    suite.specs?.filter((spec: any) => 
      spec.tests?.some((test: any) => test.results?.some((result: any) => result.status !== 'passed'))
    ).map((spec: any) => ({
      title: spec.title,
      error: spec.tests?.[0]?.results?.[0]?.error?.message || 'Unknown error'
    })) || []
  ) || [];
  
  return {
    totalTests,
    passedTests,
    failedTests,
    successRate,
    totalDuration: resultsData.stats?.duration || 0,
    failedTestDetails,
    timestamp: new Date().toISOString(),
    environment: process.env.TEST_ENV || 'development'
  };
}

function generateTextSummary(summary: any): string {
  const lines = [
    '='.repeat(80),
    'START POSITION PICKER COMPARATIVE TEST SUMMARY',
    '='.repeat(80),
    '',
    `Execution Date: ${new Date(summary.timestamp).toLocaleString()}`,
    `Environment: ${summary.environment}`,
    `Total Duration: ${(summary.totalDuration / 1000).toFixed(2)} seconds`,
    '',
    'RESULTS:',
    `  Total Tests: ${summary.totalTests}`,
    `  Passed: ${summary.passedTests}`,
    `  Failed: ${summary.failedTests}`,
    `  Success Rate: ${summary.successRate}%`,
    ''
  ];
  
  if (summary.failedTests > 0) {
    lines.push('FAILED TESTS:');
    summary.failedTestDetails.forEach((test: any) => {
      lines.push(`  - ${test.title}`);
      lines.push(`    Error: ${test.error}`);
    });
    lines.push('');
  }
  
  lines.push('RECOMMENDATIONS:');
  if (summary.successRate === 100) {
    lines.push('  ✅ All tests passed! The modern implementation has pixel-perfect parity with the legacy version.');
  } else if (summary.successRate >= 90) {
    lines.push('  ⚠️ Most tests passed, but some minor discrepancies were found.');
    lines.push('  📋 Review failed test details for specific adjustment recommendations.');
  } else if (summary.successRate >= 70) {
    lines.push('  ❌ Significant discrepancies found between legacy and modern implementations.');
    lines.push('  🔧 Major adjustments needed in coordinate calculations or rotation logic.');
  } else {
    lines.push('  🚨 Critical issues found. Modern implementation requires substantial corrections.');
    lines.push('  🔍 Review positioning algorithms, grid coordinate systems, and transform logic.');
  }
  
  lines.push('');
  lines.push('For detailed analysis, review the JSON report and generated screenshots.');
  lines.push('='.repeat(80));
  
  return lines.join('\n');
}

async function archiveResults(testConfig: any) {
  const fs = await import('fs');
  const path = await import('path');
  const archiver = await import('archiver');
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const archivePath = path.join(testConfig.reporting.outputDirectory, `test-results-${timestamp}.zip`);
  
  const output = fs.createWriteStream(archivePath);
  const archive = archiver.default('zip', { zlib: { level: 9 } });
  
  return new Promise<void>((resolve, reject) => {
    output.on('close', () => {
      console.log(`📦 Results archived to: ${archivePath} (${archive.pointer()} bytes)`);
      resolve();
    });
    
    archive.on('error', reject);
    archive.pipe(output);
    
    // Add test results directory to archive
    archive.directory('./test-results/', 'test-results');
    archive.directory(testConfig.reporting.outputDirectory, 'comparative-results');
    
    archive.finalize();
  });
}

export default globalTeardown;
