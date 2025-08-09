# TKA Modern Web App - Start Position to Option Picker Testing Protocol

This testing protocol ensures that the modern web app correctly loads real options from CSV data when a start position is selected, matching the legacy behavior.

## 🎯 Testing Objectives

1. **Verify Event Flow**: Start position selection triggers option loading
2. **Validate Real Data**: Confirm options come from actual CSV files, not placeholders
3. **Check Data Integrity**: Ensure proper pictograph data structure creation
4. **Verify Continuity**: Confirm position continuity (start position end → option start)
5. **Test UI Responsiveness**: Ensure smooth loading states and error handling

## 📋 Test Cases

### Test Case 1: Basic Start Position to Option Flow

**Purpose**: Verify the core workflow from start position selection to option loading.

**Prerequisites**:

- Modern web app running (`npm run dev`)
- CSV files present in `/static/` directory
- Browser developer tools open to console

**Steps**:

1. Navigate to the Construct tab
2. Open browser console to monitor logs
3. Click on the first start position (Alpha)
4. Observe console output and option picker behavior
5. Verify options load in the option picker

**Expected Results**:

- ✅ Console shows: "📍 Found start position in localStorage"
- ✅ Console shows: "🎯 Loading options for end position: [position]"
- ✅ Console shows: "✅ Loaded X real options from CSV data"
- ✅ Option picker displays actual options (not placeholder text)
- ✅ Options show proper letters and motion types
- ✅ No errors in console

**Debugging Commands**:

```javascript
// Check if start position was saved
console.log('Start Position:', localStorage.getItem('start_position'));

// Check CSV data loading
console.log('CSV Service Ready:', window.csvDataService?.isReady());
```

### Test Case 2: CSV Data Validation

**Purpose**: Verify that real CSV data is loaded and processed correctly.

**Steps**:

1. Open browser console
2. Execute validation commands (see below)
3. Verify CSV statistics
4. Check sample data structure

**Validation Commands**:

```javascript
// Check if CSV files are accessible
fetch('/DiamondPictographDataframe.csv')
	.then((r) => r.text())
	.then((data) => console.log('CSV Preview:', data.split('\n').slice(0, 5)))
	.catch((e) => console.error('CSV Load Error:', e));

// Check parsed data (after loading)
// Open console and run after selecting a start position:
console.log('Parsed CSV Data Available:', window.optionDataService?.csvDataService?.getDataStats());
```

**Expected Results**:

- ✅ CSV files return valid text data
- ✅ Data shows proper headers: `letter,startPos,endPos,timing,direction,blueMotionType...`
- ✅ Multiple rows of actual data (not placeholders)
- ✅ Statistics show reasonable numbers (e.g., ~500+ entries for diamond)

### Test Case 3: Pictograph Data Structure Validation

**Purpose**: Ensure proper domain object creation from CSV data.

**Steps**:

1. Select a start position
2. Wait for options to load
3. Open console and inspect the first option
4. Validate data structure

**Validation Commands**:

```javascript
// After options load, inspect the first option
const firstOption = document.querySelector('.option-container');
if (firstOption) {
	console.log('First Option Element:', firstOption);

	// Check if option has proper data structure
	// This requires accessing the component's state - might need component debugging
}

// Check localStorage for start position structure
const startPos = JSON.parse(localStorage.getItem('start_position') || '{}');
console.log('Start Position Structure:', {
	hasEndPos: !!startPos.endPos,
	hasPictographData: !!startPos.pictograph_data,
	hasMotions: !!startPos.pictograph_data?.motions,
	blueMotion: startPos.pictograph_data?.motions?.blue,
	redMotion: startPos.pictograph_data?.motions?.red,
});
```

**Expected Results**:

- ✅ Start position has proper structure with `endPos` field
- ✅ Options have valid `id`, `letter`, `motions` properties
- ✅ Motions contain `motionType`, `startLocation`, `endLocation`
- ✅ No `undefined` or `null` values in critical fields

### Test Case 4: Position Continuity Validation

**Purpose**: Verify that options' start positions match the selected start position's end position.

**Steps**:

1. Select Alpha start position (should end at specific position)
2. Check that loaded options start from that position
3. Verify this works for Beta and Gamma start positions too

**Validation Commands**:

```javascript
// Check continuity after selecting start position
const startPos = JSON.parse(localStorage.getItem('start_position') || '{}');
const endPosition = startPos.endPos;
console.log('Selected Start Position Ends At:', endPosition);

// After options load, verify they start from this position
// This requires component inspection - should be logged in console automatically
// Look for: "🎯 Loading options for end position: [position]"
```

**Expected Results**:

- ✅ Alpha start position ends at `alpha1` (or appropriate position)
- ✅ All loaded options start from `alpha1`
- ✅ Similar pattern for Beta and Gamma positions
- ✅ Console logs confirm: "Loading options for end position: alpha1"

