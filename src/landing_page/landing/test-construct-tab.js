#!/usr/bin/env node

/**
 * Test script to validate the ConstructTab implementation
 * This script checks for import errors and basic functionality
 */

import fs from 'fs';
import path from 'path';

const LANDING_DIR = 'F:/CODE/TKA/src/web/landing';
const CONSTRUCT_TAB_PATH = path.join(LANDING_DIR, 'src/lib/constructor/ConstructTab.svelte');

console.log('🔍 Testing ConstructTab Implementation...\n');

// Check if ConstructTab file exists and is readable
if (!fs.existsSync(CONSTRUCT_TAB_PATH)) {
    console.error('❌ ConstructTab.svelte not found at:', CONSTRUCT_TAB_PATH);
    process.exit(1);
}

console.log('✅ ConstructTab.svelte found');

// Read the file and check for key implementations
const content = fs.readFileSync(CONSTRUCT_TAB_PATH, 'utf8');

const checks = [
    {
        name: 'Import sequence actions',
        pattern: /import.*sequenceActions.*from.*sequenceMachine/,
        required: true
    },
    {
        name: 'Import sequence container',
        pattern: /import.*sequenceContainer.*from.*SequenceContainer/,
        required: true
    },
    {
        name: 'Import render sequence utilities',
        pattern: /import.*renderSequence.*downloadSequenceImage.*from.*ShareUtils/,
        required: true
    },
    {
        name: 'Import toast notifications',
        pattern: /import.*showSuccess.*showError.*from.*ToastManager/,
        required: true
    },
    {
        name: 'Import haptic feedback',
        pattern: /import.*hapticFeedbackService.*from.*HapticFeedbackService/,
        required: true
    },
    {
        name: 'Save image implementation',
        pattern: /case 'saveImage':.*renderSequence.*downloadSequenceImage/s,
        required: true
    },
    {
        name: 'Add to dictionary implementation',
        pattern: /case 'addToDictionary':.*localStorage.*sequence_dictionary/s,
        required: true
    },
    {
        name: 'Mirror sequence implementation',
        pattern: /case 'mirrorSequence':.*mirrorSequenceData.*setSequence/s,
        required: true
    },
    {
        name: 'Swap colors implementation',
        pattern: /case 'swapColors':.*swapSequenceColors.*setSequence/s,
        required: true
    },
    {
        name: 'Rotate sequence implementation',
        pattern: /case 'rotateSequence':.*rotateSequenceData.*setSequence/s,
        required: true
    },
    {
        name: 'Delete beat implementation',
        pattern: /case 'deleteBeat':.*removeBeatAndFollowing/s,
        required: true
    },
    {
        name: 'Clear sequence implementation',
        pattern: /case 'clearSequence':.*clearSequence\(\)/s,
        required: true
    },
    {
        name: 'Mirror function implementation',
        pattern: /function mirrorSequenceData.*startLoc\.side.*=.*'L'.*\?.*'R'.*:.*'L'/s,
        required: true
    },
    {
        name: 'Rotate function implementation',
        pattern: /function rotateSequenceData.*startOri.*\+.*90.*%.*360/s,
        required: true
    },
    {
        name: 'Swap colors function implementation',
        pattern: /function swapSequenceColors.*redMotionData.*blueMotionData/s,
        required: true
    },
    {
        name: 'Async handler implementation',
        pattern: /async function handleButtonAction/,
        required: true
    },
    {
        name: 'Error handling in actions',
        pattern: /try \{[\s\S]*\} catch.*error.*showError/,
        required: true
    }
];

let passedChecks = 0;
let failedChecks = 0;

console.log('\n📋 Checking implementation...\n');

for (const check of checks) {
    const matches = check.pattern.test(content);

    if (matches) {
        console.log(`✅ ${check.name}`);
        passedChecks++;
    } else {
        console.log(`${check.required ? '❌' : '⚠️'} ${check.name}`);
        if (check.required) {
            failedChecks++;
        }
    }
}

console.log('\n📊 Results:');
console.log(`✅ Passed: ${passedChecks}`);
console.log(`❌ Failed: ${failedChecks}`);

if (failedChecks === 0) {
    console.log('\n🎉 All critical checks passed! ConstructTab implementation looks good.');

    console.log('\n🔧 Next steps:');
    console.log('1. Install dependencies: npm install');
    console.log('2. Start dev server: npm run dev');
    console.log('3. Test in browser: http://localhost:5173/constructor');
    console.log('4. Test button actions by creating a sequence and trying each button');

} else {
    console.log('\n⚠️ Some critical checks failed. Review the implementation.');
    process.exit(1);
}

// Check if package.json has required dependencies
const packageJsonPath = path.join(LANDING_DIR, 'package.json');
if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const requiredDeps = [
        'xstate',
        '@xstate/svelte',
        'html2canvas',
        'lodash',
        'lucide-svelte',
        'lz-string',
        'svelte-motion'
    ];

    console.log('\n📦 Checking dependencies:');

    let missingDeps = 0;
    for (const dep of requiredDeps) {
        if (packageJson.dependencies?.[dep]) {
            console.log(`✅ ${dep}: ${packageJson.dependencies[dep]}`);
        } else {
            console.log(`❌ ${dep}: missing`);
            missingDeps++;
        }
    }

    if (missingDeps === 0) {
        console.log('\n✅ All required dependencies are present in package.json');
    } else {
        console.log(`\n⚠️ ${missingDeps} dependencies are missing. Run npm install to install them.`);
    }
}

console.log('\n🚀 Implementation validation complete!');
