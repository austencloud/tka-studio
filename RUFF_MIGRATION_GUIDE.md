# TKA Performance Optimization & Ruff Migration Guide

## 🎯 What We Fixed

Your VS Code was running out of memory because it was running multiple heavy Python tools simultaneously:
- **Black** (formatter)
- **isort** (import organizer) 
- **Pylint** (linter)
- **Pyright** (type checker)

**Ruff replaces Black + isort + most of Pylint** and is **10-100x faster** with much lower memory usage.

## 📁 Files Updated

✅ **`.vscode/settings.json`** - Performance optimizations + Ruff configuration
✅ **`pyproject.toml`** - Ruff rules replacing old tool configurations  
✅ **`requirements.txt`** - Added Ruff, removed old tools
✅ **`.pre-commit-config.yaml`** - Updated hooks to use Ruff
✅ **`migrate_to_ruff.py`** - Automated migration script

## 🚀 Installation Steps

### Step 1: Install Ruff Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Ruff" by Charlie Marsh
4. Install the extension

### Step 2: Run Migration Script
```bash
# Navigate to your TKA directory
cd F:\CODE\TKA

# Run the migration script
python migrate_to_ruff.py
```

### Step 3: Restart VS Code
Close and reopen VS Code to apply all the new settings.

## 🔧 Manual Steps (if script fails)

### Install Ruff manually:
```bash
# Activate your virtual environment
.venv\Scripts\activate

# Install Ruff
pip install ruff>=0.1.0

# Remove old tools (optional, saves space)
pip uninstall black isort pylint -y
```

### Run Ruff on your codebase:
```bash
# Check for issues
ruff check .

# Auto-fix what's possible
ruff check . --fix

# Format all code
ruff format .
```

## ⚡ Performance Improvements

### Before (Memory Hogs):
- **Black**: ~100MB RAM, slow formatting
- **isort**: ~50MB RAM, slow import sorting  
- **Pylint**: ~200-500MB RAM, very slow analysis
- **Multiple file watchers**: High CPU usage

### After (Ruff):
- **Ruff**: ~20-50MB RAM total
- **10-100x faster** than the old tools
- **Single tool** handles formatting, import sorting, and linting
- **Fewer file watchers**: Lower CPU usage

### Additional VS Code Optimizations:
- Disabled heavy Python analysis features
- Excluded large directories from file watching
- Reduced TypeScript checking for web components
- Disabled auto-test discovery

## 🎨 What Ruff Does

| Old Tool | Ruff Equivalent | Speed Improvement |
|----------|----------------|-------------------|
| Black (formatting) | `ruff format` | ~10x faster |
| isort (imports) | `ruff check --select I` | ~20x faster |
| Pylint (linting) | `ruff check` | ~100x faster |

## 📋 Ruff Commands Reference

```bash
# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Format code
ruff format .

# Check specific files
ruff check src/desktop/modern/

# Show what rules are enabled
ruff linter

# Check and format in one command
ruff check . --fix && ruff format .
```

## 🔍 Troubleshooting

### If VS Code still shows errors:
1. Restart VS Code completely
2. Make sure Ruff extension is installed and enabled
3. Check that old extensions (Black, isort, Pylint) are disabled
4. Run `ruff check .` in terminal to verify Ruff is working

### If formatting doesn't work:
1. Open a Python file
2. Right-click → "Format Document"
3. Choose "Ruff" as the formatter if prompted
4. Check that `"editor.defaultFormatter": "charliermarsh.ruff"` is in settings

### If imports aren't organizing:
1. Right-click in a Python file
2. Choose "Organize Imports"
3. Or save the file (it should auto-organize)

## 🎯 Expected Results

After completing this migration:

✅ **VS Code memory usage should drop by 200-400MB**
✅ **Formatting/linting should be 10-100x faster**
✅ **No more "window terminated unexpectedly" errors**
✅ **Faster file saves and code actions**
✅ **Single tool instead of multiple conflicting tools**

## 📚 Ruff Documentation

- **Official Docs**: https://docs.astral.sh/ruff/
- **Rules Reference**: https://docs.astral.sh/ruff/rules/
- **VS Code Extension**: https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff

## 🚨 Important Notes

1. **Restart VS Code** after installation
2. **Install the Ruff extension** - it won't work without it
3. **Run `ruff format .`** initially to reformat your entire codebase
4. **Old .pylintrc files** can be deleted (rules are now in pyproject.toml)
5. **Pre-commit hooks** will now use Ruff automatically

---

*This setup should eliminate your VS Code memory issues while providing faster, more reliable code formatting and linting.*