# TKA Modern Test Organization Guide

## 🎯 Test Lifecycle Philosophy

TKA follows a **lifecycle-based testing approach** where tests are categorized by their purpose and lifespan:

- **SPECIFICATION**: Permanent behavioral contracts (never delete)
- **REGRESSION**: Bug prevention tests (delete only when feature removed)
- **SCAFFOLDING**: Temporary development aids (delete after purpose achieved)

## 📁 Directory Structure

```
tests/
├── unit/                    # Isolated component tests
│   ├── application/         # Service layer tests
│   ├── core/               # DI container, interfaces
│   ├── presentation/       # UI component tests
│   └── services/           # Legacy service tests
├── integration/            # Multi-component tests
│   ├── components/        # Component integration
│   ├── services/          # Service integration
│   └── workflows/         # End-to-end workflows
├── regression/            # Bug prevention tests
│   └── bugs/             # Specific bug regression tests
├── scaffolding/          # Temporary development tests
│   └── debug/            # Debug-specific scaffolding
├── specification/        # Permanent behavioral contracts
│   ├── application/      # Service contracts
│   ├── core/            # Core system contracts
│   ├── domain/          # Domain model contracts
│   ├── presentation/    # UI behavior contracts
│   └── workflows/       # User workflow contracts
├── templates/           # Test templates for each lifecycle
├── fixtures/           # Shared test fixtures
├── scripts/           # Test utilities and runners
└── parallel/         # Legacy/Modern comparison (SCAFFOLDING)
```

## 🔄 Test Lifecycle Decision Tree

### When Creating a New Test:

1. **Is this testing a permanent business rule or contract?**
   - YES → Use `specification/` + `specification_test_template.py`
   - NO → Continue to step 2

2. **Is this preventing a specific bug from reoccurring?**
   - YES → Use `regression/bugs/` + `regression_test_template.py`
   - NO → Continue to step 3

3. **Is this temporary debugging/exploration?**
   - YES → Use `scaffolding/debug/` + `scaffolding_test_template.py`
   - NO → Continue to step 4

4. **Is this testing multiple components together?**
   - YES → Use `integration/` + appropriate template
   - NO → Use `unit/` + appropriate template

## 📋 Template Usage Guide

### Specification Tests (`specification_test_template.py`)

**Use for**: Permanent behavioral contracts that must never change
**Examples**:

- Domain model immutability contracts
- Service interface contracts
- UI behavior contracts (Legacy parity)
- Business rule enforcement

**Metadata Required**:

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce [specific behavioral contract]
PERMANENT: [Why this behavior must always be preserved]
AUTHOR: @username
"""
```

### Regression Tests (`regression_test_template.py`)

**Use for**: Preventing specific bugs from reoccurring
**Examples**:

- Crash prevention tests
- Performance regression tests
- Memory leak prevention
- Integration failure prevention

**Metadata Required**:

```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent [specific bug] from reoccurring
BUG_REPORT: #issue_number or description
FIXED_DATE: YYYY-MM-DD
AUTHOR: @username
"""
```

### Scaffolding Tests (`scaffolding_test_template.py`)

**Use for**: Temporary development aids that should be deleted
**Examples**:

- Bug reproduction and debugging
- Legacy behavior exploration
- Proof of concept testing
- Development spikes

**Metadata Required**:

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: [One-line description of why this exists]
DELETE_AFTER: YYYY-MM-DD (REQUIRED)
CREATED: YYYY-MM-DD
AUTHOR: @username
RELATED_ISSUE: #issue_number (if applicable)
"""
```

## 🚨 Critical Rules

### NEVER DELETE:

- Tests marked `TEST LIFECYCLE: SPECIFICATION`
- Tests marked `TEST LIFECYCLE: REGRESSION`
- Tests that verify user-facing functionality
- Tests that prevent known bugs from returning

### ALWAYS DELETE:

- Scaffolding tests past their DELETE_AFTER date
- Tests that always pass or always fail
- Tests that duplicate existing coverage
- Tests with no clear purpose

### REVIEW REGULARLY:

- Scaffolding tests approaching DELETE_AFTER date
- Tests that haven't been updated in >30 days
- Tests that test implementation details vs contracts

## 🎯 Best Practices

### For AI Agents:

1. **Always check lifecycle metadata** before suggesting changes
2. **Suggest deletion** for expired scaffolding tests
3. **Warn about missing metadata** in scaffolding tests
4. **Recommend migration** to specification/ when behavior becomes permanent
5. **Focus on contracts** not implementation details in specification tests

### For Developers:

1. **Start with the decision tree** when creating tests
2. **Use appropriate templates** for each lifecycle
3. **Set realistic DELETE_AFTER dates** for scaffolding tests
4. **Document the "why"** not just the "what" in test purposes
5. **Review and clean up** scaffolding tests regularly

## 📊 Test Health Metrics

### Healthy Test Suite Indicators:

- ✅ All scaffolding tests have DELETE_AFTER dates
- ✅ No expired scaffolding tests
- ✅ Clear purpose documentation for all tests
- ✅ Appropriate lifecycle categorization
- ✅ Regular cleanup of obsolete tests

### Warning Signs:

- ⚠️ Scaffolding tests without DELETE_AFTER dates
- ⚠️ Tests older than 30 days in scaffolding/
- ⚠️ Tests with unclear or missing purpose
- ⚠️ Specification tests that test implementation details
- ⚠️ Always-passing or always-failing tests

## 🔧 Maintenance Commands

```bash
# Check for expired scaffolding tests
python tests/scripts/test_lifecycle_manager.py --expired

# Generate cleanup report
python tests/scripts/test_lifecycle_manager.py --report

# Run health check
python tests/test_runner.py --health

# Run specific lifecycle categories
python tests/test_runner.py specification regression
```

This guide ensures our test suite remains clean, purposeful, and maintainable while supporting TKA's clean architecture principles.
