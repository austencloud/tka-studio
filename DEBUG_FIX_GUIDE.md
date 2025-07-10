# VS Code Debugger Fix Guide

## The Problem
You're experiencing a `FileNotFoundError` when debugging in VS Code that points to a non-existent site-packages directory:
```
[WinError 3] The system cannot find the path specified: 'C:\Users\Austen\AppData\Roaming\Python\Python312\site-packages'
```

## The Root Cause
This happens when:
1. `"justMyCode": false` is set in your launch.json (to debug library code)
2. **"Break on Raised Exceptions"** is enabled in VS Code
3. Python's standard library raises expected exceptions during import resolution

## Solution 1: Disable "Break on Raised Exceptions" (Recommended)

### Step 1: Open the Debug Panel
- Press `Ctrl+Shift+D` to open the Run and Debug view
- Or click the Debug icon in the left sidebar

### Step 2: Find the Breakpoints Section
- In the Debug panel, look for the "BREAKPOINTS" section
- You should see checkboxes for:
  - ✅ **Raised Exceptions** ← This is causing the issue
  - ⬜ Uncaught Exceptions

### Step 3: Uncheck "Raised Exceptions"
- **Uncheck the "Raised Exceptions" checkbox**
- Keep "Uncaught Exceptions" checked if you want to catch real errors

### Step 4: Test F5 Debugging
- Press F5 to start debugging
- The debugger should now work properly with `justMyCode: false`

## Solution 2: Use "Just My Code" Mode (Alternative)

If you don't need to debug into library code:
- Select the **"🚀 TKA Launcher (Just My Code)"** configuration
- This limits debugging to your application code only
- Avoids the library exception issue entirely

## What Was Happening
- The debugger was stopping at **expected exceptions** in Python's standard library
- These exceptions are normal behavior during module import resolution
- The non-existent path is from an old Python installation or registry entry
- With "Break on Raised Exceptions" disabled, these expected exceptions are ignored

## Your Debug Configurations
You now have two options in VS Code's debug dropdown:
1. **🚀 TKA Launcher** - Full debugging with library code access
2. **🚀 TKA Launcher (Just My Code)** - Application code only

Choose the first one and disable "Break on Raised Exceptions" for the best experience.
