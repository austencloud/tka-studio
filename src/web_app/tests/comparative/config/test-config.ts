/**
 * Test Configuration for Start Position Picker Comparison
 * 
 * Centralized configuration for comparative testing between legacy and modern
 * start position picker implementations.
 */

export interface TestConfig {
  tolerance: {
    coordinates: number; // pixels
    rotation: number; // degrees
    transform: number; // general tolerance for transform comparisons
  };
  urls: {
    legacy: string;
    modern: string;
  };
  timeouts: {
    navigation: number;
    componentLoad: number;
    dataExtraction: number;
  };
  gridModes: readonly ('diamond' | 'box')[];
  startPositions: {
    diamond: readonly string[];
    box: readonly string[];
  };
  selectors: {
    legacy: LegacySelectors;
    modern: ModernSelectors;
  };
  reporting: {
    generateScreenshots: boolean;
    detailedLogging: boolean;
    saveRawData: boolean;
    outputDirectory: string;
  };
}

export interface LegacySelectors {
  constructTab: string;
  gridModeSelector: string;
  startPositionPicker: string;
  positionContainer: (positionKey: string) => string;
  propElement: string;
  letterElement: string;
  pictographSvg: string;
}

export interface ModernSelectors {
  constructTab: string;
  gridModeSelector: string;
  startPositionPicker: string;
  positionContainer: (positionKey: string) => string;
  propElement: string;
  letterElement: string;
  pictographSvg: string;
}

export const DEFAULT_TEST_CONFIG: TestConfig = {
  tolerance: {
    coordinates: 1.0, // 1 pixel tolerance for coordinate differences
    rotation: 0.5, // 0.5 degree tolerance for rotation differences
    transform: 0.1 // 10% tolerance for transform matrix comparisons
  },
  
  urls: {
    legacy: 'http://localhost:5173',
    modern: 'http://localhost:5177'
  },
  
  timeouts: {
    navigation: 30000, // 30 seconds for page navigation
    componentLoad: 15000, // 15 seconds for component loading
    dataExtraction: 10000 // 10 seconds for data extraction
  },
  
  gridModes: ['diamond', 'box'] as const,
  
  startPositions: {
    diamond: ['alpha1_alpha1', 'beta5_beta5', 'gamma11_gamma11'] as const,
    box: ['alpha2_alpha2', 'beta4_beta4', 'gamma12_gamma12'] as const
  },
  
  selectors: {
    legacy: {
      constructTab: '[data-testid="construct-tab"], .construct-tab, .tab-construct',
      gridModeSelector: '[data-testid="grid-mode-selector"], select[name="gridMode"], .grid-mode-selector',
      startPositionPicker: '.start-pos-picker, [data-component="start-position-picker"]',
      positionContainer: (positionKey: string) => 
        `[data-position-key="${positionKey}"], .pictograph-container[data-letter="${getLetterFromPositionKey(positionKey)}"]`,
      propElement: '.prop-element, [data-prop-color], .prop, svg circle[data-color], svg g[data-component="prop"]',
      letterElement: '.tka-letter, [data-letter], .position-label, svg text',
      pictographSvg: 'svg.pictograph, .pictograph svg, svg'
    },
    
    modern: {
      constructTab: '[data-testid="construct-tab"], .construct-tab, .tab-construct',
      gridModeSelector: '[data-testid="grid-mode-selector"], select[name="gridMode"], .grid-mode-selector',
      startPositionPicker: '.start-pos-picker, [data-component="start-position-picker"]',
      positionContainer: (positionKey: string) => 
        `[data-position-key="${positionKey}"], .pictograph-container[data-letter="${getLetterFromPositionKey(positionKey)}"]`,
      propElement: 'svg g[data-component="prop"], svg circle[data-prop-color], svg g.prop, [data-prop-color]',
      letterElement: 'svg text, .position-label, [data-letter]',
      pictographSvg: 'svg, .modern-pictograph svg'
    }
  },
  
  reporting: {
    generateScreenshots: true,
    detailedLogging: true,
    saveRawData: true,
    outputDirectory: './test-results/comparative'
  }
};

/**
 * Position key to letter mapping for both grid modes
 */
export const POSITION_KEY_TO_LETTER: Record<string, string> = {
  // Diamond mode positions
  'alpha1_alpha1': 'A',
  'beta5_beta5': 'E', 
  'gamma11_gamma11': 'K',
  
  // Box mode positions
  'alpha2_alpha2': 'B',
  'beta4_beta4': 'D',
  'gamma12_gamma12': 'L'
};

/**
 * Expected prop counts for each position
 */
