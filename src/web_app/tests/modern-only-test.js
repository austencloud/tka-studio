/**
 * Modern App Only Test
 * 
 * Test just the modern app to see what start position elements are available
 */

import { test, expect } from '@playwright/test';

test('should find start position elements in modern app', async ({ page }) => {
  console.log('🔍 Testing Modern App...');
  
  // Navigate to modern app
  await page.goto('http://localhost:5177', { timeout: 30000 });
  console.log('✅ Modern app loaded');
  
  // Wait for the page to fully load
  await page.waitForLoadState('networkidle');
  
  // Take screenshot
  await page.screenshot({ 
    path: './test-results/modern-app-test.png', 
    fullPage: true 
  });
  
  // Look for any start position related elements
  console.log('🔍 Looking for start position elements...');
  
  // Check for various possible selectors
  const selectors = [
    '.start-pos-picker',
    '.start-position-picker', 
    '[data-component="start-position-picker"]',
    '.pictograph-container',
    '.pictograph-wrapper',
    '.modern-pictograph',
    'svg',
    '[data-prop-color]',
    '.prop',
    'circle',
    '[data-color]'
  ];
  
  for (const selector of selectors) {
    const count = await page.locator(selector).count();
    if (count > 0) {
      console.log(`✅ Found ${count} elements with selector: ${selector}`);
    }
  }
  
  // Get all SVG elements and their content
  const svgInfo = await page.evaluate(() => {
    const svgs = document.querySelectorAll('svg');
    const results = [];
    
    svgs.forEach((svg, index) => {
      const rect = svg.getBoundingClientRect();
      const children = Array.from(svg.children).map(child => ({
        tagName: child.tagName,
        attributes: Array.from(child.attributes).reduce((acc, attr) => {
          acc[attr.name] = attr.value;
          return acc;
        }, {}),
        hasChildren: child.children.length > 0
      }));
      
      results.push({
        index,
        width: rect.width,
        height: rect.height,
        viewBox: svg.getAttribute('viewBox'),
        childCount: svg.children.length,
        children: children.slice(0, 5) // First 5 children only
      });
    });
    
    return results;
  });
  
  console.log(`📊 Found ${svgInfo.length} SVG elements:`);
  svgInfo.forEach((svg, index) => {
    console.log(`   SVG ${index}: ${svg.width}x${svg.height}, viewBox: ${svg.viewBox}, children: ${svg.childCount}`);
    svg.children.forEach(child => {
      console.log(`     - ${child.tagName}: ${JSON.stringify(child.attributes)}`);
    });
  });
  
  // Look for any elements with positioning data
  const positionedElements = await page.evaluate(() => {
    const elements = document.querySelectorAll('*');
    const results = [];
    
    elements.forEach((el) => {
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      
      // Look for elements with transforms or specific positioning
      if (style.transform !== 'none' || 
          el.hasAttribute('transform') ||
          el.hasAttribute('x') ||
          el.hasAttribute('y') ||
          el.hasAttribute('cx') ||
          el.hasAttribute('cy') ||
          el.getAttribute('data-prop-color') ||
          el.getAttribute('data-color')) {
        
        results.push({
          tagName: el.tagName,
          className: el.className,
          id: el.id,
          x: el.getAttribute('x'),
          y: el.getAttribute('y'),
          cx: el.getAttribute('cx'),
          cy: el.getAttribute('cy'),
          transform: el.getAttribute('transform'),
          cssTransform: style.transform,
          color: el.getAttribute('data-prop-color') || el.getAttribute('data-color'),
          rectX: Math.round(rect.x),
          rectY: Math.round(rect.y),
          rectWidth: Math.round(rect.width),
          rectHeight: Math.round(rect.height)
        });
      }
    });
    
    return results.slice(0, 20); // Limit to first 20 results
  });
  
  console.log(`📍 Found ${positionedElements.length} positioned elements:`);
  positionedElements.forEach((el, index) => {
    console.log(`   ${index}: ${el.tagName} ${el.className} - Color: ${el.color}, Pos: (${el.rectX}, ${el.rectY})`);
    if (el.transform) console.log(`     Transform: ${el.transform}`);
    if (el.cssTransform !== 'none') console.log(`     CSS Transform: ${el.cssTransform}`);
  });
  
  // Basic assertion
  expect(svgInfo.length).toBeGreaterThan(0);
  
  console.log('✅ Modern app test completed');
});
