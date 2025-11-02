# Dead Code Analysis Tools

This directory contains automated tools to identify and analyze unused code in the TKA Studio codebase.

## Quick Start

### Run Full Analysis
```bash
npm run analyze:dead-code
```

This will:
1. Run `ts-prune` to find all unused exports
2. Categorize results by module
3. Verify which files are truly unused
4. Generate comprehensive reports

### Quick Check
```bash
npm run analyze:dead-code:quick
```

Shows just a count of unused exports in modules (faster).

---

## Generated Reports

After running the analysis, you'll get these files:

### 1. `DEAD-CODE-ANALYSIS-SUMMARY.md` ⭐
**Start here!** Human-readable summary with:
- Executive summary of findings
- Module-by-module breakdown
- Verified dead files ready for archiving
- Action plan with phases
- Recommendations

### 2. `ts-prune-full-report.txt`
Raw output from ts-prune showing every unused export with file:line numbers.

### 3. `dead-code-analysis.json`
Machine-readable JSON with:
- Summary statistics
- Module breakdowns
- Top offending files
- Export lists

### 4. `usage-verification.json`
Results from cross-checking "unused" exports with actual imports in the codebase.

### 5. `file-age-analysis.json`
Git history analysis showing when files were last modified.

---

## Analysis Scripts

### `analyze-dead-code.js`
Main analysis script that processes ts-prune output and categorizes results.

**What it does:**
- Parses ts-prune output
- Groups by module and shared category
- Identifies top offending files
- Generates detailed breakdowns

**Usage:**
```bash
node analyze-dead-code.js
```

### `verify-usage.js`
Verifies if supposedly "unused" files are truly dead by searching for imports.

**What it does:**
- Searches for import statements across codebase
- Checks for dynamic imports
- Identifies barrel export re-exports
- Confirms zero-usage files

**Usage:**
```bash
node verify-usage.js
```

### `analyze-file-age.js`
Cross-references dead code with git history to find old unused files.

**What it does:**
- Gets last modification date from git
- Counts total commits per file
- Identifies files not touched in months
- Sorts by age (oldest first)

**Usage:**
```bash
node analyze-file-age.js
```

---

## Understanding the Results

### What to Archive

✅ **Safe to archive immediately:**
- Files marked "LIKELY DEAD" in verification report
- Files with 0 import references across codebase
- Barrel `index.ts` files that are unused

🔍 **Review before archiving:**
- Service contracts and interfaces
- Domain models and types
- State management exports
- Anything with "POSSIBLY USED" verdict

❌ **Do NOT archive:**
- SvelteKit routes (`+page.ts`, `+layout.ts`, `+server.ts`)
- Test helpers (may be used by future tests)
- Generated files (`.svelte-kit/`)
- Config files
- Exports marked "(used in module)"

### Common Patterns

**Pattern 1: Unused Barrel Exports**
```typescript
// src/lib/modules/foo/index.ts - UNUSED
export { ComponentA } from './ComponentA.svelte';
```
Direct imports are used instead:
```typescript
import ComponentA from '$lib/modules/foo/ComponentA.svelte';
```

**Pattern 2: Over-Engineered Service Contracts**
```typescript
// Unused interface from old architecture
export interface IUnusedService { }
```

**Pattern 3: Dead Features**
Entire feature modules that were prototyped but never completed.

---

## Workflow

### Initial Analysis (First Time)
1. Run `npm run analyze:dead-code`
2. Read `DEAD-CODE-ANALYSIS-SUMMARY.md`
3. Review the "Verified Dead Files" section
4. Start with Phase 1 (Quick Wins)

### Phase 1: Quick Wins
Archive the 9 verified dead barrel files:
```bash
# Example
git mv src/lib/modules/about/components/index.ts archive/dead-code-2025-11/
```

### Phase 2-4: Deeper Cleanup
Review each module section in the summary and make architectural decisions.

### Regular Maintenance
Run analysis quarterly:
```bash
npm run analyze:dead-code
```

Compare results to track improvement.

---

## Adding to CI/CD

### Prevent Dead Code Accumulation

Add to your CI pipeline:

```yaml
# .github/workflows/quality.yml
- name: Check for dead code
  run: |
    UNUSED_COUNT=$(npm run analyze:dead-code:quick)
    if [ $UNUSED_COUNT -gt 1000 ]; then
      echo "Warning: High unused export count ($UNUSED_COUNT)"
      exit 1
    fi
```

Or as a weekly report:
```yaml
# .github/workflows/weekly-analysis.yml
on:
  schedule:
    - cron: '0 9 * * 1' # Every Monday at 9am

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run analyze:dead-code
      - uses: actions/upload-artifact@v3
        with:
          name: dead-code-report
          path: DEAD-CODE-ANALYSIS-SUMMARY.md
```

---

## Troubleshooting

### ts-prune is slow
ts-prune analyzes your entire TypeScript project. For large codebases:
- Use `analyze:dead-code:quick` for faster checks
- Run full analysis less frequently (monthly vs. weekly)

### False positives
Some exports may be flagged as unused but are actually needed:
- Framework exports (SvelteKit routes)
- Runtime/reflection usage (dependency injection)
- Dynamic imports with string templates

Always verify with `verify-usage.js` before archiving.

### Barrel exports showing as unused
This is expected! If your code imports directly from source files, barrel `index.ts` files will be unused. This is actually good - barrel exports can slow down builds.

**Options:**
1. Delete unused barrels (recommended)
2. Enforce barrel imports via ESLint (more work)

---

## Future Improvements

Potential enhancements to these tools:

1. **Bundle size analysis**
   - Cross-reference with bundle analyzer
   - Identify dead code that's bloating bundles

2. **Dependency graph**
   - Visualize which modules depend on each other
   - Find isolated "islands" of dead code

3. **Automated archiving**
   - Script to safely move verified dead files
   - Create archive with metadata

4. **Regression detection**
   - Track dead code over time
   - Alert when dead code increases

---

## Questions?

Check the main summary document: `DEAD-CODE-ANALYSIS-SUMMARY.md`

The summary includes:
- Detailed module-by-module analysis
- Specific files to review
- Architecture questions to answer
- Step-by-step action plan