export const EXPECTED_PROP_COUNTS: Record<string, number> = {
  'alpha1_alpha1': 2, // Blue and red props
  'beta5_beta5': 2,
  'gamma11_gamma11': 2,
  'alpha2_alpha2': 2,
  'beta4_beta4': 2,
  'gamma12_gamma12': 2
};

/**
 * Grid coordinate reference points for validation
 */
export const GRID_REFERENCE_POINTS = {
  diamond: {
    center: { x: 475, y: 475 },
    handPoints: {
      n: { x: 475, y: 331.9 },
      e: { x: 618.1, y: 475 },
      s: { x: 475, y: 618.1 },
      w: { x: 331.9, y: 475 }
    }
  },
  box: {
    center: { x: 475, y: 475 },
    handPoints: {
      n: { x: 475, y: 325 },
      e: { x: 625, y: 475 },
      s: { x: 475, y: 625 },
      w: { x: 325, y: 475 }
    }
  }
} as const;

/**
 * Helper function to get letter from position key
 */
export function getLetterFromPositionKey(positionKey: string): string {
  return POSITION_KEY_TO_LETTER[positionKey] || '';
}

/**
 * Helper function to get expected prop count for a position
 */
export function getExpectedPropCount(positionKey: string): number {
  return EXPECTED_PROP_COUNTS[positionKey] || 0;
}

/**
 * Helper function to validate if a position key is valid for a grid mode
 */
export function isValidPositionForGridMode(positionKey: string, gridMode: 'diamond' | 'box'): boolean {
  return DEFAULT_TEST_CONFIG.startPositions[gridMode].includes(positionKey as any);
}

/**
 * Helper function to get all position keys for a grid mode
 */
export function getPositionKeysForGridMode(gridMode: 'diamond' | 'box'): readonly string[] {
  return DEFAULT_TEST_CONFIG.startPositions[gridMode];
}

/**
 * Test environment configuration
 */
export interface TestEnvironment {
  name: string;
  description: string;
  config: Partial<TestConfig>;
}

export const TEST_ENVIRONMENTS: Record<string, TestEnvironment> = {
  development: {
    name: 'Development',
    description: 'Local development environment with standard ports',
    config: {
      urls: {
        legacy: 'http://localhost:5173',
        modern: 'http://localhost:5177'
      },
      timeouts: {
        navigation: 30000,
        componentLoad: 15000,
        dataExtraction: 10000
      }
    }
  },
  
  ci: {
    name: 'Continuous Integration',
    description: 'CI environment with faster timeouts and no screenshots',
    config: {
      timeouts: {
        navigation: 20000,
        componentLoad: 10000,
        dataExtraction: 5000
      },
      reporting: {
        generateScreenshots: false,
        detailedLogging: false,
        saveRawData: false,
        outputDirectory: './ci-test-results'
      }
    }
  },
  
  production: {
    name: 'Production Validation',
    description: 'Production environment testing with strict tolerances',
    config: {
      tolerance: {
        coordinates: 0.5, // Stricter coordinate tolerance
        rotation: 0.25, // Stricter rotation tolerance
        transform: 0.05 // Stricter transform tolerance
      },
      timeouts: {
        navigation: 45000,
        componentLoad: 20000,
        dataExtraction: 15000
      }
    }
  }
};

/**
 * Get merged configuration for a specific environment
 */
export function getConfigForEnvironment(environmentName: string): TestConfig {
  const environment = TEST_ENVIRONMENTS[environmentName];
  if (!environment) {
    throw new Error(`Unknown test environment: ${environmentName}`);
  }
  
  return {
    ...DEFAULT_TEST_CONFIG,
    ...environment.config,
    tolerance: {
      ...DEFAULT_TEST_CONFIG.tolerance,
      ...environment.config.tolerance
    },
    urls: {
      ...DEFAULT_TEST_CONFIG.urls,
      ...environment.config.urls
    },
    timeouts: {
      ...DEFAULT_TEST_CONFIG.timeouts,
      ...environment.config.timeouts
    },
    reporting: {
      ...DEFAULT_TEST_CONFIG.reporting,
      ...environment.config.reporting
    }
  };
}

/**
 * Validation functions for test configuration
 */
export function validateTestConfig(config: TestConfig): string[] {
  const errors: string[] = [];
  
  if (config.tolerance.coordinates < 0) {
    errors.push('Coordinate tolerance must be non-negative');
  }
  
  if (config.tolerance.rotation < 0) {
    errors.push('Rotation tolerance must be non-negative');
  }
  
  if (config.timeouts.navigation <= 0) {
    errors.push('Navigation timeout must be positive');
  }
  
  if (!config.urls.legacy || !config.urls.modern) {
    errors.push('Both legacy and modern URLs must be specified');
  }
  
  return errors;
}
