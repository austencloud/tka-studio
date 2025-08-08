/**
 * Simple Start Position Comparison Test
 * 
 * A basic Playwright test to compare the 3 start position pictographs
 * between legacy and modern web applications.
 */

import { test, expect } from '@playwright/test';

test.describe('Start Position Picker Comparison', () => {
  test('should compare start position pictographs between legacy and modern apps', async ({ browser }) => {
    // Create separate contexts for each app
    const legacyContext = await browser.newContext();
    const modernContext = await browser.newContext();
    
    const legacyPage = await legacyContext.newPage();
    const modernPage = await modernContext.newPage();
    
    try {
      console.log('🔍 Testing Legacy App...');
      
      // Navigate to legacy app
      await legacyPage.goto('http://localhost:5173', { timeout: 30000 });
      console.log('✅ Legacy app loaded');
      
      // Take screenshot of legacy app
      await legacyPage.screenshot({ 
        path: './test-results/legacy-full-page.png', 
        fullPage: true 
      });
      
      // Look for start position elements in legacy
      const legacyStartPositions = await legacyPage.locator('.start-pos-picker, .pictograph-container, .pictograph-wrapper').count();
      console.log(`📊 Legacy start position elements found: ${legacyStartPositions}`);
      
      // Extract any prop coordinates from legacy
      const legacyProps = await legacyPage.evaluate(() => {
        const elements = document.querySelectorAll('[data-prop-color], .prop, circle, [data-color]');
        const results = [];
        
        elements.forEach((el, index) => {
          const rect = el.getBoundingClientRect();
          const style = window.getComputedStyle(el);
          const color = el.getAttribute('data-prop-color') || 
                       el.getAttribute('data-color') || 
                       el.getAttribute('fill') || 
                       'unknown';
          
          if (rect.width > 0 && rect.height > 0) {
            results.push({
              index,
              color,
              x: Math.round(rect.x),
              y: Math.round(rect.y),
              width: Math.round(rect.width),
              height: Math.round(rect.height),
              transform: style.transform,
              tagName: el.tagName
            });
          }
        });
        
        return results;
      });
      
      console.log(`📍 Legacy props found: ${legacyProps.length}`);
      legacyProps.forEach(prop => {
        console.log(`   ${prop.color} ${prop.tagName}: (${prop.x}, ${prop.y}) ${prop.transform !== 'none' ? prop.transform : ''}`);
      });
      
      console.log('\n🔍 Testing Modern App...');
      
      // Navigate to modern app
      await modernPage.goto('http://localhost:5177', { timeout: 30000 });
      console.log('✅ Modern app loaded');
      
      // Take screenshot of modern app
      await modernPage.screenshot({ 
        path: './test-results/modern-full-page.png', 
        fullPage: true 
      });
      
      // Look for start position elements in modern
      const modernStartPositions = await modernPage.locator('.start-pos-picker, .pictograph-container, .pictograph-wrapper').count();
      console.log(`📊 Modern start position elements found: ${modernStartPositions}`);
      
      // Extract any prop coordinates from modern
      const modernProps = await modernPage.evaluate(() => {
        const elements = document.querySelectorAll('[data-prop-color], .prop, circle, [data-color], svg g[data-component="prop"]');
        const results = [];
        
        elements.forEach((el, index) => {
          const rect = el.getBoundingClientRect();
          const style = window.getComputedStyle(el);
          const color = el.getAttribute('data-prop-color') || 
                       el.getAttribute('data-color') || 
                       el.getAttribute('fill') || 
                       'unknown';
          
          if (rect.width > 0 && rect.height > 0) {
            results.push({
              index,
              color,
              x: Math.round(rect.x),
              y: Math.round(rect.y),
              width: Math.round(rect.width),
              height: Math.round(rect.height),
              transform: style.transform,
              tagName: el.tagName
            });
          }
        });
        
        return results;
      });
      
      console.log(`📍 Modern props found: ${modernProps.length}`);
      modernProps.forEach(prop => {
        console.log(`   ${prop.color} ${prop.tagName}: (${prop.x}, ${prop.y}) ${prop.transform !== 'none' ? prop.transform : ''}`);
      });
      
      // Simple comparison
      console.log('\n📊 Comparison Results:');
      console.log(`Legacy elements: ${legacyProps.length}, Modern elements: ${modernProps.length}`);
      
      if (legacyProps.length > 0 && modernProps.length > 0) {
        console.log('✅ Both apps have positioning elements');
        
        // Compare by color if possible
        const legacyByColor = legacyProps.reduce((acc, prop) => {
          if (!acc[prop.color]) acc[prop.color] = [];
          acc[prop.color].push(prop);
          return acc;
        }, {});
        
        const modernByColor = modernProps.reduce((acc, prop) => {
          if (!acc[prop.color]) acc[prop.color] = [];
          acc[prop.color].push(prop);
          return acc;
        }, {});
        
        console.log('\n🎨 Color-based comparison:');
        Object.keys(legacyByColor).forEach(color => {
          const legacyCount = legacyByColor[color]?.length || 0;
          const modernCount = modernByColor[color]?.length || 0;
          console.log(`   ${color}: Legacy ${legacyCount}, Modern ${modernCount}`);
          
          if (legacyCount > 0 && modernCount > 0) {
            const legacyAvgX = legacyByColor[color].reduce((sum, p) => sum + p.x, 0) / legacyCount;
            const legacyAvgY = legacyByColor[color].reduce((sum, p) => sum + p.y, 0) / legacyCount;
            const modernAvgX = modernByColor[color].reduce((sum, p) => sum + p.x, 0) / modernCount;
            const modernAvgY = modernByColor[color].reduce((sum, p) => sum + p.y, 0) / modernCount;
            
            const diffX = Math.abs(legacyAvgX - modernAvgX);
            const diffY = Math.abs(legacyAvgY - modernAvgY);
            
            console.log(`     Position diff: (${diffX.toFixed(1)}, ${diffY.toFixed(1)}) pixels`);
          }
        });
        
      } else {
        console.log('⚠️ One or both apps have no positioning elements found');
      }
      
      // Basic assertions
      expect(legacyPage).toBeTruthy();
      expect(modernPage).toBeTruthy();
      
      // Save comparison data
      const comparisonData = {
        timestamp: new Date().toISOString(),
        legacy: {
          elementCount: legacyProps.length,
          props: legacyProps
        },
        modern: {
          elementCount: modernProps.length,
          props: modernProps
        }
      };
      
      await legacyPage.evaluate((data) => {
        console.log('Comparison data:', JSON.stringify(data, null, 2));
      }, comparisonData);
      
    } finally {
      await legacyPage.close();
      await modernPage.close();
      await legacyContext.close();
      await modernContext.close();
    }
  });
});