### Test Case 5: Error Handling and Edge Cases

**Purpose**: Test robustness of the system under various conditions.

**Test 5a: Missing CSV Files**

1. Temporarily rename a CSV file (to simulate missing file)
2. Refresh page and try to select start position
3. Verify graceful error handling

**Test 5b: Corrupted localStorage**

1. Set invalid start position data: `localStorage.setItem('start_position', 'invalid')`
2. Try to select a start position
3. Verify error recovery

**Test 5c: Network Issues**

1. Open Network tab in dev tools
2. Block CSV file requests
3. Verify error messages appear

**Expected Results**:

- ✅ Clear error messages in UI
- ✅ No browser crashes
- ✅ Console logs helpful debugging info
- ✅ System recovers when issues are resolved

## 🔧 Debugging Tools and Commands

### Console Inspection Commands

```javascript
// Check service initialization
console.log('Services Status:', {
	optionService: !!window.optionDataService,
	csvService: !!window.csvDataService,
	initialized: window.csvDataService?.isReady(),
});

// Check CSV data statistics
window.csvDataService?.getDataStats();

// Check available start/end positions
console.log('Available Positions:', {
	startPositions: window.csvDataService?.getAvailableStartPositions('diamond'),
	endPositions: window.csvDataService?.getAvailableEndPositions('diamond'),
});

// Force reload options (for debugging)
// This requires accessing component methods - depends on implementation
```

### Network Tab Verification

1. Open Network tab in DevTools
2. Refresh page
3. Verify these requests succeed:
   - `DiamondPictographDataframe.csv` (Status: 200)
   - `BoxPictographDataframe.csv` (Status: 200)

### Performance Monitoring

```javascript
// Time the CSV loading process
console.time('CSV-Load');
// ... select start position ...
console.timeEnd('CSV-Load');

// Check memory usage
console.log('Memory:', performance.memory);
```

## 📊 Success Criteria

The implementation is considered successful when ALL of the following are true:

### Data Loading ✅

- [ ] CSV files load successfully from `/static/` directory
- [ ] CSV data parses correctly into proper data structures
- [ ] No placeholder or hardcoded data in options
- [ ] Statistics show realistic numbers (hundreds of options)

### Event Flow ✅

- [ ] Clicking start position triggers `'start-position-selected'` event
- [ ] OptionPicker receives and processes the event
- [ ] Options load automatically without manual refresh
- [ ] Loading states display appropriately

### Data Integrity ✅

- [ ] Options contain proper `PictographData` structures
- [ ] Motion data includes correct enums and values
- [ ] Arrow and prop data are properly created
- [ ] Letters match CSV data (A, B, C, etc.)

### Continuity ✅

- [ ] Start position `endPos` matches option `startPos`
- [ ] Position flow makes logical sense
- [ ] No broken continuity chains

### UI/UX ✅

- [ ] Smooth loading animations
- [ ] Clear error messages when issues occur
- [ ] Options display properly in grid layout
- [ ] Clicking options works correctly

### Error Handling ✅

- [ ] Graceful handling of missing CSV files
- [ ] Recovery from corrupted localStorage
- [ ] Clear error messages for users
- [ ] No console errors during normal operation

## 🚨 Common Issues and Solutions

### Issue: "CSV data not initialized"

**Solution**: Check if CSV files are in `/static/` directory and accessible

### Issue: "No options found for end position"

**Solution**: Verify CSV data contains the expected position keys

### Issue: Options show as undefined/null

**Solution**: Check CSV parsing logic and data structure creation

### Issue: Event listener not working

**Solution**: Verify `document.addEventListener('start-position-selected', ...)` is set up

### Issue: Options don't load after start position selection

**Solution**: Check console for errors in `loadOptionsFromStartPosition()` function

## 📝 Test Report Template

```markdown
# Test Execution Report - [Date]

## Test Environment

- Browser: [Chrome/Firefox/Safari] [Version]
- TKA Version: Modern Web App
- CSV Files: Present/Missing

## Test Results

- [ ] Test Case 1: Basic Flow - PASS/FAIL
- [ ] Test Case 2: CSV Validation - PASS/FAIL
- [ ] Test Case 3: Data Structure - PASS/FAIL
- [ ] Test Case 4: Position Continuity - PASS/FAIL
- [ ] Test Case 5: Error Handling - PASS/FAIL

## Issues Found

1. [Issue description]
   - Expected: [expected behavior]
   - Actual: [actual behavior]
   - Console Output: [relevant logs]

## Performance Notes

- CSV Load Time: [X]ms
- Option Load Time: [X]ms
- Memory Usage: [X]MB

## Overall Assessment

- Status: PASS/FAIL
- Ready for Production: YES/NO
- Notes: [additional comments]
```

This comprehensive testing protocol ensures that the modern web app correctly implements the start position to option picker flow with real CSV data, matching the legacy system's functionality.
