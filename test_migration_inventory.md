# Test Migration Inventory

## Current Test Locations Discovery

### Root Level Tests (`f:\CODE\TKA\tests\`)

- ✅ **Already exists** - Some infrastructure in place
- ✅ **Has conftest.py** - Basic configuration exists
- ✅ **desktop/** subdirectory exists with substantial structure
- ✅ **integration/** subdirectory exists
- ✅ **shared/** subdirectory exists

#### Current Structure in tests/:

```
tests/
├── conftest.py                     # ✅ Exists
├── desktop/                        # ✅ Exists - Large structure
│   ├── conftest.py                 # ✅ Exists
│   ├── unit/                       # ✅ Exists
│   ├── integration/                # ✅ Exists
│   ├── specification/              # ✅ Exists
│   └── [many other subdirs]
├── integration/                    # ✅ Exists
├── shared/                         # ✅ Exists
└── [various test files]
```

### Modern Desktop Tests (`f:\CODE\TKA\src\desktop\modern\tests\`)

- ⚠️ **DUPLICATE STRUCTURE** - Very similar to tests/desktop/
- ⚠️ **Need to merge/consolidate** with existing tests/desktop/

#### Structure in src/desktop/modern/tests/:

```
src/desktop/modern/tests/
├── unit/                           # ⚠️ Similar to tests/desktop/unit/
├── integration/                    # ⚠️ Similar to tests/desktop/integration/
├── specification/                  # ⚠️ Similar to tests/desktop/specification/
├── pytest.ini                     # ⚠️ Separate config - needs merging
├── conftest.py                     # ⚠️ May have unique fixtures
└── [various test files]           # ⚠️ May be duplicates
```

### Launcher Tests (`f:\CODE\TKA\launcher\tests\` and scattered)

- ⚠️ **SCATTERED ORGANIZATION** - Some in tests/ subdir, some in root
- ✅ **SMALL SCOPE** - Only 4-5 test files to move

#### Launcher Test Files:

```
launcher/
├── tests/
│   ├── test_base_clean.py
│   ├── test_integration.py
│   ├── test_base.py
│   └── test_modern_search_box.py
├── test_card_visibility.py        # ⚠️ In launcher root
├── test_design_system.py          # ⚠️ In launcher root
├── test_fluent_widgets.py         # ⚠️ In launcher root
├── test_hover_functionality.py    # ⚠️ In launcher root
├── test_launch.py                 # ⚠️ In launcher root
└── test_reliable_styling.py       # ⚠️ In launcher root
```

### Legacy Desktop Tests (`f:\CODE\TKA\src\desktop\legacy\`)

- ⚠️ **SCATTERED** - Tests embedded within source directories
- ⚠️ **LEGACY NAMING** - Some files use "test" in middle of name

### Root Level Scattered Tests

- ⚠️ **CLEANUP NEEDED** - Several test files in project root
- Files: `test_pylint_fix.py`, `test_imports_enhanced.py`, `test_imports.py`

## Analysis and Decisions

### Key Findings:

1. **tests/desktop/** already has substantial infrastructure
2. **src/desktop/modern/tests/** appears to be a duplicate/parallel structure
3. **Need to compare and merge** the two desktop test directories
4. **Launcher tests** need simple relocation
5. **Legacy tests** need extraction from source directories

### Migration Strategy:

1. **Merge modern tests** into existing tests/desktop/modern/
2. **Relocate launcher tests** to tests/desktop/launcher/
3. **Extract legacy tests** to tests/desktop/legacy/
4. **Consolidate configurations** (pytest.ini, conftest.py)
5. **Clean up root-level test files**

### Next Steps:

1. Compare tests/desktop/ vs src/desktop/modern/tests/ for duplicates
2. Create missing directory structure
3. Move and update import paths
4. Consolidate configurations
5. Validate all tests work

## Risk Assessment:

- 🟡 **MEDIUM RISK** - Substantial existing structure means less chance of breaking everything
- 🟢 **LOW RISK** - Many tests already in target location
- 🟡 **MEDIUM COMPLEXITY** - Need to merge two similar structures carefully
