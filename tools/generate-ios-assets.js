/**
 * Generate iOS-specific PWA assets
 * 
 * Creates:
 * - Apple touch icon (180x180)
 * - Splash screens for all iOS devices
 * 
 * Run: node tools/generate-ios-assets.js
 */

import sharp from 'sharp';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PWA_DIR = join(__dirname, '../static/pwa');

// Ensure PWA directory exists
if (!existsSync(PWA_DIR)) {
  mkdirSync(PWA_DIR, { recursive: true });
}

// iOS splash screen sizes (device-width x device-height x pixel-ratio)
const SPLASH_SCREENS = [
  // iPad Pro 12.9" (2048x2732)
  { width: 2048, height: 2732, name: 'splash-2048x2732.png' },
  // iPad Pro 11" (1668x2388)
  { width: 1668, height: 2388, name: 'splash-1668x2388.png' },
  // iPad 10.2" (1536x2048)
  { width: 1536, height: 2048, name: 'splash-1536x2048.png' },
  // iPhone 15 Pro Max (1290x2796)
  { width: 1290, height: 2796, name: 'splash-1290x2796.png' },
  // iPhone 15 Pro (1179x2556)
  { width: 1179, height: 2556, name: 'splash-1179x2556.png' },
  // iPhone 14 Pro (1125x2436)
  { width: 1125, height: 2436, name: 'splash-1125x2436.png' },
  // iPhone 14 Plus (1242x2688)
  { width: 1242, height: 2688, name: 'splash-1242x2688.png' },
  // iPhone 14 (828x1792)
  { width: 828, height: 1792, name: 'splash-828x1792.png' },
  // iPhone 8 Plus (1242x2208)
  { width: 1242, height: 2208, name: 'splash-1242x2208.png' },
  // iPhone 8 (750x1334)
  { width: 750, height: 1334, name: 'splash-750x1334.png' },
  // iPhone SE (640x1136)
  { width: 640, height: 1136, name: 'splash-640x1136.png' },
];

async function generateAppleTouchIcon() {
  const sourceIcon = join(PWA_DIR, 'icon-512x512.png');
  const outputIcon = join(PWA_DIR, 'icon-180x180.png');

  if (!existsSync(sourceIcon)) {
    console.error('❌ Source icon not found:', sourceIcon);
    console.log('   Please ensure icon-512x512.png exists in static/pwa/');
    return;
  }

  try {
    await sharp(sourceIcon)
      .resize(180, 180, {
        fit: 'contain',
        background: { r: 11, g: 29, b: 42, alpha: 1 } // #0b1d2a
      })
      .png()
      .toFile(outputIcon);
    
    console.log('✅ Generated Apple touch icon:', outputIcon);
  } catch (error) {
    console.error('❌ Failed to generate Apple touch icon:', error.message);
  }
}

async function generateSplashScreen(config) {
  const { width, height, name } = config;
  const outputPath = join(PWA_DIR, name);

  try {
    // Create splash screen with TKA branding
    // Background: #0b1d2a (TKA dark blue)
    // Center: TKA logo/icon
    
    const logoPath = join(PWA_DIR, 'icon-512x512.png');
    
    if (!existsSync(logoPath)) {
      console.error('❌ Logo not found:', logoPath);
      return;
    }

    // Calculate logo size (20% of screen height, max 512px)
    const logoSize = Math.min(Math.floor(height * 0.2), 512);
    
    // Create background
    const background = await sharp({
      create: {
        width,
        height,
        channels: 4,
        background: { r: 11, g: 29, b: 42, alpha: 1 } // #0b1d2a
      }
    }).png();

    // Resize logo
    const logo = await sharp(logoPath)
      .resize(logoSize, logoSize, { fit: 'contain' })
      .toBuffer();

    // Composite logo onto background (centered)
    await background
      .composite([{
        input: logo,
        top: Math.floor((height - logoSize) / 2),
        left: Math.floor((width - logoSize) / 2)
      }])
      .toFile(outputPath);

    console.log(`✅ Generated splash screen: ${name} (${width}x${height})`);
  } catch (error) {
    console.error(`❌ Failed to generate ${name}:`, error.message);
  }
}

async function generateAllAssets() {
  console.log('🎨 Generating iOS PWA assets...\n');

  // Generate Apple touch icon
  await generateAppleTouchIcon();

  // Generate all splash screens
  console.log('\n📱 Generating splash screens...');
  for (const config of SPLASH_SCREENS) {
    await generateSplashScreen(config);
  }

  console.log('\n✨ Done! iOS assets generated in static/pwa/');
  console.log('\n📝 Next steps:');
  console.log('   1. Test on iOS Safari: Add to Home Screen');
  console.log('   2. Verify splash screens appear on launch');
  console.log('   3. Check icon appears correctly on home screen');
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  generateAllAssets().catch(console.error);
}

export { generateAllAssets, generateAppleTouchIcon, generateSplashScreen };

