# Start Position Picker Comparative Test Suite

This comprehensive test suite validates the start position picker functionality between the legacy and modern web applications by comparing 3-star position pictographs for pixel-perfect positioning and rotation consistency.

## Overview

The test suite performs detailed comparisons of:
- **Individual prop positioning coordinates** (x, y positions)
- **Rotation values** applied to each prop
- **Transformation matrices** and CSS transforms
- **Visual rendering differences**

The legacy web app serves as the reference baseline, ensuring the modern implementation achieves exact coordinate and rotation parity.

## Test Structure

### Core Components

1. **`start-position-picker-comparison.test.ts`** - Main test file with Playwright test definitions
2. **`utils/comparison-utilities.ts`** - Data extraction and comparison utilities
3. **`utils/test-runner.ts`** - Test orchestration and reporting system
4. **`config/test-config.ts`** - Centralized configuration management

### Test Coverage

#### 3-Star Position Tests
- **Diamond Grid Mode**: `alpha1_alpha1`, `beta5_beta5`, `gamma11_gamma11`
- **Box Grid Mode**: `alpha2_alpha2`, `beta4_beta4`, `gamma12_gamma12`

Each position is tested for:
- Coordinate accuracy (±1 pixel tolerance)
- Rotation precision (±0.5 degree tolerance)
- Transform equivalence
- Cross-grid consistency

#### Cross-Grid Mode Consistency
- Validates consistent behavior between diamond and box grid modes
- Ensures similar success rates across grid types
- Identifies systematic differences in positioning logic

## Configuration

### Test Environments

The test suite supports multiple environments:

- **Development** (`development`): Local testing with standard timeouts
- **CI** (`ci`): Faster execution for continuous integration
- **Production** (`production`): Strict tolerances for production validation

### Tolerance Settings

```typescript
tolerance: {
  coordinates: 1.0,  // pixels
  rotation: 0.5,     // degrees
  transform: 0.1     // 10% for transform comparisons
}
```

### URLs Configuration

```typescript
urls: {
  legacy: 'http://localhost:5173',
  modern: 'http://localhost:5177'
}
```

## Running the Tests

### Prerequisites

1. Both legacy and modern web applications must be running:
   ```bash
   # Terminal 1 - Legacy app
   cd src/web_app/legacy_web
   npm run dev

   # Terminal 2 - Modern app
   cd src/web_app/modern_web
   npm run dev
   ```

2. Install test dependencies:
   ```bash
   cd src/web_app
   npm install
   ```

### Execution Commands

```bash
# Run all comparative tests
npx playwright test tests/comparative/

# Run specific position test
npx playwright test tests/comparative/ --grep "alpha1_alpha1"

# Run with UI mode for debugging
npx playwright test tests/comparative/ --ui

# Run with detailed reporting
npx playwright test tests/comparative/ --reporter=html
```

### Environment-Specific Execution

```bash
# Development environment (default)
TEST_ENV=development npx playwright test tests/comparative/

# CI environment
TEST_ENV=ci npx playwright test tests/comparative/

# Production validation
TEST_ENV=production npx playwright test tests/comparative/
```

## Test Output

### Success Criteria

A test passes when:
- Coordinate differences are within tolerance (≤1 pixel)
- Rotation differences are within tolerance (≤0.5 degrees)
- Transform methods are mathematically equivalent
- No systematic positioning errors are detected

### Failure Analysis

When tests fail, detailed reports include:

1. **Coordinate Discrepancies**:
   ```
   BLUE prop:
     Expected: (467, 323.9)
     Actual:   (469, 325.1)
     Diff:     (2.00, 1.20)
     Magnitude: 2.33 pixels
   ```

2. **Rotation Discrepancies**:
   ```
   RED prop:
     Expected: 90.00°
     Actual:   92.50°
     Diff:     2.50°
   ```

3. **Recommendations**:
   - Specific adjustments needed in modern implementation
   - Algorithm corrections required
   - Configuration changes suggested

### Report Generation

The test suite generates multiple report formats:

- **JSON Report**: Machine-readable detailed results
- **HTML Report**: Visual comparison with screenshots
- **Text Report**: Human-readable summary
- **Screenshots**: Visual evidence of differences

Reports are saved to `./test-results/comparative/`

## Data Extraction Process

### Legacy Application
1. Navigate to construct tab
2. Set grid mode (diamond/box)
3. Wait for start position picker to load
4. Extract prop elements and their positioning data
5. Parse transform matrices and coordinate values

### Modern Application
1. Navigate to construct tab
2. Set grid mode (diamond/box)
3. Wait for start position picker to load
4. Extract SVG prop elements and positioning data
5. Parse CSS transforms and coordinate values

### Comparison Algorithm
1. Match props by color (blue/red)
2. Calculate coordinate differences
3. Normalize and compare rotation values
4. Analyze transform equivalence
5. Generate discrepancy reports

## Expected Coordinate Reference

### Diamond Grid Mode
- **alpha1_alpha1 (A)**: Blue (467, 323.9), Red (483, 339.9)
- **beta5_beta5 (E)**: Blue (610.1, 467), Red (626.1, 483)
- **gamma11_gamma11 (K)**: Blue (467, 610.1), Red (483, 626.1)

### Box Grid Mode
- **alpha2_alpha2 (B)**: Blue (467, 317), Red (483, 333)
- **beta4_beta4 (D)**: Blue (617, 467), Red (633, 483)
- **gamma12_gamma12 (L)**: Blue (467, 617), Red (483, 633)

## Troubleshooting

### Common Issues

1. **Browser Context Failures**:
   - Ensure sufficient system resources
   - Check for port conflicts
   - Verify application availability

2. **Selector Mismatches**:
   - Update selectors in `config/test-config.ts`
   - Verify DOM structure changes
   - Check for dynamic loading issues

3. **Coordinate Extraction Failures**:
   - Verify transform parsing logic
   - Check for CSS changes in applications
   - Ensure grid data is loaded

### Debug Mode

Enable detailed logging:
```typescript
reporting: {
  detailedLogging: true,
  generateScreenshots: true,
  saveRawData: true
}
```

## Extending the Test Suite

### Adding New Positions
1. Update `START_POSITION_KEYS` in config
2. Add expected coordinates to test data
3. Update letter mapping if needed

### Adding New Grid Modes
1. Extend `GridMode` type
2. Add grid-specific selectors
3. Update coordinate reference data

### Custom Tolerance Settings
1. Modify tolerance values in config
2. Add position-specific tolerances if needed
3. Update validation logic accordingly

## Integration with CI/CD

The test suite is designed for automated execution:

```yaml
# Example GitHub Actions workflow
- name: Run Comparative Tests
  run: |
    npm run dev:legacy &
    npm run dev:modern &
    sleep 30  # Wait for apps to start
    TEST_ENV=ci npx playwright test tests/comparative/
```

## Maintenance

### Regular Updates
- Review tolerance settings quarterly
- Update expected coordinates when grid changes
- Verify selector accuracy with UI updates
- Monitor test execution performance

### Performance Optimization
- Parallel test execution where possible
- Efficient browser context management
- Optimized data extraction algorithms
- Minimal screenshot generation in CI

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test output logs
3. Examine generated screenshots
4. Consult the detailed JSON reports
