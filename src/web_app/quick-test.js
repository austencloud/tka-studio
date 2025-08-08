/**
 * Quick test to see what's in the modern app
 */

import { chromium } from 'playwright';

async function quickTest() {
  console.log('🚀 Quick test of modern app...');
  
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  try {
    await page.goto('http://localhost:5177', { timeout: 30000 });
    console.log('✅ Modern app loaded');
    
    // Wait a bit for content to load
    await page.waitForTimeout(3000);
    
    // Take screenshot
    await page.screenshot({ path: './test-results/quick-test.png', fullPage: true });
    
    // Look for start position related content
    const startPositionInfo = await page.evaluate(() => {
      // Look for any elements that might be start positions
      const elements = document.querySelectorAll('*');
      const results = [];
      
      elements.forEach(el => {
        const text = el.textContent?.toLowerCase() || '';
        const className = el.className?.toString().toLowerCase() || '';
        const id = el.id?.toLowerCase() || '';
        
        if (text.includes('start') || 
            text.includes('position') ||
            className.includes('start') ||
            className.includes('position') ||
            className.includes('pictograph') ||
            id.includes('start') ||
            id.includes('position')) {
          
          results.push({
            tagName: el.tagName,
            className: el.className,
            id: el.id,
            textContent: el.textContent?.substring(0, 100),
            hasChildren: el.children.length > 0
          });
        }
      });
      
      return results.slice(0, 10); // First 10 matches
    });
    
    console.log('🔍 Start position related elements:');
    startPositionInfo.forEach((el, index) => {
      console.log(`   ${index}: ${el.tagName} .${el.className} #${el.id}`);
      if (el.textContent) console.log(`      Text: ${el.textContent}`);
    });
    
    // Look for SVG elements specifically
    const svgCount = await page.locator('svg').count();
    console.log(`📊 SVG elements found: ${svgCount}`);
    
    if (svgCount > 0) {
      const svgDetails = await page.evaluate(() => {
        const svgs = document.querySelectorAll('svg');
        return Array.from(svgs).slice(0, 3).map((svg, index) => ({
          index,
          viewBox: svg.getAttribute('viewBox'),
          width: svg.getAttribute('width'),
          height: svg.getAttribute('height'),
          childCount: svg.children.length,
          hasCircles: svg.querySelectorAll('circle').length,
          hasGroups: svg.querySelectorAll('g').length
        }));
      });
      
      console.log('📊 SVG details:');
      svgDetails.forEach(svg => {
        console.log(`   SVG ${svg.index}: ${svg.width}x${svg.height}, viewBox: ${svg.viewBox}`);
        console.log(`     Children: ${svg.childCount}, Circles: ${svg.hasCircles}, Groups: ${svg.hasGroups}`);
      });
    }
    
    // Check if we can find any props or positioning elements
    const propElements = await page.evaluate(() => {
      const selectors = ['circle', '[data-prop-color]', '[data-color]', '.prop'];
      const results = [];
      
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach((el, index) => {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            results.push({
              selector,
              index,
              tagName: el.tagName,
              x: Math.round(rect.x),
              y: Math.round(rect.y),
              color: el.getAttribute('data-prop-color') || el.getAttribute('data-color') || el.getAttribute('fill')
            });
          }
        });
      });
      
      return results;
    });
    
    console.log(`📍 Prop-like elements found: ${propElements.length}`);
    propElements.forEach(prop => {
      console.log(`   ${prop.selector} ${prop.tagName}: (${prop.x}, ${prop.y}) color: ${prop.color}`);
    });
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await page.close();
    await browser.close();
  }
  
  console.log('✅ Quick test completed');
}

// Create test-results directory
import fs from 'fs';
if (!fs.existsSync('./test-results')) {
  fs.mkdirSync('./test-results', { recursive: true });
}

quickTest().catch(console.error);
