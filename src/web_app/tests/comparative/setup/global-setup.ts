/**
 * Global Setup for Comparative Tests
 * 
 * Prepares the test environment by ensuring both applications are running
 * and accessible before test execution begins.
 */

import { chromium, FullConfig } from '@playwright/test';
import { getConfigForEnvironment } from '../config/test-config';

async function globalSetup(config: FullConfig) {
  console.log('🚀 Starting comparative test setup...');
  
  const testEnv = process.env.TEST_ENV || 'development';
  const testConfig = getConfigForEnvironment(testEnv);
  
  console.log(`📋 Test Environment: ${testEnv}`);
  console.log(`🔧 Configuration loaded for ${testEnv} environment`);
  
  // Create a browser instance for health checks
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Health check for legacy application
    console.log('🔍 Checking legacy application availability...');
    await page.goto(testConfig.urls.legacy, { 
      waitUntil: 'networkidle',
      timeout: testConfig.timeouts.navigation 
    });
    
    // Verify legacy app is functional
    await page.waitForSelector('body', { timeout: 10000 });
    console.log('✅ Legacy application is accessible');
    
    // Health check for modern application
    console.log('🔍 Checking modern application availability...');
    await page.goto(testConfig.urls.modern, { 
      waitUntil: 'networkidle',
      timeout: testConfig.timeouts.navigation 
    });
    
    // Verify modern app is functional
    await page.waitForSelector('body', { timeout: 10000 });
    console.log('✅ Modern application is accessible');
    
    // Verify construct tabs are available in both applications
    console.log('🔍 Verifying construct tab availability...');
    
    // Check legacy construct tab
    await page.goto(testConfig.urls.legacy);
    const legacyConstructTab = await page.locator(testConfig.selectors.legacy.constructTab).first();
    if (await legacyConstructTab.isVisible({ timeout: 5000 })) {
      console.log('✅ Legacy construct tab found');
    } else {
      console.warn('⚠️ Legacy construct tab not immediately visible');
    }
    
    // Check modern construct tab
    await page.goto(testConfig.urls.modern);
    const modernConstructTab = await page.locator(testConfig.selectors.modern.constructTab).first();
    if (await modernConstructTab.isVisible({ timeout: 5000 })) {
      console.log('✅ Modern construct tab found');
    } else {
      console.warn('⚠️ Modern construct tab not immediately visible');
    }
    
    // Create output directories
    console.log('📁 Creating output directories...');
    const fs = await import('fs');
    const path = await import('path');
    
    const outputDirs = [
      testConfig.reporting.outputDirectory,
      path.join(testConfig.reporting.outputDirectory, 'screenshots'),
      path.join(testConfig.reporting.outputDirectory, 'raw-data'),
      './test-results',
      './test-results/html-report',
      './test-results/artifacts'
    ];
    
    for (const dir of outputDirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 Created directory: ${dir}`);
      }
    }
    
    // Log test configuration summary
    console.log('\n📊 Test Configuration Summary:');
    console.log(`   Coordinate Tolerance: ${testConfig.tolerance.coordinates} pixels`);
    console.log(`   Rotation Tolerance: ${testConfig.tolerance.rotation} degrees`);
    console.log(`   Transform Tolerance: ${testConfig.tolerance.transform * 100}%`);
    console.log(`   Navigation Timeout: ${testConfig.timeouts.navigation}ms`);
    console.log(`   Component Load Timeout: ${testConfig.timeouts.componentLoad}ms`);
    console.log(`   Screenshots Enabled: ${testConfig.reporting.generateScreenshots}`);
    console.log(`   Detailed Logging: ${testConfig.reporting.detailedLogging}`);
    
    // Log grid modes and positions to be tested
    console.log('\n🎯 Test Coverage:');
    for (const gridMode of testConfig.gridModes) {
      console.log(`   ${gridMode.toUpperCase()} Grid:`);
      for (const position of testConfig.startPositions[gridMode]) {
        console.log(`     - ${position}`);
      }
    }
    
    console.log('\n✅ Global setup completed successfully');
    
  } catch (error) {
    console.error('❌ Global setup failed:', error);
    throw error;
  } finally {
    await page.close();
    await context.close();
    await browser.close();
  }
}

export default globalSetup;
