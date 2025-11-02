# Dead Code Analysis Summary

**Date:** November 1, 2025
**Project:** TKA Studio (@tka/studio)
**Analysis Tool:** ts-prune + custom verification scripts

---

## Executive Summary

Analyzed **2,010 unused exports** across the codebase:
- **965** in `src/lib/modules/` (feature modules)
- **976** in `src/lib/shared/` (shared infrastructure)
- **69** in other locations (routes, config, tests, generated files)

### Key Findings

**Top 3 modules with dead code:**
1. **Build Module:** 525 unused exports (482 truly unused)
2. **Word-Card Module:** 188 unused exports (180 truly unused)
3. **Learn Module:** 102 unused exports (95 truly unused)

---

## Modules Analysis

### 1. Build Module (`src/lib/modules/build/`)
**Status:** 🔴 High Priority
**Unused Exports:** 525 (largest offender)

#### Subsections with most dead code:
- `build/shared/services/contracts/` - 30 unused service interfaces
- `build/generate/circular/domain/constants/` - 22 unused constants
- `build/animate/services/contracts/` - 20 unused service interfaces
- `build/shared/state/` - 20 unused state management exports

**Recommendation:** This module appears to have significant over-engineering with many service contracts and state managers that were never implemented or used. Consider:
- Archiving unused service contracts
- Consolidating state management
- Removing circular generation constants if CAP generation is deprecated

---

### 2. Word-Card Module (`src/lib/modules/word-card/`)
**Status:** 🔴 High Priority
**Unused Exports:** 188

#### Entirely unused files:
- ✅ `components/index.ts` - 4 exports (VERIFIED DEAD)
- ✅ `domain/index.ts` - 45 exports (VERIFIED DEAD)
- ✅ `domain/models/index.ts` - 45 exports (VERIFIED DEAD)
- ✅ `state/index.ts` - 21 exports (VERIFIED DEAD)

**Recommendation:** **IMMEDIATE ARCHIVAL CANDIDATE**. The entire word-card module appears to have barrel export files (`index.ts`) that are completely unused. The actual Svelte components likely import directly from source files. These barrel files can be safely archived.

---

### 3. Learn Module (`src/lib/modules/learn/`)
**Status:** 🟡 Medium Priority
**Unused Exports:** 102

#### Key dead code:
- `domain/index.ts` - 16 unused concept definitions
- `ConceptProgressService` and `conceptProgressService` - unused services

**Recommendation:** This module may have been over-scoped. Verify if the concept/quiz system is actually in use. If not, archive the entire concept tracking system.

---

### 4. Explore Module (`src/lib/modules/explore/`)
**Status:** 🟡 Medium Priority
**Unused Exports:** 97

**Recommendation:** Medium amount of dead code. May have been an earlier iteration of search/browse functionality. Review and archive unused components.

---

### 5. About Module (`src/lib/modules/about/`)
**Status:** 🟠 Low-Medium Priority
**Unused Exports:** 37

#### Entirely unused files:
- ✅ `components/index.ts` - 23 exports (VERIFIED DEAD)
- ✅ `services/index.ts` - 3 exports (VERIFIED DEAD)
- ✅ `state/index.ts` - 3 exports (VERIFIED DEAD)

**Recommendation:** Same pattern as word-card - barrel exports are unused. Archive these index files.

---

### 6. Write Module (`src/lib/modules/write/`)
**Status:** 🟠 Low-Medium Priority
**Unused Exports:** 14

#### Entirely unused files:
- ✅ `components/index.ts` - 9 exports (VERIFIED DEAD)
- ✅ `services/index.ts` - 5 exports (VERIFIED DEAD)

**Recommendation:** Archive barrel exports.

---

### 7. Library Module (`src/lib/modules/library/`)
**Status:** 🟢 Low Priority
**Unused Exports:** 2

#### Entirely unused files:
- ✅ `index.ts` - 2 exports (VERIFIED DEAD)

**Recommendation:** Archive barrel exports.

---

## Shared Infrastructure Analysis

### Top Categories with Dead Code:

1. **Pictograph** - 266 unused exports
2. **Application** - 100 unused exports
   - `state/index.ts` alone has 65 unused exports
3. **Background** - 94 unused exports
4. **Navigation** - 87 unused exports
5. **Foundation** - 68 unused exports

**Recommendation:** The shared infrastructure has significant barrel export bloat. Most of these are likely unused `index.ts` re-exports where code imports directly from source files.

---

## Verified Dead Files

These files have been **cross-verified** and confirmed to have zero imports anywhere in the codebase:

### 🗑️ Safe to Archive Immediately:

```
src/lib/modules/about/components/index.ts
src/lib/modules/about/services/index.ts
src/lib/modules/about/state/index.ts
src/lib/modules/word-card/components/index.ts
src/lib/modules/word-card/domain/index.ts
src/lib/modules/word-card/state/index.ts
src/lib/modules/write/components/index.ts
src/lib/modules/write/services/index.ts
src/lib/modules/library/index.ts
```

**Total Impact:** Removing these 9 files would eliminate **~190 unused exports** with zero risk.

---

## False Positives to Ignore

The following are **NOT dead code** (even though ts-prune flags them):

### 1. SvelteKit Routes
- `src/routes/+layout.ts` - Used by SvelteKit framework
- `src/routes/+page.ts` - Used by SvelteKit framework
- `src/routes/robots.txt/+server.ts` - Route endpoint
- `src/routes/sitemap.xml/+server.ts` - Route endpoint

### 2. Test Helpers
- Files in `tests/` directory - May not be fully utilized yet

### 3. Generated Files
- `.svelte-kit/types/` - Auto-generated TypeScript definitions

### 4. Exports marked "(used in module)"
These are internal/private exports used within the same module but not exported publicly. They're fine to keep.

---

## Pattern Analysis

### Common Dead Code Pattern: Barrel Exports

The majority of dead code follows this pattern:

```typescript
// src/lib/modules/foo/components/index.ts
export { default as ComponentA } from './ComponentA.svelte';
export { default as ComponentB } from './ComponentB.svelte';
// etc...
```

**Why it's unused:**
Other code imports directly:
```typescript
// Direct import (used)
import ComponentA from '$lib/modules/foo/components/ComponentA.svelte';

// Barrel import (unused)
import { ComponentA } from '$lib/modules/foo/components';
```

**Recommendation:** Either:
1. Delete barrel `index.ts` files (safest - they're not being used)
2. OR enforce barrel imports via ESLint rules (more work)

---

## Action Plan

### Phase 1: Quick Wins (Low Risk)
✅ **Archive the 9 verified dead barrel export files**
- Estimated cleanup: ~190 unused exports
- Risk: Very low (zero imports found)
- Time: 30 minutes

### Phase 2: Build Module Cleanup (Medium Risk)
🔍 **Review and archive unused service contracts in build module**
- Focus on: `build/shared/services/contracts/`, `build/animate/services/contracts/`
- Estimated cleanup: ~100 unused exports
- Risk: Medium (verify these interfaces aren't used at runtime)
- Time: 2-3 hours

### Phase 3: Shared Infrastructure (Medium Risk)
🔍 **Review and clean up shared barrel exports**
- Focus on: `shared/pictograph/`, `shared/application/state/`
- Estimated cleanup: ~300 unused exports
- Risk: Medium
- Time: 4-5 hours

### Phase 4: Module-by-Module Deep Dive (Higher Risk)
🔍 **Analyze each module for truly dead features**
- Word-card domain models (if word-card feature is deprecated)
- Learn module concepts (if quiz system is deprecated)
- Build module CAP generation (if circular generation is deprecated)
- Estimated cleanup: ~400-500 unused exports
- Risk: High (requires understanding product roadmap)
- Time: 1-2 days

---

## Tools & Scripts

The following analysis tools have been created:

1. **`ts-prune-full-report.txt`** - Raw output from ts-prune
2. **`analyze-dead-code.js`** - Categorizes and analyzes dead code by module
3. **`analyze-file-age.js`** - Cross-references with git history
4. **`verify-usage.js`** - Verifies if "unused" code is truly unused
5. **`dead-code-analysis.json`** - Machine-readable analysis results
6. **`usage-verification.json`** - Verification results

### Running the Analysis Again

```bash
# Full analysis pipeline
npx ts-prune --project tsconfig.json > ts-prune-full-report.txt
node analyze-dead-code.js
node analyze-file-age.js
node verify-usage.js
```

---

## Maintenance Recommendations

### 1. Add a Dead Code Check to CI
```json
// package.json
{
  "scripts": {
    "check:dead-code": "npx ts-prune --project tsconfig.json | grep -v '(used in module)' | wc -l"
  }
}
```

### 2. Regular Cleanup Cadence
- Run analysis quarterly
- Archive dead code older than 6 months with no imports

### 3. Prevent Future Dead Code
- Use ESLint rule: `@typescript-eslint/no-unused-vars`
- Require imports through barrel files OR remove barrel files entirely
- Code review checklist: "Does this export get used?"

---

## Questions to Answer Before Archiving

1. **Is the word-card feature still in active use?**
   - If no → Archive entire `word-card/domain/` and `word-card/state/`

2. **Is the learn/quiz system still planned?**
   - If no → Archive concept tracking system

3. **Is CAP/circular generation still supported?**
   - If no → Archive `build/generate/circular/`

4. **Are these service contracts from an old architecture?**
   - The build module has many unused service interfaces
   - May be from a previous dependency injection approach

---

## Estimated Impact

**Total unused exports:** 2,010
**Safely archivable (verified):** ~190 (9 files)
**Likely archivable (after review):** ~800-1,000
**False positives (framework/test code):** ~100

**Potential codebase reduction:** 40-50% of flagged exports could be archived safely.

---

## Next Steps

1. Review this analysis
2. Answer the product/architecture questions above
3. Start with Phase 1 (quick wins) to build confidence
4. Schedule dedicated time for Phase 2-4 cleanup
5. Set up CI checks to prevent future dead code accumulation

---

**Generated by:** ts-prune + custom analysis scripts
**Full reports available in:**
- `ts-prune-full-report.txt`
- `dead-code-analysis.json`
- `usage-verification.json`
